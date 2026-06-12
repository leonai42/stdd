# Spec: experience-search

## Requirement: 全文搜索经验库

对 pattern + root_cause + body 做全文检索，按相关性+质量评分排序。

### Scenario: 关键词搜索 (confidence: high)
- **GIVEN** 经验库中有 10 条经验，其中 2 条 pattern 包含 "数据库连接"
- **WHEN** 执行 `stdd experience search "数据库连接"`
- **THEN** SHALL 返回匹配的 2 条经验
- **AND** SHALL pattern 匹配的权重 (x3) 高于 body 匹配 (x1)
- **AND** SHALL 按 relevance_score 降序排列

### Scenario: 组合过滤 (confidence: high)
- **GIVEN** 经验库中有 python 和 go 的经验
- **WHEN** 执行 `stdd experience search "timeout" --language python --category cascading_errors`
- **THEN** SHALL 只返回 python + cascading_errors 分类的结果
- **AND** SHALL 展示: "关键字 timeout, 过滤: python, cascading_errors, 共 N 条"

### Scenario: 无匹配结果 (confidence: high)
- **GIVEN** 经验库中没有匹配关键词的经验
- **WHEN** 执行 `stdd experience search "xyznotfound"`
- **THEN** SHALL 展示: "未找到匹配的经验"
- **AND** SHALL 正常退出 (exit 0)

### Scenario: JSON 格式输出 (confidence: medium)
- **GIVEN** 匹配到 3 条经验
- **WHEN** 执行 `stdd experience search "pattern" --format json`
- **THEN** SHALL 输出 JSON 数组，包含 experience_id, category, pattern, relevance_score
- **AND** SHALL relevance_score 为 0-1 的浮点数

### Scenario: 空经验库 (confidence: high)
- **GIVEN** `.stdd/experiences/` 目录不存在或无 EXP-*.md 文件
- **WHEN** 执行 `stdd experience search "anything"`
- **THEN** SHALL 展示: "经验库为空，请先沉淀经验"
- **AND** SHALL 正常退出
