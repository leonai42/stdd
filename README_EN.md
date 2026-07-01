# STDD — Spec+Test Driven Development

<p align="center">
  <b>Built for High-Quality AI Coding</b>
</p>

<p align="center">
  <b>V2.9</b> &nbsp;·&nbsp; MIT License &nbsp;·&nbsp; Python 3.10+
</p>

<p align="center">
  <a href="README.md">中文</a>
</p>

---

> **AI coding isn't just about "writing code" — it's about "writing correct code"** — engineering practices meet AI-assisted development.
>
> STDD is an **AI-assisted development methodology** powered by Spec-first + TDD execution. 6 ordered phases + 3 mandatory confirmation gates + 11 failure mode checks + self-learning experience library + bidirectional traceability — transforming vague requirements into high-quality deliverables. Supports 10 languages (Python / Java / Go / Rust / TypeScript / JavaScript / C++ / Kotlin / Swift / Dart) across 8 AI coding platforms.

---

## Table of Contents

- [What is STDD](#what-is-stdd)
- [Why STDD](#why-stdd)
- [Six-Phase Flow](#six-phase-flow)
- [Core Features](#core-features)
- [Quick Start](#quick-start)
- [CLI Commands](#cli-commands)
- [Supported Platforms](#supported-platforms)
- [Multi-Language Standards](#multi-language-standards)
- [Project Structure](#project-structure)
- [Case Studies](#case-studies)
- [Version History](#version-history)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## What is STDD

**STDD (Spec+Test Driven Development)** is an AI-assisted development methodology and tool system. Its core idea: **define behavior first (Spec), write tests second (Test), implement code last** — 6 ordered phases and 3 mandatory user confirmation gates ensure every line of AI-generated code is traceable and verifiable.

### Core Philosophy

| Principle | Description |
|-----------|-------------|
| **Spec First** | Define behavior in GIVEN/WHEN/THEN format before writing code, eliminating requirement ambiguity |
| **TDD Execution** | RED → GREEN → REFACTOR, advancing by vertical slices, each independently verifiable |
| **Traceable Adjustments** | Any design deviation during implementation must be recorded in design-adjustments.md, reviewed at Gate 3 |
| **User-Confirmation-Driven** | 3 mandatory gates (requirements → design → quality), critical checkpoints cannot be skipped |

### Three Mandatory Confirmation Gates

```
Gate 1 ── End of Phase 1 ── User confirms proposal.md (scope, boundaries, success criteria)
Gate 2 ── End of Phase 2 ── User confirms design.md + specs + test-plan.md (the critical watershed)
Gate 3 ── End of Phase 5 ── User confirms test-report.md + design-adjustments.md (final quality review)
```

After Gate 2, you can choose **Full-Auto Long-Range Mode**: one-time pre-authorization followed by continuous automatic execution of Phases 3-5, pausing only at Gate 3. Alternatively, choose **Normal Interactive Mode** to pause for interaction at each phase.

---

## Why STDD

### Who Is It For

| Audience | Why It Fits |
|----------|-------------|
| **Fintech / Healthtech Teams** | High-reliability, strong compliance, full-chain traceability for high-risk domains. Built-in risk control validation, audit logging, and precision constraints |
| **AI Coding Practitioners** | Tired of AI going off-track? STDD's 11 failure mode checks systematically catch common AI mistakes |
| **Engineering Team Leads** | Want to adopt AI-assisted development while ensuring code quality and traceability. 3 confirmation gates keep you in control of key decisions |
| **Open Source Maintainers** | Accepting AI-generated contributions but worried about traceability and quality. Spec-first approach ensures contributions meet expectations |

### Problems STDD Solves

1. **Vague Requirements → Spec First**: GIVEN/WHEN/THEN format transforms ambiguous requirements into verifiable behavior specs
2. **AI Going Off-Track → 11 Failure Checks**: Systematically detects hallucinated actions, scope creep, cascading errors, instruction decay, and other AI-specific issues
3. **Uncontrolled Quality → TDD Execution**: Write tests first, code second. Passing tests is the definition of done
4. **Black-Box Process → Bidirectional Traceability**: Scenario → TC-ID → test function → source code, full mapping queryable via `stdd trace`
5. **Silent Design Deviations → Mandatory Recording**: Every design deviation is auto-recorded, reviewed at Gate 3 — nothing is silent

---

## Six-Phase Flow

| Phase | Trigger | Artifacts | Gate |
|-------|---------|-----------|------|
| **P1: UNDERSTAND** | `/stdd-understand <requirement>` | proposal.md | **Gate 1** · Mandatory user confirmation |
| **P2: SPEC** | `/stdd-spec` | design.md + specs/\*.md + test-plan.md | **Gate 2** · Mandatory user confirmation (most critical) |
| **P3: SLICE** | Auto | tasks.md + slices.md | None (long-range auto after Gate 2) |
| **P4: BUILD** | Auto | TDD RED→GREEN→REFACTOR | Pause on blocker only |
| **P5: VERIFY** | Auto | test-report.md + design-adjustments.md | **Gate 3** · Mandatory user confirmation |
| **P6: DELIVER** | `/stdd-continue` | archive + merge specs + git tag | None |

### Phase Details

**Phase 1: UNDERSTAND — Requirement Understanding**
Transforms vague requirements into a clear, verifiable change proposal (proposal.md). Covers Why / What Changes / Capabilities / Impact / Success Criteria. No files are generated before user confirmation.

**Phase 2: SPEC — Spec Design** ⭐ *Most Critical Phase*
Transforms the proposal into precise technical specs and test plans. Produces technical design (design.md), behavior specs (specs/\*.md, GIVEN/WHEN/THEN format), and test plan (test-plan.md, with TC-ID mapping and coverage matrix). Design baseline is locked after Gate 2 confirmation.

**Phase 3: SLICE — Slice Planning**
Splits the test plan into independently implementable vertical slices (1 spec Scenario → 1+ tests → 1 implementation unit). Topologically sorted by dependencies, P0 first.

**Phase 4: BUILD — TDD Implementation**
Executes RED → GREEN → REFACTOR per slice. Write tests first (RED), then minimal implementation (GREEN), then refactor (REFACTOR). Design deviations are auto-recorded to pending-adjustments.md.

**Phase 5: VERIFY — Quality Verification**
Full test suite + coverage diagnostics + multi-version tests + E2E tests + Lint + Diff review + **11 failure mode checks**. Max 5 iterations in normal mode, 10 in long-range mode. Design adjustments are summarized into design-adjustments.md.

**Phase 6: DELIVER — Delivery**
Archive change to archive/ → merge specs to specs/ → Git commit + tag.

> See [STDD.md](STDD.md) for complete flow details, [DESIGN.md](DESIGN.md) for system design.

---

## Core Features

| Feature | Description |
|---------|-------------|
| **Spec First** | Define behavior in GIVEN/WHEN/THEN format; SHALL keyword marks mandatory behaviors, eliminating ambiguity |
| **3 Mandatory Gates** | Three non-skippable checkpoints: requirements → design → quality. Gate 2 is the watershed; full-auto long-range mode available after it |
| **Long-Range Unattended** | One-time pre-auth after Gate 2, Phases 3-5 execute continuously and automatically, 90%+ operations require no human intervention |
| **Self-Learning Library** ⭐V2.5 | 5-state lifecycle (discovered→verified→deposited→shared→merged/retired), AI continuously learns from past failures |
| **Community Pool** ⭐V2.5 | GitHub Releases CDN + Gitee mirror + Issues voting, global STDD users share experiences |
| **Multi-Agent Parallel** ⭐V2.5 | Auto-dispatch parallel slices to subagents, main agent coordinates and merges results |
| **Cross-Session Resume** ⭐V2.5 | Agent resumes context within 1 round after session restart, no progress lost in long-running tasks |
| **CI Checks Enhanced** ⭐V2.5 | 3 new checks: scope validation + coverage threshold + cross-capability contract consistency |
| **Bidirectional Traceability** | Scenario → TC-ID → test function → source code, full mapping chain queryable via `stdd trace` |
| **11 Failure Mode Checks** | Hallucinated actions, scope creep, cascading errors, context loss, tool misuse, runtime deviation, pipeline chain breaks, content quality issues, instruction decay, coverage vacuums, contract gaps |
| **Coverage Gap Analysis** | `stdd diff` outputs a spec-to-test coverage gap comparison table at a glance |
| **Design Adjustment Traceability** | Every design deviation during implementation is auto-recorded to design-adjustments.md, reviewed at Gate 3 |
| **18-Command CLI** | init / install / new / validate / status / archive / trace / diff / rollback / abort / experience / ci / gate / state / curate / dependency-graph / extract-proposal + `--dry-run` |
| **Built-in Review** | Code review capability built in since V2.1 — AI auto-reviews after implementation, ensuring quality consistency |

### Eleven Failure Modes

| # | Mode | What It Detects | Since |
|---|------|----------------|-------|
| (a) | Hallucinated actions | Fabricated file paths, env vars, function names, library APIs | V1.0 |
| (b) | Scope creep | Changes beyond planned files | V1.0 |
| (c) | Cascading errors | Silently swallowed exceptions, empty-array fallbacks masking issues | V1.0 |
| (d) | Context loss | Contradictions with proposal/design/spec decisions | V1.0 |
| (e) | Tool misuse | Wrong tool selection or parameters | V1.0 |
| (f) | Runtime behavior deviation | Correct static structure, incorrect dynamic behavior | V1.1 |
| (g) | Pipeline chain break | Missing steps or implicit assumptions in multi-step transform chains | V1.1 |
| (h) | Content quality deviation | Data inconsistency, length overflow, missing references, poor design | V1.1 |
| (i) | Instruction decay | Prompt explicitly stated but AI under-executed | V1.1 |
| (j) | Coverage vacuum | A capability with zero automated test coverage | V1.2 |
| (k) | Contract gap | Cross-capability API field name / header mismatch | V1.2 |

---

## Quick Start

### Prerequisites

- Python 3.10+ (CLI script only)
- PyYAML 6.0+ (`pip install pyyaml`)
- pytest 7.0+ (`pip install pytest`)
- Git 2.0+
- At least one supported AI coding platform

### Installation

```bash
# 1. Clone the STDD repository
git clone https://github.com/leonai42/stdd.git /path/to/stdd-project

# 2. Enter your target project directory
cd /path/to/your-project

# 3. Initialize STDD directory structure
python /path/to/stdd-project/bin/stdd init

# 4. Install skills to your AI platform (Claude Code example)
python /path/to/stdd-project/bin/stdd install claude-code

# Also supports other platforms
python /path/to/stdd-project/bin/stdd install cursor
python /path/to/stdd-project/bin/stdd install copilot
python /path/to/stdd-project/bin/stdd install aider
```

### Start Your First Change

In your AI coding platform, type:

```
/stdd-understand We need to add rate limiting to the API
```

The system will guide you through Phase 1 (requirement understanding), generate proposal.md, and wait for confirmation. After confirming, continue:

```
/stdd-spec        # Phase 2: Spec design & test planning
/stdd-continue    # Phase 3-6: Auto-iterate → deliver
```

---

## CLI Commands

| Command | Description | Since |
|---------|-------------|-------|
| `stdd init` | Initialize STDD directory structure | V1.0 |
| `stdd install <platform>` | Install skills to target AI platform | V1.0 |
| `stdd new <name>` | Create new change directory scaffold | V2.0 |
| `stdd validate [name]` | Validate change structure integrity + spec format + TC-ID uniqueness | V2.0 |
| `stdd status [name]` | View current phase and status of a change | V2.0 |
| `stdd archive <name>` | Archive completed change and merge specs | V2.0 |
| `stdd trace <tc-id>` | Trace spec↔test↔code bidirectional mapping chain | V2.0 |
| `stdd diff [name]` | Show spec↔test coverage gap table | V2.0 |
| `stdd rollback <name>` | Restore archived change from archive | V2.0 |
| `stdd abort <name>` | Abort change and archive | V2.0 |
| `stdd experience <sub>` | Experience library management (list/add/stats/export/pull/verify/deposit/retire) | V2.4 |
| `stdd extract-proposal` | Extract structured data from proposal.md (JSON/YAML) | V2.4 |
| `stdd dependency-graph` | Build spec dependency graph + cycle detection + topological sort | V2.4 |
| `stdd ci <sub>` | CI checks (7 items: structure/format/scope/coverage/contracts/diff/experience) | V2.5 |
| `stdd gate approve <change> --gate <N>` | Confirm gate via file token | V2.5 |
| `stdd state <change>` | Read/write change state (resume_context/active_slice etc.) | V2.5 |
| `stdd curate <sub>` | Community pool curation (pull/deduplicate/review/pack) | V2.5 |
| `--dry-run` | Global option: preview operations without modifying filesystem | V2.0 |
| `--verbose` / `-v` | Verbose logging output | V2.0 |

---

## Supported Platforms

| Platform | Install | Invocation |
|----------|---------|------------|
| **Claude Code** | `stdd install claude-code` | `/stdd-xxx` slash commands |
| **Cursor** | `stdd install cursor` | Auto-loaded project rules |
| **GitHub Copilot** | `stdd install copilot` | `.github/copilot-instructions.md` |
| **Aider** | `stdd install aider` | `.aider.conf.yml` |
| **WorkBuddy** | `stdd install workbuddy` | Keyword-triggered |
| **Trae** | `stdd install trae` | `/stdd-xxx` slash commands |
| **OpenCode** | `stdd install opencode` | `/stdd-xxx` slash commands |

> For Windsurf and other platforms without automated install support, manually copy `STDD.md` as `.windsurfrules`.

---

## Multi-Language Standards

Language-specific development standards are auto-loaded before Phase 4 begins. V2.3 covers 5 major languages:

| Language | Test Framework | Lint Tool | Since |
|----------|---------------|-----------|-------|
| **Python** | pytest | ruff | V1.0 |
| **Java** | JUnit 5 + Mockito | Checkstyle | V2.3 |
| **Go** | testing + testify | golangci-lint | V2.3 |
| **Rust** | cargo test | clippy + rustfmt | V2.3 |
| **TypeScript** | Jest | ESLint + Prettier | V2.3 |

---

## Project Structure

```
STDD Repository                          Your Project (after init)
├── .stdd/                                ├── .stdd/
│   ├── skills/          # 6 phase skills │   ├── skills/templates/standards/
│   ├── skills/_shared/  # DRY fragments  │   ├── config.d/        # Modular config
│   ├── templates/       # 9 doc templates│   └── platforms/       # Platform adapters
│   ├── standards/       # 5 lang specs   ├── specs/               # Master specs
│   ├── config.d/        # Modular config ├── changes/             # Active changes
│   └── platforms/       # 7 platform ads ├── archive/             # Completed
├── stdd/cli/            # CLI modules    ├── STDD.md
├── bin/stdd             # CLI entry      └── AGENTS.md
├── tests/               # STDD self-tests
├── STDD.md              # Universal guide
├── DESIGN.md            # System design
├── DEPLOY.md            # Deployment guide
├── EXTENDING.md         # Extension guide
├── TROUBLESHOOTING.md   # Troubleshooting
├── CHANGELOG.md         # Changelog
├── CONTRIBUTING.md      # Contributing guide
└── README.md
```

---

## Case Studies

### FPPT — AI-Powered PPT Generation System

Built from scratch to a shippable product in 5 days using STDD V1.2.

| Metric | Data |
|--------|------|
| Lines of Code | 27,826 (excluding node_modules) |
| Test Pass Rate | 100% (326 executable test cases) |
| AI Automation Rate | 90%+ (Phases 3-5 in long-range mode) |
| Spec Files | 41 spec.md files, 319+ Scenarios |
| Test Density | 1 line of test code per 2.4 lines of business code |
| Productivity | 1,400 lines per person-hour |

### TStrategy — Quantitative Trading System

A mid-to-short-term trend strategy system built with STDD methodology, iterated to stable V4.2. 19,500+ lines of test code, multi-layer scoring decision system with multi-level risk controls. Complete changes/ + specs/ directory structure; every strategy iteration goes through the full six-phase process.

### Visio Flowchart Skill — Small Project Example

Completed in under 1 hour with the full STDD six-phase process: 271 lines of core deliverables, 29 TC at 100% pass rate. Proves STDD isn't just for medium-to-large projects — small tasks benefit equally, with no compromise on quality regardless of scale.

---

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| **V2.5** | 2026-05-21 | Experience lifecycle FSM + community pool + multi-agent support + cross-session resume + CI enhanced |
| **V2.4** | 2026-05-20 | AI-assisted: self-learning experience library + spec auto-complete + smart slice + CI/CD integration |
| **V2.3** | 2026-05-18 | Foundation: 5 language standards + 6 platforms + config modularization + skill standardization |
| **V2.2** | 2026-05-15 | Process UX: enhanced gate interaction info + long-range mode reliability improvements |
| **V2.1** | 2026-05-14 | Methodology: fixed 80 review issues + built-in review capability |
| **V2.0** | 2026-05-13 | Architecture: modular CLI + 11 commands + pytest test framework |
| **V1.x** | 2026-05 | Foundation: 6-phase flow → long-range mode → 11 failure modes → E2E + coverage |

See [CHANGELOG.md](CHANGELOG.md) for full details.

---

## Documentation

| Document | Content |
|----------|---------|
| [STDD.md](STDD.md) | Universal process guide — loadable as project rules on platforms without skill systems |
| [DESIGN.md](DESIGN.md) | Full system design: architecture, state machine, cross-platform design, user interaction protocol |
| [DEPLOY.md](DEPLOY.md) | Deployment & usage guide: installation, configuration, platform adapters, FAQ |
| [EXTENDING.md](EXTENDING.md) | Extension guide: adding platforms, language standards, failure modes, CLI commands |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Troubleshooting: common issues and solutions |
| [CHANGELOG.md](CHANGELOG.md) | Complete version changelog |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contributing guide |

---

## Contributing

We welcome community contributions! Whether reporting bugs, suggesting features, adding language standards, or building platform adapters, please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## License

[MIT License](LICENSE)

Copyright (c) 2026 Hangzhou Dadao Yiyi Technology Co., Ltd. (杭州大道一以科技有限公司)

---

<p align="center">
  <b>Spec First, TDD Execution — quality comes from the system, not luck.</b>
</p>
