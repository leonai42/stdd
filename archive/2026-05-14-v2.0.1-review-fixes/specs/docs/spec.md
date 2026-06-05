# Capability: DOCS — 文档修复

## MODIFIED Requirements

### Requirement: README.md 版本更新

README.md SHALL 反映 V2.0 版本号和新功能。

#### Scenario: README 显示 V2.0

- **GIVEN** 项目根目录存在 README.md
- **WHEN** 查看首行版本声明
- **THEN** SHALL 显示 "V2.0"

### Requirement: 模板文件完整

.stdd/templates/ SHALL 包含全部 8 个模板文件。

#### Scenario: 8 个模板全部存在

- **GIVEN** 项目已初始化
- **WHEN** 检查 .stdd/templates/ 目录
- **THEN** SHALL 包含 proposal.md、design.md、spec.md、test-plan.md、tasks.md、slices.md、design-adjustments.md、test-report.md

### Requirement: Skills 引用 config.d/

核心 Skill 文件 SHALL 引用 `config.d/` 而非 `config.yaml` 作为配置来源。

#### Scenario: build.md 引用 config.d/

- **GIVEN** build.md Skill 需要读取项目语言配置
- **WHEN** 引用配置路径
- **THEN** SHALL 指向 `config.d/project.yaml`

### Requirement: AGENTS.md 结构更新

AGENTS.md SHALL 反映 V2.0 目录结构（包含 stdd/cli/、config.d/、_shared/）。

#### Scenario: 目录结构图包含 V2.0 新增目录

- **GIVEN** AGENTS.md 包含项目结构
- **WHEN** 查看结构图
- **THEN** SHALL 包含 stdd/cli/、config.d/、_shared/
