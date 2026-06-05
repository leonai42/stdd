# Capability: STATE — 配置与工具修复

## MODIFIED Requirements

### Requirement: read_config 类型安全

`read_config()` SHALL 验证 YAML 解析结果为 dict 类型后再合并，非 dict 类型 SHALL 跳过并警告。

#### Scenario: YAML 文件包含列表时安全降级

- **GIVEN** config.d/ 中某文件包含 YAML 列表（非 dict）
- **WHEN** read_config 解析该文件
- **THEN** 系统 SHALL 跳过该文件并输出警告
- **AND** 系统 SHALL NOT 崩溃

### Requirement: 移除旧 config.yaml

项目根目录 SHALL NOT 包含旧的 `.stdd/config.yaml`，配置唯一来源为 `config.d/`。

#### Scenario: 仅有 config.d/ 存在

- **GIVEN** 项目使用 V2.0.1+
- **WHEN** 检查 .stdd/ 目录
- **THEN** config.d/ SHALL 存在
- **AND** config.yaml SHALL NOT 存在

### Requirement: 移除 install.py 死代码

`cmd_install` SHALL NOT 包含无效的 `_shared/` 守卫逻辑。

#### Scenario: 核心技能正常安装

- **GIVEN** .stdd/skills/ 包含核心技能文件和 _shared/ 子目录
- **WHEN** 执行 `stdd install claude-code`
- **THEN** _shared/ 中的文件 SHALL NOT 被安装
- **AND** 核心技能文件正常安装
