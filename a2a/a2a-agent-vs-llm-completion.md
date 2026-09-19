# Agent 间调用升级：从 Completion 直连到 A2A

> **当前状态**：多个 Agent 之间通过 Completion 接口直接调用，调用方需要封装 MCP Server / Skill 做转发。  
> **目标**：引入 A2A 协议，让多个 Agent 能够标准化接入、协作和扩展。  
> **核心结论**：A2A 不是替代 LLM，而是在 LLM 之上增加了一层 Agent 协作协议；升级有价值，但需要评估改造成本。

---

## 1. 为什么我们面临这个选择？

目前的方式很简单直接：一个 Agent 想调用另一个 Agent，就直接发一个 Completion 请求过去。

```
Agent A ──Completion──> Agent B ──Completion──> LLM
```

这种方式在 Agent 数量少的时候很好用，成本低、延迟低、实现快。但当 Agent 数量变多，问题会逐渐暴露：

- 每新增一个 Agent，调用方都要单独适配它的接口格式
- 返回内容只能是文本或 tool_calls，文件、图表、结构化数据不好传递
- 被调 Agent 内部做了哪些事、任务进行到哪一步，调用方无从感知
- 长任务、等人确认、失败恢复等场景没有标准处理方式

A2A 协议的出现，本质上是为了把 Agent 之间的调用从「点对点接口适配」变成「标准化任务协作」。

---

## 2. 两种调用方式的本质区别

如果把 LLM 看作「大脑」，那么 Completion 接口就是直接激活这个大脑；A2A 则是让两个「员工」之间交接任务。

| 维度 | 直接调 Completion | 通过 A2A 调 Agent |
|------|-------------------|-------------------|
| 你在调用谁 | 大语言模型 | 另一个 Agent 服务 |
| 请求在说什么 | "基于这段对话生成回复" | "请完成这个任务" |
| 返回的是什么 | 文本或 tool_calls | 任务状态 + 产物（Artifact） |
| 状态由谁管 | 调用方自己拼 messages | 被调 Agent 通过 sessionId 维护 |
| 适合做什么 | 文本生成、单轮推理 | 多 Agent 协作、异步任务、多模态产物 |

简单说：**Completion 是模型层的 API，A2A 是应用层的协作协议。**

---

## 3. 接口层面到底差在哪？

### 3.1 直接调 Completion

```http
POST /v1/chat/completions
Authorization: Bearer {api_key}

{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "你是数据分析助手"},
    {"role": "user", "content": "分析 Q3 销售数据"}
  ],
  "tools": [...]
}
```

返回：

```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "Q3 销售额同比增长 15%..."
    }
  }]
}
```

特点：
- 调用方必须自己维护完整对话历史
- 模型只负责生成，工具执行由调用方处理
- 返回内容局限于文本或 function_call

### 3.2 通过 A2A 调 Agent

```http
POST /agent/{agent_id}/tasks/send

{
  "id": "task-001",
  "sessionId": "session-abc",
  "message": {
    "role": "user",
    "parts": [
      {"type": "text", "text": "分析 Q3 销售数据"}
    ]
  },
  "skill": "data-analysis",
  "acceptedOutputModes": ["text", "file", "data"]
}
```

返回：

```json
{
  "id": "task-001",
  "status": {"state": "completed"},
  "artifacts": [
    {
      "name": "q3_report",
      "parts": [
        {
          "type": "file",
          "file": {
            "name": "q3_report.xlsx",
            "bytes": "base64..."
          }
        }
      ]
    }
  ]
}
```

特点：
- 请求的是「任务」，不是「生成一段文本」
- 被调 Agent 自己维护会话和状态
- 返回可以是文件、图表、结构化数据等多模态产物
- 有完整的任务生命周期

### 3.3 send 和 sendSubscribe 的区别

A2A 提供两个提交任务的入口，分别对应同步和流式两种调用方式：

| 接口 | 方式 | 返回内容 | 适用场景 |
|------|------|----------|----------|
| `tasks/send` | 同步 | 任务完成后的最终 Task 结果 | 短任务、希望一次拿到结果 |
| `tasks/sendSubscribe` | 流式（SSE） | 任务状态/产物实时更新 | 长任务、需要看进度、人机协同 |

`sendSubscribe` 返回的事件流大概长这样：

```
event: task-status
data: {"id":"task-001","status":{"state":"working"}}

event: task-artifact
data: {"id":"task-001","artifact":{"name":"chart","parts":[{"type":"file",...}]}}

event: task-status
data: {"id":"task-001","status":{"state":"completed"}}
```

### 3.4 流式推送的本质区别

| 方式 | 流式内容 |
|------|----------|
| Completion 流式 | 逐字返回 token：`Q3` → `销售额` → `同比` |
| A2A `sendSubscribe` | 返回任务状态更新：`working` → 收到图表 → `completed` |

A2A 的流式不是让你看 Agent 怎么"思考"，而是让你跟踪任务进展。

---

## 4. 升级到 A2A 的成本分析

这是我们需要重点评估的部分。成本不是单一维度，至少有以下几个方面。

### 4.1 协议改造：中等

需要把原来的 Completion 调用包装成 A2A 的 `tasks/send` 或 `tasks/sendSubscribe`：

- 请求体从 `messages` 改成 `Task` 结构
- 响应从解析 `choices[0].message` 改成解析 `status` + `artifacts`
- 流式从 token 流改成任务事件流
- 错误处理从 HTTP 状态码改成任务状态机

如果只有一两个调用点，改造很快；如果调用点散在多个 Agent 里，需要统一封装。

### 4.2 状态管理：中高

这是最大的隐性成本。

原来调 Completion 是无状态的：发一次请求，拿到结果，结束。

A2A 要求被调 Agent 维护任务状态，意味着需要引入：

- 任务存储：Redis、数据库或内存队列
- 任务调度：超时处理、重试、状态恢复
- 会话管理：`sessionId` 的生命周期维护

对于长任务、等人确认等场景，这部分是刚需；但对于短平快的调用，会显得有些重。

### 4.3 基础设施：中等

要实现多个 Agent 接入 A2A，通常需要：

- A2A Server / Client 封装
- Agent 注册与发现机制
- Skill 路由（根据 skill 字段分发到对应处理逻辑）
- 统一的认证和权限控制

如果团队已经有现成 SDK（如 Google A2A SDK、Spring AI 等），接入成本会低很多；如果自研，需要投入一定时间。

### 4.4 延迟与性能：略有增加

A2A 本身会多一层序列化和网络往返。更重要的是交互方式变了：

- 原来：一次请求拿到最终答案
- A2A：任务可能经历 `submitted → working → input-required → completed` 多个状态

对于实时性要求很高的场景，需要重点测试端到端延迟。

### 4.5 调试运维：高

这是最容易被低估的成本。

原来链路简单：

```
Agent A → Agent B → LLM
```

A2A 之后链路变长：

```
Agent A → A2A Client → A2A Server → Agent B → LLM
```

再加上任务状态机、SSE 事件流、Artifact 解析，出问题时的排查路径会复杂很多。建议提前统一日志规范和任务追踪机制。

### 4.6 团队学习：中等

团队需要理解 A2A 的核心概念：

- Task / Message / Part / Artifact
- 任务状态机
- Skill 路由
- SSE 事件类型

概念不复杂，但需要文档和至少一次内部培训。

---

## 5. 改造成本量化参考

| 场景 | 预估成本 | 说明 |
|------|----------|------|
| 1～2 个 Agent 互相调用 | 1～2 天 | 主要是请求/响应格式替换 |
| 3～5 个 Agent | 1 周左右 | 需要统一 A2A client/server，接入状态存储 |
| 10+ 个 Agent 或跨团队协作 | 2～4 周 | 需要注册发现、路由、鉴权、文档、调试工具链 |

这里只是开发改造时间，不包含后续运维和团队学习成本。

---

## 6. 什么时候建议升级？

| 情况 | 建议 |
|------|------|
| 只有 2～3 个 Agent，调用关系简单 | 暂缓，继续用 Completion 更轻量 |
| Agent 数量会持续增加 | 建议升级，避免 N×M 的接口适配 |
| 需要返回文件、图表、结构化数据 | A2A 的 Artifact 更自然 |
| 存在长任务、等人确认、失败恢复 | A2A 的状态机是刚需 |
| 需要和外部团队/第三方 Agent 互通 | A2A 是开放协议，建议直接上 |

结合我们的实际情况——**多个 Agent 需要接入并形成协作关系**——A2A 是值得投入的方向。

---

## 7. 升级路径建议

不建议一次性全部重构，推荐分阶段推进：

1. **试点验证**：选 1～2 对调用关系清晰的 Agent，先完成 A2A 改造，跑通协议、状态机和调试流程。
2. **公共 SDK**：把 A2A client/server、任务存储、错误处理封装成团队公共库，避免每个 Agent 重复实现。
3. **兼容层过渡**：旧 Agent 先通过 adapter 接入 A2A，不要一刀切全量重构。
4. **规范先行**：统一任务 ID 透传、日志格式、状态监控，否则后续排障成本会非常高。

---

## 8. 总结

- **Completion 调用**适合简单、直接、无状态的模型推理。
- **A2A 调用**适合需要标准化协作、异步任务、多模态产出的多 Agent 场景。
- 我们的现状是 Agent 数量将增长，Completion 直连会逐渐成为瓶颈。
- 升级到 A2A 的直接改造成本可控，但状态管理、调试运维、基础设施需要提前规划。
- 推荐用「试点 + 公共 SDK + 兼容层」的方式分阶段推进，而不是一次性全量重构。
