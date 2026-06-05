# Spec: extract-proposal-extended — proposal 字段扩展提取

> Capability: extract-proposal-extended
> Priority: P1 · 1d · CLI

## Requirement: 扩展字段提取

`stdd extract-proposal` SHALL 从 proposal.md 的 STDD-MARKER 注释中提取 4 个新字段。

### Scenario: 提取 Constraints

GIVEN proposal.md 包含段落：
```
## Constraints
- 支付幂等性 — 重复回调不重复开通
- 回调验签 — 防止伪造支付成功通知
```
WHEN 执行 `stdd extract-proposal <change-name> --format json`
THEN 输出的 `constraints` 字段 SHALL 为 `["支付幂等性 — ...", "回调验签 — ..."]`

### Scenario: 提取 Stakeholders

GIVEN proposal.md 包含段落：
```
## Stakeholders
- 支付团队（通知接口变更）
- 前端团队（Pro 页面升级）
```
WHEN 执行 `stdd extract-proposal <change-name> --format json`
THEN 输出的 `stakeholders` 字段 SHALL 包含两个条目

### Scenario: 提取 RiskAreas

GIVEN proposal.md 包含段落：
```
## Risk Areas
- payment: 外部网关依赖，超时风险
- membership: 到期降级的定时任务可靠性
```
WHEN 执行 `stdd extract-proposal <change-name> --format json`
THEN 输出的 `risk_areas` SHALL 为结构化列表，每个条目包含 `capability` 和 `risk` 字段

### Scenario: 提取 NonGoals

GIVEN proposal.md 包含 `## NonGoals` 段落
WHEN 执行 `stdd extract-proposal <change-name> --format json`
THEN 输出的 `non_goals` SHALL 包含明确不做的事项列表

### Scenario: 新字段不存在时不报错

GIVEN proposal.md 是 V2.4 格式，没有 Constraints/Stakeholders/RiskAreas/NonGoals 段落
WHEN 执行 `stdd extract-proposal <change-name> --format json`
THEN 新字段 SHALL 输出为空数组 `[]`
AND 现有 4 个字段（Why/What Changes/Capabilities/Success Criteria）正常提取
AND 退出码为 0

## Requirement: 输出格式向后兼容

V2.5 的输出 SHALL 与 V2.4 的 JSON 格式向后兼容。

### Scenario: 旧字段不变

GIVEN proposal.md 包含 V2.4 格式的所有字段
WHEN 执行 `stdd extract-proposal <change-name> --format json`
THEN `why` / `what_changes` / `capabilities` / `success_criteria` 字段 SHALL 与 V2.4 输出一致
AND 新字段（`constraints` 等）SHALL 作为新增 key 出现在 JSON 根级

## Requirement: proposal.md 模板更新

`.stdd/templates/proposal.md` SHALL 增加新字段的 STDD-MARKER 标记。

### Scenario: 模板包含新字段标记

GIVEN 用户执行 `stdd new <change-name>` 生成 proposal.md 模板
WHEN 查看生成的 proposal.md
THEN 模板 SHALL 包含 `## Constraints` 段落（带 STDD-MARKER 注释）
AND SHALL 包含 `## Stakeholders` 段落
AND SHALL 包含 `## Risk Areas` 段落
AND SHALL 包含 `## NonGoals` 段落
