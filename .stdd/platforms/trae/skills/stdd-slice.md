---
name: stdd-slice
description: STDD Phase 3: 切片规划 — 将测试方案拆分为可独立实现的垂直切片
---
# STDD Phase 3: SLICE — 切片规划

## 阶段目标

将 Phase 2 的测试方案拆分为可独立实现的垂直切片，规划执行顺序。

## 前置条件

- Phase 2 已完成（design.md + specs + test-plan.md 经用户确认）
- `.stdd.yaml` 中 `phases.spec.confirmed_at` 已设置

## 执行模式

**自动执行，无需用户确认。** Phase 2 已锁定设计，此阶段只做机械拆分。

## 执行流程

### Step 1: 读取 Phase 2 产出

1. 读取所有 `specs/<capability>/spec.md`，提取所有 Scenario 列表
2. 读取 `test-plan.md`，提取所有 TC-ID 及其依赖关系

### Step 2: 切片生成

以 TC 案例为最小单元，合并同一实现单元的 TC 为一个切片：

- 一个切片 = 1 个 spec Scenario → 1+ 测试函数 → 1 个实现单元
- 同一模块内紧密相关的 Scenario 可以合并为一个切片
- 标注每个切片的依赖关系

### Step 3: 排序

1. 按依赖关系拓扑排序
2. P0 切片优先
3. 无依赖的切片标记为"可并行"

### Step 4: 生成执行计划

先读取模板：`.stdd/templates/tasks.md` 和 `.stdd/templates/slices.md`

生成两个文件：

**tasks.md** — 实现任务清单（checkbox 格式，按 capability 分组）

**slices.md** — 切片执行计划（仅复杂项目需要，简单项目可跳过）：

| # | 优先级 | TC 覆盖 | 实现目标 | 依赖 |
|---|--------|---------|---------|------|
| 1 | P0 | TC-XXX-001 | `function_a()` | 无 |
| 2 | P0 | TC-YYY-001 | `function_b()` | 1 |

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
