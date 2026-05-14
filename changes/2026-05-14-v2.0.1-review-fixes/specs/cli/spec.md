# Capability: CLI — 评审问题修复

## MODIFIED Requirements

### Requirement: 异常处理显示 traceback

`__init__.py` 的 `main()` SHALL 在捕获异常时输出完整 traceback 而非仅一行错误消息。

#### Scenario: 命令执行异常时输出 traceback

- **GIVEN** 某个命令模块存在编程错误（如 AttributeError）
- **WHEN** 用户执行该命令
- **THEN** 系统 SHALL 输出完整 traceback 信息
- **AND** 系统 SHALL 以非零退出码退出

### Requirement: --dry-run 支持所有命令

init、new、rollback、abort 命令 SHALL 支持 --dry-run 选项，预览操作但不修改文件系统。

#### Scenario: init --dry-run 预览

- **GIVEN** 项目未初始化
- **WHEN** 用户执行 `stdd --dry-run init`
- **THEN** 系统 SHALL 列出将创建的文件和目录
- **AND** 文件系统 SHALL NOT 发生变化

#### Scenario: new --dry-run 预览

- **GIVEN** 项目已初始化
- **WHEN** 用户执行 `stdd --dry-run new test-feature`
- **THEN** 系统 SHALL 输出将创建的目录路径
- **AND** 文件系统 SHALL NOT 发生变化

### Requirement: finder 精确匹配检查状态文件

`find_change_dir` 在精确匹配时 SHALL 检查 `.stdd.yaml` 存在性，与模糊匹配行为一致。

#### Scenario: 精确匹配无状态文件的目录

- **GIVEN** changes/ 下存在目录但无 .stdd.yaml
- **WHEN** 用户执行精确名称查询
- **THEN** 系统 SHALL 返回 None（而非返回无状态的目录）

### Requirement: trace/diff 统一案例标题解析

trace 和 diff 命令 SHALL 使用相同的正则表达式解析案例标题（同时支持 em dash 和连字符）。

#### Scenario: 连字符案例标题被正确解析

- **GIVEN** test-plan.md 使用 `-` 作为案例标题分隔符
- **WHEN** 用户执行 trace 或 diff
- **THEN** 系统 SHALL 正确提取案例标题

### Requirement: Markdown 表格提取不含尾随管道

trace 和 diff 命令 SHALL 在提取表格单元格内容时排除尾随 `|` 字符。

#### Scenario: 预期结果不含尾随管道

- **GIVEN** test-plan.md 表格行 `| **预期结果** | 输出正确 |`
- **WHEN** 系统提取预期结果文本
- **THEN** 提取结果 SHALL 为 "输出正确" 而非 "输出正确 |"
