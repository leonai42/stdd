# Phase Context — <change-name>

<!--
  阶段交接摘要 — 每个 phase 结束时由 AI 撰写对应章节。
  新 session Agent 优先读取此文件以快速恢复上下文。
  每章节末尾附"完整上下文文件清单"，需要更多细节时回溯原文。
  
  ⚠️ 此文件由 AI 自动维护，人类不应手动编辑。
  冲突时以各 phase 的正式产出物为准。
-->

---

## Phase 1: UNDERSTAND (completed <timestamp>)

### 关键决策
- **需求边界确定**：<一句话决策>（详见 proposal.md Constraints / NonGoals）
- **优先级判断**：<为什么是 P0 / P1>

### 用户关注点
- 用户特别强调了 <X>（对话中提到 ≥2 次 / Gate 1 反馈中明确要求）

### 被否决的方向
- 方向 A：<一句话描述> — 原因：<用户反馈 / 超出范围>

### 产出物清单
- proposal.md — Gate 1 已确认，confirmed_at: <timestamp>

### 完整上下文文件清单
- proposal.md：需求背景、能力列表、约束条件、成功标准

---

## Phase 2: SPEC (completed <timestamp>)

### 关键技术决策
- 决策 1：<方案> — 理由：<为什么>；排除：<备选方案>

### 经验触发记录
- EXP-XXXX（<pattern>）— 在 <场景> 中被触发，已纳入 spec 的 <Scenario> 测试覆盖

### 已知坑点 / 注意事项
- <坑点>：描述 + 应对策略

### 未解决问题（待 Phase 4 验证）
- <问题>：描述 + 当前假设 + 验证方式

### 产出物清单
- design.md — Gate 2 已确认
- specs/<capability>/spec.md — N 个 Scenario，confirmed
- test-plan.md — M 个 TC-ID，confirmed

### 完整上下文文件清单
- design.md：架构决策（Decisions 章节）、风险与缓解（Risks/Trade-offs）
- specs/<capability>/spec.md：GIVEN/WHEN/THEN 行为规格
- test-plan.md：TC-ID 映射、测试策略、回归风险矩阵

---

## Phase 3: SLICE (completed <timestamp>)

### 切片方案
- Slice 1（P0 · 独立）：<名称> — N 个 TC
- Slice 2（P0 · 依赖 Slice 1）：<名称> — M 个 TC
- parallel_group: <N> → <切片列表> 可并行

### 风险提示
- Slice N 涉及 <核心模块>，风险评分 <高/中/低>

### 产出物清单
- slices.md — N 个切片，依赖关系已标注
- tasks.md — M 个任务

---

## Phase 4: BUILD (completed <timestamp>)

### 实现决策（非设计偏离）
- 决策：使用 <库 X 版本 Y> 而非 <版本 Z> — 因为 <原因>

### 设计偏离汇总
<!-- 详见 design-adjustments.md -->
- 偏离 1：<标题> — 严重程度 Minor/Major

### 经验触发记录
- EXP-XXXX 第 N 次触发 → occurrences 提升至 N

### 切片完成状态
| Slice | TC覆盖 | 新增测试 | 状态 |
|-------|--------|---------|:---:|
| 1 | 4/4 | 4 | ✅ |
| 2 | 3/3 | 2 | ✅ |

### 产出物清单
- <N> 个源文件（新增/修改）
- <M> 个测试文件
- design-adjustments.md

### 完整上下文文件清单
- slices.md：切片计划与完成状态
- design-adjustments.md：设计偏离详细说明
- 关键源文件：<列出路径>

---

## Phase 5: VERIFY (completed <timestamp>)

### 测试结果摘要
- 单元测试：<N>/<M> 通过，覆盖率 <X>%
- 失败模式检查：<X>/12 通过，<Y> 触发

### 设计偏离确认
- 所有偏离已在 design-adjustments.md 中记录

### 产出物清单
- test-report.md
- design-adjustments.md（最终版本）

---

## Current: Phase <N> <状态>

### 当前状态
- <一句话状态描述>

### 下一步
- <下一步动作>
