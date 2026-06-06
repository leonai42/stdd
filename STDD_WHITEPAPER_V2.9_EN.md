# STDD V2.9 White Paper

> **Version: V2.9.3 | Internal Use | Public Release at V3.0**
>
> This document is the complete reference for STDD (Specification-Driven Test-Driven Development) V2.9.
> Covers all CLI commands, the six-phase workflow, intelligent guard, dual-track documents,
> experience library, configuration system, and platform adapters.
>
> Principle: Self-contained — find any functional detail without reading source code.

---

## Table of Contents

- [Part 0: Front Matter](#part-0-front-matter)
- [Part 1: Overview](#part-1-overview)
- [Part 2: Six Phases in Detail](#part-2-six-phases-in-detail)
- [Part 3: Key Mechanisms](#part-3-key-mechanisms)
- [Part 4: Quality System](#part-4-quality-system)
- [Part 5: Spec Anchoring](#part-5-spec-anchoring)
- [Part 6: Core Subsystems](#part-6-core-subsystems)
- [Part 7: CLI Complete Reference](#part-7-cli-complete-reference)
- [Part 8: Configuration System](#part-8-configuration-system)
- [Part 9: Platforms & Standards](#part-9-platforms--standards)
- [Part 10: Version History & Future](#part-10-version-history--future)
- [Part 11: Appendices](#part-11-appendices)

---

## Part 0: Front Matter

### Ch00 Version Declaration & Document Conventions

#### Version Declaration

This document corresponds to **STDD V2.9.3**. The V2.9.x series is for internal use; public release will accompany V3.0.

The white paper content is based on V2.9.3 source code. If discrepancies are found, the source code takes precedence.

#### Target Audience

- **STDD Users**: Need to look up command parameters or concept definitions
- **AI Agents (Claude Code / Cursor / Windsurf etc.)**: Need precise understanding of STDD mechanics to execute flows correctly
- **STDD Developers**: Need to understand the system's complete architecture and module relationships

#### Reading Conventions

| Marker | Meaning |
|--------|---------|
| `` `code` `` | Commands, filenames, field names, code snippets |
| **Bold** | Key concept first appearance |
| > Quote | Note, warning, or tip |

---

### Ch01 Glossary

> Terms grouped by functional domain. Format: **Term** (中文) — Definition.

#### Core Concepts

- **STDD** (规格驱动测试驱动开发) — Specification-Driven Test-Driven Development. An AI coding workflow governance framework.
- **Change** (变更) — STDD's basic work unit. Each change creates a `changes/<date>-<name>/` directory and follows the full six-phase flow.
- **Phase** (阶段) — Six workflow steps: UNDERSTAND → SPEC → SLICE → BUILD → VERIFY → DELIVER.
- **Capability** (能力) — An independent functional unit of a system. Each capability maps to one spec file.
- **Scenario** (场景) — Basic spec unit. Format: GIVEN → WHEN → THEN(SHALL) → AND(≤5 items).
- **TC-ID** (测试用例标识符) — Test case identifier. Format: `TC-<CAPABILITY>-<NNN>`, e.g. `TC-AUTH-001`. Defined in test-plan.md, referenced in test code, enabling Spec→Test traceability.
- **Mode** (执行模式) — Three tiers: lightweight / standard / thorough.
- **Task Type** (任务类型) — code / documentation / configuration / data-migration / dependency-upgrade.

#### Dual-Track Documents

- **Canonical YAML** — AI-consumable YAML format documents. Forms the dual-track system with Human View MD.
- **Human View** — Human-readable Markdown documents. Rendered one-way from Canonical YAML (irreversible).
- **DC-HASH** — Dual-track consistency hash. SHA-256 of YAML embedded in MD to verify synchronization.
- **DC-FIELD** — Dual-track field consistency check. Verifies that fields referenced in Human View exist in Canonical YAML.

#### Gates & Guard

- **Gate** (门) — Three mandatory confirmation points. Gate 1 (end of Phase 1) / Gate 2 (end of Phase 2) / Gate 3 (end of Phase 5). Must proceed sequentially.
- **Guard** (门禁) — Intelligent code editing gate. Auto-checks before Edit/Write operations. V2.9.3: four-level scope classifier (micro/small/medium/large).
- **PreToolUse Hook** — Claude Code's pre-edit interception hook. Runs `stdd guard check` before every Edit/Write; exit code 2 blocks the operation.
- **enforce_stdd** — Switch in project.yaml. When `false`, Guard is completely disabled. Default: `true`.

#### Quality System

- **Failure Mode** (失败模式) — 12 categories of common AI coding failures (a-l), checked systematically in Phase 5.
- **pass@k** — Statistical verification metric. Probability of passing at least once across k runs. Used to detect spec ambiguity: low pass@1 + high pass@k = imprecise spec.
- **Plankton** — Three-level auto-fix system. L1: silent fix (ruff format/fix/isort). L2: suggestion (missing type annotations, bare except). L3: report (bandit/pylint/mypy guidance).
- **Complexity Score** (复杂度评分) — 0-17 point assessment across 6 dimensions, used to recommend execution mode.

#### Experience & Context

- **Experience Library** (经验库) — 5-state lifecycle (discovered→verified→deposited→shared/merged→retired) AI coding experience management system.
- **Phase Context** — Cross-session recovery file. AI updates at end of each phase with key decisions, current state, and next actions.
- **Resume Context** — Recovery fields stored in .stdd.yaml.
- **State Freshness** — Compares saved git HEAD in .stdd.yaml with current HEAD to determine if resume state is still valid.
- **Hook** (生命周期钩子) — Three auto-triggered scripts: SessionStart (load state on startup) / PreCompact (save before compaction) / Stop (persist on exit).

#### Other

- **Long-Range Mode** (长程模式) — Optional after Gate 2. Pre-authorizes Phase 3-5 for automatic cross-session execution with periodic checkpoints.
- **Batch** (批次) — Lightweight change container. Multiple micro-fixes grouped into one `changes/_batch/<id>/` directory.
- **Skill** (技能) — Markdown files guiding AI through STDD process execution. 6 phase skills (understand/spec/slice/build/verify/deliver) plus `_shared/` fragments.
- **TDD** — Test-Driven Development. Phase 4 core methodology: RED (write failing test) → GREEN (write minimal implementation) → REFACTOR (optimize).
- **Design Adjustment** — Deviation from original design recorded during BUILD. minor: auto-record → continue. major: record → pause → user confirmation.

---

## Part 1: Overview

### Ch02 What is STDD

#### Definition

STDD = **Specification-Driven Test-Driven Development**.

STDD is an **AI coding workflow governance framework**. It is not a programming language, test framework, or IDE plugin — it is a process standard that defines "how AI should code" through CLI tools + Skill instructions + intelligent guard, ensuring every AI code modification has a target, constraints, and verification.

#### Three Core Problems Solved

1. **Unreliable AI Output**: AI-generated code appears correct but behavior doesn't match expectations. STDD's Spec → Implement → Verify closed loop ensures code behavior aligns with requirements.

2. **Untraceable AI Operations**: AI changed code but there's no record of why, what was changed, or how it was verified. STDD's Change lifecycle provides complete traceability from proposal to test-report.

3. **Process Consistency Depends on User Skill**: AI behavior varies across users and sessions. STDD codifies processes into Skill files and Guard enforcement, providing consistent execution standards.

#### Relationship to Other Methodologies

| Methodology | Core Concept | STDD Relationship |
|-------------|-------------|-------------------|
| **TDD** (Test-Driven Development) | Test-first coding | Phase 4 BUILD is TDD: RED→GREEN→REFACTOR |
| **BDD** (Behavior-Driven Development) | GIVEN/WHEN/THEN behavior description | STDD's Spec format (Scenario) directly adopts BDD style |
| **DDD** (Domain-Driven Design) | Business domain modeling drives design | STDD's Capability concept maps to DDD's Bounded Context |

STDD's uniqueness: **integrating these three into an AI agent's native operating system, rather than external documentation for human developers**.

#### Design Philosophy

```
Define(Specify) → Execute(Execute) → Verify(Verify) → Learn(Learn)
     ↑                                                    ↓
     └──────────── Experience Feedback ←──────────────────┘
```

- **Define**: Write testable Spec for "what to do"
- **Execute**: Implement per slice using TDD
- **Verify**: Automated checks + failure mode inspection
- **Learn**: Distill discovered issues into experiences, feed back into next Spec

---

### Ch03 Nine Core Principles

1. **Spec-First** (规格先行): Write spec before code. `❌ Need→Code  ✅ Need→Spec→Confirm→Code`
2. **TDD Execution** (红绿重构): Every slice follows RED → GREEN → REFACTOR, non-skippable
3. **Traceable Adjustments** (可追溯调整): Every design deviation must be recorded to pending-adjustments.yaml
4. **User-Confirmation-Driven** (Gate确认驱动): Three Gates cannot be skipped; confirmation authority rests with the user
5. **Template-First** (模板先行): All deliverables start from 17 templates, ensuring structural consistency
6. **Vertical Slicing** (垂直切片): Slice by function (end-to-end increment), not by layer
7. **Test Coverage Mandate** (强制测试覆盖): Every Scenario must have a corresponding test; tracked in .stdd.yaml's traceability.tc_cases
8. **Behavior-Not-Implementation** (行为测试): Test "what the system should do" (behavior), not "how it does it internally" (implementation)
9. **Self-Learning** (经验自学习): Extract experiences from failures; auto-load matching experiences in subsequent Phase 2 for prevention

---

### Ch04 Six-Phase Flow Overview

#### State Machine

```
                        ┌─────────────┐
                        │ UNDERSTAND  │  Phase 1: Requirement Understanding
                        │  Explore→    │  → proposal.md
                        │  Proposal    │
                        └──────┬──────┘
                               │  Gate 1: Confirm scope/boundaries
                               │  Complexity score → Mode recommendation
                        ┌──────▼──────┐
                        │    SPEC     │  Phase 2: Spec Design
                        │  Spec→      │  → design.md + spec.yaml
                        │  Design     │     + test-plan.md
                        └──────┬──────┘
                               │  Gate 2: Confirm technical decisions
                               │  Mode selection (long-range/normal)
                        ┌──────▼──────┐
                        │   SLICE     │  Phase 3: Slice Planning
                        │  Analyze→   │  → slices.md + tasks.md
                        │  Group      │
                        └──────┬──────┘
                               │  (Long-range: auto-enter next phase)
                        ┌──────▼──────┐
                        │   BUILD     │  Phase 4: TDD Implementation
                        │  RED→GREEN  │  → code + pending-adjustments
                        │  →REFACTOR  │
                        └──────┬──────┘
                               │  (Long-range: auto-enter next phase)
                        ┌──────▼──────┐
                        │   VERIFY    │  Phase 5: Quality Verification
                        │  Test→      │  → test-report.md
                        │  Review     │
                        └──────┬──────┘
                               │  Gate 3: Final quality confirmation
                        ┌──────▼──────┐
                        │  DELIVER    │  Phase 6: Delivery
                        │  Archive→   │  → archive/ + specs/
                        │  Merge      │
                        └─────────────┘
```

#### Deliverables per Phase

| Phase | Name | Key Deliverables | Gate |
|-------|------|-----------------|------|
| 1 | UNDERSTAND | proposal.md (or proposal.yaml) | Gate 1 |
| 2 | SPEC | design.md, spec.yaml, agent_spec.yaml, test-plan.md | Gate 2 |
| 3 | SLICE | slices.md, tasks.md | — |
| 4 | BUILD | Code files, pending-adjustments.yaml | — |
| 5 | VERIFY | test-report.md, design-adjustments.yaml | Gate 3 |
| 6 | DELIVER | archive/ directory, merged specs/ | — |

#### Three Execution Modes — Selection Point

Mode selection occurs **after Gate 1, before Gate 2**. Phase 1 complexity scoring (0-17) provides a recommendation; the user confirms or overrides at Gate 2.

| Mode | Score Range | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|------|------------|---------|---------|---------|---------|---------|
| Lightweight | 0-3 | Simplified | Skip | Simple TDD | 1 agent + 5 modes | Batch append |
| Standard | 4-7 | Full | Smart slice | Full TDD | 3 agents + 12 modes | Full archive |
| Thorough | 8+ | Full + advanced | Parallel | TDD + pass@k | 3 agents + security + perf | Full + release notes |

---

## Part 2: Six Phases in Detail

### Ch05 Phase 1: UNDERSTAND (Requirement Understanding)

#### Objective

Transform vague requirements into a clear, verifiable change proposal.

#### Execution Flow (6 Steps)

**Step 1: Problem Exploration**
- Understand the problem or requirement described by the user
- Clarify scope boundaries: what's in scope, what's not
- Identify stakeholders and constraints

**Step 2: Read Template**
- Read `.stdd/templates/canonical/proposal.yaml` (V2.9.2 YAML-First)

**Step 3: Draft proposal.yaml**
- Fill in the Canonical proposal.yaml template:
  - `meta`: change_id, title, created, status
  - `why`: problem (the problem to solve)
  - `what_changes`: list of change items
  - `capabilities`: new + modified capabilities
  - `constraints`: technical/time/resource constraints
  - `stakeholders`: stakeholders
  - `risk_areas`: risk areas
  - `non_goals`: explicitly out of scope
  - `success_criteria`: verifiable success criteria

**Step 4: Auto-Review**
- Check proposal completeness and consistency
- Verify success_criteria are verifiable

**Step 5: Complexity Scoring → Mode Recommendation**
- 6-dimension scoring (see Ch13 for details), 0-17 points
- Recommended mode: 0-3=lightweight / 4-7=standard / 8+=thorough
- User can override recommendation at Gate 2

**Step 6: Gate 1 Confirmation**
- Present proposal summary to user
- Confirm: scope, boundaries, success criteria
- User response: confirm / feedback / back / pause

#### Deliverables

- `proposal.md` (or proposal.yaml) + `.stdd.yaml` updated (understand → completed)

---

### Ch06 Phase 2: SPEC (Specification Design)

#### Objective

Transform the proposal into testable behavior specs and verification specs.

#### Execution Flow

**Step 1: CLI Structured Extraction**
- `stdd extract-proposal` — extract structured proposal data

**Step 2: Experience Load + Cross-Check**
- `stdd experience list --language <lang> --format json`
- Filter by lifecycle_state ≥ verified
- Match pattern/root_cause against current capabilities
- Load up to 10 matching experiences

**Step 3: Technical Design (design.md)**
- Context: current system state, constraints
- Decisions: key technical decisions (with alternatives and rationale)
- Architecture: module decomposition, data flow
- Risks/Trade-offs: risks and trade-offs

**Step 4: Generate Specifications (Canonical YAML + Human View)**

| Sub-step | Coding Task | Non-Coding Task |
|----------|------------|-----------------|
| 4a | Read spec.yaml + agent_spec.yaml templates | Read agent_spec.yaml template |
| 4b | Generate spec.yaml per Capability (Scenario: GIVEN/WHEN/THEN/AND) | Skip |
| 4c | Generate agent_spec.yaml (CPs map to Scenarios) | Generate agent_spec.yaml (CPs are the spec itself) |
| 4d | Render Human View spec.md | Render Human View |

**Step 4.5: Anchoring Assessment**
- Evaluate anchoring level (L1-L4, see Ch27-28) for each Requirement
- Warn if critical/safety changes have insufficient anchoring

**Step 5: Test Plan (test-plan.md)**
- Test strategy, TC case inventory
- TC-ID format: `TC-<CAPABILITY>-<NNN>`
- Ensure TC count ≥ Scenario count

**Step 6: Gate 2 + Mode Selection**
- Present design.md + spec summary to user
- Mode selection: lightweight/standard/thorough (user confirms or overrides recommendation)
- Optional: enable long-range mode (Phase 3-5 auto-execution)
- After confirmation, mode is locked; cannot be changed in subsequent Phases

#### Deliverables

`design.md`, `spec.yaml` (coding), `agent_spec.yaml`, `test-plan.md`, `.stdd.yaml` updated

---

### Ch07 Phase 3: SLICE (Slice Planning)

#### Objective

Decompose spec into independently implementable development slices, determine execution order.

#### V2.9.2 Canonical-First Reading

1. Read `spec.yaml` (Canonical) first, fall back to `spec.md` (Human View)
2. Read `agent_spec.yaml` (verification spec)
3. Read `test-plan.md`

#### 5-Step Slice Analysis

1. **Dependency Graph Analysis**: `stdd dependency-graph --format json`, identify dependencies
2. **Risk Assessment**: Label each slice with risk level (high/medium/low)
3. **Effort Estimation**: Label each slice with effort (large/medium/small)
4. **Grouping**: Group by functional cohesion, identify parallelizable slices (parallel_group)
5. **Topological Sort**: Dependency graph → execution order, P0 first

#### Three-Mode Differences

| Mode | SLICE Behavior |
|------|---------------|
| Lightweight | **Skip this Phase**: 1 implicit slice, go directly to Phase 4 |
| Standard | Smart slicing: 5-step analysis |
| Thorough | Standard + parallelization identification + pass@k=3 configuration |

#### Deliverables

`slices.md` (slice execution plan), `tasks.md` (task checklist), `.stdd.yaml` updated

---

### Ch08 Phase 4: BUILD (TDD Implementation)

#### Objective

Implement slice by slice, passing tests at each step.

#### Step -1: Context Budget Check

- Estimate current context usage
- If >80%, prompt user or auto-compress

#### Step 0: Load Resources

1. Read `project.yaml` → get language
2. Load language standard `.stdd/standards/<lang>.md`
3. Load project rules `.stdd/rules/<lang>/*.md`
4. Load phase-context.md (if exists)
5. Load matching experience entries (max 10)
6. Generate code structure delta: `stdd structure delta <change>`

#### Step 1: Per-Slice TDD Loop

```
Per slice cycle:
  RED    → Write failing test (based on spec Scenario THEN)
  GREEN  → Write minimal implementation to pass test
  REFACTOR → Refactor and optimize
```

#### Step 1.4: Slice Verification

After each slice completion, verify:
- TC coverage 100% (all Scenarios have corresponding tests)
- Deliverable check (files exist, format correct)
- All tests passing

#### Step 1.5: Parallel Slice Merge

After all parallel-group slices complete, merge verification: no conflicts, no regressions.

#### Design Deviation Handling

| Level | Condition | Handling |
|-------|-----------|----------|
| minor | Implementation detail adjustment, doesn't affect spec Scenario | Auto-record to pending-adjustments.yaml |
| major | Changed spec Scenario behavior | Record → Pause → Ask user → May need spec update |

#### Three-Mode Differences

| Mode | BUILD Behavior |
|------|---------------|
| Lightweight | 1-2 focused tests, skip REFACTOR |
| Standard | Full RED→GREEN→REFACTOR |
| Thorough | Standard + pass@k verification |

#### Deliverables

Code files, `pending-adjustments.yaml`, `.stdd.yaml` updated

---

### Ch09 Phase 5: VERIFY (Quality Verification)

#### Objective

Comprehensively verify code quality and spec compliance.

#### Execution Flow

**Step -1: Context Budget Check**

**Step 0: Multi-Agent Parallel Review**

| Agent | Responsibility | Model |
|-------|---------------|-------|
| security-reviewer | Security vulnerability detection (injection, path traversal, auth) | Opus |
| perf-analyzer | Performance bottleneck identification | Sonnet |
| compat-checker | Compatibility checking | Sonnet |

Lightweight mode: 1 agent only.

**Step 1: Test Execution**

Execute per `.stdd/config.d/quality.yaml` configuration, in order:

1. `pytest` — unit tests + coverage (default target 80%)
2. `coverage` — coverage report
3. `ruff check` — lint check
4. `mypy` — type check (Python)
5. Multi-version tests (e.g., Python 3.10/3.11/3.12)
6. E2E tests (if enabled)

**Step 2: Diff Review**

`stdd diff` — detect Spec↔Test coverage gaps.

**Step 3: Twelve Failure Mode Checks**

Check each category (see Ch21 for details). Lightweight mode: 5 core checks; Standard/Thorough: all 12.

**Step 4: Design Adjustment Summary**

1. Read `pending-adjustments.yaml` recorded during Phase 3-4
2. Generate `design-adjustments.yaml` per Canonical template
3. Render `design-adjustments.md` (Human View)
4. If `requires_re_spec` → flag as next round's proposal input (closed loop)

**Step 5: Gate 3 Confirmation**

Present test-report.md + design-adjustments.md to user.

#### Iteration Control

| Mode | Max Iterations | Behavior |
|------|---------------|----------|
| Lightweight | 3 | Report on cap |
| Standard | 5 | Report on cap |
| Thorough | 10 | Report on cap |

#### Deliverables

`test-report.md`, `design-adjustments.yaml/.md`, `.stdd.yaml` updated

---

### Ch10 Phase 6: DELIVER (Delivery)

#### Objective

Archive change, merge specs, update documentation.

#### Execution Steps

1. **Archive**: `stdd archive <change> --yes`
   - Move change to `archive/`
   - Merge specs to project-level `specs/` (unless `--skip-specs`)

2. **Canonical YAML Merge**:
   - Merge `proposal.yaml` → `canonical/proposals/`
   - Merge `agent_spec.yaml` → `canonical/specs/agent/`
   - `stdd canon verify <change>` — verify dual-track consistency
   - Update `.canon-index.yaml`

3. **Code Structure Merge**: `stdd structure merge <change>`

4. **Git Commit + Tag**: Version tag (if configured)

#### Three-Mode Differences

| Mode | DELIVER Behavior |
|------|-----------------|
| Lightweight | Batch append (not standalone archive) |
| Standard | Full archive + specs merge |
| Thorough | Standard + release notes |

#### Deliverables

`archive/<change>/`, merged `specs/`, updated `canonical/`

---

## Part 3: Key Mechanisms

### Ch11 Three Mandatory Confirmation Gates

#### Gate Positions and Confirmation Content

| Gate | Timing | Confirms |
|------|--------|----------|
| Gate 1 | End of Phase 1 | proposal.md: scope, boundaries, success criteria |
| Gate 2 | End of Phase 2 | design.md + spec + test-plan: core technical decisions |
| Gate 3 | End of Phase 5 | test-report.md + design-adjustments.md: final quality review |

#### Three Confirmation Channels (equivalent, all write the same confirmed_at timestamp)

| Channel | Method |
|---------|--------|
| **dialog** | AI prints confirmation prompt, user replies via text |
| **file_token** | Create `GATE<N>_APPROVED` empty file in change directory |
| **cli** | `stdd gate approve --gate <N> [name]` |

#### Rules

- Gate order enforced: Gate 2 must come after Gate 1
- Idempotent: re-confirming returns existing timestamp
- Non-skippable

---

### Ch12 Three Execution Modes

#### Full Comparison Table

| Dimension | Lightweight (0-3 pts) | Standard (4-7 pts) | Thorough (8+ pts) |
|-----------|----------------------|---------------------|-------------------|
| Phase 2 SPEC | Skip design/test-plan/anchoring | Full spec | Full + confidence labels |
| Phase 3 SLICE | Skip (1 implicit slice) | Smart slicing | Slice + parallelization |
| Phase 4 BUILD | 1-2 focused tests, skip REFACTOR | Full RED→GREEN→REFACTOR | Full + pass@k |
| Phase 5 VERIFY | 1 review agent, 5 failure modes | 3 agents, 12 failure modes | 3 agents + security/perf sub-agents |
| Phase 6 DELIVER | Batch append | Full archive | Full + release notes |
| **TDD Baseline** | **Must RED→GREEN** | **Must RED→GREEN** | **Must RED→GREEN** |

#### Mode Selection Flow

```
Phase 1 Complexity Score → Recommended Mode
         ↓
Phase 2 Gate 2 → User confirms or overrides
         ↓
Phase 3+ → Locked, cannot be changed
```

#### task_type Support

| task_type | SPEC Strategy | VERIFY Strategy |
|-----------|--------------|-----------------|
| `code` | spec.yaml + agent_spec.yaml | pytest + coverage + lint |
| `documentation` | agent_spec.yaml (CPs are spec) | Content check + cross-reference |
| `configuration` | agent_spec.yaml | Config validation |
| `data-migration` | agent_spec.yaml | Data integrity check |
| `dependency-upgrade` | agent_spec.yaml | Compatibility test |

---

### Ch13 Complexity Scoring Model

#### 6 Scoring Dimensions (0-17 total)

| Dimension | Weight | Low (0) | Medium (1) | High (2-3) |
|-----------|--------|---------|------------|------------|
| Impact Scope | 3 | Single file | Multi-file same module | Cross-module/system |
| Technical Complexity | 3 | Simple CRUD | Algorithm/concurrency | Distributed/security |
| Test Complexity | 3 | Unit test | Integration test | E2E + multi-version |
| Dependency Count | 3 | 0-1 | 2-4 | 5+ |
| Risk Level | 3 | Low | Medium | High/critical |
| Documentation Needs | 2 | Code comments only | Update existing docs | New doc system |

#### Thresholds

| Total | Mode | Description |
|-------|------|-------------|
| 0-3 | Lightweight | Bug fixes, small tweaks |
| 4-7 | Standard | Feature enhancements, medium refactors |
| 8-17 | Thorough | New modules, architecture changes, safety-critical |

Score confidence: `preliminary` / `confirmed`.

---

### Ch14 Design Adjustment Traceability

#### Deviation Classification

| Level | Definition | Handling |
|-------|-----------|----------|
| **minor** | Implementation detail, doesn't affect spec Scenario | Auto-record → Continue |
| **major** | Changed spec behavior, interface, or data structure | Record → Pause → User confirm |

#### File Lifecycle

```
Phase 4: pending-adjustments.yaml  ← Continuous recording (per slice)
              ↓
Phase 5: design-adjustments.yaml   ← Summary + classification
              ↓
         design-adjustments.md     ← Human-readable version
```

---

### Ch15 Bidirectional Traceability Chain

#### Spec → TC → Test → Code Four-Layer Traceability

```
Spec Scenario "User login success"
  → TC-AUTH-001 Login Success
    → test_login_success() @ tests/test_auth.py:45
      → src/auth/login.py:login()
```

#### Key Commands

- `stdd trace <tc-id>` — Trace TC-ID across four layers
- `stdd diff [name]` — Spec↔Test↔Code coverage gap table

#### .stdd.yaml traceability Fields

```yaml
traceability:
  spec_scenarios: 8    # Total Spec Scenarios
  tc_cases: 8          # Total TC-IDs
  test_functions: 8    # Total test functions
```

---

### Ch16 Long-Range Mode

#### Enabling Conditions

- Optional after Gate 2
- `.stdd.yaml` key: `long_range.enabled: true`
- Pre-authorizes Phase 3-5

#### Pre-Authorization Scope (from long_range.yaml)

| Operation Category | Permission | Description |
|-------------------|------------|-------------|
| directory | allow | Create/delete directories |
| file_write | allow | Write files |
| file_read | allow | Read files |
| command_exec | allow | Execute commands |
| script_exec | allow | Execute scripts |
| network | allow | Network access |
| git_readonly | allow | Git read-only operations |

#### Degradation Triggers

| Condition | Threshold |
|-----------|-----------|
| Consecutive failures | 3 times |
| Pass rate | < 95% |
| Safety check | Triggered |

On degradation: auto-switch to normal mode, wait for user confirmation.

#### Gate 3 Remains Mandatory

Even in long-range mode, Gate 3 is still enforced — final delivery must have user confirmation.

---

### Ch17 Batch Directory Management

#### Problem

In lightweight mode, each micro-fix as a separate change directory would cause directory explosion.

#### Three Strategies

| Strategy | Naming | Example | Best For |
|----------|--------|---------|----------|
| `monthly` (default) | YYYY-MM-DD | 2026-06-06 | Daily use |
| `weekly` | YYYY-Www-MMDD | 2026-W23-0606 | Weekly iterations |
| `count_based` | batch-NNN | batch-001 | Non-time-based |

#### Directory Structure

```
changes/_batch/
  <batch-id>/
    .stdd.yaml          # batch_id, batch_type, items, closed_at
    items/              # Micro-change items
    archive-summary.md  # Generated on close
```

#### Anti-Collision

Same-day multiple opens → `YYYY-MM-DD-HHMM` suffix

#### Configuration

```yaml
# lite.yaml
batch:
  strategy: monthly
  max_items: 20
```

---

### Ch18 Context Engineering

#### phase-context.md

- AI updates at end of each phase
- Structure: completed phase sections (1-5) + current phase section
- Content: key decisions, user concerns, known pitfalls, next steps
- Length cap: ~200 lines (within 5% of context)

#### Context Budget Check

- Executed at Phase 4/5 Step -1
- Estimate current context usage
- >80% → prompt compression or manual cleanup

#### Cross-Session Recovery

1 read of `phase-context.md` → combined with `stdd state --resume --compact` → full context recovery

#### State Freshness

`stdd state --resume` auto-compares:
- `.stdd.yaml` key: `state_freshness.git_head`
- Current `git rev-parse --short HEAD`

Outputs `STALE` warning when mismatch detected.

---

### Ch19 Lifecycle Hooks

#### Three Hooks

| Hook | Trigger | Script | Behavior |
|------|---------|--------|----------|
| **SessionStart** | Session start | `session-start.py` | Scan changes/, print active change status line |
| **PreCompact** | Claude Code context before compaction | `pre-compact.py` | Save `.stdd.yaml` last_modified timestamp |
| **Stop** | Session end | `session-end.py` | Report experience library stats, suggest `stdd experience curate` |

#### Installation

```bash
stdd hooks install --force    # Write scripts + configure settings.local.json
stdd hooks status             # View installed hooks
stdd hooks uninstall          # Remove hook configuration
```

#### Claude Code Configuration

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

### Ch20 Project-Level Intelligent Guard

#### Three-Layer Architecture

| Layer | Mechanism | Effect |
|-------|-----------|--------|
| Layer 1 | AGENTS.md / STDD.md directive injection | AI behavior constraint (soft) |
| Layer 2 | PreToolUse Hook | Pre-edit auto-check (hard) |
| Layer 3 | `stdd guard` CLI | Manual check + status query |

#### V2.9.3 Intelligent Scope Classifier

No longer just allow/block — now analyzes change scope and gives intelligent recommendations.

**Four-Level Classification:**

| Level | Keyword Signals | Score | Behavior |
|-------|----------------|-------|----------|
| micro | 修复(fix), bug, typo... | <3 | Suggest batch |
| small | 优化(optimize), 调整(adjust), UI... | 3-9 | batch OK |
| medium | 重构(refactor), 模块(module), 数据处理(data)... | 10-19 | batch warning |
| large | 重写(rewrite), 架构(arch), API, 引擎(engine)... | ≥20 | batch blocked, require full STDD |

**Batch Hard Limits:** Files >5 warn, >10 block; Open >2 hours warn.

#### Guard Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| check | `stdd guard check --platform claude-code` | Exit code 0=allow, 2=block |
| status | `stdd guard status` | Show enforce, scope, recommended mode |
| init | `stdd guard init` | Deploy PreToolUse Hook |
| disable | `stdd guard disable` | Temporarily remove Hook |
| enable | `stdd guard enable` | Re-enable (= init) |

#### Configuration

```yaml
# project.yaml
enforce_stdd: true     # Guard switch
allow_bypass: false    # Allow bypass
```

---

## Part 4: Quality System

### Ch21 Twelve Failure Modes

Checked in Phase 5 Step 3. Each has: name, definition, detection trigger, typical example, fix template.

| ID | Name | Definition | Detection Trigger |
|----|------|-----------|-------------------|
| (a) | **Hallucinated Actions** | Non-existent file paths, env vars, function names, library APIs | grep can't find referenced paths/vars |
| (b) | **Scope Creep** | Modified files beyond planned scope | git diff --stat exceeds declared files |
| (c) | **Cascading Errors** | Silently swallowed exceptions, empty-array masking | bare `except Exception`, empty list defaults |
| (d) | **Context Loss** | Implementation contradicts proposal/design/spec | Cross-compare produced code vs spec |
| (e) | **Tool Misuse** | Wrong tool or parameter selection | Command syntax errors, version mismatch |
| (f) | **Runtime Behavior Deviation** | Static structure correct but dynamic behavior wrong | Test coverage sufficient but E2E fails |
| (g) | **Pipeline Break** | Multi-step conversion missing intermediate steps | Incomplete data flow |
| (h) | **Content Quality Deviation** | Data inconsistency, length overflow, missing references | Output format doesn't match spec |
| (i) | **Instruction Decay** | AI failed to execute explicitly given prompt instructions | Compare prompt instructions vs actual output |
| (j) | **Coverage Vacuum** | Zero test coverage for a capability | Coverage report shows 0% |
| (k) | **Contract Gap** | Inconsistent interface field names/types across capabilities | Compare API definitions vs actual calls |
| (l) | **Anchoring Deficit** | Critical/safety change has insufficient anchoring level | Check anchoring assessment results |

#### Lightweight Mode Subset

Lightweight mode only checks core 5 items: (a)(b)(c)(e)(f).

---

### Ch22 pass@k Statistical Verification

#### Principle

Same test run k times, probability of "passing at least once".

```
pass@1 = 0.3  → Single-pass rate 30%
pass@k = 0.95 → 95% chance of passing at least once in k runs
```

**Interpretation:** low pass@1 + high pass@k = **Spec is not precise enough**, AI is "guessing" the right answer.

#### Configuration

```yaml
# quality.yaml
pass@k:
  enabled: true
  k_values: [1, 3]     # Standard k=1, Thorough k=3
  threshold: 0.8
```

#### k Values by Mode

| Mode | k Value | Description |
|------|---------|-------------|
| Lightweight | Skip | |
| Standard | k=1 | Single pass confirmation |
| Thorough | k=3 | pass@k ambiguity detection |

---

### Ch23 Plankton Multi-Level Auto-Fix

#### Three-Level System

| Level | Name | Behavior | Trigger |
|-------|------|----------|---------|
| **L1** | Silent Fix | `ruff format .` + `ruff check --fix .` + `isort .` | Phase 5 auto |
| **L2** | Suggestion | Scan Python files: missing type annotations, bare `except Exception`, missing CancelledError in async def | Manual or auto |
| **L3** | Report | Prompt to manually run bandit/pylint/mypy, never auto-execute | Manual |

#### CLI

```bash
stdd fix --level 1    # Silent auto-fix
stdd fix --level 2    # Suggestion mode (max 20 suggestions)
stdd fix --level 3    # Report mode
```

---

### Ch24 Agent Verification Pipeline

#### Four Sub-Agents

| Agent | Responsibility | Default Model |
|-------|---------------|---------------|
| security-reviewer | Security vulnerabilities (injection, path traversal, auth, CVE) | Opus |
| perf-analyzer | Performance bottlenecks (N+1 queries, memory leaks, blocking I/O) | Sonnet |
| compat-checker | Compatibility (API changes, dependency versions, platform differences) | Sonnet |
| planner | Plan review (slice order, risk, resources) | Opus |

#### Checkpoint (CP) System

Checkpoints defined in agent_spec.yaml:

```yaml
steps:
  - id: CP-1
    description: "Verify user login flow"
    action: "pytest tests/test_auth.py -v"
    assertions:
      - type: "exit_code"
        expect: 0
      - type: "stdout_contains"
        expect: "test_login_success PASSED"
```

#### CLI

```bash
stdd agent verify [task] --cp CP-1    # Execute specific checkpoint
stdd agent verify [task]              # Execute all checkpoints
```

---

### Ch25 CI/CD Integration

#### Command Tree

```
stdd ci
  ├── init                          # Generate all CI config files
  ├── generate <target>             # Generate single config
  │   ├── workflow                  # GitHub Actions workflow
  │   ├── pre-commit                # .pre-commit-config.yaml
  │   └── pr-template               # PR comment template
  ├── check-failures [name]         # Full failure mode check
  ├── check-scope [name]            # Scope creep check (b)
  ├── check-coverage [name]         # Coverage vacuum check (j)
  └── check-contracts [name]        # Contract gap check (k)
```

#### Generated GitHub Actions Workflow

- Trigger: push / PR to main
- Steps: pytest + coverage + ruff + mypy
- All failure mode checks executed
- PR comment auto-outputs results

---

## Part 5: Spec Anchoring

### Ch26 Anchoring Overview

#### Problem

LLM non-determinism comes from ambiguity in Spec. The more vague the Spec, the larger the AI's "creative freedom" space, and the less predictable the output.

#### Solution

Constrain Spec through Anchoring to eliminate ambiguity sources: **replace abstract with concrete, description with example, pseudocode with code**.

#### Anti-Patterns

| Anti-Pattern | Example | Why Wrong |
|--------------|---------|-----------|
| Over-Anchoring | Specifying even variable names | Over-constrained, loses flexibility |
| Under-Anchoring | "Process user input" | Too vague, "process" has infinite implementations |
| Formalistic Anchoring | Copying RFC verbatim but Scenarios are hollow | Form without verification capability |

---

### Ch27 L1 Behavioral Anchoring

#### Rules

- THEN must contain **SHALL** (uppercase) for mandatory behavior
- Every Requirement ≥ 1 Scenario
- All boundary conditions must be covered

#### Applicability

**Default requirement for ALL changes.** L1 is the baseline; a Spec that fails L1 cannot pass Gate 2.

#### Example

```
❌ Requirement: System should correctly handle login
✅ Requirement: On successful login, system SHALL return a JWT access token (15 min validity)
   + Scenario: Username and password correct
   + Scenario: Username does not exist
   + Scenario: Password incorrect
   + Scenario: Account is locked
```

---

### Ch28 L2-L4 Advanced Anchoring

#### L2 Interface Anchoring

Define precise function signatures, API contracts, data schemas.

```yaml
# In spec.yaml
interface:
  function: "login(username: str, password: str) -> AuthResult"
  api: "POST /api/v1/auth/login"
  schema: "AuthResult { access_token: str, refresh_token: str, expires_in: int }"
```

#### L3 Pattern Anchoring

Reference proven implementation patterns (e.g., "Use Repository pattern"), with reference implementation links.

#### L4 Baseline Anchoring

Provide reference implementation code (baseline implementation) that AI starts from and modifies.

#### Applicability Criteria

| Change Type | Recommended Anchoring Level |
|-------------|---------------------------|
| General feature | L1 |
| Cross-system interface | L1 + L2 |
| Safety-critical | L1 + L3 |
| Financial/compliance | L1 + L4 |

---

## Part 6: Core Subsystems

### Ch29 Dual-Track Document System

#### Design

| Track | Format | Consumer | Role |
|-------|--------|----------|------|
| **Canonical** | YAML | AI Agents | Precisely consumable data source |
| **Human View** | Markdown | Humans | Readable rendered output |

#### Eight Core Rules

1. Canonical is the Single Source of Truth
2. Human View is **one-way** generated from Canonical (irreversible)
3. After YAML changes, MD must be regenerated
4. DC-HASH is embedded in MD for sync verification
5. canonical/ directory structure is standardized
6. `.canon-index.yaml` maintains file index
7. `stdd canon verify` auto-detects inconsistency
8. V2.9.2: YAML-First (YAML created before MD)

#### File Role Taxonomy

| Role | Marker | Meaning | Example |
|------|--------|---------|---------|
| Y | AI-Precisely Consumable | Canonical YAML | `proposal.yaml` |
| H | Human-Readable | Human View MD | `proposal.md` |
| F | Functional File | Template/Config | `.stdd/templates/` |
| T | Temporary | Intermediate artifact | `pending-adjustments.yaml` |
| C | Cumulative | Cross-Change accumulated | `.canon-index.yaml` |
| L | Lifecycle | State/Progress | `.stdd.yaml` |

---

### Ch30 Canonical YAML Format Specification

Canonical YAML has 5 core schemas + 1 index file, located in `.stdd/templates/canonical/`.

#### 1. proposal.yaml — Change Proposal

```yaml
meta: {change_id, title, created, status, version}
why: {problem}                    # Problem to solve
what_changes: [{description}]     # Change items
capabilities:
  new: [{name, description}]
  modified: [{name, description}]
constraints: []                   # Tech/time/resource constraints
stakeholders: []                  # Stakeholders
risk_areas: []                    # Risk areas
non_goals: []                     # Explicitly out of scope
critical: []                      # Critical dependencies/risks
anchoring: {level, justification}
success_criteria: []              # Verifiable criteria
```

#### 2. spec.yaml — Behavioral Spec (Coding Tasks)

```yaml
meta: {capability, change_id, created, confidence: high|medium|low}
requirements:
  - id: REQ-XXX
    description: ""               # One-sentence description
    scenarios:
      - id: SC-XXX
        confidence: high|medium|low
        evidence: ""              # Reference proposal paragraph
        given: ""
        when: ""
        then: ""                  # Contains SHALL
        and: []                   # ≤5 items
```

#### 3. agent_spec.yaml — Agent Verification Spec (All Tasks)

```yaml
meta: {task_id, change_id, created, task_type, system, description}
preconditions: []
steps:
  - id: CP-XX
    description: ""
    action: ""                    # Shell command
    assertions:
      - type: exit_code|stdout_contains|stderr_contains|file_exists
              |http_status|yaml_valid|link_alive|schema_valid|diff_empty
        expect: ...
```

#### 4. pending-adjustments.yaml — Design Deviations (Phase 4)

```yaml
meta: {change_id, updated_at}
adjustments:
  - id: ADJ-XXX
    original: ""                  # Original design reference
    actual: ""                    # Actual implementation
    reason: ""                    # Deviation reason
    severity: minor|major
    impact_scope: []              # Affected files/modules
    recorded_at: ""
```

#### 5. design-adjustments.yaml — Adjustment Summary (Phase 5)

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

#### 6. .canon-index.yaml — Index File

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
stdd canon init --change <name>              # Init canonical dir + YAML templates
stdd canon generate [name] --type proposal    # YAML → MD render
stdd canon verify <name>                      # Dual-track consistency check
```

---

### Ch31 Human View Generation Rules

#### Rendering Rules

`stdd canon generate` maps YAML fields directly to MD (no Jinja2 needed):

- `proposal.yaml` → `proposal.md`: why→##Why, what_changes→##What Changes, capabilities→###New/Modified, success_criteria→##Success Criteria
- `spec.yaml` → `spec.md`: requirements→###Requirement, scenarios→####Scenario (GIVEN/WHEN/THEN/AND)
- Each MD header embeds: `<!-- source_hash: <sha256> -->`, `<!-- generated_at: <iso> -->`, `<!-- canonical: <path> -->`

#### Auto-Repair

When `canon verify` discovers missing DC-HASH (Human View predates Canonical), it auto-regenerates MD from YAML and backfills source_hash.

---

### Ch32 Experience Library System

#### 5-State Lifecycle FSM

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
                                                     (retire, 730d inactive)
                                                           ↓
                                                        retired
```

#### Provenance & Weights

| Provenance | Weight | Description |
|------------|--------|-------------|
| `human-reported` | 0.95 | Direct human report |
| `ci-detected` | 0.85 | CI automated detection |
| `ai-inferred` | 0.60 | AI inference |
| `community-imported` | 0.50 | Community import |

#### Auto-Load

Phase 4 Step 0.5: Match by language + category + tags, load up to 10 experiences (lifecycle ≥ verified).

#### CLI

See Ch40 for complete experience CLI reference.

---

### Ch33 Community Experience Sharing

#### Zero-Backend Design

- **Primary Registry**: GitHub Releases (`github.com/leonai42/stdd-experiences`)
- **Mirror**: Gitee Releases (5-second timeout auto-failover)
- **Voting**: GitHub Issues as voting UI

#### Commands

```bash
stdd experience export --publish    # Publish experience pack to community
stdd experience pull python         # Pull Python experience pack from community
stdd experience curate pull         # Pull all packs to inbox
stdd experience curate review       # Review items one by one
stdd experience curate pack         # Package official experience pack
```

---

### Ch34 Code Structure Summary System

#### Self-Accumulating Design

Each change generates a delta → merge into cumulative index. AI understands project structure without full codebase scan.

#### Directory Structure

```
.stdd/code-structure/
  index.md               # Cumulative index
  .structure-index.yaml  # Metadata
  deltas/<change>.md     # Per-change delta
```

#### CLI

```bash
stdd structure delta <change>      # Generate delta for change
stdd structure merge <change>      # Merge delta into index
stdd structure rebuild             # Rebuild index from all deltas
stdd structure show [module]       # Show module structure
stdd structure graph               # ASCII dependency tree
```

---

### Ch35 Skill Ecosystem

#### 6 Phase Skills

| Skill | File | Content |
|-------|------|---------|
| stdd-understand | `understand.md` | Phase 1 flow: explore→template→proposal→score→Gate 1 |
| stdd-spec | `spec.md` | Phase 2 flow: extract→experience→design→spec→anchoring→Gate 2 |
| stdd-slice | `slice.md` | Phase 3 flow: 5-step analysis→dep graph→toposort→grouping |
| stdd-build | `build.md` | Phase 4 flow: context check→load→RED→GREEN→REFACTOR |
| stdd-verify | `verify.md` | Phase 5 flow: review→test→failure modes→adjustments→Gate 3 |
| stdd-deliver | `deliver.md` | Phase 6 flow: archive→merge→verify→tag |

#### _shared/ Fragments

- `confirm-gate.md` — Gate confirmation prompt template
- `mode-selection.md` — Long-range/normal mode selection
- `long-range-auth.md` — Long-range pre-authorization checklist

#### Skill Creation

```bash
stdd skill create <name> --type language|workflow|tools
```

Generates `.stdd/skills/<category>/<name>/SKILL.md`.

#### Platform Sync

`stdd install <platform>` copies 6 Skills to the corresponding platform directory (`.claude/skills/`, `.trae/skills/`, etc.).

---

## Part 7: CLI Complete Reference

### Ch36 CLI Overview

#### 27 Top-Level Commands

| # | Command | Since | Subs | Purpose |
|---|---------|-------|------|---------|
| 1 | `init` | V1.0 | 0 | Initialize STDD in project |
| 2 | `new` | V1.0 | 0 | Create change directory skeleton |
| 3 | `validate` | V1.0 | 0 | Validate change structure |
| 4 | `status` | V1.0 | 0 | Show artifact completion status |
| 5 | `archive` | V1.0 | 0 | Archive completed change |
| 6 | `trace` | V1.0 | 0 | View spec↔test↔code traceability |
| 7 | `install` | V1.0 | 0 | Install Skills to platform |
| 8 | `rollback` | V2.0 | 0 | Restore change from archive |
| 9 | `diff` | V2.0 | 0 | Show coverage diff |
| 10 | `abort` | V2.0 | 0 | Abort and archive change |
| 11 | `extract-proposal` | V2.4 | 0 | Extract proposal structured data |
| 12 | `dependency-graph` | V2.4 | 0 | Build dependency graph |
| 13 | `ci` | V2.4 | 6 | CI/CD management |
| 14 | `experience` | V2.4 | 9 | Experience library management |
| 15 | `state` | V2.5 | 0 | Cross-session state management |
| 16 | `gate` | V2.5 | 1 | Gate confirmation management |
| 17 | `proposal` | V2.7 | 3 | Canonical proposal management |
| 18 | `canon` | V2.7 | 3 | Dual-track document management |
| 19 | `index` | V2.7 | 3 | Project index management |
| 20 | `agent` | V2.7 | 1 | Agent behavior verification |
| 21 | `hooks` | V2.7 | 3 | Lifecycle hooks management |
| 22 | `structure` | V2.8 | 5 | Code structure summary management |
| 23 | `skill` | V2.7 | 1 | Skill creation |
| 24 | `fix` | V2.8 | 0 | Multi-level auto-fix |
| 25 | `upgrade` | V2.9 | 0 | Version upgrade |
| 26 | `batch` | V2.9.3 | 6 | Batch management |
| 27 | `guard` | V2.9.3 | 5 | Intelligent gate |

#### Global Flags

All commands support:
- `--dry-run`: Preview, don't modify filesystem
- `-v` / `--verbose`: `-v`=INFO, `-vv`=DEBUG

---

### Ch37 Project Lifecycle Commands

#### `stdd init [--force]`

**Purpose:** Initialize STDD in current project.

**Creates:** `.stdd/` (skills/templates/standards/config.d/platforms), `changes/`, `specs/`, `archive/`, `STDD.md`, `AGENTS.md`

**`--force`:** Overwrite existing files.

#### `stdd install <platform>`

**Purpose:** Install STDD Skills to specified platform.

**Platforms:** `claude-code` / `workbuddy` / `trae` / `cursor` / `opencode`

| Platform | Target Location | Format |
|----------|----------------|--------|
| claude-code | `.claude/skills/<name>/SKILL.md` | One dir per skill |
| workbuddy | `~/.workbuddy/skills/<name>.md` | One file per skill |
| trae | `.trae/skills/<name>.md` | One file per skill |
| cursor | `.cursor/rules/stdd.md` | Single file |
| opencode | `.opencode/skills/<name>/SKILL.md` | One dir per skill |

#### `stdd upgrade`

**Purpose:** Upgrade STDD version.

**Parameters:**

| Param | Description |
|-------|-------------|
| (none) | Upgrade current project |
| `--check` | Check version difference only |
| `--all` | Upgrade all registered projects |
| `--lock` | Lock current project version |
| `--unlock` | Unlock current project |
| `--yes` / `-y` | Skip confirmation |

**Upgrade Flow:** Check lock → backup → sync source files → merge project.yaml → reinstall platform Skills → update version.yaml → register global registry

---

### Ch38 Change Management Commands

#### `stdd new <name>`

**Purpose:** Create change directory skeleton `changes/<YYYY-MM-DD>-<name>/`.

**Name rules:** `^[a-zA-Z0-9][-a-zA-Z0-9_.]{1,49}$` (2-50 chars, starts with alphanumeric)

**Creates:** `proposal.md`, `design.md`, `test-plan.md`, `specs/`, `.stdd.yaml`

**`--parallel`:** Also creates explore + research parallel git worktrees (long-range dual-instance launch).

#### `stdd validate [name]`

**Purpose:** Validate change directory structural integrity.

**Checks:** Required file existence, spec format (Scenario count, GIVEN/WHEN/THEN balance, AND limit 5), TC-ID uniqueness, TC count ≥ Scenario count.

#### `stdd status [name]`

**Purpose:** Show artifact completion status. 6-phase progress + deliverable status.

#### `stdd archive <name> [--yes] [--skip-specs]`

**Purpose:** Archive completed change to `archive/`.

**`--yes`:** Skip confirmation. **`--skip-specs`:** Don't merge specs to project-level.

#### `stdd rollback <name>`

**Purpose:** Restore change from archive. Supports fuzzy name matching (`.endswith()`).

**Search order:** `archive/` → `archive/aborted/`.

#### `stdd abort <name> [--yes]`

**Purpose:** Abort change → `archive/aborted/`. Status marked as `aborted`.

#### `stdd diff [name]`

**Purpose:** Spec↔Test↔Code coverage diff table. Four columns: Spec Scenario | TC-ID | Test Function | Source. Outputs coverage percentage.

---

### Ch39 Trace & State Commands

#### `stdd trace <tc-id>`

**Purpose:** Trace TC-ID across four layers. Searches test-plan.md → test source files → extracts function name and line number.

#### `stdd state [name]`

**Purpose:** Cross-session state management.

| Param | Description |
|-------|-------------|
| (none) | Show full state |
| `--resume` | Show resume context (Change/Phase/Slice/Last Action/Freshness) |
| `--compact` / `-c` | Compact single-line output (cross-platform, token-efficient) |
| `--set KEY=VALUE` | Set resume field |

**Settable fields:** `resume_context`, `active_slice`, `last_action`, `last_modified`, `active_phase`, `phase_context_file`

#### `stdd gate approve --gate <1|2|3> [name]`

**Purpose:** CLI-based Gate confirmation. Equivalent to file_token and dialog channels.

#### `stdd extract-proposal [name] [--format json|yaml]`

**Purpose:** Extract structured data from proposal.md (capabilities/impact/risk_areas etc.).

---

### Ch40 Experience Commands

#### `stdd experience list`

**Filters:** `--category` / `--language` / `--lifecycle` / `--severity` / `--provenance` / `--format table|json|yaml` / `--all`

#### `stdd experience add`

**Parameters (13):** `--category` (required, one of 14), `--pattern` (required), `--root-cause`, `--detection-trigger`, `--fix-template`, `--language`, `--severity`, `--tags`, `--source-change`, `--body`, `--project-type`

#### Lifecycle State Transitions

| Command | Transition | Conditions |
|---------|-----------|------------|
| `stdd experience verify <id>` | discovered → verified | occurrences≥2, confidence≥0.7 |
| `stdd experience deposit <id>` | verified → deposited | occurrences≥3, confidence≥0.8 |
| `stdd experience retire <id> --reason "..."` | any → retired | 730 days or manual |

#### `stdd experience export [--output] [--format] [--no-sanitize] [--publish]`

Export to tar.gz. `--publish` uploads to community registry.

#### `stdd experience pull <pack> [--source]`

Pull experience pack from community.

#### `stdd experience curate`

| Sub | Purpose |
|-----|---------|
| `pull` | Pull all packs to inbox |
| `deduplicate` | Auto dedup and merge |
| `review` | Review items one by one |
| `pack` | Package official pack |

---

### Ch41 Dual-Track Commands

#### `stdd proposal`

| Sub | Purpose |
|-----|---------|
| `init [change_name]` | Generate proposal.yaml from proposal.md |
| `validate [change_name]` | Validate proposal.yaml field completeness |
| `show [change_name]` | Human-readable display |

#### `stdd canon`

| Sub | Purpose | Params |
|-----|---------|--------|
| `init` | Init canonical/ directory | `--change <name>` / `--project-level` |
| `generate` | YAML → MD render | `[change_name]` / `--type proposal\|design\|spec` / `--all` |
| `verify` | Verify dual-track consistency | `<change_name>` (required) |

---

### Ch42 Engineering Commands

#### `stdd index`

| Sub | Purpose |
|-----|---------|
| `update` | Generate/update project-index.yaml |
| `show [target]` | Show index summary or specific capability |
| `trace <file>` | Trace file to associated capabilities and changes |

#### `stdd agent verify [task] [--cp <id>]`

Execute checkpoint verification defined in agent_spec.yaml.

#### `stdd hooks`

| Sub | Purpose |
|-----|---------|
| `install [--force]` | Write hook scripts + configure settings.local.json |
| `status` | Show installed hooks |
| `uninstall` | Remove hooks configuration |

#### `stdd structure`

| Sub | Purpose |
|-----|---------|
| `delta <change>` | Generate code structure delta |
| `merge <change>` | Merge delta into index |
| `rebuild` | Rebuild index from all deltas |
| `show [module]` | Show module structure |
| `graph` | ASCII dependency tree |

#### `stdd skill create [name] [--type language|workflow|tools]`

Create new STDD Skill from template.

---

### Ch43 Quality & Version Commands

#### `stdd fix [--level 1|2|3]`

Three-level auto-fix (see Ch23 for details).

#### `stdd ci` (see Ch25)

#### `stdd batch`

| Sub | Purpose | Notes |
|-----|---------|-------|
| `open "description"` | Open batch | Includes scope validation (large rejected, medium warned) |
| `add "description"` | Add item to current batch | |
| `close` | Close batch | Generates archive-summary.md |
| `archive` | Archive batch to archive/ | Closes first if not closed |
| `list` | List all batches | |
| `status` | Show current batch status | |

**Params:** `--strategy monthly|weekly|count_based`

#### `stdd guard`

| Sub | Purpose | Notes |
|-----|---------|-------|
| `check` | Check edit permission | exit 0=allow, 2=block |
| `status` | Show guard status | Includes scope assessment |
| `init` | Deploy PreToolUse Hook | |
| `disable` | Temporarily remove Hook | |
| `enable` | Re-enable (=init) | |

**Params:** `--platform claude-code` (default), `--strict` (ignore allow_bypass), `--quiet`

---

### Ch44 Dependency Graph Command

#### `stdd dependency-graph [name] [--format text|json|dot]`

- `text` (default): Human-readable
- `json`: Structured JSON
- `dot`: Graphviz DOT format

**Output:** Nodes, edges, zero-dependency nodes, detected cycles (DFS detection).

---

## Part 8: Configuration System

### Ch45 Configuration Overview

#### Directory Layout

```
.stdd/
  config.d/
    project.yaml       # Project metadata
    gates.yaml         # Gate definitions
    long_range.yaml    # Long-range mode
    quality.yaml       # Quality checks
    experience.yaml    # Experience library
    lite.yaml          # Lightweight mode + complexity scoring
  version.yaml         # Version info
```

#### Loading & Merging

- Load order: project → gates → quality → experience → lite → long_range
- Upgrade: structure keys overwrite, identity keys (project name etc.) preserved
- Legacy compatibility: `project.yaml` falls back to old `config.yaml`

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
enforce_stdd: true           # Guard switch
allow_bypass: false          # Allow bypassing guard
```

---

### Ch47 gates.yaml

```yaml
gates:
  phase1_understand:
    required: true
    description: "Confirm proposal scope, boundaries, success criteria"
  phase2_spec:
    required: true
    description: "Confirm technical design and behavioral spec"
  phase5_verify:
    required: true
    description: "Confirm test report and quality check results"
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
  max_iterations: 5         # Max verify iterations (10 for thorough)
  auto_fix: true             # Enable Plankton L1 auto-fix
review:
  enabled: true
  max_rounds: 3
  agents: [security, performance, compatibility]  # Parallel review agents
  severity_thresholds:
    critical: "block"
    high: "warn_block"
    medium: "warn"
    low: "ignore"
test:
  runner: "pytest"
  coverage_target: 80        # Percentage
  multi_version: [3.10, 3.11, 3.12]  # Python multi-version
quality:
  lint: "ruff check"
  typecheck: "mypy"
  e2e: false                 # Disabled by default
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
  auto_record: true           # Phase 5 auto-record experiences
  auto_load:
    enabled: true
    max_experiences: 10
  lifecycle:
    verified_threshold: 3     # occurrences ≥ 3 → deposited
    settled_threshold: 10
    retire_after_days: 730
  export:
    sanitize: true            # Sanitize before export
community:
  registries:
    - url: "https://github.com/leonai42/stdd-experiences/releases/latest/download"
      priority: 1
    - url: "https://gitee.com/leonai42/stdd-experiences/releases/latest/download"
      priority: 2
      fallback_timeout: 5    # Seconds
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

### Ch52 version.yaml + Global Registry

```yaml
# .stdd/version.yaml
stdd_version: "2.9.3"
locked: false
installed_at: "2026-06-05T18:25:27"
upgraded_at: "2026-06-05T21:05:22"
source_path: "D:/mycode/stdd"
```

#### Global Registry `~/.stdd/projects.yaml`

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

## Part 9: Platforms & Standards

### Ch53 Platform Adapter Architecture

#### Design Principles

- **Core separated from adapters**: STDD core (CLI + Skill + Config) is platform-agnostic; one thin adapter per platform
- **Skill generation mechanism**: `stdd install` generates platform-specific format from `.stdd/skills/`

#### Platform-Specific Invocation

| Platform | Invocation | Adapter File |
|----------|-----------|--------------|
| Claude Code | `/stdd-<phase>` slash command | `.claude/skills/stdd-<phase>/SKILL.md` |
| WorkBuddy | Keyword trigger | `~/.workbuddy/skills/<name>.md` |
| Trae | Slash command | `.trae/skills/<name>.md` |
| Cursor | Auto-load rules | `.cursor/rules/stdd.md` |
| Windsurf | Cascade rules | `.windsurfrules` |
| Copilot | Instruction injection | `.github/copilot-instructions.md` |
| OpenCode (V2.7) | Slash command | `.opencode/skills/<name>/SKILL.md` |

---

### Ch54 Seven Platform Adapters

#### Claude Code

- **Invocation:** `/stdd-<phase>` slash commands
- **Skill Format:** YAML frontmatter (name, description) + Markdown body
- **Guard:** `PreToolUse` hook → `stdd guard check` (hard enforcement)
- **Hooks:** SessionStart / PreCompact / Stop

#### Cursor

- **Invocation:** `.cursorrules` auto-injection
- **Guard:** AI Rules inject prompt "check for active change before editing" (soft constraint)
- **No Hook support** (PreToolUse-level unavailable)

#### Windsurf

- **Invocation:** Cascade Flow rules
- **Guard:** Rule injection (soft constraint)

#### Copilot

- **Invocation:** `.github/copilot-instructions.md` auto-injection
- **Guard:** Instruction injection (soft constraint)

#### Other Platforms (WorkBuddy / Trae / OpenCode)

- Keyword or slash command trigger
- Guard: all soft constraints (rule/instruction injection)

---

### Ch55 Development Standards System

#### 5 Language Standards

| Language | File | Content |
|----------|------|---------|
| Python | `.stdd/standards/python.md` | Type annotations, async/await, CancelledError handling |
| Java | `.stdd/standards/java.md` | Spring Boot, JPA, exception handling |
| Go | `.stdd/standards/go.md` | Error handling, goroutine, context |
| Rust | `.stdd/standards/rust.md` | Cargo, ownership, unsafe |
| TypeScript | `.stdd/standards/typescript.md` | Node.js, async, type safety |

Phase 4 Step 0 auto-loads the matching standard by `project.language`.

#### Rules Directory

```
.stdd/rules/
  common/
    tdd.md              # TDD RED→GREEN→REFACTOR rules
    git-workflow.md     # Git commit conventions
    security.md         # Security baseline
  python/
    patterns.md         # Python-specific rules
  go/
    idioms.md           # Go idioms
```

---

### Ch56 Template System

#### 17 Document Templates (11 Core MD + 5 Canonical YAML + 1 Human View)

**Core MD Templates (11):**

| Template | Purpose | Phase |
|----------|---------|-------|
| `proposal.md` | Change proposal | 1 |
| `design.md` | Technical design | 2 |
| `spec.md` | Behavioral spec (Human View) | 2 |
| `spec-draft.md` | AI-generated spec draft | 2 |
| `test-plan.md` | Test plan | 2 |
| `tasks.md` | Task checklist | 3 |
| `slices.md` | Slice plan | 3 |
| `design-adjustments.md` | Design adjustments | 5 |
| `test-report.md` | Test report | 5 |
| `phase-context.md` | Phase context | All |
| `long-range-auth.md` | Long-range authorization | Gate 2 |

**Canonical YAML Templates (5):**

| Template | Format | Purpose |
|----------|--------|---------|
| `canonical/proposal.yaml` | YAML | Change proposal |
| `canonical/spec.yaml` | YAML | Behavioral spec |
| `canonical/agent_spec.yaml` | YAML | Agent verification spec |
| `canonical/pending-adjustments.yaml` | YAML | Design deviations |
| `canonical/design-adjustments.yaml` | YAML | Adjustment summary |

**Human View Templates (1):**

| Template | Format | Purpose |
|----------|--------|---------|
| `human-view/proposal-brief.md` | Markdown | Proposal render template |

#### Template Constraint Rules

- Read before write (don't overwrite existing content)
- Fixed structure (section order immutable)
- Required fields cannot be empty
- Fixed file naming

---

## Part 10: Version History & Future

### Ch57 V1.0 to V2.9 Complete Evolution

> 48 days, 13 versions, 0→260 tests, 1K→10.8K lines of code.

| Version | Date | Core Deliverable | Key Insight |
|---------|------|-----------------|-------------|
| V1.0 | May | 6-phase flow + CLI basics (7 commands) | Process must be enforced by tools, not just docs |
| V1.2 | May | Enhanced validation + initial failure modes | Automated checks more reliable than manual review |
| V2.0 | May 14 | CLI modularization, 10 commands, pytest framework | Architecture must be split to scale |
| V2.1 | May 14 | Review enhancement | Multi-agent parallel review highly effective |
| V2.4 | May 21 | Experience library + CI + dep graph + extraction | Experience is STDD's "memory system" |
| V2.5 | May 21 | Cross-session state, Gate CLI, anchoring system | Cross-session continuous work is essential |
| V2.7 | Jun 1 | Context engineering, dual-track docs, Agent verification, Skill ecosystem, Hooks | Dual-track enables AI to consume precise data |
| V2.8 | Jun 3 | Plankton auto-fix, code structure summary, pass@k, 12 failure modes complete | Quality system essentially complete |
| V2.9 | Jun 5 | Lightweight mode, complexity scoring, batch management, version upgrade, task_type | One framework serving tasks of different scales |
| V2.9.2 | Jun 5 | Canonical YAML expansion, enforcement gate, YAML-First | Gate went from nonexistent to present |
| V2.9.3 | Jun 6 | Intelligent gate (4-level classification), batch open/add/archive, lifecycle hooks deploy, --compact | Gate went from boolean to intelligent |

#### Key Metric Evolution

| Metric | V1.0 | V2.0 | V2.7 | V2.9.3 |
|--------|------|------|------|--------|
| CLI Commands | 7 | 10 | 21 | 27 |
| Tests | 0 | ~50 | ~180 | ~260 |
| Coverage | 0% | 40% | 68% | 73% |
| Source Lines | ~1K | ~3K | ~7K | ~10.8K |
| Supported Platforms | 1 | 1 | 5 | 7 |
| Failure Modes | 5 | 5 | 11 | 12 |
| Experience Entries | 0 | 0 | 0 | 7 |

---

### Ch58 V2.9 Core Differentiation vs Similar Tools

| Dimension | Copilot | Cursor | Claude Code Native | Cline | STDD V2.9 |
|-----------|---------|--------|-------------------|-------|-----------|
| Spec-driven | ❌ | ❌ | ❌ | ❌ | ✅ Spec→Implement→Verify |
| Enforcement gate | ❌ | ❌ | ❌ | ❌ | ✅ PreToolUse Hook + scope classifier |
| TDD enforcement | ❌ | ❌ | ❌ | Partial | ✅ RED→GREEN→REFACTOR |
| Failure mode detection | ❌ | ❌ | ❌ | ❌ | ✅ 12 categories |
| Experience self-learning | ❌ | ❌ | ❌ | ❌ | ✅ 5-state FSM |
| Cross-session recovery | ❌ | ❌ | ❌ | ❌ | ✅ state --resume |
| Three execution modes | ❌ | ❌ | ❌ | ❌ | ✅ Lightweight/Standard/Thorough |
| Dual-track docs | ❌ | ❌ | ❌ | ❌ | ✅ Canonical YAML + Human View |
| Batch management | ❌ | ❌ | ❌ | ❌ | ✅ Batch system |
| Version upgrade | ❌ | ❌ | ❌ | ❌ | ✅ stdd upgrade |
| Multi-platform support | — | — | — | — | ✅ 7 platforms |
| CI/CD integration | ❌ | ❌ | ❌ | ❌ | ✅ GitHub Actions + pre-commit |
| Anchoring system | ❌ | ❌ | ❌ | ❌ | ✅ L1-L4 |

---

### Ch59 V3 Outlook

> The following comes from VISION.md, under discussion. Not expanded in this white paper.

- **Phase 0 Requirements Management**: Cross-change requirement prioritization and dependency tracking
- **Phase 7 AAR**: Project-level after-action review and experience distillation
- **Full Dual-Track**: All 8 rules implemented, test-plan.yaml replacing test-plan.md
- **Non-Code Domains**: STDD applied to finance compliance, legal documents, operational processes
- **Invisible Guard**: From intelligent gate to frictionless gate; AI auto-selects optimal flow

---

## Part 11: Appendices

### AppA Complete Directory Structure Reference

```
project/
├── .stdd/                          # STDD System Directory
│   ├── version.yaml                #   C: Version info
│   ├── config.d/                   #   C: Config modules (6 files)
│   ├── skills/                     #   F: Phase Skill definitions
│   │   └── _shared/                #   F: Shared fragments
│   ├── templates/                  #   F: Document templates (17)
│   │   ├── canonical/              #   F: Canonical YAML templates (5)
│   │   └── human-view/             #   F: Human View templates
│   ├── standards/                  #   F: Language coding standards (5)
│   ├── rules/                      #   F: Project coding rules
│   ├── platforms/                  #   F: Platform adapters
│   ├── experiences/                #   C: Experience library
│   └── hooks/                      #   F: Lifecycle hook scripts
├── changes/                        # Y: Active changes
│   ├── <date>-<name>/              #   Y: Change directory (6 phase artifacts)
│   └── _batch/                     #   Y: Batch change container
├── specs/                          # C: Merged spec documents
├── archive/                        # C: Archived changes
├── stdd/                           #   Source code (CLI implementation)
├── tests/                          #   Tests
├── STDD.md                         # H: AI agent rules
├── AGENTS.md                       # H: Project memory
├── STDD_WHITEPAPER_V2.9_EN.md     # H: This file
└── pyproject.toml                  # C: Python package config
```

---

### AppB CLI Quick Reference Table

| Command | Key Params | Default | Since | Exit |
|---------|-----------|---------|-------|------|
| `init` | `--force` | false | V1.0 | 0 |
| `new` | `<name>`, `--parallel` | | V1.0 | 0/1 |
| `validate` | `[name]` | latest | V1.0 | 0/1 |
| `status` | `[name]` | latest | V1.0 | 0 |
| `archive` | `<name>`, `--yes`, `--skip-specs` | | V1.0 | 0/1 |
| `trace` | `<tc-id>` | | V1.0 | 0/1 |
| `install` | `<platform>` | | V1.0 | 0/1 |
| `rollback` | `<name>` | | V2.0 | 0/1 |
| `diff` | `[name]` | latest | V2.0 | 0/1 |
| `abort` | `<name>`, `--yes` | | V2.0 | 0/1 |
| `extract-proposal` | `[name]`, `--format json\|yaml` | json | V2.4 | 0/1 |
| `dependency-graph` | `[name]`, `--format text\|json\|dot` | text | V2.4 | 0/1 |
| `ci init` | | | V2.4 | 0 |
| `ci generate` | `<target>` | | V2.4 | 0 |
| `ci check-*` | `[name]` | | V2.4 | 0/1 |
| `experience list` | 7 filters | table | V2.4 | 0 |
| `experience add` | 13 params | | V2.4 | 0 |
| `experience stats` | `--format` | table | V2.4 | 0 |
| `experience export` | `--output`, `--format`, `--no-sanitize`, `--publish` | json | V2.4 | 0 |
| `experience pull` | `<pack>`, `--source` | | V2.4 | 0 |
| `experience verify` | `<id>` | | V2.4 | 0 |
| `experience deposit` | `<id>` | | V2.4 | 0 |
| `experience retire` | `<id>`, `--reason` | | V2.4 | 0 |
| `state` | `[name]`, `--resume`, `--compact`, `--set` | | V2.5 | 0/1 |
| `gate approve` | `--gate 1\|2\|3`, `[name]` | | V2.5 | 0/1 |
| `proposal init` | `[change_name]` | latest | V2.7 | 0/1 |
| `proposal validate` | `[change_name]` | latest | V2.7 | 0/1 |
| `proposal show` | `[change_name]` | latest | V2.7 | 0 |
| `canon init` | `--change`, `--project-level` | | V2.7 | 0/1 |
| `canon generate` | `[change_name]`, `--type`, `--all` | proposal | V2.7 | 0/1 |
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
| `skill create` | `[name]`, `--type` | language | V2.7 | 0 |
| `fix` | `--level 1\|2\|3` | 1 | V2.8 | 0 |
| `upgrade` | `--check`, `--all`, `--lock`, `--unlock`, `--yes` | | V2.9 | 0/1 |
| `batch open` | `"desc"`, `--strategy` | monthly | V2.9.3 | 0 |
| `batch add` | `"desc"` | | V2.9.3 | 0 |
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

### AppC FAQ

**Q1: How do I start using STDD?**
A: `stdd init` then use `/stdd-understand` to start your first change flow.

**Q2: How do I choose between lightweight/standard/thorough?**
A: Phase 1 complexity scoring auto-recommends. Micro-fixes → lightweight, feature enhancements → standard, new modules/architecture changes → thorough. Can override at Gate 2.

**Q3: Can Gates be skipped?**
A: No. Three Gates are mandatory and sequential. However, you can use file_token (create `GATE<N>_APPROVED` file) or CLI (`stdd gate approve`) to accelerate.

**Q4: Guard keeps blocking my edits. What do I do?**
A: Three ways to enter editable state: ① `stdd batch open "description"` for lightweight batch; ② `stdd new <name>` for formal change and advance to build phase; ③ Set `allow_bypass: true` in project.yaml (not recommended).

**Q5: What's the difference between long-range and normal mode?**
A: Long-range mode pre-authorizes Phase 3-5 after Gate 2, allowing AI to execute continuously across sessions. Gate 3 remains mandatory. Auto-degrades on 3 consecutive failures or <95% pass rate.

**Q6: What's the relationship between Canonical YAML and Human View MD?**
A: YAML is the AI-consumable data source (single source of truth). MD is one-way rendered output from YAML. Use `stdd canon verify` to check consistency.

**Q7: When should I use Batch vs Change?**
A: Micro-fixes (<5 files, e.g., bug fixes) use batch. Feature enhancements/refactors/new modules use change (full STDD flow). Guard's intelligent classifier auto-suggests at batch open based on description.

**Q8: How do I resume work across sessions?**
A: In a new session, say "continue" → Claude runs `stdd state --resume --compact` → one line recovers all context. Or SessionStart Hook auto-outputs.

**Q9: How does the experience library work?**
A: Phase 5 auto-records discovered failure patterns. Phase 4 auto-loads matched experiences. Lifecycle: discovered → verified (≥2 occurrences, confidence≥0.7) → deposited (≥3 occurrences, confidence≥0.8).

**Q10: How do I upgrade STDD version?**
A: `stdd upgrade --check` first to see differences, then `stdd upgrade`. Upgrade backs up old version, syncs new files, merges config, reinstalls platform Skills.

**Q11: Does Guard work cross-platform?**
A: `stdd guard check` CLI itself is universal. Auto-blocking currently only Claude Code (PreToolUse Hook). Other platforms use soft constraints via rule file injection.

**Q12: How do I contribute experiences to the community?**
A: `stdd experience export --publish`. Community registry on GitHub Releases + Gitee mirror. Official packs maintained via `stdd experience curate`.

---

### AppD .stdd.yaml Complete Field Reference

| Field | Type | Default | Writer | Reader |
|-------|------|---------|--------|--------|
| `change_id` | str | — | new | all |
| `change_name` | str | — | new | all |
| `status` | str | `"active"` | new, archive, abort, rollback | guard, validate, status |
| `current_phase` | str | `"understand"` | new, state, phases | guard, status, state |
| `task_type` | str | `"code"` | new, user | guard, spec |
| `mode` | str | `"standard"` | new, Gate2 | build, verify |
| `complexity_score` | int\|null | null | understand | spec |
| `score_confidence` | str\|null | null | understand | spec |
| `version` | str | `"2.0"` | new | — |
| `phases.<phase>.status` | str | `"pending"` | phases | all |
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

> **End.** STDD V2.9.3 White Paper · 11 Parts · 60 Chapters · English Human Edition
