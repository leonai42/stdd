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

### Ch00 Version Declaration & Conventions

**Version:** STDD V2.9.3. Internal use during V2.9.x series; public release at V3.0.

**Audience:** STDD users, AI agents (Claude Code / Cursor / Windsurf etc.), STDD developers.

**Conventions:** `` `code` `` for commands/filenames/fields, **bold** for first-occurrence concepts, `>` for notes and warnings.

---

### Ch01 Glossary

#### Core Concepts

- **STDD** — Specification-Driven Test-Driven Development. An AI coding workflow governance framework.
- **Change** — The basic work unit. Each change creates a `changes/<date>-<name>/` directory and goes through the full six-phase flow.
- **Phase** — Six workflow steps: UNDERSTAND → SPEC → SLICE → BUILD → VERIFY → DELIVER.
- **Capability** — An independent functional unit. Each capability has one spec file.
- **Scenario** — Basic spec unit. Format: GIVEN → WHEN → THEN(SHALL) → AND(≤5 items).
- **TC-ID** — Test case identifier. Format: `TC-<CAPABILITY>-<NNN>`.
- **Mode** — Three tiers: lightweight / standard / thorough.
- **Task Type** — code / documentation / configuration / data-migration / dependency-upgrade.

#### Dual-Track Documents

- **Canonical YAML** — AI-consumable YAML documents. Forms dual-track with Human View MD.
- **Human View** — Human-readable Markdown, rendered one-way from Canonical YAML.
- **DC-HASH** — Dual-track consistency hash. SHA-256 of YAML embedded in MD.
- **DC-FIELD** — Dual-track field consistency check.

#### Gates & Guard

- **Gate** — Three mandatory confirmation points. Gate 1 (end of Phase 1) / Gate 2 (end of Phase 2) / Gate 3 (end of Phase 5). Must proceed in order.
- **Guard** — Intelligent edit gate. Auto-checks before Edit/Write. V2.9.3: four-level scope classifier (micro/small/medium/large).
- **PreToolUse Hook** — Claude Code's pre-edit interception hook. Exit code 2 blocks the operation.
- **enforce_stdd** — Switch in project.yaml. Guard disabled when `false`.

#### Quality System

- **Failure Mode** — 12 categories of common AI coding failures (a-l), checked in Phase 5.
- **pass@k** — Statistical metric. Probability of passing at least once in k runs. Low pass@1 + high pass@k = spec ambiguity.
- **Plankton** — Three-level auto-fix system. L1: silent fix / L2: suggestion / L3: report.

#### Experience & Context

- **Experience Library** — 5-state lifecycle (discovered→verified→deposited→shared/merged→retired) management system.
- **Phase Context** — Cross-session recovery file. AI updates at end of each phase.
- **Resume Context** — Recovery fields in .stdd.yaml.
- **State Freshness** — Compares saved git HEAD with current HEAD.
- **Hook** — Three auto-triggered scripts: SessionStart / PreCompact / Stop.

#### Other

- **Long-Range Mode** — Optional after Gate 2. Phase 3-5 pre-authorized for automatic cross-session execution.
- **Batch** — Lightweight change container under `changes/_batch/<id>/`.
- **Skill** — Markdown files guiding AI through STDD phases. 6 phase skills + `_shared/` fragments.
- **TDD** — Test-Driven Development. Phase 4 core: RED → GREEN → REFACTOR.
- **Design Adjustment** — Deviations from original design recorded during BUILD. minor: auto-record, major: pause+confirm.

---

## Part 1: Overview

### Ch02 What is STDD

**Definition:** STDD = Specification-Driven Test-Driven Development. A framework for governing AI coding processes through CLI tools + Skill instructions + intelligent guard, ensuring every code change has a target, constraints, and verification.

**Three Core Problems Solved:**
1. **Unreliable AI output** — Spec → Implement → Verify closed loop
2. **Untraceable AI operations** — Full change lifecycle traceability
3. **Process inconsistency** — Skills + Guard provide consistent standards

**Relationship to Other Methodologies:**
| Methodology | Core | STDD Relationship |
|-------------|------|-------------------|
| TDD | Test-first | Phase 4 = RED→GREEN→REFACTOR |
| BDD | GIVEN/WHEN/THEN | Spec Scenarios use BDD format |
| DDD | Domain modeling | Capability ≈ Bounded Context |

**Design Philosophy:** Define → Execute → Verify → Learn (with experience feedback loop).

---

### Ch03 Nine Core Principles

1. **Spec-First**: Write spec before code. `❌ need→code  ✅ need→spec→confirm→code`
2. **TDD Execution**: Every slice: RED → GREEN → REFACTOR, non-skippable
3. **Traceable Adjustments**: Every design deviation must be recorded
4. **User-Confirmation-Driven**: Three Gates cannot be skipped; user has final approval
5. **Template-First**: All deliverables start from 17 templates
6. **Vertical Slicing**: Slice by function (end-to-end increment), not by layer
7. **Test Coverage Mandate**: Every Scenario must have a corresponding test
8. **Behavior-Not-Implementation**: Test "what it does", not "how it does it"
9. **Self-Learning**: Extract experiences from failures, feed back into future specs

---

### Ch04 Six-Phase Flow Overview

```
UNDERSTAND(1) → SPEC(2) → SLICE(3) → BUILD(4) → VERIFY(5) → DELIVER(6)
     ↓ Gate1       ↓ Gate2                          ↓ Gate3
  Score→Mode    Mode confirmed                  Final approval
```

**Deliverables per Phase:**
| Phase | Name | Deliverables | Gate |
|-------|------|-------------|------|
| 1 | UNDERSTAND | proposal.md | Gate 1 |
| 2 | SPEC | design.md, spec.yaml, agent_spec.yaml, test-plan.md | Gate 2 |
| 3 | SLICE | slices.md, tasks.md | — |
| 4 | BUILD | code, pending-adjustments.yaml | — |
| 5 | VERIFY | test-report.md, design-adjustments.yaml | Gate 3 |
| 6 | DELIVER | archive/, merged specs/ | — |

**Three Modes:**
| Mode | Score | P2 | P3 | P4 | P5 | P6 |
|------|-------|----|----|----|----|----|
| Lightweight | 0-3 | Simplified | Skip | Simple TDD | 1 agent+5 modes | Batch append |
| Standard | 4-7 | Full | Smart slice | Full TDD | 3 agents+12 modes | Full archive |
| Thorough | 8+ | Full+advanced | Parallel | TDD+pass@k | 3 agents+security+perf | Full+release notes |

---

## Part 2: Six Phases in Detail

### Ch05 Phase 1: UNDERSTAND

6-step flow: Problem exploration → Read template → Draft proposal.yaml → Auto-review → Complexity scoring → Gate 1 confirmation.

**Complexity scoring:** 6 dimensions, 0-17 points. Score confidence: preliminary / confirmed.

**Deliverables:** proposal.yaml, .stdd.yaml updated (understand → completed).

---

### Ch06 Phase 2: SPEC

Step 1: CLI extract → Step 2: Experience load (≤10 items) → Step 3: design.md → Step 4: Generate specs (Canonical YAML + Human View) → Step 4.5: Anchoring assessment → Step 5: test-plan.md → Step 6: Gate 2 + mode selection.

**For coding tasks:** spec.yaml (Scenarios: GIVEN/WHEN/THEN/AND) + agent_spec.yaml (CPs mapped to Scenarios).

**For non-coding tasks:** agent_spec.yaml only (CPs are the specification itself).

**TC-ID format:** `TC-<CAPABILITY>-<NNN>`. Gate 2 locks the mode; optionally enables long-range mode.

**Deliverables:** design.md, spec.yaml (coding), agent_spec.yaml, test-plan.md, .stdd.yaml updated.

---

### Ch07 Phase 3: SLICE

5-step analysis: Dependency graph → Risk assessment → Effort estimation → Grouping → Parallelization. Then topological sort.

**Lightweight mode:** Skip this phase (1 implicit slice).

**Long-range mode:** Auto-enters Phase 4.

**Deliverables:** slices.md, tasks.md, .stdd.yaml updated.

---

### Ch08 Phase 4: BUILD

Step -1: Context budget check (>80% → warn). Step 0: Load standards/rules/phase-context/experiences (≤10)/structure delta. Step 1: Per-slice RED → GREEN → REFACTOR. Step 1.4: Slice verification (TC coverage 100%). Step 1.5: Parallel slice merge.

**Design deviations:** minor → auto-record, major → pause + user confirmation.

**Deliverables:** code files, pending-adjustments.yaml, .stdd.yaml updated.

---

### Ch09 Phase 5: VERIFY

Step -1: Context budget. Step 0: Multi-agent parallel review (security/perf/compat — 1 agent for lightweight). Step 1: pytest → coverage → ruff → mypy → multi-version → E2E. Step 2: `stdd diff`. Step 3: 12 failure mode checks (5 for lightweight). Step 4: Design adjustment summary. Step 5: Gate 3 confirmation.

**Iteration caps:** lightweight=3, standard=5, thorough=10.

**Deliverables:** test-report.md, design-adjustments.yaml/.md, .stdd.yaml updated.

---

### Ch10 Phase 6: DELIVER

1. Archive: `stdd archive <change> --yes`
2. Canonical YAML merge: proposal.yaml + agent_spec.yaml → `canon verify`
3. Structure merge: `stdd structure merge <change>`
4. Git commit + tag

**Deliverables:** archive/<change>/, merged specs/, updated canonical/.

---

## Part 3: Key Mechanisms

### Ch11 Three Mandatory Gates

| Gate | Timing | Confirms |
|------|--------|----------|
| Gate 1 | End of Phase 1 | proposal: scope, boundaries, success criteria |
| Gate 2 | End of Phase 2 | design + spec: technical decisions |
| Gate 3 | End of Phase 5 | test-report + design adjustments |

Three equivalent confirmation channels: dialog / file_token / cli. Gates are sequential and mandatory.

---

### Ch12 Three Execution Modes

Mode is recommended by Phase 1 scoring, confirmed at Gate 2, locked from Phase 3 onward.

**task_type support:**
| type | SPEC strategy | VERIFY strategy |
|------|-------------|----------------|
| code | spec.yaml + agent_spec.yaml | pytest+coverage+lint |
| documentation | agent_spec.yaml | content+references |
| configuration | agent_spec.yaml | config_validation |
| data-migration | agent_spec.yaml | data_integrity |
| dependency-upgrade | agent_spec.yaml | compatibility |

---

### Ch13 Complexity Scoring Model

6 dimensions (weight 3 each, documentation weight 2): impact scope, technical complexity, test complexity, dependency count, risk level, documentation needs. Total: 0-17.

---

### Ch14 Design Adjustment Traceability

| Level | Condition | Handling |
|-------|-----------|----------|
| minor | Implementation detail, doesn't affect spec | Auto-record → continue |
| major | Changes spec behavior, interface, or data structure | Record → pause → user confirm |

---

### Ch15 Bidirectional Traceability Chain

Spec → TC → Test → Code (four layers). Commands: `stdd trace <tc-id>`, `stdd diff [name]`.

---

### Ch16 Long-Range Mode

Enabled after Gate 2. Pre-authorizes Phase 3-5. Degradation: 3 consecutive failures or pass rate <95%. Gate 3 remains mandatory.

---

### Ch17 Batch Directory Management

Three strategies: monthly (YYYY-MM-DD) / weekly (YYYY-Www-MMDD) / count_based (batch-NNN). Same-day collision → +HHMM suffix. Config in lite.yaml.

---

### Ch18 Context Engineering

phase-context.md (≤200 lines). Cross-session recovery: `stdd state --resume --compact`. Freshness: git HEAD comparison.

---

### Ch19 Lifecycle Hooks

SessionStart (print active change), PreCompact (save last_modified), Stop (experience stats). Installed: `stdd hooks install --force`.

---

### Ch20 Intelligent Guard

**Three-layer architecture:** Layer 1 (AGENTS.md directive injection, soft) / Layer 2 (PreToolUse Hook, hard) / Layer 3 (CLI check, manual).

**Four-level classifier:** micro(<3 points) → suggest batch | small(3-9) → batch OK | medium(10-19) → batch warn, suggest full STDD | large(≥20) → batch blocked, force full STDD.

**Hard limits:** files >5 warn, >10 block; open >2h warn. Exit codes: 0=allow, 2=block.

---

## Part 4: Quality System

### Ch21 Twelve Failure Modes

| ID | Name | Trigger |
|----|------|---------|
| (a) | Hallucinated actions | Non-existent file paths/variables/functions |
| (b) | Scope creep | Modified files beyond declared scope |
| (c) | Cascading errors | Silently swallowed exceptions, empty-array masking |
| (d) | Context loss | Implementation contradicts proposal/design/spec |
| (e) | Tool misuse | Wrong tool or parameter selection |
| (f) | Runtime deviation | Static structure correct but dynamic behavior wrong |
| (g) | Pipeline break | Missing intermediate steps in multi-step conversion |
| (h) | Content quality | Output format doesn't match spec |
| (i) | Instruction decay | AI didn't execute explicit prompt instructions |
| (j) | Coverage vacuum | Zero test coverage for a capability |
| (k) | Contract gap | Inconsistent field names/types across capabilities |
| (l) | Anchoring deficit | Insufficient anchoring for critical/safety changes |

Lightweight subset: (a)(b)(c)(e)(f).

---

### Ch22 pass@k

Low pass@1 + high pass@k = spec ambiguity. Config: quality.yaml. Lightweight: skip, Standard: k=1, Thorough: k=3.

---

### Ch23 Plankton Multi-Level Auto-Fix

L1: ruff format+check --fix+isort (silent). L2: scan for missing type annotations/bare except/CancelledError (max 20 suggestions). L3: bandit/pylint/mypy (report only). CLI: `stdd fix --level 1|2|3`.

---

### Ch24 Agent Verification Pipeline

Four sub-agents: security-reviewer (Opus), perf-analyzer (Sonnet), compat-checker (Sonnet), planner (Opus). Checkpoint system with typed assertions. CLI: `stdd agent verify [task] [--cp <id>]`.

---

### Ch25 CI/CD Integration

Command tree: `stdd ci {init, generate <target>, check-failures, check-scope, check-coverage, check-contracts}`. Generates GitHub Actions workflow, pre-commit hooks, PR template.

---

## Part 5: Spec Anchoring

### Ch26 Anchoring Overview

Problem: LLM non-determinism from spec ambiguity. Solution: constrain spec to eliminate ambiguity. Anti-patterns: over-anchoring, under-anchoring, formalistic anchoring.

---

### Ch27 L1 Behavioral Anchoring

SHALL (uppercase) in THEN for mandatory behavior. Every Requirement ≥1 Scenario. All boundary conditions covered. Required for ALL changes.

---

### Ch28 L2-L4 Advanced Anchoring

| Level | Content | Applicability |
|-------|---------|---------------|
| L1 | SHALL behavior, Scenario coverage | All changes (default) |
| L2 | Function signatures, API contracts, data schemas | Cross-system interfaces |
| L3 | Referenced proven implementation patterns | Safety-critical |
| L4 | Baseline reference implementation | Financial/compliance |

---

## Part 6: Core Subsystems

### Ch29 Dual-Track Document System

**Canonical track (YAML):** AI-consumable data source. **Human View track (MD):** Human-readable rendered output. One-way generation (YAML→MD, never reverse). Eight core rules govern the system.

---

### Ch30 Canonical YAML Format Specification

5 core schemas + 1 index file:

1. **proposal.yaml** — meta, why, what_changes, capabilities, constraints, stakeholders, risk_areas, non_goals, critical, anchoring, success_criteria
2. **spec.yaml** — meta, requirements[] with scenarios[] (given/when/then/and)
3. **agent_spec.yaml** — meta, preconditions, steps[] with assertions
4. **pending-adjustments.yaml** — adjustments[] recorded during Phase 4
5. **design-adjustments.yaml** — Phase 5 summary with requires_re_spec flag
6. **.canon-index.yaml** — file index

CLI: `stdd canon init|generate|verify`.

---

### Ch31 Human View Generation

`stdd canon generate` renders YAML→MD via direct field mapping. Each MD embeds source_hash, generated_at, and canonical path. Auto-repair when DC-HASH missing.

---

### Ch32 Experience Library

**5-state FSM:** discovered → verified (occur≥2, conf≥0.7) → deposited (occur≥3, conf≥0.8) → shared → merged. retired after 730 days.

**Provenance weights:** human-reported=0.95, ci-detected=0.85, ai-inferred=0.60, community-imported=0.50.

**Auto-load:** Phase 4 Step 0.5, match by language+category+tags, max 10 items.

---

### Ch33 Community Experience Sharing

Zero-backend design: GitHub Releases (primary) + Gitee mirror (5s timeout failover). Commands: `stdd experience export --publish`, `stdd experience pull <pack>`, `stdd experience curate`.

---

### Ch34 Code Structure Summary

Self-accumulating: delta per change → merge into cumulative index. AI understands project structure without full codebase scan. CLI: `stdd structure delta|merge|rebuild|show|graph`.

---

### Ch35 Skill Ecosystem

6 Phase Skills (understand/spec/slice/build/verify/deliver) + 3 shared fragments (confirm-gate, mode-selection, long-range-auth). CLI: `stdd skill create`. Platform sync via `stdd install <platform>`.

---

## Part 7: CLI Complete Reference

### Ch36 CLI Overview

**27 top-level commands:**
| # | Command | Introduced | Subcommands | Purpose |
|---|---------|-----------|-------------|---------|
| 1 | `init` | V1.0 | 0 | Initialize STDD in project |
| 2 | `new` | V1.0 | 0 | Create change skeleton |
| 3 | `validate` | V1.0 | 0 | Validate change structure |
| 4 | `status` | V1.0 | 0 | Show artifact completion |
| 5 | `archive` | V1.0 | 0 | Archive completed change |
| 6 | `trace` | V1.0 | 0 | Trace spec↔test↔code |
| 7 | `install` | V1.0 | 0 | Install Skills to platform |
| 8 | `rollback` | V2.0 | 0 | Restore from archive |
| 9 | `diff` | V2.0 | 0 | Show coverage diff |
| 10 | `abort` | V2.0 | 0 | Abort and archive change |
| 11 | `extract-proposal` | V2.4 | 0 | Extract proposal data |
| 12 | `dependency-graph` | V2.4 | 0 | Build dependency graph |
| 13 | `ci` | V2.4 | 6 | CI/CD management |
| 14 | `experience` | V2.4 | 9 | Experience library |
| 15 | `state` | V2.5 | 0 | Cross-session state |
| 16 | `gate` | V2.5 | 1 | Gate confirmation |
| 17 | `proposal` | V2.7 | 3 | Canonical proposal |
| 18 | `canon` | V2.7 | 3 | Dual-track documents |
| 19 | `index` | V2.7 | 3 | Project index |
| 20 | `agent` | V2.7 | 1 | Agent verification |
| 21 | `hooks` | V2.7 | 3 | Lifecycle hooks |
| 22 | `structure` | V2.8 | 5 | Code structure |
| 23 | `skill` | V2.7 | 1 | Skill creation |
| 24 | `fix` | V2.8 | 0 | Multi-level auto-fix |
| 25 | `upgrade` | V2.9 | 0 | Version upgrade |
| 26 | `batch` | V2.9.3 | 6 | Batch management |
| 27 | `guard` | V2.9.3 | 5 | Intelligent gate |

Global flags: `--dry-run`, `-v`/`--verbose`.

---

### Ch37 Project Lifecycle Commands

**`stdd init [--force]`** — Initialize STDD. Creates .stdd/, changes/, specs/, archive/, STDD.md, AGENTS.md.

**`stdd install <platform>`** — Install Skills to platform (claude-code/workbuddy/trae/cursor/opencode).

**`stdd upgrade [--check|--all|--lock|--unlock|--yes]`** — Upgrade STDD version. Flow: check lock→backup→sync→merge config→reinstall Skills→update version.yaml→register in global registry.

---

### Ch38 Change Management Commands

**`stdd new <name>`** — Create change directory. Name regex: `^[a-zA-Z0-9][-a-zA-Z0-9_.]{1,49}$`. Optional `--parallel` for dual git worktrees.

**`stdd validate [name]`** — Check required files, spec format (Scenarios, GIVEN/WHEN/THEN balance, AND≤5), TC-ID uniqueness, TC count ≥ Scenario count.

**`stdd status [name]`** — Display 6-phase progress and artifact status.

**`stdd archive <name> [--yes] [--skip-specs]`** — Archive to archive/. Merges specs unless --skip-specs.

**`stdd rollback <name>`** — Restore from archive. Fuzzy name matching. Search order: archive/ → archive/aborted/.

**`stdd abort <name> [--yes]`** — Abort to archive/aborted/. Status marked as aborted.

**`stdd diff [name]`** — Spec↔Test↔Code coverage table with percentage.

---

### Ch39 Trace & State Commands

**`stdd trace <tc-id>`** — Trace TC-ID across all four layers.

**`stdd state [name] [--resume] [--compact] [--set KEY=VALUE]`** — Cross-session state. Settable fields: resume_context, active_slice, last_action, last_modified, active_phase, phase_context_file. `--compact` for single-line output.

**`stdd gate approve --gate 1|2|3 [name]`** — CLI gate confirmation.

**`stdd extract-proposal [name] [--format json|yaml]`** — Extract structured proposal data.

---

### Ch40 Experience Commands

`list` (filter by category/language/lifecycle/severity/provenance/format), `add` (13 params), `stats`, `export [--publish]`, `pull <pack>`, `verify <id>`, `deposit <id>`, `retire <id> --reason`, `curate {pull,deduplicate,review,pack}`.

---

### Ch41 Dual-Track Commands

`stdd proposal {init,validate,show}`, `stdd canon {init [--change|--project-level], generate [--type|--all], verify <name>}`.

---

### Ch42 Engineering Commands

`stdd index {update,show,trace}`, `stdd agent verify [task] [--cp]`, `stdd hooks {install [--force],status,uninstall}`, `stdd structure {delta,merge,rebuild,show,graph}`, `stdd skill create [name] [--type]`.

---

### Ch43 Quality & Version Commands

`stdd fix [--level 1|2|3]`, `stdd ci {init,generate,check-*}`, `stdd batch {open,add,close,archive,list,status} [--strategy]`, `stdd guard {check,status,init,disable,enable} [--platform] [--strict] [--quiet]`.

---

### Ch44 Dependency Graph

`stdd dependency-graph [name] [--format text|json|dot]`. Nodes, edges, zero-dependency nodes, cycle detection (DFS).

---

## Part 8: Configuration System

### Ch45 Configuration Overview

`.stdd/config.d/` contains 6 module files + `.stdd/version.yaml`. Loading order: project → gates → quality → experience → lite → long_range. Upgrade merge: overwrite structure keys, preserve identity keys.

---

### Ch46 project.yaml
```yaml
stdd_version: "2.9.3"
project: {name, language, python_version, source_dir}
paths: {changes, specs, archive, tests}
enforce_stdd: true
allow_bypass: false
```

### Ch47 gates.yaml
```yaml
gates: {phase1_understand, phase2_spec, phase5_verify}
confirmation: {channels: [dialog, file_token, cli]}
```

### Ch48 long_range.yaml
```yaml
long_range: {recommended, pre_auth: {design_deviation, technical_blocker, iteration, operations, gate3}, degradation: {max_consecutive_failures, pass_rate_threshold, safety_check}}
```

### Ch49 quality.yaml
```yaml
verify: {max_iterations, auto_fix}
review: {max_rounds, agents: [security, performance, compatibility], severity_thresholds}
test: {runner, coverage_target, multi_version}
quality: {lint, typecheck, e2e}
pass@k: {enabled, k_values, threshold}
```

### Ch50 experience.yaml
```yaml
experience: {auto_record, auto_load: {max_experiences: 10}}
lifecycle: {verified_threshold: 3, settled_threshold: 10, retire_after_days: 730}
community: {registries: [{url, priority}], packs: [{name, version}]}
```

### Ch51 lite.yaml
```yaml
scoring: {dimensions: [{name, weight, levels}], thresholds: {lightweight: 3, standard: 7, thorough: 17}}
scaling: {lightweight, standard, thorough}  # per-phase behavior
batch: {strategy: monthly, max_items: 20}
task_types: {code, documentation, configuration, data-migration, dependency-upgrade}
```

### Ch52 version.yaml + Global Registry
```yaml
# .stdd/version.yaml
stdd_version, locked, installed_at, upgraded_at, source_path
# ~/.stdd/projects.yaml (global)
projects: [{name, path, version, locked, last_seen}]
```

---

## Part 9: Platforms & Standards

### Ch53 Platform Adapter Architecture

Core (CLI+Skill+Config) platform-agnostic; thin adapter per platform. Skill generation via `stdd install`.

### Ch54 Seven Platform Adapters

| Platform | Invocation | Guard Type |
|----------|-----------|------------|
| Claude Code | `/stdd-<phase>` command | PreToolUse Hook (hard) |
| Cursor | `.cursorrules` injection | Rule injection (soft) |
| Windsurf | Cascade rules | Rule injection (soft) |
| Copilot | `.github/copilot-instructions.md` | Instruction injection (soft) |
| WorkBuddy | Keyword trigger | Soft |
| Trae | Slash command | Soft |
| OpenCode | Slash command | Soft |

### Ch55 Development Standards

5 language standards (Python/Java/Go/Rust/TypeScript) in `.stdd/standards/`. Rules in `.stdd/rules/` (common + per-language). Auto-loaded at Phase 4 Step 0.

### Ch56 Template System

**17 templates:** 11 core MD + 5 Canonical YAML + 1 Human View.

Core MD: proposal, design, spec, spec-draft, test-plan, tasks, slices, design-adjustments, test-report, phase-context, long-range-auth.

Canonical YAML: proposal.yaml, spec.yaml, agent_spec.yaml, pending-adjustments.yaml, design-adjustments.yaml.

Human View: proposal-brief.md.

---

## Part 10: Version History & Future

### Ch57 V1.0 to V2.9 Complete Evolution

| Version | Core |
|---------|------|
| V1.0 | 6-phase flow + 7 CLI commands |
| V2.0 | CLI modularization + 10 commands + test framework |
| V2.4 | Experience library + CI + dependency graph + extraction |
| V2.5 | Cross-session state + Gate CLI + Anchoring |
| V2.7 | Context engineering + Dual-track + Agent verification + Skills + Hooks |
| V2.8 | Plankton + Structure summary + pass@k + 12 failure modes |
| V2.9 | Lightweight + Complexity scoring + Batch + Upgrade + task_type |
| V2.9.2 | Canonical expansion + Enforcement gate + YAML-First |
| V2.9.3 | Intelligent guard (4-level classification) + batch open/add/archive + Hooks deploy + --compact |

**Key metrics:** CLI: 7→27, Tests: 0→~260, Coverage: 0%→73%, Lines: ~1K→~10.8K, Platforms: 1→7.

---

### Ch58 V2.9 Differentiation vs Similar Tools

| Dimension | Copilot | Cursor | Claude Code Native | STDD V2.9 |
|-----------|---------|--------|-------------------|-----------|
| Spec-driven | ❌ | ❌ | ❌ | ✅ |
| Enforcement gate | ❌ | ❌ | ❌ | ✅ PreToolUse Hook + Scope classifier |
| TDD enforcement | ❌ | ❌ | ❌ | ✅ RED→GREEN→REFACTOR |
| Failure mode detection | ❌ | ❌ | ❌ | ✅ 12 categories |
| Experience self-learning | ❌ | ❌ | ❌ | ✅ 5-state FSM |
| Cross-session recovery | ❌ | ❌ | ❌ | ✅ state --resume |
| Three execution modes | ❌ | ❌ | ❌ | ✅ |
| Dual-track docs | ❌ | ❌ | ❌ | ✅ |
| Batch management | ❌ | ❌ | ❌ | ✅ |
| Version upgrade | ❌ | ❌ | ❌ | ✅ |
| Multi-platform | — | — | — | ✅ 7 platforms |
| CI/CD integration | ❌ | ❌ | ❌ | ✅ |
| Anchoring L1-L4 | ❌ | ❌ | ❌ | ✅ |

---

### Ch59 V3 Outlook

> Under discussion, not expanded in this white paper.

- Phase 0: Cross-change requirements management
- Phase 7: AAR (After-Action Review)
- Full dual-track: all 8 rules, test-plan.yaml
- Non-code domains: finance compliance, legal documents, operational processes
- Invisible guard: from intelligent gate to zero-friction gate

---

## Part 11: Appendices

### AppA Complete Directory Structure

```
project/
├── .stdd/                      # System
│   ├── config.d/               # 6 config modules
│   ├── skills/                 # 6 Phase Skills + _shared/
│   ├── templates/              # 11 MD + 5 YAML + 1 HV
│   ├── standards/              # 5 languages
│   ├── rules/                  # Project rules
│   ├── platforms/              # 7 platform adapters
│   ├── experiences/            # Experience library
│   └── hooks/                  # 3 lifecycle scripts
├── changes/<date>-<name>/      # Standard change
│   └── canonical/              # Dual-track
├── changes/_batch/<id>/        # Batch container
├── specs/                      # Merged specs
├── archive/                    # Archived changes
├── stdd/                       # CLI source
└── tests/                      # Test suite
```

---

### AppB CLI Quick Reference

| Command | Key Params | Exit |
|---------|-----------|------|
| `init` | `--force` | 0 |
| `new` | `<name>`, `--parallel` | 0/1 |
| `validate` | `[name]` | 0/1 |
| `status` | `[name]` | 0 |
| `archive` | `<name>`, `--yes`, `--skip-specs` | 0/1 |
| `trace` | `<tc-id>` | 0/1 |
| `install` | `<platform>` | 0/1 |
| `rollback` | `<name>` | 0/1 |
| `diff` | `[name]` | 0/1 |
| `abort` | `<name>`, `--yes` | 0/1 |
| `extract-proposal` | `[name]`, `--format json\|yaml` | 0/1 |
| `dependency-graph` | `[name]`, `--format text\|json\|dot` | 0/1 |
| `ci {init,generate,check-*}` | `<target>`, `[name]` | 0/1 |
| `experience list` | 7 filters | 0 |
| `experience add` | 13 params | 0 |
| `experience {stats,export,pull,verify,deposit,retire}` | varies | 0 |
| `state` | `[name]`, `--resume`, `--compact`, `--set` | 0/1 |
| `gate approve` | `--gate 1\|2\|3`, `[name]` | 0/1 |
| `proposal {init,validate,show}` | `[change_name]` | 0/1 |
| `canon init` | `--change`, `--project-level` | 0/1 |
| `canon generate` | `[change_name]`, `--type`, `--all` | 0/1 |
| `canon verify` | `<change_name>` | 0/1 |
| `index {update,show,trace}` | `[target]`, `<file>` | 0/1 |
| `agent verify` | `[task]`, `--cp` | 0/1 |
| `hooks {install,status,uninstall}` | `--force` | 0 |
| `structure {delta,merge,rebuild,show,graph}` | `<change>`, `[module]` | 0 |
| `skill create` | `[name]`, `--type` | 0 |
| `fix` | `--level 1\|2\|3` | 0 |
| `upgrade` | `--check`, `--all`, `--lock`, `--unlock`, `--yes` | 0/1 |
| `batch {open,add,close,archive,list,status}` | `"desc"`, `--strategy` | 0 |
| `guard check` | `--platform`, `--strict`, `--quiet` | 0/2 |
| `guard {status,init,disable,enable}` | `--platform` | 0 |

---

### AppC FAQ

**Q1: How to start with STDD?** → `stdd init` then `/stdd-understand`.

**Q2: How to choose mode?** → Phase 1 scoring auto-recommends. Override at Gate 2.

**Q3: Can Gates be skipped?** → No. Three Gates are mandatory and sequential. Use file_token or CLI for faster confirmation.

**Q4: Guard keeps blocking my edits?** → Three ways: (1) `stdd batch open "desc"`, (2) `stdd new <name>` and advance to build phase, (3) set `allow_bypass: true` (not recommended).

**Q5: Long-range vs normal mode?** → Long-range pre-authorizes Phase 3-5. Gate 3 remains mandatory. Degrades on 3 consecutive failures or <95% pass rate.

**Q6: Canonical YAML vs Human View MD?** → YAML is the single source of truth for AI. MD is one-way rendered output. Use `stdd canon verify` to check consistency.

**Q7: Batch vs Change?** → Micro-fixes (<5 files) use batch. Feature/refactor/new module uses change. Guard's classifier auto-suggests at batch open.

**Q8: How to resume across sessions?** → Say "continue" → Claude runs `stdd state --resume --compact` → one-line recovery.

**Q9: How does the experience library work?** → Phase 5 auto-records, Phase 4 auto-loads (matched by language+category+tags, max 10).

**Q10: How to upgrade STDD?** → `stdd upgrade --check` then `stdd upgrade`. Backs up, syncs, merges config, reinstalls Skills.

**Q11: Does Guard work across platforms?** → `stdd guard check` CLI is universal. Auto-blocking currently Claude Code only (PreToolUse Hook). Other platforms use soft constraints via rule injection.

---

### AppD .stdd.yaml Complete Field Reference

| Field | Type | Default | Writer | Reader |
|-------|------|---------|--------|--------|
| change_id | str | — | new | all |
| status | str | active | new,archive,abort,rollback | guard,validate |
| current_phase | str | understand | new,state | guard,status,state |
| task_type | str | code | new,user | guard,spec |
| mode | str | standard | new,Gate2 | build,verify |
| complexity_score | int\|null | null | understand | spec |
| score_confidence | str\|null | null | understand | spec |
| phases.<p>.status | str | pending | phases | all |
| phases.<p>.confirmed_at | str\|null | null | gate | validate |
| long_range.enabled | bool | false | Gate2 | build,verify |
| traceability.{spec_scenarios,tc_cases,test_functions} | int | 0 | spec,build | validate,trace |
| design_adjustments.count | int | 0 | build,verify | verify |
| resume_context | str\|null | null | state | state |
| active_slice | str\|int\|null | null | state | state |
| last_action | str\|null | null | state,hooks | state |
| last_modified | str\|null | null | state,hooks | state |
| active_phase | str\|null | null | state | state |
| phase_context_file | str\|null | null | state | state |
| state_freshness.{verified_at,git_head} | str\|null | null | hooks | state |

---

> **End.** STDD V2.9.3 White Paper · English Human Edition · 11 Parts · 60 Chapters
