# Spec: experience-extract

## Requirement: 自动提取经验草稿

从 test-report.md 和测试输出中自动识别可沉淀的经验模式，生成 lifecycle=discovered 的草稿。

### Scenario: 从12类失败检查提取 (confidence: high)
- **GIVEN** test-report.md 包含"12 类失败模式检查结果"表格，其中 cascading_errors 标记为 FAIL
- **WHEN** 执行 `stdd experience extract`
- **THEN** SHALL 生成 EXP-*.md，category=cascading_errors
- **AND** SHALL 从失败描述中提取 pattern 摘要
- **AND** SHALL 设置 lifecycle_state=discovered, provenance=ci-detected
- **AND** SHALL 设置 severity 与检查结果一致

### Scenario: 筛选低价值模式 (confidence: high)
- **GIVEN** test-report.md 中某失败模式 severity=low 且 occurrences=1
- **WHEN** 执行 `stdd experience extract`
- **THEN** SHALL 跳过该模式，不生成草稿
- **AND** SHALL 在输出中说明 "X 个低价值模式已跳过"

### Scenario: 重复出现的模式识别 (confidence: medium)
- **GIVEN** 同一 category 在连续 2 个 change 的 test-report 中出现
- **WHEN** 执行 `stdd experience extract`
- **THEN** SHALL 在草稿中设置 occurrences=2
- **AND** SHALL 推荐自动晋升: "该模式重复出现 2 次，建议 review 时选 [S] 共享"

### Scenario: test-report 不存在时优雅降级 (confidence: high)
- **GIVEN** 当前 change 的 test-report.md 不存在
- **WHEN** 执行 `stdd experience extract`
- **THEN** SHALL 输出 "当前 change 无 test-report.md，跳过提取"
- **AND** SHALL 不报错，正常退出

### Scenario: 从测试异常提取 (confidence: medium)
- **GIVEN** test-report.md 的"测试摘要"显示 test_api_rate_limit 失败 3 次
- **WHEN** 执行 `stdd experience extract`
- **THEN** SHALL 生成草稿，category=test_anomaly
- **AND** SHALL 在 root_cause 中记录失败堆栈摘要
