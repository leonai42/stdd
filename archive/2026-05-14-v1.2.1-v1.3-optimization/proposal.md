# STDD V1.2.1 + V1.3 优化

> 基于 Hermes 评审 + 独立评审两份报告的综合优化变更

## Why

STDD V1.2 经过 Hermes AI Agent 和独立人工评审（详见 `review/` 目录），确认存在以下问题需要修复和优化：

1. **严重 Bug**：`archive` 命令目录名错误，归档时丢失日期前缀
2. **数据兼容性风险**：`.stdd.yaml` 状态文件无版本字段，未来格式变更将破坏已有 change
3. **验证逻辑缺陷**：`validate` 的 GIVEN/WHEN/THEN 计数检查使用错误的 `!=` 操作符；`trace` 搜索范围不完整（仅 changes/ 不搜 specs/）
4. **工程质量不足**：CLI 脚本未遵循自身 Python 规范（零类型注解、无异常处理、print 代替日志）
5. **CLI 功能缺口**：`init` 缺 `--force`、`new` 缺格式验证、`install` 缺源文件检查
6. **版本号矛盾**：README 标注 V1.2，config.yaml 中写 1.0.0
7. **模板质量不均**：spec.md（15行）和 tasks.md（12行）过于简略，缺乏引导性示例

本次变更聚焦 V1.2.1（关键修复）+ V1.3（质量提升），是 STDD 自身工程质量的系统性补强。

## What Changes

### V1.2.1 关键修复（P0）
- 修复 `archive` 命令目录名 Bug（`args.name` → `change_dir.name`）
- 修复 `archive` 操作非原子性问题（先合并 specs 再移动目录）
- `.stdd.yaml` 增加 `version` 字段，当前设为 `"1.2"`
- 修复 `validate` 正则逻辑（GIVEN/WHEN/THEN 统一改为 `<` 检查）
- 修复 `trace` 搜索范围，增加主 `specs/` 目录搜索
- 统一版本号：config.yaml `stdd_version: "1.2.1"`

### V1.3 质量提升（P1）
- CLI 代码规范化：公共函数增加类型注解、关键操作增加异常处理
- `init` 增加 `--force` 选项
- `new` 增加 change_name 格式验证（禁止空格和特殊字符）
- `install` 增加源文件存在性检查
- `status` 增加 long_range 模式显示
- 优化极简模板：spec.md 增加 AND 示例，tasks.md 增加优先级和依赖示例
- README.md 与 STDD.md 职责分离（去重）

## Capabilities

### Modified Capabilities
- `CLI`：bin/stdd 的功能修复和质量提升（Bug修复 + 类型注解 + 异常处理 + 新选项）
- `STATE`：.stdd.yaml 状态文件架构变更（增加 version 字段，向后兼容）
- `TEMPLATE`：spec.md、tasks.md 模板增强（增加内嵌示例）
- `CONFIG`：config.yaml 版本号修正
- `DOCS`：README.md、STDD.md 职责分离

### New Capabilities
- 无新增 capability（本次为修复和优化，不增加功能维度）

## Impact

**代码层面**：
- `bin/stdd`：约 50-80 行变更（Bug修复 + 类型注解 + 异常处理 + 新选项），总规模约 700 行
- `config.yaml`：1 行变更（版本号）
- `.stdd/templates/spec.md`：约 +15 行（AND 多条件示例）
- `.stdd/templates/tasks.md`：约 +10 行（优先级和依赖示例）
- `README.md`：约 -20 行（去重，减少与 STDD.md 的重复）
- `STDD.md`：约 +10 行（补充独立加载时需要的规则说明）

**配置层面**：
- `.stdd.yaml` 新增 `version: "1.2"` 字段，旧文件缺少 version 时 CLI 兼容处理
- config.yaml `stdd_version` 更新为 `"1.2.1"`

**基础设施**：
- 无新依赖，无新服务，纯代码级变更

## Success Criteria

- [ ] `stdd archive my-feature` 归档到 `archive/2026-05-14-my-feature/`（含完整日期前缀）
- [ ] `stdd archive` 操作原子性：specs 合并 + 状态更新完成后再移动目录
- [ ] `.stdd.yaml` 包含 `version: "1.2"` 字段
- [ ] `stdd validate` 对 1 Scenario + 2 GIVEN（AND）不产生误报警告
- [ ] `stdd trace TC-XXX-001` 能同时搜索 `changes/` 和 `specs/` 目录
- [ ] `config.yaml` 中 `stdd_version: "1.2.1"`
- [ ] `stdd init --force` 覆盖已存在的模板文件
- [ ] `stdd new "invalid name with spaces"` 被格式验证拒绝并给出提示
- [ ] `stdd install unsupported-platform` 源文件不存在时给出明确错误
- [ ] `stdd status` 显示当前执行模式（长程/普通）
- [ ] spec.md 模板包含 AND 多条件示例
- [ ] tasks.md 模板包含优先级标注和依赖关系示例
- [ ] README.md 不再重复六阶段完整描述，改为引用 STDD.md
- [ ] 所有现有 CLI 命令行为向后兼容（`--help` 正常、已有 change 不受影响）
