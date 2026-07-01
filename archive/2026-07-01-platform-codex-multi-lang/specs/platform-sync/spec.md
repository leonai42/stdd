# Spec: 平台同步更新

> 对应 proposal C7 | 1 个 Modified Capability
> platform-sync

## MODIFIED Requirements

### Requirement: install.py platform_map 扩展 <!-- confidence: high -->

`stdd/cli/commands/install.py` 的 `platform_map` SHALL 新增 `codex` 平台配置，支持 `stdd install codex` 命令。

**证据来源**：proposal.md `What Changes > C7` + `Capabilities > Modified > platform-sync`

#### Scenario: platform_map 包含 codex 条目 <!-- confidence: high -->

- **GIVEN** `install.py` 的 `platform_map` 包含 5 个平台（claude-code, workbuddy, trae, cursor, opencode）
- **WHEN** 新增 Codex 平台支持后
- **THEN** `platform_map` SHALL 新增 `"codex"` 键
- **AND** codex 配置 SHALL 包含：`target_base: ".codex/skills"`, `description: "OpenAI Codex CLI"`, `frontmatter_fn: _make_claude_code_frontmatter`, `is_dir_per_skill: True`, `skill_filename: "SKILL.md"`

#### Scenario: stdd install codex --help 可见 <!-- confidence: high -->

- **GIVEN** `install.py` 已注册 codex 平台
- **WHEN** 执行 `stdd install --help`
- **THEN** 帮助信息 SHALL 列出 `codex` 为可用平台选项
- **AND** 平台描述 SHALL 为 "OpenAI Codex CLI"

#### Scenario: 使用提示正确 <!-- confidence: medium -->

- **GIVEN** `stdd install codex` 执行成功
- **WHEN** 安装完成后输出使用提示
- **THEN** 提示 SHALL 包含 Codex CLI 的 skill 触发方式（如 `/stdd-understand`）
- **AND** 提示 SHALL 说明 skills 安装路径（`.codex/skills/`）

---

### Requirement: EXTENDING.md 平台列表更新 <!-- confidence: high -->

`EXTENDING.md` 的「现有平台参考」表格 SHALL 包含 Codex 平台条目。

**证据来源**：proposal.md `What Changes > C7`

#### Scenario: EXTENDING.md 包含 Codex 条目 <!-- confidence: high -->

- **GIVEN** `EXTENDING.md` 的现有平台参考表格包含 6 行（Claude Code/WorkBuddy/Trae/Cursor/Copilot/Aider）
- **WHEN** 新增 Codex 平台后
- **THEN** 表格 SHALL 增加一行：Codex | directory-per-skill（`.codex/skills/`） | YAML frontmatter, `/` slash commands

---

### Requirement: AGENTS.md 元信息更新 <!-- confidence: high -->

项目根 `AGENTS.md` 和 `STDD.md` SHALL 同步更新平台数量（7→8）和语言数量（5→10）。

**证据来源**：design.md `Decisions > 6`

#### Scenario: 平台和语言计数更新 <!-- confidence: high -->

- **GIVEN** `AGENTS.md` 当前描述 "适配 6 大 AI 编程平台" 和 "支持 5 门语言"
- **WHEN** 完成 Codex 平台和 5 门语言的新增
- **THEN** `AGENTS.md` SHALL 更新为 "适配 8 大 AI 编程平台"（+Codex+OpenCode）
- **AND** `AGENTS.md` SHALL 更新为 "支持 10 门语言"
- **AND** `STDD.md` SHALL 做相同更新

#### Scenario: AGENTS.md 与 STDD.md 一致 <!-- confidence: medium -->

- **GIVEN** 两个文件均包含平台和语言数量描述
- **WHEN** Phase 5 VERIFY 执行文档一致性检查
- **THEN** 两个文件的平台数量 SHALL 相同
- **AND** 两个文件的语言数量 SHALL 相同
