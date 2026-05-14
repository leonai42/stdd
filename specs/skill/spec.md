# Capability: SKILL — 技能系统改进

## MODIFIED Requirements

### Requirement: 核心 Skill 作为平台 Skill 的唯一来源

`stdd install` 命令 SHALL 从核心 Skill（`.stdd/skills/`）读取内容，根据平台模板生成平台 Skill，不再依赖手动维护的 `.stdd/platforms/*/skills/` 副本。

#### Scenario: install 从核心 Skill 生成 Claude Code 版本

- **GIVEN** `.stdd/skills/spec.md` 核心 Skill 内容已更新
- **WHEN** 用户执行 `stdd install claude-code`
- **THEN** 生成的 `.claude/skills/stdd-spec/SKILL.md` SHALL 包含核心 Skill 的完整内容
- **AND** frontmatter SHALL 包含 `name: stdd-spec` 和对应描述

#### Scenario: install 从核心 Skill 生成 WorkBuddy 版本

- **GIVEN** `.stdd/skills/spec.md` 核心 Skill 内容已更新
- **WHEN** 用户执行 `stdd install workbuddy`
- **THEN** 生成的 Skill SHALL 包含 `trigger_keywords` 的 YAML frontmatter
- **AND** 内容 SHALL 与核心 Skill 一致

### Requirement: Skill 共享内容 DRY

核心 Skill 文件 SHALL 通过引用机制复用 `_shared/` 目录下的共享片段，而非各自维护重复内容。

#### Scenario: 确认门消息模板集中维护

- **GIVEN** `_shared/confirm-gate.md` 包含确认门消息模板
- **WHEN** 修改确认消息格式
- **THEN** 只需修改 `_shared/confirm-gate.md` 一处
- **AND** 所有引用此模板的 Skill（understand/spec/verify）SHALL 自动使用新格式

### Requirement: Skill-CLI 桥接检查

Skill 涉及 CLI 操作时，执行前 SHALL 检查 CLI 可用性，执行后 SHALL 检查退出码。

#### Scenario: CLI 不可用时提前报告

- **GIVEN** `python bin/stdd --help` 返回非零退出码
- **WHEN** Skill 尝试调用 CLI 命令
- **THEN** 系统 SHALL 报告"CLI 不可用"并暂停
- **AND** 系统 SHALL NOT 尝试执行后续 CLI 操作

#### Scenario: CLI 命令执行失败时报告

- **GIVEN** CLI 可用但命令返回非零退出码
- **WHEN** Skill 调用 CLI 命令
- **THEN** 系统 SHALL 报告命令失败和退出码
- **AND** 系统 SHALL 暂停等待用户处理
