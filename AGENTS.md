# AGENTS.md — STDD 项目记忆文件 / Project Memory

## 项目概述 / Project Overview

STDD (Spec+Test Driven Development) 是一套 AI 辅助的研发流程系统，通过 Spec 先行 + TDD 执行的方式保证研发质量。支持 5 门语言（Python/Java/Go/Rust/TypeScript），适配 6 大 AI 编程平台。
STDD is an AI-assisted development methodology that ensures quality through Spec-first + TDD execution. Supports 5 languages across 6 AI platforms.

## 目录结构 / Directory Structure

```
.stdd/                  # STDD 核心系统 / Core system
  skills/               # 6 个阶段 Skill 文件 / 6 phase skill files
    _shared/            # DRY 共享片段（确认门/模式选择/长程授权）
  templates/            # 9 个文档模板 / 9 document templates
  standards/            # 5 语言开发规范 / 5 language dev standards
  config.d/             # 模块化配置 / Modular config (project/gates/long_range/quality)
  platforms/            # 6 平台适配层 / 6 platform adapters
stdd/cli/               # CLI 模块 / CLI modules
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
- Hybrid mode: Skills control the process ("how to think"), CLI handles structural operations ("what to do")
- Cross-platform: one set of core skills → `stdd install` generates platform-specific adapters
