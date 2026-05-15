# Capability: platform-aider

## NEW Requirements

### Requirement: Aider 约定文件

系统 SHALL 提供 Aider AI 编程工具的 `CONVENTIONS.md` 约定文件和 `.aider.conf.yml` 配置示例，使 Aider 在代码生成和修改时遵循 STDD 开发规范。

#### Scenario: Aider 约定文件存在且内容完整

- **GIVEN** `.stdd/platforms/aider/` 目录存在
- **WHEN** 用户将 `CONVENTIONS.md` 和 `.aider.conf.yml` 复制到项目根目录
- **THEN** `CONVENTIONS.md` SHALL 包含：编码规范引用、测试规范要求、命名约定、错误处理原则
- **AND** `.aider.conf.yml` SHALL 包含：`read` 字段引用 `CONVENTIONS.md` 和 `.stdd/standards/` 规范文件

#### Scenario: Aider 根据约定调整代码行为

- **GIVEN** 项目根目录存在 `CONVENTIONS.md`
- **WHEN** Aider 生成或修改代码
- **THEN** Aider SHALL 遵循 `CONVENTIONS.md` 中的编码规范
- **AND** 生成的测试代码 SHALL 遵循 `CONVENTIONS.md` 中的测试命名和结构规范
