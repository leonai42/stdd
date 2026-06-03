# Spec: pass@k 质量度量

## ADDED Requirements

### Requirement: pass@k 统计验证

#### Scenario: k=3 重复验证全部通过
- **GIVEN** Phase 5 VERIFY 开始，`quality.yaml` 配置 `pass_k.enabled: true`, `pass_k.default_k: 3`
- **WHEN** 执行 `stdd verify --pass-k 3`
- **THEN** 系统 SHALL 运行 pytest 3 次
- **AND** 输出 pass@1 (第1次结果), pass@3 (3次中至少1次通过), pass^3 (3次全部通过)

#### Scenario: pass@1 低但 pass@3 高 → Spec 歧义检测
- **GIVEN** pass@1=40% (第1次大量失败), pass@3=90% (3次中至少1次高通过)
- **WHEN** 生成 pass@k 报告
- **THEN** 报告 SHALL 标记 "⚠️ Spec 可能存在歧义 — pass@1=40% 但 pass@3=90%"
- **AND** 建议在 Phase 2 中提升锚定等级

#### Scenario: k=1 默认行为不变
- **GIVEN** 未指定 --pass-k
- **WHEN** Phase 5 执行
- **THEN** 行为 SHALL 与 V2.7 完全一致（运行 1 次 pytest）

---

### Requirement: pass@k 配置

#### Scenario: P0 only scope
- **GIVEN** `pass_k.scope: p0_only`
- **WHEN** 执行 pass@k
- **THEN** 系统 SHALL 仅对 P0 TC 执行重复验证
- **AND** P1/P2 TC SHALL 仅运行 1 次
