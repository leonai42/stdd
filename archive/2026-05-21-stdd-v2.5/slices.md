# STDD V2.5 切片方案

> 版本：V1.0
> 创建日期：2026-05-21
> 总工时：~13.7d · 4 个 Slice

## 一、依赖关系图

```
experience-lifecycle (A) ──→ community-experience-pool (C)
                                    │
ci-check-enhanced (B1) ──→ (无上游依赖)
session-resume (B2) ──→ (无上游依赖)
gate-file-confirm (B3) ──→ (无上游依赖)
                                    │
extract-proposal-extended (D1) ──→ (无上游依赖)
non-code-change-support (D2) ──→ experience.py 数据模型 (依赖 A)
parallel-slice-guide (D3) ──→ (纯 skill，无依赖)
```

关键依赖链：
- **A → C**：community-experience-pool 的 pull/export/curate 依赖 experience-lifecycle 的状态机（`lifecycle_state` 字段和 `verify`/`retire` 命令）
- **A → D2**：non-code-change-support 的 `project_type` 写入依赖 experience.py 的数据模型
- **B1/B2/B3**：三者互不依赖，可与 A 并行
- **D1**：独立，可任意时间切入

## 二、切片分组

### Slice A：经验生命周期状态机（P0 · 2.5d）

**依赖**：无（基础设施层）
**风险**：🟡 中 — 修改 experience.py 核心逻辑，影响现有 13 个测试

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `stdd/cli/commands/experience.py` | 修改 | +`cmd_verify` / +`cmd_deposit` / +`cmd_retire` / +`_check_transition()` / +`_auto_promote()` |
| 2 | `.stdd/experiences/.experience-index.yaml` | — | schema 已有 `by_lifecycle`，无需改动 |
| 3 | `tests/commands/test_experience.py` | 修改 | +9 个 TC（TC-EXP-LC-001 ~ 009） |

**验证**：`pytest tests/commands/test_experience.py -v` — 9 个新测试 + 13 个回归测试全绿

---

### Slice B：CI 增强 + Session 恢复 + Gate 确认（P0+P1 · 4.0d）

**依赖**：无（三个独立模块，可并行开发）
**风险**：🟡 中 — ci.py 扩展 check-failures 注册表，需确保已有 14 个测试不退化

#### B1: ci-check-enhanced（1.5d）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 4 | `stdd/cli/commands/ci.py` | 修改 | +`check_scope_creep()` / +`check_coverage_vacuum()` / +`check_contract_gap()` / 注册到 CHECKS 列表 |
| 5 | `tests/commands/test_ci.py` | 修改 | +10 个 TC（TC-CI-ENH-001 ~ 010） |

#### B2: session-resume（1.0d）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 6 | `stdd/cli/commands/state.py` | 修改 | +`_write_resume_context()` / +`_read_resume_context()` / 4 字段读写 |
| 7 | `tests/commands/test_state.py` | 修改 | +4 个 TC（TC-SR-001 ~ 004） |

#### B3: gate-file-confirm（1.5d）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 8 | `stdd/cli/commands/gate.py` | **新建** | `cmd_approve()` + `_check_gate_order()` + `_check_file_token()` |
| 9 | `.stdd/config.d/gates.yaml` | 修改 | +`confirmation.channels` 配置段 |
| 10 | `tests/commands/test_gate.py` | **新建** | +7 个 TC（TC-GF-001 ~ 007） |

**验证**：`pytest tests/commands/test_ci.py tests/commands/test_state.py tests/commands/test_gate.py -v`

---

### Slice C：社区经验共享池（P1 · 4.5d）

**依赖**：Slice A（experience.py 状态机）
**风险**：🟡 中 — 新增 curate.py，扩展 experience.py，HTTP mock 测试

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 11 | `stdd/cli/commands/experience.py` | 修改 | +`cmd_pull()` / +`_download_with_fallback()` / +`cmd_export()` 增强 / +`_sanitize()` |
| 12 | `stdd/cli/commands/curate.py` | **新建** | +`cmd_curate_pull()` / +`cmd_curate_deduplicate()` / +`cmd_curate_review()` / +`cmd_curate_pack()` |
| 13 | `.stdd/config.d/experience.yaml` | 修改 | +`community` 配置段（registries / fallback_timeout / packs） |
| 14 | `tests/commands/test_experience.py` | 修改 | +15 个 TC（TC-COM-001 ~ 015，含 8 个新增 + 7 个已有占位） |
| 15 | `tests/commands/test_curate.py` | **新建** | curate 子命令测试 |

**验证**：`pytest tests/commands/test_experience.py tests/commands/test_curate.py -v`

---

### Slice D：proposal 扩展 + 非代码支持 + 并行切片（P1 · 2.7d）

**依赖**：Slice A（D2 的 project_type 写入依赖 experience.py 数据模型）
**风险**：🟢 低 — 主要是 skill 文件改动 + extract_proposal 字段扩展

#### D1: extract-proposal-extended（1.0d）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 16 | `stdd/cli/commands/extract_proposal.py` | 修改 | `_parse_section()` 扩展识别 Constraints/Stakeholders/RiskAreas/NonGoals |
| 17 | `.stdd/templates/proposal.md` | 修改 | +新字段 STDD-MARKER 标记 |
| 18 | `tests/commands/test_extract_proposal.py` | 修改 | +7 个 TC（TC-EPE-001 ~ 007） |

#### D2: non-code-change-support（0.7d）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 19 | `stdd/cli/commands/experience.py` | 修改 | +`_detect_project_type()` / 经验创建时自动标记 |
| 20 | `.stdd/skills/build.md` | 修改 | Step 0.5 +`project_type` 过滤逻辑 |
| 21 | `.stdd/skills/verify.md` | 修改 | Step 3 后 +非代码检查清单分支（5 项替代检查） |
| 22 | `tests/commands/test_experience.py` | 修改 | +5 个 TC（TC-NCC-001 ~ 005） |

#### D3: parallel-slice-guide（1.0d）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 23 | `.stdd/skills/build.md` | 修改 | +并行执行策略（parallel_group / 子任务派发 / 结果合并） |

> D3 是纯 skill 增强，目视验证，无 pytest。

**验证**：`pytest tests/commands/test_extract_proposal.py tests/commands/test_experience.py -v` + 目视 build.md / verify.md

---

## 三、执行顺序

```
Week 1:
  Day 1-2.5: Slice A (experience-lifecycle) ← 基础设施，优先
  Day 1-4:   Slice B (ci + session + gate) ← 与 A 并行启动

Week 2:
  Day 3-6.5: Slice C (community pool) ← 依赖 A 完成
  Day 5-7.7: Slice D (extract + non-code + parallel) ← D1 独立，D2 依赖 A
```

```
Timeline:
  Slice A: ████████░░░░░░░░ (2.5d)
  Slice B: ██████████████░░ (4.0d)  ← 三人并行：B1/B2/B3
  Slice C: ░░░░██████████████ (4.5d) ← 等 A 完成后启动
  Slice D: ░░░░░░░░█████████ (2.7d)  ← D2 等 A，D1/D3 可提前
```

## 四、文件改动汇总

| 文件 | Slice | 操作 |
|------|-------|------|
| `stdd/cli/commands/experience.py` | A, C, D2 | 修改 3 次 |
| `stdd/cli/commands/ci.py` | B1 | 修改 |
| `stdd/cli/commands/state.py` | B2 | 修改 |
| `stdd/cli/commands/gate.py` | B3 | **新建** |
| `stdd/cli/commands/curate.py` | C | **新建** |
| `stdd/cli/commands/extract_proposal.py` | D1 | 修改 |
| `.stdd/config.d/experience.yaml` | C | 修改 |
| `.stdd/config.d/gates.yaml` | B3 | 修改 |
| `.stdd/skills/build.md` | D2, D3 | 修改 |
| `.stdd/skills/verify.md` | D2 | 修改 |
| `.stdd/templates/proposal.md` | D1 | 修改 |
| `tests/commands/test_experience.py` | A, C, D2 | 修改 3 次 |
| `tests/commands/test_ci.py` | B1 | 修改 |
| `tests/commands/test_state.py` | B2 | 修改 |
| `tests/commands/test_gate.py` | B3 | **新建** |
| `tests/commands/test_curate.py` | C | **新建** |
| `tests/commands/test_extract_proposal.py` | D1 | 修改 |

**统计**：新建 3 文件 · 修改 14 文件 · 新增测试 ~60 个

## 五、风险与缓解

| 风险 | 等级 | 缓解 |
|------|------|------|
| experience.py 被 3 个 Slice 修改，合并冲突 | 🟡 | Slice A 先合入，C/D2 基于 A 的最终版本开发 |
| curate dedup 相似度算法精度 | 🟡 | 仅用关键词 Jaccard 重叠率，阈值 >80% 偏保守 |
| HTTP fallback mock 覆盖不足 | 🟢 | mock `requests.get` 的超时异常和状态码，不发起真实请求 |
| skill 文件膨胀（build.md 改两次） | 🟢 | D2 和 D3 的改动是独立段落（Step 0.5 vs 并行策略），不重叠 |
