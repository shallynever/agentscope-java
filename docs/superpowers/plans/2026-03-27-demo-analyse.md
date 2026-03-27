# Demo-Analyse 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个演示 ReActAgent 使用 SkillBox 进行业务数据分析的 Web 应用

**Architecture:** Spring Boot WebFlux 后端 + 原生 JavaScript 前端，通过 SSE 实现实时流式响应。Agent 使用 SkillBox 管理数据洞察技能，技能绑定三个工具：可行性分析、获取数据、生成报告。

**Tech Stack:** Java 17, Spring Boot 3.x, WebFlux, AgentScope Core, 原生 JavaScript, SSE

---

## File Structure

```
demo-analyse/
├── pom.xml
├── src/main/
│   ├── java/io/agentscope/examples/demoanalyse/
│   │   ├── DemoAnalyseApplication.java
│   │   ├── config/AgentConfig.java
│   │   ├── controller/ChatController.java
│   │   ├── dto/ChatEvent.java
│   │   ├── dto/ChatRequest.java
│   │   ├── service/AgentService.java
│   │   └── tools/DataAnalysisTools.java
│   └── resources/
│       ├── application.yml
│       ├── skills/data_insight/SKILL.md
│       └── static/
│           ├── index.html
│           ├── css/style.css
│           └── js/app.js
```

---

### Task 1: 创建项目目录和 pom.xml

**Files:**
- Create: `agentscope-examples/demo-analyse/pom.xml`

- [ ] **Step 1: 创建项目目录**

```bash
mkdir -p agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/{config,controller,dto,service,tools}
mkdir -p agentscope-examples/demo-analyse/src/main/resources/{skills/data_insight,static/css,static/js}
```

- [ ] **Step 2: 创建 pom.xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  ~ Copyright 2024-2026 the original author or authors.
  ~
  ~ Licensed under the Apache License, Version 2.0 (the "License");
  ~ you may not use this file except in compliance with the License.
  ~ You may obtain a copy of the License at
  ~
  ~     http://www.apache.org/licenses/LICENSE-2.0
  ~
  ~ Unless required by applicable law or agreed to in writing, software
  ~ distributed under the License is distributed on an "AS IS" BASIS,
  ~ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  ~ See the License for the specific language governing permissions and
  ~ limitations under the License.
-->

<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>io.agentscope</groupId>
        <artifactId>agentscope-examples</artifactId>
        <version>${revision}</version>
        <relativePath>../pom.xml</relativePath>
    </parent>

    <groupId>io.agentscope.examples</groupId>
    <artifactId>demo-analyse</artifactId>
    <packaging>jar</packaging>

    <name>AgentScope Java - Examples - Demo Analyse</name>
    <description>Demo project showcasing ReActAgent with SkillBox for data analysis</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.deploy.skip>true</maven.deploy.skip>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring.boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <dependency>
            <groupId>io.agentscope</groupId>
            <artifactId>agentscope-core</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-webflux</artifactId>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>${spring.boot.version}</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>
```

- [ ] **Step 3: 提交**

```bash
git add agentscope-examples/demo-analyse/pom.xml
git commit -m "feat(demo-analyse): add Maven project configuration"
```

---

### Task 2: 创建启动类和配置文件

**Files:**
- Create: `agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/DemoAnalyseApplication.java`
- Create: `agentscope-examples/demo-analyse/src/main/resources/application.yml`

- [ ] **Step 1: 创建 Spring Boot 启动类**

```java
/*
 * Copyright 2024-2026 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.agentscope.examples.demoanalyse;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Demo Analyse Application - showcases ReActAgent with SkillBox for data analysis.
 */
@SpringBootApplication
public class DemoAnalyseApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoAnalyseApplication.class, args);
    }
}
```

- [ ] **Step 2: 创建 application.yml**

```yaml
server:
  port: 8081

spring:
  application:
    name: demo-analyse

dashscope:
  api-key: ${AI_DASHSCOPE_API_KEY:}
  model-name: qwen-plus

logging:
  level:
    io.agentscope: INFO
    io.agentscope.examples: DEBUG
```

- [ ] **Step 3: 提交**

```bash
git add agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/DemoAnalyseApplication.java
git add agentscope-examples/demo-analyse/src/main/resources/application.yml
git commit -m "feat(demo-analyse): add Spring Boot application entry and config"
```

---

### Task 3: 创建数据分析工具类

**Files:**
- Create: `agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/tools/DataAnalysisTools.java`

- [ ] **Step 1: 创建 DataAnalysisTools 类**

```java
/*
 * Copyright 2024-2026 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.agentscope.examples.demoanalyse.tools;

import io.agentscope.core.tool.Tool;
import io.agentscope.core.tool.ToolParam;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

/**
 * Data analysis tools for business data insight.
 *
 * <p>Contains three tools:
 * <ul>
 *   <li>analyzeFeasibility - Analyze query feasibility</li>
 *   <li>fetchBusinessData - Fetch business data</li>
 *   <li>generateInsightReport - Generate analysis report</li>
 * </ul>
 */
public class DataAnalysisTools {

    private static final Random RANDOM = new Random();

    /**
     * Analyze the feasibility of a user query.
     */
    @Tool(description = "分析用户查询的可行性，评估数据需求并返回分析建议")
    public String analyzeFeasibility(
            @ToolParam(name = "query", description = "用户的分析请求") String query,
            @ToolParam(name = "context", description = "可选的上下文信息", required = false) String context) {

        StringBuilder result = new StringBuilder();
        result.append("## 可行性分析报告\n\n");
        result.append("**查询内容**: ").append(query).append("\n\n");

        // 分析数据类型
        String dataType = detectDataType(query);
        result.append("**识别数据类型**: ").append(dataType).append("\n\n");

        // 可行性评估
        result.append("**可行性评估**: ✅ 可行\n\n");

        // 建议的数据源
        result.append("**建议数据源**:\n");
        result.append("- 数据类型: ").append(dataType).append("\n");
        result.append("- 时间范围: 最近30天\n");
        result.append("- 指标: 根据查询自动确定\n\n");

        // 分析方法建议
        result.append("**分析方法建议**:\n");
        result.append("1. 获取").append(dataType).append("相关数据\n");
        result.append("2. 进行趋势分析\n");
        result.append("3. 生成洞察报告\n");

        return result.toString();
    }

    /**
     * Fetch business data based on analysis requirements.
     */
    @Tool(description = "获取业务数据，返回模拟的销售、用户或营收数据")
    public String fetchBusinessData(
            @ToolParam(name = "data_type", description = "数据类型: sales/users/revenue") String dataType,
            @ToolParam(name = "time_range", description = "时间范围，如 last_30_days, last_quarter") String timeRange,
            @ToolParam(name = "metrics", description = "需要的指标列表，逗号分隔", required = false) String metrics) {

        StringBuilder result = new StringBuilder();
        result.append("## 业务数据\n\n");
        result.append("**数据类型**: ").append(dataType).append("\n");
        result.append("**时间范围**: ").append(timeRange).append("\n\n");

        // 生成模拟数据
        switch (dataType.toLowerCase()) {
            case "sales" -> {
                result.append("### 销售数据\n");
                result.append("| 日期 | 订单数 | 销售额 | 客单价 |\n");
                result.append("|------|--------|--------|--------|\n");
                for (int i = 0; i < 7; i++) {
                    int orders = 100 + RANDOM.nextInt(50);
                    double amount = orders * (80 + RANDOM.nextInt(40));
                    result.append(String.format("| Day-%d | %d | ¥%.0f | ¥%.0f |\n",
                            i + 1, orders, amount, amount / orders));
                }
                result.append("\n**汇总**: 总订单数 875，总销售额 ¥73,500，平均客单价 ¥84\n");
            }
            case "users" -> {
                result.append("### 用户数据\n");
                result.append("| 日期 | 新增用户 | 活跃用户 | 转化率 |\n");
                result.append("|------|----------|----------|--------|\n");
                for (int i = 0; i < 7; i++) {
                    int newUsers = 200 + RANDOM.nextInt(100);
                    int activeUsers = 1000 + RANDOM.nextInt(300);
                    double rate = 2.5 + RANDOM.nextDouble() * 2;
                    result.append(String.format("| Day-%d | %d | %d | %.1f%% |\n",
                            i + 1, newUsers, activeUsers, rate));
                }
                result.append("\n**汇总**: 新增用户 1,890，平均日活 1,150，平均转化率 3.2%\n");
            }
            case "revenue" -> {
                result.append("### 营收数据\n");
                result.append("| 渠道 | 收入 | 占比 | 同比增长 |\n");
                result.append("|------|------|------|----------|\n");
                String[] channels = {"线上商城", "线下门店", "合作伙伴", "其他"};
                int total = 0;
                int[] revenues = new int[4];
                for (int i = 0; i < 4; i++) {
                    revenues[i] = 50000 + RANDOM.nextInt(30000);
                    total += revenues[i];
                }
                for (int i = 0; i < 4; i++) {
                    double percent = (double) revenues[i] / total * 100;
                    double growth = 5 + RANDOM.nextDouble() * 15;
                    result.append(String.format("| %s | ¥%d | %.1f%% | +%.1f%% |\n",
                            channels[i], revenues[i], percent, growth));
                }
                result.append("\n**汇总**: 总营收 ¥").append(total).append("，同比增长 +12.5%\n");
            }
            default -> {
                result.append("无法识别的数据类型，返回默认数据...\n");
                result.append("- 数据点1: 100\n");
                result.append("- 数据点2: 150\n");
                result.append("- 数据点3: 200\n");
            }
        }

        return result.toString();
    }

    /**
     * Generate insight report based on analysis.
     */
    @Tool(description = "基于分析数据生成结构化的洞察报告")
    public String generateInsightReport(
            @ToolParam(name = "data", description = "分析数据内容") String data,
            @ToolParam(name = "analysis_focus", description = "分析重点，如趋势、对比、异常等") String analysisFocus) {

        StringBuilder result = new StringBuilder();
        result.append("# 数据洞察报告\n\n");

        result.append("## 执行摘要\n\n");
        result.append("本报告基于").append(analysisFocus).append("分析，识别关键业务洞察和行动建议。\n\n");

        result.append("## 关键发现\n\n");
        result.append("### 1. 趋势分析\n");
        result.append("- 整体呈上升趋势，周环比增长 8.5%\n");
        result.append("- 工作日表现优于周末，差异约 15%\n");
        result.append("- 高峰时段集中在 10:00-14:00\n\n");

        result.append("### 2. 异常识别\n");
        result.append("- Day-4 出现数据低谷，需调查原因\n");
        result.append("- 转化率在 Day-6 有明显提升，可复用策略\n\n");

        result.append("### 3. 机会点\n");
        result.append("- 用户活跃度有提升空间\n");
        result.append("- 客单价可通过推荐系统优化\n\n");

        result.append("## 行动建议\n\n");
        result.append("1. **短期行动** (1-2周)\n");
        result.append("   - 调查 Day-4 数据异常原因\n");
        result.append("   - 分析 Day-6 转化率提升因素\n\n");
        result.append("2. **中期优化** (1-2月)\n");
        result.append("   - 优化高峰时段服务资源\n");
        result.append("   - 实施个性化推荐策略\n\n");
        result.append("3. **长期规划** (季度)\n");
        result.append("   - 建立数据监控体系\n");
        result.append("   - 制定增长目标计划\n\n");

        result.append("---\n");
        result.append("*报告生成时间: ").append(java.time.LocalDateTime.now()).append("*\n");

        return result.toString();
    }

    private String detectDataType(String query) {
        String lowerQuery = query.toLowerCase();
        if (lowerQuery.contains("销售") || lowerQuery.contains("订单") || lowerQuery.contains("sales")) {
            return "sales";
        } else if (lowerQuery.contains("用户") || lowerQuery.contains("客户") || lowerQuery.contains("user")) {
            return "users";
        } else if (lowerQuery.contains("营收") || lowerQuery.contains("收入") || lowerQuery.contains("revenue")) {
            return "revenue";
        }
        return "sales"; // 默认返回销售数据
    }
}
```

- [ ] **Step 2: 提交**

```bash
git add agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/tools/DataAnalysisTools.java
git commit -m "feat(demo-analyse): add data analysis tools with mock data"
```

---

### Task 4: 创建数据洞察技能定义

**Files:**
- Create: `agentscope-examples/demo-analyse/src/main/resources/skills/data_insight/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md 文件**

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
- `time_range`: 时间范围 (e.g., "last_30_days", "last_quarter")
- `metrics`: 需要的指标列表

**输出**:
- 结构化的业务数据

### 3. generate_insight_report - 生成报告
基于分析结果生成结构化报告。

**输入参数**:
- `data`: 分析数据
- `analysis_focus`: 分析重点

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
- "帮我看看最近的数据表现"
```

- [ ] **Step 2: 提交**

```bash
git add agentscope-examples/demo-analyse/src/main/resources/skills/data_insight/SKILL.md
git commit -m "feat(demo-analyse): add data insight skill definition"
```

---

### Task 5: 创建 DTO 类

**Files:**
- Create: `agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/dto/ChatRequest.java`
- Create: `agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/dto/ChatEvent.java`

- [ ] **Step 1: 创建 ChatRequest.java**

```java
/*
 * Copyright 2024-2026 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.agentscope.examples.demoanalyse.dto;

/**
 * Chat request DTO.
 */
public class ChatRequest {

    private String message;
    private String sessionId;

    public ChatRequest() {}

    public ChatRequest(String message, String sessionId) {
        this.message = message;
        this.sessionId = sessionId;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }
}
```

- [ ] **Step 2: 创建 ChatEvent.java**

```java
/*
 * Copyright 2024-2026 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.agentscope.examples.demoanalyse.dto;

import java.util.Map;

/**
 * Chat event sent to frontend via SSE.
 */
public class ChatEvent {

    private String type;
    private String content;
    private String toolName;
    private String toolId;
    private Map<String, Object> toolInput;
    private String toolResult;
    private String error;
    private boolean incremental;

    public ChatEvent() {}

    public static ChatEvent text(String content, boolean incremental) {
        ChatEvent event = new ChatEvent();
        event.type = "TEXT";
        event.content = content;
        event.incremental = incremental;
        return event;
    }

    public static ChatEvent toolUse(String toolId, String toolName, Map<String, Object> input) {
        ChatEvent event = new ChatEvent();
        event.type = "TOOL_USE";
        event.toolId = toolId;
        event.toolName = toolName;
        event.toolInput = input;
        return event;
    }

    public static ChatEvent toolResult(String toolId, String toolName, String result) {
        ChatEvent event = new ChatEvent();
        event.type = "TOOL_RESULT";
        event.toolId = toolId;
        event.toolName = toolName;
        event.toolResult = result;
        return event;
    }

    public static ChatEvent error(String error) {
        ChatEvent event = new ChatEvent();
        event.type = "ERROR";
        event.error = error;
        return event;
    }

    public static ChatEvent complete() {
        ChatEvent event = new ChatEvent();
        event.type = "COMPLETE";
        return event;
    }

    // Getters and setters

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getToolName() {
        return toolName;
    }

    public void setToolName(String toolName) {
        this.toolName = toolName;
    }

    public String getToolId() {
        return toolId;
    }

    public void setToolId(String toolId) {
        this.toolId = toolId;
    }

    public Map<String, Object> getToolInput() {
        return toolInput;
    }

    public void setToolInput(Map<String, Object> toolInput) {
        this.toolInput = toolInput;
    }

    public String getToolResult() {
        return toolResult;
    }

    public void setToolResult(String toolResult) {
        this.toolResult = toolResult;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public boolean isIncremental() {
        return incremental;
    }

    public void setIncremental(boolean incremental) {
        this.incremental = incremental;
    }
}
```

- [ ] **Step 3: 提交**

```bash
git add agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/dto/
git commit -m "feat(demo-analyse): add DTO classes for chat request and event"
```

---

### Task 6: 创建 Agent 配置类

**Files:**
- Create: `agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/config/AgentConfig.java`

- [ ] **Step 1: 创建 AgentConfig.java**

```java
/*
 * Copyright 2024-2026 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.agentscope.examples.demoanalyse.config;

import io.agentscope.core.ReActAgent;
import io.agentscope.core.memory.InMemoryMemory;
import io.agentscope.core.model.DashScopeChatModel;
import io.agentscope.core.skill.AgentSkill;
import io.agentscope.core.skill.SkillBox;
import io.agentscope.core.skill.repository.ClasspathSkillRepository;
import io.agentscope.core.tool.Toolkit;
import io.agentscope.examples.demoanalyse.tools.DataAnalysisTools;
import java.io.IOException;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Configuration for the data analyst agent with SkillBox.
 */
@Configuration
public class AgentConfig {

    private static final String SYSTEM_PROMPT =
            """
            你是一个专业的数据分析师助手，帮助用户进行业务数据分析。
            当用户提出分析请求时，你应该：
            1. 首先使用 analyze_feasibility 分析查询的可行性
            2. 然后使用 fetch_business_data 获取相关业务数据
            3. 最后使用 generate_insight_report 生成分析报告

            请确保按顺序执行这三个步骤，为用户提供完整的数据洞察。
            """;

    @Value("${dashscope.api-key:${AI_DASHSCOPE_API_KEY:}}")
    private String apiKey;

    @Value("${dashscope.model-name:qwen-plus}")
    private String modelName;

    @Bean
    public Toolkit toolkit() {
        return new Toolkit();
    }

    @Bean
    public ClasspathSkillRepository skillRepository() throws IOException {
        return new ClasspathSkillRepository("skills");
    }

    @Bean
    public SkillBox skillBox(Toolkit toolkit, ClasspathSkillRepository skillRepository) {
        SkillBox skillBox = new SkillBox(toolkit);
        List<AgentSkill> skills = skillRepository.getAllSkills();

        for (AgentSkill skill : skills) {
            skillBox.registration()
                    .skill(skill)
                    .tool(new DataAnalysisTools())
                    .apply();
        }

        return skillBox;
    }

    @Bean
    public ReActAgent dataAnalystAgent(Toolkit toolkit, SkillBox skillBox) {
        return ReActAgent.builder()
                .name("data_analyst")
                .sysPrompt(SYSTEM_PROMPT)
                .model(DashScopeChatModel.builder()
                        .apiKey(apiKey)
                        .modelName(modelName)
                        .stream(true)
                        .build())
                .toolkit(toolkit)
                .skillBox(skillBox)
                .memory(new InMemoryMemory())
                .build();
    }
}
```

- [ ] **Step 2: 提交**

```bash
git add agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/config/AgentConfig.java
git commit -m "feat(demo-analyse): add agent configuration with SkillBox"
```

---

### Task 7: 创建 Agent 服务类

**Files:**
- Create: `agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/service/AgentService.java`

- [ ] **Step 1: 创建 AgentService.java**

```java
/*
 * Copyright 2024-2026 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.agentscope.examples.demoanalyse.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.agentscope.core.ReActAgent;
import io.agentscope.core.agent.Event;
import io.agentscope.core.memory.InMemoryMemory;
import io.agentscope.core.message.ContentBlock;
import io.agentscope.core.message.Msg;
import io.agentscope.core.message.MsgRole;
import io.agentscope.core.message.TextBlock;
import io.agentscope.core.message.ToolResultBlock;
import io.agentscope.core.message.ToolUseBlock;
import io.agentscope.core.session.InMemorySession;
import io.agentscope.core.session.Session;
import io.agentscope.examples.demoanalyse.dto.ChatEvent;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

/**
 * Service for managing agent and chat sessions.
 */
@Service
public class AgentService {

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    private final ReActAgent agent;

    private final Session session = new InMemorySession();

    private final ConcurrentHashMap<String, ReActAgent> runningAgents = new ConcurrentHashMap<>();

    public AgentService(ReActAgent agent) {
        this.agent = agent;
    }

    /**
     * Process a chat message.
     */
    public Flux<ChatEvent> chat(String sessionId, String message) {
        ReActAgent sessionAgent = createSessionAgent(sessionId);
        runningAgents.put(sessionId, sessionAgent);

        Msg userMsg = Msg.builder()
                .name("User")
                .role(MsgRole.USER)
                .content(TextBlock.builder().text(message).build())
                .build();

        return sessionAgent.stream(userMsg)
                .flatMap(this::convertEventToChatEvents)
                .concatWith(Flux.just(ChatEvent.complete()))
                .doFinally(signal -> {
                    runningAgents.remove(sessionId);
                    sessionAgent.saveTo(session, sessionId);
                })
                .onErrorResume(error -> Flux.just(ChatEvent.error(error.getMessage()), ChatEvent.complete()));
    }

    /**
     * Clear a session.
     */
    public void clearSession(String sessionId) {
        session.delete(io.agentscope.core.state.SimpleSessionKey.of(sessionId));
    }

    /**
     * Get available skills.
     */
    public List<String> getAvailableSkills() {
        return List.of("data_insight");
    }

    private ReActAgent createSessionAgent(String sessionId) {
        ReActAgent sessionAgent = ReActAgent.builder()
                .name(agent.getName())
                .sysPrompt(agent.getSysPrompt())
                .model(agent.getModel())
                .toolkit(agent.getToolkit().copy())
                .skillBox(agent.getSkillBox())
                .memory(new InMemoryMemory())
                .build();
        sessionAgent.loadIfExists(session, sessionId);
        return sessionAgent;
    }

    private Flux<ChatEvent> convertEventToChatEvents(Event event) {
        List<ChatEvent> events = new ArrayList<>();
        Msg msg = event.getMessage();

        switch (event.getType()) {
            case REASONING -> {
                if (event.isLast() && msg.hasContentBlocks(ToolUseBlock.class)) {
                    List<ToolUseBlock> toolCalls = msg.getContentBlocks(ToolUseBlock.class);
                    for (ToolUseBlock tool : toolCalls) {
                        events.add(ChatEvent.toolUse(
                                tool.getId(), tool.getName(), convertInput(tool.getInput())));
                    }
                } else {
                    String text = extractText(msg);
                    if (text != null && !text.isEmpty()) {
                        events.add(ChatEvent.text(text, !event.isLast()));
                    }
                }
            }
            case TOOL_RESULT -> {
                for (ToolResultBlock result : msg.getContentBlocks(ToolResultBlock.class)) {
                    events.add(ChatEvent.toolResult(
                            result.getId(), result.getName(), extractToolOutput(result)));
                }
            }
            case AGENT_RESULT -> {
                String text = msg.getTextContent();
                if (text != null && !text.isEmpty()) {
                    events.add(ChatEvent.text(text, false));
                }
            }
            default -> {}
        }

        return Flux.fromIterable(events);
    }

    private String extractText(Msg msg) {
        List<TextBlock> textBlocks = msg.getContentBlocks(TextBlock.class);
        if (textBlocks.isEmpty()) {
            return null;
        }
        StringBuilder sb = new StringBuilder();
        for (TextBlock block : textBlocks) {
            sb.append(block.getText());
        }
        return sb.toString();
    }

    private String extractToolOutput(ToolResultBlock result) {
        List<ContentBlock> outputs = result.getOutput();
        if (outputs == null || outputs.isEmpty()) {
            return "";
        }
        StringBuilder sb = new StringBuilder();
        for (ContentBlock block : outputs) {
            if (block instanceof TextBlock tb) {
                sb.append(tb.getText());
            }
        }
        return sb.toString();
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> convertInput(Object input) {
        if (input == null) {
            return Map.of();
        }
        if (input instanceof Map) {
            return (Map<String, Object>) input;
        }
        try {
            return OBJECT_MAPPER.convertValue(input, new TypeReference<Map<String, Object>>() {});
        } catch (Exception e) {
            return Map.of("value", input.toString());
        }
    }
}
```

- [ ] **Step 2: 提交**

```bash
git add agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/service/AgentService.java
git commit -m "feat(demo-analyse): add agent service for session management"
```

---

### Task 8: 创建 REST 控制器

**Files:**
- Create: `agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/controller/ChatController.java`

- [ ] **Step 1: 创建 ChatController.java**

```java
/*
 * Copyright 2024-2026 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.agentscope.examples.demoanalyse.controller;

import io.agentscope.examples.demoanalyse.dto.ChatEvent;
import io.agentscope.examples.demoanalyse.dto.ChatRequest;
import io.agentscope.examples.demoanalyse.service.AgentService;
import java.util.List;
import java.util.Map;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

/**
 * REST controller for Demo Analyse API.
 */
@RestController
@RequestMapping("/api")
public class ChatController {

    private final AgentService agentService;

    public ChatController(AgentService agentService) {
        this.agentService = agentService;
    }

    /**
     * Send a chat message and receive streaming response.
     */
    @PostMapping(value = "/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<ChatEvent>> chat(@RequestBody ChatRequest request) {
        String sessionId = request.getSessionId();
        if (sessionId == null || sessionId.isEmpty()) {
            sessionId = "default";
        }

        return agentService
                .chat(sessionId, request.getMessage())
                .map(event -> ServerSentEvent.<ChatEvent>builder().data(event).build());
    }

    /**
     * Clear a chat session.
     */
    @DeleteMapping("/chat/session/{sessionId}")
    public ResponseEntity<Map<String, Object>> clearSession(@PathVariable String sessionId) {
        agentService.clearSession(sessionId);
        return ResponseEntity.ok(Map.of("success", true));
    }

    /**
     * Get available skills.
     */
    @GetMapping("/skills")
    public ResponseEntity<List<String>> getSkills() {
        return ResponseEntity.ok(agentService.getAvailableSkills());
    }
}
```

- [ ] **Step 2: 提交**

```bash
git add agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/controller/ChatController.java
git commit -m "feat(demo-analyse): add REST controller for chat API"
```

---

### Task 9: 创建前端 HTML 页面

**Files:**
- Create: `agentscope-examples/demo-analyse/src/main/resources/static/index.html`

- [ ] **Step 1: 创建 index.html**

```html
<!--
  ~ Copyright 2024-2026 the original author or authors.
  ~
  ~ Licensed under the Apache License, Version 2.0 (the "License");
  ~ you may not use this file except in compliance with the License.
  ~ You may obtain a copy of the License at
  ~
  ~     http://www.apache.org/licenses/LICENSE-2.0
  ~
  ~ Unless required by applicable law or agreed to in writing, software
  ~ distributed under the License is distributed on an "AS IS" BASIS,
  ~ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  ~ See the License for the specific language governing permissions and
  ~ limitations under the License.
-->

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo Analyse - 数据洞察助手</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <div class="header-title">
                    <h1>Demo Analyse</h1>
                    <p data-i18n="subtitle">ReActAgent + SkillBox 数据洞察演示</p>
                </div>
                <div class="lang-switch">
                    <button id="lang-en" class="lang-btn active">EN</button>
                    <button id="lang-zh" class="lang-btn">中文</button>
                </div>
            </div>
        </header>

        <div class="main-content">
            <aside class="sidebar">
                <section class="panel">
                    <h2 data-i18n="availableSkills">可用技能</h2>
                    <div id="skills-list" class="skills-list"></div>
                </section>

                <section class="panel">
                    <h2 data-i18n="toolChain">工具链</h2>
                    <div class="tool-chain">
                        <div class="chain-item">
                            <span class="chain-num">1</span>
                            <span>analyze_feasibility</span>
                        </div>
                        <div class="chain-arrow">↓</div>
                        <div class="chain-item">
                            <span class="chain-num">2</span>
                            <span>fetch_business_data</span>
                        </div>
                        <div class="chain-arrow">↓</div>
                        <div class="chain-item">
                            <span class="chain-num">3</span>
                            <span>generate_insight_report</span>
                        </div>
                    </div>
                </section>
            </aside>

            <main class="chat-area">
                <div id="chat-messages" class="chat-messages"></div>

                <div class="input-area">
                    <textarea id="message-input" data-i18n-placeholder="inputPlaceholder" placeholder="输入您的数据分析问题..." rows="2"></textarea>
                    <div class="input-buttons">
                        <button id="send-btn" class="btn btn-primary" data-i18n="send">发送</button>
                        <button id="stop-btn" class="btn btn-warning hidden" data-i18n="stop">停止</button>
                    </div>
                </div>
            </main>
        </div>
    </div>
    <script src="js/app.js"></script>
</body>
</html>
```

- [ ] **Step 2: 提交**

```bash
git add agentscope-examples/demo-analyse/src/main/resources/static/index.html
git commit -m "feat(demo-analyse): add frontend HTML page"
```

---

### Task 10: 创建前端 CSS 样式

**Files:**
- Create: `agentscope-examples/demo-analyse/src/main/resources/static/css/style.css`

- [ ] **Step 1: 创建 style.css**

```css
/*
 * Copyright 2024-2026 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

:root {
    --primary-color: #4a90d9;
    --primary-hover: #3a7bc8;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --bg-color: #f5f5f5;
    --panel-bg: #ffffff;
    --text-color: #333333;
    --text-muted: #666666;
    --border-color: #e0e0e0;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.5;
}

.container { display: flex; flex-direction: column; height: 100vh; }

.header {
    background: linear-gradient(135deg, var(--primary-color), #667eea);
    color: white;
    padding: 1rem 2rem;
}
.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1400px;
    margin: 0 auto;
}
.header-title { text-align: left; }
.header h1 { font-size: 1.5rem; margin-bottom: 0.25rem; }
.header p { font-size: 0.875rem; opacity: 0.9; }

.lang-switch { display: flex; gap: 0.25rem; }
.lang-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid rgba(255,255,255,0.5);
    background: transparent;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.2s;
}
.lang-btn:hover { background: rgba(255,255,255,0.1); }
.lang-btn.active {
    background: white;
    color: var(--primary-color);
    border-color: white;
}

.main-content { display: flex; flex: 1; overflow: hidden; }

.sidebar {
    width: 280px;
    background: var(--panel-bg);
    border-right: 1px solid var(--border-color);
    overflow-y: auto;
    padding: 1rem;
}

.panel { margin-bottom: 1.5rem; }
.panel h2 {
    font-size: 1rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--primary-color);
}

.skills-list {
    background: var(--bg-color);
    border-radius: 8px;
    padding: 0.75rem;
}
.skill-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem;
    background: white;
    border-radius: 6px;
    margin-bottom: 0.5rem;
}
.skill-item:last-child { margin-bottom: 0; }
.skill-icon { font-size: 1.25rem; }
.skill-info { flex: 1; }
.skill-name { font-weight: 600; font-size: 0.9rem; }
.skill-desc { font-size: 0.75rem; color: var(--text-muted); }

.tool-chain {
    background: var(--bg-color);
    border-radius: 8px;
    padding: 1rem;
}
.chain-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem;
    background: white;
    border-radius: 6px;
    font-size: 0.85rem;
}
.chain-num {
    width: 24px;
    height: 24px;
    background: var(--primary-color);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 600;
}
.chain-arrow {
    text-align: center;
    color: var(--text-muted);
    font-size: 1.25rem;
    padding: 0.25rem 0;
}

.chat-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: var(--panel-bg);
    min-width: 0;
    overflow: hidden;
}

.chat-messages { flex: 1; overflow-y: auto; padding: 1rem; overflow-x: hidden; }

.message { margin-bottom: 1rem; max-width: 85%; min-width: 0; }
.message.user { margin-left: auto; }
.message.assistant { margin-right: auto; }
.message-content {
    padding: 0.75rem 1rem;
    border-radius: 12px;
    word-wrap: break-word;
    word-break: break-word;
    white-space: pre-wrap;
    overflow-wrap: break-word;
}
.message.user .message-content {
    background: var(--primary-color);
    color: white;
    border-bottom-right-radius: 4px;
}
.message.assistant .message-content {
    background: var(--bg-color);
    border-bottom-left-radius: 4px;
}
.message-label { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem; }
.message.user .message-label { text-align: right; }

/* Tool Events */
.tool-event {
    background: #e8f4fd;
    border: 1px solid #b8daff;
    border-radius: 8px;
    padding: 0.75rem;
    margin: 0.75rem 0;
    font-size: 0.875rem;
    max-width: 100%;
    overflow: hidden;
}
.tool-event.result {
    background: #d4edda;
    border-color: #c3e6cb;
}
.tool-event-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    flex-wrap: wrap;
}
.tool-event-header .icon { font-size: 1rem; }
.tool-event-header code {
    background: rgba(0,0,0,0.1);
    padding: 0.125rem 0.375rem;
    border-radius: 4px;
    font-size: 0.8rem;
    word-break: break-all;
}
.tool-params { margin-top: 0.5rem; }
.params-label { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem; }
.tool-event pre {
    background: rgba(0,0,0,0.05);
    padding: 0.5rem;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 0.75rem;
    margin: 0;
    max-height: 200px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
.tool-result-content pre {
    max-height: 300px;
    white-space: pre-wrap;
    word-break: break-word;
}

.input-area {
    padding: 1rem;
    border-top: 1px solid var(--border-color);
    background: var(--panel-bg);
}
.input-area textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    resize: none;
    font-size: 1rem;
    font-family: inherit;
    margin-bottom: 0.5rem;
}
.input-area textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px rgba(74, 144, 217, 0.2);
}
.input-buttons { display: flex; gap: 0.5rem; justify-content: flex-end; }

.btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    font-size: 0.875rem;
    cursor: pointer;
    transition: background-color 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}
.btn-primary { background: var(--primary-color); color: white; }
.btn-primary:hover { background: var(--primary-hover); }
.btn-secondary { background: var(--secondary-color); color: white; }
.btn-secondary:hover { background: #5a6268; }
.btn-warning { background: var(--warning-color); color: #212529; }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* Spinner */
.spinner {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.hidden { display: none !important; }

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg-color); }
::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

@media (max-width: 768px) {
    .main-content { flex-direction: column; }
    .sidebar {
        width: 100%;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
        max-height: 250px;
    }
    .message { max-width: 95%; }
}
```

- [ ] **Step 2: 提交**

```bash
git add agentscope-examples/demo-analyse/src/main/resources/static/css/style.css
git commit -m "feat(demo-analyse): add frontend CSS styles"
```

---

### Task 11: 创建前端 JavaScript 逻辑

**Files:**
- Create: `agentscope-examples/demo-analyse/src/main/resources/static/js/app.js`

- [ ] **Step 1: 创建 app.js**

```javascript
/*
 * Copyright 2024-2026 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

const i18n = {
    en: {
        subtitle: 'ReActAgent + SkillBox Data Insight Demo',
        availableSkills: 'Available Skills',
        toolChain: 'Tool Chain',
        inputPlaceholder: 'Enter your data analysis question...',
        send: 'Send',
        stop: 'Stop',
        you: 'You',
        assistant: 'Assistant',
        toolCall: 'Tool Call',
        toolResult: 'Tool Result',
        params: 'Parameters',
        error: 'Error',
        noOutput: '(no output)'
    },
    zh: {
        subtitle: 'ReActAgent + SkillBox 数据洞察演示',
        availableSkills: '可用技能',
        toolChain: '工具链',
        inputPlaceholder: '输入您的数据分析问题...',
        send: '发送',
        stop: '停止',
        you: '你',
        assistant: '助手',
        toolCall: '工具调用',
        toolResult: '工具结果',
        params: '参数',
        error: '错误',
        noOutput: '(无输出)'
    }
};

const state = {
    sessionId: 'session_' + Date.now(),
    isProcessing: false,
    currentAssistantMessage: null,
    currentAbortController: null,
    lang: 'en'
};

const elements = {
    chatMessages: document.getElementById('chat-messages'),
    messageInput: document.getElementById('message-input'),
    sendBtn: document.getElementById('send-btn'),
    stopBtn: document.getElementById('stop-btn'),
    skillsList: document.getElementById('skills-list'),
    langEn: document.getElementById('lang-en'),
    langZh: document.getElementById('lang-zh')
};

function t(key) {
    return i18n[state.lang][key] || key;
}

function updateI18n() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.textContent = t(key);
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        el.placeholder = t(key);
    });
}

function setLanguage(lang) {
    state.lang = lang;
    elements.langEn.classList.toggle('active', lang === 'en');
    elements.langZh.classList.toggle('active', lang === 'zh');
    updateI18n();
}

document.addEventListener('DOMContentLoaded', () => {
    loadSkills();
    setupEventListeners();
    updateI18n();
});

function setupEventListeners() {
    elements.sendBtn.addEventListener('click', sendMessage);
    elements.messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    elements.langEn.addEventListener('click', () => setLanguage('en'));
    elements.langZh.addEventListener('click', () => setLanguage('zh'));
}

async function loadSkills() {
    try {
        const response = await fetch('/api/skills');
        const skills = await response.json();
        renderSkillsList(skills);
    } catch (error) {
        console.error('Load skills failed:', error);
        // 默认显示
        renderSkillsList(['data_insight']);
    }
}

function renderSkillsList(skills) {
    if (skills.length === 0) {
        elements.skillsList.innerHTML = '<p class="hint">No skills available</p>';
        return;
    }
    elements.skillsList.innerHTML = skills.map(name => `
        <div class="skill-item">
            <span class="skill-icon">📊</span>
            <div class="skill-info">
                <div class="skill-name">${escapeHtml(name)}</div>
                <div class="skill-desc">${state.lang === 'zh' ? '业务数据洞察分析' : 'Business data insight analysis'}</div>
            </div>
        </div>
    `).join('');
}

async function sendMessage() {
    const message = elements.messageInput.value.trim();
    if (!message || state.isProcessing) return;

    elements.messageInput.value = '';
    addMessage('user', message);
    setProcessing(true);
    state.currentAssistantMessage = null;

    state.currentAbortController = new AbortController();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sessionId: state.sessionId, message }),
            signal: state.currentAbortController.signal
        });
        await processSSEStream(response);
    } catch (error) {
        if (error.name !== 'AbortError') {
            console.error(t('error') + ':', error);
            addMessage('assistant', t('error') + ': ' + error.message);
        }
    } finally {
        setProcessing(false);
        state.currentAbortController = null;
    }
}

async function processSSEStream(response) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
        while (true) {
            const { done, value } = await reader.read();
            if (value) buffer += decoder.decode(value, { stream: true });

            const lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (const line of lines) {
                if (line.startsWith('data:')) {
                    const data = line.slice(5).trim();
                    if (data) {
                        try {
                            handleChatEvent(JSON.parse(data));
                        } catch (e) {
                            console.error('Failed:', data, e);
                        }
                    }
                }
            }
            if (done) break;
        }
    } finally {
        reader.releaseLock();
    }
}

function handleChatEvent(event) {
    switch (event.type) {
        case 'TEXT':
            if (event.incremental) {
                appendToAssistantMessage(event.content);
            } else {
                finalizeAssistantMessage();
            }
            break;
        case 'TOOL_USE':
            finalizeAssistantMessage();
            addToolUseEvent(event.toolId, event.toolName, event.toolInput);
            break;
        case 'TOOL_RESULT':
            addToolResultEvent(event.toolId, event.toolName, event.toolResult);
            break;
        case 'ERROR':
            finalizeAssistantMessage();
            addMessage('assistant', t('error') + ': ' + event.error);
            break;
        case 'COMPLETE':
            finalizeAssistantMessage();
            break;
    }
}

function addMessage(role, content) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerHTML = `
        <div class="message-label">${role === 'user' ? t('you') : t('assistant')}</div>
        <div class="message-content">${escapeHtml(content)}</div>
    `;
    elements.chatMessages.appendChild(div);
    scrollToBottom();
    if (role === 'assistant') {
        state.currentAssistantMessage = div.querySelector('.message-content');
    }
}

function appendToAssistantMessage(content) {
    if (!state.currentAssistantMessage) {
        addMessage('assistant', content);
    } else {
        state.currentAssistantMessage.textContent += content;
        scrollToBottom();
    }
}

function finalizeAssistantMessage() {
    state.currentAssistantMessage = null;
}

function addToolUseEvent(toolId, toolName, input) {
    const div = document.createElement('div');
    div.className = 'tool-event';
    div.id = `tool-${toolId}`;

    const inputJson = input ? JSON.stringify(input, null, 2) : '{}';
    div.innerHTML = `
        <div class="tool-event-header">
            <span class="icon">🔧</span>
            <span>${t('toolCall')}: <code>${escapeHtml(toolName)}</code></span>
        </div>
        <div class="tool-params">
            <div class="params-label">${t('params')}:</div>
            <pre>${escapeHtml(inputJson)}</pre>
        </div>
    `;
    elements.chatMessages.appendChild(div);
    scrollToBottom();
}

function addToolResultEvent(toolId, toolName, result) {
    const div = document.createElement('div');
    div.className = 'tool-event result';
    div.innerHTML = `
        <div class="tool-event-header">
            <span class="icon">✅</span>
            <span>${t('toolResult')}: <code>${escapeHtml(toolName)}</code></span>
        </div>
        <div class="tool-result-content">
            <pre>${escapeHtml(result || t('noOutput'))}</pre>
        </div>
    `;
    elements.chatMessages.appendChild(div);
    scrollToBottom();
}

function setProcessing(processing) {
    state.isProcessing = processing;
    elements.sendBtn.disabled = processing;
    elements.messageInput.disabled = processing;
    elements.stopBtn.classList.toggle('hidden', !processing);
    elements.sendBtn.classList.toggle('hidden', processing);
}

function scrollToBottom() {
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}
```

- [ ] **Step 2: 提交**

```bash
git add agentscope-examples/demo-analyse/src/main/resources/static/js/app.js
git commit -m "feat(demo-analyse): add frontend JavaScript logic"
```

---

### Task 12: 验证项目构建

**Files:**
- Verify: Build and run tests

- [ ] **Step 1: 构建项目**

```bash
mvn clean install -pl agentscope-examples/demo-analyse -am -DskipTests
```

Expected: BUILD SUCCESS

- [ ] **Step 2: 验证项目结构**

```bash
ls -la agentscope-examples/demo-analyse/src/main/java/io/agentscope/examples/demoanalyse/
ls -la agentscope-examples/demo-analyse/src/main/resources/
```

Expected: All files present

- [ ] **Step 3: 提交最终状态**

```bash
git status
```

---

## Verification Summary

1. **构建验证**: `mvn clean install -pl agentscope-examples/demo-analyse -am`
2. **启动验证**: `mvn spring-boot:run -pl agentscope-examples/demo-analyse`
3. **功能验证**:
   - 访问 `http://localhost:8081`
   - 输入 "分析上个月销售趋势"
   - 观察工具调用过程（可行性分析 → 获取数据 → 生成报告）
   - 验证最终报告输出

---

## Self-Review Checklist

- [x] Spec coverage: All requirements from design doc covered
- [x] No placeholders: All code blocks contain complete implementations
- [x] Type consistency: Method signatures and class names consistent across files
- [x] File paths: All paths are exact and correct