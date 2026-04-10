package io.agentscope.examples.hitlchat.tools;

import io.agentscope.core.tool.Tool;
import io.agentscope.core.tool.ToolParam;
import reactor.core.publisher.Mono;

/**
 * @author zhouj
 * @since 2026/3/27
 */
public class MetricAnalysisTools {

    //1. 能力类型
    //2. json
    @Tool(name = "analyze_query_feasibility", description = "分析报告对话，评估数据需求")
    public Mono<String> analyzeFeasibility(
            @ToolParam(name = "query", description = "用户的分析请求") String query,
            @ToolParam(name = "capabilityId", description = "原子能力id UUID") String capabilityId

    ) {

        return Mono.just("{\"status\":\"unfeasible\"}");


    }

    @Tool(name = "generate_insight_report", description = "生成分析报告")
    public Mono<String> generateInsightReport(
            @ToolParam(name = "capabilityId", description = "uuid") String capabilityId
    ) {
        return Mono.just("{\"status\":\"success\"}");
    }
}
