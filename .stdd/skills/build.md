---
name: stdd-build
description: "STDD Phase 4: TDD 实现 — 按切片执行 RED→GREEN→REFACTOR 循环"
---
# STDD Phase 4: BUILD — TDD 实现

## 阶段目标

按切片逐一执行 RED → GREEN → REFACTOR，完成所有实现代码和测试代码。

## 前置条件

- Phase 3 已完成（tasks.md + slices.md 已生成）
- `.stdd.yaml` 中 `phases.slice.status == "completed"`

## 执行模式

**自动迭代，行为取决于所选模式：**

- **普通模式**：仅在遇到阻塞或重大设计偏离时暂停与用户交互。
- **长程模式**：所有偏离和阻塞自动处理并记录，全程不中断。仅在触发降级条件时暂停。

进入本阶段时，先读取 `.stdd.yaml` 中的 `long_range.mode` 确定当前模式。

**长程退出检测**：在每个切片开始前，检查用户最新消息是否包含"切换普通模式"或"退出长程"。如检测到，更新 `.stdd.yaml` 中 `long_range.mode: normal`，当前切片完成后暂停等待用户确认，后续切片按普通模式交互。

## 长程模式运行协议（仅在 `long_range.mode == "full_auto"` 时适用）

### ⚠️ 长程模式强制约束 / MANDATORY LONG-RANGE CONSTRAINTS

> 长程模式 ≠ 可以跳过流程步骤。
> Long-range mode skips authorization interactions, NOT process steps.

以下规则不可违反。违反任一条 = 流程失败 / The following rules CANNOT be violated:

| # | 中文 | English |
|---|------|---------|
| 1 | **每个 Step 必须执行** — 长程模式跳过的是授权交互（AskUserQuestion），不是流程步骤 | **EVERY Step MUST be executed** — long-range skips authorization (AskUserQuestion), NOT process steps |
| 2 | **Step 1.4 切片验证不可跳过** — 每个切片必须通过 TC 覆盖 + 产出物核对 + 测试通过三项检查 | **Step 1.4 slice verification CANNOT be skipped** — every slice MUST pass TC coverage + deliverable check + test pass |
| 3 | **每个切片必须有新增测试** — 如果 test-plan 中本切片有 TC，新增测试数必须 > 0 | **EVERY slice MUST have new tests** — if test-plan has TCs for this slice, new test count MUST be > 0 |
| 4 | **进度标记必须有证据** — .stdd.yaml 的 slice done 必须关联 tc_coverage / new_tests / verified_at | **Progress markers MUST be evidence-backed** — slice done requires tc_coverage / new_tests / verified_at |
| 5 | **降级触发覆盖静默失败** — 切片 TC 覆盖率为 0 → WARNING；连续 3 个切片无新增测试 → DEGRADE | **Degradation covers silent failures** — 0 TC coverage → WARNING; 3 consecutive slices with 0 new tests → DEGRADE |
| 6 | **禁止占位符标记完成** — 产出物为 [TODO] 或骨架占位符的切片不能标记为 done | **NEVER mark placeholders as done** — slices with [TODO] output CANNOT be marked complete |

### 运行协议

1. **无交互原则**：整个阶段内不使用 AskUserQuestion，不等待用户回复。**但所有 Step 必须执行**
2. **批量执行**：将同一切片的 RED+GREEN+REFACTOR 合并在一轮内完成
3. **自动降级检测**：每步操作后检查是否触发降级条件：
   - 连续 3 次修复失败
   - 通过率 < 95%
   - 安全问题
   - **切片 TC 覆盖率为 0%（新增·V2.7 复盘）**
   - **连续 3 个切片新增测试数为 0（新增·V2.7 复盘）**
   - **产出物为 [TODO] 占位符（新增·V2.7 复盘）**
4. **切片验证**：每个切片完成后必须执行 Step 1.4 切片验证，通过后才能进入下一切片
5. **进度汇报**：每个切片完成后输出验证结果（TC 覆盖率 + 测试数），但不等待回复
6. **阶段衔接**：所有切片完成 + 验证通过后，自动调用 Phase 5（stdd-verify）
7. **仅降级时暂停**：仅在触发降级条件时才使用 AskUserQuestion 暂停

## 执行流程

### Step -1: 上下文预算检查（V2.7 context-budget-check）

在开始本阶段之前，检查当前会话的上下文状态。**本步骤不可跳过。**

1. **估算上下文长度**：
   - 回顾对话轮次：当前会话大致经历了多少轮用户-Agent 交互？
   - 如果 > 50 轮 → 上下文可能已接近模型有效窗口的 60-70%
   - 如果用户反馈"变慢了" → 上下文几乎确定已膨胀

2. **判断是否需要重置**：
   - 满足以下任一条件时，建议重置：
     a. 对话轮次 > 80 轮
     b. 用户明确说"好慢"或"怎么这么慢"
     c. 上一阶段已完成，且 phase-context.md 已更新
   - 长程模式下，建议每个 phase 完成后主动重置 session

3. **如果建议重置**：
   - 确认当前 phase-context.md 已更新到最新状态
   - 确认 .stdd.yaml 的 state_freshness 已更新
   - 向用户输出重置建议和 `stdd state --resume` 结果

4. **如果选择继续**（或不满足重置条件）：
   - 正常进入 Step 0

> 上下文预算检查是**软建议**，不阻断流程。仅做提示。

---

### Step 0: 学习开发规范与项目规则

在开始编码之前，**必须先读取开发规范**：

1. 读取 `.stdd/config.d/project.yaml` → 获取 `project.language`
2. 读取 `.stdd/standards/<language>.md`（如 `python.md`）
3. 学习：命名规范、类型注解要求、异步规则、错误处理模式、测试规范
4. **V2.9: 加载 `.stdd/rules/`**：读取 `.stdd/rules/common/*.md` 和 `.stdd/rules/<language>/*.md`，将 TDD、安全、Git 工作流等规则注入编码上下文
5. **V2.9: 执行代码结构摘要**：`python bin/stdd structure delta <change>` — 记录本 change 的代码结构变化，为长期自积累代码知识打基础

### Step 0.5: 加载匹配经验

在开始编写代码之前，从项目经验库加载与当前变更相关的经验，预防已知失败模式：

1. 执行 `python bin/stdd experience list --language <project.language> --format json`
2. 从输出中筛选 `lifecycle_state` 为 `verified` 或 `settled` 的经验（已充分验证的经验更可靠）
3. **project_type 过滤（V2.5）**：按当前 change 的 `project_type` 过滤经验：
   - 匹配同类型或 `project_type: null`（通配，V2.4 兼容）的经验 → 加载
   - `project_type` 不匹配的经验 → 跳过
   - 输出摘要：`已加载 <N> 条匹配经验（<project_type>），过滤 <M> 条不匹配`
4. 根据当前 change 的 capabilities 和 spec，选出模式文本（pattern/root_cause/detection_trigger）与当前工作最相关的经验（默认加载最多 10 条，可从 `.stdd/config.d/experience.yaml` 的 `auto_load.max_experiences` 读取）
5. 将匹配的经验内容（pattern + root_cause + fix_template）主动注入编码上下文
6. 编码时对照经验库检查：
   - 模式匹配 → 参考 fix_template 预防已知错误
   - 不匹配 → 正常编码
7. 经验库加载结果输出一行摘要：`经验库加载: <N> 条匹配经验已注入上下文`

### Step 1: 按切片顺序执行

对 `slices.md` 中的每个切片（或 `tasks.md` 中的每个任务）：

---

#### Step 1.1: RED — 编写测试

**V2.9 模式缩放**：先检查 `.stdd.yaml` 中的 `mode` 字段。

*lightweight 模式*：
1. 从 spec 中找到 bug 复现点或优化验证点
2. 写 **1-2 个聚焦测试**（不生成完整 TC 文件）
3. 测试直接针对 bug 条件或优化预期行为
4. 运行测试 → **确认失败（RED）**
5. **TDD 底线**：轻量模式也必须 RED→GREEN，差异在测试数量而非有无

*standard/thorough 模式*：
1. 从 `test-plan.md` 中找到本切片对应的 TC 案例
2. 将 TC 案例转化为 pytest 测试函数
3. 测试命名：`test_<被测方法>_<场景>_<预期结果>`
4. 测试函数注释中标注 TC-ID
5. 运行测试 → **确认失败（RED）**
6. 如果测试直接通过 → 检查是否已有等价测试，有则跳过 RED 阶段
7. **经验检查点**：测试是否反映了 Step 0.5 加载的经验模式？

---

#### Step 1.2: GREEN — 最小实现

*lightweight 模式*：最小实现代码，仅满足聚焦测试。
*standard/thorough 模式*：
1. 写刚好够通过测试的代码
2. **不写超过测试覆盖范围的代码**（不做"顺便"的事）
3. 遵循开发规范（命名、类型注解、异步、错误处理）
4. 运行测试 → **确认通过（GREEN）**
5. 同时运行已有测试 → 确认无回归

---

#### Step 1.3: REFACTOR — 重构

1. 消除重复代码
2. 改善命名（确保名称匹配实际行为）
3. 提取公共逻辑
4. 应用 deep modules 原则（小接口隐藏大复杂度）
5. 应用 deletion test（如果移除这个模块，复杂度是否集中在调用方？如果不是，这个模块不值得存在）
6. 运行测试 → **保持 GREEN**

---

#### Step 1.4: 切片验证（V2.7 复盘新增 — 每切片强制）

**本步骤不可跳过。长程模式下也必须执行。**

在进入下一个切片之前，必须逐项验证本切片的完成情况：

1. **TC 覆盖检查**：
   - 读取 `test-plan.md`，获取本切片对应的所有 TC-ID
   - 搜索 `tests/` 目录，确认每个 TC-ID 是否在测试函数注释中出现
   - 本切片 TC 覆盖率 = 有测试的 TC 数 / 本切片 TC 总数
   - **如果本切片 TC 覆盖率 < 100%** → 切片未完成 → 回到 Step 1.1

2. **产出物核对**：
   - 对照 `slices.md` 中本切片的"实现目标"列
   - 逐项检查：目标中的每个文件/模块是否真实存在？
   - **如果有目标未实现** → 切片未完成 → 回到 Step 1.1

3. **测试运行**：
   - 运行本切片相关的测试：`pytest tests/ -k "<slice_test_pattern>" -v`
   - **本切片新增测试必须全部通过**
   - **本切片新增测试数必须 > 0**（如果 test-plan 中本切片有 TC）
   - 如果新增测试 = 0 且 test-plan 中有 TC → 切片未完成 → 回到 Step 1.1
   - 同时运行全量回归 → 确认无回归

4. **更新状态**（仅在全部通过后）：
   ```yaml
   # .stdd.yaml
   phase4:
     slices_completed:
       "<N>":
         status: "done"
         tc_coverage: "<M>/<K>"
         new_tests: <M>
         verified_at: "<timestamp>"
   ```

5. **不通过处理**：
   - 修复问题 → 重新验证 → 最多 3 次
   - 3 次仍不通过 → 降级为普通模式，暂停等待用户确认

#### Step 1.5: 并行切片合并验证（V2.8 C1 — 条件触发）

**执行条件**：slices.md 中存在 parallel_group 标记，且本组所有切片已完成 Step 1.4 验证。

1. **冲突检查**：`git diff --check` 检查合并冲突
2. **交叉测试**：运行全量测试确保并行切片间无意外交互
3. **接口一致性**：如果两个并行切片修改了同一模块的接口，验证签名兼容
4. **产出物合并**：如果并行切片各自生成了 delta，合并到同一个 phase-context 条目

> 非并行模式（单切片顺序执行）跳过此步骤。

#### Step 1.6: 更新 phase-context.md（V2.8 C3）

每个切片完成（含 Step 1.4 验证通过）后：

1. 在 phase-context.md 的 Phase 4 章节追加当前切片的简要记录：
   - 切片编号 + 名称
   - TC 覆盖情况（X/Y 通过）
   - 新产生的文件列表
2. 如果触发了经验库条目（Step 0.5），注明 EXP-ID
3. 所有切片完成后，更新 phase-context.md 的 Phase 4 状态为 completed

> 此步骤确保后续 session 恢复时，Agent 可精确知道每个切片的完成状态。

---

### Step 2: 处理设计偏离

如果在实现过程中发现 spec/design 需要调整：

**小的偏离**（不改变接口和行为语义）：
- 记录到 `pending-adjustments.md`
- 检查偏离是否命中经验库中的已知模式 → 如命中，记录到 pending-adjustments 并引用 EXP-ID
- 继续执行（两种模式行为一致）

**大的偏离**（改变接口或行为语义）：

*普通模式*：
- 记录到 `pending-adjustments.md`
- **暂停自动迭代，向用户报告**：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD Phase 4: BUILD — 设计偏离
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 实现过程中发现需要调整设计：

  原始设计：<引用 design.md 或 spec.md 的原文>
  实际需要：<描述需要的调整>
  原因：<为什么需要调整>

  这个调整影响较大，需要你确认。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

*长程模式*：
- 自动记录到 `pending-adjustments.md`，包含：原始设计引用、实际调整内容、调整原因、影响范围
- 继续执行，不暂停（按预授权 A1 策略）
- 调整将在 Phase 5 的 `design-adjustments.md` 中汇总

**技术阻塞**：

*普通模式*：
- 暂停，向用户报告阻塞情况，询问处理方案

*长程模式*：
- 按预授权 A2 策略处理：
  - `workaround`：尝试绕过方案，记录到 `pending-adjustments.md`
  - `skip_slice`：标记当前切片为待处理，跳过继续后续切片
  - 若无法绕过且无法跳过 → 降级为暂停等待（触发降级条件）

### Step 3: 切片完成

每个切片完成后：
- 标记 tasks.md 中对应任务为 `[x]`
- 进入下一个切片
- **所有切片完成后**：
  - 长程模式（`long_range.mode == "full_auto"`）：**立即在同一轮次内自动调用 `stdd-verify` skill，不等待用户输入**
  - 普通模式：提示用户可进入 Phase 5: VERIFY

## 产出物

- 实现的源代码文件（新增/修改）
- 新增/修改的测试文件
- `pending-adjustments.md`（如有设计偏离）

## 质量检查

每个切片完成后确认：
- [ ] RED：测试先失败
- [ ] GREEN：最小实现通过测试
- [ ] REFACTOR：重构后测试保持绿色
- [ ] 已有测试无回归

## 用户交互规则

| 场景 | 普通模式 | 长程模式 |
|------|---------|---------|
| 切片正常执行 | 自动完成，不中断 | 自动完成，不中断 |
| 切片之间切换 | 自动进入下一个切片 | 自动进入下一个切片 |
| 小设计偏离 | 记录 pending-adjustments，继续 | 记录 pending-adjustments，继续 |
| 大设计偏离 | 暂停，报告用户 | 自动记录并继续（test-report 汇总） |
| 技术阻塞 | 暂停，询问用户 | 尝试绕过/跳过；无法处理时降级暂停 |
| 所有切片完成 | 自动进入 Phase 5 | 自动进入 Phase 5 |

## 并行执行策略（V2.5 parallel-slice-guide）

当 `slices.md` 中存在标记为 `parallel_group: N` 的切片时，可采用并行执行策略：

### 条件检测

1. 读取 `slices.md`，检查是否有切片标记了 `parallel_group`
2. 检查当前执行环境是否支持子任务派发（delegation / sub-agent）
3. **有 delegation 能力** → 并行派发
4. **无 delegation 能力** → 串行 fallback（按拓扑顺序逐个执行）

### 并行派发流程

1. 同 `parallel_group` 的切片可同时派发给多个子 agent
2. 每个子 agent 独立执行 RED → GREEN → REFACTOR 循环
3. 父 agent 等待所有子 agent 完成后收集结果
4. 验证：合并所有切片的变更，运行全量回归测试

### 串行 Fallback

若无 delegation 能力或并行派发失败：
- 按 `slices.md` 的依赖拓扑顺序串行执行
- 无依赖的切片优先
- P0 优先于 P1

### 结果合并

并行执行完成后：
1. 检查各切片是否有代码冲突（同一文件被多个切片修改）
2. 冲突文件 → 合并变更（优先顺序：Slice A → B → C → D）
3. 运行全量 pytest 确认无回归
4. 输出合并摘要：`并行执行完成: <N> 个切片，<M> 个冲突已合并`

## 下一阶段

Phase 4 完成 → 自动进入 Phase 5: VERIFY（质量验证）
