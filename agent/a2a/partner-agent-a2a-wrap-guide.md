> 目标：让已有 Completion 接口的合作方 Agent，**只新增一个 A2A 模块**，不改原有接口和业务代码，就能被主 Agent 通过 A2A 调用。

# 合作方 Agent A2A 封装指南（最小化改造）

## 1. 核心原则：只新增，不修改

你们的现有系统长这样：

```
调用方 ──HTTP──> 合作方 Agent 的 /v1/chat/completions ──> 原有业务逻辑
```

改造后变成这样：

```
调用方 ──A2A──> 新增 A2A 模块 ──Completion──> 原有 /v1/chat/completions ──> 原有业务逻辑
              (HTTP+JSON/SSE)
```

**原有 `/v1/chat/completions` 接口不改、原有业务逻辑不改、原有数据库不改。**

只新增一个 A2A 接入层模块，把外部 A2A 请求翻译成内部 Completion 调用。

---

## 2. 最重要的约定：必须正确处理 `context_id`

A2A v1.0 里，`context_id` 是连续会话的核心标识。**调用方会在同一个 `context_id` 下多次请求你们**，所以你们必须：

1. **保存 `context_id` 对应的历史消息**
2. **同一个 `context_id` 的请求，要把历史消息一起传给 Completion 接口**
3. **如果请求没带 `context_id`，你们生成一个新的返回**

简单说：`context_id` 就是你们的「记忆钥匙」。同一个 `context_id` 下的多次调用，应该被当成同一段对话。

### 示例

```text
Round 1:
  调用方 -> 你们: context_id=ctx-001, "分析 Q3 销售数据"
  你们 -> 调用方: task_id=task-001, context_id=ctx-001, "Q3 销售额增长 15%"

Round 2:
  调用方 -> 你们: context_id=ctx-001, "那 Q2 呢？"
  你们应该能知道：用户是在问销售数据，返回 Q2 的分析

Round 3:
  调用方 -> 你们: context_id=ctx-001, "把这两个季度对比下"
  你们应该能结合 Q2 和 Q3 的数据给出对比
```

如果 Round 2 和 Round 3 不带 `ctx-001`，调用方会当成新会话，你们的回复也会失去上下文。

### 实现要点

- 请求带了 `context_id`：查历史，追加当前消息，一起传给 Completion
- 请求没带 `context_id`：生成新的 `context_id`，在第一次 `task_status_update` 里返回
- 助手回复也要保存到该 `context_id` 的历史中
- 注意控制历史长度，避免超过 Completion 的上下文限制

---

## 3. 新增模块要暴露哪些接口？

只需要 4 个接口就能跑通：

| 接口 | 方法 | 作用 |
|------|------|------|
| `/agent-card.json` | GET | 告诉外部：我是谁、我能做什么 |
| `/message:send` | POST | 同步处理任务 |
| `/message:stream` | POST | 流式处理任务（推荐） |
| `/tasks/{id}` | GET | 查询任务状态 |

可选（按需实现）：

| 接口 | 方法 | 作用 |
|------|------|------|
| `/tasks/{id}:subscribe` | GET | 单独订阅任务更新 |
| `/tasks/{id}:cancel` | POST | 取消任务 |

---

## 4. 新增模块内部结构

```
新增 A2A 模块
├── HTTP 路由层           # 接收 /agent-card.json、/message:*、/tasks/*
├── A2A 协议解析层        # 解析 Message、Part、Configuration
├── Task 管理器           # 创建 Task、更新状态、维护生命周期
├── Context 存储          # 按 context_id 保存历史消息
├── Completion 调用客户端  # 调用你们原有的 /v1/chat/completions
└── SSE 推送器            # 把 Task 状态/产物推给外部
```

**和原有系统的关系：**
- A2A 模块是新增的一个独立 HTTP 服务，或者原有服务里的一个新路由组
- A2A 模块唯一依赖原有系统的地方：调用 `/v1/chat/completions`
- 不读写原有数据库，不改动原有代码

---

## 5. 最小实现流程

### 步骤 1：实现 /agent-card.json

返回一个 JSON，描述 Agent 能力：

```json
{
  "name": "销售数据分析 Agent",
  "description": "分析销售数据并生成报告",
  "version": "1.0.0",
  "supported_interfaces": [
    {
      "url": "https://your-agent.example.com/a2a/v1",
      "protocol_binding": "HTTP+JSON",
      "protocol_version": "1.0"
    }
  ],
  "capabilities": {
    "streaming": true,
    "push_notifications": false
  },
  "skills": [
    {
      "id": "sales-analysis",
      "name": "销售数据分析",
      "description": "按季度、大区、产品线分析销售数据",
      "tags": ["sales", "data", "report"],
      "input_modes": ["text/plain"],
      "output_modes": ["text/plain", "application/json"]
    }
  ]
}
```

### 步骤 2：实现 /message:stream

这是最重要的接口。外部会通过 SSE 方式调用。

#### 2.1 接收的请求

```json
{
  "message": {
    "message_id": "msg-001",
    "role": "USER",
    "context_id": "ctx-001",
    "parts": [
      {
        "text": "分析 Q3 销售数据",
        "media_type": "text/plain"
      }
    ]
  },
  "configuration": {
    "accepted_output_modes": ["text/plain", "application/json"]
  }
}
```

#### 2.2 处理流程

```
1. 生成 task_id
2. 记录 context_id（如果没有就新建）
3. 推送 task_status_update: SUBMITTED
4. 推送 task_status_update: WORKING
5. 把 A2A Message 转成 Completion messages
6. 调用内部 /v1/chat/completions?stream=true
7. 每收到一个 delta.content，推送 task_artifact_update
8. 流结束，推送 task_status_update: COMPLETED
```

#### 2.3 返回的 SSE

```
event: task_status_update
data: {"task_id":"task-001","context_id":"ctx-001","status":{"state":"SUBMITTED"}}

event: task_status_update
data: {"task_id":"task-001","context_id":"ctx-001","status":{"state":"WORKING"}}

event: task_artifact_update
data: {"task_id":"task-001","context_id":"ctx-001","artifact":{"artifact_id":"art-001","name":"result","parts":[{"text":"Q3","media_type":"text/plain"}]}}

event: task_artifact_update
data: {"task_id":"task-001","context_id":"ctx-001","artifact":{"artifact_id":"art-001","name":"result","parts":[{"text":" 销售额同比增长 15%","media_type":"text/plain"}]}}

event: task_status_update
data: {"task_id":"task-001","context_id":"ctx-001","status":{"state":"COMPLETED"}}
```

### 步骤 3：实现 /tasks/{id}

返回指定 Task 的当前状态：

```json
{
  "id": "task-001",
  "context_id": "ctx-001",
  "status": {
    "state": "COMPLETED"
  },
  "artifacts": [
    {
      "artifact_id": "art-001",
      "name": "result",
      "parts": [
        {"text": "Q3 销售额同比增长 15%", "media_type": "text/plain"}
      ]
    }
  ]
}
```

### 步骤 4：实现 /message:send（同步版）

和 `/message:stream` 逻辑一样，但等到 Task 完成后再一次性返回 Task 结果。

---

## 6. 代码示例（Python Flask 版）

下面是一个最小可运行的示例，展示新增 A2A 模块怎么包原有 Completion 接口。

```python
import uuid
import json
import requests
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

# 内存存储，生产环境请换 Redis/DB
TASKS = {}
CONTEXTS = {}

# 你们原有的 Completion 接口地址
COMPLETION_URL = "http://localhost:8000/v1/chat/completions"
API_KEY = "your-key"


@app.route("/agent-card.json", methods=["GET"])
def agent_card():
    return jsonify({
        "name": "销售数据分析 Agent",
        "description": "分析销售数据并生成报告",
        "version": "1.0.0",
        "supported_interfaces": [
            {
                "url": "https://your-agent.example.com/a2a/v1",
                "protocol_binding": "HTTP+JSON",
                "protocol_version": "1.0"
            }
        ],
        "capabilities": {"streaming": True},
        "skills": [
            {
                "id": "sales-analysis",
                "name": "销售数据分析",
                "description": "按季度分析销售数据",
                "tags": ["sales", "data"],
                "input_modes": ["text/plain"],
                "output_modes": ["text/plain", "application/json"]
            }
        ]
    })


def build_messages(context_id, message):
    """把 A2A Message 转成 Completion messages，并保留上下文"""
    if context_id not in CONTEXTS:
        CONTEXTS[context_id] = []

    # 提取当前消息文本
    text_parts = [p.get("text", "") for p in message.get("parts", []) if "text" in p]
    user_text = " ".join(text_parts)

    # 保存到上下文
    CONTEXTS[context_id].append({"role": "user", "content": user_text})

    return CONTEXTS[context_id]


def save_assistant_message(context_id, content):
    """保存助手回复到上下文"""
    CONTEXTS[context_id].append({"role": "assistant", "content": content})


def sse_event(event_type, data):
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


@app.route("/message:stream", methods=["POST"])
def message_stream():
    body = request.json
    message = body.get("message", {})
    context_id = message.get("context_id") or str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # 创建 Task
    TASKS[task_id] = {
        "id": task_id,
        "context_id": context_id,
        "status": "SUBMITTED",
        "artifacts": []
    }

    def generate():
        # SUBMITTED
        yield sse_event("task_status_update", {
            "task_id": task_id,
            "context_id": context_id,
            "status": {"state": "SUBMITTED"}
        })

        # WORKING
        TASKS[task_id]["status"] = "WORKING"
        yield sse_event("task_status_update", {
            "task_id": task_id,
            "context_id": context_id,
            "status": {"state": "WORKING"}
        })

        # 调用内部 Completion
        messages = build_messages(context_id, message)
        resp = requests.post(
            COMPLETION_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "gpt-4", "messages": messages, "stream": True},
            stream=True
        )

        full_content = ""
        artifact_id = f"art-{task_id}"

        for line in resp.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            if not line.startswith("data: "):
                continue
            data = line[6:]
            if data == "[DONE]":
                break

            chunk = json.loads(data)
            content = chunk["choices"][0]["delta"].get("content", "")
            if not content:
                continue

            full_content += content

            # 推送 artifact update
            yield sse_event("task_artifact_update", {
                "task_id": task_id,
                "context_id": context_id,
                "artifact": {
                    "artifact_id": artifact_id,
                    "name": "result",
                    "parts": [{"text": content, "media_type": "text/plain"}]
                }
            })

        # 保存助手回复到上下文
        save_assistant_message(context_id, full_content)

        # COMPLETED
        TASKS[task_id]["status"] = "COMPLETED"
        yield sse_event("task_status_update", {
            "task_id": task_id,
            "context_id": context_id,
            "status": {"state": "COMPLETED"}
        })

    return Response(generate(), mimetype="text/event-stream")


@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = TASKS.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

**这个示例展示了：**
- 原有 `/v1/chat/completions` 完全不动
- 新增 `/agent-card.json`、`/message:stream`、`/tasks/{id}`
- A2A 模块只负责协议转换和状态维护
- `context_id` 用于保存上下文历史

---

## 7. 关于 context_id 的处理

### 6.1 请求带了 context_id

说明是连续会话。你要：
- 用这个 `context_id` 查历史消息
- 把当前用户消息追加进去
- 一起传给 Completion 接口

### 6.2 请求没带 context_id

说明是新会话。你要：
- 生成一个新的 `context_id`
- 在第一次 `task_status_update` 里返回给外部
- 外部会保存这个 `context_id`，后续请求带上

### 6.3 上下文长度控制

Completion 接口对 `messages` 长度有限制，建议：
- 保留最近 10-20 轮对话
- 或者按 token 数截断
- 不要让历史无限增长

---

## 8. 最小改造 checklist

- [ ] 新增一个 HTTP 服务/路由组，不改动原有 Completion 服务
- [ ] 实现 `GET /agent-card.json`
- [ ] 实现 `POST /message:stream`（SSE 返回 Task 事件）
- [ ] 实现 `GET /tasks/{id}`
- [ ] 实现 `context_id` 历史消息维护
- [ ] Task 状态至少支持 `SUBMITTED`、`WORKING`、`COMPLETED`、`FAILED`
- [ ] 返回的 `task_status_update` 必须带 `task_id` 和 `context_id`

---

## 9. 常见问答

**Q：需要改动原有的 `/v1/chat/completions` 吗？**
A：不需要。A2A 模块只是它的调用方。

**Q：需要改动原有业务逻辑吗？**
A：不需要。A2A 模块只负责协议翻译。

**Q：A2A 模块必须和原服务部署在一起吗？**
A：不一定。可以是一个独立服务，也可以是一个 Sidecar。只要它能访问到原 Completion 接口即可。

**Q：如果原 Completion 接口不支持 SSE，A2A 还能流式吗？**
A：可以。A2A 的流式不要求原接口必须流式。即使原接口是同步返回完整结果，A2A 模块也可以把完整结果一次性作为 `task_artifact_update` 推送，只是流式体验弱一些。

**Q：需要支持 `INPUT_REQUIRED` 吗？**
A：如果你们的 Agent 会主动问用户问题，就支持；否则可以先不做。Completion 接口本身没有原生 `INPUT_REQUIRED`，要模拟的话需要额外约定。

---

## 10. 一句话总结

**只新增一个 A2A 接入模块，把外部 A2A 请求翻译成内部 Completion 调用，原有接口和业务逻辑完全不动。**
