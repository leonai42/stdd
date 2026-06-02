# STDD V2.7 — 技术设计

> 对应 proposal：changes/2026-06-01-stdd-v2.7-context-engineering/proposal.md
> 覆盖板块：E（结构化基础）+ A（锚定落地+双轨验证）+ B（上下文工程）+ C（ECC 借鉴）+ D（CodeGraph 借鉴）
> 板块 B/C/D 设计已完成（2026-06-02），板块 E/A 设计本章补充（2026-06-03）

---

## Context

### 当前 V2.5 的跨 Session 恢复机制

```yaml
# .stdd.yaml（V2.5）
resume_context: "正在执行 STDD V2.5 的 BUILD 阶段，当前在第 3 个 slice（共 4 个）"
active_slice: 3
last_action: "完成了 ci-check-enhanced 的 TDD RED 步骤"
last_modified: "2026-05-21T15:30:00"
```

`stdd state --resume` 输出一段自然语言提示，Agent 据此恢复。这是 V2.5 的"一句话恢复"方案。

### 暴露的问题

从 OpenCode 用户反馈和「AI编码框架上下文管理策略对比」分析中识别出三个层次的问题：

| 层次 | 问题 | 现象 |
|------|------|------|
| **位置层** | resume_context 说清了"在哪"，但 Agent 不知道"发生了什么" | 新 session 仍需翻读 3-5 个文件来理解背景 |
| **决策层** | 阶段中做的关键决策（尤其是被否决的方案）没有汇总 | Agent 可能重蹈已排除的技术路径 |
| **预警层** | 上一阶段发现的坑、触发的经验、未解决的问题无法传递 | 同样的坑在不同阶段的 Agent 之间反复触发 |

### 行业对照

「AI编码框架上下文管理策略对比」一文提出的有效策略：

```
分阶段执行（最有效） + 文件系统作为状态载体 + 决策日志
```

STDD 的 Gate 体系天然适合分阶段。缺失的是**决策日志**和**阶段交接单**——即 phase-context.md 要解决的问题。

---

## Decisions

### 1. resume_context 与 phase-context.md 的分工设计

**方案**：resume_context 退为"指针"，phase-context.md 承担"叙事"

**为什么**：当前 resume_context 试图用一句话同时承担"位置指示"和"上下文摘要"两个职责，结果两者都做得不够好。分离后各司其职。

**分工矩阵**：

| 维度 | resume_context (.stdd.yaml) | phase-context.md |
|------|---------------------------|-----------------|
| **定位** | 机器可读的快速状态指针 | 人+Agent 可读的结构化叙事 |
| **内容** | 当前 phase/slice、最后动作、时间戳、phase_context_file 路径 | 关键决策、已知坑点、未解问题、下一阶段注意事项 |
| **长度** | 1-2 句话 + 结构化字段 | 每阶段 ~20-50 行，累计 ~100-200 行 |
| **更新者** | AI 在每个 phase 切换时自动更新 | AI 在每个 phase 结束时撰写该阶段的章节 |
| **消费者** | `stdd state` CLI、Agent 快速状态检查 | Agent 首次进入新 session 时读取、人类审阅 |
| **读取优先级** | 先读（判断当前进度） | 后读（理解上下文背景） |
| **格式** | YAML 字段 | Markdown 结构化章节 |

**Agent 恢复流程（新 session）**：

```
Step 1: 读取 .stdd.yaml → 获取 active_phase / active_slice / phase_context_file
Step 2: 读取 phase-context.md → 获取完整上下文（2-3 分钟阅读）
Step 3: 如果需要更详细的信息 → 按 phase-context.md 末尾的"完整上下文文件清单"回溯原文
Step 4: 继续执行
```

对比 V2.5 当前：Step 1 后 Agent 只知道位置，Step 2 需要自己翻 proposal.md + design.md + specs + test-plan.md + pending-adjustments.md 来重建上下文。phase-context.md 把 Step 2 从"翻阅 5 个文件"变成"读 1 个文件"。

**备选方案及排除原因**：

- 备选 A：继续扩大 resume_context 字段（加更多 YAML 字段如 `key_decisions: []`, `pitfalls: []`）→ 排除。YAML 不适合写叙事性内容，结构化程度越高越像双轨制——那是 V3.0 的事，V2.7 不做。
- 备选 B：每个 phase 独立一个 context 文件 → 排除。增加文件碎片化，Agent 需要读多个文件。单个累积文件一次性读完。

### 2. phase-context.md 的文件结构

**方案**：单个累积文件 `changes/<change-name>/phase-context.md`，每个 phase 末尾追加一个章节

**模板结构**：

```markdown
# Phase Context — <change-name>

<!--
  阶段交接摘要 — 每个 phase 结束时由 AI 撰写对应章节。
  新 session Agent 优先读取此文件以快速恢复上下文。
  每章节末尾附"完整上下文文件清单"，需要更多细节时回溯原文。
-->

---

## Phase 1: UNDERSTAND (completed 2026-06-01 10:30)

### 关键决策
- **需求边界确定**：<一句话决策>（详见 proposal.md Constraints / NonGoals）
- **优先级判断**：<为什么是 P0 / P1>

### 用户关注点
- 用户特别强调了 <X>（对话中提到 ≥2 次 / Gate 1 反馈中明确要求）

### 被否决的方向
- 方向 A：<一句话描述> — 原因：<用户反馈 / 超出范围>
- 方向 B：<一句话描述> — 原因：<技术不可行 / 优先级低>

### 产出物清单
- proposal.md — Gate 1 已确认，confirmed_at: 2026-06-01T10:30:00

### 完整上下文文件清单
- proposal.md：需求背景、能力列表、约束条件、成功标准

---

## Phase 2: SPEC (completed 2026-06-02 14:00)

### 关键技术决策
- 决策 1：<方案> — 理由：<为什么>；排除：<备选方案>
- 决策 2：...

### 经验触发记录
- EXP-0042（async CancelledError）— 在 <场景> 中被触发，已纳入 spec 的 <Scenario> 测试覆盖

### 已知坑点 / 注意事项
- <坑点 1>：描述 + 应对策略
- <坑点 2>：描述 + 应对策略

### 未解决问题（待 Phase 4 验证）
- <问题 1>：描述 + 当前假设 + 验证方式
- <问题 2>：...

### 产出物清单
- design.md — Gate 2 已确认
- specs/<capability>/spec.md — N 个 Scenario，confirmed
- test-plan.md — M 个 TC-ID，confirmed

### 完整上下文文件清单
- design.md：架构决策（Decisions 章节）、风险与缓解（Risks/Trade-offs）
- specs/<capability>/spec.md：GIVEN/WHEN/THEN 行为规格
- test-plan.md：TC-ID 映射、测试策略、回归风险矩阵

---

## Phase 3: SLICE (completed 2026-06-02 16:00)

### 切片方案
- Slice 1（P0 · 独立）：<名称> — N 个 TC，预估工作量 <X>
- Slice 2（P0 · 依赖 Slice 1）：<名称> — M 个 TC
- parallel_group: 1 → Slice 3 & Slice 4 可并行

### 风险提示
- Slice N 涉及 <核心模块>，风险评分 <高/中/低>

### 产出物清单
- slices.md — N 个切片，依赖关系已标注

---

## Phase 4: BUILD (completed 2026-06-03 11:00)

### 实现决策（非设计偏离，不记录到 design-adjustments）
- 决策 1：使用 <库 X 版本 Y> 而非 <版本 Z> — 因为 <原因>
- 决策 2：<实现模式选择> — 因为 <原因>

### 设计偏离汇总
<!-- 详见 design-adjustments.md -->
- 偏离 1：<标题> — 严重程度 Minor/Major，用户已知/未知
- 偏离 2：...

### 经验触发记录
- EXP-0042 在 <文件:行号> 第 3 次触发 → occurrences 提升至 3，建议 deposit

### 并行执行记录（如适用）
- Slice 3 & Slice 4 并行派发，<M> 个冲突已合并

### 产出物清单
- <N> 个源文件（新增/修改）
- <M> 个测试文件
- pending-adjustments.md（如有设计偏离）

### 完整上下文文件清单
- design-adjustments.md：设计偏离详细说明
- slices.md：切片计划与完成状态
- 源代码文件列表：<列出关键文件路径>

---

## Phase 5: VERIFY (completed 2026-06-03 15:00)

### 测试结果摘要
- 单元测试：<N>/<M> 通过，覆盖率 <X>%
- 集成测试：...
- E2E：...

### 失败模式检查结果
- 11 类检查：<X> 项通过，<Y> 项触发 → 详见 test-report.md

### 设计偏离确认
- 所有偏离已在 design-adjustments.md 中记录，用户已确认

### 产出物清单
- test-report.md
- design-adjustments.md（最终版本）

---

## Current: Phase 6 DELIVER (in progress / completed)

### 当前状态
- <一句话状态描述>

### 下一步
- <下一步动作>
```

**为什么是累积文件而非每 phase 独立文件**：新 session Agent 只需读一个文件即可获得完整上下文。文件总长度预估 ~100-200 行（6 个 phase），在 Agent 上下文预算中占比 < 5%，可接受。

### 3. .stdd.yaml 字段重新设计

**方案**：resume_context 退为简短指针，新增 phase_context_file 字段

```yaml
# .stdd.yaml — V2.7 恢复相关字段
resume_context: "Phase 4 BUILD 完成，3/4 slices 已实现，下一阶段 Phase 5 VERIFY"
active_phase: 4           # 当前所在阶段（1-6）
active_slice: null        # 当前切片号（phase 完成时为 null）
last_action: "所有切片 REFACTOR 完成，全量测试通过，准备进入 Phase 5"
last_modified: "2026-06-03T11:00:00"
phase_context_file: "changes/2026-06-01-feature-x/phase-context.md"
```

变化：
- `resume_context`：从"详细进度描述"退为"一句话状态 + 下一步提示"
- `active_phase`：新增，明确当前阶段号（V2.5 的 `current_phase` 是字符串）
- `phase_context_file`：新增，指向 phase-context.md 的相对路径
- 移除语义上属于 phase-context.md 的冗余信息

**向后兼容**：V2.5 格式的文件中 `phase_context_file` 为 null，Agent 按旧逻辑从各阶段产物重建上下文。

### 4. 上下文预算检查指令

**方案**：build.md 和 verify.md 的 Step 0 之前，增加上下文预算软检查

**为什么放在 build.md 和 verify.md**：这两个阶段对话最长（多轮 RED→GREEN→REFACTOR 循环 + 全量测试验证），上下文膨胀风险最高。Phase 1-2 对话相对短（主要是生成文档+确认），Phase 3/6 更短。

**指令内容**（注入 build.md 和 verify.md 的 Step 0 之前）：

```markdown
### Step -1: 上下文预算检查（V2.7 context-budget-check）

在开始本阶段之前，检查当前会话的上下文状态：

1. **估算上下文长度**：
   - 回顾对话轮次：当前会话大致经历了多少轮用户-Agent 交互？
   - 如果 > 50 轮 → 上下文可能已接近模型有效窗口的 60-70%
   - 如果用户反馈"变慢了" → 上下文几乎确定已膨胀

2. **判断是否需要重置**：
   - 满足以下任一条件时，建议重置：
     a. 对话轮次 > 80 轮
     b. 用户明确说"好慢"或"怎么这么慢"
     c. 上一阶段已完成，且 phase-context.md 已更新
   - **特别提示**：如果你在 OpenCode 中运行，OpenCode 采用完整积累策略无压缩，
     上下文膨胀更快，建议每个 phase 完成后主动重置 session。

3. **如果建议重置**：
   - 确认当前 phase-context.md 已更新到最新状态
   - 确认 .stdd.yaml 的 resume 字段已更新
   - 向用户输出：
     
     ```
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       STDD 上下文预算建议
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     
     当前对话已进行约 <N> 轮，上下文可能接近模型有效窗口上限。
     建议在此保存进度并开启新会话：
     
        stdd state --resume
     
     将上述命令的输出粘贴到新会话中，即可无间断继续。
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ```

4. **如果用户选择重置**：
   - 确保 phase-context.md 已写入最新状态
   - 确保 .stdd.yaml 已更新
   - 输出 `stdd state --resume` 的完整结果
   - 提示用户在新会话中粘贴

5. **如果用户选择继续**（或不满足重置条件）：
   - 正常进入 Step 0，不做额外处理
```

**关键设计决策**：不尝试精确计算 token 数（Agent 无法可靠获取），用对话轮次和用户体感作为代理指标。这是一个**软建议**，不阻断流程。

### 5. `stdd install opencode` 平台适配器

**方案**：复用 OpenCode 对 `.claude/skills/` 的 fallback 读取能力，同时写入 `.opencode/skills/` 作为主路径

**OpenCode 的 skill 加载机制**（来自调研）：

```
主路径：  .opencode/skills/<name>/SKILL.md
Fallback：.claude/skills/<name>/SKILL.md
全局：    ~/.config/opencode/skills/<name>/SKILL.md
```

OpenCode 使用单一 `skill` 工具，所有 SKILL.md 的 name+description 被注入该工具描述。模型通过匹配 description 自动触发，也支持 `/skill-name` 斜杠命令。

**适配器行为**：

```
stdd install opencode

执行动作：
1. 在项目根目录创建 .opencode/skills/ 目录
2. 将 STDD 6 个阶段 skill 复制到 .opencode/skills/<name>/SKILL.md
   命名映射：
     .stdd/skills/understand.md  → .opencode/skills/stdd-understand/SKILL.md
     .stdd/skills/spec.md       → .opencode/skills/stdd-spec/SKILL.md
     .stdd/skills/slice.md      → .opencode/skills/stdd-slice/SKILL.md
     .stdd/skills/build.md      → .opencode/skills/stdd-build/SKILL.md
     .stdd/skills/verify.md     → .opencode/skills/stdd-verify/SKILL.md
     .stdd/skills/deliver.md    → .opencode/skills/stdd-deliver/SKILL.md
3. 如果项目已有 .claude/skills/ → 不做额外写入（OpenCode 可 fallback）
4. 如果项目无 opencode.json → 不自动创建（避免干扰用户现有配置）
   如果项目已有 opencode.json → 检查 instructions 字段是否包含 AGENTS.md，无则提示
5. 输出安装确认摘要
```

**CLI 命令**：

```bash
stdd install opencode              # 安装到当前项目
stdd install opencode --global     # 安装到 ~/.config/opencode/skills/
```

**为什么不做更复杂的 opencode.json 自动配置**：OpenCode 的 `opencode.json` 是用户的核心配置文件（权限、代理、MCP），自动修改风险高。STDD 的 AGENTS.md 已经会被 OpenCode 自动加载为项目指令，skill 通过目录扫描发现，两者组合已足够触发 STDD 流程。

---

## Architecture

### 数据流：阶段切换时的上下文保存

```
Phase N 完成
    │
    ├── 1. AI 撰写 phase-context.md 的 "Phase N" 章节
    │      └── 包含：关键决策、经验触发、已知坑点、未解问题、产出物清单
    │
    ├── 2. AI 更新 .stdd.yaml
    │      ├── resume_context: "Phase N 完成，下一阶段 Phase N+1"
    │      ├── active_phase: N+1 (或 null 如果全部完成)
    │      ├── active_slice: null (阶段切换时清空)
    │      ├── last_action: "Phase N 完成，phase-context.md 已更新"
    │      ├── last_modified: <当前时间戳>
    │      └── phase_context_file: "changes/<name>/phase-context.md" (不变)
    │
    └── 3. 如果是 Gate 确认点（Phase 1/2/5）
           └── 等待用户确认 → 确认后进入下一阶段
```

### 数据流：新 Session 的上下文恢复

```
新 Session 启动
    │
    ├── 1. Agent 读取 .stdd.yaml → 获取 active_phase / phase_context_file
    │
    ├── 2. Agent 读取 phase-context.md → 获取完整上下文
    │      └── 读到 Current 章节 → 知道当前该做什么
    │
    ├── 3. 如果 phase-context.md 中某条决策需要详细信息
    │      └── 按"完整上下文文件清单"回溯对应的正式文档
    │
    └── 4. 上下文预算检查（Step -1）
           └── 判断当前 session 是否需要重置，如需要则提示用户
```

### CLI：stdd state 命令更新

```bash
stdd state                    # 输出当前状态摘要（含 active_phase / active_slice）
stdd state --resume           # 输出完整恢复提示（含 phase-context.md 路径）
stdd state --context          # 打开/输出 phase-context.md 内容
```

`--resume` 输出将包含：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD Resume Context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Change: 2026-06-01-feature-x
Phase: 4 BUILD (completed)
Next Phase: 5 VERIFY
Last Action: 所有切片 REFACTOR 完成，全量测试通过
Last Modified: 2026-06-03T11:00:00

Phase Context: changes/2026-06-01-feature-x/phase-context.md

Key decisions from previous phases:
  - Phase 2: <关键决策摘要>
  - Phase 4: <实现决策摘要>

Known pitfalls:
  - EXP-0042 async CancelledError — triggered 3 times

To resume, read phase-context.md for full context,
then start Phase 5 VERIFY.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| AI 撰写的 phase-context.md 遗漏关键决策 | 章节末尾"完整上下文文件清单"确保可回溯原文；Gate 确认时用户可审核 phase-context 内容 |
| phase-context.md 与正式文档（design.md等）信息不同步 | phase-context 是摘要而非权威源，始终注明"详见 <原文文件>"，冲突时以原文为准 |
| 上下文预算检查误判（轮次少但 token 多） | 软建议不强制；用户可根据实际体感自行决定 |
| OpenCode 未来版本改变 skill 加载路径 | 同时写入 `.opencode/skills/` 和 `.claude/skills/` 双路径，任一有效即可 |
| phase-context.md 在 V3.0 双轨制后成为冗余 | 设计为过渡方案——V3.0 时 content 自动从 Canonical YAML 生成，phase-context.md 退为 Human View |

---

## 【ECC-1】Token 优化策略体系

> 灵感来源：ECC 的模型分层策略（Haiku→Sonnet→Opus）、`/clear` 阶段间上下文清理、小文件约束。STDD 当前无 token 预算意识，借鉴 ECC 的成熟做法。

### 1. 模型分层建议

**方案**：在每个阶段 skill 的开头注入模型推荐提示，帮助用户按任务复杂度选择合适的模型

**推荐矩阵**：

| 阶段 | 推荐模型 | 理由 | 备选（成本敏感） |
|------|---------|------|-----------------|
| Phase 1: UNDERSTAND | Sonnet | 需要深度理解和结构化输出，但文本量不大 | Haiku |
| Phase 2: SPEC | Sonnet / Opus | **最关键阶段**，设计质量直接决定最终质量 | Sonnet |
| Phase 3: SLICE | Haiku / Sonnet | 主要是结构化分析（依赖图、排序），不需要太强推理 | Haiku |
| Phase 4: BUILD | Sonnet | 代码生成主力，需要准确性和速度的平衡 | Haiku（简单切片） |
| Phase 5: VERIFY | Opus / Sonnet | 审查需要强分析能力，尤其是 11 类失败模式检查 | Sonnet |
| Phase 6: DELIVER | Haiku | 纯机械操作（归档、合并、git tag），不需要强推理 | Haiku |

**注入方式**（以 build.md 为例）：

```markdown
## Step -2: 模型选择建议（V2.7 token-optimization）

> 💡 **Token 优化提示**：当前阶段推荐使用 **Claude Sonnet**。
> 
> - 如果当前切片是简单改动（< 3 个 Scenario、无核心模块触碰）→ 可降级到 Haiku 以节省成本
> - 如果当前切片涉及复杂架构决策或安全关键代码 → 建议升级到 Opus
> - 阶段间建议 `/clear` 重置上下文，避免 token 线性膨胀（详见 Step -1 上下文预算检查）
```

**CLI 配置支持**：

```bash
# 在 quality.yaml 中新增模型策略配置段
stdd config set token.model_tiering true     # 启用/禁用模型分层建议（默认启用）
stdd config set token.cost_sensitive true    # 启用成本敏感模式（更激进地推荐 Haiku）
```

**配置结构**（`quality.yaml` 新增）：

```yaml
token:
  model_tiering:
    enabled: true
    mode: default           # default | cost_sensitive
  context_reset_hint: true  # 阶段间提示 /clear
  file_size:
    max_lines: 500          # 建议最大文件行数
    warn_threshold: 400     # 警告阈值
```

### 2. 阶段间上下文重置指导

**方案**：在每个阶段 skill 的结尾注入上下文重置提示，利用 STDD 的 Gate 体系天然分段特性

**注入位置**：每个阶段 skill（understand.md / spec.md / slice.md / build.md / verify.md / deliver.md）的末尾

**模板**：

```markdown
---
## 阶段完成后的上下文管理

本阶段已产出所有必需文件（见产出物清单）。在进入下一阶段之前：

1. **推荐**：开启新对话（`/clear`），将以下内容粘贴到新对话中：
   ```
   stdd state --resume
   ```
   这会让新 session 的 Agent 从干净的上下文开始，避免本阶段的冗长对话影响下一阶段的推理质量。

2. **如果选择继续当前对话**：请留意以下迹象表明上下文可能已膨胀：
   - 响应速度明显变慢
   - Agent 开始"忘记"本阶段早期的决策
   - 生成的代码/文档质量下降

3. **强制时机**：如果当前对话已超过 80 轮，强烈建议重置。
```

**为什么 Embed 在 skill 末尾而非 hooks**：skill 指令是跨平台可移植的（不依赖 Claude Code 特定机制），hooks 是 Claude Code 平台的加速方案。两者互补：skill 提供通用指导，hooks 提供自动化。

### 3. 文件大小约束

**方案**：在各语言规范（`.stdd/standards/<lang>.md`）中增加文件大小指导章节

**模板**（以 python.md 为例）：

```markdown
## 文件大小约束（V2.7 token-optimization）

> 约束目的：控制单文件 token 消耗 + 保持模块可维护性

| 文件类型 | 建议上限 | 硬上限 | 超出时的处理 |
|---------|---------|--------|-------------|
| 业务逻辑模块 | 300 行 | 500 行 | 按职责拆分为多个模块 |
| 测试文件 | 400 行 | 600 行 | 按测试场景拆分为多个测试文件 |
| 配置/常量文件 | 200 行 | 300 行 | 按功能域拆分 |
| `__init__.py` | 30 行 | 50 行 | 仅保留公共 API 导出 |

**Agent 指令**：在 BUILD 阶段生成代码时，如果单个文件将超过建议上限，自动询问用户是否拆分为多个模块。
```

### 设计决策

| 决策 | 选择 | 排除方案及原因 |
|------|------|---------------|
| 模型分层实现方式 | Skill 指令中的**软建议** | 硬编码模型选择 → 排除。STDD 不应替用户决定花多少钱 |
| 阶段间重置 | Skill 末尾嵌入提示（跨平台） + hooks 自动化（Claude Code） | 纯 hooks 方案 → 不够，其他平台需要 skill 层面的指导 |
| 文件大小约束 | 语言规范中增加指导章节 | 新增独立规则文件 → 碎片化，放在现有规范中最自然 |

---

## 【ECC-2】Agent 颗粒度细化

> 灵感来源：ECC 的 48 个专用 subagent（planner / tdd-guide / code-reviewer / security-reviewer / typescript-reviewer / rust-reviewer / go-reviewer 等）。STDD 当前 agent 概念仅在 review 配置中粗略区分 3 类。

### 1. 新增专项 Subagent 定义

**方案**：在 `AGENTS.md` 中定义 4 个新 subagent，复用 Claude Code 的 agent 发现机制

**Agent 清单**：

| Agent ID | 名称 | 职责 | 推荐模型 | 适用阶段 |
|----------|------|------|---------|---------|
| `planner` | 架构规划师 | Phase 2 独立执行技术设计，输出 design.md | Opus | Phase 2 |
| `security-reviewer` | 安全审计员 | 代码安全审计：注入/SQL/XSS/认证/敏感数据 | Opus | Phase 5 |
| `perf-analyzer` | 性能分析师 | 性能热点分析：N+1查询/内存泄漏/阻塞IO | Sonnet | Phase 5 |
| `compat-checker` | 兼容性检查员 | 多版本/多平台兼容性：API breaking/依赖冲突/平台差异 | Sonnet | Phase 5 |

**Agent 定义格式**（以 `security-reviewer` 为例，写入 `AGENTS.md`）：

```markdown
## Subagent: security-reviewer

- **ID**: security-reviewer
- **模型**: Opus（安全审计需要强推理能力）
- **工具**: Read, Grep, Glob, Bash
- **触发条件**: Phase 5 VERIFY 的 review 阶段启用；用户也可通过 `/security-review` 手动触发

### 审查清单

1. **注入漏洞**：SQL 注入、命令注入、模板注入
2. **认证与授权**：Token 管理、权限检查缺失、会话固定
3. **敏感数据**：日志中泄露密钥/密码、明文存储、不安全的传输
4. **依赖安全**：已知 CVE、过期依赖、供应链风险
5. **配置安全**：DEBUG 模式未关、CORS 过于宽松、默认密钥

### 输出格式

```yaml
# 审查结果
severity: critical | high | medium | low
location: <file:line>
finding: <一句话描述>
recommendation: <修复建议>
cwe: <CWE 编号（如适用）>
```
```

### 2. Review 配置扩展

**方案**：`quality.yaml` 的 `review.agents` 从 3 类扩展到 7 类

**变更前（V2.5）**：

```yaml
review:
  agents:
    - name: code
    - name: test_config
    - name: docs_skills
```

**变更后（V2.7）**：

```yaml
review:
  agents:
    # === 原有 3 类（保留） ===
    - name: code
      scope: "代码质量：Bug风险、死代码、一致性、错误处理、安全"
      enabled: true
    - name: test_config
      scope: "测试/配置：测试覆盖、Fixture质量、配置完整性、测试隔离"
      enabled: true
    - name: docs_skills
      scope: "文档/Skills：版本一致性、引用正确性、模板完整性、Skill正确性"
      enabled: true
    
    # === 新增 4 类（默认禁用） ===
    - name: security
      scope: "安全审计：注入/SQL/XSS/认证/敏感数据/依赖CVE"
      enabled: false           # 默认禁用，安全敏感项目手动启用
    - name: performance
      scope: "性能分析：N+1查询、内存泄漏、阻塞IO、算法复杂度"
      enabled: false
    - name: compatibility
      scope: "兼容性检查：API breaking、依赖冲突、平台差异、Python版本"
      enabled: false
    - name: architecture
      scope: "架构一致性：设计偏离、模式违反、SOLID原则、耦合度"
      enabled: false
```

**启用方式**：

```bash
stdd config set review.agents.security.enabled true
stdd config set review.agents.performance.enabled true
```

### 3. Planner Agent 独立化

**方案**：Phase 2 SPEC 阶段引入独立的 planner agent 概念，与当前"一个 Agent 完成所有 Phase 2 工作"的模式形成互补

**两种使用模式**：

```
模式 A（默认·单 Agent）：当前行为不变 — 一个 Agent 完成 Gateway 1 → Phase 2 全部工作

模式 B（可选·双 Agent）：用户显式启用 planner 后
  ┌─ Agent 1 (planner)   : 读取 proposal.md → 产出 design.md
  └─ Agent 2 (spec-writer): 读取 design.md + proposal.md → 产出 specs/*.md + test-plan.md
```

**为什么分离**：
- design.md 是架构决策，specs/*.md 是行为规格——两件事所需的思维模式不同
- 分离后 design.md 的质量更高（独立 agent 不被 spec 细节干扰）
- 符合 ECC "Two-Instance Kickoff" 的思路——不同性质的工作用不同 Agent

**实现**：在 spec.md skill 中增加条件分支：

```markdown
## Step 0: 检查是否启用独立 planner

如果 `quality.yaml` 中 `agents.planner.enabled == true`：
  → 当前 Agent 角色切换为 spec-writer
  → 读取 design.md（由 planner agent 在上一步产出）
  → 从 Step 1 开始（跳过 design.md 生成）

如果未启用或 design.md 不存在：
  → 当前 Agent 同时承担 planner + spec-writer 角色（V2.5 行为）
```

### 设计决策

| 决策 | 选择 | 排除方案及原因 |
|------|------|---------------|
| Agent 启用策略 | **默认禁用**，用户按需开启 | 默认全开 → 增加 token 消耗和噪音，小项目不需要安全审计 |
| Agent 定义位置 | `AGENTS.md` + `quality.yaml` | 独立 agent 文件目录 → V2.7 不做新目录结构，复用现有机制 |
| Planner 独立性 | **可选双 Agent 模式** | 强制分离 → 增加复杂度，简单项目不需要 |

---

## 【ECC-3】Hooks 生命周期增强

> 灵感来源：ECC 的 SessionStart/PreCompact/Stop hooks + 20+ hook 脚本。STDD 当前依赖 AI 手动读取文件恢复状态，hooks 可以实现自动化。

### 1. Hooks 架构设计

**方案**：利用 Claude Code 原生 hooks 机制（`.claude/settings.json`），创建 3 个生命周期 hooks + 对应的 Python 脚本

```
会话生命周期：
  
  SessionStart ────────────────────────────────────────────→ Stop
      │                                                        │
      ├─ hook: session-start.py                                ├─ hook: session-end.py
      │  1. 检测当前目录是否为 STDD 项目                         │  1. 检查是否有未提交的经验条目
      │  2. 读取 .stdd.yaml 获取 active_phase                  │  2. 如果 Phase 5 刚完成 → 提示提取经验
      │  3. 读取 phase-context.md 摘要                          │  3. 更新 session 统计（耗时、轮次）
      │  4. 输出结构化恢复提示                                   │  4. 输出 "本次 session 摘要"
      │                                                        │
      │  PreCompact                                            │
      │      │                                                 │
      │      └─ hook: pre-compact.py                           │
      │         1. 保存当前阶段状态到 .stdd.yaml                 │
      │         2. 确保 phase-context.md 最新                   │
      │         3. 输出压缩后恢复所需的最小上下文                  │
```

### 2. Hook 脚本设计

#### Hook 1: session-start.py

**触发时机**：每次新 session 启动

**逻辑**：

```python
#!/usr/bin/env python3
"""STDD SessionStart Hook — 自动恢复上下文"""

import sys
from pathlib import Path

def main():
    project_root = find_stdd_root()
    if not project_root:
        return  # 非 STDD 项目，静默退出
    
    stdd_yaml = project_root / "changes" / find_active_change(project_root) / ".stdd.yaml"
    if not stdd_yaml.exists():
        print("[STDD] 未检测到活跃 change。使用 /stdd-understand <需求> 开始新变更。")
        return
    
    state = load_yaml(stdd_yaml)
    phase = state.get("active_phase", "unknown")
    phase_context = state.get("phase_context_file", "")
    
    print("━" * 50)
    print("  STDD Session 恢复")
    print("━" * 50)
    print(f"  Change: {state.get('change_name', 'unknown')}")
    print(f"  当前阶段: Phase {phase}")
    print(f"  最后动作: {state.get('last_action', 'unknown')}")
    print(f"  最后更新: {state.get('last_modified', 'unknown')}")
    
    if phase_context:
        pc_path = project_root / phase_context
        if pc_path.exists():
            print(f"\n  📄 阶段上下文: {phase_context}")
            print(f"  💡 建议: 先读取 phase-context.md 了解完整背景")
    
    print(f"\n  下一阶段: Phase {int(phase)+1 if phase != '6' else '完成'}")
    print(f"  执行命令: stdd state --resume")
    print("━" * 50)

if __name__ == "__main__":
    main()
```

#### Hook 2: pre-compact.py

**触发时机**：上下文压缩前

**逻辑**：确保关键状态已持久化到文件系统（而非仅存于对话记忆中）

```python
#!/usr/bin/env python3
"""STDD PreCompact Hook — 压缩前状态保存"""

def main():
    project_root = find_stdd_root()
    if not project_root:
        return
    
    # 关键操作：确保 .stdd.yaml 和 phase-context.md 是最新的
    # 这些文件是压缩后恢复状态的唯一依据
    state = load_stdd_yaml(project_root)
    
    print("[STDD] 上下文即将压缩，当前状态已保存到文件系统：")
    print(f"  - .stdd.yaml: active_phase={state.get('active_phase')}")
    print(f"  - phase-context.md: {state.get('phase_context_file', '未设置')}")
    print("[STDD] 压缩后新 session 可通过 stdd state --resume 恢复。")

if __name__ == "__main__":
    main()
```

#### Hook 3: session-end.py (Stop Hook)

**触发时机**：Session 结束

**逻辑**：提取 session 中的潜在经验，提示用户确认

```python
#!/usr/bin/env python3
"""STDD Stop Hook — Session 结束时的经验提取提示"""

def main():
    project_root = find_stdd_root()
    if not project_root:
        return
    
    state = load_stdd_yaml(project_root)
    phase = state.get("active_phase")
    
    # 仅在 Phase 4/5 结束时提示（这些阶段最可能产生经验）
    if phase in [4, 5]:
        print("[STDD] 本次 session 已完成 BUILD/VERIFY 阶段。")
        print("[STDD] 建议: 运行 stdd experience curate 检查是否有新的失败模式可沉淀为经验。")
        print("[STDD] 当前经验库状态: stdd experience list")

if __name__ == "__main__":
    main()
```

### 3. CLI 安装命令

```bash
stdd hooks install              # 安装 hooks 到 .claude/settings.json
stdd hooks install --force      # 覆盖现有 hooks 配置
stdd hooks status               # 查看当前 hooks 状态
stdd hooks uninstall            # 移除 STDD hooks
```

**`stdd hooks install` 行为**：

1. 读取 `.claude/settings.json`（如不存在则创建）
2. 在 `hooks` 字段中注入 STDD 的 3 个 hook 定义
3. 将 Python hook 脚本复制到 `.stdd/hooks/` 目录
4. 不覆盖用户已有的其他 hooks 配置

### 4. 跨平台降级策略

非 Claude Code 平台（Cursor / Copilot / Aider / OpenCode / Trae / WorkBuddy）不支持原生 hooks，降级为 skill 指令中的手动步骤：

```markdown
## 阶段完成后的手动步骤（非 Claude Code 平台）

如果当前平台不支持自动 hooks，请手动执行：
1. 确认 .stdd.yaml 已更新（active_phase、last_action、last_modified）
2. 确认 phase-context.md 已追加本阶段章节
3. 在新 session 中粘贴: stdd state --resume
```

### 设计决策

| 决策 | 选择 | 排除方案及原因 |
|------|------|---------------|
| Hooks 实现语言 | **Python**（复用 bin/stdd 生态） | Node.js（ECC 方式）→ STDD 是 Python 项目，引入 Node.js 增加依赖 |
| 平台策略 | Claude Code 用 hooks，其他平台降级为手动 | 跨平台通用 hooks 抽象层 → V2.7 不做，成本太高 |
| Hook 脚本位置 | `.stdd/hooks/` 目录 | 散落在 bin/ 中 → 专用目录更清晰 |

---

## 【ECC-4】Skill 生态扩展

> 灵感来源：ECC 的 182 个 Skill 按 6 大类别（语言标准、框架模式、工作流、领域知识、工具集成、学习自动化）组织。STDD 当前仅 6 个阶段 Skill。

### 1. Skill 目录结构重构

**方案**：`.stdd/skills/` 从平铺 6 个文件扩展为按类别组织的目录树

**变更前（V2.5）**：

```
.stdd/skills/
├── _shared/
├── understand.md
├── spec.md
├── slice.md
├── build.md
├── verify.md
└── deliver.md
```

**变更后（V2.7）**：

```
.stdd/skills/
├── _shared/                          # 共享模板和工具函数

├── core/                             # 核心 6 阶段 Skill（原位置，重组织）
│   ├── understand.md
│   ├── spec.md
│   ├── slice.md
│   ├── build.md
│   ├── verify.md
│   └── deliver.md

├── languages/                        # 【新增】语言专项 Skill
│   ├── python-patterns/
│   │   ├── SKILL.md                  # Python 惯用法、async、类型提示
│   │   └── examples/
│   ├── fastapi-patterns/
│   │   ├── SKILL.md                  # FastAPI 路由/依赖注入/中间件模式
│   │   └── examples/
│   ├── go-idioms/
│   │   ├── SKILL.md                  # Go 并发/错误处理/接口设计惯用法
│   │   └── examples/
│   ├── typescript-standards/
│   │   ├── SKILL.md                  # TS 类型系统/ESM-CJS/React 模式
│   │   └── examples/
│   └── rust-patterns/
│       ├── SKILL.md                  # Rust 所有权/生命周期/错误处理模式
│       └── examples/

├── workflow/                         # 【新增】工作流辅助 Skill
│   ├── search-first/
│   │   └── SKILL.md                  # "先搜索现有方案再写代码" —— ECC 的 search-first 理念
│   └── skill-create/
│       └── SKILL.md                  # 指导 AI 如何创建新的 STDD Skill

└── tools/                            # 【新增】工具集成 Skill
    ├── docker-build/
    │   └── SKILL.md                  # Docker 镜像构建和 compose 配置
    └── db-migration/
        └── SKILL.md                  # 数据库迁移：Alembic/Flygoose 最佳实践
```

### 2. Skill 规范（SKILL.md 格式）

采用 ECC 兼容的 YAML frontmatter + Markdown body 格式，确保与 ECC 生态互操作：

```markdown
---
name: python-patterns
description: Python 惯用法、async/await 模式、类型提示、PEP 合规。在编写 Python 代码时自动激活。
origin: STDD
version: 1.0.0
category: language-standards
language: python
related_skills:
  - fastapi-patterns
  - python-testing
---

# Python 编程模式

## 何时激活
- 当 STDD change 的 project_type 为 python
- 当 Phase 4 BUILD 开始且语言为 Python
- 当用户手动触发 `/python-patterns`

## 核心规范

### 1. 类型提示（PEP 484/585/604）
```python
# ✅ 推荐：使用 Python 3.10+ 新语法
def process(items: list[str], config: dict[str, int] | None = None) -> Result:
    ...

# ❌ 避免：旧式类型提示
from typing import List, Dict, Optional
def process(items: List[str], config: Optional[Dict[str, int]] = None) -> Result:
    ...
```

### 2. async/await 模式
```python
# ✅ 推荐：结构化并发（asyncio.TaskGroup）
async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch_a())
        tg.create_task(fetch_b())

# ❌ 避免：裸 create_task 无生命周期管理
```

### 3. 错误处理
```python
# ✅ 推荐：具体异常 + 上下文
try:
    await client.fetch(url)
except aiohttp.ClientError as e:
    raise AppError(f"Failed to fetch {url}") from e

# ❌ 避免：裸 except + 吞异常
except:
    pass
```

## 反模式
1. **可变默认参数**：`def f(items=[])` → `def f(items=None)`
2. **循环中导入**：`for x in xs: import module` → 顶部导入
3. **字符串拼接 SQL**：`f"SELECT * FROM {table}"` → 使用参数化查询

## 相关 STDD 经验
- EXP-0042: async CancelledError 未捕获
- EXP-0017: asyncio.create_task 任务泄漏
```

### 3. search-first Skill（工作流辅助）

> 直接借鉴 ECC 的 `search-first` skill 理念：在开始编写代码之前先搜索现有方案。

```markdown
---
name: search-first
description: Adopt → Extend → Compose → Build 决策矩阵。在写任何代码之前，先搜索现有方案。
origin: STDD (inspired by ECC)
version: 1.0.0
category: workflow
---

# Search-First：先搜索再编码

## 核心理念

在 AI 编程中，"直接写"通常比"先搜索"更慢——因为 AI 可能实现一个已有成熟库的方案。

## 决策矩阵

在 Phase 2 SPEC 或 Phase 4 BUILD 开始前，对每个 capability 执行：

1. **Adopt**：是否有现成的标准库/官方方案可以直接采用？
2. **Extend**：是否有成熟库可以通过少量扩展满足需求？
3. **Compose**：是否可以通过组合多个现有库实现？
4. **Build**：前 3 步都不满足 → 自己写。

## 工作流

```
Phase 2 SPEC 开始前:
  1. 对每个 capability 执行 search-first
  2. 在 design.md 的 Decisions 中记录搜索结果
  3. 如果选择 Build（自己写），必须记录理由

Phase 4 BUILD 开始前:
  1. 对每个切片执行 search-first
  2. 搜索结果记录在 code comment 或 design-adjustments 中
```
```

### 4. skill-create 命令

```bash
stdd skill create <name>          # 基于模板创建新 Skill（交互式）
stdd skill create <name> --type language  # 指定类型
stdd skill create <name> --from-ecc <skill-name>  # 从 ECC 生态导入（未来功能）
```

**`stdd skill create` 行为**：

1. 在 `.stdd/skills/<category>/<name>/` 创建目录
2. 基于内置模板生成 `SKILL.md` 骨架
3. 如果 `--type language`：自动关联语言规范（`.stdd/standards/<lang>.md`）
4. 向用户提示下一步：填充 SKILL.md 内容 → 测试 skill 激活 → 提交

### 5. 第一阶段交付清单

V2.7 不追求 182 个 Skill，而是建立框架 + 精选示范：

| Skill | 类别 | 状态 | 说明 |
|-------|------|------|------|
| `python-patterns` | languages | V2.7 交付 | Python 最常用，优先做 |
| `fastapi-patterns` | languages | V2.7 交付 | FastAPI 社区大，需求明确 |
| `go-idioms` | languages | V2.7 交付 | Go 语言规范已存在，skill 做深化 |
| `search-first` | workflow | V2.7 交付 | 直接借鉴 ECC，方法论成熟 |
| `skill-create` | workflow | V2.7 交付 | 用于用户自己扩展更多 skill |
| `typescript-standards` | languages | V2.8 | 排在第二批 |
| `rust-patterns` | languages | V2.8 | 排在第二批 |
| `docker-build` | tools | V2.8 | 排在第二批 |
| `db-migration` | tools | V2.8 | 排在第二批 |

### 设计决策

| 决策 | 选择 | 排除方案及原因 |
|------|------|---------------|
| Skill 格式 | ECC 兼容的 YAML frontmatter + Markdown | 自定义格式 → 失去与 ECC 生态互操作的可能 |
| 第一阶段范围 | 框架 + 5 个示范 Skill | 批量创建 20+ Skill → 质量无法保证，先做精再做多 |
| 目录结构 | `core/` + `languages/` + `workflow/` + `tools/` 四级分类 | ECC 的一级平铺 → STDD Skill 数量少但职责分明，分类更重要 |

---

## 【CG-1】代码结构摘要系统 (Code Structure Summary)

> 灵感来源：CodeGraph 的预索引代码知识图谱 + 用户提的需求——"STDD 代码大部分是 STDD 流程中写的，BUILD 完成后立即生成结构摘要，后续 change 直接读取"。
>
> 与 CodeGraph 的关键差异：CodeGraph 用 tree-sitter 自动解析生成**语法精确但无意图**的符号图；STDD 代码结构摘要是 AI 在 BUILD 阶段撰写、记录**设计意图和模块职责**的人类可读摘要。两者互补而非替代。

### 1. 核心理念

```
传统 AI 编程（每个 change 从零开始）:
  Change 1 BUILD → 代码产出
  Change 2 启动 → Agent 从头扫描文件系统（grep/Read 大量文件）
  Change 3 启动 → Agent 再次从头扫描...
  → 每个新 change 都在重新"发现"代码结构，浪费 token

STDD 代码结构摘要（自积累代码知识）:
  Change 1 BUILD → 代码产出 → AI 撰写 code-structure-delta.md ──→ 合并到 index.md
  Change 2 启动 → Agent 读取 index.md（1 个文件，了解全部代码结构）
  Change 2 BUILD → 代码产出 → AI 撰写新的 delta ──→ 追加到 index.md
  Change 3 启动 → Agent 读取 index.md（包含了 Change 1+2 的所有结构）
  → 项目越久，index.md 越丰富，Agent 理解代码越快
```

**关键洞察**：STDD 不需要像 CodeGraph 那样"扫描"代码——因为在 BUILD 阶段，AI **已经知道自己写了什么**。只需要在写完之后**记录下来**即可。

### 2. 目录结构

```
项目根目录/
├── .stdd/
│   ├── code-structure/                    # 【新增】代码结构知识库
│   │   ├── .structure-index.yaml          # 机器可读索引（AI 消费者）
│   │   ├── index.md                       # 人类可读累积摘要（AI + 人消费者）
│   │   └── deltas/                        # 每次 change 的增量（存档追溯）
│   │       ├── 2026-05-14-api-rate-limit.md
│   │       ├── 2026-05-15-user-auth.md
│   │       └── ...
│   ├── experiences/                       # 现有
│   ├── templates/                         # 现有
│   └── ...
└── changes/
    └── <change-name>/
        ├── code-structure-delta.md        # 【新增】本 change 的结构增量
        ├── proposal.md
        ├── design.md
        └── ...
```

### 3. 数据流与生命周期

```
Phase 4 BUILD ──────────────────────────────────────────────────────────────────
  │
  │  AI 完成所有切片的 RED→GREEN→REFACTOR
  │
  ├── Step 4.N: 撰写代码结构增量
  │     AI 根据本 change 产生/修改的代码，撰写 code-structure-delta.md
  │     内容聚焦：新增/修改模块、关键符号、依赖关系、集成点
  │
Phase 5 VERIFY ──────────────────────────────────────────────────────────────────
  │
  ├── 检查项：code-structure-delta.md 与源代码一致性
  │     Agent 抽查：delta 中列出的文件是否存在？关键符号签名是否匹配？
  │     发现偏差 → 更新 delta
  │
Phase 6 DELIVER ──────────────────────────────────────────────────────────────────
  │
  ├── stdd deliver 执行：
  │     1. 将 code-structure-delta.md 复制到 .stdd/code-structure/deltas/
  │     2. 解析 delta，提取结构化数据更新 .structure-index.yaml
  │     3. 基于最新 index.yaml 重新生成 index.md（追加 + 合并）
  │     4. 更新 index.md 头部的 "最后更新" 时间戳和 git HEAD
  │
New Change Phase 1/2 ─────────────────────────────────────────────────────────────
  │
  ├── Agent 启动时：
  │     1. 检测 .stdd/code-structure/index.md 是否存在
  │     2. 如果存在 → 读取 index.md（建议在 proposal 生成前）
  │     3. 根据当前 change 的 capability 列表 → 定位相关模块章节
  │     4. 在 proposal 的 Impact 评估中引用代码结构信息
  │
  ├── Phase 2 SPEC 时：
  │     读取 index.md 中与本 change 相关的模块 → 评估设计决策的影响范围
  │     如果 index.md 显示相关模块复杂度过高 → 提示需要更详细的 spec 锚定
```

### 4. 文件格式设计

#### 4.1 code-structure-delta.md（Change 级增量）

```markdown
# Code Structure Delta — <change-name>

> 生成时间: 2026-05-14T16:30:00 | Git commit: a1b2c3d
> 置信度: 0.70 (AI-generated — 以源代码为准)
> STDD change: changes/2026-05-14-api-rate-limit/

## 新增模块

### middleware/rate_limit.py
- **职责**: API 速率限制中间件，基于令牌桶算法实现请求限流
- **关键符号**:
  - `class TokenBucket` — 令牌桶数据结构（capacity, refill_rate, tokens）
  - `async def rate_limit_middleware(request, call_next)` — FastAPI ASGI 中间件
  - `def get_client_identifier(request)` — 提取 IP + Token 作为限流键
- **上游依赖** (本模块引用了什么):
  - `app.core.config.settings` → 读取 `RateLimitConfig`
  - `app.lib.redis_client` → 分布式令牌桶存储（`incr` + `expire`）
- **下游被依赖** (什么引用了本模块):
  - `app.main:app.add_middleware()` → 注册为全局中间件
- **设计背景**: Phase 2 决策 #3 — 选择令牌桶而非漏桶（详见 design.md Decisions）

### app/core/config.py (修改)
- **变更类型**: 扩展
- **新增符号**:
  - `class RateLimitConfig(BaseSettings)` — max_requests / window_seconds / whitelist_ips
  - `settings.rate_limit` — 新增配置访问点
- **下游影响**: middleware/rate_limit.py 依赖此配置

## 新增 API 端点

### GET /api/v1/rate-limit/status
- **方法/路径**: GET /api/v1/rate-limit/status
- **处理器**: `api.v1.rate_limit.get_status()`
- **认证**: 需要 Bearer Token
- **返回**: { remaining, limit, reset_at } — 当前 IP 的配额状态

## 集成点

- **中间件栈顺序**: auth → **rate_limit** → logging → error_handler
- **Redis 新增键模式**: `ratelimit:{ip}:{token}` — TTL = window_seconds
- **配置新增节**: `[rate_limit]` — max_requests / window_seconds / whitelist_ips

## 测试文件

- `tests/middleware/test_rate_limit.py` (8 tests) — TC-RATE-001 ~ TC-RATE-008
- `tests/api/v1/test_rate_limit_status.py` (4 tests) — TC-RATE-009 ~ TC-RATE-012
```

**模板规范**（写入 `.stdd/templates/code-structure-delta.md`）：

每个 delta 必须包含：
- ✅ **新增模块**（新文件/新类/新函数及其职责）
- ✅ **修改模块**（对现有文件的扩展及其影响）
- ✅ **API 端点**（如有，含 HTTP 方法/路径/处理器/认证）
- ✅ **集成点**（中间件栈、数据库、消息队列、外部服务）
- ✅ **测试文件**（关联的测试文件和 TC-ID 范围）
- 可选：**已知坑位**（本次开发中发现但未修复的技术债务）

#### 4.2 index.md（项目级累积索引）

```markdown
# 项目代码结构索引

> 最后更新: 2026-05-21T15:30:00 | Git HEAD: f3e4d5c
> 累计 changes: 7 | 覆盖模块: 23 个文件 | 最新 change: 2026-05-21-user-pro-upgrade
> 置信度: 0.70 (AI 累积生成 — 以源代码为准)
>
> 🟢 状态: FRESH — 最近更新于 2 小时前

## 按模块浏览

### middleware/ (3 个模块)

#### rate_limit.py
- **职责**: API 速率限制（令牌桶算法）
- **关键符号**: TokenBucket / rate_limit_middleware / get_client_identifier
- **依赖**: app.core.config(RateLimitConfig) → app.lib.redis_client
- **被依赖**: app.main (全局中间件) → api.v1.rate_limit.get_status
- **变更历史**: [2026-05-14-api-rate-limit]

#### auth.py
- **职责**: Bearer Token 认证中间件
- **关键符号**: AuthMiddleware / verify_token / extract_bearer_token
- **依赖**: app.core.config(AuthConfig) → app.lib.redis_client(token黑名单)
- **被依赖**: app.main (全局中间件) → 所有 /api/v1/* 端点
- **变更历史**: [2026-05-15-user-auth]

### app/core/ (2 个模块)

#### config.py
- **职责**: 全局配置管理（pydantic BaseSettings）
- **关键符号**: Settings, RateLimitConfig, AuthConfig, DatabaseSettings
- **被依赖**: middleware.rate_limit, middleware.auth, api.v1.auth, db.session
- **变更历史**: [2026-05-14-api-rate-limit, 2026-05-15-user-auth]

### api/v1/ (4 个模块)

#### rate_limit.py
- **职责**: 限流状态查询 API
- **端点**: GET /api/v1/rate-limit/status
- **关键符号**: get_status()
- **依赖**: middleware.rate_limit.TokenBucket
- **变更历史**: [2026-05-14-api-rate-limit]

## 集成点总览

### 中间件栈
```
app.main
  ├── middleware.auth (→ redis, config)
  ├── middleware.rate_limit (→ redis, config)
  ├── middleware.logging
  └── middleware.error_handler
```

### Redis 键空间
| 键模式 | 使用者 | 用途 |
|--------|--------|------|
| `ratelimit:{ip}:{token}` | middleware.rate_limit | 请求计数+TTL |
| `blacklist:token:{jti}` | middleware.auth | Token 黑名单 |
| `cache:response:{hash}` | api.v1.cache | 响应缓存 |

## 依赖关系图

```
app.main
  ├── middleware.auth ─────→ redis_client, config
  ├── middleware.rate_limit → redis_client, config
  │     └── TokenBucket
  ├── middleware.logging
  └── api.v1
        ├── rate_limit.get_status → TokenBucket
        ├── auth.login → redis_client, config
        └── users.get_profile → db.session
```
```

#### 4.3 .structure-index.yaml（机器可读索引）

```yaml
# 代码结构索引 — 机器可读版本（AI 消费者）
# 由 stdd deliver 自动更新，AI 可直接 parse 此文件进行结构化查询

meta:
  last_updated: "2026-05-21T15:30:00"
  git_head: "f3e4d5c"
  total_changes: 7
  total_modules: 23
  freshness: fresh     # fresh | stale (>7天) | unknown

modules:
  - path: middleware/rate_limit.py
    symbols:
      - name: TokenBucket
        type: class
        role: "令牌桶数据结构"
      - name: rate_limit_middleware
        type: async_function
        role: "FastAPI ASGI 限流中间件"
      - name: get_client_identifier
        type: function
        role: "提取客户端标识"
    dependencies:
      - app.core.config.RateLimitConfig
      - app.lib.redis_client
    dependents:
      - app.main
      - api.v1.rate_limit.get_status
    changes:
      - 2026-05-14-api-rate-limit

integration_points:
  - type: middleware_stack
    order: [auth, rate_limit, logging, error_handler]
  - type: redis_keyspace
    entries:
      - pattern: "ratelimit:{ip}:{token}"
        user: middleware.rate_limit
      - pattern: "blacklist:token:{jti}"
        user: middleware.auth

api_endpoints:
  - method: GET
    path: /api/v1/rate-limit/status
    handler: api.v1.rate_limit.get_status
    auth: Bearer Token
    change: 2026-05-14-api-rate-limit
```

### 5. 新鲜度与陈旧检测

借鉴 CodeGraph 的 index freshness 机制：

```markdown
<!-- index.md 头部显示 -->
> 🟢 状态: FRESH — 最近更新于 2 小时前
> 🟡 状态: STALE — 最近更新于 3 天前，期间有 2 个未归档的 git commit
> 🔴 状态: STALE — 最近更新于 12 天前，建议运行 stdd structure rebuild
```

**检测逻辑**（嵌入 `stdd state --resume` 和 Phase 1/2 skill）：

```
1. 读取 index.md 头部的 git_head
2. git rev-parse HEAD → 当前 HEAD
3. 如果 git_head != HEAD → 🟡 输出 "代码结构索引可能过时，建议在 DELIVER 后更新"
4. 如果 index.md 的 last_updated > 7 天 → 🔴 提示重新生成
```

### 6. CLI 命令

```bash
stdd structure delta <change-name>    # 为指定 change 生成 code-structure-delta.md（Phase 4 末尾自动调用）
stdd structure merge <change-name>    # 将 delta 合并到 index（Phase 6 自动调用）
stdd structure rebuild                # 全量重建索引（当 index 严重过时时）
stdd structure show [module]          # 查看代码结构摘要（按模块过滤）
stdd structure graph                  # 输出 ASCII 依赖关系图
```

### 7. Skill 指令注入

#### build.md 新增步骤

```markdown
### Step N: 生成代码结构增量（V2.7 code-structure-summary）

在所有切片 REFACTOR 完成后、进入 Phase 5 之前：

1. **收集**：本 change 新增/修改的所有文件列表（从 git diff 或 slices.md 获取）
2. **分析**：每个文件的核心职责、关键符号、上下游依赖
3. **撰写**：按模板生成 code-structure-delta.md（`./stdd/templates/code-structure-delta.md`）
4. **自查**：
   - 是否覆盖了所有新增/修改的模块？
   - 依赖关系是否与 import 语句一致？
   - 集成点是否与 design.md 的架构决策一致？
5. **标注置信度**：在 delta 头部注明 `置信度: 0.70 (AI-generated)`
```

#### understand.md / spec.md 新增步骤

```markdown
### Step -1: 读取代码结构索引（V2.7 code-structure-summary）

在生成 proposal 之前：

1. **检测**：`.stdd/code-structure/index.md` 是否存在？
2. **如果存在**：
   - 读取 index.md → 快速理解现有代码结构
   - 检查新鲜度：索引是否过时（> 7 天或 git HEAD 不一致）？
   - 识别与当前需求相关的已有模块
3. **在 proposal 中引用**：
   - Impact 章节添加 "相关现有模块" 列表（来自 index.md）
   - 如果一个模块被多个 change 依赖 → 标记为 "核心模块，修改需高风险评审"
```

### 设计决策

| 决策 | 选择 | 排除方案及原因 |
|------|------|---------------|
| 生成方式 | **AI 撰写**（在 BUILD 完成后） | tree-sitter 自动解析（CodeGraph 方式）→ 缺少设计意图，且需要额外依赖 |
| 索引格式 | **Markdown（人读）+ YAML（机读）双轨** | 纯 YAML → 可读性差，不符合 STDD "人可审阅" 的原则 |
| 合并策略 | **Phase 6 DELIVER 时正式合并** | 实时更新 → 实现复杂，DELIVER 时合并更符合 STDD 的 Gate 确认模式 |
| 陈旧检测 | **git HEAD 对比 + 时间戳**（软检查） | 文件监控自动同步 → 超出 V2.7 范围，留给 V3.0 |
| 与 CodeGraph 的关系 | **互补推荐**：用户可同时安装 CodeGraph 获取精确的符号级查询，STDD 摘要提供意图级理解 | 替代 CodeGraph → 两者定位不同，不应互相替代 |

---

## 【CG-2】经验 Provenance 字段

> 灵感来源：CodeGraph 的 Trust Signal 系统——每条边标注 `provenance`(tree-sitter/heuristic) + `confidence`(0.3-0.95)。STDD 的经验条目有 `confidence` 但无 `provenance`。

### 1. 经验数据模型扩展

**变更前（V2.5）**：

```yaml
---
experience_id: EXP-2026-0042
category: cascading_errors
confidence: 0.92
occurrences: 3
---
```

**变更后（V2.7）**：

```yaml
---
experience_id: EXP-2026-0042
category: cascading_errors
confidence: 0.92
provenance: ci-detected           # 【新增】ci-detected | ai-inferred | human-reported | community-imported
provenance_weight: 0.85           # 【新增】该来源的基础权重
occurrences: 3
# provenance 历史（可选，追踪来源变化）
provenance_history:
  - source: ai-inferred
    recorded_at: "2026-05-15T10:00:00"
  - source: ci-detected
    recorded_at: "2026-05-16T14:00:00"  # CI 再次确认后升级
---
```

### 2. Provenance 权重体系

```yaml
# .stdd/config.d/experience.yaml 新增配置
provenance:
  weights:
    human-reported: 0.95       # 人工报告 — 最高可信度
    ci-detected: 0.85          # CI 自动化检测 — 高可信度但可能误报
    ai-inferred: 0.60          # AI 推测 — 需要后续验证
    community-imported: 0.50   # 社区导入 — 需本地验证后方可提升
  auto_promote:
    enabled: true
    rules:
      - if: provenance == "ai-inferred" AND occurrences >= 3
        then: provenance → "ci-detected", confidence → max(confidence, 0.85)
        # 同一模式被 AI 反复发现 3 次 → 升级为 CI 检测级别
      - if: provenance == "community-imported" AND occurrences >= 2
        then: provenance → "ci-detected", confidence → max(confidence, 0.80)
        # 社区经验在本地验证 2 次后 → 升级
```

### 3. CLI 支持

```bash
# 按 provenance 过滤经验
stdd experience list --provenance ci-detected
stdd experience list --provenance human-reported

# 手动修改 provenance（如 AI 推断的经验被人工确认）
stdd experience update EXP-0042 --provenance human-reported

# 查看 provenance 分布统计
stdd experience stats --by-provenance
```

### 设计决策

| 决策 | 选择 | 排除方案及原因 |
|------|------|---------------|
| 默认值 | 现有经验默认 `ai-inferred` (0.60) | `human-reported` (0.95) → V2.5 之前的经验都是 AI 推断的，高估会误导 |
| 权重配置 | YAML 配置文件可调 | 硬编码 → 不同项目对来源的信任偏好不同 |
| 自动升级 | 3 次以上 AI 发现 → 自动升级为 ci-detected | 不自动升级 → 违背"项目用得越久 STDD 越聪明"的理念 |

---

## 【CG-3】状态新鲜度校验

> 灵感来源：CodeGraph 的 Index Freshness Awareness — 每次 MCP 响应尾部带 `Index updated 5 minutes ago`，超 30 分钟 → 陈旧警告。

### 1. .stdd.yaml 字段扩展

**变更前（V2.5）**：

```yaml
resume_context: "Phase 4 BUILD 完成，3/4 slices 已实现"
active_phase: 4
last_modified: "2026-06-03T11:00:00"
```

**变更后（V2.7）**：

```yaml
resume_context: "Phase 4 BUILD 完成，3/4 slices 已实现"
active_phase: 4
last_modified: "2026-06-03T11:00:00"

state_freshness:                        # 【新增】
  verified_at: "2026-06-03T11:00:00"   # 状态确认时间
  git_head: "a1b2c3d4"                 # 状态保存时的 git HEAD
  key_files_hash:                       # 关键产出物的内容哈希
    phase-context.md: "sha256:e3b0c4..."
    proposal.md: "sha256:d2a1b3..."
    test-report.md: "sha256:f4c5d6..."
```

### 2. 新鲜度检查逻辑

**触发时机**：Agent 启动时（session-start hook）、`stdd state --resume` 时、Phase 切换时

**检查流程**：

```python
def check_state_freshness(stdd_yaml):
    current_head = git("rev-parse HEAD")
    saved_head = stdd_yaml["state_freshness"]["git_head"]
    
    elapsed = now() - stdd_yaml["state_freshness"]["verified_at"]
    
    if current_head != saved_head:
        commits_diff = git(f"rev-list {saved_head}..{current_head} --count")
        return {
            "status": "stale",
            "level": "🟡",
            "message": f"Git HEAD 已变更（+{commits_diff} commits since 状态保存）。"
                       f"建议: 检查变更是否影响当前 change 的产出物。",
            "diff_commits": commits_diff
        }
    
    if elapsed > timedelta(days=7):
        return {
            "status": "stale",
            "level": "🔴",
            "message": f"状态已 {elapsed.days} 天未更新。建议重新验证当前状态。"
        }
    
    if elapsed > timedelta(days=3):
        return {
            "status": "aging",
            "level": "🟡",
            "message": f"状态已 {elapsed.days} 天未更新。"
        }
    
    return {"status": "fresh", "level": "🟢"}
```

### 3. 输出示例

**`stdd state --resume` 输出**：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD Resume Context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Change: 2026-06-01-feature-x
Phase: 4 BUILD (completed)
Next Phase: 5 VERIFY

🟡 State Freshness: AGING
   Git HEAD 已变更：+2 commits since 状态保存
   建议: 运行 git diff --stat 检查是否影响本 change
   强制继续: stdd state --resume --force
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 设计决策

| 决策 | 选择 | 排除方案及原因 |
|------|------|---------------|
| 校验频率 | 仅在 `--resume` 和 phase 切换时检查 | 每次工具调用时检查 → 增加噪音和延迟 |
| 旧状态处理 | 软警告 + `--force` 跳过 | 硬阻断 → 用户可能在 STDD 之外正常提交，不应阻断 |
| files_hash 范围 | 仅 STDD 产出物（.stdd.yaml / phase-context.md / test-report.md） | 包含源代码文件 → 源代码频繁变更会导致大量误报 |

---

## 【CG-4】关键规则双语注入

> 灵感来源：CodeGraph 的 "5 English NEVER rules + 5 Chinese 「绝不」 rules" — 解决中文模型（DeepSeek/Qwen/GLM）忽略纯英文置信度警告的问题。

### 1. 规则清单（10 条强制性约束）

| # | 中文 | English |
|---|------|---------|
| 1 | **绝不可跳过 Gate 确认** — 三道 Gate 都必须收到用户明确确认后才能继续 | **NEVER skip a Gate** — all three Gates must receive explicit user confirmation before proceeding |
| 2 | **绝不静默修改设计** — 实现中对设计的任何偏离必须记录到 design-adjustments.md | **NEVER silently deviate from the design** — every design deviation must be recorded in design-adjustments.md |
| 3 | **绝不可先写代码再补测试** — 严格 RED → GREEN → REFACTOR 顺序 | **NEVER write code before tests** — strictly follow RED → GREEN → REFACTOR order |
| 4 | **绝不可跳过失败模式检查** — Phase 5 必须全量检查 11 类失败模式 | **NEVER skip failure mode checks** — Phase 5 must check all 11 failure mode categories |
| 5 | **绝不可在 Gate 2 确认前开始实现** — 没有确认的 design + spec + test-plan，不得进入 Phase 3 | **NEVER start implementation before Gate 2 confirmation** — without confirmed design + spec + test-plan, do not enter Phase 3 |
| 6 | **绝不可忽略模板** — 生成任何 STDD 文档前必须先读取对应模板 | **NEVER ignore templates** — always read the corresponding template before generating any STDD document |
| 7 | **绝不可跳过覆盖率诊断** — Phase 5 必须运行覆盖率检查并输出覆盖率报告 | **NEVER skip coverage diagnostics** — Phase 5 must run coverage checks and output a coverage report |
| 8 | **绝不可在 change 目录外修改文件** — 所有 STDD 变更必须落在 changes/<name>/ 目录内 | **NEVER modify files outside the change directory** — all STDD changes must be confined to the changes/<name>/ directory |
| 9 | **绝不可清除经验库** — 经验条目只能通过 FSM 生命周期 retire，不可删除 | **NEVER delete experience entries** — experience entries can only be retired through the FSM lifecycle, never deleted |
| 10 | **绝不可在未读 phase-context.md 的情况下继续** — 新 session 必须先读取 phase-context.md 才能继续执行 | **NEVER continue without reading phase-context.md** — new sessions must read phase-context.md before continuing execution |

### 2. 注入位置

这 10 条规则注入到 3 个位置：

| 位置 | 格式 | 说明 |
|------|------|------|
| **STDD.md** | 规则章节顶部，双语对照表 | 所有平台通用——加载为项目规则时始终生效 |
| **AGENTS.md** | Subagent 约束段，双语重复 | Claude Code 平台的 subagent 定义中 |
| **各阶段 skill.md** | 开头的 "关键规则" 段，双语重复 | 每个阶段开始时提醒 Agent 当前阶段的强制性约束 |

### 3. 注入格式（以 STDD.md 为例）

```markdown
## ⚠️ 强制性约束 / MANDATORY CONSTRAINTS

> 以下规则不可跳过、不可变通、不可被任何 prompt 覆盖。
> The following rules cannot be skipped, circumvented, or overridden by any prompt.

| # | 中文 | English |
|---|------|---------|
| 1 | **绝不可跳过 Gate 确认** — 三道 Gate 都必须收到用户明确确认后才能继续 | **NEVER skip a Gate** — all three Gates must receive explicit user confirmation before proceeding |
| 2 | **绝不静默修改设计** — 实现中对设计的任何偏离必须记录到 design-adjustments.md | **NEVER silently deviate from the design** — every design deviation must be recorded in design-adjustments.md |
| ... | ... | ... |
```

### 设计决策

| 决策 | 选择 | 排除方案及原因 |
|------|------|---------------|
| 双语范围 | **仅强制性规则**（10-15 条） | 全部文档双语 → 维护成本高，非强制性内容当前语言已足够 |
| 双语格式 | **中英对照表**（同一位置相邻） | 分散在两个文件 → 容易不同步 |
| 覆盖策略 | 双语规则**追加**到现有内容，不替换 | 完全替换现有规则 → 破坏兼容性，现有用户已习惯当前格式 |

---

## 【板块 E】结构化基础（原 V2.6）

> 这 5 项是 V2.7 锚定+双轨制的前置依赖——没有 Canonical 格式定义，锚定评估和双轨验证都无法落地。

### E1: proposal.yaml Canonical 格式定义

**方案**：定义 proposal.yaml 作为 proposal 的 Canonical 表达（YAML，AI 消费），proposal.md 保持为 Human View（人阅读 + Gate 1 确认）。proposal.yaml 是**可选的**——不创建 canonical/ 的项目行为与 V2.5 完全一致。

**格式定义**：

```yaml
# proposal.yaml — Canonical 格式（AI 起草、AI 修改、AI 消费）
meta:
  change_id: "2026-06-01-feature-x"
  title: "变更标题"
  created: "2026-06-01T10:00:00"
  status: draft            # draft | confirmed | in_progress | completed

why:
  problem: "问题陈述"
  motivation: "为什么现在做"

what_changes:
  - id: C1
    description: "变更项描述"
    type: new              # new | modified | removed

capabilities:
  new:
    - name: capability-name
      description: "描述"
  modified:
    - name: existing-capability
      description: "修改描述"

constraints:
  - "约束项 1"

stakeholders:
  - "干系人 1"

risk_areas:
  - capability: capability-name
    risk: "风险描述"
    mitigation: "缓解措施"

non_goals:
  - "明确不做的事"

critical:
  is_critical: false
  risk_assessment:
    safety_critical: false
    financial: false
    cross_system: false

anchoring:
  level: L1                 # L1 | L2 | L3 | L4
  reference_changes: []     # L3 时引用
  anchor_implementations: [] # L4 时引用

success_criteria:
  - "可验证条件 1"
```

**CLI 支持**：

```bash
stdd proposal init          # 从 proposal.md 生成 proposal.yaml（AI 辅助转换）
stdd proposal validate      # 校验 proposal.yaml 字段完整性
stdd proposal show          # 输出 proposal.yaml 的人类可读摘要
```

**与 Human View 的关系**：`proposal.md` 是 Human View——从 proposal.yaml 单向生成，人通过 Gate 1 审阅的依然是 proposal.md。canonical/ 目录对人是透明的。

### E2: agent_spec.yaml 格式定义

**方案**：定义 agent_spec.yaml 作为 Agent 任务验证规格的 Canonical 表达。扩展 STDD 的验证对象从代码产物到 Agent 操作过程。

**格式定义**：

```yaml
# agent_spec.yaml — 单系统 Agent 验证规格
meta:
  task_id: "deploy-staging"
  system: "staging-server"
  preconditions:
    - "SSH 密钥已配置"
    - "Docker 已安装"

steps:
  - id: CP-1
    description: "拉取最新镜像"
    action: "docker pull <image>:latest"
    assertions:
      - type: exit_code
        expected: 0
      - type: stdout_contains
        expected: "Digest:"
        
  - id: CP-2
    description: "重启容器"
    action: "docker compose up -d"
    assertions:
      - type: exit_code
        expected: 0
      - type: http_status
        url: "https://<domain>/health"
        expected: 200

rollback:
  steps:
    - "docker compose down"
    - "docker compose up -d --no-build"   # 用旧镜像
```

**Why YAML 而非 Markdown**：Agent 验证管线需要精确解析检查点（CP）和断言，YAML 可被 CLI 直接解析执行，无需 AI 理解自然语言。

### E3: Spec 锚定法 L1 方法论文档

**方案**：在 VISION.md 第十二章已有完整的四级锚定理论基础上，新增一个独立的 `STDD_ANCHORING.md` 方法论文档，并将 L1 锚定要求注入 Phase 2 的 spec.md skill 指令。

**STDD_ANCHORING.md 结构**：

```markdown
# STDD Spec 锚定法

## 为什么需要锚定
LLM 相同输入不保证相同输出。根因不是 "AI 不稳定"——是 spec 给了 AI 太多自由发挥空间。
当 spec 精确到 "AI 没有发挥空间" 时，不可重复性自然消失。

## 四级锚定

### L1 · 行为锚定（所有 Change 默认要求）
- THEN 用 SHALL 写死所有强制行为
- 每个 Requirement 至少 1 个 Scenario
- 无额外成本

### L2 · 接口锚定
- spec 中附加精确的函数签名 / API 契约 / 数据 schema
- 低额外成本（多写几行）

### L3 · 模式锚定
- spec 中引用参考实现模式（"参照 Change-X 的 TokenSystem 模式"）
- 适用于有成熟模式的重复性工作

### L4 · 基准锚定
- spec 中附一条参考实现代码（Anchor Implementation）
- 适用于关键 Change、安全/金融场景
- 中等成本（人工编写参考代码）

## 流程集成
在 Phase 2 SPEC 中新增 Step 2.4 锚定评估（仅 critical Change）
```

**spec.md skill 指令增强**：

```markdown
### Step 2.4: 锚定评估（V2.7 anchoring）

**执行条件**：proposal 的 Critical 勾选了 "关键变更" 或 risk_assessment 中有任意 true

1. AI 评估 spec 的"自由度"：
   - 是否有 SHALL 未覆盖的行为路径？
   - 是否有"合理但不同"的多种实现可能？
   - 关键决策点是否被锁定？

2. 自由度 > 阈值 → spec 需要补充锚定（建议 L2/L3/L4）
3. 自由度 ≤ 阈值 → 通过，进入 Gate 2
```

### E4: project-index.yaml 格式定义

**方案**：定义项目级结构化索引，记录所有 changes、specs、capabilities、模块映射。这是 V3.0 知识图谱的前置数据基础。

```yaml
# project-index.yaml
project:
  name: "my-project"
  language: python
  stdd_version: "2.7"

changes:
  - id: "2026-05-14-api-rate-limit"
    status: completed
    capabilities: [rate-limiting]
    modules: [middleware/rate_limit.py, app/core/config.py]
  - id: "2026-06-01-user-auth"
    status: in_progress
    phase: 4
    capabilities: [user-auth]

capabilities:
  rate-limiting:
    specs: specs/rate-limiting/spec.md
    modules: [middleware/rate_limit.py]
    changes: [2026-05-14-api-rate-limit]
  user-auth:
    specs: specs/user-auth/spec.md
    modules: [middleware/auth.py]
    changes: [2026-06-01-user-auth]

module_index:
  middleware/rate_limit.py:
    capabilities: [rate-limiting]
    symbols: [TokenBucket, rate_limit_middleware]
  app/core/config.py:
    capabilities: [rate-limiting, user-auth]
    symbols: [RateLimitConfig, AuthConfig]
```

**CLI**：

```bash
stdd index update              # 扫描项目更新 project-index.yaml
stdd index show [capability]   # 查看 capability 关联的 changes/modules
stdd index trace <file>        # 追溯文件关联的需求和 changes
```

### E5: 双轨制文档基础

> 完整理论见 `DUAL_TRACK_DOC_SYSTEM.md`。V2.7 只做基础：canonical/ 目录结构 + `stdd canon generate` CLI 骨架。

**canonical/ 目录结构**：

```
项目根目录/
├── canonical/                    # Canonical Source（AI 消费）
│   ├── proposals/
│   │   └── <change-name>.yaml
│   ├── designs/
│   │   └── <change-name>.yaml
│   └── specs/
│       ├── code/
│       │   └── <capability>.yaml
│       └── agent/
│           └── <task>.yaml
│
├── changes/                      # Human View（人阅读，现有目录）
│   └── <change-name>/
│       ├── proposal.md           # 从 canonical/proposals/<name>.yaml 生成
│       ├── design.md
│       └── specs/
│           └── <capability>/
│               └── spec.md       # 从 canonical/specs/code/<name>.yaml 生成
│
└── .stdd/
    └── templates/
        ├── canonical/            # Canonical 模板（AI 维护）
        │   ├── proposal.yaml
        │   ├── design.yaml
        │   └── spec.yaml
        └── human-view/           # Human View 模板（人定制）
            ├── proposal-brief.md
            ├── design-rationale.md
            └── spec-summary.md
```

**`stdd canon generate` CLI**：

```bash
stdd canon generate <change-name>           # 从 Canonical YAML 生成所有 Human View
stdd canon generate <change-name> --type proposal  # 只生成 proposal-brief.md
stdd canon generate --all                   # 生成所有 change 的 Human View
```

**V2.7 实现方式**：`stdd canon generate` 通过 CLI **调用 AI 完成转换**（读取 YAML → AI 按模板生成 MD），而非自动模板引擎渲染。V3.0 升级为自动引擎。

### 板块 E 设计决策

| 决策 | 选择 | 排除方案及原因 |
|------|------|---------------|
| Canonical 格式 | **YAML**（纯数据，AI 友好） | JSON → 不如 YAML 可读；TOML → 嵌套表达能力弱 |
| 双轨生成方式 | **CLI 调用 AI**（V2.7）→ 自动引擎（V3.0） | 纯模板引擎（Jinja2）→ 无法生成自然语言叙事，输出质量差 |
| canonical/ 目录 | **可选** | 强制 → 小项目不需要，增加认知负担 |
| project-index | 独立 YAML 文件 | 嵌入 .stdd.yaml → 单文件膨胀，职责不清 |
| agent_spec 范围 | **单系统** CP 验证 | 多系统跨系统验证 → TEAM 版专属 |

---

## 【板块 A】锚定落地 + 双轨验证（原 V2.7 板块 A）

### A1: 锚定评估 Phase 2 集成

**方案**：在 Phase 2 SPEC 流程中新增 Step 2.4（锚定评估），仅在 `proposal.critical == true` 或 `risk_assessment` 中有 true 时触发。评估结果纳入 Gate 2 检查项。

**集成流程**：

```
Phase 2 SPEC 流程（增强后）:
  Step 2.1: 读取 proposal → 提取 capabilities
  Step 2.2: 加载匹配经验 → 交叉检查
  Step 2.3: 生成 design.md + specs + test-plan
  Step 2.4: 【新增】锚定评估（条件触发）
    ├─ 检查 proposal.critical 和 risk_assessment
    ├─ 如果非 critical 且无风险 → 跳过，直接进入 Gate 2
    └─ 如果 critical：
        ├─ AI 评估 spec 自由度（未覆盖路径 / 多实现可能 / 决策点锁定度）
        ├─ 计算最低锚定等级需求：
        │   safety_critical=true → 至少 L3
        │   financial=true → 至少 L4
        │   cross_system=true → 至少 L2
        │   默认 critical → 至少 L3
        └─ proposal.anchoring.level ≥ 最低需求 → 通过
           proposal.anchoring.level < 最低需求 → Gate 2 阻塞
  Step 2.5: Gate 2 用户确认（含锚定评估结果）
```

**Gate 2 检查项扩展**（`gates.yaml` 变更）：

```yaml
gates:
  phase2_spec:
    checks:
      - id: design_completeness
        description: "design.md 覆盖所有技术决策"
        blocking: true
      - id: spec_coverage
        description: "每个 capability 有对应 spec，每个 Requirement 有 Scenario"
        blocking: true
      - id: anchoring_assessment       # 【新增】
        description: "critical Change 的锚定等级满足最低要求"
        blocking: true
        condition: "proposal.critical == true"
        rule: "proposal.anchoring.level >= required_level"
```

### A2: 第 12 类失败模式 (l) 锚定缺失

**定义**：

```yaml
failure_mode_l:
  id: l
  name: 锚定缺失 (anchor_missing)
  description: |
    critical Change 的 spec 未达到最低锚定等级要求。
    spec 给了 AI 过多自由发挥空间，导致实现不可重复、质量不可控。
  detection:
    - Phase 2 Gate 2 检查时自动发现
    - Phase 5 VERIFY 时，如果 AI 的实现与 spec 意图偏差 > 阈值 → 回溯标记为可能锚定不足
  severity: high
  auto_detectable: true
  auto_detect_tool: "stdd ci check-anchoring <change-name>"
```

**Phase 5 VERIFY 检查清单新增**：

```markdown
### (l) 锚定缺失检查
- [ ] critical Change 的 proposal.anchoring.level ≥ required_level？
- [ ] 如果 Phase 4 中出现了 3+ 次设计偏离 → 回溯标记：spec 锚定可能不足
- [ ] 如果 pass@1 低但 pass@3 高 → spec 歧义可能需更高级别锚定
```

### A3: Canonical Source 目录标准化

**方案**：将 E5 定义的 canonical/ 目录结构标准化为 STDD 正式目录约定。所有 Canonical 文件集中存放，AI 在 Phase 切换时自动维护。

**标准目录布局**：

```
<项目根>/
├── canonical/                         # Canonical Source（AI 真相源）
│   ├── .canon-index.yaml              # Canonical 文件索引
│   ├── proposals/
│   │   └── <change-id>.yaml
│   ├── designs/
│   │   └── <change-id>.yaml
│   └── specs/
│       ├── code/
│       │   └── <capability>.yaml      # 代码行为 spec
│       └── agent/
│           └── <task-id>.yaml          # Agent 验证 spec
├── specs/                             # 【保留】传统的 Human View spec 目录
│   └── <capability>/
│       └── spec.md
└── changes/                           # 【保留】传统 change 目录
    └── <change-name>/
        ├── proposal.md
        ├── design.md
        └── ...
```

**关键设计**：`canonical/` 和 `changes/` **并行存在**，不是替代关系。canonical/ 存 YAML（AI 消费），changes/ 存 MD（人阅读+Gate 确认）。

### A4: specs/code/ 与 specs/agent/ 分目录

**方案**：在 canonical/specs/ 下区分代码行为验证（code）和 Agent 操作验证（agent）两个子目录。反映 STDD 从"验证代码"到"验证代码 + 验证 Agent 操作"的扩展。

**两种 spec 的差异**：

| 维度 | specs/code/*.yaml | specs/agent/*.yaml |
|------|------------------|-------------------|
| GIVEN | 系统前置状态 | Agent 操作前的世界状态 |
| WHEN | 函数调用 / API 请求 | Agent 执行的操作序列 |
| THEN | 返回值 / 状态变更 | 检查点 (CP) + 断言 |
| 验证方式 | pytest / unittest | CP 断言执行器 |
| TC 映射 | TC-{CAP}-{NNN} | CP-{TASK}-{NN} |
| 引入版本 | V2.0 | V2.7 |

### A5: 单系统 Agent 验证管线

**方案**：基于 agent_spec.yaml（E2）实现单系统 Agent 验证管线——不依赖外部系统，只在单个系统上执行检查点并验证断言。

**管线流程**：

```
agent_spec.yaml
      │
      ├── 1. 读取 spec → 解析 CP 列表
      ├── 2. 对每个 CP：
      │     ├── 执行 action（CLI 命令 / HTTP 请求）
      │     ├── 采集输出（exit_code / stdout / stderr / http_response）
      │     └── 逐条验证 assertions
      ├── 3. 任一 CP 断言失败 → 记录失败原因 + 实际输出
      └── 4. 生成 agent-verification-report.md
```

**CLI**：

```bash
stdd agent verify <task-id>              # 执行 agent_spec 的所有 CP
stdd agent verify <task-id> --cp CP-2    # 只执行指定 CP
stdd agent verify <task-id> --dry-run    # 展示将要执行的操作但不实际执行
```

**关键设计**：CP 执行器只做**断言验证**，不做状态变更的自动回滚。回滚策略由 `agent_spec.yaml` 的 `rollback` 段定义，由用户在确认失败后手动触发或由上层编排系统处理。

### A6: stdd canon verify CLI

**方案**：实现双轨一致性检查 CLI——验证 Canonical YAML 和 Human View MD 之间的源哈希和字段完整性。

**检查项**：

```bash
stdd canon verify <change-name>
```

| 检查 | ID | 描述 | 阻断 |
|------|----|------|:---:|
| 源哈希 | DC-HASH | Human View 头部的 `source_hash` 是否与 Canonical YAML 的 SHA256 一致？ | 是 |
| 字段覆盖 | DC-FIELD | Human View 是否引用了 Canonical 中不存在的字段？ | 是 |
| 生成时间 | DC-TIME | Human View 的 `generated_at` 是否晚于 Canonical 的 `last_modified`？ | 否（警告） |
| 模板版本 | DC-TMPL | Human View 使用的模板版本是否与当前 canonical/ 模板一致？ | 否（警告） |

**输出**：

```
  Canonical YAML  →  Human View MD
  ─────────────────────────────────
  ✅ DC-HASH  源哈希一致
  ✅ DC-FIELD 字段引用完整
  ⚠️ DC-TIME  Human View 可能过时 (Canonical 修改于 2h 前)
  ✅ DC-TMPL  模板版本一致

  结论: 3/4 通过, 0 阻断 — 可安全进入 Gate 2
```

### A7: anchors/ 目录 + L2/L3/L4 锚定支持

**方案**：创建 `anchors/` 目录存放锚定参考物，按锚定等级组织。

**目录结构**：

```
<项目根>/
└── anchors/
    ├── L2-interfaces/                   # L2 接口锚定
    │   └── <change-name>/
    │       └── api-contract.yaml        # 精确的 API 签名 / 数据 schema
    ├── L3-patterns/                     # L3 模式锚定
    │   └── <change-name>/
    │       └── reference-change.md      # 引用的已有 Change 的 spec 摘要
    └── L4-baselines/                    # L4 基准锚定
        └── <change-name>/
            └── anchor-impl.py           # 参考实现代码
```

**Phase 2 流程增强**（spec.md skill）：

```markdown
如果 proposal.anchoring.level >= L2：
  1. 在 anchors/L2-interfaces/<change-name>/ 下创建接口定义文件
  2. 在 spec 的 Scenario 中引用接口定义："THEN 返回值 SHALL 符合 api-contract.yaml 的 Response 定义"

如果 proposal.anchoring.level == L3：
  1. 在 anchors/L3-patterns/<change-name>/ 下创建参考索引
  2. 引用已有 Change 的 spec/design

如果 proposal.anchoring.level == L4：
  1. 在 anchors/L4-baselines/<change-name>/ 下编写参考实现
  2. spec 开头注明 "Anchor Implementation: anchors/L4-baselines/<name>/anchor-impl.py"
```

### A8: 经验库扩展

**方案**：在现有 11 类失败模式基础上新增 2 个经验类别，均在 V2.7 引入。

**新增类别**：

```yaml
# agent_cp_failure — Agent 检查点断言失败
category: agent_cp_failure
label: "(l-aux) Agent CP 失败"
description: |
  Agent 验证管线中任一 CP 的断言未通过。
  常见于：操作后状态与预期不一致、API 返回非预期值、超时。
detection_trigger: "stdd agent verify 输出中有 FAILED 断言"
fix_template: "检查 CP 的 assertions 是否过于严格 / action 是否正确 / 前置条件是否满足"

# spec_ambiguity — Spec 过于模糊导致 AI 方差
category: spec_ambiguity
label: "(l-aux) Spec 歧义"
description: |
  Spec 中存在多个 "合理但不同" 的实现路径，导致 AI 在不同 session 中产生不同结果。
  常见于：THEN 用了非强制性语言（should 而非 SHALL）、缺少边界值定义。
detection_trigger: "pass@1 低但 pass@3 高 → spec 可能有歧义"
fix_template: "将模糊 THEN 改写为 SHALL 声明 + 增加边界 Scenario 覆盖歧义分支"
```

> 注：这两个类别不是独立的失败模式编号，而是 (l) 锚定缺失的辅助子类别，用于经验库的精细化分类。

### 板块 A 设计决策

| 决策 | 选择 | 排除方案及原因 |
|------|------|---------------|
| 锚定评估触发条件 | **仅 critical Change** | 所有 Change → 非 critical 的评估是噪音，浪费 token |
| Gate 2 锚定阻塞 | **硬阻断**（critical + 等级不足） | 软警告 → 锚定是质量底线，不能降级为建议 |
| canon verify 阻断项 | 仅 DC-HASH 和 DC-FIELD 阻断 | 全部阻断 → DC-TIME 和 DC-TMPL 不应阻断 CI |
| Agent 管线回滚 | 仅记录失败，**不回滚** | 自动回滚 → 危险（生产环境误操作），留给上层编排 |
| 经验新类别 | **辅助子类别**（不独立编号） | 独立编号 → 14 类失败模式会分散注意力，保持主编号简洁 |
