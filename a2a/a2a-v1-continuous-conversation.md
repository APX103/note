> 一句话结论：A2A v1.0 的连续会话不是强制绑定在同一个 Task 里，而是通过 `context_id` 把多个 Task 串成一个会话上下文。同一个 Task 内只能通过 `INPUT_REQUIRED` 状态实现一次「中断-继续」。

# A2A v1.0 连续会话实现方式

## 1. 核心概念：context_id vs. task_id

A2A v1.0 里有两个关键 ID：

| ID | 含义 | 生命周期 |
|----|------|----------|
| `task_id` | 一个具体任务的 ID | 从创建到 `COMPLETED` / `FAILED` / `CANCELED` / `REJECTED` 结束 |
| `context_id` | 会话上下文的 ID | 可以跨越多个 Task，代表一段连续的对话 |

从 protobuf 注释看：

```protobuf
message Task {
  string id = 1;              // Task ID，服务端生成
  string context_id = 2;      // 交互上下文集合（tasks and messages）
  TaskStatus status = 3;
  repeated Artifact artifacts = 4;
  repeated Message history = 5;
}

message Message {
  string message_id = 1;
  string context_id = 2;      // 所属会话上下文
  string task_id = 3;         // 所属 Task（可选）
  Role role = 4;
  repeated Part parts = 5;
}
```

`context_id` 才是 A2A 里「连续会话」的载体，不是 `task_id`。

---

## 2. 连续会话的两种实现模式

### 模式一：同一个 Task 内中断-继续（适合单轮交互中的确认/补充）

当 Agent 执行任务时，发现缺少信息，可以把 Task 状态改为 `INPUT_REQUIRED`，然后等用户回复。**用户回复后，同一个 Task 继续执行**。

流程：

```
USER: 分析 Q3 销售数据
      ↓
Task-001: SUBMITTED → WORKING → INPUT_REQUIRED
      ↓
AGENT: "我需要确认，你要按大区还是按产品线分析？"
      ↓
USER: 按大区
      ↓
Task-001: WORKING → COMPLETED
```

**用户回复时的请求：**

```http
POST /message:send

{
  "message": {
    "message_id": "msg-002",
    "role": "USER",
    "context_id": "ctx-001",
    "task_id": "task-001",
    "parts": [
      {"text": "按大区", "media_type": "text/plain"}
    ]
  }
}
```

**关键点：**
- 必须带上 `task_id: "task-001"`
- 必须带上 `context_id: "ctx-001"`
- Agent 收到后把 Task 从 `INPUT_REQUIRED` 改回 `WORKING`，继续执行

**适用场景：**
- 任务执行到一半需要补充信息
- 单次对话内的确认、澄清、选择

**不适用场景：**
- 用户隔了很久才回复
- 需要保存多个独立的对话轮次
- 任务已经 `COMPLETED` 后还想继续聊

---

### 模式二：跨 Task 的连续会话（推荐的标准做法）

更常见的连续会话是：**每一轮用户请求创建一个新 Task，但这些 Task 共享同一个 `context_id`**。被调 Agent 通过 `context_id` 读取历史交互，保持上下文。

流程：

```
Round 1:
  USER: 分析 Q3 销售数据
  Task-001 (ctx-001): SUBMITTED → WORKING → COMPLETED
  AGENT: 返回 Q3 报告

Round 2:
  USER: 那 Q2 呢？
  Task-002 (ctx-001): SUBMITTED → WORKING → COMPLETED
  AGENT: 返回 Q2 报告（知道用户在问同一个数据维度）

Round 3:
  USER: 把这两个季度对比下
  Task-003 (ctx-001): SUBMITTED → WORKING → COMPLETED
  AGENT: 返回 Q2 vs Q3 对比
```

**第二轮请求：**

```http
POST /message:stream

{
  "message": {
    "message_id": "msg-003",
    "role": "USER",
    "context_id": "ctx-001",
    "parts": [
      {"text": "那 Q2 呢？", "media_type": "text/plain"}
    ]
  }
}
```

**关键点：**
- 不带 `task_id`，让服务端创建新 Task
- 带上 `context_id: "ctx-001"`，表示这是同一会话
- 服务端根据 `context_id` 查询该会话下的历史 Tasks/Messages

**适用场景：**
- 正常的多轮对话
- 每次用户发言都是一个独立任务，但要有上下文记忆
- 任务已经结束后还想继续聊

---

## 3. 服务端怎么维护 context 历史？

A2A v1.0 只定义了 `context_id` 是上下文集合，具体怎么存储和查询由实现决定。常见做法：

### 方案 A：Task 自带 history（简单）

每个 Task 的 `history` 字段保存自己的交互记录。服务端通过 `context_id` 查询该 context 下的所有 Task，再聚合 history。

```python
def get_context_history(context_id, limit=10):
    tasks = task_store.list_by_context(context_id)
    messages = []
    for task in tasks:
        messages.extend(task.history)
    return messages[-limit:]
```

**优点：** 简单，直接复用 Task.history
**缺点：** 历史分散在多个 Task 里，查询效率低；需要决定聚合策略

### 方案 B：独立的 Context 存储（推荐）

单独维护一个 Context 表/Key，保存该会话下所有的 Messages。

```python
class ContextStore:
    def add_message(self, context_id, message):
        self.contexts[context_id].append(message)

    def get_messages(self, context_id, limit=20):
        return self.contexts[context_id][-limit:]
```

每个 Task 创建时，从 Context 存储读取历史作为 prompt 上下文。

**优点：** 查询高效，容易控制上下文长度
**缺点：** 需要额外存储层

### 方案 C：只保留最近 N 个 Tasks 的 artifacts（产物驱动）

有些 Agent 的执行不需要完整 message 历史，只需要之前 Task 的产物。服务端可以只保留最近几个 Task 的 `artifacts`。

```python
def get_context_artifacts(context_id, limit=3):
    tasks = task_store.list_by_context(context_id, limit=limit)
    artifacts = []
    for task in tasks:
        artifacts.extend(task.artifacts)
    return artifacts
```

**适用场景：** 数据分析、报告生成等产物型任务

---

## 4. 请求时的选择：带不带 task_id？

| 场景 | 是否带 task_id | 是否带 context_id | 结果 |
|------|---------------|------------------|------|
| 开启全新对话 | 不带 | 不带（服务端生成新 context） | 创建新 context + 新 Task |
| 继续同一会话，发起新任务 | 不带 | 带 | 同一 context 下的新 Task |
| 回复当前挂起的任务 | 带 | 带 | 同一个 Task 继续 |
| 只带 task_id，不带 context_id | 带 | 不带 | 服务端从 task_id 推断 context_id |

---

## 5. 流式场景下的连续会话

如果是 `POST /message:stream`，连续会话的处理逻辑：

```python
# 第一轮
response = client.post("/message:stream", json={
    "message": {
        "message_id": "msg-001",
        "role": "USER",
        "parts": [{"text": "分析 Q3 销售数据"}]
    }
})
# 从 SSE 中提取 context_id 和 task_id
context_id = extract_context_id(response)

# 第二轮
response = client.post("/message:stream", json={
    "message": {
        "message_id": "msg-002",
        "role": "USER",
        "context_id": context_id,  # 带上同一个 context
        "parts": [{"text": "那 Q2 呢？"}]
    }
})
```

**注意：** 第一轮响应里的 `task_status_update` 会带 `context_id`，客户端要保存下来。

---

## 6. 与 Completion 的对比

| 模式 | Completion 接口 | A2A v1.0 |
|------|----------------|----------|
| 上下文维护 | 客户端每次发送完整 `messages` | 服务端通过 `context_id` 维护 |
| 一轮交互 | 一次请求 | 一个 Task |
| 多轮对话 | 客户端拼 messages | 同一 `context_id` 下多个 Task |
| 中断等人 | 不支持（或靠客户端逻辑） | `INPUT_REQUIRED` 原生支持 |
| 恢复方式 | 继续发完整 messages | 回复到同一个 Task 或开新 Task |

---

## 7. 实践建议

1. **优先用模式二（跨 Task 连续会话）**
   - 更符合人类对话习惯
   - 每个 Task 职责清晰，便于调试和审计
   - 任务结束后不阻塞 context

2. **模式一只用于必要的单任务中断**
   - 比如需要用户确认参数、补充文件
   - 不要滥用，否则 Task 生命周期会拖得很长

3. **服务端实现 Context 存储**
   - 建议独立存储 context messages，不要每次都扫描所有 Tasks
   - 设置上下文长度限制，避免 token 爆炸

4. **返回 context_id 给客户端**
   - 第一次交互的响应里，客户端要保存 `context_id`
   - 后续请求都带上它

---

## 8. 一句话总结

A2A v1.0 的连续会话靠 `context_id` 实现。**每一轮用户请求通常是一个新 Task，同一个 `context_id` 把这些 Task 串成一段有上下文的对话**。同一个 Task 内只能通过 `INPUT_REQUIRED` 实现「中断-继续」，任务一旦 `COMPLETED` 就不能再续。
