# STDD — 系统设计文档 | System Design

> 版本 / Version：V1.1
> 日期 / Date：2026-05-07
>
> STDD (Spec+Test Driven Development) 是一套 AI 辅助的 Spec 先行 + TDD 执行的研发流程系统。
> STDD is an AI-assisted, spec-first + TDD execution methodology for software development.

---

## 目录 / Table of Contents

1. [概述 / Overview](#1-概述--overview)
2. [六阶段流程 / Six-Phase Flow](#2-六阶段流程--six-phase-flow)
3. [关键机制 / Key Mechanisms](#3-关键机制--key-mechanisms)
4. [系统架构 / System Architecture](#4-系统架构--system-architecture)
5. [Skill 与模板系统 / Skill & Template System](#5-skill-与模板系统--skill--template-system)
6. [开发规范 / Development Standards](#6-开发规范--development-standards)
7. [跨平台设计 / Cross-Platform Design](#7-跨平台设计--cross-platform-design)
8. [CLI 辅助脚本 / CLI Helper Script](#8-cli-辅助脚本--cli-helper-script)

---

## 1. 概述 / Overview

### 核心理念 / Core Principles

| 原则 / Principle | 说明 / Description |
|-----------------|-------------------|
| **Spec 先行 / Spec First** | 先定义行为（GIVEN/WHEN/THEN），再写代码。Define behavior before writing code. |
| **TDD 执行 / TDD Execution** | RED → GREEN → REFACTOR，按垂直切片推进。Proceed by vertical slices. |
| **设计调整可追溯 / Traceable Adjustments** | 实现中对设计的任何偏离必须记录。Every design deviation must be documented. |
| **用户确认驱动 / User-Confirmation-Driven** | 关键节点必须用户确认。Key checkpoints require explicit user confirmation. |

### 三道强制确认门 / Three Mandatory Gates

```
Gate 1: Phase 1 结束 — 用户确认 proposal.md
        End of Phase 1 — User confirms proposal.md

Gate 2: Phase 2 结束 — 用户确认 design.md + specs/*.md + test-plan.md
        End of Phase 2 — User confirms design + specs + test-plan

Gate 3: Phase 5 结束 — 用户确认 test-report.md + design-adjustments.md
        End of Phase 5 — User confirms test report + design adjustments
```

三道门都是必须的，不可跳过。没有用户明确确认，Skill 必须中断等待。
All three gates are mandatory. Without explicit user confirmation, the Skill must pause and wait.

Gate 2 之后可选择执行模式：
- **全自动长程模式（默认）**：一次性预授权所有 Phase 3-5 交互点，之后连续自动执行，仅在 Gate 3 等待确认。
- **普通交互模式**：Phase 3-5 按需暂停交互，保持现有行为。
After Gate 2, execution mode can be selected:
- **Full-Auto Long-Range Mode (default)**: One-time pre-auth for all Phase 3-5 interaction points, then continuous auto-execution, only pausing at Gate 3.
- **Normal Interactive Mode**: Phase 3-5 pauses for interaction as needed, maintaining existing behavior.

---

## 2. 六阶段流程 / Six-Phase Flow

```
Phase 1                Phase 2                Phase 3-5               Phase 6
UNDERSTAND             SPEC                   BUILD LOOP             DELIVER
─────────              ────                   ──────────             ───────

  需求输入           design.md              ┌── SLICE ──┐            归档 + 合并
  Input              specs/*.md             │ 切片规划    │           Archive + Merge
    │                test-plan.md           └────┬───────┘              │
    ▼                    │                      ▼                     ▼
  proposal.md ←── 用户确认(必须)         ┌── BUILD ──┐           specs 更新
    │              User confirm           │ RED→GREEN  │           git tag
    ▼                                    │ →REFACTOR  │              │
  用户确认(必须)                          └────┬───────┘           完成 / Done
  User confirm                               │
                                             ▼
                                       ┌── VERIFY ──┐
                                       │ 质量验证    │
                                       └────┬───────┘
                                            │
                                      用户确认产出(必须)
                                      User confirm
                                       ├── 有异议→回到P2
                                       └── 确认→P6 DELIVER

图例 / Legend:
  ──→  自动推进 / Auto-advance
  ←──  等待用户确认（必须）/ Wait for user confirmation (mandatory)
```

### Phase 1: UNDERSTAND — 需求理解与确认 | Requirement Understanding

- **中文**：将模糊需求转化为清晰、可验证的变更提案（proposal.md）。包含问题探索、提案起草、用户评审确认三个步骤。确认前不生成文件。
- **EN**：Transforms vague requirements into a clear, verifiable change proposal (proposal.md). Three steps: problem exploration, draft proposal, user review & confirmation. No files are written before confirmation.

### Phase 2: SPEC — 规格设计与测试方案 | Spec & Test Design

- **中文**：将 proposal 转化为精确的技术规格和测试方案。这是整个流程中**最重要的阶段**。产出 design.md（技术方案）、specs/\*.md（行为规格，GIVEN/WHEN/THEN 格式）、test-plan.md（TC-ID 映射 + 覆盖矩阵）。必须用户确认后才能进入实现阶段。
- **EN**：Transforms the proposal into precise technical specs and test plans. **The most critical phase.** Produces design.md (technical decisions), specs/\*.md (behavior specs in GIVEN/WHEN/THEN format), and test-plan.md (TC-ID mapping + coverage matrix). User must confirm before implementation begins.

**Spec → Test 映射规则 / Mapping Rule**：

| spec Scenario | test-plan TC Case |
|--------------|-------------------|
| GIVEN: 前置条件 / Precondition | 预置条件 / Arrange |
| WHEN: 触发动作 / Trigger | 输入 / Act |
| THEN: 预期结果 / Expected result | 预期结果 / Assert |
| AND: 附加结果 / Additional result | 额外的 Assert |

**TC-ID 命名规则 / Naming**：`TC-<CAPABILITY>-<NNN>`（如 TC-CASUAL-001）

### Phase 3: SLICE — 切片规划 | Slice Planning

- **中文**：将测试方案拆分为可独立实现的垂直切片。按依赖关系拓扑排序，P0 优先。产出 tasks.md 和 slices.md。自动推进，无需用户确认。
- **EN**：Splits the test plan into independently implementable vertical slices. Topological sort by dependencies, P0 first. Produces tasks.md and slices.md. Auto-advances without user confirmation.

### Phase 4: BUILD — TDD 实现 | TDD Implementation

- **中文**：按切片逐一执行 RED → GREEN → REFACTOR。先编写测试（RED），再写最小实现（GREEN），最后重构（REFACTOR）。自动迭代，仅在遇到阻塞或重大设计偏离时暂停询问用户。如有设计偏离，记录到 pending-adjustments.md。
- **EN**：Executes RED → GREEN → REFACTOR per slice. Write tests first (RED), then minimal implementation (GREEN), then refactor (REFACTOR). Auto-iterates; only pauses on blockers or major design deviations. Design deviations are recorded to pending-adjustments.md.

### Phase 5: VERIFY — 质量验证 | Quality Verification

- **中文**：全量质量检查 + 设计调整汇总。最多 5 轮迭代：运行 pytest/lint → Diff 审查 → 五类失败模式检查 → 汇总设计调整 → 生成 test-report.md。完成后必须等待用户确认。
- **EN**：Full quality check + design adjustment summary. Max 5 iterations: run pytest/lint → diff review → five failure mode check → summarize design adjustments → generate test-report.md. Must wait for user confirmation upon completion.

**九类失败模式检查 / Nine Failure Modes**：

| # | 模式 / Mode | 说明 / Description | 版本 |
|---|------------|-------------------|------|
| (a) | 幻觉行为 / Hallucinated actions | 编造的文件路径、环境变量、函数名、库 API | V1.0 |
| (b) | 范围蔓延 / Scope creep | 超出计划文件的改动 | V1.0 |
| (c) | 级联错误 / Cascading errors | 异常被静默吞掉、空数组 fallback 掩盖问题 | V1.0 |
| (d) | 上下文丢失 / Context loss | 与 proposal/design/spec 决策矛盾 | V1.0 |
| (e) | 工具误用 / Tool misuse | 错误的工具选择或参数 | V1.0 |
| (f) | 运行时行为偏差 / Runtime behavior deviation | 静态结构正确但动态行为异常（CSS/JS/交互） | V1.1 |
| (g) | 管线断链 / Pipeline chain break | 多步转换链路缺失步骤或隐式假定 | V1.1 |
| (h) | 内容质量偏差 / Content quality deviation | 数据不一致、长度越界、引用缺失、设计不当 | V1.1 |
| (i) | 指令衰减 / Instruction decay | Prompt 明确写了但 AI 未充分执行 | V1.1 |

> (f)-(i) 为 V1.1 新增，基于 FPPT 项目 Phase 2-5 实测中发现的 4 个 TDD 系统性盲区：
> 盲区A "静态结构 vs 动态行为" → (f)；盲区B "单元测试 vs 集成链路" → (g)；
> 盲区C "结构合规 vs 内容质量" → (h)；盲区D "Prompt测试 vs 执行结果测试" → (i)。

### Phase 6: DELIVER — 交付 | Delivery

- **中文**：归档变更到 archive/ → 合并 specs 到 specs/ → Git commit + tag。用户确认 commit message 后执行。
- **EN**：Archive change to archive/ → merge specs to specs/ → Git commit + tag. Executed after user confirms commit message.

---

## 3. 关键机制 / Key Mechanisms

### 3.1 强制确认门 / Mandatory Confirmation Gates

整个 STDD 流程设置三道强制确认门。Skill 在每道门前必须中断等待用户明确确认。
Three mandatory gates in the STDD flow. The Skill must pause and wait for explicit user confirmation at each gate.

| 门 / Gate | 位置 / Position | 确认内容 / Confirmation Content |
|-----------|---------------|-------------------------------|
| Gate 1 | Phase 1 结束 | proposal.md — 范围、边界、成功标准 |
| Gate 2 | Phase 2 结束 | design.md + specs + test-plan.md — 技术方案、行为规格、测试覆盖 |
| Gate 3 | Phase 5 结束 | test-report.md + design-adjustments.md — 测试结果、设计调整 |

### 3.2 设计调整追溯 / Design Adjustment Traceability

Phase 3-5 期间对 Phase 2 设计的任何偏离都必须记录。
Any deviation from the Phase 2 design during Phases 3-5 must be documented.

**处理流程 / Process**：
```
Phase 3-4: 发现偏离 → 记录到 pending-adjustments.md
           Deviation found → record to pending-adjustments.md

Phase 4:   小偏离 → 记录继续 / Minor → record & continue
           大偏离 → 暂停，询问用户 / Major → pause, ask user

Phase 5:   汇总 pending-adjustments → 生成 design-adjustments.md
           Summarize pending-adjustments → generate design-adjustments.md
           test-report.md 中引用变更说明 / Reference adjustments in test-report.md
```

### 3.3 双向追溯链 / Bidirectional Traceability

```
spec Scenario          test-plan TC          pytest 测试            源码 / Source
────────────────────────────────────────────────────────────────────────────
Scenario: 纯emoji →  TC-CASUAL-001    →  test_pure_unicode_  →  _is_pure_emoji()
GIVEN: 用户发emoji                        emoji_filtered        (message_service.py)
WHEN: 调用过滤
THEN: 返回友好回复
```

**追溯层级 / Trace Levels**：
- spec Scenario → TC-ID（test-plan.md 维护 / maintained in test-plan.md）
- TC-ID → 测试函数（测试文件注释 / annotated in test files）
- 测试函数 → 源码（import 调用链 / import chain）

### 3.4 自动迭代 vs 用户交互 / Auto-Iteration vs. User Interaction

| 场景 / Scenario | 普通模式 / Normal | 长程模式 / Long-Range |
|----------------|-------------------|---------------------|
| Phase 3 切片规划 / Slice planning | 自动完成，不中断 | 自动完成，不中断 |
| Phase 4 单切片 TDD / Single slice TDD | 自动完成 | 自动完成 |
| Phase 4 小设计偏离 / Minor design deviation | 记录 pending-adjustments，继续 | 记录 pending-adjustments，继续 |
| Phase 4 大设计偏离 / Major design deviation | 暂停，询问用户 | 自动记录并继续（test-report 汇总） |
| Phase 4 技术阻塞 / Technical blocker | 暂停，询问用户 | 尝试绕过/跳过；无法处理时降级暂停 |
| Phase 5 质量检查失败 / Quality check failure | 自动修复，重新检查 | 自动修复，重新检查 |
| Phase 5 达到迭代上限 / Iteration cap hit | 暂停，向用户报告 | 汇总到 test-report，继续（通过率<95%时降级） |
| Phase 5 完成 / Complete | **强制等待用户确认** | **强制等待用户确认**（不自动跳过） |
| Phase 5 用户有异议 / User disagrees | 回到 Phase 2 | 回到 Phase 2 |

### 3.5 长程模式预授权 / Long-Range Mode Pre-Auth

长程模式下，Gate 2 确认后进入一次性预授权流程，扫描 Phase 3-5 所有潜在交互点并统一授权：

**A. 流程决策授权**：
- 设计偏离处理策略（小偏离/大偏离）
- 技术阻塞处理策略（绕过/跳过/降级）
- 迭代上限策略（扩展轮数 + 达上限行为）

**B. 操作类授权**（最常见的打断源）：
- 目录操作、文件写入、命令执行（pytest/ruff/mypy）
- 脚本执行、网络访问（pip install）、文件读取、Git 只读操作

**C. 降级触发条件**：
- 连续自动修复同一问题达到上限（3 次）仍失败
- 测试通过率低于 95%
- 发现安全相关问题
- 预授权范围外的未预期情况

长程模式状态记录在 `.stdd.yaml` 的 `long_range` 字段中。

---

## 4. 系统架构 / System Architecture

### 4.1 整体架构 / Overall Architecture

STDD 采用**混合模式**：6 个核心 Skill（流程控制）+ Python CLI 脚本（结构化操作）。
STDD uses a **hybrid model**: 6 core Skills (flow control) + Python CLI scripts (structured operations).

```
┌──────────────────────────────────────────────────────────────────┐
│                       STDD System                                │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────────┐   │
│  │   Skill    │  │   Config   │  │   Change Management      │   │
│  │   Engine   │  │   Loader   │  │   (proposal/design/      │   │
│  │            │  │            │  │    specs/test-plan/       │   │
│  │ 6 phase    │  │  .stdd/    │  │    test-report/...)      │   │
│  │  skills    │  │  config    │  │                          │   │
│  └────────────┘  └────────────┘  └──────────────────────────┘   │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────────┐   │
│  │    Gate    │  │   Trace    │  │   Template Engine        │   │
│  │   Manager  │  │   Engine   │  │   (document generation)  │   │
│  │            │  │            │  │                          │   │
│  │ 3 forced   │  │ spec↔test  │  │   .stdd/templates/       │   │
│  │  gates     │  │  mapping   │  │                          │   │
│  └────────────┘  └────────────┘  └──────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 核心组件 / Core Components

| 组件 / Component | 职责 / Responsibility | 实现 / Implementation |
|-----------------|----------------------|----------------------|
| Skill Engine | 6 个 Phase Skill 的调度和执行 / Schedule & execute 6 phase skills | Markdown Skill 文件 + AI 平台调用 |
| Config Loader | 读取 .stdd/config.yaml，加载项目配置 / Load project config | Python CLI + Skill Read |
| Change Manager | 管理 changes/specs/archive 目录结构 / Manage directory structure | 文件系统 + 模板生成 |
| Gate Manager | 强制执行三道确认门 / Enforce three confirmation gates | Skill 内嵌确认逻辑 |
| Trace Engine | 维护 spec↔TC↔test↔code 映射 / Maintain traceability | test-plan.md TC-ID 体系 |
| Template Engine | 模板读取与文档生成 / Template reading & document generation | .stdd/templates/ 目录 |

### 4.3 目录结构 / Directory Structure

```
项目根目录 / Project Root
│
├── .stdd/                          # STDD 系统目录 / System directory
│   ├── config.yaml                 # 项目配置 / Project config
│   ├── skills/                     # 6 个阶段 Skill 定义 / 6 phase skill definitions
│   │   ├── understand.md           # Phase 1
│   │   ├── spec.md                 # Phase 2
│   │   ├── slice.md                # Phase 3
│   │   ├── build.md                # Phase 4
│   │   ├── verify.md               # Phase 5
│   │   └── deliver.md              # Phase 6
│   ├── templates/                  # 8 个文档模板 / 8 document templates
│   │   ├── proposal.md             # 变更提案
│   │   ├── design.md               # 技术设计
│   │   ├── spec.md                 # 行为规格
│   │   ├── test-plan.md            # 测试方案
│   │   ├── tasks.md                # 任务清单
│   │   ├── slices.md               # 切片计划
│   │   ├── design-adjustments.md   # 设计调整说明
│   │   └── test-report.md          # 测试报告
│   ├── standards/                  # 开发规范 / Development standards
│   │   └── python.md               # Python 开发规范
│   └── platforms/                  # 多平台适配 / Platform adapters
│       ├── claude-code/skills/
│       ├── workbuddy/skills/
│       └── trae/skills/
│
├── specs/                          # 主规范（canonical）/ Master specs (merged)
│   └── <capability>/spec.md
│
├── changes/                        # 活跃变更 / Active changes
│   └── <YYYY-MM-DD>-<name>/
│       ├── .stdd.yaml              # 变更状态文件 / Change state file
│       ├── proposal.md
│       ├── design.md
│       ├── specs/<capability>/spec.md
│       ├── test-plan.md
│       ├── tasks.md
│       ├── slices.md               # 可选 / Optional
│       ├── pending-adjustments.md  # Phase 3-4 设计偏离记录
│       ├── design-adjustments.md   # Phase 5 设计调整汇总
│       └── test-report.md
│
└── archive/                        # 已完成变更 / Completed changes
    └── <YYYY-MM-DD>-<name>/
```

### 4.4 变更状态文件 / .stdd.yaml

```yaml
# changes/<date>-<name>/.stdd.yaml
change_id: "2026-05-03-v1.5-stability-ux-upgrade"
status: "active"          # active | archived
current_phase: "verify"   # understand | spec | slice | build | verify | deliver

phases:
  understand:
    status: "completed"   # pending | in_progress | completed
    confirmed_at: "2026-05-03T10:00:00"
  spec:
    status: "completed"
    confirmed_at: "2026-05-03T11:30:00"
  # ...

design_adjustments:
  count: 2
  file: "design-adjustments.md"

traceability:
  spec_scenarios: 12
  tc_cases: 35
  test_functions: 94
```

---

## 5. Skill 与模板系统 / Skill & Template System

### 5.1 Skill 清单 / Skill List

| Skill | 阶段 / Phase | 触发方式 / Trigger | 确认门 / Gate |
|-------|-------------|-------------------|--------------|
| `/stdd-understand` | Phase 1 | 用户发起 / User initiates | 结束时有 / Yes |
| `/stdd-spec` | Phase 2 | Phase 1 确认后 / After P1 confirm | 结束时有 / Yes |
| `/stdd-slice` | Phase 3 | 自动 / Auto | 无 / No |
| `/stdd-build` | Phase 4 | 自动 / Auto | 仅阻塞时 / On blocker |
| `/stdd-verify` | Phase 5 | 自动 / Auto | 结束时有 / Yes |
| `/stdd-deliver` | Phase 6 | Phase 5 确认后 / After P5 confirm | 无 / No |
| `/stdd-status` | 任意 / Any | 用户随时 / User anytime | — |
| `/stdd-continue` | 任意 / Any | 恢复中断 / Resume | — |

### 5.2 模板约束规则 / Template Constraint Rules

1. **先读后写 / Read Before Write**：编写任何文档前，Skill 必须先读取对应模板。Must read template before generating document.
2. **章节不可增删 / Fixed Structure**：文档章节必须与模板一致，不得自行增删。Section structure must match template exactly.
3. **字段不可省略 / Required Fields**：模板中标注必填的字段必须填写。All required fields must be filled.
4. **命名不可变 / Fixed Naming**：文件命名严格遵循规范。File naming follows the convention strictly.

### 5.3 模板列表 / Template List

| 模板 / Template | 阶段 / Phase | 关键约束 / Key Constraint |
|----------------|-------------|-------------------------|
| proposal.md | Phase 1 | Success Criteria 可验证；Impact 三维度 |
| design.md | Phase 2 | 每个决策有方案对比；风险有缓解措施 |
| spec.md | Phase 2 | THEN 含 SHALL；GIVEN/WHEN/THEN/AND 格式 |
| test-plan.md | Phase 2 | TC-ID 全局唯一；覆盖矩阵完整 |
| tasks.md | Phase 3 | checkbox 格式；按 capability 分组 |
| slices.md | Phase 3 | 依赖无循环；P0 优先 |
| design-adjustments.md | Phase 5 | 原始设计引用 + 调整原因 + 影响范围 |
| test-report.md | Phase 5 | 失败项有根因；通过率计算正确 |

---

## 6. 开发规范 / Development Standards

Phase 4 (BUILD) 开始前，Skill 必须先读取对应开发语言的规范文件。
Before Phase 4 begins, the Skill must read the standard file for the target language.

```
.stdd/standards/
├── python.md        # Python 开发规范（默认 / Default）
├── java.md          # Java 开发规范（后续 / Planned）
├── rust.md          # Rust 开发规范（后续 / Planned）
└── go.md            # Go 开发规范（后续 / Planned）
```

**Python 规范包含 / Python Standard Covers**：代码风格（ruff、命名约定、import 顺序）、类型注解、异步编程、错误处理、日志规范、测试代码规范、代码审查清单。
Code style (ruff, naming, imports), type annotations, async programming, error handling, logging, test conventions, review checklist.

更多细节见模板文件 / See template file for details: `.stdd/standards/python.md`

---

## 7. 跨平台设计 / Cross-Platform Design

### 7.1 策略 / Strategy

```
STDD 核心（平台无关）                 平台适配层（最小化）
Platform-agnostic core               Minimal platform adapter
─────────────────────────           ──────────────────────────
.stdd/                              .stdd/platforms/
├── skills/         ←──────┬──→     ├── claude-code/skills/   # YAML frontmatter
├── templates/              ├──→    ├── workbuddy/skills/     # YAML frontmatter + trigger_keywords
├── standards/              ├──→    ├── trae/skills/
├── config.yaml             │       └── cursor/               # 单文件规则 / Single rule file
│                           │
STDD.md (通用 fallback) ────┘       # 无 Skill 系统的平台用 / For platforms without skill systems
```

### 7.2 支持的平台 / Supported Platforms

| 平台 / Platform | Skill 机制 | 安装方式 / Install | 调用方式 / Invocation |
|----------------|-----------|-------------------|----------------------|
| Claude Code | SKILL.md | `stdd install claude-code` | `/stdd-xxx` |
| WorkBuddy | SKILL.md + frontmatter | `stdd install workbuddy` | 关键词触发 / Keyword trigger |
| Trae | SKILL.md | `stdd install trae` | `/stdd-xxx` |
| Cursor | Rules | `stdd install cursor` | 自动加载 / Auto-load |
| Windsurf | Rules | 手动复制 / Manual copy | `.windsurfrules` |
| Copilot | Instructions | 手动复制 / Manual copy | `.github/copilot-instructions.md` |

### 7.3 核心 Skill 设计原则 / Core Skill Design Principles

为确保跨平台兼容，核心 Skill 文件遵循以下原则：
To ensure cross-platform compatibility, core Skill files follow these principles:

- 不引用特定平台工具名（如 "AskUserQuestion"），写"暂停并等待用户确认"。
  No platform-specific tool names; write "pause and wait for user confirmation".
- 用通用动词描述操作（"执行命令"而非"Bash"）。
  Use generic verbs ("run command" not "Bash").
- 步骤描述**要做什么**，而非用什么工具做。
  Describe **what to do**, not which tool to use.

---

## 8. CLI 辅助脚本 / CLI Helper Script

STDD 提供 Python CLI 脚本处理程序化操作。Skill 负责"怎么想"，CLI 负责"做什么结构性操作"。
The Python CLI handles programmatic operations. Skills handle "how to think", CLI handles "what structural operations to do".

### 命令列表 / Command List

| 命令 / Command | 功能 / Function |
|---------------|----------------|
| `stdd init` | 初始化 .stdd/ 目录 + specs/changes/archive 骨架 |
| `stdd install <platform>` | 安装 skills 到目标 AI 平台 |
| `stdd new <name>` | 创建 change 目录骨架（从模板） |
| `stdd validate [name]` | 验证 change 结构完整性 + spec 格式 + TC-ID 唯一性 |
| `stdd status [name]` | 显示当前变更的阶段和状态 |
| `stdd archive <name>` | 归档 change 到 archive/ + 合并 specs 到 specs/ |
| `stdd trace <tc-id>` | 追溯 TC-ID 的 spec↔test↔code 映射链 |

### 依赖 / Dependencies

- Python 3.10+
- PyYAML 6.0+

---

## 附录 A. 用户交互协议 / User Interaction Protocol

在强制确认门处，Skill 向用户展示标准化的确认消息。
At each mandatory gate, the Skill presents a standardized confirmation message.

**确认消息格式 / Confirmation Format**：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD Phase <N>: <阶段名> — 等待确认 / Awaiting Confirmation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 产出物 / Artifacts:
  ✅ proposal.md (已生成 / Generated)
  ✅ design.md (已生成 / Generated)
  ...

📊 关键指标 / Key Metrics:
  - Spec Scenarios: N
  - TC Cases: N

⚠️ 需要你确认的内容 / Items to Confirm:
  1. ...
  2. ...

👉 请回复「确认」继续，或提出修改意见。
   Reply "confirm" to proceed, or provide feedback.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**用户响应处理 / User Response Handling**：

| 用户输入 / Input | 行为 / Behavior |
|----------------|----------------|
| "确认" / "OK" | 锁定当前阶段，进入下一阶段 / Lock phase, advance |
| 具体修改意见 / Specific feedback | 修订文档，重新展示 / Revise & re-present |
| "回到 Phase N" / "Back to Phase N" | 回到指定阶段重新开始 / Return to specified phase |
| "暂停" / "Pause" | 保存状态，等待 /stdd-continue / Save state, await /stdd-continue |

---

## 附录 B. 状态机 / State Machine

```
                    ┌─────────┐
                    │  IDLE   │
                    └────┬────┘
                         │ /stdd-understand
                         ▼
                    ┌───────────┐
                    │ UNDERSTAND│──→ 用户确认 → completed
                    └────┬──────┘
                         │ /stdd-spec
                         ▼
                    ┌───────────┐
              ┌──→  │   SPEC    │──→ 用户确认 → completed
              │     └────┬──────┘
              │          │ 模式选择 (Gate 2 后)
              │          ▼
              │     ┌─────────────────────┐
              │     │  长程模式?           │
              │     │  Long-Range Mode?   │
              │     └────┬────────┬───────┘
              │          │ 是     │ 否
              │          ▼        ▼
              │     ┌────────┐  ┌────────┐
              │     │一次性   │  │ 普通   │
              │     │预授权   │  │ 模式   │
              │     └───┬────┘  └───┬────┘
              │         └────┬─────┘
              │              ▼
              │     ┌───────────┐
              │     │   SLICE   │──→ auto-completed
              │     └────┬──────┘
              │          │ /stdd-build (auto)
              │          ▼
              │     ┌───────────┐
              │     │   BUILD   │──→ auto-completed
              │     │(长程:自动 │     (降级时暂停)
              │     │ 处理偏离) │
              │     └────┬──────┘
              │          │ /stdd-verify (auto)
              │          ▼
              │     ┌───────────┐
              │     │  VERIFY   │──→ 用户确认(Gate 3) → completed
              │     │(长程:10轮)│     (两种模式均强制)
              │     └────┬──────┘
              │          │
              │     ┌────┴────┐
              │     │         │
              │   有异议    确认通过
              │   Disagree  Confirmed
              │     │         │
              └─────┘         ▼
                         ┌─────────┐
                         │ DELIVER │──→ auto-completed
                         └─────────┘
```
