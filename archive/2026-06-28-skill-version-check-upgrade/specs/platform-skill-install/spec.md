# platform-skill-install — 行为规格

> Capability: platform-skill-install (Modified)
> Change: skill-version-check-upgrade
> Confidence: high

## REQ-PSI-001: install.py 扩展支持 upgrade 技能与版本号注入

### Scenario: SC-PSI-001 — SKILL_META 包含 upgrade 条目

- **GIVEN** STDD 源码 `.stdd/skills/upgrade.md` 存在
- **WHEN** 执行 `stdd install <任意平台>`
- **THEN** `SKILL_META["upgrade"]` SHALL 存在，包含 `name: "stdd-upgrade"`、`description`、`keywords` 字段
- **AND** `stdd-upgrade/SKILL.md` SHALL 被安装到目标平台的技能目录

### Scenario: SC-PSI-002 — frontmatter 包含版本号

- **GIVEN** STDD 源版本为 `2.9.5`
- **WHEN** `stdd install` 为任意技能文件生成 YAML frontmatter
- **THEN** 生成的 frontmatter SHALL 包含 `stdd_version: "2.9.5"` 字段
- **AND** 版本号值 SHALL 与 `get_source_version()` 返回值一致

### Scenario: SC-PSI-003 — 所有已支持平台均安装 upgrade

- **GIVEN** 用户指定平台为 `claude-code` / `opencode` / `cursor` / `workbuddy` / `trae` 中任意一个
- **WHEN** 执行 `stdd install <platform>`
- **THEN** upgrade 技能 SHALL 出现在该平台的安装输出列表中
