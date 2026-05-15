# Capability: platform-copilot

## NEW Requirements

### Requirement: GitHub Copilot 指令文件

系统 SHALL 提供 `.github/copilot-instructions.md` 格式的 STDD 方法论指令文件，使 GitHub Copilot 在代码生成和审查时遵循 STDD 规范。

#### Scenario: Copilot 指令文件存在且内容完整

- **GIVEN** `.stdd/platforms/copilot/` 目录存在
- **WHEN** 用户将 `copilot-instructions.md` 复制到项目 `.github/` 目录
- **THEN** 指令文件 SHALL 包含：STDD 流程概述、测试优先原则（RED→GREEN→REFACTOR）、编码规范引用、Commit 规范
- **AND** 指令文件 SHALL 引用 `.stdd/standards/` 中的语言规范文件

#### Scenario: Copilot 根据指令调整代码生成行为

- **GIVEN** 项目已启用 `.github/copilot-instructions.md`
- **WHEN** Copilot 生成代码或提供建议
- **THEN** Copilot SHALL 遵循指令中的测试优先原则
- **AND** 生成的代码 SHALL 符合指令中引用的语言规范标准
