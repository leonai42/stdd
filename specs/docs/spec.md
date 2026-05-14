# Capability: DOCS — 文档与生态

## NEW Requirements

### Requirement: CHANGELOG.md

项目 SHALL 包含 `CHANGELOG.md` 文件，记录从 V1.0 至当前版本的完整版本历史。

#### Scenario: CHANGELOG 包含完整版本历史

- **GIVEN** 项目根目录存在 CHANGELOG.md
- **WHEN** 查看内容
- **THEN** 文件 SHALL 包含 V1.0、V1.1、V1.2、V1.4（V1.2.1+V1.3 合并）、V2.0 的版本条目
- **AND** 每个版本 SHALL 包含日期和变更摘要

### Requirement: TROUBLESHOOTING.md

项目 SHALL 包含 `TROUBLESHOOTING.md` 文件，覆盖常见问题和解决方案。

#### Scenario: 覆盖至少 5 个常见问题

- **GIVEN** 项目根目录存在 TROUBLESHOOTING.md
- **WHEN** 查看内容
- **THEN** 文件 SHALL 覆盖≥5 个问题（含 Windows Unicode 错误、路径问题、PyYAML 安装失败等）
- **AND** 每个问题 SHALL 包含症状描述和解决步骤

### Requirement: EXTENDING.md

项目 SHALL 包含 `EXTENDING.md` 文件，说明如何扩展 STDD。

#### Scenario: 覆盖 3 个扩展点

- **GIVEN** 项目根目录存在 EXTENDING.md
- **WHEN** 查看内容
- **THEN** 文件 SHALL 说明如何新增平台适配
- **AND** SHALL 说明如何新增开发语言规范
- **AND** SHALL 说明如何新增自定义失败模式检查

### Requirement: 示例项目

项目 SHALL 包含 `examples/hello-stdd/` 目录，提供可独立运行的完整演示。

#### Scenario: 示例项目可独立初始化

- **GIVEN** examples/hello-stdd/ 存在
- **WHEN** 在该目录执行 `python ../../bin/stdd init`
- **THEN** 系统 SHALL 成功初始化 STDD 目录结构

#### Scenario: 示例项目包含完整 6 阶段产出示例

- **GIVEN** examples/hello-stdd/ 存在
- **WHEN** 查看目录内容
- **THEN** SHALL 包含 proposal.md、design.md、specs/、test-plan.md 等 PHase 2 产出示例
- **AND** 文件 SHALL 包含实际内容（非模板占位符）
