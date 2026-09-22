> 本文解决三个问题：
> 1. Eino 主 Agent 怎么接入 A2A v1.0
> 2. 只有 Completion 接口的子 Agent 怎么被包成 A2A 服务
> 3. 给子 Agent 提供商的自助封装文档该怎么写

# Eino + A2A v1.0 集成与 Completion-to-A2A Adapter 方案

---

## 1. Eino 主 Agent 接入 A2A v1.0

### 1.1 现状

主 Agent 用 Eino 实现，内部是 Graph + ChatModel + ToolsNode 的执行流。现在要让它既能发 A2A 请求给其他 Agent，也能作为 A2A 服务被其他 Agent 调用。

### 1.2 好消息：Eino 官方有 A2A 扩展

CloudWeGo 已经提供了 Eino 的 A2A 扩展包：

```bash
go get github.com/cloudwego/eino-ext/a2a
```

这个包提供了：
- `client`：A2A 客户端，用于主 Agent 调用其他 A2A Agent
- `server`：A2A 服务端，用于把 Eino Agent 封装成 A2A 服务
- `extension/eino`：Eino 框架专用集成层
- `models`：A2A v1.0 数据模型（Task、Message、Part、Artifact 等）
- `transport`：HTTP / JSON-RPC 传输绑定

### 1.3 让 Eino Agent 对外提供 A2A 服务

核心思路：实现 `TaskProcessor` 接口，把 A2A 的 Task 映射到 Eino Graph 的执行。

```go
package main

import (
    "context"
    "github.com/cloudwego/eino-ext/a2a/extension/eino"
    "github.com/cloudwego/eino-ext/a2a/models"
    "github.com/cloudwego/eino/compose"
)

// EinoAgentTaskProcessor 把 A2A Task 转成 Eino Graph 执行
type EinoAgentTaskProcessor struct {
    graph compose.Graph
}

func (p *EinoAgentTaskProcessor) Process(
    ctx context.Context,
    taskID string,
    message models.Message,
    handle eino.TaskHandle,
) error {
    // 1. 更新任务状态为 WORKING
    handle.UpdateStatus(ctx, models.TaskStateWorking, "开始处理任务")

    // 2. 把 A2A Message 转成 Eino 的输入
    input := convertMessageToEinoInput(message)

    // 3. 调用 graph.Stream 执行
    stream, err := p.graph.Stream(ctx, input)
    if err != nil {
        handle.UpdateStatus(ctx, models.TaskStateFailed, err.Error())
        return err
    }

    // 4. 流式收集输出，并作为 Artifact 推送
    var fullText strings.Builder
    for chunk := range stream {
        text := extractText(chunk)
        fullText.WriteString(text)

        // 可以每积累一段就推送一次 artifact update
        handle.PushArtifact(ctx, models.Artifact{
            ArtifactID: "art-" + taskID,
            Name:       "stream-output",
            Parts: []models.Part{
                {Text: text, MediaType: "text/plain"},
            },
        })
    }

    // 5. 任务完成
    handle.UpdateStatus(ctx, models.TaskStateCompleted, "处理完成")
    return nil
}
```

然后启动 A2A Server：

```go
func main() {
    processor := &EinoAgentTaskProcessor{graph: buildGraph()}

    server := eino.NewServer(eino.ServerConfig{
        AgentCard: models.AgentCard{
            Name:        "Main Agent",
            Description: "主调度 Agent",
            Version:     "1.0.0",
            SupportedInterfaces: []models.AgentInterface{
                {
                    URL:              "https://main-agent.example.com/a2a/v1",
                    ProtocolBinding:  "HTTP+JSON",
                    ProtocolVersion:  "1.0",
                },
            },
            Capabilities: models.AgentCapabilities{
                Streaming: true,
            },
            Skills: []models.AgentSkill{
                {
                    ID:          "task-delegation",
                    Name:        "任务委派",
                    Description: "把任务分发给合适的子 Agent",
                    Tags:        []string{"orchestration"},
                },
            },
        },
        TaskProcessor: processor,
    })

    server.Run(":8080")
}
```

### 1.4 让 Eino Agent 调用其他 A2A Agent

主 Agent 内部需要有一个 Tool，这个 Tool 实际是一个 A2A 客户端：

```go
func NewA2ADelegateTool(agentCardURL string) tool.BaseTool {
    return tool.NewTool(
        "delegate_to_agent",
        "把任务委派给指定的 A2A Agent",
        delegateSchema,
        func(ctx context.Context, input string) (string, error) {
            // 1. 发现 Agent Card
            card, err := a2a.DiscoverAgentCard(ctx, agentCardURL)
            if err != nil {
                return "", err
            }

            // 2. 创建 A2A 客户端
            client, err := a2a.NewClient(card)
            if err != nil {
                return "", err
            }

            // 3. 发送流式消息
            stream, err := client.SendStreamingMessage(ctx, models.Message{
                Role: models.RoleUser,
                Parts: []models.Part{
                    {Text: input, MediaType: "text/plain"},
                },
            })
            if err != nil {
                return "", err
            }

            // 4. 收集结果
            var result strings.Builder
            for event := range stream {
                switch e := event.(type) {
                case *models.TaskArtifactUpdateEvent:
                    for _, part := range e.Artifact.Parts {
                        if part.Text != "" {
                            result.WriteString(part.Text)
                        }
                    }
                case *models.TaskStatusUpdateEvent:
                    if e.Status.State == models.TaskStateCompleted {
                        return result.String(), nil
                    }
                    if e.Status.State == models.TaskStateFailed {
                        return "", fmt.Errorf("task failed")
                    }
                }
            }
            return result.String(), nil
        },
    )
}
```

### 1.5 连续会话（context_id）的支持

Eino Agent 作为 A2A 服务时，需要维护 `context_id` 到 Eino Graph 执行状态的映射。

建议方案：

```go
type ContextManager struct {
    store map[string]*ContextSession // context_id -> session
}

type ContextSession struct {
    ContextID string
    History   []models.Message
    // 其他 Eino 执行上下文
}

func (p *EinoAgentTaskProcessor) Process(
    ctx context.Context,
    taskID string,
    message models.Message,
    handle eino.TaskHandle,
) error {
    contextID := message.ContextID
    if contextID == "" {
        contextID = generateUUID()
        message.ContextID = contextID
    }

    session := p.contextManager.GetOrCreate(contextID)
    session.History = append(session.History, message)

    // 构造 Eino 输入时，把历史消息带进去
    input := buildEinoInput(session.History)

    // ... 执行 graph
}
```

**关键点：**
- `context_id` 是连续会话的纽带，不是 `task_id`
- 每个 Task 是一轮独立的请求-响应
- 服务端需要在内存或 Redis 中维护 `context_id` 到历史消息的映射
- 如果 `context_id` 不存在，服务端生成一个新的

---

## 2. 子 Agent 只有 Completion 接口：Completion-to-A2A Adapter

### 2.1 核心思路

子 Agent 暴露的是 `/v1/chat/completions`，A2A 客户端发的是 `/message:stream`。Adapter 的作用就是把 A2A 请求翻译成 Completion 请求，再把 Completion 的响应翻译成 A2A 的 Task 事件流。

```
A2A Client ──A2A──> Adapter ──Completion──> Sub-Agent
             (message:stream)    (chat/completions)
```

### 2.2 Adapter 的职责

| A2A 侧 | Completion 侧 |
|--------|--------------|
| 接收 `Message` + `Part` | 转成 `messages` 数组 |
| 创建 Task，维护 Task 状态 | 调用 `/v1/chat/completions` |
| 把模型输出包装成 `Artifact` | 解析 `choices[].delta.content` |
| 流式推送 `task_status_update` / `task_artifact_update` | 转发 SSE chunk |
| 处理 `INPUT_REQUIRED` | 模型没有原生支持，需要额外逻辑 |
| 支持 `context_id` | 维护上下文历史 |

### 2.3 Adapter 实现示例

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "strings"
    "time"

    "github.com/cloudwego/eino-ext/a2a/models"
)

// CompletionAdapter 把 A2A 请求转发给 Completion 接口
type CompletionAdapter struct {
    completionURL string
    apiKey        string
    httpClient    *http.Client
    taskStore     TaskStore
    contextStore  ContextStore
}

func (a *CompletionAdapter) HandleSendMessageStream(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    // 1. 解析 A2A 请求
    var req models.SendMessageRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // 2. 创建 Task
    contextID := req.Message.ContextID
    if contextID == "" {
        contextID = generateUUID()
    }

    task := a.taskStore.Create(ctx, contextID, req.Message)

    // 3. 设置 SSE 头
    w.Header().Set("Content-Type", "text/event-stream")
    w.Header().Set("Cache-Control", "no-cache")
    w.Header().Set("Connection", "keep-alive")
    flusher := w.(http.Flusher)

    // 4. 推送 SUBMITTED 状态
    a.writeEvent(w, flusher, "task_status_update", models.TaskStatusUpdateEvent{
        TaskID:    task.ID,
        ContextID: contextID,
        Status: models.TaskStatus{
            State: models.TaskStateSubmitted,
        },
    })

    // 5. 启动 goroutine 调用 Completion
    go a.processTask(ctx, task.ID)

    // 6. 订阅 Task 更新并推送给客户端
    sub := a.taskStore.Subscribe(task.ID)
    defer a.taskStore.Unsubscribe(task.ID, sub)

    for event := range sub {
        a.writeEvent(w, flusher, event.Type, event.Data)
        if isTerminalEvent(event) {
            break
        }
    }
}

func (a *CompletionAdapter) processTask(ctx context.Context, taskID string) {
    task := a.taskStore.Get(taskID)

    // 更新为 WORKING
    a.taskStore.UpdateStatus(taskID, models.TaskStatus{
        State: models.TaskStateWorking,
        Message: &models.Message{
            Role:  models.RoleAgent,
            Parts: []models.Part{{Text: "正在调用模型", MediaType: "text/plain"}},
        },
    })

    // 构造 messages
    messages := a.buildMessages(task.ContextID, task.InitialMessage)

    // 调用 Completion 接口
    payload := map[string]interface{}{
        "model":    "gpt-4", // 可从 AgentCard 或配置读取
        "messages": messages,
        "stream":   true,
    }

    reqBody, _ := json.Marshal(payload)
    req, _ := http.NewRequestWithContext(ctx, "POST", a.completionURL, bytes.NewReader(reqBody))
    req.Header.Set("Authorization", "Bearer "+a.apiKey)
    req.Header.Set("Content-Type", "application/json")

    resp, err := a.httpClient.Do(req)
    if err != nil {
        a.taskStore.UpdateStatus(taskID, models.TaskStatus{
            State: models.TaskStateFailed,
            Message: &models.Message{
                Role:  models.RoleAgent,
                Parts: []models.Part{{Text: err.Error(), MediaType: "text/plain"}},
            },
        })
        return
    }
    defer resp.Body.Close()

    // 流式读取 Completion 响应
    reader := bufio.NewReader(resp.Body)
    var fullText strings.Builder
    artifactID := "art-" + taskID

    for {
        line, err := reader.ReadString('\n')
        if err == io.EOF {
            break
        }
        if err != nil {
            a.taskStore.UpdateStatus(taskID, models.TaskStatus{
                State: models.TaskStateFailed,
                Message: &models.Message{
                    Role:  models.RoleAgent,
                    Parts: []models.Part{{Text: err.Error(), MediaType: "text/plain"}},
                },
            })
            return
        }

        line = strings.TrimSpace(line)
        if !strings.HasPrefix(line, "data: ") {
            continue
        }
        data := strings.TrimPrefix(line, "data: ")
        if data == "[DONE]" {
            break
        }

        var chunk CompletionChunk
        if err := json.Unmarshal([]byte(data), &chunk); err != nil {
            continue
        }

        content := chunk.Choices[0].Delta.Content
        if content == "" {
            continue
        }

        fullText.WriteString(content)

        // 推送 artifact update
        a.taskStore.PushArtifact(taskID, models.Artifact{
            ArtifactID: artifactID,
            Name:       "completion-output",
            Parts: []models.Part{
                {Text: content, MediaType: "text/plain"},
            },
        })
    }

    // 完成
    a.taskStore.UpdateStatus(taskID, models.TaskStatus{
        State: models.TaskStateCompleted,
        Message: &models.Message{
            Role:  models.RoleAgent,
            Parts: []models.Part{{Text: "处理完成", MediaType: "text/plain"}},
        },
    })
}

func (a *CompletionAdapter) buildMessages(contextID string, initial models.Message) []map[string]string {
    // 1. 取历史消息
    history := a.contextStore.GetMessages(contextID)

    // 2. 把 A2A Message 转成 Completion Message
    var messages []map[string]string
    for _, msg := range history {
        role := "user"
        if msg.Role == models.RoleAgent {
            role = "assistant"
        }
        text := concatenateParts(msg.Parts)
        messages = append(messages, map[string]string{
            "role":    role,
            "content": text,
        })
    }

    // 3. 追加当前消息
    messages = append(messages, map[string]string{
        "role":    "user",
        "content": concatenateParts(initial.Parts),
    })

    // 4. 保存到 context
    a.contextStore.AddMessage(contextID, initial)

    return messages
}
```

### 2.4 关于 INPUT_REQUIRED 的处理

Completion 接口没有原生 `INPUT_REQUIRED` 概念。如果子 Agent 需要等人输入，Adapter 有两种处理方式：

**方式 A：不模拟 INPUT_REQUIRED，直接当单轮处理**
- 把子 Agent 的 Completion 调用当成一次性调用
- 如果模型返回需要补充信息，就把这段文本作为 Task 的 COMPLETED 结果返回
- 由上游 Agent 或用户决定是否再次发起新 Task

**方式 B：通过约定模板模拟 INPUT_REQUIRED**
- 在 Adapter 里配置：如果模型输出包含特定标记（如 `[NEED_INPUT] 请提供...`），就把 Task 状态改为 `INPUT_REQUIRED`
- 用户回复时，同一个 `context_id` 下创建新 Task，Adapter 把历史 + 新回复一起发给 Completion
- 这种方式需要子 Agent 配合输出特定格式，不够通用

**推荐：** 对纯 Completion 子 Agent 用方式 A，不强求 `INPUT_REQUIRED`。`INPUT_REQUIRED` 只留给真正实现了 A2A 的子 Agent。

---

## 3. 给子 Agent 提供商的封装文档

### 3.1 文档目标

告诉子 Agent 提供商：如果你们已经有 `/v1/chat/completions` 接口，怎么自己包一层 A2A v1.0 服务出来。

### 3.2 文档大纲

```markdown
# 子 Agent A2A v1.0 封装指南

## 1. 你要实现什么？

只需要实现以下 4 个接口，就能被我们的主 Agent 通过 A2A 调用：

- `GET /agent-card.json` —— 返回 Agent 能力描述
- `POST /message:send` —— 同步处理任务
- `POST /message:stream` —— 流式处理任务（推荐）
- `GET /tasks/{id}` —— 查询任务状态

可选：
- `POST /tasks/{id}:cancel` —— 取消任务
- `GET /tasks/{id}:subscribe` —— 订阅任务更新

## 2. Agent Card 怎么写？

```json
{
  "name": "你的 Agent 名称",
  "description": "一句话说明你的 Agent 能做什么",
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
      "id": "your-skill-id",
      "name": "你的技能名",
      "description": "技能描述",
      "tags": ["tag1", "tag2"],
      "input_modes": ["text/plain"],
      "output_modes": ["text/plain", "application/json"]
    }
  ]
}
```

## 3. /message:stream 必须怎么做？

### 3.1 请求体

```json
{
  "message": {
    "message_id": "msg-001",
    "role": "USER",
    "context_id": "ctx-001",
    "parts": [
      {
        "text": "用户输入",
        "media_type": "text/plain"
      }
    ]
  },
  "configuration": {
    "accepted_output_modes": ["text/plain", "application/json"]
  }
}
```

### 3.2 响应（SSE）

必须返回 `text/event-stream`，事件类型只能是：

- `task_status_update`
- `task_artifact_update`

示例：

```
event: task_status_update
data: {"task_id":"task-001","context_id":"ctx-001","status":{"state":"SUBMITTED"}}

event: task_status_update
data: {"task_id":"task-001","context_id":"ctx-001","status":{"state":"WORKING"}}

event: task_artifact_update
data: {"task_id":"task-001","context_id":"ctx-001","artifact":{"artifact_id":"art-001","name":"result","parts":[{"text":"这是结果","media_type":"text/plain"}]}}

event: task_status_update
data: {"task_id":"task-001","context_id":"ctx-001","status":{"state":"COMPLETED"}}
```

### 3.3 状态机必须支持

```
SUBMITTED → WORKING → COMPLETED
                 ↘ FAILED
```

至少支持这 4 个状态。如果你们的子 Agent 需要等人输入，再实现 `INPUT_REQUIRED`。

## 4. context_id 怎么处理？

- 如果请求带了 `context_id`，说明是连续会话，你要保留这个会话的历史消息
- 如果没带，你生成一个新的 `context_id` 返回
- 同一个 `context_id` 下的多次请求，你要能读取历史上下文

## 5. Task ID 谁生成？

由你（服务端）生成。第一次响应的 `task_status_update` 里必须带 `task_id`。

## 6. 文件/结构化数据怎么返回？

通过 `Artifact.parts` 返回：

```json
{
  "artifact_id": "art-001",
  "name": "report",
  "parts": [
    {
      "data": {"total": 1000, "growth": 0.15},
      "media_type": "application/json"
    },
    {
      "raw": "base64...",
      "filename": "report.xlsx",
      "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }
  ]
}
```

## 7. 最简单的实现路径

1. 把你们的 `/v1/chat/completions` 调用包一层 HTTP 服务
2. 收到 A2A 请求后，调用自己的 Completion 接口（带 `stream: true`）
3. 把每个 `delta.content` 包装成 `task_artifact_update` 推送
4. 流结束时推送 `task_status_update`（`COMPLETED`）
5. 加上 `GET /agent-card.json` 和 `GET /tasks/{id}`

## 8. 验收 checklist

- [ ] `GET /agent-card.json` 能正常返回
- [ ] `POST /message:stream` 返回 SSE，包含至少一次 `task_status_update` 和一次 `task_artifact_update`
- [ ] `task_status_update` 最终状态是 `COMPLETED` 或 `FAILED`
- [ ] 同一 `context_id` 下的多次请求能保留上下文
- [ ] 任务失败时返回 `FAILED` 状态并附带错误信息
```

---

## 4. 架构总览

```
                         ┌─────────────────────────────────────┐
                         │           主 Agent (Eino)            │
                         │  ┌──────────────┐                  │
                         │  │   Eino Graph  │                  │
                         │  │ ChatModel+Tools│                  │
                         │  └──────┬───────┘                  │
                         │         │                          │
                         │  ┌──────▼───────┐                  │
                         │  │ A2A Client   │                  │
                         │  │ (eino-ext/a2a)│                  │
                         │  └──────┬───────┘                  │
                         └─────────┼──────────────────────────┘
                                   │ A2A v1.0
                                   │ message:stream
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
   ┌─────▼──────┐           ┌──────▼──────┐          ┌───────▼────────┐
   │ 子 Agent A  │           │  Adapter B  │          │  子 Agent C    │
   │ 原生 A2A    │           │ (Completion │          │ 原生 A2A       │
   │            │           │  → A2A)     │          │               │
   └────────────┘           └──────┬──────┘          └───────────────┘
                                   │
                                   │ /v1/chat/completions
                            ┌──────▼──────┐
                            │ 子 Agent B' │
                            │ 只有 Completion
                            └─────────────┘
```

---

## 5. 关键决策建议

### 5.1 Eino 主 Agent 接入

- 直接用 `github.com/cloudwego/eino-ext/a2a`
- 实现 `TaskProcessor`，内部调用 `graph.Stream`
- 通过 Callback 把 Eino 的执行状态映射到 A2A Task 状态
- 上下文用 `context_id` 维护，建议用 Redis

### 5.2 子 Agent 集成策略

| 子 Agent 情况 | 推荐方案 | 工作量 |
|--------------|----------|--------|
| 有开发能力，愿意改 | 给封装文档，让他们自己实现 A2A | 他们 2-5 天 |
| 只有 Completion，不愿改 | 我们写 Adapter | 我们 1-2 天一个 |
| 是重要的合作伙伴 | 我们派人协助封装 | 视情况而定 |

### 5.3 必须坚持的协议要求

- 必须支持 SSE（`message:stream`）
- 必须支持 `context_id` 连续会话
- 必须实现 `AgentCard`
- 必须处理 `WORKING` / `COMPLETED` / `FAILED` 三种基础状态
- 建议实现 `INPUT_REQUIRED`（如果业务需要）
- 建议实现 `cancel`（如果任务可能长时间运行）

---

## 6. 一句话总结

Eino 主 Agent 直接用 `eino-ext/a2a` 包接入 A2A；只有 Completion 的子 Agent 通过 Adapter 桥接，桥接的核心是把 `delta.content` 流转成 A2A 的 `task_artifact_update` 事件，同时用 `context_id` 维护会话历史。给子 Agent 提供商的文档要聚焦「4 个接口 + AgentCard + SSE 状态机」。
