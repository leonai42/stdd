# Capability: CODE — 代码健壮性修复

## MODIFIED Requirements

### Requirement: install.py --dry-run 支持

`cmd_install` SHALL 检测 `args.dry_run` 标志，预览操作但不修改文件系统。

#### Scenario: install --dry-run 预览但不安装

- **GIVEN** 项目已初始化
- **WHEN** 用户执行 `stdd install --dry-run claude-code`
- **THEN** 系统 SHALL 列出将安装的 Skill 名称和目标路径
- **AND** 文件系统 SHALL NOT 发生变化

### Requirement: yaml.safe_load 返回值 None 防护

所有 `yaml.safe_load()` 调用 SHALL 使用 `or {}` 防护 None 返回值。

#### Scenario: 空 YAML 文件不导致崩溃

- **GIVEN** .stdd.yaml 文件为空或仅含注释
- **WHEN** validate/status/archive/rollback/abort 读取该文件
- **THEN** 系统 SHALL 正常执行而非崩溃

### Requirement: archive --dry-run 输出到 stdout

`cmd_archive` 的 --dry-run 输出 SHALL 使用 `print()` 而非 `logger.info()`，与其他命令一致。

#### Scenario: --dry-run 输出无需 -v 可见

- **GIVEN** 用户不指定 -v
- **WHEN** 执行 `stdd archive --dry-run <name>`
- **THEN** 预览信息 SHALL 在 stdout 可见

### Requirement: fix_windows_encoding 防御性检查

`fix_windows_encoding()` SHALL 在访问 `sys.stdout.buffer` 前检查其存在性。

#### Scenario: 非标准 stdout 不崩溃

- **GIVEN** sys.stdout 被测试框架替换为 StringIO
- **WHEN** 调用 fix_windows_encoding()
- **THEN** 系统 SHALL NOT 抛出 AttributeError

### Requirement: trace.py 移除空操作搜索

`cmd_trace` SHALL NOT 在 `specs/` 目录搜索 test-plan.md（该目录不含 test-plan）。

#### Scenario: 仅搜索 changes/ 目录

- **GIVEN** specs/ 目录存在 spec 文件
- **WHEN** 用户执行 trace <TC-ID>
- **THEN** 系统 SHALL 仅在 changes/ 目录搜索

### Requirement: 清理死代码

`__init__.py` SHALL NOT 包含重复的 `from pathlib import Path`。

#### Scenario: 无重复导入

- **GIVEN** 查看 __init__.py 导入区域
- **WHEN** 检查 import 语句
- **THEN** Path SHALL 仅导入一次（模块级别）

### Requirement: diff.py 异常日志

`cmd_diff` SHALL 在捕获异常时记录 DEBUG 级别日志而非静默丢弃。

#### Scenario: 搜索异常被记录

- **GIVEN** 源码搜索遇到 UnicodeDecodeError
- **WHEN** 读取不可解码的文件
- **THEN** 系统 SHALL 记录 DEBUG 日志并继续

### Requirement: rollback 支持恢复 aborted 变更

`cmd_rollback` SHALL 在 `archive/aborted/` 子目录中搜索可恢复的变更。

#### Scenario: 恢复已放弃的变更

- **GIVEN** archive/aborted/ 下存在已放弃的变更
- **WHEN** 用户执行 `stdd rollback <name>`
- **THEN** 系统 SHALL 找到并恢复该变更

### Requirement: archive 状态更新顺序

`cmd_archive` SHALL 在移动成功后更新状态文件，避免中间故障导致不一致。

#### Scenario: 移动失败不破坏状态

- **GIVEN** 归档过程中 shutil.move 失败
- **WHEN** 检查原始 change 目录
- **THEN** .stdd.yaml SHALL 保持原始状态不变

### Requirement: abort.py EOFError 处理

`cmd_abort` SHALL 在 stdin 关闭时（如 CI 环境）优雅处理而非崩溃。

#### Scenario: 无 stdin 时默认拒绝

- **GIVEN** stdin 不可用（EOFError）
- **WHEN** 用户执行 abort 未指定 --yes
- **THEN** 系统 SHALL 输出提示并退出
