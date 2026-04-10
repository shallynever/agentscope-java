# AgentScope Java 示例目录

本目录包含 AgentScope Java 框架的各种示例，帮助开发者快速理解和学习框架的核心功能。

## 示例概览

| 示例名称 | 主要功能 | 关键技术 | AgentScope 特性 |
|---------|---------|---------|----------------|
| [quickstart](#1-quickstart) | 核心概念入门 | Spring Boot WebFlux | ReActAgent, Toolkit, Hooks, Session |
| [a2a](#2-a2a) | 智能体间通信协议 | Nacos, A2A Protocol | A2aAgent, AgentCard |
| [agui](#3-agui) | 前端集成协议 | WebFlux, AG-UI | AguiAgentRegistry |
| [advanced](#4-advanced) | RAG、记忆、HITL 高级功能 | Elasticsearch, Mem0 | Knowledge, LongTermMemory |
| [chat-tts](#5-chat-tts) | 语音输出聊天 | WebFlux, WebSocket | TTSHook, RealtimeTTS |
| [chat-completions-web](#6-chat-completions-web) | OpenAI 兼容 API | Spring MVC | Chat Completions Starter |
| [hitl-chat](#7-hitl-chat) | 人机交互聊天 | WebFlux, MySQL | ToolConfirmation, Interrupt |
| [boba-tea-shop](#8-boba-tea-shop) | 多智能体业务系统 | Spring Boot, Nacos, Vue | 多智能体协作, A2A, MCP |
| [werewolf](#9-werewolf) | 狼人杀游戏模拟 | WebFlux, SSE | MsgHub, FanoutPipeline |
| [werewolf-hitl](#10-werewolf-hitl) | 真人参与狼人杀 | WebFlux | WebUserInput, HITL |
| [micronaut](#11-micronaut) | Micronaut 框架集成 | Micronaut | Factory Bean 注入 |
| [quarkus](#12-quarkus) | Quarkus 框架集成 | Quarkus | CDI 注入 |
| [model-request-compression](#13-model-request-compression) | HTTP 请求压缩 | Brotli, Zstd | 自定义传输层 |
| [plan-notebook](#14-plan-notebook) | 任务规划笔记本 | WebFlux, SSE | PlanNotebook |
| [multiagent-patterns](#15-multiagent-patterns) | 多智能体设计模式 | StateGraph | Pipeline, Routing, Skills |

---

## 详细说明

### 1. quickstart

**路径**: `quickstart/`

**功能**: 核心功能演示集合，涵盖 AgentScope 的基础概念。

**使用场景**: 学习 AgentScope 基础概念的最佳起点。

**子示例说明**:

| 子示例 | 功能描述 |
|-------|---------|
| BasicChatExample | 最简单的智能体对话，演示 ReActAgent 的基本用法 |
| ToolCallingExample | 使用 `@Tool` 注解定义工具并让智能体调用 |
| StructuredOutputExample | 从自然语言生成结构化输出（JSON 对象） |
| ToolGroupExample | 智能体自主管理工具组，使用 meta-tool 动态切换工具集 |
| McpToolExample | MCP (Model Context Protocol) 工具服务器集成示例 |
| HookExample | 事件钩子系统，用于监控智能体执行过程 |
| StreamingWebExample | Spring Boot + SSE 流式输出示例 |
| SessionExample | JsonSession 持久化会话，支持对话历史保存 |
| InterruptionExample | 用户中断智能体执行机制演示 |

**关键技术**: Spring Boot WebFlux, DashScope LLM, MCP Protocol

---

### 2. a2a

**路径**: `a2a/`

**功能**: 演示 A2A (Agent-to-Agent) 协议，实现智能体间的通信与服务发现。

**使用场景**:
- 跨服务智能体调用
- 微服务架构下的智能体协作
- 服务注册与发现

**关键技术**: Spring Boot Web, Nacos Service Discovery, A2A Protocol

**核心特性**: A2aAgent, AgentCard, NacosAgentCardResolver, WellKnownAgentCardResolver

---

### 3. agui

**路径**: `agui/`

**功能**: 演示 AG-UI 协议，实现前端与智能体的实时通信。

**使用场景**:
- Web 前端集成
- 多智能体选择与切换
- 实时流式响应展示

**关键技术**: Spring Boot WebFlux, AG-UI Protocol

**核心特性**: AguiAgentRegistryCustomizer, agent factory 注册, WebFlux 流式输出

---

### 4. advanced

**路径**: `advanced/`

**功能**: RAG、长时记忆、人机交互等高级特性演示。

**子示例说明**:

| 子示例 | 功能描述 | 使用场景 |
|-------|---------|---------|
| RAGExample | 检索增强生成 (RAG) 基础示例 | 知识库问答系统 |
| BailianRAGExample | 阿里云百炼 RAG 集成 | 企业级知识库解决方案 |
| ElasticsearchRAGExample | Elasticsearch 向量检索 RAG | 文档检索与问答 |
| Mem0Example | Mem0 长期记忆集成 | 对话历史持久化与用户画像 |
| ReMeExample | 记忆管理示例 | 智能体记忆操作 |
| AutoMemoryExample | 自动上下文压缩与长期记忆 | 长对话场景下的上下文管理 |
| LangfuseExample | Langfuse 可观测性集成 | 追踪、监控与调试智能体行为 |
| StudioExample | AgentScope Studio 集成 | 可视化智能体开发与管理 |
| RoutingByToolCallsExample | 基于工具调用的路由 | 动态路由决策 |
| HitlInteractionExample | 人机交互示例 | 动态 UI 组件与危险操作确认 |

**关键技术**: Elasticsearch, Mem0, Bailian RAG, Langfuse, Spring Boot WebFlux

---

### 5. chat-tts

**路径**: `chat-tts/`

**功能**: 实时文字转语音流式输出，实现语音 AI 助手。

**使用场景**:
- 语音 AI 助手应用
- 实时音频流播放
- 新消息自动中断当前 TTS

**关键技术**: Spring Boot WebFlux, DashScope TTS, WebSocket, SSE

**核心特性**: TTSHook, DashScopeRealtimeTTSModel, 流式响应, 音频回调

---

### 6. chat-completions-web

**路径**: `chat-completions-web/`

**功能**: 提供 OpenAI 兼容的 Chat Completions API 端点。

**使用场景**:
- 替换 OpenAI API 作为后端
- 流式与非流式聊天补全
- 工具调用 schema 支持

**关键技术**: Spring Boot MVC, OpenAI-compatible API

**核心特性**: Chat Completions Web Starter, 工具挂起机制, 流式输出

---

### 7. hitl-chat

**路径**: `hitl-chat/`

**功能**: 支持 MCP 工具动态配置、智能体中断、危险工具确认的人机交互聊天应用。

**使用场景**:
- 动态 MCP 工具配置
- 对话过程中中断智能体执行
- 敏感操作的人工确认

**关键技术**: Spring Boot WebFlux, MySQL, MCP Protocol

**核心特性**: ToolConfirmationHook, agent interrupt, MCP 客户端管理, SkillRepository

---

### 8. boba-tea-shop

**路径**: `boba-tea-shop/`

**功能**: 完整的多智能体业务系统演示 - 珍珠奶茶店智能助手。

**使用场景**: 学习复杂多智能体系统架构的最佳示例。

**系统组件**:

| 组件 | 路径 | 职责 |
|------|------|------|
| supervisor-agent | `boba-tea-shop/supervisor-agent/` | 入口协调器，使用 A2A 协议路由请求 |
| business-sub-agent | `boba-tea-shop/business-sub-agent/` | 订单管理、反馈处理，通过 MCP 提供能力 |
| consult-sub-agent | `boba-tea-shop/consult-sub-agent/` | 产品咨询，集成百炼 RAG 知识库 |
| business-mcp-server | `boba-tea-shop/business-mcp-server/` | MCP 工具服务器，提供业务工具 |

**业务能力**:
- 自然语言智能下单
- 订单查询与管理
- 产品知识库咨询
- 用户反馈处理
- 业务报表生成

**关键技术**: Spring Boot, MySQL, Nacos, Vue 3, MCP, A2A, Bailian RAG, Mem0

**核心特性**: 多智能体协作, A2A 协议, MCP 协议, RAG, AutoContextMemory, Session 持久化

---

### 9. werewolf

**路径**: `werewolf/`

**功能**: 多智能体狼人杀游戏模拟，AI 智能体扮演各角色进行游戏。

**使用场景**: 学习多智能体协调、消息分发与角色扮演。

**关键技术**: Spring Boot WebFlux, SSE, i18n

**核心特性**: MsgHub, FanoutPipeline, 结构化输出, 多智能体协调

---

### 10. werewolf-hitl

**路径**: `werewolf-hitl/`

**功能**: 支持真人玩家参与的狼人杀游戏。

**使用场景**: 人机混合游戏场景，学习 HITL 集成模式。

**关键技术**: Spring Boot WebFlux, SSE, WebUserInput

**核心特性**: HITL 集成, WebUserInput, 事件可见性控制

---

### 11. micronaut

**路径**: `micronaut/`

**功能**: AgentScope 与 Micronaut 框架的集成示例。

**使用场景**:
- Micronaut 项目集成 AgentScope
- 依赖注入与 Bean 配置
- 多 LLM 提供商配置

**关键技术**: Micronaut, ApplicationContext

**核心特性**: Micronaut Factory, Bean 注入, YAML 配置

---

### 12. quarkus

**路径**: `quarkus/`

**功能**: AgentScope 与 Quarkus 框架的集成示例。

**使用场景**:
- Quarkus 项目集成 AgentScope
- Native Image 支持
- CDI Bean 注入

**关键技术**: Quarkus, JAX-RS, CDI

**核心特性**: Quarkus Bean 注入, REST API

---

### 13. model-request-compression

**路径**: `model-request-compression/`

**功能**: LLM HTTP 请求与响应的压缩支持。

**使用场景**:
- 减少长对话的数据传输量
- 降低带宽成本
- 提升响应速度

**关键技术**: Brotli, Zstd, GZIP, OkHttp

**核心特性**: 自定义 HTTP 传输层, 压缩工具

---

### 14. plan-notebook

**路径**: `plan-notebook/`

**功能**: 任务规划 Web 应用，演示 PlanNotebook 功能。

**使用场景**:
- 创建、更新、追踪任务计划与子任务
- 人机交互式计划审核
- SSE 流式推送计划变更

**关键技术**: Spring Boot WebFlux, SSE

**核心特性**: PlanNotebook, Plan Tools, HITL Plan Review, 流式输出

---

### 15. multiagent-patterns

**路径**: `multiagent-patterns/`

**功能**: 多智能体协作设计模式演示集合。

**子示例说明**:

#### 15.1 handoffs - 交接模式

**路径**: `multiagent-patterns/handoffs/`

**功能**: 销售与客服智能体通过交接工具转移控制权。

**核心特性**: StateGraph, Handoff Tools, ToolContext, 条件路由

---

#### 15.2 pipeline - 流水线模式

**路径**: `multiagent-patterns/pipeline/`

**功能**: 顺序、并行、循环流水线执行模式。

**核心特性**: SequentialAgent, ParallelAgent, LoopAgent, Spring AI Alibaba Flow Agents

---

#### 15.3 routing - 路由模式

**路径**: `multiagent-patterns/routing/`

**功能**: 用户查询分类并路由到专家智能体（GitHub、Notion、Slack）。

**核心特性**: AgentScopeRoutingAgent, StateGraph 路由, 并行智能体调用

---

#### 15.4 skills - 技能模式

**路径**: `multiagent-patterns/skills/`

**功能**: SQL 助手渐进式技能加载示例。

**核心特性**: ClasspathSkillRepository, SkillBox, read_skill 工具, SKILL.md 格式

---

#### 15.5 subagent - 子智能体模式

**路径**: `multiagent-patterns/subagent/`

**功能**: 技术尽职调查助手，通过 Task 工具委托子任务。

**核心特性**: TaskTool, TaskOutputTool, 子智能体注册, Markdown Agent Spec

---

#### 15.6 supervisor - 监督者模式

**路径**: `multiagent-patterns/supervisor/`

**功能**: 个人助理协调日历和邮件智能体。

**核心特性**: Toolkit.registration().subAgent(), 专业智能体作为工具注册

---

#### 15.7 workflow - 工作流模式

**路径**: `multiagent-patterns/workflow/`

**功能**: 使用 StateGraph 自定义执行流程。

**核心特性**: StateGraph, RAG 工作流, SQL Agent 工作流, 确定性节点与智能体节点

---

## 学习路径建议

### 入门阶段

1. **quickstart** → 从 BasicChatExample 开始，逐步学习 ToolCallingExample、HookExample
2. **advanced/RAGExample** → 了解 RAG 基础
3. **hitl-chat** → 学习人机交互模式

### 进阶阶段

4. **multiagent-patterns/skills** → 学习技能系统
5. **multiagent-patterns/pipeline** → 掌握流水线编排
6. **boba-tea-shop** → 理解完整业务系统架构

### 高级阶段

7. **multiagent-patterns/supervisor** → 多智能体协作模式
8. **a2a** + **agui** → 分布式智能体与前端集成
9. **werewolf** → 复杂多智能体游戏系统

---

## 运行示例

每个示例目录下都有独立的 `pom.xml`，可以单独运行：

```bash
# 进入示例目录
cd agentscope-examples/quickstart

# 运行特定示例
mvn spring-boot:run

# 或直接运行主类
mvn exec:java -Dexec.mainClass="io.agentscope.examples.quickstart.BasicChatExample"
```

> 注意：运行前需要配置 LLM API Key，请参考各示例目录下的 `application.yml` 配置文件。