# Spec: Agent 行为验证管线

> 对应板块 A（A5）| 1 个 New Capability
> agent-verification-pipeline

## ADDED Requirements

### Requirement: 单系统 Agent 验证管线 <!-- confidence: high -->

STDD SHALL 提供基于 agent_spec.yaml 的单系统 Agent 验证管线，执行检查点并验证断言。

**证据来源**：proposal.md `Capabilities > New > agent-verification-pipeline`

#### Scenario: 执行全部检查点 <!-- confidence: high -->

- **GIVEN** `canonical/specs/agent/deploy-staging.yaml` 定义了 CP-1（拉镜像）和 CP-2（重启容器）
- **WHEN** 执行 `stdd agent verify deploy-staging`
- **THEN** 系统 SHALL 按 CP 顺序依次执行每个检查点的 action
- **AND** 每个 CP 执行后 SHALL 采集输出（exit_code / stdout / stderr / http_response）
- **AND** 逐条验证 assertions，记录通过/失败状态

#### Scenario: 单检查点执行 <!-- confidence: high -->

- **GIVEN** deploy-staging 定义了 3 个 CP
- **WHEN** 执行 `stdd agent verify deploy-staging --cp CP-2`
- **THEN** 系统 SHALL 仅执行 CP-2，跳过 CP-1 和 CP-3

#### Scenario: 预览模式 <!-- confidence: medium -->

- **GIVEN** deploy-staging 定义了 "docker compose down" 回滚步骤
- **WHEN** 执行 `stdd agent verify deploy-staging --dry-run`
- **THEN** 系统 SHALL 展示每个 CP 的 action 和预期断言，但不实际执行任何操作

#### Scenario: CP 断言失败记录 <!-- confidence: high -->

- **GIVEN** CP-2 的 http_status 断言期望 200 但实际返回 503
- **WHEN** 执行 `stdd agent verify deploy-staging`
- **THEN** 系统 SHALL 记录 "CP-2 FAILED: http_status expected 200, got 503"
- **AND** 继续执行后续 CP（不因单个 CP 失败而中止）
- **AND** 最终以非零状态码退出，输出 agent-verification-report.md

#### Scenario: 不自动回滚 <!-- confidence: medium -->

- **GIVEN** CP-2 断言失败且 agent_spec 定义了 rollback 步骤
- **WHEN** 验证管线完成所有 CP 执行
- **THEN** 系统 SHALL NOT 自动执行 rollback
- **AND** 报告 SHALL 包含 rollback 步骤建议，提示用户手动执行或确认后执行

#### Scenario: 无外部依赖验证 <!-- confidence: high -->

- **GIVEN** agent_spec 的操作均在单个系统上执行（本地 Docker / 本地文件系统）
- **WHEN** 执行 `stdd agent verify <task>`
- **THEN** 验证管线 SHALL NOT 依赖任何外部系统（不连接远程服务器 / 不调用第三方 API）
- **AND** 所有 CP 的执行 SHALL 在本地完成
