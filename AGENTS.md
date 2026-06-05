# AGENTS.md — STDD 项目记忆文件 / Project Memory

> **V2.9.2 强制门已启用**：本项目 `enforce_stdd: true`。修改代码前必须先走 STDD 流程（/stdd-understand）。
> 如果项目未启动 STDD change 而收到代码修改请求，请提示用户先启动 STDD 流程。

## 项目概述 / Project Overview

STDD (Spec+Test Driven Development) 是一套 AI 辅助的研发流程系统，通过 Spec 先行 + TDD 执行的方式保证研发质量。支持 5 门语言（Python/Java/Go/Rust/TypeScript），适配 6 大 AI 编程平台。
STDD is an AI-assisted development methodology that ensures quality through Spec-first + TDD execution. Supports 5 languages across 6 AI platforms.

## 目录结构 / Directory Structure

```
.stdd/                  # STDD 核心系统 / Core system
  skills/               # 6 个阶段 Skill 文件 / 6 phase skill files
    _shared/            # DRY 共享片段（确认门/模式选择/长程授权）
  templates/            # 10 个文档模板 / 10 document templates
  standards/            # 5 语言开发规范 / 5 language dev standards
  config.d/             # 模块化配置 / Modular config (project/gates/long_range/quality/experience)
  platforms/            # 6 平台适配层 / 6 platform adapters
  experiences/          # 自学习经验库 / Self-learning experience library (V2.5: 5状态生命周期)
stdd/cli/               # CLI 模块 / CLI modules (18 命令 / commands)
bin/stdd                # CLI 入口 / CLI entry point
changes/                # 活跃变更 / Active changes
specs/                  # 主规范 / Master specs
archive/                # 已完成变更 / Completed changes
```

## 常用命令 / Common Commands

| 命令 / Command | 用途 / Purpose |
|---------------|---------------|
| `/stdd-understand` | Phase 1: 启动新变更需求理解 / Start new change understanding |
| `/stdd-spec` | Phase 2: 进入规格设计 / Enter spec design |
| `/stdd-continue` | 继续执行当前变更（Phase 3-6）/ Continue current change |
| `/stdd-status` | 查看变更状态 / View change status |

## 开发约定 / Development Conventions

- STDD 自身使用 STDD 流程开发 / STDD is built using STDD methodology
- Python 辅助脚本遵循 `.stdd/standards/python.md` 规范
- 模板和 Skill 文件使用中英双语编写 / Templates and skills are bilingual (CN+EN)
- 所有文档变更需经过 Phase 2 规格设计 + 用户确认 / All doc changes go through Phase 2 + user confirmation

## 关键设计决策 / Key Design Decisions

- STDD 系统独立自建，核心为纯 Markdown Skill 文件，辅以 Python CLI 脚本
- 混合模式：Skill 负责流程控制（"怎么想"），CLI 负责结构化操作（"做什么"）
- 跨平台兼容：一套核心 Skill → `stdd install` 生成平台适配文件
- V2.5 新增：经验生命周期状态机（发现→验证→沉淀→共享→合并/退休）、社区经验共享池、多Agent并行切片、跨Session状态恢复、Gate文件确认、CI检查增强（scope/coverage/contracts）
- V2.4 新增：自学习经验库（项目级 AI 经验积累）、Spec 自动补全、智能切片推荐、CI/CD 集成
- Hybrid mode: Skills control the process ("how to think"), CLI handles structural operations ("what to do")
- Cross-platform: one set of core skills → `stdd install` generates platform-specific adapters
- V2.5 new: Experience lifecycle FSM (discover→verify→deposit→share→merge/retire), Community experience pool, Multi-agent parallel slices, Cross-session state resume, Gate file confirmation, CI checks enhanced (scope/coverage/contracts)
- V2.4 new: Self-learning experience library, Spec auto-complete, Smart slice recommendation, CI/CD integration

## 专项 Subagent 定义 / Specialized Subagents (V2.7)

> 以下 agent 默认禁用。在 quality.yaml review.agents 中按需启用。

### security-reviewer / 安全审计员
- **ID**: security-reviewer | **模型**: Opus | **阶段**: Phase 5
- **职责**: 注入/SQL/XSS/认证/敏感数据/依赖CVE 安全审计
- **触发**: Phase 5 VERIFY review 阶段启用，或手动 `/security-review`

### perf-analyzer / 性能分析师
- **ID**: perf-analyzer | **模型**: Sonnet | **阶段**: Phase 5
- **职责**: N+1查询/内存泄漏/阻塞IO/算法复杂度 性能分析
- **触发**: Phase 5 VERIFY review 阶段启用

### compat-checker / 兼容性检查员
- **ID**: compat-checker | **模型**: Sonnet | **阶段**: Phase 5
- **职责**: API breaking/依赖冲突/平台差异/Python版本兼容性
- **触发**: Phase 5 VERIFY review 阶段启用

### planner / 架构规划师
- **ID**: planner | **模型**: Opus | **阶段**: Phase 2
- **职责**: 独立执行技术设计，产出 design.md
- **触发**: quality.yaml 中 agents.planner.enabled=true 时，Phase 2 分离为 planner + spec-writer 双 Agent

## ⚠️ 强制性约束 / MANDATORY CONSTRAINTS (V2.7)

> 以下规则不可跳过、不可变通 / NEVER skip or override these rules:

| # | 中文 | English |
|---|------|---------|
| 1 | **绝不可跳过 Gate 确认** — 三道 Gate 必须用户明确确认 | **NEVER skip a Gate** — all three Gates require explicit user confirmation |
| 2 | **绝不静默修改设计** — 偏离必须记录到 design-adjustments.md | **NEVER silently deviate from design** — deviations MUST be recorded |
| 3 | **绝不可先写代码再补测试** — 严格 RED→GREEN→REFACTOR | **NEVER write code before tests** — strict RED→GREEN→REFACTOR |
| 4 | **绝不可跳过失败模式检查** — Phase 5 必须全量 12 类检查 | **NEVER skip failure mode checks** — all 12 categories mandatory |
| 5 | **绝不可跳过切片验证** — 每个切片必须通过 Step 1.4 验证 | **NEVER skip slice verification** — Step 1.4 mandatory per slice |
