# Capability: platform-sync

## MODIFIED Requirements

### Requirement: workbuddy 平台 V2.2 同步

workbuddy 平台下的 6 个 skill 文件 SHALL 与 claude-code 平台版本在内容上等价，覆盖 V2.2 全部特性，同时保留 workbuddy 特有的 YAML frontmatter 格式。

#### Scenario: workbuddy skill 文件内容等同 claude-code gold source

- **GIVEN** `.stdd/platforms/claude-code/skills/` 包含 V2.2 完整的 6 个 skill 文件
- **WHEN** 对比 workbuddy 和 claude-code 对应文件的内容
- **THEN** workbuddy 每个 skill 文件 SHALL 包含 claude-code 对应文件的所有 V2.2 关键特征
- **AND** 关键特征 SHALL 包括：Step 0 多路并行评审、11类失败模式(a-k)、长程模式运行协议、强制步骤清单、Gate review 结果展示、覆盖率诊断配置、E2E配置、模式选择强制化、长程权限配置、自动衔接指令、降级条件检测

#### Scenario: workbuddy 保留 platform-specific frontmatter

- **GIVEN** workbuddy 平台的 skill 文件使用 `version` 和 `trigger_keywords` 字段
- **WHEN** 同步 claude-code 内容到 workbuddy 文件
- **THEN** workbuddy 文件 SHALL 保留其现有的 frontmatter 格式（含 `version`、`trigger_keywords`）
- **AND** 仅正文内容 SHALL 被更新为 V2.2 版本

---

### Requirement: trae 平台 V2.2 同步

trae 平台下的 6 个 skill 文件 SHALL 与 claude-code 平台版本在内容上等价，覆盖 V2.2 全部特性。

#### Scenario: trae skill 文件内容等同 claude-code gold source

- **GIVEN** `.stdd/platforms/claude-code/skills/` 包含 V2.2 完整的 6 个 skill 文件
- **WHEN** 对比 trae 和 claude-code 对应文件的内容
- **THEN** trae 每个 skill 文件 SHALL 包含 claude-code 对应文件的所有 V2.2 关键特征
- **AND** 关键特征 SHALL 与 workbuddy 同步要求相同（11 项特征清单）

#### Scenario: trae 保留 platform-specific format

- **GIVEN** trae 平台的 skill 文件当前无 YAML frontmatter
- **WHEN** 同步 claude-code 内容到 trae 文件
- **THEN** trae 文件 SHALL 在正文开头添加最小 frontmatter（`name` + `description`）
- **AND** 正文内容 SHALL 更新为 V2.2 版本

---

### Requirement: 平台同步质量验证

同步后的平台文件 SHALL 通过一致性验证：关键 V2.2 特征在 claude-code / workbuddy / trae 三个平台的对应文件中出现次数一致。

#### Scenario: 三平台特征计数一致性

- **GIVEN** 三个平台的 6 个 skill 文件均已完成同步
- **WHEN** 使用 Grep 在三个平台中搜索 V2.2 关键特征关键词
- **THEN** 每个关键特征在三个平台中的出现次数 SHALL 相同（允许 ±1 误差，因 frontmatter 差异）
- **AND** 关键特征关键词 SHALL 包括：`Step 0.*多路并行`、`十一类失败模式`、`长程模式运行协议`、`强制步骤清单`、`Gate review`、`覆盖率诊断`、`E2E.*测试`、`模式选择.*强制`、`权限配置`、`自动衔接`、`降级条件`

---

## V2.10 ADDED Requirements

> 来源：2026-07-01-platform-codex-multi-lang

### Requirement: install.py platform_map 扩展（Codex）

`stdd/cli/commands/install.py` 的 `platform_map` SHALL 支持 `codex` 平台键，允许通过 `stdd install codex` 部署 STDD skill。

#### Scenario: platform_map 包含 codex 条目

- **GIVEN** `install.py` 的 `platform_map` 已更新
- **WHEN** 读取 `platform_map.keys()`
- **THEN** `"codex"` SHALL 在 `platform_map` 中
- **AND** codex 配置 SHALL 包含 `target_base: ".codex/skills"`, `is_dir_per_skill: True`, `skill_filename: "SKILL.md"`

#### Scenario: stdd install codex 部署成功

- **GIVEN** 项目已安装 STDD V2.10
- **WHEN** 执行 `stdd install codex`
- **THEN** 系统 SHALL 创建 `.codex/skills/stdd-<phase>/SKILL.md`（6 个 phase）
- **AND** 每个 SKILL.md SHALL 包含 YAML frontmatter（name + description + stdd_version）

---

### Requirement: EXTENDING.md 平台列表更新

`EXTENDING.md` SHALL 在「现有平台参考」表格中包含 Codex 平台条目。

#### Scenario: EXTENDING.md 包含 Codex

- **GIVEN** `EXTENDING.md` 已更新
- **WHEN** 读取「现有平台参考」表格
- **THEN** 表格 SHALL 包含 Codex 行
- **AND** 描述 SHALL 标注 "directory-per-skill" + "OpenAI Codex CLI"

---

### Requirement: AGENTS.md / STDD.md 元信息同步

项目根文档 SHALL 同步更新平台数量（8）和语言数量（10）。

#### Scenario: 文档计数一致

- **GIVEN** AGENTS.md, STDD.md, README.md, README_EN.md 均已更新
- **WHEN** 分别读取各文件的平台和语言计数
- **THEN** 所有文件的平台计数 SHALL 为 8
- **AND** 所有文件的语言计数 SHALL 为 10
