# Capability: TEST — 测试补充

## MODIFIED Requirements

### Requirement: 补充 --dry-run 测试

所有支持 --dry-run 的命令 SHALL 有对应测试验证文件系统未变化。

#### Scenario: abort --dry-run 测试

- **GIVEN** 存在活跃 change
- **WHEN** 执行 abort --dry-run
- **THEN** change 目录 SHALL 仍在 changes/ 下

#### Scenario: new --dry-run 测试

- **GIVEN** 项目已初始化
- **WHEN** 执行 new --dry-run test
- **THEN** changes/ 目录 SHALL NOT 新增子目录

#### Scenario: rollback --dry-run 测试

- **GIVEN** archive/ 下有已归档变更
- **WHEN** 执行 rollback --dry-run
- **THEN** 变更 SHALL 仍在 archive/ 下

#### Scenario: install --dry-run 测试

- **GIVEN** 项目已初始化
- **WHEN** 执行 install --dry-run claude-code
- **THEN** .claude/skills/ SHALL NOT 新增文件

### Requirement: 补充 read_config 类型安全测试

`read_config` 的非 dict YAML 文件处理 SHALL 有测试覆盖。

#### Scenario: config.d/ 包含 YAML 列表文件

- **GIVEN** config.d/ 下存在包含 YAML 列表的文件
- **WHEN** 调用 read_config()
- **THEN** 该文件 SHALL 被跳过且记录警告

### Requirement: 补充 finder 精确匹配测试

`find_change_dir` 的精确匹配路径 SHALL 测试无状态文件的目录返回 None。

#### Scenario: 精确匹配无 .stdd.yaml 的目录

- **GIVEN** changes/ 下存在目录但无 .stdd.yaml
- **WHEN** 传入精确目录名调用 find_change_dir
- **THEN** 返回 SHALL 为 None

### Requirement: 补充异常处理测试

`main()` 的异常处理路径 SHALL 有测试覆盖。

#### Scenario: 命令抛出异常时输出 traceback

- **GIVEN** 某命令执行时抛出 AttributeError
- **WHEN** 通过 main() 调度执行
- **THEN** 系统 SHALL 输出 traceback 并以非零退出码退出

### Requirement: 补充 validate 未覆盖路径

`cmd_validate` 的 6 个未覆盖验证路径 SHALL 有测试。

#### Scenario: GIVEN 数量不足时警告

- **GIVEN** spec 中 GIVEN 语句数 < Scenario 数
- **WHEN** 执行 validate
- **THEN** 系统 SHALL 输出警告

#### Scenario: SHALL 关键字缺失时警告

- **GIVEN** spec 中 THEN 语句无 SHALL 关键字
- **WHEN** 执行 validate
- **THEN** 系统 SHALL 输出警告

#### Scenario: TC 案例数不足时报错

- **GIVEN** test-plan 中 TC 案例数 < Scenario 数
- **WHEN** 执行 validate
- **THEN** 系统 SHALL 以非零退出码退出

### Requirement: 补充 status 输出断言

`cmd_status` 的测试 SHALL 断言输出内容而非仅验证不崩溃。

#### Scenario: status 输出包含阶段信息

- **GIVEN** 存在有效 change
- **WHEN** 执行 status
- **THEN** 输出 SHALL 包含 "当前阶段" 和 "状态"

### Requirement: 补充 WorkBuddy 安装测试

`cmd_install` 的 WorkBuddy 平台 SHALL 有测试覆盖。

#### Scenario: 安装到 WorkBuddy

- **GIVEN** 核心技能文件存在
- **WHEN** 执行 install workbuddy
- **THEN** Skills SHALL 安装到 .workbuddy/skills/
