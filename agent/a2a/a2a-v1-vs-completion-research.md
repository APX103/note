# A2A v1.0 与最新 LLM Completion 接口对比调研

> 调研范围：A2A v1.0 正式规范（2026 年 4 月发布，Linux Foundation 治理） vs. OpenAI Chat Completions API / Responses API（2025-2026 最新版本）。
>
> 核心结论：A2A v1.0 和 OpenAI Responses API 都在往「有状态、任务化、Agent 原生」方向演进，但 A2A 是跨 Agent 协作协议，OpenAI API 是单一模型服务接口。

---

## 1. A2A v1.0 关键变化（与旧版草案对比）

A2A 从早期草案进入 v1.0 后，规范化和协议绑定更加严格：

| 变化项 | 旧版草案（v0.x） | A2A v1.0 |
|--------|------------------|----------|
| 规范事实源 | JSON Schema / Pydantic | `a2a.proto`（Protobuf） |
| 发送消息 | `tasks/send` | `POST /message:send` |
| 流式发送 | `tasks/sendSubscribe` | `POST /message:stream` |
| 任务 ID | 客户端可生成 | 服务端生成 |
| 协议绑定 | JSON-RPC over HTTP 为主 | JSON-RPC / gRPC / HTTP+JSON 三种绑定 |
| Agent Card | `agent.json` | `agent-card.json`，支持签名 |
| 传输接口 | 单一 URL | `supported_interfaces` 多接口声明 |

> 参考：[A2A v1.0 Core Specification](https://agent2agent.info/specification/core/)、[a2a.proto](https://raw.githubusercontent.com/a2aproject/A2A/main/specification/a2a.proto)

---

## 2. A2A v1.0 核心数据模型

A2A v1.0 的核心实体基于 Protobuf 定义：

### 2.1 AgentCard（Agent 名片）

Agent 通过 `agent-card.json` 自描述能力：

```json
{
  "name": "Data Analysis Agent",
  "description": "Analyzes sales data and generates reports",
  "version": "1.0.0",
  "supported_interfaces": [
    {
      "url": "https://agent.example.com/a2a/v1",
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
      "name": "Sales Analysis",
      "description": "Analyzes quarterly sales data",
      "tags": ["data", "sales", "report"]
    }
  ]
}
```

### 2.2 Task（任务）

`Task` 是 A2A 的核心工作单元：

```protobuf
message Task {
  string id = 1;              // 服务端生成
  string context_id = 2;      // 会话上下文 ID
  TaskStatus status = 3;      // 当前状态
  repeated Artifact artifacts = 4;  // 输出产物
  repeated Message history = 5;     // 交互历史
  google.protobuf.Struct metadata = 6;
}
```

### 2.3 TaskState（任务生命周期）

```
SUBMITTED → WORKING → COMPLETED
                 ↘ FAILED
                 ↘ CANCELED
                 ↘ REJECTED
                 ↘ INPUT_REQUIRED  （中断态，等用户输入）
                 ↘ AUTH_REQUIRED   （中断态，等认证）
```

### 2.4 Message / Part

`Message` 是通信单元，`Part` 是内容片段：

```protobuf
message Message {
  string message_id = 1;
  string context_id = 2;
  string task_id = 3;
  Role role = 4;            // USER 或 AGENT
  repeated Part parts = 5;
}

message Part {
  oneof content {
    string text = 1;        // 文本
    bytes raw = 2;          // 文件（base64）
    string url = 3;         // 文件 URL
    google.protobuf.Value data = 4;  // 结构化数据
  }
  string filename = 6;
  string media_type = 7;    // MIME type
}
```

### 2.5 Artifact（产物）

```protobuf
message Artifact {
  string artifact_id = 1;
  string name = 2;
  string description = 3;
  repeated Part parts = 4;  // 多模态输出
}
```

---

## 3. A2A v1.0 接口清单

| RPC 方法 | HTTP 绑定 | 作用 |
|----------|-----------|------|
| `SendMessage` | `POST /message:send` | 发送消息，创建/更新任务 |
| `SendStreamingMessage` | `POST /message:stream` | 流式发送消息，实时返回任务更新 |
| `GetTask` | `GET /tasks/{id}` | 查询任务最新状态 |
| `ListTasks` | `GET /tasks` | 列出任务 |
| `CancelTask` | `POST /tasks/{id}:cancel` | 取消任务 |
| `SubscribeToTask` | `GET /tasks/{id}:subscribe` | 订阅指定任务的更新 |
| `GetExtendedAgentCard` | `GET /extendedAgentCard` | 获取认证后的 Agent 详情 |

---

## 4. OpenAI 最新 Completion 接口

### 4.1 Chat Completions API（仍支持，但非首推）

```http
POST /v1/chat/completions

{
  "model": "gpt-5.6",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "分析 Q3 销售数据"}
  ],
  "tools": [...],
  "stream": false
}
```

返回：

```json
{
  "id": "chatcmpl-xxx",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "Q3 销售额..."
    }
  }]
}
```

特点：
- 无状态，每次请求需携带完整 `messages`
- 返回 `choices[0].message.content` 或 `tool_calls`
- 工具执行由调用方负责
- 流式返回 `delta` token

### 4.2 Responses API（OpenAI 当前推荐）

OpenAI 在 2025 年推出 Responses API，作为 Chat Completions 的演进，官方明确「推荐所有新项目使用」。

```http
POST /v1/responses

{
  "model": "gpt-5.6",
  "input": "分析 Q3 销售数据",
  "instructions": "你是数据分析助手",
  "tools": [
    {"type": "web_search"},
    {"type": "code_interpreter"}
  ],
  "store": true
}
```

返回：

```json
{
  "id": "resp_xxx",
  "object": "response",
  "output": [
    {
      "type": "reasoning",
      "id": "rs_xxx",
      "summary": []
    },
    {
      "type": "message",
      "id": "msg_xxx",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Q3 销售额..."
        }
      ]
    }
  ]
}
```

Responses API 相比 Chat Completions 的关键变化：

| 能力 | Chat Completions | Responses API |
|------|------------------|---------------|
| 状态管理 | 无状态，手动维护 messages | `store: true` 自动维护，支持 `previous_response_id` |
| 输出结构 | `choices[].message` | `output[]` 数组，按 Item 类型区分 |
| 内置工具 | 需自己实现 | 原生支持 web_search、file_search、code_interpreter、computer use、MCP 等 |
| 函数调用 | `tools` 外部标签结构 | `tools` 内部标签结构，默认尝试 strict mode |
| 结构化输出 | `response_format` | `text.format` |
| 流式 | `delta` token chunk | 按类型分事件：`response.output_text.delta`、`response.function_call_arguments.done` 等 |
| 缓存效率 | 较低 | 官方称提升 40%-80% |

> 参考：[Migrate to the Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses)

---

## 5. A2A v1.0 vs. OpenAI Completion 接口对比

### 5.1 抽象层级对比

| 维度 | A2A v1.0 | OpenAI Chat Completions | OpenAI Responses API |
|------|----------|------------------------|---------------------|
| 协议层级 | Agent 间协作协议（应用层） | 模型推理 API | 模型推理 API（Agent 增强版） |
| 调用对象 | 另一个 Agent | 大语言模型 | 大语言模型 |
| 核心交互单元 | Task | Message | Response / Item |
| 状态管理 | 被调 Agent 维护 Task 状态 | 调用方维护 messages | OpenAI 维护（store=true） |
| 输出形式 | Artifact（文件/数据/文本） | 文本 / tool_calls | Items（message/reasoning/function_call 等） |
| 发现机制 | AgentCard | 无 | 无 |
| 多 Agent 协作 | 原生支持 | 不支持 | 不支持 |
| 异步长任务 | 原生支持 | 不支持 | 部分支持（background mode） |

### 5.2 接口形态对比

| 场景 | A2A v1.0 | OpenAI Responses API |
|------|----------|---------------------|
| 发送请求 | `POST /message:send` | `POST /v1/responses` |
| 流式请求 | `POST /message:stream` | `POST /v1/responses` + streaming |
| 查状态 | `GET /tasks/{id}` | 通过 `previous_response_id` 链式查询 |
| 取消任务 | `POST /tasks/{id}:cancel` | 无直接对应 |
| 订阅更新 | `GET /tasks/{id}:subscribe` | SSE 流事件 |

### 5.3 输出内容对比

**A2A v1.0 返回 Artifact：**

```json
{
  "id": "task-001",
  "status": {"state": "COMPLETED"},
  "artifacts": [
    {
      "artifact_id": "art-001",
      "name": "q3_report",
      "parts": [
        {
          "data": {"total": 1500000, "growth": 0.15}
        },
        {
          "raw": "base64...",
          "filename": "q3_report.xlsx",
          "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }
      ]
    }
  ]
}
```

**OpenAI Responses API 返回 Items：**

```json
{
  "id": "resp_xxx",
  "output": [
    {"type": "reasoning", "summary": [...]},
    {
      "type": "message",
      "content": [{"type": "output_text", "text": "Q3 销售额..."}]
    }
  ]
}
```

关键差异：
- A2A 的 `Artifact` 明确承载任务产物，支持文件、数据、URL 等多模态形式
- Responses API 的 `output` 是模型产生的 Items，文件产物通常通过 tool/function call 间接产生

---

## 6. 流式机制对比

### 6.1 A2A v1.0 流式

通过 `SendStreamingMessage`（`POST /message:stream`）或 `SubscribeToTask`（`GET /tasks/{id}:subscribe`）实现。

SSE 事件类型：

```
event: task_status_update
data: {"task_id":"task-001","status":{"state":"WORKING"}}

event: task_artifact_update
data: {"task_id":"task-001","artifact":{"artifact_id":"art-001","parts":[...]}}

event: task_status_update
data: {"task_id":"task-001","status":{"state":"COMPLETED"}}
```

流式内容：**任务状态和产物更新**。

### 6.2 OpenAI Responses API 流式

SSE 事件按类型分发：

```
event: response.created
event: response.output_text.delta
event: response.function_call_arguments.delta
event: response.function_call_arguments.done
event: response.completed
```

流式内容：**模型输出 token 和工具调用事件**。

### 6.3 本质区别

| 维度 | A2A v1.0 流式 | OpenAI Responses 流式 |
|------|---------------|----------------------|
| 流的内容 | 任务状态、产物交付 | token、reasoning、工具调用 |
| 谁在流 | 被调 Agent 汇报进度 | 模型逐字生成 |
| 消费方 | 调度 Agent / 用户界面 | 需要实时文本展示的 UI |

---

## 7. 从 Completion 升级到 A2A v1.0 的成本评估

### 7.1 协议改造

需要把 OpenAI 风格的调用迁移到 A2A v1.0：

| 旧模式 | A2A v1.0 |
|--------|----------|
| `messages` 数组 | `Message` + `Part` |
| `choices[].message.content` | `Task.artifacts[].parts` |
| `tool_calls` | `Artifact` / `Message` 中的结构化 `data` |
| 手动维护 messages | `context_id` + Task history |
| `stream: true` delta | `message:stream` 任务事件 |

### 7.2 新增基础设施

- **AgentCard 发布**：每个 Agent 需提供 `agent-card.json`
- **发现机制**：客户端需先发现 Agent Card
- **任务存储**：被调 Agent 需持久化 Task 状态
- **多协议绑定支持**：根据场景选择 HTTP+JSON / JSON-RPC / gRPC
- **安全协商**：处理 AgentCard 中的 security_schemes

### 7.3 成本量化参考

| 场景 | 预估成本 | 说明 |
|------|----------|------|
| 1～2 个 Agent 互调 | 2～3 天 | 协议格式替换 + AgentCard |
| 3～5 个 Agent | 1～2 周 | 公共 SDK + 任务存储 |
| 10+ Agent 或跨组织 | 1～2 月 | 发现注册、路由、鉴权、可观测性 |

---

## 8. 选型建议

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| 单模型推理、文本生成 | OpenAI Responses API | 官方推荐，内置工具，状态管理更简单 |
| 需要调用 OpenAI 原生工具 | Responses API | web_search、code_interpreter 等开箱即用 |
| 内部多个 Agent 协作 | A2A v1.0 | 标准化 Agent 间通信和发现 |
| 跨组织 / 第三方 Agent 互通 | A2A v1.0 | 开放协议，AgentCard + 安全协商 |
| 长任务、异步执行、等人确认 | A2A v1.0 | Task 生命周期 + 订阅机制是原生设计 |
| 需要返回文件/结构化产物 | A2A v1.0 | Artifact 明确支持多模态产物 |

---

## 9. 总结

- **A2A v1.0** 是正式的跨 Agent 协作协议，核心变化是端点从 `tasks/send` 改为 `message:send/stream`，并以 Protobuf 为规范源。
- **OpenAI Responses API** 是单一模型服务的 Agent 化增强，重点在状态管理、内置工具和 Item 化输出。
- 两者都在解决「有状态、任务化、工具化」的问题，但 **A2A 解决 Agent 之间的协议互通，OpenAI API 解决模型服务的 Agent 能力暴露**。
- 如果你们的场景是「多个内部 Agent 互相调用」，A2A v1.0 是更合适的方向；如果只是「让 Agent 调用 OpenAI 模型」，Responses API 更直接。

---

## 参考资料

1. [A2A v1.0 Core Specification](https://agent2agent.info/specification/core/)
2. [A2A v1.0 Data Structures](https://agent2agent.info/specification/data-structures/)
3. [A2A v1.0 Protobuf (a2a.proto)](https://raw.githubusercontent.com/a2aproject/A2A/main/specification/a2a.proto)
4. [What Changed in A2A v1.0](https://a2acn.com/en/docs/community/whats-new-v1/)
5. [OpenAI Chat Completions API Reference](https://platform.openai.com/docs/api-reference/chat)
6. [OpenAI Migrate to Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses)
