# Spec: experience-review

## Requirement: 交互式审核经验草稿

逐条展示 lifecycle=discovered 的经验草稿，用户选择沉淀+共享、仅本地沉淀或跳过。

### Scenario: 展示草稿列表 (confidence: high)
- **GIVEN** `.stdd/experiences/` 中有 3 个 lifecycle=discovered 的草稿
- **WHEN** 执行 `stdd experience review`
- **THEN** SHALL 逐条展示: [序号] category | pattern | severity | occurrences
- **AND** SHALL 每条约 80 字符宽度的分隔线

### Scenario: 用户选择"沉淀+共享" (confidence: high)
- **GIVEN** 当前展示草稿 EXP-2026-0042
- **WHEN** 用户输入 S
- **THEN** SHALL 将 lifecycle 推进: discovered -> verified -> deposited -> shared
- **AND** SHALL 自动调用 `stdd experience share EXP-2026-0042`
- **AND** SHALL 展示: "EXP-2026-0042: 已沉淀 + 已提交共享"

### Scenario: 用户选择"仅本地沉淀" (confidence: high)
- **GIVEN** 当前展示草稿 EXP-2026-0043
- **WHEN** 用户输入 L
- **THEN** SHALL 将 lifecycle 推进: discovered -> verified -> deposited
- **AND** SHALL 不执行 share
- **AND** SHALL 展示: "EXP-2026-0043: 已本地沉淀"

### Scenario: 用户选择"跳过" (confidence: high)
- **GIVEN** 当前展示草稿 EXP-2026-0044
- **WHEN** 用户输入 D
- **THEN** SHALL 删除该草稿文件
- **AND** SHALL 展示: "EXP-2026-0044: 已删除"

### Scenario: 批量全部共享 (confidence: medium)
- **GIVEN** 展示第 1 条草稿
- **WHEN** 用户输入 A
- **THEN** SHALL 对所有剩余草稿执行 S 操作
- **AND** SHALL 一次性展示汇总结果

### Scenario: 退出保留草稿 (confidence: high)
- **GIVEN** 展示过程中
- **WHEN** 用户输入 Q
- **THEN** SHALL 保留所有未处理的草稿在 discovered 状态
- **AND** SHALL 展示: "已退出，N 条草稿保留待下次审核"
