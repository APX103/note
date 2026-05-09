# A2A 智能协作平台 — 产品需求与架构设计文档

> **版本**：v0.1  
> **定位**：基于 A2A 协议的多 Agent 去中心化协作基础设施平台  
> **核心目标**：让团队内各领域的 Agent 能够自主发现、自主协商、协同完成复杂任务，同时平台提供发现、代理、追踪、分析四大基础设施能力。

---

## 一、系统概述

### 1.1 背景与问题

当前 A2A 生态存在以下生产级缺口：
- **无标准服务发现**：A2A 协议仅定义 Agent Card 格式，未规定注册与发现机制
- **无通信代理层**：Agent 间直连无法实现集中审计、流量管控、链路追踪
- **无任务追踪能力**：跨 Agent 的 Task 生命周期不可见，无法排查故障
- **无数据沉淀**：Agent 间协作数据散落，无法用于后续优化与分析

本平台旨在填补上述缺口，在**不破坏 A2A 协议兼容性**的前提下，构建一层基础设施，使 Agent 协作从"点对点野路子"升级为"可观测、可治理、可优化"的企业级网络。

### 1.2 核心设计哲学

| 原则 | 说明 |
|------|------|
| **去中心化编排** | 不设置中心 Orchestrator。由 Agent 自主决策"问谁、问什么、何时终止"。平台只做通信代理与发现服务。 |
| **协议兼容** | 对外暴露标准 A2A 接口（Agent Card、JSON-RPC、SSE），第三方 A2A Agent 可零改造接入。 |
| **平台不介入推理** | 平台不干预 Agent 的内部逻辑、Prompt 或工具选择，只管控"信封"（元数据、路由、权限）。 |
| **数据归集** | 所有通信经过平台，天然形成全量数据湖，支撑追踪、分析、审计。 |
| **上下文一致性** | 同一 Task 下，所有参与 Agent 共享统一的 Session 上下文，确保多轮对话记忆一致。 |

---

## 二、功能需求

### 2.1 服务发现与注册（Discovery & Registry）

#### 2.1.1 Agent 注册
- Agent 启动时向平台 Registry 注册，提交 Agent Card（名称、描述、Skills、端点、能力声明）
- 支持 **主动注册**（Agent 启动调用 API）和 **代理注册**（DevOps 配置 CI/CD 时批量注册）
- 注册信息支持版本管理（Agent 升级时保留历史版本）

#### 2.1.2 心跳与健康检查
- 已注册 Agent 周期性向平台发送心跳（默认 30s，可配置）
- 平台自动清理超时未心跳的 Agent（默认 90s 无心跳标记为 Offline）
- 提供健康检查端点供外部监控集成

#### 2.1.3 Agent 发现查询
- **技能搜索**：按 skill 名称/描述/标签搜索 Agent（如查找具有 "code-review" 能力的 Agent）
- **语义搜索**（可选 V2）：用自然语言描述需求，返回最匹配的 Agent（基于 Embedding）
- **权限过滤**：查询结果自动按调用方 Agent 的权限范围过滤，不可见的 Agent 不出现在结果中
- **列表缓存**：Registry 数据缓存于 Redis，保证亚秒级查询响应

#### 2.1.4 Agent 元数据更新与注销
- Agent 支持热更新 Agent Card（能力变更、版本升级）
- 支持优雅注销（通知平台下线，平台转发完存量消息后关闭路由）

---

### 2.2 通信代理（Message Proxy）

#### 2.2.1 统一消息网关
- 所有 Agent 间通信**必须经过平台转发**，禁止 Agent 间直连（通过网络安全策略 + SDK 约束）
- 平台对外暴露标准 A2A 端点（`/.well-known/agent-card`、`/sendMessage`、`/sendMessageStream`）
- Agent 实际向平台发送消息，平台根据目标 Agent ID 路由到真实目的地

#### 2.2.2 消息路由
- **直接路由**：Agent A → 平台 → Agent B（点对点）
- **广播路由**（可选 V2）：Agent A → 平台 → Agent B/C/D（一对多，用于投票/征集场景）
- **负载均衡**：同一 Skill 有多个 Agent 实例时，按 Round Robin / 最少连接 / 响应时间加权分发

#### 2.2.3 消息持久化
- 所有经过平台的消息（Task 创建、状态更新、Artifact、心跳）写入时序数据库或消息日志
- 持久化字段：消息 ID、Task ID、Session ID、发送方、接收方、时间戳、消息类型、Payload（可选脱敏）、路由耗时
- 保留策略：默认 90 天，支持按项目/团队配置

#### 2.2.4 异步与流式支持
- 支持同步请求/响应（`/sendMessage`）
- 支持 SSE 流式传输（`/sendMessageStream`），平台透传 Agent 的进度推送，同时记录流事件
- 支持长任务（LRO）的挂起与恢复

---

### 2.3 Task 与链路追踪（Task Management & Tracing）

#### 2.3.1 Task 生命周期管理
平台维护每个 Task 的完整状态机：

```
CREATED → SUBMITTED → WORKING → [COMPLETED / FAILED / CANCELLED / TIMEOUT]
   ↑         ↑          ↓
   └─────────┴── 支持状态回退与重试
```

- **Task 创建**：任意 Agent（通常是入口 Agent）创建 Task，平台分配全局 Task ID
- **Task 分配**：平台记录 Task 与参与 Agent 的关联关系
- **状态变更**：Agent 通过 A2A 消息上报状态，平台更新状态机
- **Task 查询**：提供 API 查询 Task 当前状态、参与 Agent、耗时、结果摘要

#### 2.3.2 分布式链路追踪
- 每个 Task 生成全局 Trace ID，贯穿所有参与 Agent 的交互
- 每个消息包含 Span ID + Parent Span ID，形成调用树
- 追踪维度：
  - Agent 间调用链（谁调用了谁，调用几次）
  - 每轮交互延迟（发送→接收→处理→回复）
  - 消息大小与模态分布（文本/图片/文件）
  - 错误与重试次数

#### 2.3.3 Session 上下文一致性
- 平台为每个 Task 维护一个**共享 Session 上下文**（Shared Context）
- 当 Agent A 邀请 Agent B 加入 Task 时，平台自动将当前 Session Context 注入给 Agent B
- Session Context 包含：
  - Task 原始目标与用户输入
  - 历史对话摘要（或完整消息引用）
  - 已产生的 Artifact 索引
  - 共享变量/状态（如"当前审批人"、"已确认的需求列表"）
- Agent B 回复后，其产出自动合并回 Shared Context，供下一轮 Agent 使用

> **关键设计**：A2A 协议原生没有"跨 Agent Session"概念，平台通过 Adapter 层实现——对外是标准 A2A，对内维护 Task 级 Context Map。

---

### 2.4 数据分析（Analytics）

#### 2.4.1 实时看板
- Agent 在线状态总览（谁在/离线、心跳健康度）
- Task 实时大盘（进行中/已完成/失败数量、平均耗时）
- 热点 Skill 排行（哪些 Agent 被调用最频繁）
- 消息流量图（Agent 间通信拓扑可视化）

#### 2.4.2 离线分析
- Agent 协作效率分析（哪些 Agent 组合完成任务最快）
- 瓶颈定位（哪些 Agent 平均响应慢、错误率高）
- 对话轮次分布（Task 平均需要几轮交互完成）
- 成本分析（Token 消耗估算、API 调用成本分摊）

#### 2.4.3 数据导出
- 支持按 Task / Agent / 时间范围导出消息日志
- 支持 OpenTelemetry 格式导出，对接外部 APM（Jaeger / Grafana Tempo）

---

### 2.5 去中心化编排（Agent Autonomous Orchestration）

#### 2.5.1 设计定位
平台**不提供中心编排器**，编排逻辑由 Agent 自主完成。平台只提供"编排所需的工具与信息"。

#### 2.5.2 Agent 获取可协作 Agent 列表
- 平台将"Registry 查询能力"封装为一个标准工具/函数（可类比 MCP Tool），注入到每个接入 Agent 的可用工具集中
- Agent 在执行 Task 时，可主动调用该工具：
  - `query_agents(skill="code-review")` → 返回具备代码审查能力的 Agent 列表
  - `query_agents_by_description("能处理中文法律文档的 Agent")` → 语义匹配
- 返回结果已按权限过滤，Agent 只能看到自己有权限调用的 Agent

#### 2.5.3 Agent 自主决策循环
单个 Agent 作为 Task Owner 时的标准推理循环：

```
1. 接收用户/上游 Task 目标
2. 【自检】评估自身能力是否足以独立完成
3. 【发现】若不能，调用 query_agents() 发现具备相关能力的 Agent(s)
4. 【选择】根据 Agent Card 的描述、历史评分、当前负载，选择 1~N 个候选 Agent
5. 【委派】通过平台向候选 Agent 发送子 Task（携带 Shared Session Context）
6. 【等待】接收候选 Agent 的回复（Artifact / 状态更新）
7. 【整合】将回复整合到 Shared Context，评估当前进展
8. 【判断】
   - 若目标已达成 → 标记 Task COMPLETED，返回最终产物
   - 若需补充信息 → 回到步骤 4，继续询问其他 Agent
   - 若陷入僵局 → 标记 FAILED 或请求人工介入（Human-in-the-loop）
```

#### 2.5.4 终止条件与边界
- **成功终止**：Task Owner Agent 判定目标达成，向平台发送 Task COMPLETED 状态
- **失败终止**：达到最大交互轮次（默认 20 轮）、超时（默认 5 分钟）、Agent 明确声明无法完成
- **死循环检测**：平台监控同一 Task 内 Agent 间重复询问相同内容，触发熔断
- **人工介入**：Agent 主动请求 `HUMAN_ESCALATION`，平台将 Task 挂起并通知人类操作员

---

## 三、架构设计

### 3.1 总体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              接入层 (Access Layer)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Agent A    │  │  Agent B    │  │  Agent C    │  │  Human UI   │        │
│  │(需求分析)   │  │(代码生成)   │  │(测试验证)   │  │(监控/介入)  │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │                │
│         └────────────────┴────────────────┴────────────────┘                │
│                                     │                                       │
│                              A2A over HTTPS                                 │
│                              (JSON-RPC / SSE)                               │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
┌─────────────────────────────────────┼───────────────────────────────────────┐
│                           平台层 (Platform Layer)                            │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     A2A Gateway (通信代理)                           │   │
│  │  • 协议解析 / 消息路由 / 负载均衡 / 流式透传                          │   │
│  │  • 消息持久化 → 时序数据库 (如 ClickHouse / TimescaleDB)            │   │
│  │  • 速率限制 / 熔断 / 重试                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐ │
│  │   Registry Service  │  │   Task Manager      │  │   Trace Collector   │ │
│  │  (服务发现 + 心跳)   │  │  (Task 生命周期)     │  │  (链路追踪)          │ │
│  │  • PostgreSQL       │  │  • Redis 状态缓存    │  │  • OpenTelemetry    │ │
│  │  • Redis Cache      │  │  • 超时/重试调度     │  │  • Jaeger Export    │ │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘ │
│                                     │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                   Session Context Manager                            │   │
│  │  • Task 级 Shared Context 存储与同步                                  │   │
│  │  • Agent 加入/退出 Task 时的上下文注入与合并                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                   Analytics Engine                                   │   │
│  │  • 实时聚合 (Flink / Materialize)                                    │   │
│  │  • 离线分析 (Spark / DuckDB)                                         │   │
│  │  • 可视化看板 (Grafana / 自研前端)                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
┌─────────────────────────────────────┼───────────────────────────────────────┐
│                           数据层 (Data Layer)                                │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ PostgreSQL   │ │ Redis        │ │ ClickHouse   │ │ Object Store │        │
│  │ (Registry    │ │ (Cache /     │ │ (Message Log │ │ (Artifact    │        │
│  │  + Metadata) │ │  Session)    │ │  + Metrics)  │ │  Storage)    │        │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 核心组件说明

| 组件 | 职责 | 技术选型建议 |
|------|------|------------|
| **A2A Gateway** | 接收所有 Agent 消息，解析 JSON-RPC，路由到目标，透传 SSE | Python/FastAPI 或 Go/Gin |
| **Registry Service** | Agent 注册、心跳、发现查询、元数据管理 | PostgreSQL + Redis |
| **Task Manager** | Task 状态机、超时调度、参与 Agent 关系维护 | Redis（状态）+ PostgreSQL（持久化） |
| **Session Context Manager** | Task 级共享上下文的 CRUD 与版本控制 | Redis（热数据）+ PostgreSQL JSONB（归档） |
| **Trace Collector** | 接收 OpenTelemetry Span，构建调用链 | OTel Collector + ClickHouse/Jaeger |
| **Analytics Engine** | 实时/离线数据处理与可视化 | ClickHouse + Grafana / 自研前端 |

---

## 四、关键交互流程

### 4.1 Agent 注册与发现

```
Agent A 启动
    │
    ├──► POST /registry/register {Agent Card}
    │    │
    │    └──► Registry Service 写入 PostgreSQL
    │         返回注册确认 + Agent ID
    │
    ├──► 每 30s POST /registry/heartbeat
    │
    ▼
【需要协作时】
    │
    ├──► Agent A 调用内部工具 query_agents(skill="data-analysis")
    │    │
    │    └──► 平台 Registry 返回过滤后的 Agent 列表
    │         [{name: "Agent-B", url: "...", skills: [...]}, ...]
    │
    └──► Agent A 选择 Agent B，准备发起 Task
```

### 4.2 Task 创建与多 Agent 协作（含 Session 同步）

```
Agent A (Task Owner)
    │
    ├──► POST /tasks/create {goal: "分析Q3销售数据", session_context: {...}}
    │    │
    │    └──► Task Manager 创建 Task T-001，分配 Session Context S-001
    │
    ├──► POST /sendMessage
    │      {task_id: "T-001", to: "Agent-B", body: "请提供Q3原始数据"}
    │
    │         Gateway 拦截消息
    │              │
    │              ├──► 记录消息日志（Trace ID: trace-001）
    │              ├──► 从 Session Manager 获取 S-001
    │              ├──► 将 S-001 注入消息 Payload 的 _session_context 字段
    │              └──► 转发给 Agent B
    │
    ▼
Agent B 收到消息（携带 S-001）
    │
    ├──► Agent B 处理，产生结果
    │
    ├──► POST /sendMessage
    │      {task_id: "T-001", to: "Agent-A", body: "原始数据如下...", artifact: {...}}
    │
    │         Gateway 拦截
    │              │
    │              ├──► 记录消息日志
    │              ├──► 将 Agent B 的产出合并到 S-001
    │              └──► 转发给 Agent A
    │
    ▼
Agent A 评估结果，决定：
    ├── 已完成 → POST /tasks/T-001/complete
    ├── 需继续问 Agent C → 重复上述流程（S-001 自动携带）
    └── 无法推进 → POST /tasks/T-001/escalate（人工介入）
```

### 4.3 链路追踪数据流

```
Agent A ──► Gateway ──► Agent B
    │          │            │
    │          ▼            │
    │    ┌──────────┐       │
    │    │ OTel Span│       │
    │    │ - trace_id      │
    │    │ - span_id       │
    │    │ - parent_id     │
    │    │ - agent_from    │
    │    │ - agent_to      │
    │    │ - task_id       │
    │    │ - latency_ms    │
    │    │ - msg_size      │
    │    └────┬─────┘       │
    │         ▼             │
    │    OTel Collector ──► ClickHouse / Jaeger
    │
    └── 最终在看板展示完整调用树
```

---

## 五、安全与权限模型（待补充设计）

### 5.1 认证
- Agent 接入平台需携带 JWT Token（平台签发，含 Agent ID、所属团队、权限范围）
- 支持 mTLS（机器对机器高安全场景）

### 5.2 授权（RBAC）
- **Namespace/Project 隔离**：Agent 只能发现同 Namespace 内的 Agent（除非显式授权跨 Namespace）
- **Skill 级 ACL**：Agent A 可以被允许/禁止调用具有特定 Skill 的 Agent
- **Rate Limiting**：按 Agent、按 Skill、按 Namespace 限制调用频次

### 5.3 审计
- 所有消息、注册、发现查询均记录审计日志
- 审计日志不可篡改，独立存储，保留 1 年+

---

## 六、需要补充与待决策的事项

### 6.1 概念澄清：MCP vs Registry 查询
> 原文需求："agent 知道了调用什么 mcp 能获取到它可以 access 到的 agents"

**建议调整**：Agent 发现其他 Agent 的能力应通过**平台的 Registry 查询工具**提供，而非 MCP。
- MCP 是 Agent ↔ Tool/数据的连接标准
- Registry 查询是 Agent ↔ Agent 发现能力

**实现方式**：平台为每个接入 Agent 注入一个名为 `discover_agents` 的 Tool（内部实现为调用 Registry Service API），Agent 通过调用这个 Tool 获取可协作 Agent 列表。

### 6.2 待补充的关键需求

| 领域 | 缺失项 | 重要性 |
|------|--------|--------|
| **人机协同** | Agent 无法解决时如何请求人工介入？人工操作界面长什么样？ | ⭐⭐⭐⭐⭐ |
| **容错** | Agent 挂掉、消息丢失、平台重启时的恢复机制 | ⭐⭐⭐⭐⭐ |
| **成本管控** | 是否限制单 Task 的最大 Token 消耗/最大调用次数？ | ⭐⭐⭐⭐ |
| **隐私/合规** | 消息持久化是否涉及敏感数据脱敏？GDPR 删除权？ | ⭐⭐⭐⭐ |
| **多模态** | Agent 交换图片/文件时，平台是否做存储/转码/病毒扫描？ | ⭐⭐⭐ |
| **灰度/AB** | Agent 新版本上线时，是否支持按流量比例灰度路由？ | ⭐⭐⭐ |

### 6.3 技术待决策

| 问题 | 选项 | 影响 |
|------|------|------|
| Agent 与平台的连接方式 | HTTP 短连接 vs WebSocket 长连接 vs gRPC | 实时性、资源消耗、SDK 复杂度 |
| Session Context 存储 | Redis（快但容量有限） vs PostgreSQL JSONB（大但慢） | 大 Task 上下文（如长文档）的承载能力 |
| 消息持久化格式 | 原始 JSON  vs  压缩存储  vs  对象存储引用 | 存储成本、查询灵活性 |
| 部署模式 | 单体服务 vs 微服务拆分 | 初期迭代速度 vs 长期可扩展性 |

---

## 七、里程碑规划建议

| 阶段 | 周期 | 目标 |
|------|------|------|
| **MVP** | 2~3 周 | Registry（注册/心跳/查询）+ Gateway（消息代理+记录）+ 简单状态看板 |
| **V1.0** | 1.5~2 月 | + Task 生命周期管理 + Session Context 同步 + 链路追踪 + 权限模型 |
| **V1.5** | 3~4 月 | + 语义搜索 + 数据分析看板 + 人机介入界面 + 容错恢复 |
| **V2.0** | 6 月+ | + 多 Namespace 隔离 + 成本管控 + 灰度发布 + 外部 A2A Agent 接入 |

---

## 八、总结

本平台的核心创新点在于：

1. **在 A2A 协议之上构建了生产级基础设施层**（发现、代理、追踪、分析），而非替代 A2A
2. **坚持去中心化编排哲学**，Agent 自主决策、自主协商，平台只做"赋能"不做"指挥"
3. **Task 级 Session 一致性设计**，解决了多 Agent 协作中的上下文割裂问题
4. **数据天然归集**，为后续优化 Agent 协作策略、评估 Agent 质量提供了数据基础

**最大风险点**：去中心化编排的"终止条件"和"死循环检测"需要精细设计，否则 Agent 间可能陷入无意义的反复询问。
