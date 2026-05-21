---
name: stdd-slice
description: "STDD Phase 3: 切片规划 — 将 spec 拆分为可实现的开发切片"
---
---
name: stdd-slice
description: "STDD Phase 3: 切片规划 — 将测试方案拆分为可独立实现的垂直切片"
---
# STDD Phase 3: SLICE — 切片规划

## 阶段目标

将 Phase 2 的测试方案拆分为可独立实现的垂直切片，规划执行顺序。

## 前置条件

- Phase 2 已完成（design.md + specs + test-plan.md 经用户确认）
- `.stdd.yaml` 中 `phases.spec.confirmed_at` 已设置

## 执行模式

**自动执行，无需用户确认。** Phase 2 已锁定设计，此阶段只做机械拆分。

**长程退出检测**：如有用户输入"切换普通模式"或"退出长程"，更新 `.stdd.yaml` 中 `long_range.mode: normal`，当前操作完成后暂停等待用户确认。

## 执行流程

### Step 1: 读取 Phase 2 产出

1. 读取所有 `specs/<capability>/spec.md`，提取所有 Scenario 列表
2. 读取 `test-plan.md`，提取所有 TC-ID 及其依赖关系
3. **执行 CLI 依赖图构建**：`python bin/stdd dependency-graph --format json`
   - 获取 `nodes`, `edges`, `zero_dependency`, `cycles`
   - 如检测到循环依赖（exit code 1），先分析 cycles 输出再手动审查

### Step 2: 五步智能切片分析

基于依赖图数据和经验库，进行以下五步分析：

---

#### Step 2a: 依赖图分析

从 `dependency-graph` JSON 输出中提取：
- **零依赖节点**（可并行开发）：`zero_dependency` 列表
- **依赖链深度**：从零依赖节点到最下游节点的最长路径
- **关键路径**：包含最多下游依赖的节点链 → 优先实现

---

#### Step 2b: 风险评分

对每个 capability 进行风险评分（1-5），基于以下因素：

1. **经验库风险**：执行 `python bin/stdd experience list --format json`，检查是否有与该 capability 相关的失败经验
   - 有 `severity: high` 的匹配经验 → +2 风险分
   - 有 `severity: medium` 的匹配经验 → +1 风险分
2. **复杂度风险**：
   - capability 的 Scenario 数量 > 5 → +1 风险分
   - 涉及多个外部系统或跨模块交互 → +1 风险分
3. **变更类型**：
   - MODIFIED 且涉及接口变更 → +1 风险分

风险分 ≥ 4：高风险 🟡 | 2-3：中风险 🟢 | 1：低风险

---

#### Step 2c: 工作量预估

对每个 capability 估算实现工作量（以 TC 案例数和 Scenario 复杂度为输入）：

| 粒度 | 估算 |
|------|------|
| S（小）| 1-2 个 TC，单一文件修改 |
| M（中）| 3-5 个 TC，2-3 个文件修改 |
| L（大）| 6+ 个 TC 或 >3 个文件修改 |

---

#### Step 2d: 智能分组

将 TC 案例合并为切片，遵循以下规则：

1. 同一 capability 内的紧密相关 Scenario 合并为一个切片
2. 风险高的 capability 独立成切片（便于隔离和重点测试）
3. 工作量大的 capability 拆分为多个切片（每个切片 S-M 粒度）
4. 跨 capability 的 Scenario（如共享 GIVEN）合并为集成切片

---

#### Step 2e: 并行化建议

基于依赖图和无依赖节点分析：

1. 零依赖节点标记为"可并行"（parallel_group = 1, 2, 3...）
2. 同组内切片标记为 `parallel_group: N`（同一并行组可同时开发）
3. 每个并行组约 2-3 个切片（避免过多人同时协作产生冲突）

---

### Step 3: 排序

1. 按依赖关系拓扑排序
2. P0 切片优先
3. 无依赖的切片标记为"可并行"

### Step 4: 生成执行计划

先读取模板：`.stdd/templates/tasks.md` 和 `.stdd/templates/slices.md`

生成两个文件：

**tasks.md** — 实现任务清单（checkbox 格式，按 capability 分组）

**slices.md** — 切片执行计划（含五步分析结果）：

- **Dependency Graph Summary**：ASCII 依赖拓扑图 + 并行化说明
- **Slice Execution Plan 表格**：包含 risk/effort/parallel_group/rationale 列
- **Rationale 章节**：每个切片的依赖关系、风险分析、工作量估算说明

### Step 5: 写入文件并自动进入 Phase 4

1. 写入 `tasks.md`
2. 如需要，写入 `slices.md`
3. 更新 `.stdd.yaml`（phase: slice → completed）
4. 通知用户切片数量和执行顺序
5. **自动进入 Phase 4: BUILD**

## 产出物

- `tasks.md` — 实现任务清单
- `slices.md` — 切片执行计划（可选）

## 质量检查

- [ ] tasks.md 覆盖所有 spec Requirements
- [ ] 切片无循环依赖（A 等 B，B 等 A）
- [ ] P0 切片排在前面
- [ ] 每个切片有明确的实现目标

## 下一阶段

Phase 3 完成 → 自动进入 Phase 4: BUILD（TDD 实现）
