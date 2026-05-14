# AGENTS.md — STDD 项目记忆文件

## 项目概述

STDD (Spec+Test Driven Development) 是一套 AI 辅助的研发流程系统，通过 Spec 先行 + TDD 执行的方式保证研发质量。

## 目录结构

```
.stdd/                  # STDD 核心系统
  skills/               # 6 个阶段 Skill 文件
    _shared/            # DRY 共享片段（确认门/模式选择/长程授权）
  templates/            # 8 个文档模板
  standards/            # 开发规范（Python 默认）
  config.d/             # 模块化配置（project/gates/long_range/quality）
  platforms/            # 多平台适配层
stdd/cli/               # CLI 模块（15 个文件）
bin/stdd                # CLI 入口
changes/                # 活跃变更
specs/                  # 主规范
archive/                # 已完成变更
STDD.md                 # 通用流程指引
DESIGN.md               # 完整设计文档
```

## 常用命令

- `/stdd-understand` — 启动新变更的需求理解阶段
- `/stdd-spec` — 进入规格设计阶段
- `/stdd-continue` — 继续执行当前变更（Phase 3-5）
- `/stdd-status` — 查看变更状态

## 业务知识库

在进行基金、证券、期货、资产管理业务的设计与开发时，须参考 `.claude/memory/` 下的金融业务知识库：
- [基金资管业务知识库](.claude/memory/finance-knowledge-base.md) — 术语、公式、规则标准、监管规范
- 源文档位于 `D:\mycode\FPPT\output\finance-reference\`（4份规范文档，2026年5月版）

## 开发约定

- STDD 本身使用 STDD 流程开发
- Python 辅助脚本遵循 `.stdd/standards/python.md` 规范
- 模板和 Skill 文件使用中文编写
- 所有文档变更需经过 Phase 2 规格设计 + 用户确认

## 关键设计决策

- STDD 系统独立于 OpenSpec 和 EvanFlow，完全自建
- 核心为纯 Skill（Markdown 文件），辅以 Python 辅助脚本
- 跨平台兼容：Claude Code / WorkBuddy / Trae / Cursor / Copilot
- 混合模式：Skill 负责流程控制，Python 脚本负责结构化操作
