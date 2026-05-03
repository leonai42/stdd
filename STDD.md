# STDD (Spec+Test Driven Development) — 通用流程指引

> 此文件可作为项目规则加载到任何 AI 编程平台（Cursor, Copilot, Windsurf 等）。
> 完整设计文档见 [DESIGN.md](DESIGN.md)

## 核心原则

STDD 是一套 Spec+Test 双驱动的研发流程，通过 6 个阶段将需求转化为高质量交付。

**三道强制确认门**：
1. Phase 1 结束：用户确认 proposal.md
2. Phase 2 结束：用户确认 design.md + specs + test-plan.md
3. Phase 5 结束：用户确认 test-report.md + design-adjustments.md

**核心理念**：
- Spec 先行：先定义行为（GIVEN/WHEN/THEN），再写代码
- TDD 执行：RED → GREEN → REFACTOR，按垂直切片推进
- 设计调整可追溯：实现中对设计的任何偏离必须记录
- 用户确认驱动：关键节点必须用户确认

## 六阶段流程

```
Phase 1: UNDERSTAND  →  proposal.md  →  用户确认
Phase 2: SPEC        →  design.md + specs + test-plan.md  →  用户确认
Phase 3: SLICE       →  tasks.md + slices.md  →  自动
Phase 4: BUILD       →  TDD RED→GREEN→REFACTOR  →  自动
Phase 5: VERIFY      →  test-report.md + design-adjustments.md  →  用户确认
Phase 6: DELIVER     →  archive + merge specs + git tag
```

## 关键规则

1. **模板先行**：编写任何文档前，必须先读取 `.stdd/templates/` 中的对应模板
2. **开发规范**：Phase 4 开始前，必须先读取 `.stdd/standards/<language>.md`
3. **Spec→Test 映射**：GIVEN→Arrange, WHEN→Act, THEN→Assert
4. **垂直切片**：每次只实现一个 spec Scenario → 1+ 测试 → 1 个实现单元
5. **测试覆盖**：新行为必须有测试；测试验证行为而非实现

## 目录结构

```
.stdd/              # STDD 系统文件
changes/            # 活跃变更
specs/              # 主规范
archive/            # 已完成变更
```

## 文档模板

所有模板位于 `.stdd/templates/`：
- `proposal.md` — 变更提案
- `design.md` — 技术设计
- `spec.md` — 行为规格 (GIVEN/WHEN/THEN)
- `test-plan.md` — 测试方案
- `tasks.md` — 任务清单
- `slices.md` — 切片计划
- `design-adjustments.md` — 设计调整说明
- `test-report.md` — 测试报告

## 开发规范

位于 `.stdd/standards/`：
- `python.md` — Python 开发规范

## 命令

| 命令 | 说明 |
|------|------|
| `/stdd-understand` | Phase 1: 需求理解与确认 |
| `/stdd-spec` | Phase 2: 规格设计与测试方案 |
| `/stdd-continue` | 从当前阶段继续执行 (Phase 3-5) |
| `/stdd-status` | 查看当前变更状态 |
