# Capability: platform-cursor

## NEW Requirements

### Requirement: Cursor 规则文件

系统 SHALL 提供 Cursor IDE 的 `.cursor/rules/stdd.md` 规则文件，描述 STDD 6 阶段方法论的核心流程和触发关键词，使 Cursor 用户在 AI 对话中能够启动 STDD 工作流。

#### Scenario: Cursor 规则文件存在且内容完整

- **GIVEN** `.stdd/platforms/cursor/` 目录存在
- **WHEN** 用户将规则文件复制到项目 `.cursor/rules/` 目录
- **THEN** 规则文件 SHALL 包含 STDD 6 阶段概述（Understand→Spec→Slice→Build→Verify→Deliver）
- **AND** 每个阶段 SHALL 包含：阶段目标、触发关键词、产出物、下一阶段
- **AND** 规则文件 SHALL 包含 3 个确认门（Gate 1/2/3）的说明

#### Scenario: Cursor 规则触发 STDD 工作流

- **GIVEN** Cursor 已加载 `.cursor/rules/stdd.md` 规则
- **WHEN** 用户在对话中使用触发关键词（如 "STDD"、"spec-driven"、"stdd-understand"）
- **THEN** Cursor AI SHALL 识别并引导用户进入 STDD 6 阶段流程
- **AND** AI SHALL 按照规则文件中的流程顺序执行对应阶段
