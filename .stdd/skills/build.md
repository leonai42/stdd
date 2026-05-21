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

1. **无交互原则**：整个阶段内不使用 AskUserQuestion，不等待用户回复
2. **批量执行**：将同一切片的 RED+GREEN+REFACTOR 合并在一轮内完成
3. **自动降级检测**：每步操作后检查是否触发降级条件（连续3次修复失败/通过率<95%/安全问题）
4. **进度汇报**：每个切片完成后输出简短进度（1行），但不等待回复
5. **阶段衔接**：完成后立即自动调用下一阶段 Skill（stdd-verify）
6. **仅降级时暂停**：仅在触发降级条件时才使用 AskUserQuestion 暂停

## 执行流程

### Step 0: 学习开发规范

在开始编码之前，**必须先读取开发规范**：

1. 读取 `.stdd/config.d/project.yaml` → 获取 `project.language`
2. 读取 `.stdd/standards/<language>.md`（如 `python.md`）
3. 学习：命名规范、类型注解要求、异步规则、错误处理模式、测试规范

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

1. 从 `test-plan.md` 中找到本切片对应的 TC 案例
2. 将 TC 案例转化为 pytest 测试函数
3. 测试命名：`test_<被测方法>_<场景>_<预期结果>`
4. 测试函数注释中标注 TC-ID
5. 运行测试 → **确认失败（RED）**
6. 如果测试直接通过 → 检查是否已有等价测试，有则跳过 RED 阶段
7. **经验检查点**：测试是否反映了 Step 0.5 加载的经验模式？如经验提示"异步函数中裸 except 遗漏 CancelledError"，测试是否覆盖了超时/取消场景？

---

#### Step 1.2: GREEN — 最小实现

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
