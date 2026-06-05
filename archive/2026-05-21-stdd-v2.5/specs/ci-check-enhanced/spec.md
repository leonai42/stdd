# Spec: ci-check-enhanced — CI 检查增强

> Capability: ci-check-enhanced
> Priority: P0 · 3d · CLI

## Requirement: 范围蔓延检测

`stdd ci check-scope` SHALL 对比 proposal 声明的文件范围与实际 git diff，标记超出范围的文件。

### Scenario: 正常范围检测

GIVEN proposal.md 中声明 Capability: order, payment
AND `git diff --stat` 显示仅变更了 `app/billing/order.py`, `app/billing/payment.py`
WHEN 执行 `stdd ci check-scope 2026-05-21-stdd-v2.5`
THEN 输出 SHALL 为 "[PASS] scope check: 2 files within declared scope"
AND 退出码为 0

### Scenario: 检测到范围蔓延

GIVEN proposal.md 声明 Capability: order
AND `git diff --stat` 显示变更了 `app/billing/order.py`, `app/auth/login.py`
WHEN 执行 `stdd ci check-scope <change-name>`
THEN 输出 SHALL 包含 "[WARN] potential scope creep: app/auth/login.py outside declared scope"
AND 退出码为 0（警告，不阻断）

### Scenario: proposal 无 capability 声明

GIVEN proposal.md 中无 STDD-MARKER capability 注释
WHEN 执行 `stdd ci check-scope <change-name>`
THEN 输出 SHALL 为 "[SKIP] no capability declarations found in proposal.md"
AND 退出码为 0

## Requirement: 覆盖真空检测

`stdd ci check-coverage` SHALL 解析 pytest coverage JSON 输出，识别有 spec 但无测试覆盖的模块。

### Scenario: 覆盖正常

GIVEN pytest coverage JSON 显示 `app/billing/order.py` 覆盖率为 92%
AND quality.yaml 中 `coverage_threshold: 80`
WHEN 执行 `stdd ci check-coverage`
THEN 输出 SHALL 为 "[PASS] coverage: 92% >= 80% threshold"
AND 退出码为 0

### Scenario: 覆盖不足

GIVEN pytest coverage JSON 显示 `app/billing/payment.py` 覆盖率为 62%
WHEN 执行 `stdd ci check-coverage`
THEN 输出 SHALL 包含 "[FAIL] coverage gap: app/billing/payment.py (62% < 80%)"
AND 退出码为 1

### Scenario: 无 coverage 数据

GIVEN 项目中没有 `coverage.json` 文件
WHEN 执行 `stdd ci check-coverage`
THEN 输出 SHALL 为 "[SKIP] no coverage data found (non-code change?)"
AND 退出码为 0

## Requirement: 契约断层检测

`stdd ci check-contracts` SHALL 基于 `dependency-graph` 输出，校验相邻 capability 间的字段一致性。

### Scenario: 契约一致

GIVEN capability A (payment) 的 spec 引用 capability B (membership) 的 `user_id` 字段
AND capability B 的 spec 中定义了 `user_id` 字段
WHEN 执行 `stdd ci check-contracts <change-name>`
THEN 输出 SHALL 为 "[PASS] contract check: 5 cross-capability references verified"
AND 退出码为 0

### Scenario: 契约断层

GIVEN capability A 引用 capability B 的 `payer_id` 字段
AND capability B 的 spec 中只定义了 `user_id` 和 `order_id`，无 `payer_id`
WHEN 执行 `stdd ci check-contracts <change-name>`
THEN 输出 SHALL 包含 "[FAIL] contract gap: 'payer_id' referenced by payment.spec.md:23 but not defined in membership spec"
AND 退出码为 1

### Scenario: 无跨 capability 引用

GIVEN change 只有一个 capability，无跨 capability 依赖
WHEN 执行 `stdd ci check-contracts <change-name>`
THEN 输出 SHALL 为 "[SKIP] no cross-capability references found"
AND 退出码为 0

## Requirement: check-failures 总入口

`stdd ci check-failures` SHALL 聚合所有 7 项检查。

### Scenario: 全量检查执行

WHEN 执行 `stdd ci check-failures <change-name>`
THEN 输出 SHALL 按顺序包含 7 个检查段（4 项已有 + 3 项新增）
AND 汇总行 SHALL 显示 "PASS: X, FAIL: Y, SKIP: Z"
AND 任意 FAIL 时退出码为 1
