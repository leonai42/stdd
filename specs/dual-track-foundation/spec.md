# Spec: 双轨制文档基础（Dual-Track Foundation）

> 对应板块 E（E5）| 1 个 New Capability
> dual-track-foundation

## ADDED Requirements

### Requirement: canonical/ 目录结构 <!-- confidence: high -->

STDD SHALL 定义标准化的 `canonical/` 目录结构，作为 Canonical YAML 文件的统一存放位置。

**证据来源**：proposal.md `Capabilities > New > dual-track-foundation`

#### Scenario: 初始化 canonical 目录 <!-- confidence: high -->

- **GIVEN** 项目已安装 STDD V2.7
- **WHEN** 执行 `stdd canon init`
- **THEN** 系统 SHALL 创建 `canonical/proposals/`、`canonical/designs/`、`canonical/specs/code/`、`canonical/specs/agent/` 四个目录
- **AND** 在 `canonical/` 根目录生成 `.canon-index.yaml` 索引文件

#### Scenario: canonical/ 目录可选 <!-- confidence: high -->

- **GIVEN** 项目未执行 `stdd canon init`
- **WHEN** 执行任何 STDD Phase 1-6 流程
- **THEN** 系统 SHALL 按照 V2.5 的纯 Markdown 模式运行，不产生任何错误或警告

---

### Requirement: stdd canon generate CLI <!-- confidence: high -->

STDD SHALL 提供 `stdd canon generate` 命令，将 Canonical YAML 单向生成为 Human View Markdown。

**证据来源**：proposal.md `Capabilities > New > dual-track-foundation`

#### Scenario: 生成 Human View <!-- confidence: high -->

- **GIVEN** `canonical/proposals/2026-06-01-feature.yaml` 已存在
- **WHEN** 执行 `stdd canon generate 2026-06-01-feature --type proposal`
- **THEN** 系统 SHALL 读取 YAML → AI 按 `templates/human-view/proposal-brief.md` 模板生成 `changes/<name>/proposal.md`
- **AND** 生成的 proposal.md 头部 SHALL 包含 `source_hash: <sha256-of-yaml>` 和 `generated_at: <timestamp>`

#### Scenario: 生成全部 Human View <!-- confidence: high -->

- **GIVEN** `canonical/` 目录下存在多个 change 的 YAML
- **WHEN** 执行 `stdd canon generate --all`
- **THEN** 系统 SHALL 为每个 change 生成全部 Human View（proposal.md / design.md / spec-summary.md）

#### Scenario: Canonical 修改后 Human View 过时检测 <!-- confidence: medium -->

- **GIVEN** `canonical/proposals/feature.yaml` 已修改（last_modified 晚于 proposal.md 的 generated_at）
- **WHEN** 执行 `stdd canon verify feature`
- **THEN** 系统 SHALL 输出 ⚠️ 警告："Human View may be stale — Canonical modified at <time>"
