# skill-only-upgrade — 行为规格

> Capability: skill-only-upgrade (New)
> Change: skill-version-check-upgrade
> Confidence: high (SC-UP-001~007, SC-UP-009), medium (SC-UP-004, SC-UP-008, SC-UP-010)

## REQ-UP-001: 技能调用入口

### Scenario: SC-UP-001 — 升级技能注册

- **GIVEN** STDD 已通过 `stdd install` 或手动安装到当前平台
- **WHEN** 用户输入 `/stdd-upgrade`
- **THEN** AI SHALL 识别 `stdd-upgrade` 为有效技能并执行升级流程

## REQ-UP-002: 平台检测

### Scenario: SC-UP-002 — 检测 Claude Code 平台

- **GIVEN** 项目目录下 `.claude/skills/` 目录存在
- **WHEN** 升级技能执行平台检测步骤
- **THEN** AI SHALL 识别当前平台为 `claude-code`

### Scenario: SC-UP-003 — 检测 OpenCode 平台

- **GIVEN** 项目目录下 `.opencode/skills/` 目录存在
- **WHEN** 升级技能执行平台检测步骤
- **THEN** AI SHALL 识别当前平台为 `opencode`

### Scenario: SC-UP-004 — 多平台共存处理

- **GIVEN** 项目目录下同时存在 `.claude/skills/` 和 `.opencode/skills/`
- **WHEN** 升级技能执行平台检测步骤
- **THEN** AI SHALL 列出所有检测到的平台，并对每个平台执行技能重装

## REQ-UP-003: 资源同步

### Scenario: SC-UP-005 — 同步技能文件

- **GIVEN** 网络可达 `https://raw.githubusercontent.com/leonai42/stdd/master/.stdd/skills/`
- **WHEN** 升级技能执行资源同步步骤
- **THEN** 项目 `.stdd/skills/` 下的 6 个阶段技能文件 + `_shared/` 目录 + `upgrade.md` SHALL 更新为源仓库最新版本

### Scenario: SC-UP-006 — 同步配置文件

- **GIVEN** 网络可达 GitHub raw
- **WHEN** 升级技能执行资源同步步骤
- **THEN** 项目 `.stdd/config.d/` 下的配置文件 SHALL 更新为最新版本
- **AND** `project.yaml` 中的 `project` 和 `paths` 字段 SHALL 保留项目原有值

### Scenario: SC-UP-007 — 同步模板文件

- **GIVEN** 网络可达 GitHub raw
- **WHEN** 升级技能执行资源同步步骤
- **THEN** 项目 `.stdd/templates/` 和 `.stdd/templates/canonical/` SHALL 更新为最新版本

### Scenario: SC-UP-008 — 网络不可用降级

- **GIVEN** GitHub raw 返回超时或 403 错误
- **WHEN** 升级技能尝试拉取文件
- **THEN** AI SHALL 向用户展示明确的网络错误提示
- **AND** AI SHALL 提供手动下载 URL（`https://github.com/leonai42/stdd`）和手动升级步骤说明

## REQ-UP-004: 版本更新与平台重装

### Scenario: SC-UP-009 — 更新版本文件

- **GIVEN** 所有资源同步完成，源版本为 `2.9.5`
- **WHEN** 升级技能写入版本信息
- **THEN** `.stdd/version.yaml` 的 `stdd_version` SHALL 更新为 `2.9.5`
- **AND** `upgraded_at` SHALL 更新为当前 ISO 8601 时间戳

### Scenario: SC-UP-010 — 重装平台技能

- **GIVEN** 平台检测为 `claude-code`，资源同步完成，源版本为 `2.9.5`
- **WHEN** 升级技能执行平台重装步骤
- **THEN** `.claude/skills/stdd-*/SKILL.md` SHALL 从最新 `.stdd/skills/` 重新生成
- **AND** 每个 SKILL.md 的 frontmatter SHALL 包含 `stdd_version: "2.9.5"`
