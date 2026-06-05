# Capability: DOCS — 文档修复

## MODIFIED Requirements

### Requirement: DESIGN.md 版本更新

DESIGN.md SHALL 反映 V2.0 版本号，包含完整版本历史。

#### Scenario: 标题显示 V2.0

- **GIVEN** 查看 DESIGN.md 第3行
- **WHEN** 检查版本声明
- **THEN** SHALL 显示 "V2.0"

#### Scenario: 版本历史包含 V2.0

- **GIVEN** DESIGN.md 附录 C
- **WHEN** 查看版本历史
- **THEN** SHALL 包含 V1.4、V2.0、V2.0.1 条目

### Requirement: DEPLOY.md 版本更新

DEPLOY.md SHALL 反映 V2.0 版本号和 config.d/ 配置架构。

#### Scenario: 标题显示 V2.0

- **GIVEN** 查看 DEPLOY.md 第3行
- **WHEN** 检查版本声明
- **THEN** SHALL 显示 "V2.0"

#### Scenario: 配置引用指向 config.d/

- **GIVEN** DEPLOY.md 引用配置路径
- **WHEN** 检查所有引用
- **THEN** SHALL 指向 config.d/ 而非 config.yaml

### Requirement: 平台 Skills 同步

`.stdd/platforms/` 下的平台 Skill 文件 SHALL 引用 config.d/ 而非 config.yaml。

#### Scenario: 平台 Skills config 引用

- **GIVEN** .stdd/platforms/claude-code/skills/stdd-build.md
- **WHEN** 检查配置引用
- **THEN** SHALL 指向 config.d/project.yaml

### Requirement: 文档 config.yaml 引用清零

所有文档（DESIGN、DEPLOY、STDD、TROUBLESHOOTING、EXTENDING）SHALL NOT 包含对已删除 `config.yaml` 的引用。

#### Scenario: 文档无 config.yaml 引用

- **GIVEN** 全部文档文件
- **WHEN** 搜索 config.yaml
- **THEN** SHALL NOT 出现（除历史版本说明外）

### Requirement: 模板计数一致

所有文档中模板数量 SHALL 统一为 9 个（含 long-range-auth.md）。

#### Scenario: 模板数量声明一致

- **GIVEN** DESIGN.md、DEPLOY.md、AGENTS.md
- **WHEN** 检查模板数量声明
- **THEN** SHALL 均为 "9 个"

### Requirement: 文档补齐 CLI 命令

DESIGN.md 和 DEPLOY.md SHALL 包含全部 10 个 CLI 命令。

#### Scenario: CLI 命令完整

- **GIVEN** DESIGN.md 命令表
- **WHEN** 检查命令列表
- **THEN** SHALL 包含 rollback、diff、abort

### Requirement: 示例项目同步

`examples/hello-stdd/` 的 AGENTS.md SHALL 与主 AGENTS.md 保持一致。

#### Scenario: 示例 AGENTS 结构匹配

- **GIVEN** 示例项目 AGENTS.md
- **WHEN** 检查目录结构图
- **THEN** SHALL 包含 config.d/、_shared/、stdd/cli/

### Requirement: AGENTS.md 可移植性

AGENTS.md SHALL NOT 包含特定机器的绝对路径。

#### Scenario: 无绝对路径

- **GIVEN** AGENTS.md
- **WHEN** 搜索路径
- **THEN** SHALL NOT 包含 "D:\" 开头的绝对路径

### Requirement: 过时故障排除条目移除

TROUBLESHOOTING.md SHALL NOT 包含已过时的 config.yaml vs config.d/ 冲突条目。

#### Scenario: 无过时条目

- **GIVEN** TROUBLESHOOTING.md
- **WHEN** 查看条目列表
- **THEN** SHALL NOT 包含 config.yaml 冲突诊断

### Requirement: EXTENDING.md 路径更新

EXTENDING.md SHALL 指向 V2.0 模块化目录结构。

#### Scenario: 扩展点路径正确

- **GIVEN** EXTENDING.md
- **WHEN** 查看扩展指南
- **THEN** 命令注册 SHALL 指向 stdd/cli/__init__.py
