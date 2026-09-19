# 流式接口改造：Completion Streaming → A2A v1.0 Streaming

> 本文只聚焦一件事：如果现在的 Agent 调用另一个 Agent 时走的是 Completion 流式接口（`stream: true`），改成 A2A v1.0 流式接口后，**具体要改哪些代码、每步有多难**。

---

## 1. 现在的 Completion 流式长什么样？

### 1.1 请求

```http
POST /v1/chat/completions
Authorization: Bearer {api_key}
Content-Type: application/json

{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "你是数据分析助手"},
    {"role": "user", "content": "分析 Q3 销售数据"}
  ],
  "tools": [...],
  "stream": true
}
```

### 1.2 响应（SSE）

```
data: {"choices":[{"delta":{"content":"Q3"}}]}
data: {"choices":[{"delta":{"content":"销售"}}]}
data: {"choices":[{"delta":{"content":"数据"}}]}
data: {"choices":[{"delta":{"content":"分析"}}]}
data: {"choices":[{"delta":{},"finish_reason":"stop"}]}
data: [DONE]
```

### 1.3 客户端代码通常怎么写

```python
import openai

stream = openai.chat.completions.create(
    model="gpt-4",
    messages=[...],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### 1.4 现在的核心逻辑

- 把用户请求 + 历史 messages 一次性发过去
- 服务端模型逐字生成 token
- 客户端每收到一个 chunk，把 `delta.content` 拼起来展示
- 如果模型想调用工具，会收到 `delta.tool_calls`，客户端执行工具后再发一轮

---

## 2. A2A v1.0 流式长什么样？

A2A v1.0 有两个流式入口：

| 方式 | 端点 | 用途 |
|------|------|------|
| 发消息同时流式 | `POST /message:stream` | 提交任务并立即订阅其更新 |
| 单独订阅已有任务 | `GET /tasks/{id}:subscribe` | 先创建任务，再单独订阅更新 |

### 2.1 请求（POST /message:stream）

```http
POST /message:stream
Content-Type: application/json

{
  "message": {
    "message_id": "msg-001",
    "role": "USER",
    "parts": [
      {
        "text": "分析 Q3 销售数据",
        "media_type": "text/plain"
      }
    ]
  },
  "configuration": {
    "accepted_output_modes": ["text/plain", "application/json", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
  }
}
```

### 2.2 响应（SSE）

```
event: task_status_update
data: {"task_id":"task-001","context_id":"ctx-001","status":{"state":"SUBMITTED"}}

event: task_status_update
data: {"task_id":"task-001","context_id":"ctx-001","status":{"state":"WORKING"}}

event: task_artifact_update
data: {"task_id":"task-001","context_id":"ctx-001","artifact":{"artifact_id":"art-001","name":"q3_report","parts":[{"text":"已加载销售数据..."}]}}

event: task_artifact_update
data: {"task_id":"task-001","context_id":"ctx-001","artifact":{"artifact_id":"art-001","name":"q3_report","parts":[{"data":{"total":1500000,"growth":0.15}}]}}

event: task_status_update
data: {"task_id":"task-001","context_id":"ctx-001","status":{"state":"COMPLETED"}}
```

### 2.3 A2A 流式的核心逻辑

- 发一个 `Message` 给被调 Agent
- 被调 Agent 创建 Task，进入 `SUBMITTED`
- Agent 开始干活，进入 `WORKING`
- Agent 可能随时推送 `task_artifact_update`（文本、数据、文件）
- 任务结束进入 `COMPLETED` / `FAILED` / `CANCELED`
- 如果需要用户输入，会进入 `INPUT_REQUIRED`，等用户回复后继续

---

## 3. 具体改造清单

下面按改造模块列出具体工作量和难度。

### 3.1 客户端请求构造（难度：低）

**现在：**

```python
payload = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "你是数据分析助手"},
        {"role": "user", "content": user_input}
    ],
    "stream": True
}
```

**改成 A2A：**

```python
payload = {
    "message": {
        "message_id": generate_uuid(),
        "role": "USER",
        "parts": [
            {"text": user_input, "media_type": "text/plain"}
        ]
    },
    "configuration": {
        "accepted_output_modes": ["text/plain", "application/json"]
    }
}
```

**工作量：** 1～2 小时一个调用点。

**注意点：**
- `message_id` 由客户端生成，需保证唯一
- `role` 在 v1.0 是 `USER` / `AGENT`（大写）
- `content` 要拆成 `Part`，支持 text / raw / url / data 多种形式

---

### 3.2 服务端端点改造（难度：中）

**现在：** 被调 Agent 暴露的是类似 `/v1/chat/completions` 的端点。

**改成 A2A：** 被调 Agent 需要实现：

```
POST /message:stream        # 接收消息并流式返回
POST /message:send          # 同步版本（建议一起实现）
GET  /tasks/{id}            # 查询任务状态
GET  /tasks/{id}:subscribe  # 订阅任务更新
POST /tasks/{id}:cancel     # 取消任务
```

**工作量：** 2～3 天一个 Agent（含路由 + 参数解析 + 基础错误处理）。

**注意点：**
- A2A v1.0 支持 HTTP+JSON / JSON-RPC / gRPC 三种绑定，建议先只实现 HTTP+JSON
- 必须实现 `Content-Type: text/event-stream` 的 SSE 输出
- 需要区分 `task_status_update` 和 `task_artifact_update` 两种事件

---

### 3.3 流式响应解析改造（难度：中）

**现在的解析逻辑：**

```python
for chunk in stream:
    delta = chunk.choices[0].delta
    if delta.content:
        yield delta.content
    elif delta.tool_calls:
        handle_tool_call(delta.tool_calls)
```

**A2A 的解析逻辑：**

```python
for event in sse_stream:
    if event.event == "task_status_update":
        data = json.loads(event.data)
        state = data["status"]["state"]
        if state == "COMPLETED":
            break
        elif state == "INPUT_REQUIRED":
            # 需要暂停等人输入
            handle_input_required(data)
        elif state == "FAILED":
            raise TaskFailed(data["status"]["message"])
    elif event.event == "task_artifact_update":
        data = json.loads(event.data)
        for part in data["artifact"]["parts"]:
            if "text" in part:
                yield part["text"]
            elif "data" in part:
                yield part["data"]
            elif "raw" in part:
                yield save_file(part["raw"], part["filename"])
```

**工作量：** 半天到 1 天一个消费方。

**注意点：**
- A2A 流式不是按 token 返回，而是按「任务事件」返回
- 文本内容可能在 `task_artifact_update` 里分多次推送
- 文件内容以 base64 形式在 `raw` 字段里返回

---

### 3.4 任务状态机接入（难度：中高）

**现在：** 没有任务概念，一次请求结束就释放。

**A2A 要求：** 被调 Agent 必须维护 Task 状态。

```python
class TaskStore:
    def create_task(self, context_id, message) -> Task:
        task = Task(id=generate_uuid(), context_id=context_id, status=SUBMITTED)
        self.save(task)
        return task

    def update_status(self, task_id, state, message=None):
        task = self.get(task_id)
        task.status = TaskStatus(state=state, message=message)
        self.save(task)

    def add_artifact(self, task_id, artifact):
        task = self.get(task_id)
        task.artifacts.append(artifact)
        self.save(task)
```

**工作量：**
- 内存实现：半天
- Redis / DB 持久化：2～3 天
- 加入超时、重试、幂等：1 周

**注意点：**
- Task ID 在 v1.0 由服务端生成
- `context_id` 相当于会话 ID，多轮对话要用同一个
- `INPUT_REQUIRED` 状态需要把任务挂起，等用户回复后继续

---

### 3.5 工具调用与产物返回改造（难度：中）

**现在：** 模型返回 `tool_calls`，调用方执行后把结果塞回 messages 再调一次。

```python
# 模型说：我要调用 get_sales_data
# 调用方执行工具
result = get_sales_data(quarter="Q3")

# 把结果塞回 messages
messages.append({"role": "tool", "tool_call_id": "...", "content": result})

# 再调一次模型
stream = openai.chat.completions.create(messages=messages, stream=True)
```

**A2A：** 被调 Agent 内部自己执行工具，把结果包装成 Artifact 推送。

```python
# 在被调 Agent 内部
async def run_task(task_id):
    update_status(task_id, WORKING)

    data = get_sales_data(quarter="Q3")
    push_artifact(task_id, Artifact(
        name="raw_data",
        parts=[Part(data=data, media_type="application/json")]
    ))

    report = generate_report(data)
    push_artifact(task_id, Artifact(
        name="report",
        parts=[Part(text=report, media_type="text/plain")]
    ))

    update_status(task_id, COMPLETED)
```

**工作量：** 2～3 天一个 Agent（如果工具链已经成熟，只是换返回形式）。

**注意点：**
- 工具执行从「调用方负责」变成「被调 Agent 负责」
- 工具执行结果要通过 `task_artifact_update` 事件推送
- 如果执行时间长，要保持在 `WORKING` 状态并定期发送心跳更新

---

### 3.6 错误处理改造（难度：中）

**现在：** 看 HTTP 状态码 + `error` JSON。

```python
try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
except HTTPError as e:
    print(e.response.json()["error"]["message"])
```

**A2A：** 错误体现在 Task 状态里。

```python
for event in sse_stream:
    if event.event == "task_status_update":
        data = json.loads(event.data)
        state = data["status"]["state"]
        if state == "FAILED":
            error_msg = data["status"]["message"]["parts"][0]["text"]
            raise TaskFailed(error_msg)
        elif state == "REJECTED":
            raise TaskRejected()
```

**工作量：** 半天。

**注意点：**
- A2A 的 `FAILED` 状态可能包含结构化错误信息
- 网络层错误和任务层错误要分开处理
- `CANCELED` 和 `REJECTED` 语义不同：一个是外部取消，一个是 Agent 拒绝执行

---

### 3.7 取消任务支持（难度：低）

**现在：** 客户端直接断开 SSE 连接即可。

**A2A：** 建议显式调用取消。

```http
POST /tasks/{task_id}:cancel
```

**工作量：** 半天到 1 天。

**注意点：**
- 取消后任务状态变为 `CANCELED`
- 服务端需要能优雅中断正在执行的工具链
- 取消后不要再推送后续 artifact

---

## 4. 改造工作量汇总

| 模块 | 难度 | 工作量 | 说明 |
|------|------|--------|------|
| 客户端请求构造 | 低 | 1～2 小时/调用点 | messages → Message + Part |
| 服务端端点实现 | 中 | 2～3 天/Agent | message:stream / message:send / tasks 接口 |
| 流式响应解析 | 中 | 半天～1 天/消费方 | token delta → task events |
| 任务状态机 | 中高 | 2 天～1 周 | Task 持久化 + 生命周期管理 |
| 工具调用与产物返回 | 中 | 2～3 天/Agent | 工具在 Agent 内部执行并推送 Artifact |
| 错误处理 | 中 | 半天 | HTTP 错误 → Task 状态错误 |
| 取消任务 | 低 | 半天～1 天 | 新增 cancel 端点 |

**总估算（单个 Agent 对）：**
- 最小改造（内存状态、简单文本输出）：3～5 天
- 完整改造（持久化、文件产物、错误恢复）：1.5～2 周

---

## 5. 最容易踩的坑

### 5.1 以为 A2A 流式也是按 token 返回

**坑：** 把 A2A 的 `task_artifact_update` 当成 Completion 的 `delta.content` 来解析。

**实际情况：** A2A 推送的是「任务产物」，可能一次性推送一段话、一个 JSON、一个文件。不要期望它是逐字的。

### 5.2 忽略 `INPUT_REQUIRED` 状态

**坑：** 任务走着走着停了，以为失败了。

**实际情况：** Agent 可能在等人确认或补充信息，状态是 `INPUT_REQUIRED`。需要把问题展示给用户，用户回复后再通过 `message:send` 继续。

### 5.3 客户端自己生成 Task ID

**坑：** 还按旧版习惯让客户端生成 task id。

**实际情况：** v1.0 里 Task ID 由服务端生成，客户端在第一次响应后才能拿到。

### 5.4 把文件内容直接放在 text 里

**坑：** 文件内容用 `Part.text` 传。

**实际情况：** 文件应该用 `Part.raw`（base64）或 `Part.url`，并设置正确的 `media_type`。

### 5.5 忘记处理 `context_id`

**坑：** 每轮对话都创建新 Task，没有上下文。

**实际情况：** 多轮对话要在同一个 `context_id` 下创建/关联 Task，被调 Agent 通过 `context_id` 维护会话历史。

---

## 6. 最小可运行改造方案

如果只想先跑通一条链路，建议按这个顺序：

1. **被调 Agent 实现 `POST /message:stream`**
   - 接收 Message
   - 创建 Task，返回 `SUBMITTED`
   - 进入 `WORKING`
   - 执行原有逻辑
   - 把最终结果包装成 Artifact 推送
   - 更新为 `COMPLETED`

2. **调用方把 `openai.chat.completions.create` 换成 A2A SSE 客户端**
   - 构造 Message + Part
   - 解析 `task_status_update` / `task_artifact_update`
   - 把 `text` part 输出到前端

3. **加 Task 状态存储**
   - 先用内存字典，跑通后再换 Redis/DB

4. **补同步接口 `POST /message:send`、查询接口 `GET /tasks/{id}`、取消接口 `POST /tasks/{id}:cancel`**

5. **处理 `INPUT_REQUIRED` 等多状态**
   - 等主链路稳定后再做

---

## 7. 一句话总结

Completion 流式是「模型逐字吐结果」，A2A v1.0 流式是「Agent 按任务阶段汇报进度和产物」。

改造的核心不是把 SSE 格式换一换，而是**把调用逻辑从『请求-生成-结束』变成『创建任务-跟踪状态-接收产物-处理中断』**。
