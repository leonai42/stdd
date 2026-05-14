# Capability: TEMPLATE — 文档模板

## MODIFIED Requirements

### Requirement: spec.md 模板包含 AND 多条件示例

spec.md 模板 SHALL 包含一个使用 HTML 注释标注的多 AND 用法示例，引导 AI 正确生成多条件 Scenario。

#### Scenario: 模板包含 AND 示例

- **GIVEN** 用户/系统读取 `.stdd/templates/spec.md` 模板
- **WHEN** 查看模板内容
- **THEN** 模板 SHALL 包含至少 1 个带有 2 条 AND 的 Scenario 示例（HTML 注释形式）
- **AND** 示例 SHALL 说明 AND 最多可扩展至 5 条

### Requirement: tasks.md 模板包含优先级和依赖示例

tasks.md 模板 SHALL 包含优先级标注和依赖关系的示例条目。

#### Scenario: 模板包含优先级标注

- **GIVEN** 用户/系统读取 `.stdd/templates/tasks.md` 模板
- **WHEN** 查看模板内容
- **THEN** 模板 SHALL 包含标注了 P0/P1/P2 优先级的任务条目示例

#### Scenario: 模板包含依赖关系示例

- **GIVEN** 用户/系统读取 `.stdd/templates/tasks.md` 模板
- **WHEN** 查看模板内容
- **THEN** 模板 SHALL 包含标注了（依赖 #N）的任务条目示例

### Requirement: README.md 与 STDD.md 职责分离

README.md SHALL 作为项目入口提供概览，六阶段详细描述 SHALL 引用 STDD.md。STDD.md SHALL 保持自包含的完整流程描述。

#### Scenario: README 简要引用六阶段

- **GIVEN** README.md 中的六阶段流程部分
- **WHEN** 查看内容
- **THEN** 该部分 SHALL 为简要表格形式
- **AND** SHALL 包含指向 STDD.md 的引用链接

#### Scenario: STDD.md 保持完整流程

- **GIVEN** STDD.md 作为独立可加载的规则文件
- **WHEN** 查看内容
- **THEN** 该文件 SHALL 包含完整的六阶段流程描述
- **AND** SHALL 包含关键规则和目录结构说明
