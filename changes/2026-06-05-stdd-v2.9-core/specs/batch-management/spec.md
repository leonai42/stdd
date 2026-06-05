# batch-management — 批次目录管理

<!-- confidence: high -->
<!-- evidence: proposal.md "新增批次目录管理" + V2.9_PLAN.md B.6 -->

## Requirement: 批次创建与追加

BATCH-REQ-001: SHALL 将轻量变更自动组织到批次目录中。

### Scenario: 首次轻量变更创建新批次

<!-- confidence: high -->
GIVEN `changes/_batch/` 下没有当前周期的批次
AND batch 策略为 `monthly`
AND 当前日期为 2026-06-05
WHEN 轻量变更启动
THEN SHALL 创建 `changes/_batch/2026-06-05/` 目录
AND SHALL 在 `items/001-<change-name>/` 下存储变更文件

### Scenario: 后续轻量变更追加到已有批次

<!-- confidence: high -->
GIVEN `changes/_batch/2026-06-05/` 已有 3 个 item
WHEN 新的轻量变更启动
THEN SHALL 追加为 `items/004-<change-name>/`
AND SHALL 自动递增编号

### Scenario: weekly 策略使用周标识

<!-- confidence: medium -->
GIVEN batch 策略为 `weekly`
AND 当前为 2026 年第 23 周，首次创建日期为 6 月 2 日
WHEN 轻量变更启动
THEN SHALL 创建 `changes/_batch/2026-W23-0602/` 目录

### Scenario: count_based 策略达阈值自动闭合

<!-- confidence: medium -->
GIVEN batch 策略为 `count_based`，`max_items: 20`
AND 当前批次已有 20 个 item
WHEN 新的轻量变更启动
THEN SHALL 先闭合当前批次
AND SHALL 创建新批次 `batch-002/`

## Requirement: 批次闭合

BATCH-REQ-002: SHALL 支持手动和自动闭合批次。

### Scenario: 手动闭合批次

<!-- confidence: high -->
GIVEN 当前批次 `changes/_batch/2026-06-05/` 有 5 个 item，未闭合
WHEN 用户执行 `stdd batch close`
THEN SHALL 生成 `archive-summary.md`
AND SHALL 设置 `.stdd.yaml` 中 `closed_at` 时间戳

### Scenario: 闭合后新变更创建不同名批次

<!-- confidence: high -->
GIVEN 批次 `2026-06-05/` 已闭合
AND 当前日期为 2026-06-15
WHEN 新轻量变更启动
THEN SHALL 创建 `changes/_batch/2026-06-15/`（不冲突）

### Scenario: 同日闭合再新建追加小时后缀

<!-- confidence: medium -->
GIVEN 批次 `2026-06-05/` 已闭合
AND 当前日期仍为 2026-06-05，时间为 14:30
WHEN 新轻量变更启动
THEN SHALL 创建 `changes/_batch/2026-06-05-14/`

## Requirement: 批次状态查看

BATCH-REQ-003: SHALL 支持查看当前批次状态。

### Scenario: 查看当前批次

<!-- confidence: high -->
GIVEN 存在未闭合批次 `2026-06-05/` 包含 5 个 item
WHEN 用户执行 `stdd batch status`
THEN SHALL 显示批次 ID、策略、创建时间、item 列表

### Scenario: 查看所有批次

<!-- confidence: medium -->
GIVEN `changes/_batch/` 下有 3 个批次（1 个未闭合，2 个已闭合）
WHEN 用户执行 `stdd batch list`
THEN SHALL 列出所有批次及其状态

## Requirement: 批次归档

BATCH-REQ-004: SHALL 将闭合的批次移入 archive。

### Scenario: 执行 deliver 时归档已闭合批次

<!-- confidence: medium -->
GIVEN 批次 `2026-06-05/` 已闭合
WHEN 执行 `stdd deliver`
THEN SHALL 将批次移至 `archive/_batch/2026-06-05/`
AND SHALL 生成 Git 提交
