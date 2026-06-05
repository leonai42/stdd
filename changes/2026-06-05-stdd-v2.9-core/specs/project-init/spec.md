# project-init — init.py 共享常量提取

<!-- confidence: high -->
<!-- evidence: proposal.md "重构 init.py 提取共享常量" + init.py 代码分析 -->

## Requirement: 模块级常量导出

INIT-REQ-001: init.py SHALL 将 DIRS、FILES_TO_COPY、PLATFORMS 提取为模块级常量，供 upgrade.py 等模块导入复用。

### Scenario: upgrade.py 导入 FILES_TO_COPY

<!-- confidence: high -->
GIVEN init.py 定义了 `FILES_TO_COPY` 模块级常量
WHEN `from stdd.cli.commands.init import FILES_TO_COPY` 被导入
THEN SHALL 返回与 init.py 中 `cmd_init` 使用的相同文件列表

### Scenario: upgrade.py 导入 DIRS

<!-- confidence: high -->
GIVEN init.py 定义了 `DIRS` 模块级常量
WHEN upgrade.py 使用 DIRS 确保目标目录存在
THEN SHALL 包含 `.stdd/skills`, `.stdd/templates`, `.stdd/standards`, `.stdd/config.d` 等目录

### Scenario: upgrade.py 导入 PLATFORMS

<!-- confidence: high -->
GIVEN init.py 定义了 `PLATFORMS` 模块级常量
WHEN upgrade.py 重新安装平台 skills
THEN SHALL 遍历 `["claude-code", "workbuddy", "trae"]`

### Scenario: cmd_init 行为不变

<!-- confidence: high -->
GIVEN init.py 的 DIRS 和 FILES_TO_COPY 已提取为模块级常量
AND `cmd_init` 内部使用这些常量
WHEN 用户执行 `stdd init`
THEN SHALL 与提取前行为完全一致（无退化）

## Requirement: 升级专用常量

INIT-REQ-002: init.py SHALL 定义 CONFIG_MERGE_FILES 和 CONFIG_ALL_FILES 常量，用于 upgrade 时区分合并和覆盖策略。

### Scenario: CONFIG_MERGE_FILES 包含 project.yaml

<!-- confidence: high -->
GIVEN init.py 定义了 `CONFIG_MERGE_FILES`
WHEN upgrade.py 读取该常量
THEN SHALL 包含 `".stdd/config.d/project.yaml"`

### Scenario: CONFIG_ALL_FILES 包含所有 config.d 文件

<!-- confidence: high -->
GIVEN init.py 定义了 `CONFIG_ALL_FILES`
WHEN upgrade.py 读取该常量
THEN SHALL 包含 project.yaml, gates.yaml, long_range.yaml, quality.yaml
