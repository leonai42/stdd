# STDD (Spec+Test Driven Development) — 通用流程指引 | Universal Guide

> 此文件可作为项目规则加载到任何 AI 编程平台（Cursor, Copilot, Windsurf, Aider 等）。
> This file can be loaded as project rules on any AI coding platform (Cursor, Copilot, Windsurf, Aider, etc.).
>
> 完整设计文档见 / Full design document: [DESIGN.md](DESIGN.md)

---

## 核心原则 / Core Principles

STDD 是一套 Spec+Test 双驱动的研发流程，通过 6 个阶段将需求转化为高质量交付。
STDD is a Spec+Test dual-driven development methodology that transforms requirements into high-quality deliverables through 6 phases.

**三道强制确认门 / Three Mandatory Confirmation Gates**：
1. Phase 1 结束：用户确认 proposal.md | End of Phase 1: User confirms proposal.md
2. Phase 2 结束：用户确认 design.md + specs + test-plan.md | End of Phase 2: User confirms design + specs + test-plan
3. Phase 5 结束：用户确认 test-report.md + design-adjustments.md | End of Phase 5: User confirms test report + design adjustments

**Gate 2 后执行模式选择 / Execution Mode Selection After Gate 2**：
- 🚀 全自动长程模式（默认）：一次性预授权 → Phase 3-5 连续自动执行 → Gate 3 等待确认
- 📋 普通交互模式：Phase 3-5 按需暂停交互 → Gate 3 等待确认

**核心理念 / Core Philosophy**：
- Spec 先行 / Spec-first：先定义行为（GIVEN/WHEN/THEN），再写代码。Define behavior before writing code.
- TDD 执行 / TDD execution：RED → GREEN → REFACTOR，按垂直切片推进。Proceed by vertical slices.
- 设计调整可追溯 / Traceable adjustments：实现中对设计的任何偏离必须记录。Every design deviation must be documented.
- 用户确认驱动 / User-confirmation-driven：关键节点必须用户确认。Key checkpoints require explicit user confirmation.

---

## 六阶段流程 / Six-Phase Flow

```
Phase 1: UNDERSTAND  →  proposal.md  →  用户确认 / User confirm
Phase 2: SPEC        →  design.md + specs + test-plan.md  →  用户确认 / User confirm
                       └→ 执行模式选择（长程/普通）
Phase 3: SLICE       →  tasks.md + slices.md  →  自动 / Auto
Phase 4: BUILD       →  TDD RED→GREEN→REFACTOR  →  自动(长程)/按需交互(普通)
Phase 5: VERIFY      →  test-report.md + design-adjustments.md  →  用户确认 / User confirm
                       (十一类失败模式检查 / Eleven failure mode checks)
Phase 6: DELIVER     →  archive + merge specs + git tag
```

### 各阶段简要说明 / Phase Summary

**Phase 1: UNDERSTAND — 需求理解 | Requirement Understanding**
将模糊需求转化为清晰、可验证的变更提案（proposal.md）。Why / What Changes / Capabilities / Impact / Success Criteria。
Transform vague requirements into a clear, verifiable proposal (proposal.md). Why / What Changes / Capabilities / Impact / Success Criteria.

**Phase 2: SPEC — 规格设计 | Spec Design**
这是整个流程中**最重要的阶段** / **The most critical phase**。产出技术设计（design.md）、行为规格（specs/\*.md，GIVEN/WHEN/THEN 格式）、测试方案（test-plan.md，TC-ID 映射）。
Produce technical design (design.md), behavior specs (specs/\*.md, GIVEN/WHEN/THEN format), test plan (test-plan.md, TC-ID mapping).

**Phase 3: SLICE — 切片规划 | Slice Planning**
将测试方案拆分为可独立实现的垂直切片。按依赖排序，P0 优先。
Split test plan into independently implementable vertical slices. Ordered by dependency, P0 first.

**Phase 4: BUILD — TDD 实现 | TDD Implementation**
逐一执行 RED → GREEN → REFACTOR。先写测试（RED），再写最小实现（GREEN），最后重构（REFACTOR）。
Execute RED → GREEN → REFACTOR per slice. Write test first (RED), minimal implementation (GREEN), then refactor (REFACTOR).

**Phase 5: VERIFY — 质量验证 | Quality Verification**
全量测试 + 覆盖率诊断 + 多版本测试 + E2E 测试（可配置）+ Lint + Diff 审查 + 十一类失败模式检查。普通模式最多 5 轮迭代，长程模式最多 10 轮。汇总设计调整到 design-adjustments.md。
Full test + coverage diagnostics + multi-version test + E2E tests (configurable) + Lint + Diff review + eleven failure mode checks. Max 5 iterations (normal) or 10 (long-range). Summarize design adjustments to design-adjustments.md.

**Phase 6: DELIVER — 交付 | Delivery**
归档到 archive/ → 合并 specs 到 specs/ → Git commit + tag。
Archive to archive/ → merge specs to specs/ → Git commit + tag.

---

## 关键规则 / Key Rules

1. **模板先行 / Template First**：编写任何文档前，必须先读取 `.stdd/templates/` 中的对应模板。Must read the template before generating any document.
2. **开发规范 / Dev Standards**：Phase 4 开始前，必须先读取 `.stdd/standards/<language>.md`。Must read language standard before Phase 4.
3. **Spec→Test 映射 / Mapping**：GIVEN→Arrange, WHEN→Act, THEN→Assert。
4. **垂直切片 / Vertical Slice**：每次只实现一个 spec Scenario → 1+ 测试 → 1 个实现单元。One spec Scenario → 1+ tests → 1 implementation unit per slice.
5. **测试覆盖 / Test Coverage**：新行为必须有测试；测试验证行为而非实现。New behavior must have tests; tests verify behavior not implementation.

---

## 目录结构 / Directory Structure

```
.stdd/              # STDD 系统文件 / System files
changes/            # 活跃变更 / Active changes
specs/              # 主规范 / Master specs
archive/            # 已完成变更 / Completed changes
```

---

## 文档模板 / Document Templates

所有模板位于 / All templates at `.stdd/templates/`：
- `proposal.md` — 变更提案 / Change proposal
- `design.md` — 技术设计 / Technical design
- `spec.md` — 行为规格 (GIVEN/WHEN/THEN) / Behavior spec
- `test-plan.md` — 测试方案 / Test plan
- `tasks.md` — 任务清单 / Task list
- `slices.md` — 切片计划 / Slice plan
- `design-adjustments.md` — 设计调整说明 / Design adjustments
- `test-report.md` — 测试报告 / Test report

---

## 开发规范 / Development Standards

位于 / Located at `.stdd/standards/`：
- `python.md` — Python 开发规范 / Python dev standard（V1.0 起）
- `java.md` — Java / Spring Boot 规范（V2.3 新增）
- `go.md` — Go 标准布局规范（V2.3 新增）
- `rust.md` — Rust / Cargo 规范（V2.3 新增）
- `typescript.md` — TypeScript / Node.js 规范（V2.3 新增）

---

## 命令 / Commands

| 命令 / Command | 说明 / Description |
|---------------|-------------------|
| `/stdd-understand` | Phase 1: 需求理解与确认 / Requirement understanding |
| `/stdd-spec` | Phase 2: 规格设计与测试方案 / Spec & test design |
| `/stdd-continue` | 从当前阶段继续执行 (Phase 3-5) / Continue from current phase |
| `/stdd-status` | 查看当前变更状态 / View current change status |
