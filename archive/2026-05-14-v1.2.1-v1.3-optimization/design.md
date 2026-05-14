# STDD V1.2.1 + V1.3 优化 - 技术设计

## Context

STDD V1.2 的 CLI 脚本（`bin/stdd`，635行 Python）是核心的结构化操作入口。经过 Hermes AI Agent 和独立人工评审，发现 3 个 Bug 和若干工程质量问题。

**当前技术栈**：Python 3.10+，依赖 PyYAML，单文件 argparse CLI 架构。

**约束条件**：
- 必须向后兼容（已有 change 目录、.stdd.yaml 格式不能破坏）
- 保持单文件部署的简洁性（不引入新依赖）
- 不改变 CLI 命令签名（`--help` 输出保持一致）

## Decisions

### 1. archive 目录名修复

**方案**：`args.name` → `change_dir.name`

**为什么**：`_find_change_dir` 已返回完整目录名（含日期前缀），直接使用其 `.name` 属性即可。

**备选方案**：在 archive 命令中重复拼接日期前缀 — 排除，因为日期格式可能变化，且 `change_dir.name` 是唯一权威来源。

### 2. archive 操作顺序调整

**方案**：改为 合并specs → 更新状态 → 移动目录 的顺序

**为什么**：当前"先移动后处理"在合并或状态更新失败时导致数据已迁移但状态不一致。新顺序确保任何步骤失败都可安全重试。

**备选方案**：增加 try/except + 回滚逻辑 — 排除，过于复杂，调整顺序即可解决原子性问题。

### 3. .stdd.yaml version 字段

**方案**：在 `cmd_new` 生成的 `.stdd.yaml` 中增加 `version: "1.2"`，CLI 读取时兼容缺失 version 的旧文件（默认视为 "1.0"）。

**为什么**：最小化兼容性破坏。旧 change 不受影响，新 change 自动获得版本标记。

**备选方案**：增加迁移脚本自动升级旧 .stdd.yaml — 暂不实施，version 字段目前仅用于未来兼容性预留，无实际迁移逻辑。

### 4. validate 正则逻辑修复

**方案**：GIVEN/WHEN/THEN 的计数检查统一改为 `given_count < len(scenarios)`（即 `<` 而非 `!=`）。

**为什么**：一个 Scenario 可以有多个 GIVEN/WHEN/THEN（通过 AND 扩展），`!=` 严格相等会产生误报。Hermes 建议的 `<=` 会导致恰好匹配时也报警告（如 2 个 Scenario + 2 个 GIVEN → 2<=2 True → 误报）。`<` 是正确语义："每个 Scenario 至少应有 1 个 GIVEN/WHEN/THEN"。

**备选方案**：完全移除数量检查 — 排除，检查仍有价值，能发现遗漏的 Scenario。

### 5. trace 搜索范围扩展

**方案**：在 `cmd_trace` 中增加对 `specs/` 目录的搜索（与 `changes/` 并行）。

**为什么**：`archive` 命令会将 specs 合并到 `specs/`，已归档 change 的 TC-ID 只能在 `specs/` 中找到。

**备选方案**：trace 时同时读取 archive/ 目录 — 暂不实施，archive 目录包含完整 change 副本但 specs 已合并到 specs/，搜索 specs/ 已足够。

### 6. init --force 选项

**方案**：增加 `--force` / `-f` 标志，当设置时覆盖已存在的目标文件，否则保持当前静默跳过行为。

**为什么**：用户升级 STDD 版本时需要用新模板/配置覆盖旧文件。保持默认静默跳过以确保不会意外覆盖用户修改。

### 7. new 格式验证

**方案**：`change_name` 必须匹配 `^[a-zA-Z0-9][-a-zA-Z0-9_.]*$`（字母数字开头，后续可含连字符/下划线/点），长度 2-50 字符。

**为什么**：change_name 会作为目录名的一部分，需确保文件系统兼容性。禁止空格和特殊字符。

### 8. install 源文件存在性检查

**方案**：在复制操作前检查 `source_dir` 是否存在且非空，不存在时给出明确错误信息和平台名称。

**为什么**：当前 `source_dir.iterdir()` 源不存在时静默无输出，用户无法区分"安装成功但无文件"和"源目录不存在"。

### 9. status 显示执行模式

**方案**：在 `cmd_status` 输出中增加一行显示 `long_range.mode`（全自动长程 / 普通交互 / 未设置）。

**为什么**：用户需要知道当前处于哪种执行模式，特别是在长程模式下需要明确提示自动行为边界。

### 10. 模板增强

**方案**：spec.md 增加 1 个多 AND 的 Scenario 示例（用 HTML 注释标注，不影响模板结构）。tasks.md 增加优先级标注和依赖关系示例。

**为什么**：极简模板缺乏引导性，AI 可能产生不一致的填充结果。内嵌示例（注释形式）在不增加模板结构复杂度的前提下改善引导。

### 11. README / STDD.md 去重

**方案**：README.md 的六阶段描述改为简要表格 + 引用 STDD.md。STDD.md 保留完整的六阶段流程描述（因为它需要作为独立规则文件加载）。

**为什么**：README 是项目入口，保持简洁；STDD.md 是独立可加载的规则文件，需要自包含。

### 12. CLI 类型注解与异常处理

**方案**：为所有公共函数（`cmd_init`, `cmd_new`, `cmd_validate`, `cmd_status`, `cmd_archive`, `cmd_trace`, `cmd_install`, `_find_change_dir`, `main`）增加类型注解。为文件 I/O 操作增加 `try/except` 包装。

**为什么**：STDD 自身的 Python 规范要求公共函数有完整类型注解。异常处理防止 CLI 以 traceback 形式崩溃。

**备选方案**：引入 mypy 强制类型检查 — 暂不实施，先加注解，后续在 quality 配置中启用 mypy。

## Architecture

本次变更不改变整体架构。变更集中在：

```
bin/stdd                    ← 主要变更文件（~70行 diff）
  ├─ _find_change_dir()     ← 不变
  ├─ cmd_init()             ← + --force + 异常处理 + 类型注解
  ├─ cmd_new()              ← + 格式验证 + version字段 + 异常处理 + 类型注解
  ├─ cmd_validate()         ← + 正则修复 + 异常处理 + 类型注解
  ├─ cmd_status()           ← + 模式显示 + 异常处理 + 类型注解
  ├─ cmd_archive()          ← + 目录名修复 + 操作顺序 + 异常处理 + 类型注解
  ├─ cmd_trace()            ← + specs/搜索 + 异常处理 + 类型注解
  ├─ cmd_install()          ← + 源文件检查 + 异常处理 + 类型注解
  └─ main()                 ← + 类型注解

.stdd/
  ├─ config.yaml            ← 版本号修正
  └─ templates/
      ├─ spec.md            ← + AND 示例
      └─ tasks.md           ← + 优先级/依赖示例

README.md                   ← 六阶段去重
STDD.md                     ← 补充规则说明
```

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|----------|
| 类型注解可能遗漏某些路径 | 使用 `Optional`、`Union` 等宽类型，不过度约束 |
| archive 顺序修改引入回归 | 手动测试 archive 完整流程 |
| validate `<` 可能漏检某些格式错误 | `<` 是必要非充分条件，Scenario 格式检查还有其他维度（SHALL 检查、TC-ID 唯一性） |
| --force 可能覆盖用户自定义修改 | 默认行为保持静默跳过，--force 需用户显式指定 |
| 旧 .stdd.yaml 无 version 字段 | CLI 读取时使用 `.get("version", "1.0")` 提供默认值 |
