# Spec: OpenCode 平台适配器

> 对应板块 B（B4）| 1 个 New Capability
> opencode-platform-adapter

## ADDED Requirements

### Requirement: stdd install opencode <!-- confidence: high -->

STDD SHALL 支持 `stdd install opencode` 命令，将 STDD skill 部署到 OpenCode 可识别的路径。

**证据来源**：proposal.md `Capabilities > New > opencode-platform-adapter`

#### Scenario: 安装到项目目录 <!-- confidence: high -->

- **GIVEN** 项目已安装 STDD V2.7 且 OpenCode 为已安装的 IDE
- **WHEN** 执行 `stdd install opencode`
- **THEN** 系统 SHALL 创建 `.opencode/skills/` 目录
- **AND** 将 6 个阶段 skill 复制为 `.opencode/skills/stdd-<phase>/SKILL.md`
- **AND** 映射关系：`understand.md` → `stdd-understand/SKILL.md`

#### Scenario: 双路径 fallback <!-- confidence: high -->

- **GIVEN** 项目同时存在 `.opencode/skills/` 和 `.claude/skills/`
- **WHEN** OpenCode 启动并加载 skills
- **THEN** OpenCode SHALL 优先读取 `.opencode/skills/`（主路径）
- **AND** 如果主路径不存在 → fallback 到 `.claude/skills/`（已在 V2.5 中支持）

#### Scenario: 全局安装 <!-- confidence: medium -->

- **GIVEN** 开发者希望所有项目都使用 STDD skills
- **WHEN** 执行 `stdd install opencode --global`
- **THEN** 系统 SHALL 安装 skills 到 `~/.config/opencode/skills/`
- **AND** 全局 skills 可被所有 OpenCode 项目发现

#### Scenario: 不自动修改 opencode.json <!-- confidence: high -->

- **GIVEN** 项目已有 `opencode.json` 配置文件
- **WHEN** 执行 `stdd install opencode`
- **THEN** 系统 SHALL NOT 自动修改 `opencode.json`
- **AND** 如果 `opencode.json` 的 instructions 字段未包含 AGENTS.md → 输出提示建议手动添加
