# STDD V2.9.3 White Paper (AI Reference Edition)

> Compressed from the human edition. Compact format for fast AI model retrieval.
> Full details: `STDD_WHITEPAPER_V2.9_EN.md`.

---

## Quick Reference

### Commands
| Cmd | Sub | Key Params | Phase |
|-----|-----|-----------|-------|
| `init` | | `--force` | — |
| `new` | | `<name>`, `--parallel` | P1 |
| `validate` | | `[name]` | — |
| `status` | | `[name]` | — |
| `archive` | | `<name>`, `--yes`, `--skip-specs` | P6 |
| `trace` | | `<tc-id>` | — |
| `install` | | `<platform>` | — |
| `rollback` | | `<name>` | — |
| `diff` | | `[name]` | — |
| `abort` | | `<name>`, `--yes` | — |
| `extract-proposal` | | `[name]`, `--format json\|yaml` | P2 |
| `dependency-graph` | | `[name]`, `--format text\|json\|dot` | P3 |
| `ci` | `init`,`generate`,`check-*` | `<target>`,`[name]` | P5 |
| `experience` | `list`,`add`,`stats`,`export`,`pull`,`verify`,`deposit`,`retire`,`curate` | many | P5 |
| `state` | | `[name]`,`--resume`,`--compact`,`--set` | all |
| `gate` | `approve` | `--gate 1\|2\|3` | P1/2/5 |
| `proposal` | `init`,`validate`,`show` | `[change_name]` | P1 |
| `canon` | `init`,`generate`,`verify` | `--change`,`--type`,`--all` | P2/6 |
| `index` | `update`,`show`,`trace` | `[target]`,`<file>` | all |
| `agent` | `verify` | `[task]`,`--cp` | P5 |
| `hooks` | `install`,`status`,`uninstall` | `--force` | all |
| `structure` | `delta`,`merge`,`rebuild`,`show`,`graph` | `<change>` | P4 |
| `skill` | `create` | `[name]`,`--type` | all |
| `fix` | | `--level 1\|2\|3` | P5 |
| `upgrade` | | `--check`,`--all`,`--lock`,`--unlock`,`--yes` | all |
| `batch` | `open`,`add`,`close`,`archive`,`list`,`status` | `"desc"`,`--strategy` | P4 |
| `guard` | `check`,`status`,`init`,`disable`,`enable` | `--platform`,`--strict`,`--quiet` | all |

### Config
| File | Key Fields |
|------|-----------|
| `project.yaml` | `stdd_version`, `project.{name,language}`, `enforce_stdd`, `allow_bypass` |
| `gates.yaml` | `gates.phase{1,2,5}`, `confirmation.channels` |
| `long_range.yaml` | `long_range.{recommended,pre_auth,degradation}` |
| `quality.yaml` | `verify`, `review`, `test`, `quality`, `pass@k` |
| `experience.yaml` | `experience.{auto_record,auto_load}`, `lifecycle`, `community` |
| `lite.yaml` | `scoring`, `scaling`, `batch`, `task_types` |
| `version.yaml` | `stdd_version`, `locked`, `installed_at`, `source_path` |

### Gates
| Gate | Phase | Confirms | Channels |
|------|-------|----------|----------|
| 1 | P1 end | proposal scope/boundaries | dialog/file_token/cli |
| 2 | P2 end | design + spec decisions | dialog/file_token/cli |
| 3 | P5 end | test-report + adjustments | dialog/file_token/cli |

Sequential, mandatory, idempotent.

### Modes
| Mode | Score | P2 | P3 | P4 | P5 | P6 |
|------|-------|----|----|----|----|----|
| lightweight | 0-3 | simplified | skip | simpleTDD | 1ag+5fm | batch |
| standard | 4-7 | full | smart | fullTDD | 3ag+12fm | archive |
| thorough | 8+ | full+ | parallel | TDD+pass@k | 3ag+sec+perf | full+notes |

TDD baseline (RED→GREEN) mandatory for ALL modes.

### task_type
| Type | SPEC | VERIFY |
|------|------|--------|
| code | spec.yaml + agent_spec.yaml | pytest+coverage+lint |
| documentation | agent_spec.yaml | content+references |
| configuration | agent_spec.yaml | config_validation |
| data-migration | agent_spec.yaml | data_integrity |
| dependency-upgrade | agent_spec.yaml | compatibility |

### Failure Modes
(a)hallucinated (b)scope_creep (c)cascading (d)context_loss (e)tool_misuse (f)runtime_deviation (g)pipeline_break (h)content_quality (i)instruction_decay (j)coverage_vacuum (k)contract_gap (l)anchoring_deficit
Lightweight subset: (a)(b)(c)(e)(f)

### Anchoring
L1: SHALL+Scenario (all changes) | L2: signatures/API/schemas (cross-system) | L3: proven patterns (safety-critical) | L4: baseline code (financial/compliance)

---

## Core Flow

**P1 UNDERSTAND:** explore→read template→draft proposal.yaml→review→complexity score(6dim,0-17)→Gate1
**P2 SPEC:** extract→load experiences(≤10)→design.md→spec.yaml+agent_spec.yaml→anchoring→test-plan.md→Gate2+mode
**P3 SLICE:** read spec→5-step analysis(dep/risk/effort/group/parallel)→toposort→slices.md+tasks.md (skip if lightweight)
**P4 BUILD:** ctx budget→load→per-slice RED→GREEN→REFACTOR→verify(TC100%)→merge. Deviations: minor=auto,major=pause+confirm
**P5 VERIFY:** ctx→review(sec/perf/compat)→pytest/coverage/ruff/mypy/multi-ver/E2E→diff→12 failure modes→adjustments→Gate3
**P6 DELIVER:** archive→merge specs→merge canon→canon verify→structure merge→git tag

---

## Key Mechanisms

**Guard 4-classifier:** micro(<3:fix,bug)→batch | small(3-9:optimize,UI)→batchOK | medium(10-19:refactor,module)→warn | large(≥20:rewrite,arch,API)→block→fullSTDD. Hard limits: files>5 warn,>10 block; >2h warn. exit: 0=allow,2=block.

**Batch:** `open(scope-check)→edit(guard-allow)→add→close→archive`. Strategy: monthly/weekly/count_based. Dir: `changes/_batch/<id>/`.

**Dual-track:** Canonical YAML(AI) → canon generate → Human View MD(human). 5 YAML schemas + 1 index. One-way. DC-HASH embedded.

**Experience FSM:** discovered→verified(occur≥2,conf≥0.7)→deposited(occur≥3,conf≥0.8)→shared→merged. retired(730d). Weights: human=0.95, ci=0.85, ai=0.60, community=0.50. Auto-load: P4 Step0.5, ≤10.

**Hooks:** SessionStart(print active change)→PreCompact(save last_modified)→Stop(experience stats). `stdd hooks install --force`.

**Long-range:** Gate2 enable→P3-5 pre-auth→Gate3 mandatory. Degrade: 3 fails|<95% pass.

**Complexity:** 6 dims × weight 3(doc×2), 0-17. 0-3=light,4-7=std,8-17=thorough.

**Context:** phase-context.md(≤200ln). `stdd state --resume --compact` single-line recovery. Freshness: git HEAD compare.

**Platforms:** Claude Code: hard(PreToolUse). Others: soft(rule injection).

---

## Canonical YAML Schemas

### proposal.yaml
`meta:{change_id,title,created,status,version} why:{problem} what_changes:[{description}] capabilities:{new:[],modified:[]} constraints:[] stakeholders:[] risk_areas:[] non_goals:[] critical:[] anchoring:{level,justification} success_criteria:[]`

### spec.yaml
`meta:{capability,change_id,created,confidence} requirements:[{id:REQ-XXX,description,scenarios:[{id:SC-XXX,confidence,evidence,given,when,then(SHALL),and[]}]}]`

### agent_spec.yaml
`meta:{task_id,change_id,created,task_type,system,description} preconditions:[] steps:[{id:CP-XX,description,action,assertions:[{type,expect}]}]`

### pending-adjustments.yaml
`meta:{change_id,updated_at} adjustments:[{id:ADJ-XXX,original,actual,reason,severity:minor|major,impact_scope,recorded_at}]`

### design-adjustments.yaml
`meta:{change_id,generated_at,requires_re_spec:bool} summary:{total,minor,major} categories:[] adjustments:[{id,original,adjusted,reason,severity,resolved_in_phase}]`

### .canon-index.yaml
`version:"2.9" proposals:{} designs:{} specs:{code:{},agent:{}}`

---

## .stdd.yaml Fields

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
| traceability.{scenarios,tc_cases,functions} | int | 0 | spec,build | validate,trace |
| design_adjustments.count | int | 0 | build,verify | verify |
| resume_context | str\|null | null | state | state |
| active_slice | str\|int\|null | null | state | state |
| last_action | str\|null | null | state,hooks | state |
| last_modified | str\|null | null | state,hooks | state |
| active_phase | str\|null | null | state | state |
| phase_context_file | str\|null | null | state | state |
| state_freshness.{verified_at,git_head} | str\|null | null | hooks | state |

---

## Version Evolution
V1.0(6Phase+7CLI)→V2.0(modular+10cmd)→V2.4(exp+CI+dep-graph)→V2.5(state+GateCLI+anchoring)→V2.7(ctx+dual-track+agent+Hooks)→V2.8(Plankton+structure+pass@k+12fm)→V2.9(lite+score+batch+upgrade+task_type)→V2.9.2(canon+guard+YAML-first)→V2.9.3(smart-guard+batch+compact)

---

> AI Reference Edition, compressed from `STDD_WHITEPAPER_V2.9_EN.md` (Stage D).
