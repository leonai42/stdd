---
name: stdd-spec
description: "STDD Phase 2: 规格设计与测试方案 — 将 proposal 转化为精确的技术规格、行为规格和测试方案（最重要的阶段）"
---
# STDD Phase 2: SPEC — 规格设计与测试方案

## 阶段目标

将 proposal 转化为精确的技术规格和测试方案。**这是整个 STDD 流程中最重要的阶段。**

## 前置条件

- Phase 1 已完成（proposal.md 经用户确认）
- `.stdd.yaml` 中 `phases.understand.status == "completed"`

## 执行流程

### Step 1: 读取 Phase 1 产出

读取 `proposal.md`，理解：
- 变更范围和边界
- 涉及的 Capabilities
- 成功标准

### Step 2: 生成技术设计（design.md）

先读取模板：`.stdd/templates/design.md`

按模板生成 design.md：
- **Context**：当前技术背景和约束
- **Decisions**：每个技术决策包含：
  - 方案描述
  - 为什么选这个方案
  - 备选方案及排除原因
- **Architecture**：数据流/组件图/调用链
- **Risks / Trade-offs**：风险表和缓解措施

### Step 3: 生成行为规格（specs/*.md）

先读取模板：`.stdd/templates/spec.md`

为每个 Capability 生成一个 spec 文件（`specs/<capability>/spec.md`）：

格式规则：
- 每个 Requirement 至少 1 个 Scenario
- 严格使用 GIVEN/WHEN/THEN/AND 格式
- THEN 中必须包含 SHALL（大写），表示强制行为
- Scenario 名称描述场景状态，不是动作
- GIVEN/WHEN/THEN 各一条，AND 可有多条（最多 5 条）

### Step 4: 生成测试方案（test-plan.md）

先读取模板：`.stdd/templates/test-plan.md`

从 specs 映射生成 test-plan.md：

**Spec → Test 映射规则**：
```
spec Scenario            test-plan TC Case
─────────────────────────────────────────
GIVEN: <前置条件>    →   预置条件（Arrange）
WHEN: <触发动作>     →   输入（Act）
THEN: <预期结果>     →   预期结果（Assert）
AND: <附加结果>      →   额外的 Assert
```

**TC-ID 命名规则**：`TC-<CAPABILITY>-<NNN>`
- CAPABILITY 取 capability 名的缩写（如 CASUAL, INTENT, CSM, KM, SOURCE）
- NNN 从 001 递增

**必须包括的章节**：
1. 测试策略（金字塔 + 原则 + 已有资产）
2. 详细测试案例（每个 spec Scenario 至少 1 个 TC）
3. 测试执行矩阵（功能 × 测试层次）
4. 回归风险矩阵（改动区域风险评估）
5. 建议补充顺序（P0 → P1 → P2）

### Step 5: 用户确认（强制门 — STDD 最关键的门）

向用户展示完整的 Phase 2 产出后，**必须等待用户明确确认**：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD Phase 2: SPEC — 等待确认
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 产出物：
  ✅ design.md — 技术设计
  ✅ specs/<capability>/spec.md (N 个文件) — 行为规格
  ✅ test-plan.md — 测试方案

📊 关键指标：
  - Spec Requirements: N
  - Spec Scenarios: N
  - TC Cases: N
  - P0: N / P1: N / P2: N
  - 回归风险: 🔴高:N 🟡中:N 🟢低:N

⚠️ 需要你逐一确认：
  1. 技术方案是否合理？（design.md）
  2. 每个 Scenario 的描述是否准确？（specs/*.md）
  3. 测试覆盖是否充分？（test-plan.md）
  4. TC 案例优先级是否合理？

👉 确认无误请回复，或提出修改意见。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

如果用户提出修改意见 → 根据反馈修订文档 → 重新展示等待确认
如果用户确认 → 锁定所有 Phase 2 文档

**未确认前，绝对不允许进入 Phase 3。**

### Step 6: 写入文件

用户确认后：
1. 写入 `design.md`
2. 写入 `specs/<capability>/spec.md`（每个 capability 一个文件）
3. 写入 `test-plan.md`
4. 更新 `.stdd.yaml`（phase: spec → completed, confirmed_at 时间戳）
5. 提示用户：Phase 2 完成，Phase 3-5 将自动迭代执行

## 产出物

- `design.md` — 技术设计文档
- `specs/<capability>/spec.md` — 行为规格
- `test-plan.md` — 测试方案（含 TC-ID 映射、覆盖矩阵、回归风险）

## 质量检查

完成前确认：
- [ ] design.md 覆盖所有技术决策，包含方案对比和选择理由
- [ ] 每个 spec Requirement 有 ≥1 个 Scenario
- [ ] 每个 Scenario 的 THEN 可客观验证且包含 SHALL
- [ ] test-plan.md 与 specs 的 Scenario 一一对应（无遗漏）
- [ ] TC-ID 全局唯一
- [ ] 回归风险矩阵标注了高/中/低风险区域
- [ ] 用户已明确确认所有 Phase 2 文档

## 下一阶段

Phase 2 确认完成 → 自动进入 Phase 3: SLICE（切片规划）
