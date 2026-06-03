# Capability: CI/CD 集成 (ci-integration)

## ADDED Requirements

### Requirement: CI 文件生成

系统 SHALL 提供 `stdd ci` CLI 命令组，生成 GitHub Actions / Pre-commit / PR Bot 配置文件。

#### Scenario: 交互式初始化所有 CI 文件

- **GIVEN** 用户项目根目录下不存在 `.github/workflows/` 目录
- **WHEN** 执行 `stdd ci init`
- **THEN** 系统 SHALL 创建 `.github/workflows/stdd-quality.yml`
- **AND** SHALL 创建 `.pre-commit-config.yaml`
- **AND** SHALL 创建 `.github/stdd-pr-comment.md`
- **AND** 生成前 SHALL 检测已有文件并提示是否覆盖

#### Scenario: 单独生成工作流文件

- **GIVEN** 用户只需要 GitHub Actions workflow
- **WHEN** 执行 `stdd ci generate workflow`
- **THEN** 系统 SHALL 仅生成 `.github/workflows/stdd-quality.yml`
- **AND** workflow SHALL 包含 job：validate → pytest --cov → diff → lint → typecheck → check-failures

#### Scenario: 生成 pre-commit hook

- **GIVEN** 项目已有 `.pre-commit-config.yaml`
- **WHEN** 执行 `stdd ci generate pre-commit`
- **THEN** 系统 SHALL 检测已有文件并提示
- **AND** 用户确认后 SHALL 在已有配置中追加 STDD hook 段

#### Scenario: 根据质量配置调整生成内容

- **GIVEN** `.stdd/config.d/quality.yaml` 中 coverage_target 设为 85，python_version 设为 "3.12"
- **WHEN** 生成 GitHub Actions workflow
- **THEN** workflow YAML SHALL 使用 Python 3.12
- **AND** SHALL 包含 `--cov-fail-under=85` 参数

#### Scenario: dry-run 预览

- **GIVEN** 用户想预览生成结果
- **WHEN** 执行 `stdd ci init --dry-run`
- **THEN** 系统 SHALL 输出所有将要生成的文件内容和路径
- **AND** SHALL 不创建任何文件

### Requirement: CI 失败模式检查

系统 SHALL 提供 `stdd ci check-failures` 命令，实现 11 类失败模式的确定性子集检查。

#### Scenario: 运行确定性检查子集

- **GIVEN** 当前 change 的 proposal.md / specs / test-plan.md 完整
- **WHEN** 执行 `stdd ci check-failures`
- **THEN** 系统 SHALL 检查：(a) 文件存在性（proposal/design/specs/test-plan），(b) TC-ID 唯一性，(c) SHALL 关键字存在，(d) AND 子句数 ≤ 5，(e) TC 数量 ≥ Scenario 数量
- **AND** 输出通过/失败的逐项结果

#### Scenario: 输出检查报告

- **GIVEN** check-failures 发现了 2 个问题
- **WHEN** 检查完成
- **THEN** 系统 SHALL 按 `.stdd/templates/failure-check-report.md` 格式输出报告
- **AND** 每个问题 SHALL 标注对应的失败模式类别（a-k）

#### Scenario: 明确标注覆盖边界

- **GIVEN** check-failures 命令执行
- **WHEN** 输出结果
- **THEN** 系统 SHALL 在结果末尾显示提示："确定性检查覆盖约 60% 的失败模式。完整 11 类检查（含语义分析）请使用 /stdd-verify"
- **AND** SHALL 列出未覆盖的失败模式及原因

### Requirement: CI 配置段

系统 SHALL 在 `quality.yaml` 中增加 `ci` 配置段。

#### Scenario: CI 配置读取

- **GIVEN** `quality.yaml` 包含 `ci` 配置段，`github_actions.python_version: "3.11"`
- **WHEN** 执行 `stdd ci generate workflow`
- **THEN** 生成的 workflow SHALL 使用 python-version: "3.11"
- **AND** 如果 ci.enabled 为 false，`stdd ci` 命令仍可正常使用（仅影响 CI 服务的自动触发行为）

### Requirement: PR Bot 模板

系统 SHALL 提供 PR 自动评论模板，用于在 PR 中摘要 STDD 质量门结果。

#### Scenario: PR 模板内容

- **GIVEN** 生成的 `.github/stdd-pr-comment.md`
- **WHEN** CI workflow 在 PR 上运行
- **THEN** PR 评论 SHALL 包含：测试通过率、覆盖率、diff 摘要、失败模式检查结果
- **AND** SHALL 包含指向 test-report.md 和 design-adjustments.md 的链接
