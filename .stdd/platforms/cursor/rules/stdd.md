# STDD — Spec+Test Driven Development

> 适配平台：Cursor IDE
> STDD 版本：V2.2
> 格式版本：Cursor Rules v1

## 概述

STDD 是一套双驱动（Spec + TDD）的开发方法论，6 个阶段从模糊需求 → 高质量交付，3 个强制用户确认门。

## 6 阶段流程

### Phase 1: UNDERSTAND — 需求理解

**触发关键词**：`/stdd-understand`、`STDD Phase 1`、`需求理解`

**流程**：探索问题 → 评估影响范围 → 生成 proposal.md → Gate 1 用户确认

**产出物**：`changes/<date>-<name>/proposal.md`

### Phase 2: SPEC — 规格设计

**触发关键词**：`/stdd-spec`、`STDD Phase 2`、`规格设计`

**流程**：技术设计 design.md → 行为规格 specs/*.md → 测试方案 test-plan.md → Gate 2 用户确认

**产出物**：`design.md`、`specs/<capability>/spec.md`、`test-plan.md`

### Phase 3: SLICE — 切片规划

**触发关键词**：`/stdd-slice`、`STDD Phase 3`、`切片规划`

**流程**：将 test-plan.md 的 TC 案例拆分为独立可实现的垂直切片

**产出物**：`tasks.md`、`slices.md`

### Phase 4: BUILD — TDD 实现

**触发关键词**：`/stdd-build`、`STDD Phase 4`、`TDD 实现`

**流程**：RED（写测试→失败）→ GREEN（最小实现→通过）→ REFACTOR（重构→保持绿色）

**原则**：测试先于代码，不写超过测试覆盖范围的代码

### Phase 5: VERIFY — 质量验证

**触发关键词**：`/stdd-verify`、`STDD Phase 5`、`质量验证`

**流程**：Step 0 多路并行评审 → Step 1 全量质量检查 → Step 2 Diff审查 → Step 3 十一类失败模式检查 → Step 4 设计调整汇总 → Step 5 测试报告 → Gate 3 用户确认

**产出物**：`test-report.md`、`design-adjustments.md`（如有）

### Phase 6: DELIVER — 交付

**触发关键词**：`/stdd-deliver`、`STDD Phase 6`、`交付`

**流程**：归档变更 → 合并 specs → 版本标记

**产出物**：`archive/` 中的归档文件、更新后的 `specs/`、git tag

## 3 个强制确认门

| Gate | 位置 | 确认内容 |
|------|------|---------|
| Gate 1 | Phase 1 结束 | 确认 proposal.md（范围/成功标准） |
| Gate 2 | Phase 2 结束 | 确认 design.md + specs + test-plan（技术方案/规格/测试覆盖） |
| Gate 3 | Phase 5 结束 | 确认 test-report.md + design-adjustments（测试结果/设计偏离） |

## 执行模式

- **长程模式**：一次性预授权 → Phase 3-5 全自动连续执行，仅 Gate 3 等待确认
- **普通模式**：逐步执行，重大偏离/阻塞时暂停交互

## 文件结构

```
.stdd/
├── standards/      # 语言开发规范（python/java/go/rust/typescript）
├── platforms/      # 平台适配（claude-code/cursor/copilot/aider/workbuddy/trae）
├── skills/         # Master skill 文件
├── templates/      # 文档模板
└── config.d/       # 配置文件（quality/project/long_range/gates）
```

## 使用方式

在 Cursor 对话中直接使用触发关键词启动对应阶段，AI 将按 STDD 流程引导你完成开发任务。

例如：
- "帮我做一个用户登录功能" → AI 自动进入 Phase 1 需求理解
- "/stdd-build" → AI 按切片执行 RED→GREEN→REFACTOR
