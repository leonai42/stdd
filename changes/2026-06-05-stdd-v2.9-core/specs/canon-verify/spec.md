# canon-verify — Canonical 验证 DC-HASH 修复

<!-- confidence: high -->
<!-- evidence: proposal.md BUG-02 + canon.py 代码分析 -->

## Requirement: 正确的生成顺序

CANON-REQ-001: 生成 Human View Markdown 之前 SHALL 先生成 Canonical YAML，确保 source_hash 可回填。

### Scenario: 先生成 YAML 再生成 Human View

<!-- confidence: high -->
GIVEN 存在 `proposal.yaml`（Canonical YAML）
AND proposal.yaml 的 source_hash 已计算并写入
WHEN 执行 `stdd canon generate --all`
THEN SHALL 先生成/更新 `proposal.yaml`
AND SHALL 计算并写入 `source_hash` 到 proposal.yaml
AND SHALL 从 proposal.yaml 渲染 `proposal-brief.md`（Human View）
AND proposal-brief.md 的 `source_hash` 字段 SHALL 与 proposal.yaml 一致

## Requirement: DC-HASH 验证通过

CANON-REQ-002: `canon verify` 的 DC-HASH 检查 SHALL 通过。

### Scenario: 生成后验证 DC-HASH

<!-- confidence: high -->
GIVEN proposal.yaml 已生成且包含有效的 source_hash
AND proposal-brief.md 已从该 YAML 渲染
WHEN 用户执行 `stdd canon verify`
THEN DC-HASH 检查 SHALL 通过
AND DC-FIELD 检查 SHALL 通过

### Scenario: source_hash 不一致时 detect

<!-- confidence: medium -->
GIVEN proposal-brief.md 被手动修改
AND source_hash 与 proposal.yaml 不一致
WHEN 用户执行 `stdd canon verify`
THEN DC-HASH 检查 SHALL 报告失败
AND SHALL 显示不一致的文件路径
