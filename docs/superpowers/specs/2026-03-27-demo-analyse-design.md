# Demo-Analyse 项目设计文档

## Context

创建一个演示项目，展示 ReActAgent 如何使用 SkillBox 进行业务数据分析。该项目结合 `skills` 示例的 SkillBox 使用模式和 `hitl-chat` 的 Web 界面风格，提供一个完整的交互式演示。

**目标**：
- 演示 SkillBox 与 ReActAgent 的集成
- 展示自定义 Skill 和 Tool 的开发方式
- 提供可交互的 Web 界面用于演示

---

## Architecture

### 项目结构

```
demo-analyse/
├── pom.xml
├── src/main/
│   ├── java/io/agentscope/examples/demoanalyse/
│   │   ├── DemoAnalyseApplication.java      # Spring Boot 启动类
│   │   ├── config/
│   │   │   └── AgentConfig.java             # Agent + SkillBox 配置
│   │   ├── controller/
│   │   │   └── ChatController.java          # REST API 端点
│   │   ├── dto/
│   │   │   ├── ChatEvent.java               # SSE 事件类型定义
│   │   │   └── ChatRequest.java             # 请求 DTO
│   │   ├── service/
│   │   │   └── AgentService.java            # Agent 生命周期管理
│   │   └── tools/
│   │       └── DataAnalysisTools.java       # 三个数据分析工具实现
│   └── resources/
│       ├── application.yml                  # 应用配置
│       ├── skills/
│       │   └── data_insight/
│       │       └── SKILL.md                 # 数据洞察技能定义
│       └── static/
│           ├── index.html                   # 主页面
│           ├── css/style.css                # 样式
│           └── js/app.js                    # 前端逻辑
```

### 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Spring Boot 3.x + WebFlux |
| Agent 框架 | AgentScope Core |
| 前端 | 原生 JavaScript + SSE |
| 构建工具 | Maven |
| Java 版本 | Java 17 |

---

## Components

### 1. 数据洞察 Skill (data_insight)

**位置**: `src/main/resources/skills/data_insight/SKILL.md`

**SKILL.md 内容**:
```markdown
---
name: data_insight
description: 业务数据洞察分析技能，用于分析销售趋势、用户行为、营收指标等业务数据
---

# 数据洞察分析技能

## 概述
本技能帮助用户进行业务数据分析，自动执行三个核心步骤完成从问题到洞察的全流程。

## 核心工具

### 1. analyze_feasibility - 可行性分析
评估用户查询的分析可行性，识别数据需求。

**输入参数**:
- `query`: 用户的分析请求
- `context`: 可选的上下文信息

**输出**:
- 可行性评估结果
- 建议的数据源
- 分析方法建议

### 2. fetch_business_data - 获取数据
根据分析需求获取相关业务数据。

**输入参数**:
- `data_type`: 数据类型 (sales/users/revenue)
- `time_range`: 时间范围 (e.g., "last_30_days", "q1_2024")
- `metrics`: 需要的指标列表

**输出**:
- JSON 格式的业务数据

### 3. generate_insight_report - 生成报告
基于分析结果生成结构化报告。

**输入参数**:
- `data`: 分析数据
- `analysis_focus`: 分析重点
- `output_format`: 输出格式 (markdown/json)

**输出**:
- 结构化分析报告

## 使用流程
1. 用户提出业务分析问题
2. 系统自动进行可行性分析
3. 获取相关业务数据
4. 生成洞察报告

## 示例问题
- "分析上个月的销售趋势"
- "用户增长情况如何？"
- "本季度营收表现分析"
```

### 2. DataAnalysisTools.java

三个工具的具体实现：

```java
public class DataAnalysisTools {

    @Tool(description = "分析用户查询的可行性，评估数据需求")
    public String analyzeFeasibility(
        @ToolParam(name = "query", description = "用户的分析请求") String query,
        @ToolParam(name = "context", description = "可选上下文") String context
    ) {
        // 返回模拟的可行性分析结果
    }

    @Tool(description = "获取业务数据")
    public String fetchBusinessData(
        @ToolParam(name = "data_type", description = "数据类型: sales/users/revenue") String dataType,
        @ToolParam(name = "time_range", description = "时间范围") String timeRange,
        @ToolParam(name = "metrics", description = "指标列表") String metrics
    ) {
        // 返回模拟的业务数据 JSON
    }

    @Tool(description = "生成分析报告")
    public String generateInsightReport(
        @ToolParam(name = "data", description = "分析数据") String data,
        @ToolParam(name = "analysis_focus", description = "分析重点") String analysisFocus
    ) {
        // 返回 Markdown 格式报告
    }
}
```

### 3. AgentConfig.java

SkillBox 与 Agent 集成配置：

```java
@Configuration
public class AgentConfig {

    @Bean
    public SkillBox skillBox(Toolkit toolkit) {
        SkillBox skillBox = new SkillBox(toolkit);

        // 加载技能
        ClasspathSkillRepository repository = new ClasspathSkillRepository("skills");
        List<AgentSkill> skills = repository.getAllSkills();

        for (AgentSkill skill : skills) {
            skillBox.registration()
                .skill(skill)
                .tool(new DataAnalysisTools())  // 绑定工具到技能
                .apply();
        }

        return skillBox;
    }

    @Bean
    public ReActAgent agent(SkillBox skillBox, Toolkit toolkit, Model model) {
        return ReActAgent.builder()
            .name("data_analyst")
            .sysPrompt(DATA_ANALYST_PROMPT)
            .model(model)
            .toolkit(toolkit)
            .skillBox(skillBox)
            .memory(new InMemoryMemory())
            .build();
    }
}
```

### 4. ChatController.java

REST API 端点：

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/chat` | POST | 发送消息，返回 SSE 流 |
| `/api/chat/session/{sessionId}` | DELETE | 清除会话 |
| `/api/skills` | GET | 获取可用技能列表 |

### 5. 前端界面

基于 hitl-chat 风格，主要功能：
- SSE 流式响应显示
- 工具调用过程可视化
- 技能状态指示器
- 响应式布局

---

## Data Flow

```
用户输入 "分析上个月销售趋势"
    ↓
前端 POST /api/chat
    ↓
AgentService.chat()
    ↓
ReActAgent.stream()
    ↓
[Agent 推理] 判断需要 data_insight 技能
    ↓
调用 load_skill_through_path("data_insight_classpath-skills", "SKILL.md")
    ↓
技能激活，工具可用
    ↓
调用 analyze_feasibility("分析上个月销售趋势")
    ↓ SSE 事件: TOOL_USE
返回可行性分析结果
    ↓ SSE 事件: TOOL_RESULT
调用 fetch_business_data("sales", "last_month", "revenue,orders")
    ↓ SSE 事件: TOOL_USE
返回模拟销售数据
    ↓ SSE 事件: TOOL_RESULT
调用 generate_insight_report(data, "销售趋势")
    ↓ SSE 事件: TOOL_USE
生成分析报告
    ↓ SSE 事件: TOOL_RESULT
Agent 整合结果返回用户
    ↓ SSE 事件: TEXT/COMPLETE
前端渲染最终报告
```

---

## Error Handling

- **技能加载失败**: 返回错误提示，Agent 继续处理
- **工具执行异常**: 记录日志，返回错误信息给 Agent
- **SSE 连接中断**: 前端显示断开状态，提供重连按钮

---

## Testing

### 单元测试
- `DataAnalysisTools` 各工具方法测试
- `AgentConfig` 配置加载测试

### 集成测试
- Agent 完整流程测试
- SSE 流式响应测试

### 手动验证
1. 启动应用: `mvn spring-boot:run`
2. 访问 `http://localhost:8080`
3. 输入分析问题，观察工具调用过程
4. 验证报告生成结果

---

## Implementation Order

1. 创建 Maven 项目结构和 pom.xml
2. 实现后端核心类 (Application, Config, Controller, Service, Tools)
3. 创建 SKILL.md 技能定义文件
4. 实现前端界面 (HTML, CSS, JS)
5. 配置 application.yml
6. 测试验证

---

## Files to Create

| 文件路径 | 说明 |
|----------|------|
| `pom.xml` | Maven 配置 |
| `src/main/java/.../DemoAnalyseApplication.java` | 启动类 |
| `src/main/java/.../config/AgentConfig.java` | Agent 配置 |
| `src/main/java/.../controller/ChatController.java` | REST 控制器 |
| `src/main/java/.../dto/ChatEvent.java` | SSE 事件定义 |
| `src/main/java/.../dto/ChatRequest.java` | 请求 DTO |
| `src/main/java/.../service/AgentService.java` | Agent 服务 |
| `src/main/java/.../tools/DataAnalysisTools.java` | 数据分析工具 |
| `src/main/resources/application.yml` | 应用配置 |
| `src/main/resources/skills/data_insight/SKILL.md` | 技能定义 |
| `src/main/resources/static/index.html` | 主页面 |
| `src/main/resources/static/css/style.css` | 样式文件 |
| `src/main/resources/static/js/app.js` | 前端逻辑 |