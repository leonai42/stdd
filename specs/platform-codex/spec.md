# Spec: OpenAI Codex CLI 平台适配器

> 对应 proposal C1 | 1 个 New Capability
> platform-codex

## ADDED Requirements

### Requirement: stdd install codex <!-- confidence: high -->

STDD SHALL 支持 `stdd install codex` 命令，将 STDD 6 阶段 skill 部署到 Codex CLI 可识别的项目目录。

**证据来源**：proposal.md `What Changes > C1` + `Capabilities > New > platform-codex`

#### Scenario: 安装到项目目录 <!-- confidence: high -->

- **GIVEN** 项目已安装 STDD V2.9.4 且 Codex CLI 为已安装的编码代理
- **WHEN** 执行 `stdd install codex`
- **THEN** 系统 SHALL 创建 `.codex/skills/` 目录
- **AND** 将 6 个阶段 skill 复制为 `.codex/skills/stdd-<phase>/SKILL.md`
- **AND** 映射关系：`understand.md` → `stdd-understand/SKILL.md`
- **AND** 每个 SKILL.md 包含 YAML frontmatter（name + description + stdd_version）

#### Scenario: 与 Claude Code skills 共存 <!-- confidence: high -->

- **GIVEN** 项目同时存在 `.codex/skills/` 和 `.claude/skills/`
- **WHEN** Codex CLI 和 Claude Code 分别启动并加载 skills
- **THEN** Codex CLI SHALL 读取 `.codex/skills/`（Codex 路径）
- **AND** Claude Code SHALL 读取 `.claude/skills/`（Claude Code 路径）
- **AND** 两个平台的 skill 内容 SHALL 来自同一 master（`.stdd/skills/`）

#### Scenario: 安装后 AGENTS.md 包含 STDD 引用 <!-- confidence: medium -->

- **GIVEN** 项目根目录存在 `AGENTS.md` 文件
- **WHEN** 执行 `stdd install codex`
- **THEN** 系统 SHALL 检查 `AGENTS.md` 是否包含 STDD 工作流关键词
- **AND** 如果未包含 SHALL 输出提示建议手动添加引用
- **AND** 系统 SHALL NOT 自动修改 `AGENTS.md`

#### Scenario: 全局安装 <!-- confidence: medium -->

- **GIVEN** 开发者希望所有项目都使用 STDD skills
- **WHEN** 执行 `stdd install codex --global`
- **THEN** 系统 SHALL 安装 skills 到 `~/.codex/skills/`
- **AND** 全局 skills 可被所有 Codex CLI 项目发现

#### Scenario: 不支持的平台错误 <!-- confidence: high -->

- **GIVEN** install.py platform_map 中不含 `codex`
- **WHEN** 执行 `stdd install codex`
- **THEN** 系统 SHALL 输出 "不支持的平台: codex" 并列出支持平台

---

### Requirement: Codex skill frontmatter 格式兼容 <!-- confidence: high -->

Codex 平台的 skill 文件 SHALL 使用与 Claude Code 相同的 YAML frontmatter 格式（name + description），确保跨平台 skill 一致性。

**证据来源**：design.md `Decisions > 2. Codex frontmatter 格式`

#### Scenario: frontmatter 格式与 claude-code 一致 <!-- confidence: high -->

- **GIVEN** `_make_claude_code_frontmatter` 生成 Claude Code 格式 frontmatter
- **WHEN** 为 Codex 平台生成 skill frontmatter
- **THEN** 系统 SHALL 复用 `_make_claude_code_frontmatter` 函数
- **AND** 生成的 frontmatter SHALL 包含 `name` 和 `description` 字段
- **AND** 如果 `stdd_version` 可用 SHALL 包含版本号

#### Scenario: Codex CLI 可解析 frontmatter <!-- confidence: medium -->

- **GIVEN** `.codex/skills/stdd-understand/SKILL.md` 包含 YAML frontmatter
- **WHEN** Codex CLI 启动并扫描 skills 目录
- **THEN** Codex CLI SHALL 正确解析 YAML frontmatter
- **AND** skill 名称和描述 SHALL 在 Codex CLI 中可见
