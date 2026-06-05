# Capability: CLI — STD 命令行工具

## MODIFIED Requirements

### Requirement: archive 命令使用正确的归档目录名

系统 SHALL 使用 change 目录的完整名称（含日期前缀）作为归档目录名，而非用户输入的短名称。

#### Scenario: 用户使用短名称归档 change

- **GIVEN** change 目录 `changes/2026-05-14-my-feature/` 存在，含有效 .stdd.yaml
- **WHEN** 用户执行 `stdd archive my-feature`
- **THEN** 系统 SHALL 归档到 `archive/2026-05-14-my-feature/`
- **AND** 系统 SHALL NOT 归档到 `archive/my-feature/`

#### Scenario: 用户使用完整目录名归档 change

- **GIVEN** change 目录 `changes/2026-05-14-my-feature/` 存在
- **WHEN** 用户执行 `stdd archive 2026-05-14-my-feature`
- **THEN** 系统 SHALL 归档到 `archive/2026-05-14-my-feature/`

### Requirement: archive 操作具有原子性安全顺序

archive 操作 SHALL 按"合并 specs → 更新状态 → 移动目录"的顺序执行，确保任何步骤失败时原有数据不受影响。

#### Scenario: specs 合并成功后移动目录

- **GIVEN** change 目录存在且 VERIFY 已完成
- **WHEN** 用户执行 `stdd archive my-feature --yes`
- **THEN** 系统 SHALL 先合并 specs 到 `specs/` 目录
- **AND** 系统 SHALL 更新 .stdd.yaml 状态为 archived
- **AND** 系统 SHALL 最后移动 change 目录到 archive/

#### Scenario: specs 合并失败时保护源目录

- **GIVEN** change 目录存在，但 specs/ 目录无写权限
- **WHEN** 用户执行 `stdd archive my-feature --yes`
- **THEN** 系统 SHALL 报告合并失败错误
- **AND** change 目录 SHALL 保持原位置不变
- **AND** 系统 SHALL 以非零退出码退出

### Requirement: validate 命令正确检查 GIVEN/WHEN/THEN 数量

系统 SHALL 使用 `count < len(scenarios)` 检查每个 Scenario 至少有一个对应标记，而非要求精确相等。

#### Scenario: 一个 Scenario 有多个 GIVEN（AND 连接）

- **GIVEN** spec 文件包含 1 个 Scenario，该 Scenario 有 2 个 GIVEN（通过 AND 连接）
- **WHEN** 用户执行 `stdd validate`
- **THEN** 系统 SHALL NOT 报告 GIVEN 数量不匹配的警告
- **AND** 系统 SHALL 报告验证通过（如无其他问题）

#### Scenario: Scenario 缺少 GIVEN

- **GIVEN** spec 文件包含 1 个 Scenario 但没有 GIVEN 标记
- **WHEN** 用户执行 `stdd validate`
- **THEN** 系统 SHALL 报告 GIVEN 数量少于 Scenario 数量的警告

### Requirement: trace 命令搜索 specs/ 目录

trace 命令 SHALL 同时搜索 `changes/` 和 `specs/` 目录下的 test-plan.md 文件。

#### Scenario: TC-ID 存在于主 specs/ 目录

- **GIVEN** 某 TC-ID 对应的 change 已归档，specs 合并到 `specs/` 目录
- **AND** `changes/` 目录中不存在该 TC-ID
- **WHEN** 用户执行 `stdd trace TC-XXX-001`
- **THEN** 系统 SHALL 在 `specs/` 目录的 test-plan.md 中找到该 TC-ID
- **AND** 系统 SHALL 显示对应的追溯信息

### Requirement: init 命令支持 --force 选项

init 命令 SHALL 接受 `--force` / `-f` 选项，设置时覆盖已存在的目标文件。

#### Scenario: 使用 --force 覆盖已存在文件

- **GIVEN** 项目已初始化过 STDD，模板文件已存在
- **WHEN** 用户执行 `stdd init --force`
- **THEN** 系统 SHALL 覆盖所有已存在的模板和配置文件
- **AND** 系统 SHALL 提示文件已被更新

#### Scenario: 默认行为保持静默跳过

- **GIVEN** 项目已初始化过 STDD，模板文件已存在
- **WHEN** 用户执行 `stdd init`（不带 --force）
- **THEN** 系统 SHALL 跳过已存在的文件不覆盖
- **AND** 系统 SHALL 输出 init 完成消息

### Requirement: new 命令验证 change_name 格式

new 命令 SHALL 验证 change_name 符合 `^[a-zA-Z0-9][-a-zA-Z0-9_.]{1,49}$` 格式（字母数字开头，长度 2-50）。

#### Scenario: 合法的 change_name

- **GIVEN** 用户输入 change_name `fix-login-bug`
- **WHEN** 系统验证格式
- **THEN** 系统 SHALL 接受该名称，正常创建 change 目录

#### Scenario: 包含空格的 change_name

- **GIVEN** 用户输入 change_name `fix login bug`
- **WHEN** 系统验证格式
- **THEN** 系统 SHALL 拒绝该名称，报告格式错误
- **AND** 系统 SHALL 以非零退出码退出

#### Scenario: 包含特殊字符的 change_name

- **GIVEN** 用户输入 change_name `feature/rate-limit`
- **WHEN** 系统验证格式
- **THEN** 系统 SHALL 拒绝该名称，报告格式错误

### Requirement: install 命令检查源文件存在性

install 命令 SHALL 在复制操作前验证源目录或源文件存在。

#### Scenario: 平台源文件不存在

- **GIVEN** 目标平台（如 workbuddy）的 skills 源目录不存在
- **WHEN** 用户执行 `stdd install workbuddy`
- **THEN** 系统 SHALL 报告"源文件不存在"错误
- **AND** 系统 SHALL 以非零退出码退出

#### Scenario: 平台源文件存在

- **GIVEN** 目标平台的 skills 源目录存在且包含 .md 文件
- **WHEN** 用户执行 `stdd install claude-code`
- **THEN** 系统 SHALL 正常复制 skills 文件
- **AND** 系统 SHALL 报告安装成功的文件数量

### Requirement: status 命令显示执行模式

status 命令 SHALL 显示当前 change 的长程/普通模式状态。

#### Scenario: 长程模式状态显示

- **GIVEN** .stdd.yaml 中 `long_range.mode` 为 `full_auto`
- **WHEN** 用户执行 `stdd status`
- **THEN** 系统 SHALL 显示"🚀 全自动长程模式"

#### Scenario: 未设置模式时显示默认

- **GIVEN** .stdd.yaml 中不存在 `long_range` 字段
- **WHEN** 用户执行 `stdd status`
- **THEN** 系统 SHALL 显示"📋 普通交互模式（默认）"


<!-- 合并自 2026-05-14-v2.0-architecture-upgrade -->
# Capability: CLI — 命令行工具架构升级

## MODIFIED Requirements

### Requirement: CLI 模块化拆分

系统 SHALL 将 `bin/stdd` 拆分为入口文件 + `stdd/cli/` 包结构，每个子命令独立模块。

#### Scenario: bin/stdd 入口保持兼容

- **GIVEN** 用户或脚本调用 `python bin/stdd <command>`
- **WHEN** 执行任意命令
- **THEN** 系统 SHALL 行为与拆分前完全一致
- **AND** `bin/stdd --help` SHALL 输出相同的帮助信息

#### Scenario: 子命令模块可独立导入测试

- **GIVEN** 开发者在 Python 中 `from stdd.cli.commands.init import cmd_init`
- **WHEN** 调用 `cmd_init(args)`
- **THEN** 系统 SHALL 正常执行 init 逻辑
- **AND** 函数签名 SHALL 包含完整类型注解

### Requirement: --dry-run 全局选项

系统 SHALL 接受 `--dry-run` 全局选项，预览操作但不修改文件系统。

#### Scenario: dry-run 模式预览 archive 操作

- **GIVEN** change 目录存在且已完成
- **WHEN** 用户执行 `stdd --dry-run archive my-change --yes`
- **THEN** 系统 SHALL 输出将执行的步骤（合并 specs、移动目录）
- **AND** 文件系统 SHALL NOT 发生变化

#### Scenario: dry-run 模式预览 init 操作

- **GIVEN** 项目未初始化 STDD
- **WHEN** 用户执行 `stdd --dry-run init`
- **THEN** 系统 SHALL 列出将创建的文件和目录
- **AND** 文件系统 SHALL NOT 发生变化

### Requirement: --verbose 分级日志

系统 SHALL 使用 Python logging 模块替代 print()，支持 `-v` (INFO) 和 `-vv` (DEBUG) 选项。

#### Scenario: 默认输出简洁

- **GIVEN** 用户执行 `stdd status`
- **WHEN** 不带 -v 选项
- **THEN** 系统 SHALL 仅输出最终结果（当前行为）

#### Scenario: -v 输出详细信息

- **GIVEN** 用户执行 `stdd -v validate`
- **WHEN** 带 -v 选项
- **THEN** 系统 SHALL 输出检查步骤的详细日志（如"检查必需文件..."）

### Requirement: rollback 命令

系统 SHALL 提供 `stdd rollback <name>` 命令，从 archive 恢复已归档的 change。

#### Scenario: 成功恢复已归档的 change

- **GIVEN** archive/2026-05-14-my-feature/ 存在
- **AND** changes/ 下无同名目录
- **WHEN** 用户执行 `stdd rollback my-feature`
- **THEN** 系统 SHALL 将目录移回 changes/2026-05-14-my-feature/
- **AND** 系统 SHALL 更新 .stdd.yaml 状态为 active

#### Scenario: 目标已存在时拒绝恢复

- **GIVEN** archive/2026-05-14-my-feature/ 存在
- **AND** changes/2026-05-14-my-feature/ 已存在
- **WHEN** 用户执行 `stdd rollback my-feature`
- **THEN** 系统 SHALL 报告冲突错误
- **AND** 系统 SHALL 以非零退出码退出

### Requirement: diff 命令

系统 SHALL 提供 `stdd diff <name>` 命令，显示 spec Scenario ↔ TC 案例 ↔ 测试函数 ↔ 源码的覆盖对比。

#### Scenario: diff 显示覆盖差异表

- **GIVEN** change 目录包含 test-plan.md 且源码中存在 TC-ID 引用
- **WHEN** 用户执行 `stdd diff my-change`
- **THEN** 系统 SHALL 输出四列对照表（Scenario | TC-ID | 测试函数 | 源码）
- **AND** 未覆盖项 SHALL 标注为 ❌

#### Scenario: diff 处理无 test-plan 的 change

- **GIVEN** change 目录不包含 test-plan.md
- **WHEN** 用户执行 `stdd diff my-change`
- **THEN** 系统 SHALL 报告"无 test-plan.md"
- **AND** 系统 SHALL 以非零退出码退出
---
## V2.9 变更: 2026-06-05-stdd-v2.9-core
- 详见 archive/2026-06-05-stdd-v2.9-core/
