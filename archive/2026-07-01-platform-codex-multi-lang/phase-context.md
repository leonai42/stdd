# Phase Context — 2026-07-01-platform-codex-multi-lang

> V2.9: Phase 间上下文传递，供 Phase 3-5 加载

## Phase 1-2 关键决策

1. **Codex 用 directory-per-skill**（`.codex/skills/stdd-<phase>/SKILL.md`），复用 `_make_claude_code_frontmatter`
2. **C/C++ 单文件 `c.md`**，内部 C/C++ 分区（用户已确认）
3. **5 语言规范均遵循 python.md 7 章 6 维度模板**
4. **最小化适配 + 渐进增强**（Codex 先做最小可用版本）
5. **AGENTS.md + STDD.md 双轨同步**更新平台/语言计数（8 平台、10 语言）

## 用户关注点

- 支持 Flutter/Dart 作为移动端跨平台方案
- Codex CLI 适配不要太重，先最小可用
- 语言规范质量优先于数量

## Phase 3-5 范围

- **平台实现**：`install.py` platform_map + `.stdd/platforms/codex/skills/` 6 个 SKILL.md
- **语言规范**：5 个 `.stdd/standards/{javascript,c,kotlin,swift,dart}.md`
- **文档更新**：`EXTENDING.md`、`AGENTS.md`、`STDD.md`、`README.md`、`README_EN.md`
- **测试**：13 个 TC（P0:10, P1:3）

## 产出物清单

| Phase | 文件 | 状态 |
|-------|------|------|
| 1 | proposal.md + proposal.yaml | ✅ |
| 2 | design.md | ✅ |
| 2 | specs/ ×7 | ✅ |
| 2 | test-plan.md | ✅ |
| 3 | slices.md | 待生成 |
| 4 | 实现文件（install.py + 平台文件 + 语言规范 + 文档） | 待实现 |
| 5 | test-report.md | 待生成 |
| 6 | archive | 待归档 |
