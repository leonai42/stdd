# STDD V2.9 白皮书

> **版本：V2.9.3 | 内部使用 | V3.0 公开发布**
>
> 本文档是 STDD (Specification-Driven Test-Driven Development) V2.9 的完整参考。
> 覆盖所有 CLI 命令、六阶段流程、智能门禁、双轨文档、经验库、配置系统和平台适配。
>
> 编写原则：自包含 —— 无需阅读源代码即可查找到任何功能细节。

---

## 目录

- [Part 0: 前置](#part-0-前置)
  - [Ch00 版本声明与文档约定](#ch00-版本声明与文档约定)
  - [Ch01 术语表](#ch01-术语表)
- [Part 1: 总论](#part-1-总论)
  - [Ch02 STDD 是什么](#ch02-stdd-是什么)
  - [Ch03 九大核心原则](#ch03-九大核心原则)
  - [Ch04 六阶段流程总览](#ch04-六阶段流程总览)
- [Part 2: 六阶段详解](#part-2-六阶段详解)
- [Part 3: 关键机制](#part-3-关键机制)
- [Part 4: 质量体系](#part-4-质量体系)
- [Part 5: Spec 锚定法](#part-5-spec-锚定法)
- [Part 6: 核心子系统](#part-6-核心子系统)
- [Part 7: CLI 完整参考](#part-7-cli-完整参考)
- [Part 8: 配置系统](#part-8-配置系统)
- [Part 9: 平台与规范](#part-9-平台与规范)
- [Part 10: 版本演进与未来](#part-10-版本演进与未来)
- [Part 11: 附录](#part-11-附录)

---

## Part 0: 前置

### Ch00 版本声明与文档约定

#### 版本声明

本文档对应 **STDD V2.9.3**。V2.9.x 系列为内部使用版本，V3.0 时将随正式发布对外公开。

白皮书内容以 V2.9.3 的源代码为准。如发现与代码不一致，以代码为准。

#### 目标读者

- **STDD 使用者**：需要查找命令参数、概念定义
- **AI 代理**：需要精确理解 STDD 原理以正确执行流程
- **STDD 开发者**：需要了解系统完整架构和模块关系

#### 阅读约定

| 标记 | 含义 |
|------|------|
| `` `代码` `` | 命令、文件名、字段名、代码片段 |
| **加粗** | 关键概念首次出现 |
| > 引用 | 提示、注意、警告 |

---

### Ch01 术语表

> 按功能领域分组。每词条格式：**中文** (English) — 定义。

#### 核心概念

- **STDD** — Specification-Driven Test-Driven Development，规格驱动的测试驱动开发。
- **Change（变更）** — STDD 的基本工作单元。每次变更创建 `changes/<date>-<name>/` 目录，走完整六阶段流程。
- **Phase（阶段）** — 工作流的六个步骤：UNDERSTAND → SPEC → SLICE → BUILD → VERIFY → DELIVER。
- **Capability（能力）** — 系统的一个独立功能单元。每个 Capability 对应一个 spec 文件。
- **Scenario（场景）** — Spec 的基本单元。格式：GIVEN → WHEN → THEN(SHALL) → AND(≤5条)。
- **TC-ID** — 测试用例标识符。格式 `TC-<CAPABILITY>-<NNN>`，实现 Spec→Test 追溯。
- **Mode（执行模式）** — 三档：lightweight(轻量) / standard(标准) / thorough(彻底)。
- **Task Type（任务类型）** — code / documentation / configuration / data-migration / dependency-upgrade。

#### 双轨文档

- **Canonical YAML** — AI 可消费的 YAML 格式文档，与 Human View MD 构成双轨制。
- **Human View** — 人类阅读的 Markdown 文档，从 Canonical YAML 单向渲染生成。
- **DC-HASH** — 双轨一致性哈希。YAML 的 SHA-256 嵌入 MD 用于验证同步。
- **DC-FIELD** — 双轨字段一致性检查。

#### 门禁与确认

- **Gate（门）** — 三道强制确认点。Gate 1(Phase1结束) / Gate 2(Phase2结束) / Gate 3(Phase5结束)。
- **Guard（门禁）** — 智能编辑门禁。Edit/Write 前自动检查，V2.9.3 四级范围分类。
- **PreToolUse Hook** — Claude Code 的编辑前拦截钩子。exit code 2 时阻止操作。
- **enforce_stdd** — project.yaml 开关。设为 false 时 Guard 不生效。

#### 质量系统

- **失败模式 (Failure Mode)** — 12 类 AI 编程常见失败(a-l)，Phase 5 逐类检查。
- **pass@k** — k 次重复测试"至少一次通过"的概率，用于检测 Spec 歧义。
- **Plankton** — 三级自动修复系统。L1 静默修复 / L2 建议 / L3 报告。
- **复杂度评分 (Complexity Score)** — 0-17 分评估，6 维度，据此推荐执行模式。

#### 经验与上下文

- **经验库 (Experience Library)** — 5 态生命周期(discovered→verified→deposited→shared/merged→retired)的 AI 编程经验管理系统。
- **Phase Context** — 跨 Session 恢复文件，记录关键决策和当前状态。
- **Resume Context** — .stdd.yaml 中的恢复字段。
- **State Freshness** — 比较 git HEAD 判断恢复状态是否有效。
- **Hook（生命周期钩子）** — SessionStart / PreCompact / Stop 三个自动触发脚本。

#### 其他

- **Long-Range Mode（长程模式）** — Gate 2 后可选，Phase 3-5 预授权自动执行。
- **Batch（批次）** — 轻量变更容器，多微修复归入 `changes/_batch/<id>/`。
- **Skill（技能）** — 引导 AI 执行流程的 Markdown 文件，6 个 Phase Skill + _shared/ 共享片段。
- **TDD** — Test-Driven Development。Phase 4 核心：RED → GREEN → REFACTOR。
- **Design Adjustment** — Phase 4 偏离原始设计时记录。minor 自动 / major 暂停。

---

## Part 1: 总论

### Ch02 STDD 是什么

#### 定义

STDD = **Specification-Driven Test-Driven Development**。

一套 **AI 编程流程管控框架**。不是编程语言、测试框架或 IDE 插件 —— 是一套通过 CLI 工具 + Skill 指令 + 智能门禁确保 AI 代码修改"有目标、有约束、有验证"的流程标准。

#### 三个核心问题

1. **AI 输出不可靠**：代码看似正确，行为不符预期 → Spec → 实现 → 验证闭环
2. **AI 操作缺乏追溯**：不知道为什么改、改了什么 → Change 生命周期完整追溯
3. **流程依赖用户技能**：不同 Session 行为不一致 → Skill 固化 + Guard 强制执行

#### 与其他方法论

| 方法论 | 核心 | STDD 关系 |
|--------|------|----------|
| TDD | 先写测试再写代码 | Phase 4 就是 RED→GREEN→REFACTOR |
| BDD | GIVEN/WHEN/THEN 描述行为 | Spec Scenario 直接采用 BDD 格式 |
| DDD | 业务领域建模 | Capability 对应 Bounded Context |

STDD 独特之处：**将三者整合为 AI 代理的原生操作系统，而非人类开发者的外部文档**。

#### 设计哲学

```
定义(Specify) → 执行(Execute) → 验证(Verify) → 学习(Learn)
     ↑                                              ↓
     └─────────── 经验反馈 ←─────────────────────────┘
```

---

### Ch03 九大核心原则

1. **Spec-First（规格先行）**：先写 Spec，再写代码。`❌ 需求→代码  ✅ 需求→Spec→确认→代码`
2. **TDD Execution（红绿重构）**：每切片 RED → GREEN → REFACTOR，不可跳过
3. **Traceable Adjustments（可追溯调整）**：任何设计偏离必须记录到 pending-adjustments.yaml
4. **User-Confirmation-Driven（Gate 确认驱动）**：三道 Gate 不可跳过，确认权在用户
5. **Template-First（模板先行）**：所有产出物从 13 个模板开始，结构一致
6. **Vertical Slicing（垂直切片）**：按功能切片（端到端增量），不按层级切片
7. **Test Coverage Mandate（强制测试覆盖）**：每 Scenario 必须有对应测试
8. **Behavior-Not-Implementation**：测试"做什么"不测试"怎么做"
9. **Self-Learning（经验自学习）**：从失败中提取经验，反哺后续 Spec

---

### Ch04 六阶段流程总览

#### 状态机

```
UNDERSTAND(1) → SPEC(2) → SLICE(3) → BUILD(4) → VERIFY(5) → DELIVER(6)
     ↓ Gate1       ↓ Gate2                          ↓ Gate3
  复杂度评分    模式选择                          最终确认
```

#### 各阶段产出物

| Phase | 名称 | 产出物 | Gate |
|-------|------|--------|------|
| 1 | UNDERSTAND | proposal.md | Gate 1 |
| 2 | SPEC | design.md, spec.yaml, agent_spec.yaml, test-plan.md | Gate 2 |
| 3 | SLICE | slices.md, tasks.md | — |
| 4 | BUILD | 代码, pending-adjustments.yaml | — |
| 5 | VERIFY | test-report.md, design-adjustments.yaml | Gate 3 |
| 6 | DELIVER | archive/, 合并 specs/ | — |

#### 三档模式

| 模式 | 评分 | Phase2 | Phase3 | Phase4 | Phase5 | Phase6 |
|------|------|--------|--------|--------|--------|--------|
| 轻量 | 0-3 | 简化 | 跳过 | 简化TDD | 1代理+5模式 | 批次追加 |
| 标准 | 4-7 | 完整 | 智能切片 | 完整TDD | 3代理+12模式 | 完整归档 |
| 彻底 | 8+ | 完整+高级 | 并行化 | TDD+pass@k | 3代理+安全+性能 | 完整+发行说明 |

---

---

## Part 2: 六阶段详解

### Ch05 Phase 1: UNDERSTAND（需求理解）

#### 目标

将模糊需求转化为清晰、可验证的变更提案（proposal）。

#### 执行流程（6 步）

**Step 1: 问题探索**
- 理解用户描述的问题或需求
- 明确范围边界：做什么、不做什么
- 识别干系人和约束条件

**Step 2: 读取模板**
- 读取 `.stdd/templates/canonical/proposal.yaml`（V2.9.2 YAML-First）

**Step 3: 起草 proposal.yaml**
- 按 Canonical proposal.yaml 模板填写：
  - `meta`: change_id, title, created, status
  - `why`: problem（要解决的问题）
  - `what_changes`: 变更项列表
  - `capabilities`: new + modified 能力
  - `constraints`: 技术/时间/资源约束
  - `stakeholders`: 干系人
  - `risk_areas`: 风险区域
  - `non_goals`: 明确不做的事
  - `success_criteria`: 可验证的成功标准

**Step 4: 自动审查**
- 检查 proposal 完整性和一致性
- 检查 success_criteria 是否可验证

**Step 5: 复杂度评分 → 模式推荐**
- 6 维度评分（详见 Ch13），0-17 分
- 推荐模式：0-3=轻量 / 4-7=标准 / 8+=彻底
- 用户可在 Gate 2 覆盖推荐

**Step 6: Gate 1 确认**
- 向用户展示 proposal 摘要
- 确认内容：范围、边界、成功标准
- 用户响应：确认 / 反馈修改 / 退回 / 暂停

#### 产出物

- `proposal.md`（或 proposal.yaml）+ `.stdd.yaml` 状态更新（understand → completed）

---

### Ch06 Phase 2: SPEC（规格设计）

#### 目标

将 proposal 转化为可测试的行为规格和验证规格。

#### 执行流程

**Step 1: CLI 结构化提取**
- `stdd extract-proposal` 提取 proposal 结构化数据

**Step 2: 经验加载 + 交叉检查**
- `stdd experience list --language <lang> --format json`
- 过滤 lifecycle_state ≥ verified
- 匹配 pattern/root_cause 与当前 capabilities
- 加载最多 10 条匹配经验

**Step 3: 技术设计 (design.md)**
- Context：当前系统状态、约束
- Decisions：关键技术决策（含备选方案和选择理由）
- Architecture：模块划分、数据流
- Risks/Trade-offs：风险与权衡

**Step 4: 生成规格（Canonical YAML + Human View）**

| 子步骤 | Coding 任务 | Non-Coding 任务 |
|--------|-----------|---------------|
| 4a | 读取 spec.yaml + agent_spec.yaml 模板 | 读取 agent_spec.yaml 模板 |
| 4b | 为每 Capability 生成 spec.yaml（Scenario: GIVEN/WHEN/THEN/AND） | 跳过 |
| 4c | 生成 agent_spec.yaml（CP 检查点对应 Scenario） | 生成 agent_spec.yaml（CP 检查点即规格本身） |
| 4d | 渲染 Human View spec.md | 渲染 Human View |

**Step 4.5: 锚定评估**
- 评估每个 Requirement 的锚定等级（L1-L4，详见 Ch27-28）
- 关键/安全变更锚定不足时警告

**Step 5: 测试计划 (test-plan.md)**
- 测试策略、TC 用例清单
- TC-ID 格式：`TC-<CAPABILITY>-<NNN>`
- 确保 TC 数 ≥ Scenario 数

**Step 6: Gate 2 + 模式选择**
- 向用户展示 design.md + spec 摘要
- 模式选择：轻量/标准/彻底（用户确认或覆盖推荐）
- 可选：启用长程模式（Phase 3-5 自动执行）
- 确认后锁定 mode，后续 Phase 不可更改

#### 产出物

`design.md`, `spec.yaml`(coding), `agent_spec.yaml`, `test-plan.md`, `.stdd.yaml` 更新

---

### Ch07 Phase 3: SLICE（切片规划）

#### 目标

将 spec 拆分为可独立实现的开发切片，确定执行顺序。

#### V2.9.2 Canonical-First 读取

1. 优先读取 `spec.yaml`（Canonical），回退读取 `spec.md`（Human View）
2. 读取 `agent_spec.yaml`（验证规格）
3. 读取 `test-plan.md`

#### 5 步切片分析

1. **依赖图分析**：`stdd dependency-graph --format json`，识别依赖关系
2. **风险评估**：每切片标注风险等级 (高/中/低)
3. **工作量评估**：每切片标注工作量 (大/中/小)
4. **分组**：按功能内聚性分组，识别可并行的切片（parallel_group）
5. **拓扑排序**：依赖图 → 执行顺序，P0 优先

#### 三档模式差异

| 模式 | SLICE 行为 |
|------|----------|
| 轻量 | **跳过本 Phase**：1 个隐式切片，直接进 Phase 4 |
| 标准 | 智能切片：5 步分析 |
| 彻底 | 标准 + 并行化识别 + pass@k=3 配置 |

#### 产出物

`slices.md`（切片执行计划）、`tasks.md`（任务清单）、`.stdd.yaml` 更新

---

### Ch08 Phase 4: BUILD（TDD 实现）

#### 目标

逐切片实现并通过测试。

#### Step -1: 上下文预算检查

- 估算当前上下文使用量
- 如超过 80%，提示用户或自动压缩

#### Step 0: 加载资源

1. 读取 `project.yaml` → 获取语言
2. 加载语言标准 `.stdd/standards/<lang>.md`
3. 加载项目规则 `.stdd/rules/<lang>/*.md`
4. 加载 phase-context.md（如有）
5. 加载经验库匹配条目（最多 10 条）
6. 生成代码结构 delta：`stdd structure delta <change>`

#### Step 1: 逐切片 TDD 循环

```
每切片循环：
  RED    → 写失败测试（基于 spec Scenario 的 THEN）
  GREEN  → 写最小实现使测试通过
  REFACTOR → 重构优化
```

#### Step 1.4: 切片验证

每切片完成后验证：
- TC 覆盖率 100%（所有 Scenario 有对应测试）
- 产物检查（文件存在、格式正确）
- 所有测试通过

#### Step 1.5: 并行切片合并

并行组切片全部完成后，合并验证：无冲突、无回归。

#### 设计偏离处理

| 级别 | 条件 | 处理 |
|------|------|------|
| minor | 不影响 spec Scenario，仅实现细节调整 | 自动记录到 pending-adjustments.yaml |
| major | 改变了 spec Scenario 的行为 | 暂停 → 记录 → 询问用户 → 可能需要更新 spec |

#### 三档模式差异

| 模式 | BUILD 行为 |
|------|----------|
| 轻量 | 1-2 个聚焦测试，跳过 REFACTOR |
| 标准 | 完整 RED→GREEN→REFACTOR |
| 彻底 | 标准 + pass@k 验证 |

#### 产出物

代码文件、`pending-adjustments.yaml`、`.stdd.yaml` 更新

---

### Ch09 Phase 5: VERIFY（质量验证）

#### 目标

全面验证代码质量和 spec 符合性。

#### 执行流程

**Step -1: 上下文预算检查**

**Step 0: 多代理并行审查**

| 代理 | 职责 | 模型 |
|------|------|------|
| security-reviewer | 安全漏洞检测（注入、路径遍历、认证） | Opus |
| perf-analyzer | 性能瓶颈识别 | Sonnet |
| compat-checker | 兼容性检查 | Sonnet |

轻量模式仅 1 个代理。

**Step 1: 测试执行**

按 `.stdd/config.d/quality.yaml` 配置顺序执行：

1. `pytest` — 单元测试 + 覆盖率（默认目标 80%）
2. `coverage` — 覆盖率报告
3. `ruff check` — Lint 检查
4. `mypy` — 类型检查（Python）
5. 多版本测试（如 Python 3.10/3.11/3.12）
6. E2E 测试（如启用）

**Step 2: Diff 审查**

`stdd diff` — 检测 Spec↔Test 覆盖差异。

**Step 3: 十二类失败模式检查**

逐类检查（详见 Ch21），轻量模式 5 项核心，标准/彻底全部 12 项。

**Step 4: 设计调整汇总**

1. 读取 Phase 3-4 记录的 `pending-adjustments.yaml`
2. 按 Canonical 模板生成 `design-adjustments.yaml`
3. 渲染 `design-adjustments.md`（Human View）
4. 如有 `requires_re_spec` → 标记为下轮 proposal 输入（闭环）

**Step 5: Gate 3 确认**

向用户展示 test-report.md + design-adjustments.md。

#### 迭代控制

| 模式 | 最大迭代 | 行为 |
|------|---------|------|
| 轻量 | 3 | 超限后报告 |
| 标准 | 5 | 超限后报告 |
| 彻底 | 10 | 超限后报告 |

#### 产出物

`test-report.md`, `design-adjustments.yaml/.md`, `.stdd.yaml` 更新

---

### Ch10 Phase 6: DELIVER（交付）

#### 目标

归档 change、合并 specs、更新文档。

#### 执行步骤

1. **归档**：`stdd archive <change> --yes`
   - 移动 change 到 `archive/`
   - 合并 specs 到项目级 `specs/`（除非 `--skip-specs`）

2. **Canonical YAML 合并**：
   - 合并 `proposal.yaml` → `canonical/proposals/`
   - 合并 `agent_spec.yaml` → `canonical/specs/agent/`
   - `stdd canon verify <change>` 验证双轨一致性
   - 更新 `.canon-index.yaml`

3. **代码结构合并**：`stdd structure merge <change>`

4. **Git 提交 + 标签**：版本标签（如有配置）

#### 三档模式差异

| 模式 | DELIVER 行为 |
|------|------------|
| 轻量 | 批次追加（不独立归档）|
| 标准 | 完整归档 + specs 合并 |
| 彻底 | 标准 + 发行说明 |

#### 产出物

`archive/<change>/`、合并后的 `specs/`、更新的 `canonical/`

---

## Part 3: 关键机制

### Ch11 三道强制确认门

#### Gate 位置与确认内容

| Gate | 时机 | 确认内容 |
|------|------|---------|
| Gate 1 | Phase 1 结束 | proposal.md：范围、边界、成功标准 |
| Gate 2 | Phase 2 结束 | design.md + spec + test-plan：核心技术决策 |
| Gate 3 | Phase 5 结束 | test-report.md + design-adjustments.md：质量最终审查 |

#### 三种确认通道（等价，写入同一 confirmed_at 时间戳）

| 通道 | 方式 |
|------|------|
| **dialog** | AI 打印确认提示，用户文本回复 |
| **file_token** | 在 change 目录创建 `GATE<N>_APPROVED` 空文件 |
| **cli** | `stdd gate approve --gate <N> [name]` |

#### 规则

- Gate 顺序强制：Gate 2 必须在 Gate 1 之后
- 幂等：重复确认返回已有时间戳
- 不可跳过

---

### Ch12 三档执行模式

#### 完整对比表

| 维度 | 轻量 (0-3分) | 标准 (4-7分) | 彻底 (8+分) |
|------|------------|------------|-----------|
| Phase 2 SPEC | 跳过 design/test-plan/anchoring | 完整 spec | 完整 + 置信度标签 |
| Phase 3 SLICE | 跳过（1 隐式切片） | 智能切片 | 切片 + 并行化 |
| Phase 4 BUILD | 1-2 聚焦测试，跳过 REFACTOR | 完整 RED→GREEN→REFACTOR | 完整 + pass@k |
| Phase 5 VERIFY | 1 审查代理，5 失败模式 | 3 代理，12 失败模式 | 3 代理 + 安全/性能子代理 |
| Phase 6 DELIVER | 批次追加 | 完整归档 | 完整 + 发行说明 |
| **TDD 基线** | **必须 RED→GREEN** | **必须 RED→GREEN** | **必须 RED→GREEN** |

#### 模式选择流程

```
Phase 1 复杂度评分 → 推荐模式
         ↓
Phase 2 Gate 2 → 用户确认或覆盖
         ↓
Phase 3+ → 锁定，不可更改
```

#### task_type 支持

| task_type | SPEC 策略 | VERIFY 策略 |
|-----------|---------|-----------|
| `code` | spec.yaml + agent_spec.yaml | pytest + coverage + lint |
| `documentation` | agent_spec.yaml（CP 即规格） | 内容检查 + 交叉引用 |
| `configuration` | agent_spec.yaml | 配置有效性验证 |
| `data-migration` | agent_spec.yaml | 数据完整性检查 |
| `dependency-upgrade` | agent_spec.yaml | 兼容性测试 |

---

### Ch13 复杂度评分模型

#### 6 个评分维度（0-17 分）

| 维度 | 权重 | 低(0) | 中(1) | 高(2-3) |
|------|------|-------|-------|--------|
| 影响范围 | 3 | 单文件 | 多文件同模块 | 跨模块/系统 |
| 技术难度 | 3 | 简单CRUD | 算法/并发 | 分布式/安全 |
| 测试复杂度 | 3 | 单元测试 | 集成测试 | E2E+多版本 |
| 依赖数量 | 3 | 0-1 | 2-4 | 5+ |
| 风险等级 | 3 | 低 | 中 | 高/关键 |
| 文档需求 | 2 | 仅代码注释 | 需更新文档 | 新文档体系 |

#### 阈值

| 总分 | 模式 | 说明 |
|------|------|------|
| 0-3 | 轻量 | bug 修复、小调整 |
| 4-7 | 标准 | 功能增强、中等重构 |
| 8-17 | 彻底 | 新模块、架构变更、安全关键 |

分数置信度 (`score_confidence`)：preliminary（初步）/ confirmed（已确认）。

---

### Ch14 设计调整追溯

#### 偏离分类

| 级别 | 定义 | 处理 |
|------|------|------|
| **minor** | 实现细节调整，不影响 spec Scenario | 自动记录 → 继续 |
| **major** | 改变了 spec 行为、接口或数据结构 | 记录 → 暂停 → 用户确认 |

#### 文件生命周期

```
Phase 4: pending-adjustments.yaml  ← 持续记录（每切片）
              ↓
Phase 5: design-adjustments.yaml   ← 汇总 + 分类
              ↓
         design-adjustments.md     ← 人类阅读版
```

---

### Ch15 双向追溯链

#### Spec → TC → Test → Code 四层追溯

```
Spec Scenario "用户登录成功"
  → TC-AUTH-001 登录成功
    → test_login_success() @ tests/test_auth.py:45
      → src/auth/login.py:login()
```

#### 关键命令

- `stdd trace <tc-id>` — 追踪 TC-ID 的四层链路
- `stdd diff [name]` — Spec↔Test↔Code 覆盖差异表

#### .stdd.yaml traceability 字段

```yaml
traceability:
  spec_scenarios: 8    # Spec Scenario 总数
  tc_cases: 8          # TC-ID 总数
  test_functions: 8    # 测试函数总数
```

---

### Ch16 长程模式

#### 启用条件

- Gate 2 之后可选
- `.stdd.yaml` 中 `long_range.enabled: true`
- 对 Phase 3-5 进行预授权

#### 预授权范围（来自 long_range.yaml）

| 操作类别 | 权限 | 说明 |
|---------|------|------|
| directory | allow | 创建/删除目录 |
| file_write | allow | 写入文件 |
| file_read | allow | 读取文件 |
| command_exec | allow | 执行命令 |
| script_exec | allow | 执行脚本 |
| network | allow | 网络访问 |
| git_readonly | allow | Git 只读操作 |

#### 降级触发

| 条件 | 阈值 |
|------|------|
| 连续失败 | 3 次 |
| 通过率 | < 95% |
| 安全检测 | 触发 |

降级后自动切换为普通模式，等待用户确认。

#### Gate 3 保持强制

长程模式下 Gate 3 仍然强制 —— 最终交付前必须用户确认。

---

### Ch17 批次目录管理

#### 问题

轻量模式下每个微修复一个 change 目录会导致目录爆炸。

#### 三种策略

| 策略 | 命名 | 示例 | 适用 |
|------|------|------|------|
| `monthly`（默认） | YYYY-MM-DD | 2026-06-06 | 日常使用 |
| `weekly` | YYYY-Www-MMDD | 2026-W23-0606 | 周迭代 |
| `count_based` | batch-NNN | batch-001 | 无时间关联 |

#### 目录结构

```
changes/_batch/
  <batch-id>/
    .stdd.yaml          # batch_id, batch_type, items, closed_at
    items/              # 微变更项
    archive-summary.md  # 闭合时生成
```

#### 反碰撞

同日多次 open → `YYYY-MM-DD-HHMM` 后缀

#### 配置

```yaml
# lite.yaml
batch:
  strategy: monthly
  max_items: 20
```

---

### Ch18 上下文工程

#### phase-context.md

- 每 Phase 结束时 AI 更新
- 结构：Phase 1-5 已完成章节 + 当前 Phase 章节
- 内容：关键决策、用户关注点、已知陷阱、下一步
- 长度上限：~200 行（上下文 5% 以内）

#### 上下文预算检查

- Phase 4/5 的 Step -1 执行
- 估算当前上下文使用量
- 超过 80% → 提示压缩或手动清理

#### 跨 Session 恢复

1 次读取 `phase-context.md` → 结合 `stdd state --resume --compact` → 完全恢复上下文

#### 状态新鲜度

`stdd state --resume` 自动比较：
- `.stdd.yaml` 中 `state_freshness.git_head`
- 当前 `git rev-parse --short HEAD`

不一致时输出 `STALE` 警告。

---

### Ch19 生命周期 Hooks

#### 三个 Hook

| Hook | 触发时机 | 脚本 | 行为 |
|------|---------|------|------|
| **SessionStart** | Session 启动 | `session-start.py` | 扫描 changes/，打印 active change 状态行 |
| **PreCompact** | Claude Code 上下文压缩前 | `pre-compact.py` | 保存 `.stdd.yaml` 的 last_modified 时间戳 |
| **Stop** | Session 结束 | `session-end.py` | 报告经验库统计，建议 `stdd experience curate` |

#### 安装

```bash
stdd hooks install --force    # 写入脚本 + 配置 settings.local.json
stdd hooks status              # 查看已安装 Hook
stdd hooks uninstall           # 移除 Hook 配置
```

#### Claude Code 配置

```json
{
  "hooks": {
    "SessionStart": "python .stdd/hooks/session-start.py",
    "PreCompact": "python .stdd/hooks/pre-compact.py",
    "Stop": "python .stdd/hooks/session-end.py"
  }
}
```

---

### Ch20 项目级智能门禁

#### 三层架构

| 层 | 机制 | 作用 |
|----|------|------|
| Layer 1 | AGENTS.md / STDD.md 指令注入 | AI 行为约束（软） |
| Layer 2 | PreToolUse Hook | 编辑前自动检查（硬） |
| Layer 3 | `stdd guard` CLI | 手动检查 + 状态查询 |

#### V2.9.3 智能范围分类器

不再只是 allow/block，而是分析变更范围给出智能建议。

**四级分类：**

| 级别 | 关键词信号 | Score | 行为 |
|------|----------|-------|------|
| micro | 修复, fix, bug, typo... | <3 | 建议 batch |
| small | 优化, 调整, UI... | 3-9 | batch OK |
| medium | 重构, 模块, 数据处理... | 10-19 | batch 警告 |
| large | 重写, 架构, API, 引擎... | ≥20 | batch 拒绝，要求 full STDD |

**Batch 硬限制：** 文件数 > 5 警告，> 10 阻止；打开 > 2 小时警告。

#### Guard 操作

| 操作 | 命令 | 说明 |
|------|------|------|
| check | `stdd guard check --platform claude-code` | 退出码 0=允许 2=阻止 |
| status | `stdd guard status` | 显示 enforce、scope、recommended mode |
| init | `stdd guard init` | 部署 PreToolUse Hook |
| disable | `stdd guard disable` | 临时移除 Hook |
| enable | `stdd guard enable` | 重新启用（= init） |

#### 配置

```yaml
# project.yaml
enforce_stdd: true     # 门禁开关
allow_bypass: false    # 是否允许绕过
```

---

> **Slice 2 (Part 2-3) 完成。** 下一 Slice：Part 4(质量体系) + Part 5(锚定法) + Part 6(核心子系统)

---

## Part 4: 质量体系

### Ch21 十二类失败模式

Phase 5 Step 3 中逐类检查。每类有：名称、定义、检测触发条件、典型示例、修复模板。

| ID | 名称 | 定义 | 检测触发 |
|----|------|------|---------|
| (a) | **幻觉动作** | 引用不存在的文件路径、环境变量、函数名、库 API | grep 找不到引用的路径/变量 |
| (b) | **范围蔓延** | 修改了计划外的文件 | git diff --stat 超出声明文件 |
| (c) | **级联错误** | 静默吞掉异常、空数组掩盖错误 | 裸 `except Exception`、空列表默认值 |
| (d) | **上下文丢失** | 实现与 proposal/design/spec 矛盾 | 交叉对比产出的代码 vs spec |
| (e) | **工具误用** | 选错工具或参数 | 命令语法错误、工具版本不匹配 |
| (f) | **运行时行为偏差** | 静态结构正确但动态行为错误 | 测试覆盖率够但 E2E 失败 |
| (g) | **管道断裂** | 多步转换缺失中间步骤 | 数据流不完整 |
| (h) | **内容质量偏差** | 数据不一致、长度溢出、缺少引用 | 输出格式不符合 spec |
| (i) | **指令衰减** | AI 未能执行 prompt 中明确给出的指令 | 对比 prompt 指令 vs 实际产出 |
| (j) | **覆盖真空** | Capability 的测试覆盖率为零 | coverage report 显示 0% |
| (k) | **契约断层** | 跨 Capability 的接口字段名/类型不一致 | 对比 API 定义 vs 实际调用 |
| (l) | **锚定不足** | 关键/安全变更的锚定等级不够 | 检查 anchoring 评估结果 |

#### 轻量模式子集

轻量模式仅检查核心 5 项：(a)(b)(c)(e)(f)。

---

### Ch22 pass@k 统计验证

#### 原理

同一测试运行 k 次，"至少一次通过"的概率。

```
pass@1 = 0.3  → 单次通过率 30%
pass@k = 0.95 → 跑 k 次后 95% 概率至少通过一次
```

**解读：** pass@1 低 + pass@k 高 = **Spec 不够精确**，AI 在"猜测"正确答案。

#### 配置

```yaml
# quality.yaml
pass@k:
  enabled: true
  k_values: [1, 3]     # 标准 k=1, 彻底 k=3
  threshold: 0.8
```

#### 各模式 k 值

| 模式 | k 值 | 说明 |
|------|------|------|
| 轻量 | 跳过 | |
| 标准 | k=1 | 单次确认 |
| 彻底 | k=3 | pass@k 歧义检测 |

---

### Ch23 Plankton 多级自动修复

#### 三级体系

| 级别 | 名称 | 行为 | 触发 |
|------|------|------|------|
| **L1** | 静默修复 | `ruff format .` + `ruff check --fix .` + `isort .` | Phase 5 自动 |
| **L2** | 建议 | 扫描 Python 文件找：缺少类型注解、裸 `except Exception`、async def 中缺 CancelledError 处理 | 手动或自动 |
| **L3** | 报告 | 提示手动运行 bandit/pylint/mypy，不自动执行 | 手动 |

#### CLI

```bash
stdd fix --level 1    # 静默自动修复
stdd fix --level 2    # 建议模式（最多 20 条）
stdd fix --level 3    # 报告模式
```

---

### Ch24 Agent 验证管线

#### 四个子代理

| 代理 | 职责 | 默认模型 |
|------|------|---------|
| security-reviewer | 安全漏洞（注入、路径遍历、认证、CVE） | Opus |
| perf-analyzer | 性能瓶颈（N+1 查询、内存泄漏、阻塞 I/O） | Sonnet |
| compat-checker | 兼容性（API 变更、依赖版本、平台差异） | Sonnet |
| planner | 计划审查（切片顺序、风险、资源） | Opus |

#### Checkpoint (CP) 系统

agent_spec.yaml 中定义检查点：

```yaml
steps:
  - id: CP-1
    description: "验证用户登录流程"
    action: "pytest tests/test_auth.py -v"
    assertions:
      - type: "exit_code"
        expect: 0
      - type: "stdout_contains"
        expect: "test_login_success PASSED"
```

#### CLI

```bash
stdd agent verify [task] --cp CP-1    # 执行特定检查点
stdd agent verify [task]              # 执行全部检查点
```

---

### Ch25 CI/CD 集成

#### 命令树

```
stdd ci
  ├── init                          # 生成所有 CI 配置文件
  ├── generate <target>             # 生成单个配置
  │   ├── workflow                  # GitHub Actions workflow
  │   ├── pre-commit                # .pre-commit-config.yaml
  │   └── pr-template               # PR 评论模板
  ├── check-failures [name]         # 全量失败模式检查
  ├── check-scope [name]            # 范围蔓延检查 (b)
  ├── check-coverage [name]         # 覆盖真空检查 (j)
  └── check-contracts [name]        # 契约断层检查 (k)
```

#### 生成的 GitHub Actions Workflow

- 触发：push / PR 到 main
- Steps：pytest + coverage + ruff + mypy
- 失败模式检查全部执行
- PR 评论自动输出结果

---

## Part 5: Spec 锚定法

### Ch26 锚定法总论

#### 问题

LLM 的非确定性来自 Spec 中的歧义。Spec 越模糊，AI 的"自由发挥"空间越大，输出越不可预测。

#### 方案

通过锚定（Anchoring）约束 Spec，消除歧义来源：**用具体替代抽象，用示例替代描述，用代码替代伪代码。**

#### 反模式

| 反模式 | 示例 | 为什么错 |
|--------|------|---------|
| 过度锚定 | 连变量名都规定 | 过度约束，失去灵活性 |
| 不足锚定 | "处理用户输入" | 太模糊，"处理"有无数种实现 |
| 形式化锚定 | 照抄 RFC 但 Scenario 空洞 | 徒有形式，无法验证 |

---

### Ch27 L1 行为锚定

#### 规则

- THEN 中 **SHALL**（大写）标注强制行为
- 每个 Requirement ≥ 1 Scenario
- 所有边界条件必须覆盖

#### 适用

**所有变更的默认要求**。L1 是基线，不满足 L1 的 Spec 不能通过 Gate 2。

#### 示例

```
❌ Requirement: 系统应正确处理登录
✅ Requirement: 登录成功时系统 SHALL 返回 JWT access token (15min 有效)
   + Scenario: 用户名密码正确
   + Scenario: 用户名不存在
   + Scenario: 密码错误
   + Scenario: 账户被锁定
```

---

### Ch28 L2-L4 高级锚定

#### L2 接口锚定

定义精确的函数签名、API 契约、数据模式。

```yaml
# spec.yaml 中
interface:
  function: "login(username: str, password: str) -> AuthResult"
  api: "POST /api/v1/auth/login"
  schema: "AuthResult { access_token: str, refresh_token: str, expires_in: int }"
```

#### L3 模式锚定

引用已验证的实现模式（如"使用 Repository 模式"），附参考实现链接。

#### L4 基线锚定

提供参考实现代码（baseline implementation），AI 以此为起点修改。

#### 适用性标准

| 变更类型 | 建议锚定等级 |
|---------|-----------|
| 一般功能 | L1 |
| 跨系统接口 | L1 + L2 |
| 安全关键 | L1 + L3 |
| 金融/合规 | L1 + L4 |

---

## Part 6: 核心子系统

### Ch29 双轨制文档体系

#### 设计

| 轨道 | 格式 | 消费者 | 角色 |
|------|------|--------|------|
| **Canonical** | YAML | AI 代理 | 精确消费的数据源 |
| **Human View** | Markdown | 人类 | 可读的渲染输出 |

#### 八项核心规则

1. Canonical 是唯一数据源（Single Source of Truth）
2. Human View 从 Canonical **单向**生成（不可逆）
3. YAML 变更后，MD 必须重新生成
4. DC-HASH 嵌入 MD 用于验证同步
5. canonical/ 目录结构是标准化的
6. `.canon-index.yaml` 维护文件索引
7. `stdd canon verify` 自动检测不一致
8. V2.9.2：YAML-First（YAML 先于 MD 创建）

#### 文件角色分类

| 角色 | 标记 | 含义 | 示例 |
|------|------|------|------|
| Y | 可被 AI 精确消费 | Canonical YAML | `proposal.yaml` |
| H | 人类可读 | Human View MD | `proposal.md` |
| F | 功能文件 | 模板/配置 | `.stdd/templates/` |
| T | 临时 | 中间产物 | `pending-adjustments.yaml` |
| C | 累积 | 跨 Change 累加 | `.canon-index.yaml` |
| L | 生命周期 | 状态/进度 | `.stdd.yaml` |

---

### Ch30 Canonical YAML 格式规范

Canonical YAML 共 5 个核心 schema + 1 个索引文件，位于 `.stdd/templates/canonical/`。

#### 1. proposal.yaml — 变更提案

```yaml
meta: {change_id, title, created, status, version}
why: {problem}                    # 要解决的问题
what_changes: [{description}]     # 变更项列表
capabilities:
  new: [{name, description}]
  modified: [{name, description}]
constraints: []                   # 技术/时间/资源约束
stakeholders: []                  # 干系人
risk_areas: []                    # 风险区域
non_goals: []                     # 明确不做什么
critical: []                      # 关键依赖/风险
anchoring: {level, justification}
success_criteria: []              # 可验证标准
```

#### 2. spec.yaml — 行为规格（Coding 任务）

```yaml
meta: {capability, change_id, created, confidence: high|medium|low}
requirements:
  - id: REQ-XXX
    description: ""               # 一句话描述
    scenarios:
      - id: SC-XXX
        confidence: high|medium|low
        evidence: ""              # 引用 proposal 段落
        given: ""
        when: ""
        then: ""                  # 包含 SHALL
        and: []                   # ≤5 条
```

#### 3. agent_spec.yaml — Agent 验证规格（所有任务）

```yaml
meta: {task_id, change_id, created, task_type, system, description}
preconditions: []
steps:
  - id: CP-XX
    description: ""
    action: ""                    # shell 命令
    assertions:
      - type: exit_code|stdout_contains|stderr_contains|file_exists
              |http_status|yaml_valid|link_alive|schema_valid|diff_empty
        expect: ...
```

#### 4. pending-adjustments.yaml — 设计偏离记录（Phase 4）

```yaml
meta: {change_id, updated_at}
adjustments:
  - id: ADJ-XXX
    original: ""                  # 原始设计引用
    actual: ""                    # 实际实现
    reason: ""                    # 偏离原因
    severity: minor|major
    impact_scope: []              # 影响的文件/模块
    recorded_at: ""
```

#### 5. design-adjustments.yaml — 设计调整汇总（Phase 5）

```yaml
meta: {change_id, generated_at, requires_re_spec: true|false}
summary:
  total_adjustments: 0
  minor: 0
  major: 0
categories: []
adjustments:
  - id: ADJ-XXX
    original: ""
    adjusted: ""
    reason: ""
    severity: minor|major
    resolved_in_phase: "phase5"
```

#### 6. .canon-index.yaml — 索引文件

```yaml
version: "2.9"
proposals: {<change_id>: "proposals/<change_id>.yaml"}
designs: {}
specs:
  code: {<change_id>: "specs/code/<change_id>.yaml"}
  agent: {<change_id>: "specs/agent/<change_id>.yaml"}
```

#### CLI

```bash
stdd canon init --change <name>              # 初始化 canonical 目录 + YAML 模板
stdd canon generate [name] --type proposal    # YAML → MD 渲染
stdd canon verify <name>                      # 双轨一致性验证
```

---

### Ch31 Human View 生成规则

#### 渲染规则

`stdd canon generate` 从 YAML 直接字段映射到 MD（无需 Jinja2）：

- `proposal.yaml` → `proposal.md`：why → ##Why，what_changes → ##What Changes，capabilities → ###New/Modified，success_criteria → ##Success Criteria
- `spec.yaml` → `spec.md`：requirements → ###Requirement，scenarios → ####Scenario（GIVEN/WHEN/THEN/AND）
- 每个 MD 头部嵌入：`<!-- source_hash: <sha256> -->`、`<!-- generated_at: <iso> -->`、`<!-- canonical: <path> -->`

#### 自动修复

`canon verify` 发现 DC-HASH 缺失时（Human View 早于 Canonical），自动从 YAML 重新生成 MD 并回填 source_hash。

---

### Ch32 经验库系统

#### 5 态生命周期 FSM

```
discovered ──(verify, occurrences≥2, confidence≥0.7)──→ verified
                                                           │
                              (deposit, occurrences≥3, confidence≥0.8)
                                                           ↓
                                                        deposited ──(export --publish)──→ shared
                                                           │                                │
                                                           │                     (community imports≥3)
                                                           │                                ↓
                                                           │                             merged
                                                           │
                                                     (retire, 730d无活动)
                                                           ↓
                                                        retired
```

#### 来源与权重

| 来源 | 权重 | 说明 |
|------|------|------|
| `human-reported` | 0.95 | 人类直接报告 |
| `ci-detected` | 0.85 | CI 自动化检测 |
| `ai-inferred` | 0.60 | AI 推断 |
| `community-imported` | 0.50 | 社区导入 |

#### 自动加载

Phase 4 Step 0.5：按 language + category + tags 匹配，加载最多 10 条经验（lifecycle ≥ verified）。

#### CLI

详见 Ch40。

---

### Ch33 社区经验共享

#### 零后端设计

- **主注册表**：GitHub Releases (`github.com/leonai42/stdd-experiences`)
- **镜像**：Gitee Releases（5 秒超时自动故障转移）
- **投票**：GitHub Issues 作为投票 UI

#### 命令

```bash
stdd experience export --publish    # 发布经验包到社区
stdd experience pull python         # 从社区拉取 Python 经验包
stdd experience curate pull         # 拉取全量经验包到 inbox
stdd experience curate review       # 逐条审核
stdd experience curate pack         # 打包官方经验包
```

---

### Ch34 代码结构摘要系统

#### 自累积设计

每次 change 生成 delta → merge 到累积索引。AI 无需全量扫描代码库即可理解项目结构。

#### 目录结构

```
.stdd/code-structure/
  index.md               # 累积索引
  .structure-index.yaml  # 元数据
  deltas/<change>.md     # 每 change 的 delta
```

#### CLI

```bash
stdd structure delta <change>      # 为 change 生成 delta
stdd structure merge <change>      # 合并 delta 到索引
stdd structure rebuild             # 从所有 delta 重建索引
stdd structure show [module]       # 显示模块结构
stdd structure graph               # ASCII 依赖树
```

---

### Ch35 Skill 生态系统

#### 6 个 Phase Skill

| Skill | 文件 | 内容 |
|-------|------|------|
| stdd-understand | `understand.md` | Phase 1 流程：探索→模板→proposal→评分→Gate 1 |
| stdd-spec | `spec.md` | Phase 2 流程：提取→经验→设计→spec→锚定→Gate 2 |
| stdd-slice | `slice.md` | Phase 3 流程：5 步分析→依赖图→拓扑排序→分组 |
| stdd-build | `build.md` | Phase 4 流程：上下文检查→加载→RED→GREEN→REFACTOR |
| stdd-verify | `verify.md` | Phase 5 流程：审查→测试→失败模式→调整→Gate 3 |
| stdd-deliver | `deliver.md` | Phase 6 流程：归档→合并→验证→标签 |

#### _shared/ 片段

- `confirm-gate.md` — Gate 确认提示模板
- `mode-selection.md` — 长程/普通模式选择
- `long-range-auth.md` — 长程预授权清单

#### Skill 创建

```bash
stdd skill create <name> --type language|workflow|tools
```

生成 `.stdd/skills/<category>/<name>/SKILL.md`。

#### 平台同步

`stdd install <platform>` 将 6 个 Skill 复制到对应平台目录（`.claude/skills/`、`.trae/skills/` 等）。

---

> **Slice 3 (Part 4-6) 完成。** 下一 Slice：Part 7(CLI完整参考) + Part 8(配置系统) + Part 9(平台与规范)

---

## Part 7: CLI 完整参考

### Ch36 CLI 总览

#### 27 个顶级命令

| # | 命令 | 引入 | 子命令数 | 功能 |
|---|------|------|---------|------|
| 1 | `init` | V1.0 | 0 | 初始化 STDD 到项目 |
| 2 | `new` | V1.0 | 0 | 创建 change 目录骨架 |
| 3 | `validate` | V1.0 | 0 | 验证 change 结构 |
| 4 | `status` | V1.0 | 0 | 显示工件完成状态 |
| 5 | `archive` | V1.0 | 0 | 归档已完成 change |
| 6 | `trace` | V1.0 | 0 | 查看 spec↔test↔code 追溯 |
| 7 | `install` | V1.0 | 0 | 安装 Skills 到平台 |
| 8 | `rollback` | V2.0 | 0 | 从 archive 恢复 change |
| 9 | `diff` | V2.0 | 0 | 显示覆盖差异 |
| 10 | `abort` | V2.0 | 0 | 放弃变更并归档 |
| 11 | `extract-proposal` | V2.4 | 0 | 提取 proposal 结构化数据 |
| 12 | `dependency-graph` | V2.4 | 0 | 构建依赖图 |
| 13 | `ci` | V2.4 | 6 | CI/CD 集成管理 |
| 14 | `experience` | V2.4 | 9 | 经验库管理 |
| 15 | `state` | V2.5 | 0 | 跨 Session 状态管理 |
| 16 | `gate` | V2.5 | 1 | Gate 确认管理 |
| 17 | `proposal` | V2.7 | 3 | Canonical proposal 管理 |
| 18 | `canon` | V2.7 | 3 | 双轨制文档管理 |
| 19 | `index` | V2.7 | 3 | 项目索引管理 |
| 20 | `agent` | V2.7 | 1 | Agent 行为验证 |
| 21 | `hooks` | V2.7 | 3 | 生命周期 Hooks 管理 |
| 22 | `structure` | V2.8 | 5 | 代码结构摘要管理 |
| 23 | `skill` | V2.7 | 1 | Skill 创建 |
| 24 | `fix` | V2.8 | 0 | 多级自动修复 |
| 25 | `upgrade` | V2.9 | 0 | 版本升级 |
| 26 | `batch` | V2.9.3 | 6 | 批次管理 |
| 27 | `guard` | V2.9.3 | 5 | 智能门禁 |

#### 全局标志

所有命令都支持：
- `--dry-run`：预览，不修改文件系统
- `-v` / `--verbose`：`-v`=INFO, `-vv`=DEBUG

---

### Ch37 项目生命周期命令

#### `stdd init [--force]`

**功能：** 初始化 STDD 到当前项目。

**创建：** `.stdd/`（skills/templates/standards/config.d/platforms）、`changes/`、`specs/`、`archive/`、`STDD.md`、`AGENTS.md`

**`--force`**：覆盖已存在文件。

#### `stdd install <platform>`

**功能：** 安装 STDD Skills 到指定平台。

**平台：** `claude-code` / `workbuddy` / `trae` / `cursor` / `opencode`

| 平台 | 目标位置 | 格式 |
|------|---------|------|
| claude-code | `.claude/skills/<name>/SKILL.md` | 每 Skill 一目录 |
| workbuddy | `~/.workbuddy/skills/<name>.md` | 每 Skill 一文件 |
| trae | `.trae/skills/<name>.md` | 每 Skill 一文件 |
| cursor | `.cursor/rules/stdd.md` | 单文件 |
| opencode | `.opencode/skills/<name>/SKILL.md` | 每 Skill 一目录 |

#### `stdd upgrade`

**功能：** 升级 STDD 版本。

**参数：**

| 参数 | 说明 |
|------|------|
| (无) | 升级当前项目 |
| `--check` | 仅检查版本差异 |
| `--all` | 升级所有注册项目 |
| `--lock` | 锁定当前项目版本 |
| `--unlock` | 解锁当前项目 |
| `--yes` / `-y` | 跳过确认 |

**升级流程：** 检查锁状态 → 备份 → 同步源文件 → 合并 project.yaml → 重装平台 Skills → 更新 version.yaml → 注册全局注册表

---

### Ch38 变更管理命令

#### `stdd new <name>`

**功能：** 创建 change 目录骨架 `changes/<YYYY-MM-DD>-<name>/`。

**名称规则：** `^[a-zA-Z0-9][-a-zA-Z0-9_.]{1,49}$`（2-50 字符，字母数字开头）

**创建：** `proposal.md`, `design.md`, `test-plan.md`, `specs/`, `.stdd.yaml`

**`--parallel`**：同时创建 explore + research 并行 git worktree（长程模式双实例启动）。

#### `stdd validate [name]`

**功能：** 验证 change 目录结构完整性。

**检查项：** 必需文件存在、Spec 格式（Scenario 数量、GIVEN/WHEN/THEN 平衡、AND 上限 5）、TC-ID 唯一性、TC 数 ≥ Scenario 数。

#### `stdd status [name]`

**功能：** 显示工件完成状态。6 Phase 进度 + 产出物状态。

#### `stdd archive <name> [--yes] [--skip-specs]`

**功能：** 归档已完成 change 到 `archive/`。

**`--yes`**：跳过确认。**`--skip-specs`**：不合并 specs 到项目级。

#### `stdd rollback <name>`

**功能：** 从 archive 恢复 change。支持模糊名称匹配（`.endswith()`）。

**搜索顺序：** `archive/` → `archive/aborted/`。

#### `stdd abort <name> [--yes]`

**功能：** 放弃变更 → `archive/aborted/`。状态标记为 `aborted`。

#### `stdd diff [name]`

**功能：** Spec↔Test↔Code 覆盖差异表。四列：Spec Scenario | TC-ID | Test Function | Source。输出覆盖率百分比。

---

### Ch39 追溯与状态命令

#### `stdd trace <tc-id>`

**功能：** 追溯 TC-ID 的四层链。搜索 test-plan.md → 测试源文件 → 提取函数名和行号。

#### `stdd state [name]`

**功能：** 跨 Session 状态管理。

| 参数 | 说明 |
|------|------|
| (无) | 显示完整状态 |
| `--resume` | 显示恢复上下文（Change/Phase/Slice/Last Action/Freshness） |
| `--compact` / `-c` | 紧凑单行输出（跨平台省 token） |
| `--set KEY=VALUE` | 设置恢复字段 |

**可设置字段：** `resume_context`, `active_slice`, `last_action`, `last_modified`, `active_phase`, `phase_context_file`

#### `stdd gate approve --gate <1|2|3> [name]`

**功能：** 通过 CLI 确认 Gate。等效于 file_token 和 dialog 通道。

#### `stdd extract-proposal [name] [--format json|yaml]`

**功能：** 从 proposal.md 提取结构化数据（capabilities/impact/risk_areas 等）。

---

### Ch40 经验库命令

#### `stdd experience list`

**筛选参数：** `--category` / `--language` / `--lifecycle` / `--severity` / `--provenance` / `--format table|json|yaml` / `--all`

#### `stdd experience add`

**参数（13 个）：** `--category`（必需，14 类之一）、`--pattern`（必需）、`--root-cause`、`--detection-trigger`、`--fix-template`、`--language`、`--severity`、`--tags`、`--source-change`、`--body`、`--project-type`

#### 生命周期状态转换

| 命令 | 转换 | 条件 |
|------|------|------|
| `stdd experience verify <id>` | discovered → verified | occurrences≥2, confidence≥0.7 |
| `stdd experience deposit <id>` | verified → deposited | occurrences≥3, confidence≥0.8 |
| `stdd experience retire <id> --reason "...\"` | 任意 → retired | 730 天或手动 |

#### `stdd experience export [--output] [--format] [--no-sanitize] [--publish]`

导出到 tar.gz。`--publish` 上传到社区注册表。

#### `stdd experience pull <pack> [--source]`

从社区拉取经验包。

#### `stdd experience curate`

| 子命令 | 功能 |
|--------|------|
| `pull` | 拉取全量经验包到 inbox |
| `deduplicate` | 自动去重合并 |
| `review` | 逐条审核 |
| `pack` | 打包官方经验包 |

---

### Ch41 双轨制命令

#### `stdd proposal`

| 子命令 | 功能 |
|--------|------|
| `init [change_name]` | 从 proposal.md 生成 proposal.yaml |
| `validate [change_name]` | 验证 proposal.yaml 字段完整性 |
| `show [change_name]` | 人类可读显示 |

#### `stdd canon`

| 子命令 | 功能 | 参数 |
|--------|------|------|
| `init` | 初始化 canonical/ 目录 | `--change <name>` / `--project-level` |
| `generate` | YAML → MD 渲染 | `[change_name]` / `--type proposal|design|spec` / `--all` |
| `verify` | 验证双轨一致性 | `<change_name>`（必需）|

---

### Ch42 工程化命令

#### `stdd index`

| 子命令 | 功能 |
|--------|------|
| `update` | 生成/更新 project-index.yaml |
| `show [target]` | 显示索引摘要或特定 capability |
| `trace <file>` | 追踪文件到关联的 capabilities 和 changes |

#### `stdd agent verify [task] [--cp <id>]`

执行 agent_spec.yaml 中定义的检查点验证。

#### `stdd hooks`

| 子命令 | 功能 |
|--------|------|
| `install [--force]` | 写入 hook 脚本 + 配置 settings.local.json |
| `status` | 显示已安装 hooks |
| `uninstall` | 移除 hooks 配置 |

#### `stdd structure`

| 子命令 | 功能 |
|--------|------|
| `delta <change>` | 生成代码结构 delta |
| `merge <change>` | 合并 delta 到索引 |
| `rebuild` | 从所有 delta 重建索引 |
| `show [module]` | 显示模块结构 |
| `graph` | ASCII 依赖树 |

#### `stdd skill create [name] [--type language|workflow|tools]`

从模板创建新 STDD Skill。

---

### Ch43 质量与版本命令

#### `stdd fix [--level 1|2|3]`

三级自动修复（详见 Ch23）。

#### `stdd ci`（详见 Ch25）

#### `stdd batch`

| 子命令 | 功能 | 说明 |
|--------|------|------|
| `open "描述"` | 打开批次 | 含范围校验（large 拒绝，medium 警告） |
| `add "描述"` | 添加项到当前批次 | |
| `close` | 闭合批次 | 生成 archive-summary.md |
| `archive` | 归档批次到 archive/ | 先闭合（如未闭合）再移动 |
| `list` | 列出所有批次 | |
| `status` | 显示当前批次状态 | |

**参数：** `--strategy monthly|weekly|count_based`

#### `stdd guard`

| 子命令 | 功能 | 说明 |
|--------|------|------|
| `check` | 检查编辑权限 | exit 0=允许 2=阻止 |
| `status` | 显示门禁状态 | 含 scope 评估 |
| `init` | 部署 PreToolUse Hook | |
| `disable` | 临时移除 Hook | |
| `enable` | 重新启用 (=init) | |

**参数：** `--platform claude-code`（默认）、`--strict`（忽略 allow_bypass）、`--quiet`

---

### Ch44 依赖图命令

#### `stdd dependency-graph [name] [--format text|json|dot]`

- `text`（默认）：人类可读
- `json`：结构化 JSON
- `dot`：Graphviz DOT 格式

**输出：** 节点、边、零依赖节点、检测到的循环（DFS 检测）。

---

## Part 8: 配置系统

### Ch45 配置总览

#### 目录布局

```
.stdd/
  config.d/
    project.yaml       # 项目元数据
    gates.yaml         # Gate 定义
    long_range.yaml    # 长程模式
    quality.yaml       # 质量检查
    experience.yaml    # 经验库
    lite.yaml          # 轻量模式 + 复杂度评分
  version.yaml         # 版本信息
```

#### 加载与合并

- 加载顺序：project → gates → quality → experience → lite → long_range
- 升级时：结构键覆盖，身份键（project name 等）保留
- 旧项目兼容：`project.yaml` 回退到 legacy `config.yaml`

---

### Ch46 project.yaml

```yaml
stdd_version: "2.9.3"
project:
  name: "my-project"
  language: python          # python|go|java|rust|typescript
  python_version: "3.12"
  source_dir: "src"
paths:
  changes: "changes"
  specs: "specs"
  archive: "archive"
  tests: "tests"
enforce_stdd: true           # Guard 门禁开关
allow_bypass: false          # 是否允许绕过门禁
```

---

### Ch47 gates.yaml

```yaml
gates:
  phase1_understand:
    required: true
    description: "确认 proposal 范围、边界、成功标准"
  phase2_spec:
    required: true
    description: "确认技术设计与行为规格"
  phase5_verify:
    required: true
    description: "确认测试报告与质量检查结果"
confirmation:
  channels: [dialog, file_token, cli]
```

---

### Ch48 long_range.yaml

```yaml
long_range:
  recommended: true
  pre_auth:
    design_deviation:
      minor: "auto_record"
      major: "auto_record_continue"
    technical_blocker:
      strategy: "workaround"
    iteration:
      max_rounds: 10
      on_cap: "report_in_summary"
    operations:
      directory: "allow"
      file_write: "allow"
      command_exec: "allow"
      script_exec: "allow"
      network: "allow"
      file_read: "allow"
      git_readonly: "allow"
    gate3: "mandatory"
  degradation:
    max_consecutive_failures: 3
    pass_rate_threshold: 0.95
    safety_check: true
```

---

### Ch49 quality.yaml

```yaml
verify:
  max_iterations: 5         # 最大验证迭代（彻底模式 10）
  auto_fix: true             # 启用 Plankton L1 自动修复
review:
  enabled: true
  max_rounds: 3
  agents: [security, performance, compatibility]  # 并行审查代理
  severity_thresholds:
    critical: "block"
    high: "warn_block"
    medium: "warn"
    low: "ignore"
test:
  runner: "pytest"
  coverage_target: 80        # 百分比
  multi_version: [3.10, 3.11, 3.12]  # Python 多版本
quality:
  lint: "ruff check"
  typecheck: "mypy"
  e2e: false                 # 默认关闭
pass@k:
  enabled: true
  k_values: [1, 3]
  threshold: 0.8
```

---

### Ch50 experience.yaml

```yaml
experience:
  dir: ".stdd/experiences"
  auto_record: true           # Phase 5 自动记录经验
  auto_load:
    enabled: true
    max_experiences: 10
  lifecycle:
    verified_threshold: 3     # occurrences ≥ 3 → deposited
    settled_threshold: 10
    retire_after_days: 730
  export:
    sanitize: true            # 脱敏后导出
community:
  registries:
    - url: "https://github.com/leonai42/stdd-experiences/releases/latest/download"
      priority: 1
    - url: "https://gitee.com/leonai42/stdd-experiences/releases/latest/download"
      priority: 2
      fallback_timeout: 5    # 秒
  packs:
    - name: "python"
      version: "v1.0.0"
    - name: "go"
      version: "v1.0.0"
```

---

### Ch51 lite.yaml

```yaml
scoring:
  dimensions:
    - name: "impact_scope"
      weight: 3
      levels: ["single_file", "multi_file", "cross_module"]
    - name: "technical_complexity"
      weight: 3
    - name: "test_complexity"
      weight: 3
    - name: "dependency_count"
      weight: 3
    - name: "risk_level"
      weight: 3
    - name: "documentation_needs"
      weight: 2
  thresholds:
    lightweight: 3    # 0-3
    standard: 7       # 4-7
    thorough: 17      # 8-17
scaling:
  lightweight: {spec: "simplified", slice: "skip", build: "simplified", verify: "1_agent_5_modes", deliver: "batch_append"}
  standard:   {spec: "full", slice: "smart", build: "full_tdd", verify: "3_agents_12_modes", deliver: "full_archive"}
  thorough:   {spec: "full_advanced", slice: "parallel", build: "full_tdd_passk", verify: "3_agents_security_perf", deliver: "full_release_notes"}
batch:
  strategy: "monthly"
  max_items: 20
task_types:
  code: {spec: "spec.yaml", verify: "pytest+coverage"}
  documentation: {spec: "agent_spec.yaml", verify: "content+references"}
  configuration: {spec: "agent_spec.yaml", verify: "config_validation"}
  data-migration: {spec: "agent_spec.yaml", verify: "data_integrity"}
  dependency-upgrade: {spec: "agent_spec.yaml", verify: "compatibility"}
```

---

### Ch52 version.yaml + 全局注册表

```yaml
# .stdd/version.yaml
stdd_version: "2.9.3"
locked: false
installed_at: "2026-06-05T18:25:27"
upgraded_at: "2026-06-05T21:05:22"
source_path: "D:/mycode/stdd"
```

#### 全局注册表 `~/.stdd/projects.yaml`

```yaml
registry_version: 1
projects:
  - name: "my-project"
    path: "/path/to/project"
    version: "2.9.3"
    locked: false
    last_seen: "2026-06-06T20:00:00"
```

---

## Part 9: 平台与规范

### Ch53 平台适配架构

#### 设计原则

- **核心与适配器分离**：STDD 核心（CLI + Skill + 配置）平台无关，每平台一个薄适配层
- **Skill 生成机制**：`stdd install` 从 `.stdd/skills/` 生成平台特定格式

#### 平台特定调用

| 平台 | 调用方式 | 适配文件 |
|------|---------|---------|
| Claude Code | `/stdd-<phase>` 斜杠命令 | `.claude/skills/stdd-<phase>/SKILL.md` |
| WorkBuddy | 关键词触发 | `~/.workbuddy/skills/<name>.md` |
| Trae | 斜杠命令 | `.trae/skills/<name>.md` |
| Cursor | 自动加载规则 | `.cursor/rules/stdd.md` |
| Windsurf | Cascade 规则 | `.windsurfrules` |
| Copilot | 指令注入 | `.github/copilot-instructions.md` |
| OpenCode (V2.7) | 斜杠命令 | `.opencode/skills/<name>/SKILL.md` |

---

### Ch54 七大平台适配

#### Claude Code

- **调用：** `/stdd-<phase>` 斜杠命令
- **Skill 格式：** YAML frontmatter（name, description）+ Markdown body
- **门禁：** `PreToolUse` hook → `stdd guard check`
- **Hooks：** SessionStart / PreCompact / Stop

#### Cursor

- **调用：** `.cursorrules` 自动注入
- **门禁：** AI Rules 注入提示"编辑前先确认有 active change"（软约束）
- **无 Hook 支持**（PreToolUse 级别不可用）

#### Windsurf

- **调用：** Cascade Flow 规则
- **门禁：** 规则注入（软约束）

#### Copilot

- **调用：** `.github/copilot-instructions.md` 自动注入
- **门禁：** 指令注入（软约束）

#### 其他平台（WorkBuddy / Trae / OpenCode）

- 关键词或斜杠命令触发
- 门禁均为软约束（规则/指令注入）

---

### Ch55 开发规范体系

#### 5 语言标准

| 语言 | 文件 | 内容 |
|------|------|------|
| Python | `.stdd/standards/python.md` | 类型注解、async/await、CancelledError 处理 |
| Java | `.stdd/standards/java.md` | Spring Boot、JPA、异常处理 |
| Go | `.stdd/standards/go.md` | 错误处理、goroutine、context |
| Rust | `.stdd/standards/rust.md` | Cargo、所有权、unsafe |
| TypeScript | `.stdd/standards/typescript.md` | Node.js、async、类型安全 |

Phase 4 Step 0 自动按 `project.language` 加载对应标准。

#### Rules 目录

```
.stdd/rules/
  common/
    tdd.md              # TDD 红绿重构规则
    git-workflow.md     # Git 提交规范
    security.md         # 安全基线
  python/
    patterns.md         # Python 特定规则
  go/
    idioms.md           # Go 惯用法
```

---

### Ch56 模板系统

#### 17 个文档模板（11 核心 MD + 5 Canonical YAML + 1 Human View）

**核心 MD 模板（11 个）：**

| 模板 | 用途 | Phase |
|------|------|-------|
| `proposal.md` | 变更提案 | 1 |
| `design.md` | 技术设计 | 2 |
| `spec.md` | 行为规格（Human View） | 2 |
| `spec-draft.md` | AI 生成 spec 草稿 | 2 |
| `test-plan.md` | 测试计划 | 2 |
| `tasks.md` | 任务清单 | 3 |
| `slices.md` | 切片计划 | 3 |
| `design-adjustments.md` | 设计调整 | 5 |
| `test-report.md` | 测试报告 | 5 |
| `phase-context.md` | Phase 上下文 | 全 Phase |
| `long-range-auth.md` | 长程授权 | Gate 2 |

**Canonical YAML 模板（5 个）：**

| 模板 | 格式 | 用途 |
|------|------|------|
| `canonical/proposal.yaml` | YAML | 变更提案 |
| `canonical/spec.yaml` | YAML | 行为规格 |
| `canonical/agent_spec.yaml` | YAML | Agent 验证规格 |
| `canonical/pending-adjustments.yaml` | YAML | 设计偏离记录 |
| `canonical/design-adjustments.yaml` | YAML | 设计调整汇总 |

**Human View 模板（1 个）：**

| 模板 | 格式 | 用途 |
|------|------|------|
| `human-view/proposal-brief.md` | Markdown | proposal 渲染模板 |

#### 模板约束规则

- 读取后才写入（不覆盖已有内容）
- 固定结构（Section 顺序不可变）
- 必填字段不可为空
- 文件命名固定

---

> **Slice 4 (Part 7-9) 完成。** 下一 Slice：Part 10(版本演进) + Part 11(附录)

---

## Part 10: 版本演进与未来

### Ch57 V1.0 至 V2.9 完整演进

> 48 天、13 个版本、0→250 测试、1K→10.8K 行代码。

| 版本 | 日期 | 核心交付 | 关键洞察 |
|------|------|---------|---------|
| V1.0 | 5月 | 6-Phase 流程 + CLI 基础（7 命令） | 流程必须由工具强制执行，不能只靠文档 |
| V1.2 | 5月 | 验证增强 + 失败模式初版 | 自动化检查比人工审查更可靠 |
| V2.0 | 5月14日 | CLI 模块化拆分、10 命令、pytest 测试框架 | 架构不拆分则无法扩展 |
| V2.1 | 5月14日 | 审查增强 | 多代理并行审查效果显著 |
| V2.4 | 5月21日 | 经验库 + CI 集成 + 依赖图 + 提取 | 经验是 STDD 的"记忆系统" |
| V2.5 | 5月21日 | 跨 Session 状态（state）、Gate CLI 确认、锚定系统 | 跨 Session 连续工作是刚需 |
| V2.7 | 6月1日 | 上下文工程、双轨文档、Agent 验证、Skill 生态、Hooks | 双轨制让 AI 消费精确数据 |
| V2.8 | 6月3日 | Plankton 自动修复、代码结构摘要、pass@k、12 类失败模式完整 | 质量系统基本完备 |
| V2.9 | 6月5日 | 轻量模式、复杂度评分、批次管理、版本升级、task_type | 一套框架服务多种规模的任务 |
| V2.9.2 | 6月5日 | Canonical YAML 扩展、强制门、YAML-First | 门禁从无到有 |
| V2.9.3 | 6月6日 | 智能门禁（4 级范围分类）、batch open/add/archive、生命周期 Hooks deploy、--compact | 门禁从布尔→智能 |

#### 关键指标演进

| 指标 | V1.0 | V2.0 | V2.7 | V2.9.3 |
|------|------|------|------|--------|
| CLI 命令 | 7 | 10 | 21 | 27 |
| 测试数 | 0 | ~50 | ~180 | ~260 |
| 覆盖率 | 0% | 40% | 68% | 73% |
| 源文件行数 | ~1K | ~3K | ~7K | ~10.8K |
| 支持平台 | 1 | 1 | 5 | 7 |
| 失败模式 | 5 | 5 | 11 | 12 |
| 经验条目 | 0 | 0 | 0 | 7 |

---

### Ch58 V2.9 核心差异化 vs 同类工具

| 维度 | Copilot | Cursor | Claude Code 原生 | Cline | STDD V2.9 |
|------|---------|--------|-----------------|-------|-----------|
| 规格驱动 | ❌ | ❌ | ❌ | ❌ | ✅ Spec→实现→验证 |
| 强制门禁 | ❌ | ❌ | ❌ | ❌ | ✅ PreToolUse Hook + 范围分类 |
| TDD 强制 | ❌ | ❌ | ❌ | 部分 | ✅ RED→GREEN→REFACTOR |
| 失败模式检测 | ❌ | ❌ | ❌ | ❌ | ✅ 12 类 |
| 经验自学习 | ❌ | ❌ | ❌ | ❌ | ✅ 5 态 FSM |
| 跨 Session 恢复 | ❌ | ❌ | ❌ | ❌ | ✅ state --resume |
| 三档执行模式 | ❌ | ❌ | ❌ | ❌ | ✅ 轻量/标准/彻底 |
| 双轨文档 | ❌ | ❌ | ❌ | ❌ | ✅ Canonical YAML + Human View |
| 批量管理 | ❌ | ❌ | ❌ | ❌ | ✅ batch 系统 |
| 版本升级 | ❌ | ❌ | ❌ | ❌ | ✅ stdd upgrade |
| 多平台支持 | — | — | — | — | ✅ 7 平台 |
| CI/CD 集成 | ❌ | ❌ | ❌ | ❌ | ✅ GitHub Actions + pre-commit |
| 锚定体系 | ❌ | ❌ | ❌ | ❌ | ✅ L1-L4 |

---

### Ch59 V3 展望

> 以下内容来自 VISION.md，处于讨论阶段，白皮书不展开。

- **Phase 0 需求管理**：跨 Change 的需求优先级和关联跟踪
- **Phase 7 AAR**：项目级复盘和经验提炼
- **完整双轨**：8 条规则全部实现，test-plan.yaml 替代 test-plan.md
- **非代码领域**：金融合规、法律文书、运营流程的 STDD 化
- **无感门禁**：从智能门禁到无感门禁，AI 自动选择最佳流程

---

## Part 11: 附录

### AppA 完整目录结构参考

```
项目根目录/
├── .stdd/                          # STDD 系统目录
│   ├── version.yaml                #   C: 版本信息
│   ├── config.d/                   #   C: 配置模块（6 文件）
│   ├── skills/                     #   F: Phase Skill 定义
│   │   └── _shared/                #   F: 共享片段
│   ├── templates/                  #   F: 文档模板（13 个）
│   │   ├── canonical/              #   F: Canonical YAML 模板（5 个）
│   │   └── human-view/             #   F: Human View 模板
│   ├── standards/                  #   F: 语言编码标准（5 语言）
│   ├── rules/                      #   F: 项目编码规则
│   ├── platforms/                  #   F: 平台适配层
│   ├── experiences/                #   C: 经验库
│   └── hooks/                      #   F: 生命周期 Hook 脚本
├── changes/                        # Y: 活动变更
│   ├── <date>-<name>/              #   Y: 变更目录（6 Phase 产物）
│   └── _batch/                     #   Y: 批次变更容器
├── specs/                          # C: 合并后的规格文档
├── archive/                        # C: 已归档变更
├── stdd/                           #   源码（CLI 实现）
├── tests/                          #   测试
├── STDD.md                         # H: AI 代理规则
├── AGENTS.md                       # H: 项目记忆
├── STDD_WHITEPAPER_V2.9_CN.md     # H: 本文件
└── pyproject.toml                  # C: Python 包配置
```

---

### AppB CLI 命令速查表

| 命令 | 参数 | 默认值 | 引入 | exit code |
|------|------|--------|------|-----------|
| `init` | `--force` | false | V1.0 | 0 |
| `new` | `<name>`, `--parallel` | | V1.0 | 0/1 |
| `validate` | `[name]` | 最近 | V1.0 | 0/1 |
| `status` | `[name]` | 最近 | V1.0 | 0 |
| `archive` | `<name>`, `--yes`, `--skip-specs` | | V1.0 | 0/1 |
| `trace` | `<tc-id>` | | V1.0 | 0/1 |
| `install` | `<platform>` | | V1.0 | 0/1 |
| `rollback` | `<name>` | | V2.0 | 0/1 |
| `diff` | `[name]` | 最近 | V2.0 | 0/1 |
| `abort` | `<name>`, `--yes` | | V2.0 | 0/1 |
| `extract-proposal` | `[name]`, `--format json\|yaml` | json | V2.4 | 0/1 |
| `dependency-graph` | `[name]`, `--format text\|json\|dot` | text | V2.4 | 0/1 |
| `ci init` | | | V2.4 | 0 |
| `ci generate` | `<target>` | | V2.4 | 0 |
| `ci check-*` | `[name]` | | V2.4 | 0/1 |
| `experience list` | `--category`, `--language`, `--lifecycle`, `--severity`, `--provenance`, `--format`, `--all` | table | V2.4 | 0 |
| `experience add` | `--category`, `--pattern` 等 13 参数 | | V2.4 | 0 |
| `experience stats` | `--format` | table | V2.4 | 0 |
| `experience export` | `--output`, `--format`, `--no-sanitize`, `--publish` | json | V2.4 | 0 |
| `experience pull` | `<pack>`, `--source` | | V2.4 | 0 |
| `experience verify` | `<id>` | | V2.4 | 0 |
| `experience deposit` | `<id>` | | V2.4 | 0 |
| `experience retire` | `<id>`, `--reason` | | V2.4 | 0 |
| `state` | `[name]`, `--resume`, `--compact`, `--set KEY=VALUE` | | V2.5 | 0/1 |
| `gate approve` | `--gate 1\|2\|3`, `[name]` | | V2.5 | 0/1 |
| `proposal init` | `[change_name]` | 最近 | V2.7 | 0/1 |
| `proposal validate` | `[change_name]` | 最近 | V2.7 | 0/1 |
| `proposal show` | `[change_name]` | 最近 | V2.7 | 0 |
| `canon init` | `--change`, `--project-level` | | V2.7 | 0/1 |
| `canon generate` | `[change_name]`, `--type proposal\|design\|spec`, `--all` | proposal | V2.7 | 0/1 |
| `canon verify` | `<change_name>` | | V2.7 | 0/1 |
| `index update` | | | V2.7 | 0 |
| `index show` | `[target]` | | V2.7 | 0 |
| `index trace` | `<file>` | | V2.7 | 0 |
| `agent verify` | `[task]`, `--cp <id>` | | V2.7 | 0/1 |
| `hooks install` | `--force` | false | V2.7 | 0 |
| `hooks status` | | | V2.7 | 0 |
| `hooks uninstall` | | | V2.7 | 0 |
| `structure delta` | `<change>` | | V2.8 | 0 |
| `structure merge` | `<change>` | | V2.8 | 0 |
| `structure rebuild` | | | V2.8 | 0 |
| `structure show` | `[module]` | | V2.8 | 0 |
| `structure graph` | | | V2.8 | 0 |
| `skill create` | `[name]`, `--type language\|workflow\|tools` | language | V2.7 | 0 |
| `fix` | `--level 1\|2\|3` | 1 | V2.8 | 0 |
| `upgrade` | `--check`, `--all`, `--lock`, `--unlock`, `--yes` | | V2.9 | 0/1 |
| `batch open` | `"description"`, `--strategy` | monthly | V2.9.3 | 0 |
| `batch add` | `"description"` | | V2.9.3 | 0 |
| `batch close` | | | V2.9.3 | 0 |
| `batch archive` | | | V2.9.3 | 0 |
| `batch list` | | | V2.9.3 | 0 |
| `batch status` | | | V2.9.3 | 0 |
| `guard check` | `--platform`, `--strict`, `--quiet` | claude-code | V2.9.3 | 0/2 |
| `guard status` | | | V2.9.3 | 0 |
| `guard init` | `--platform` | claude-code | V2.9.3 | 0 |
| `guard disable` | | | V2.9.3 | 0 |
| `guard enable` | | | V2.9.3 | 0 |

---

### AppC 常见问题 (FAQ)

**Q1: 如何开始使用 STDD？**
A: `stdd init` → 用 `/stdd-understand` 启动第一个变更流程。

**Q2: 轻量/标准/彻底模式怎么选？**
A: Phase 1 复杂度评分自动推荐。微修复选轻量，功能增强选标准，新模块/架构变更选彻底。可在 Gate 2 手动覆盖。

**Q3: Gate 确认可以跳过吗？**
A: 不可以。三道 Gate 强制、顺序执行。但可以通过 file_token（创建 `GATE<N>_APPROVED` 文件）或 CLI（`stdd gate approve`）来加速。

**Q4: Guard 总是阻止我的编辑怎么办？**
A: 三种方式进入可编辑状态：① 用 `stdd batch open "描述"` 开启轻量批次；② 用 `stdd new <name>` 创建正式 change 并推进到 build phase；③ 在 project.yaml 中设 `allow_bypass: true`（不推荐）。

**Q5: 长程模式和普通模式有什么区别？**
A: 长程模式在 Gate 2 后对 Phase 3-5 预授权，允许 AI 跨 Session 连续执行。Gate 3 仍然强制。连续失败 3 次或通过率 <95% 自动降级为普通模式。

**Q6: Canonical YAML 和 Human View MD 的关系是什么？**
A: YAML 是 AI 精确消费的数据源（唯一真相来源）。MD 是从 YAML 单向生成的渲染输出。使用 `stdd canon verify` 检查一致性。

**Q7: Batch 和 Change 什么时候用哪个？**
A: 微修复（<5 文件，如 bug fix）用 batch。功能增强/重构/新模块用 change（full STDD 流程）。Guard 的智能分类器会在 batch open 时根据描述自动建议。

**Q8: 如何跨 Session 恢复工作？**
A: 新 Session 中说"继续" → Claude 执行 `stdd state --resume --compact` → 一行恢复所有上下文。或 SessionStart Hook 自动输出。

**Q9: 经验库如何工作？**
A: Phase 5 自动记录发现的失败模式。Phase 4 自动加载匹配的经验。生命周期：discovered → verified（≥2次，置信度≥0.7）→ deposited（≥3次，置信度≥0.8）。

**Q10: 如何升级 STDD 版本？**
A: `stdd upgrade --check` 先检查差异，确认后 `stdd upgrade`。升级会备份旧版本、同步新文件、合并配置、重装平台 Skills。

**Q11: Guard 跨平台能用吗？**
A: `stdd guard check` CLI 本身跨平台通用。自动拦截目前仅 Claude Code（PreToolUse Hook）。其他平台通过规则文件做软约束。

**Q12: 如何贡献经验到社区？**
A: `stdd experience export --publish`。社区注册表在 GitHub Releases + Gitee 镜像。官方经验包通过 `stdd experience curate` 维护。

---

### AppD .stdd.yaml 完整字段参考

| 字段 | 类型 | 默认值 | 写入端 | 读取端 |
|------|------|--------|--------|--------|
| `change_id` | str | — | new.py | 全局 |
| `change_name` | str | — | new.py | 全局 |
| `status` | str | `"active"` | new, archive, abort, rollback | guard, validate, status |
| `current_phase` | str | `"understand"` | new, state, phases | guard, status, state |
| `task_type` | str | `"code"` | new, 用户 | guard, spec |
| `mode` | str | `"standard"` | new, Gate2 | build, verify |
| `complexity_score` | int\|null | null | understand | spec |
| `score_confidence` | str\|null | null | understand | spec |
| `version` | str | `"2.0"` | new | — |
| `phases.<phase>.status` | str | `"pending"` | 各 Phase | 全局 |
| `phases.<phase>.confirmed_at` | str\|null | null | gate | validate |
| `long_range.enabled` | bool | false | Gate2 | build, verify |
| `long_range.mode` | str | `"full_auto"` | Gate2 | build, verify |
| `long_range.pre_auth_completed` | bool | false | Gate2 | build, verify |
| `traceability.spec_scenarios` | int | 0 | spec | validate |
| `traceability.tc_cases` | int | 0 | spec | validate, trace |
| `traceability.test_functions` | int | 0 | build | trace |
| `design_adjustments.count` | int | 0 | build, verify | verify |
| `resume_context` | str\|null | null | state | state |
| `active_slice` | str\|int\|null | null | state | state |
| `last_action` | str\|null | null | state, hooks | state |
| `last_modified` | str\|null | null | state, hooks | state |
| `active_phase` | str\|null | null | state | state |
| `phase_context_file` | str\|null | null | state | state |
| `state_freshness.verified_at` | str\|null | null | hooks | state |
| `state_freshness.git_head` | str\|null | null | hooks | state |

---

> **全文完。** STDD V2.9.3 白皮书 · 11 Parts · 60 Chapters · 中文人类版
