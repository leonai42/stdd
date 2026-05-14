# Hermes 评审结果分析报告

> 分析日期：2026-05-14
> 分析对象：Hermes AI Agent 对 STDD V1.2 的评审报告
> 分析方法：逐条对照源码核实，标注确认/部分确认/存疑

---

## 一、总体评价核实

Hermes 给出了 **⭐⭐⭐⭐ (4/5) — 有条件通过** 的总体评价。经核实，这个评分合理，主要扣分项（3个Bug、状态管理、模板简略）确实存在。

---

## 二、Bug 核实 — 逐条代码对照

### Bug 1: `archive` 命令目录名错误

**Hermes 描述**：archive_dir 使用 args.name 而非 change_dir.name，丢失日期前缀。

**源码核实**（`bin/stdd`）：

```python
# 第 348 行：正确查找到了完整目录名
change_dir = _find_change_dir(args.name)
# 例如 change_dir = Path("changes/2026-05-14-my-feature")

# 第 368 行：但归档时用的是用户输入 ❌
archive_dir = project_root / "archive" / args.name
# args.name = "my-feature"，丢失了 "2026-05-14-" 前缀
```

**_find_change_dir 支持模糊匹配**（第 39-42 行），用户输入 `my-feature` 可以匹配到 `2026-05-14-my-feature`。但归档目录名使用 `args.name` 而非 `change_dir.name`。

**核实结论：✅ 确认，严重 Bug。** 修复很简单：`args.name` → `change_dir.name`。

**影响**：归档后目录变成 `archive/my-feature`，丢失日期前缀，破坏了归档目录的命名一致性，且当同一天存在多个同名 change 时可能混淆。

---

### Bug 2: `validate` 正则逻辑 "不对称"

**Hermes 描述**：

> GIVEN 使用 `!=` 严格等于，THEN 使用 `<` 小于，不对称。

**源码核实**（`bin/stdd` 第 219-223 行）：

```python
# 第 219 行：GIVEN — 使用 !=（警告）
if given_count != len(scenarios):
    warnings.append(...)

# 第 221 行：WHEN — 使用 !=（警告）
if when_count != len(scenarios):
    warnings.append(...)

# 第 223 行：THEN — 使用 <（错误）
if then_count < len(scenarios):
    errors.append(...)
```

**核实结论：⚠️ Hermes 的描述部分有误。**

- GIVEN 和 WHEN **实际上是对称的**（都用 `!=`，都产生 Warning），Hermes 将二者描述为不对称是错误的。
- 真正的差异是：GIVEN/WHEN 用 `!=`（Warning 级别），THEN 用 `<`（Error 级别）。
- THNE 用 `<` 相对更合理（至少一个 THEN 即可，允许多个 AND），但 GIVEN/WHEN 用 `!=` 则过于严格——一个 Scenario 可以有多个 GIVEN/WHEN + AND。

**Hermes 建议的修复**：改为 `<=`。

**建议评估：❌ 错误。** `<=` 会让每个恰好有 1 个 GIVEN/WHEN 的 Scenario 也触发警告（如 生成 2 个 Scenario，2 个 GIVEN → 2 <= 2 为 True → 误报）。

**正确修复**：统一改为 `<`（检查是否少于 Scenario 数，每个 Scenario 至少应有 1 个 GIVEN/WHEN/THEN）。同时建议 GIVEN/WHEN 降级为 Warning，THEN 保持 Error。

---

### Bug 3: `trace` 搜索范围不完整

**Hermes 描述**：只搜索 `changes/` 目录，不搜索主 `specs/`。

**源码核实**（`bin/stdd` 第 429-431 行）：

```python
changes_dir = project_root / "changes"
if changes_dir.exists():
    for change_dir in changes_dir.iterdir():
```

**核实结论：✅ 确认。** `archive` 命令会将 specs 合并到 `specs/` 目录，此时 trace 无法在 `specs/` 中找到已归档 change 的 TC-ID。需同时搜索 `changes/` 和 `specs/`。

---

## 三、改进建议核实

| # | 建议 | 优先级 | 核实结果 |
|---|------|--------|----------|
| 1 | 修复 archive 目录名 Bug | 🔴 高 | **确认**，`args.name` → `change_dir.name` |
| 2 | `.stdd.yaml` 增加 version 字段 | 🔴 高 | **确认**，`cmd_new` 生成的状态文件无版本号 |
| 3 | 增加 `stdd rollback` 命令 | 🔴 高 | **确认**，当前无从 archive 恢复的机制 |
| 4 | 增加 `stdd diff` 命令 | 🔴 高 | **确认**，当前无 spec↔test↔code 差异对比 |
| 5 | 修复 validate 正则逻辑 | 🟡 中 | **部分确认**，问题存在但 Hermes 修复建议有误 |
| 6 | 增加 `init --force` 选项 | 🟡 中 | **确认**，`init` 静默跳过已存在文件 |
| 7 | 增加 `new` 的 change_name 格式验证 | 🟡 中 | **确认**，无格式校验（如不能含空格/特殊字符） |
| 8 | 增加 trace 对主 `specs/` 的搜索 | 🟡 中 | **确认**，与 Bug 3 相同 |
| 9 | 增加 install 源文件存在性检查 | 🟡 中 | **确认**，`source_dir.iterdir()` 源目录不存在时静默 |
| 10 | 增加 `--verbose` 日志选项 | 🟢 低 | **合理建议** |
| 11 | status 显示 long_range 模式 | 🟢 低 | **确认**，当前 status 不显示执行模式 |
| 12 | archive 的 specs 合并冲突检测 | 🟢 低 | **确认**，当前简单追加，可能产生重复内容 |
| 13 | 为 spec.md 模板增加示例 | 🟢 低 | **确认**，spec.md 仅 15 行无示例 |
| 14 | 为 CLI 增加单元测试 | 🟢 低 | **确认**，CLI 零测试覆盖 |

---

## 四、模板评估核实

| 模板 | Hermes 评估 | 实际行数 | 核实 |
|------|------------|----------|------|
| proposal.md | 36行，缺"假设与约束" | 37行 | ✅ 评估准确 |
| design.md | 31行，缺"回滚方案" | 32行 | ✅ 评估准确 |
| spec.md | 14行，极简 | 15行 | ✅ 评估准确（差1行） |
| test-plan.md | 58行，缺"测试数据准备" | 59行 | ✅ 评估准确 |
| tasks.md | 11行，过于简略 | 12行 | ✅ 评估准确（差1行） |
| slices.md | 7行，建议加"预估工时" | 7行 | ✅ 评估准确 |
| design-adjustments.md | 26行，缺"影响评估" | 27行 | ✅ 评估准确（实际包含影响范围） |
| test-report.md | 99行，最详细 | 100行 | ✅ 评估准确 |
| long-range-auth.md | 78行，覆盖全面 | 79行 | ✅ 评估准确 |

---

## 五、Hermes 评审遗漏项

Hermes 评审聚焦于 CLI 和模板，但遗漏了以下重要问题：

1. **CLI 代码未遵循自身 Python 规范**：无类型注解、无日志系统、import 分散
2. **Skill 与 CLI 之间无验证桥接**：Skill 描述"做什么"，但无机制确认 CLI 是否成功执行
3. **README 版本号不一致**：README 说 V1.2，但 `config.yaml` 中 `stdd_version: "1.0.0"`
4. **`archive` 操作非原子性**：先 move 目录，再更新状态，若第二步失败，状态不一致
5. **`_find_change_dir` 排序逻辑**：用 mtime 决定"最近的 change"，行为不够透明
6. **无 dry-run 模式**：所有 CLI 命令直接执行，无预览机制
7. **平台适配不完整**：`init` 只复制 3 个平台，但 `install` 支持 4 个（缺 cursor 的 init）
8. **长程模式配置复杂**：79 行模板 + config.yaml 中 58 行配置，对用户心智负担大

---

## 六、总结

### Hermes 评审质量评估

- **准确率**：14 项建议中，9 项完全确认，1 项修复建议有误（Bug 2），4 项低优先级建议合理
- **覆盖率**：覆盖了 CLI 代码和模板的主要问题，但遗漏了架构层面和代码质量层面的问题
- **评分合理性**：4/5 合理，体现了"设计优秀但实现有瑕疵"的实际情况

### 建议采纳优先级

| 优先级 | 建议项 | 行动 |
|--------|--------|------|
| P0 | Bug 1: archive 目录名 | 立即修复 |
| P0 | `.stdd.yaml` 版本字段 | 立即添加 |
| P1 | Bug 2: validate 正则（修正方案） | 统一改为 `<` |
| P1 | Bug 3: trace 搜索范围 | 增加 specs/ 搜索 |
| P1 | init --force | 增加选项 |
| P1 | new 格式验证 | 增加校验 |
| P2 | rollback / diff 命令 | 规划 V1.3 |
| P2 | 模板优化 | 增加示例章节 |
| P3 | CLI 单元测试 | 长期补充 |
| P3 | verbose 日志 | 可选增强 |
