# STDD V2.9.3 White Paper (AI Reference Edition)

> Compressed from `STDD_WHITEPAPER_V2.9_EN.md` (2,239 lines). Compact format for fast AI model retrieval.

---

## Quick Reference

### Commands (27 total)
| Cmd | Sub | Key Params | Phase | Purpose |
|-----|-----|-----------|-------|---------|
| `init` | | `--force` | — | Initialize STDD |
| `new` | | `<name>`, `--task-type`, `--parallel` | P1 | Create change |
| `validate` | | `[name]` | — | Validate structure |
| `status` | | `[name]` | — | Artifact status |
| `archive` | | `<name>`, `--yes`, `--skip-specs` | P6 | Archive change |
| `trace` | | `<tc-id>` | — | Trace spec↔test↔code |
| `install` | | `<platform>` | — | Install Skills |
| `rollback` | | `<name>` | — | Restore from archive |
| `diff` | | `[name]` | — | Coverage diff |
| `abort` | | `<name>`, `--yes` | — | Abort change |
| `extract-proposal` | | `[name]`, `--format json\|yaml` | P2 | Extract structured data |
| `dependency-graph` | | `[name]`, `--format text\|json\|dot` | P3 | Build dep graph |
| `ci` | `init`,`generate`,`check-*` | `<target>`,`[name]` | P5 | CI/CD |
| `experience` | `list`,`add`,`stats`,`export`,`pull`,`verify`,`deposit`,`retire`,`curate` | many | P5 | Experience library |
| `state` | | `[name]`,`--resume`,`--compact`,`--set` | all | Cross-session state |
| `gate` | `approve` | `--gate 1\|2\|3` | P1/2/5 | Gate confirmation |
| `proposal` | `init`,`validate`,`show` | `[change_name]` | P1 | Canonical proposal |
| `canon` | `init`,`generate`,`verify` | `--change`,`--type`,`--all` | P2/6 | Dual-track docs |
| `index` | `update`,`show`,`trace` | `[target]`,`<file>` | all | Project index |
| `agent` | `verify` | `[task]`,`--cp` | P5 | Agent verification |
| `hooks` | `install`,`status`,`uninstall` | `--force` | all | Lifecycle hooks |
| `structure` | `delta`,`merge`,`rebuild`,`show`,`graph` | `<change>` | P4 | Code structure |
| `skill` | `create` | `[name]`,`--type` | all | Skill creation |
| `fix` | | `--level 1\|2\|3` | P5 | Auto-fix |
| `upgrade` | | `--check`,`--all`,`--lock`,`--unlock`,`--yes` | all | Version upgrade |
| `batch` | `open`,`add`,`close`,`archive`,`list`,`status` | `"desc"`,`--strategy`,`--force` | P4 | Batch management |
| `guard` | `check`,`status`,`init`,`disable`,`enable` | `--platform`,`--strict`,`--quiet` | all | Intelligent gate |
| `phase` | `status`,`advance`,`set` | `[name]`,`[target_phase]` | all | Phase management |
| `work` | `add`,`list` | `[name]`,`--type`,`--commit` | all | Related work |

### Config Quick Reference
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
| Type | SPEC | VERIFY | Editable Phases |
|------|------|--------|-----------------|
| code | spec.yaml+agent_spec.yaml | pytest+coverage+lint | build, verify |
| documentation | agent_spec.yaml | content+references | understand,spec,slice,build,verify |
| configuration | agent_spec.yaml | config_validation | understand,spec,slice,build,verify |
| data-migration | agent_spec.yaml | data_integrity | build, verify |
| dependency-upgrade | agent_spec.yaml | compatibility | build, verify |

### Failure Modes (12)
(a)hallucinated (b)scope_creep (c)cascading (d)context_loss (e)tool_misuse (f)runtime_deviation (g)pipeline_break (h)content_quality (i)instruction_decay (j)coverage_vacuum (k)contract_gap (l)anchoring_deficit
Lightweight subset: (a)(b)(c)(e)(f)

### Anchoring
L1: SHALL+Scenario (all) | L2: signatures/API/schemas (cross-system) | L3: proven patterns (safety-critical) | L4: baseline code (financial/compliance)

---

## Core Flow

**P1 UNDERSTAND:** explore→read template→draft proposal.yaml→review→complexity score(6dim,0-17)→Gate1
**P2 SPEC:** extract→load experiences(≤10)→design.md→spec.yaml+agent_spec.yaml→anchoring→test-plan.md→Gate2+mode
**P3 SLICE:** read spec→5-step(dep/risk/effort/group/parallel)→toposort→slices.md+tasks.md (skip if lightweight)
**P4 BUILD:** ctx budget→load→per-slice RED→GREEN→REFACTOR→verify(TC100%)→merge. Deviations: minor=auto, major=pause+confirm
**P5 VERIFY:** ctx→review(sec/perf/compat)→pytest/coverage/ruff/mypy→diff→12 failure modes→adjustments→Gate3
**P6 DELIVER:** archive→merge specs→merge canon→canon verify→structure merge→git tag

---

## Key Mechanisms

**Guard V2.9.4:** Phase integrity check (prev phases completed + gates confirmed) + task_type-aware editable phases + file type mismatch detection + 4-level scope classifier (micro/small/medium/large). exit: 0=allow, 2=block.

**Batch V2.9.4:** `open(scope-check+active-change-warn)→edit→add(git-diff≤3 files)→close(≤1item+<1h warn)→archive`. max_items=5. Strategy: monthly/weekly/count_based.

**Dual-track:** Canonical YAML(AI)→canon generate→Human View MD(human). 5 YAML schemas + 1 index. One-way. DC-HASH embedded.

**Experience FSM:** discovered→verified(occur≥2,conf≥0.7)→deposited(occur≥3,conf≥0.8)→shared→merged. retired(730d). Weights: human=0.95, ci=0.85, ai=0.60, community=0.50.

**Hooks:** SessionStart(print active change)→PreCompact(save state)→Stop(experience stats). `stdd hooks install --force`.

**Long-range:** Gate2 enable→P3-5 pre-auth→Gate3 mandatory. Degrade: 3 fails|<95% pass.

**Complexity:** 6 dims×weight 3(doc×2), 0-17. 0-3=light,4-7=std,8-17=thorough.

**Phase advance V2.9.4:** Gate phases (understand/spec/verify) require confirmed_at before advancing. Non-gate phases auto-confirm.

**Archive V2.9.4:** Refuses to archive if VERIFY not completed (even with --yes).

**Related work V2.9.4:** `stdd work add --type bugfix|test|experience|doc "desc" --commit <hash>`. Stored in .stdd.yaml `related_work` field.

**Batch anti-abuse V2.9.4:** add checks git diff (≤3 files), max_items=5, open warns about active change.

---

## Canonical YAML Schemas (5+1)

proposal.yaml: `meta, why:{problem}, what_changes, capabilities:{new,modified}, constraints, stakeholders, risk_areas, non_goals, critical, anchoring, success_criteria`

spec.yaml: `meta, requirements:[{id,description,scenarios:[{id,confidence,evidence,given,when,then(SHALL),and}]}]`

agent_spec.yaml: `meta, preconditions, steps:[{id,description,action,assertions:[{type,expect}]}]`

pending-adjustments.yaml: `meta, adjustments:[{id,original,actual,reason,severity,impact_scope,recorded_at}]`

design-adjustments.yaml: `meta:{requires_re_spec}, summary, categories, adjustments`

.canon-index.yaml: `version, proposals:{}, designs:{}, specs:{code:{},agent:{}}`

---

## .stdd.yaml Fields

| Field | Type | Default | Writer | Reader |
|-------|------|---------|--------|--------|
| change_id | str | — | new | all |
| status | str | active | new,archive,abort,rollback | guard,validate |
| current_phase | str | understand | new,state,phase | guard,status,state |
| task_type | str | code | new,user | guard,spec |
| mode | str | standard | new,Gate2 | build,verify |
| complexity_score | int\|null | null | understand | spec |
| score_confidence | str\|null | null | understand | spec |
| phases.<p>.status | str | pending | phases | all |
| phases.<p>.confirmed_at | str\|null | null | gate | guard(integrity),validate |
| long_range.enabled | bool | false | Gate2 | build,verify |
| traceability.{scenarios,tc_cases,functions} | int | 0 | spec,build | validate,trace |
| design_adjustments.count | int | 0 | build,verify | verify |
| related_work | list | [] | work | work |
| resume_context | str\|null | null | state | state |
| active_slice | str\|int\|null | null | state | state |
| last_action | str\|null | null | state,hooks | state |
| state_freshness.{verified_at,git_head} | str\|null | null | hooks | state |

---

## Version Evolution
V1.0(6Phase+7CLI)→V2.0(modular+10cmd)→V2.4(exp+CI+dep-graph)→V2.5(state+GateCLI+anchoring)→V2.7(ctx+dual-track+agent+Hooks)→V2.8(Plankton+structure+pass@k+12fm)→V2.9(lite+score+batch+upgrade+task_type)→V2.9.2(canon+guard+YAML-first)→V2.9.3(smart-guard+batch+compact)→V2.9.4(phase-integrity+task_type-perms+anti-abuse+related-work+28cmds)

---

> AI Reference Edition, compressed from `STDD_WHITEPAPER_V2.9_EN.md` (Stage D).
