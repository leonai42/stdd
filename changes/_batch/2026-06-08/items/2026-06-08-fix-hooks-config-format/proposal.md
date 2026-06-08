# 修复 hooks 配置格式 + 补齐测试/校验

## Why

`/doctor` 发现三个生命周期 hook（SessionStart/PreCompact/Stop）因配置格式错误被 Claude Code 静默忽略，从 2026-06-06 部署以来从未执行过。

**根因**：`stdd hooks install` 将 hook 值写为字符串（`"python .stdd/hooks/xxx.py"`），但 Claude Code 要求 array-of-matchers 格式 `[{hooks: [{type: "command", command: "..."}]}]`。测试只验证 key 存在不验证 value 类型，install 后无自动校验，三道防线全部失守。

**经验依据**：EXP-2026-0008（配置写入-验证缺口）、EXP-2026-0009（关键基础设施静默失败）。

## What Changes

- **C1** (modified)：`stdd/cli/commands/hooks.py` — `cmd_hooks_install` 将 hook 值从字符串改为 array-of-matchers 格式；新增 `_validate_hooks_config()` 在 install 后自动校验配置结构
- **C2** (modified)：`tests/commands/test_hooks.py` — `test_install_creates_scripts_and_config` 增加 value 类型/结构断言
- **C3** (new)：`tests/commands/test_hooks.py` — 新增 `test_install_validates_config_format` 测试校验函数

## Capabilities

### New Capabilities

- **hooks install 自校验**：install 完成后自动验证写入的 hooks 配置格式有效性，错误时打印警告。

### Modified Capabilities

- **hooks install 格式**：输出正确的 array-of-matchers 格式，与 PreToolUse 保持一致。
- **hooks 测试断言**：从 key-existence 升级为 key + type + structure 三级验证。

## Impact

**代码层面**：
- `stdd/cli/commands/hooks.py` ~30 行增改
- `tests/commands/test_hooks.py` ~25 行增改

**配置层面**：
- 无（fix 的是配置生成逻辑本身）

**基础设施**：
- install 后增加自动校验步骤

## Constraints

- 与现有 PreToolUse 格式保持一致
- 不影响 hooks uninstall / status 行为
- 向后兼容：已有正确格式的配置不被覆盖

## Stakeholders

- STDD 用户（依赖 lifecycle hooks 正常工作）

## Risk Areas

- capability: hooks install 格式 — 如果用户手动编辑过 settings.local.json 为其他自定义格式，可能被覆盖。缓解：install 时检测已有配置，若已为数组格式则跳过。

## NonGoals

- 不修复 Claude Code 本身的静默丢弃行为（那是平台侧问题）
- 不改动 hooks uninstall/status 的行为
- 不引入新的外部依赖

## Critical

- [x] 非关键变更（默认）

## Risk Assessment

- **safety_critical**：false
- **financial**：false
- **cross_system**：false

## Anchoring

- **level**：L1（行为锚定）
- **reference_changes**：无
- **anchor_implementations**：无

## Success Criteria

- [ ] `stdd hooks install` 写入的 hook 值类型为 `list`，每个元素含 `hooks` 数组，`hooks[0]` 含 `type` 和 `command` 字段
- [ ] `_validate_hooks_config()` 在格式错误时打印警告信息
- [ ] `test_hooks.py` 断言验证 value 是 `list` + 结构正确
- [ ] 已有测试全部通过，无回归
