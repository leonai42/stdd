# Spec: gate-file-confirm — Gate 文件确认通道

> Capability: gate-file-confirm
> Priority: P1 · 1.5d · CLI + Skill + Config

## Requirement: CLI 命令确认 Gate

`stdd gate approve` SHALL 允许通过 CLI 确认 Gate，等效于对话确认。

### Scenario: CLI 确认 Gate 1

GIVEN change `2026-05-21-stdd-v2.5` 当前在 Phase 1
AND Gate 1 尚未确认
WHEN 执行 `stdd gate approve 2026-05-21-stdd-v2.5 --gate 1`
THEN `.stdd.yaml` SHALL 写入 `phases.understand.confirmed_at: "<timestamp>"`
AND 输出 SHALL 为 "Gate 1 confirmed for change 2026-05-21-stdd-v2.5"

### Scenario: 重复确认幂等

GIVEN Gate 1 已确认
WHEN 再次执行 `stdd gate approve 2026-05-21-stdd-v2.5 --gate 1`
THEN 输出 SHALL 为 "Gate 1 already confirmed at <timestamp>"
AND 退出码为 0
AND `.stdd.yaml` 中的 `confirmed_at` 不变

### Scenario: Gate 顺序校验

GIVEN change 当前在 Phase 1（understand），Gate 1 尚未确认
WHEN 尝试确认 Gate 2
THEN CLI SHALL 返回错误："Gate 2 cannot be confirmed: Gate 1 is not yet confirmed"
AND 退出码为 1

### Scenario: 无效 Gate 编号

WHEN 执行 `stdd gate approve <change-name> --gate 4`
THEN CLI SHALL 返回错误："Invalid gate number: 4. Valid gates: 1, 2, 3"
AND 退出码为 1

## Requirement: 文件 Token 确认

在 change 目录创建 `GATE<N>_APPROVED` 文件 SHALL 等效于确认 Gate。

### Scenario: 文件 token 确认 Gate 2

GIVEN Gate 1 已确认
WHEN 在 change 目录创建 `GATE2_APPROVED` 文件（内容可为空）
AND `stdd status` 检查 change 状态
THEN Gate 2 SHALL 被识别为已确认
AND `phases.spec.confirmed_at` SHALL 写入创建时间

### Scenario: 文件 token 与 CLI 确认等效

GIVEN 用户通过创建 `GATE1_APPROVED` 文件确认了 Gate 1
AND 用户之后执行 `stdd gate approve <change-name> --gate 1`
THEN 输出 SHALL 为 "Gate 1 already confirmed"
AND 两种确认方式的结果一致（都是 `.stdd.yaml` 中的同一 `confirmed_at`）

## Requirement: 配置化确认通道

`gates.yaml` SHALL 支持配置启用/禁用确认通道。

### Scenario: 默认通道配置

GIVEN `gates.yaml` 使用默认配置
WHEN AI 读取 Gate 配置
THEN `confirmation.channels` SHALL 包含 `[dialog, file_token, cli]`

### Scenario: 禁用对话确认

GIVEN 用户在 `gates.yaml` 设置 `channels: [file_token, cli]`
WHEN AI 到达 Gate
THEN AI SHALL 不等待对话输入
AND AI SHALL 检查文件 token 是否存在
AND 若不存在 SHALL 提示用户通过 CLI 或文件方式确认
