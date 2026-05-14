# STDD — Spec+Test Driven Development

> V1.4 · AI 辅助的 Spec 先行 + TDD 执行研发流程系统 | AI-assisted Spec-first + TDD execution methodology
>
> 通过 6 个阶段 + 3 道强制确认门保证研发质量 | 6 phases + 3 mandatory confirmation gates to ensure quality

---

## 核心理念 / Core Philosophy

---

## 快速开始 / Quick Start

```bash
# 1. 克隆本仓库 / Clone this repo
git clone <repo-url> /path/to/stdd-project

# 2. 进入你的目标项目 / Enter your target project
cd /path/to/your-project

# 3. 初始化 STDD / Initialize STDD
python /path/to/stdd-project/bin/stdd init

# 4. 安装 STDD 技能到 AI 平台 / Install skills to AI platform
python /path/to/stdd-project/bin/stdd install claude-code
```

---

## 六阶段流程 / Six-Phase Flow

| 阶段 / Phase | 命令 / Command | 产出物 / Artifacts | 确认门 / Gate |
|-------------|---------------|-------------------|--------------|
| **P1: UNDERSTAND** | `/stdd-understand <需求>` | proposal.md | **强制用户确认** / Forced |
| **P2: SPEC** | `/stdd-spec` | design.md + specs + test-plan.md | **强制用户确认** / Forced |
| **P3: SLICE** | 自动 / Auto | tasks.md + slices.md | 无 / None |
| **P4: BUILD** | 自动 / Auto | TDD RED→GREEN→REFACTOR | 仅阻塞时 / On blocker |
| **P5: VERIFY** | 自动 / Auto | test-report.md + design-adjustments.md | **强制用户确认** / Forced |
|                |            | 全量测试 + 覆盖率诊断 + E2E + Lint |                           |
|                |            | + 十一类失败模式检查 |                           |
| **P6: DELIVER** | `/stdd-continue` | archive + merge specs + git tag | 无 / None |

> 完整流程详解、关键规则、目录结构见 [STDD.md](STDD.md) — 可作为 AI 平台项目规则加载。
> See [STDD.md](STDD.md) for full flow details, key rules, and directory structure.

---
## 项目结构 / Project Structure

```
STDD 项目 / STDD Project                  你的项目（安装后）/ Your Project (after init)
├── .stdd/                                ├── .stdd/
│   ├── skills/          # 6 阶段 Skill   │   ├── skills/ templates/ standards/
│   ├── templates/       # 8 文档模板     │   └── platforms/ config.yaml
│   ├── standards/       # 开发规范       ├── specs/           # 主规范 / Master specs
│   └── platforms/       # 多平台适配     ├── changes/         # 活跃变更 / Active changes
├── bin/stdd             # CLI 脚本       ├── archive/         # 已完成 / Archived
├── STDD.md              # 通用流程指引   ├── STDD.md
├── DESIGN.md            # 系统设计       └── AGENTS.md
├── DEPLOY.md            # 部署指南
└── README.md
```

---

## CLI 命令 / CLI Commands

| 命令 / Command | 说明 / Description |
|---------------|-------------------|
| `stdd init` | 在当前项目初始化 STDD 目录结构 / Initialize STDD in current project |
| `stdd install <platform>` | 安装 skills 到指定 AI 平台 / Install skills to specified AI platform |
| `stdd new <name>` | 创建新 change 目录骨架 / Create new change directory scaffold |
| `stdd validate [name]` | 验证 change 结构完整性 / Validate change structure integrity |
| `stdd status [name]` | 查看变更当前阶段 / View current phase of a change |
| `stdd archive <name>` | 归档已完成变更并合并 specs / Archive completed change and merge specs |
| `stdd trace <tc-id>` | 追溯 spec↔test↔code 双向映射链 / Trace spec↔test↔code bidirectional chain |

---

## 支持的平台 / Supported Platforms

| 平台 / Platform | 安装命令 / Install | 调用方式 / Invocation |
|----------------|-------------------|----------------------|
| **Claude Code** | `stdd install claude-code` | `/stdd-xxx` 斜杠命令 |
| **WorkBuddy** | `stdd install workbuddy` | 关键词匹配触发 / Keyword trigger |
| **Trae** | `stdd install trae` | `/stdd-xxx` 斜杠命令 |
| **Cursor** | `stdd install cursor` | 项目规则自动加载 / Auto-load rules |
| **Windsurf** | 手动复制 / Manual copy | `.windsurfrules` |
| **GitHub Copilot** | 手动复制 / Manual copy | `.github/copilot-instructions.md` |

---

## 系统要求 / Requirements

- Python 3.10+（仅 CLI 脚本需要 / CLI only）
- PyYAML 6.0+ (`pip install pyyaml`)
- Git 2.0+
- 至少一个支持的 AI 编程平台 / At least one supported AI coding platform

---

## 更多文档 / Further Reading

- [系统设计文档 / Design Document](DESIGN.md) — 完整架构与机制设计 / Full architecture & mechanism design
- [部署与使用指南 / Deployment Guide](DEPLOY.md) — 安装方式、配置说明、常见问题 / Installation, config, FAQ
- [通用流程指引 / Universal Guide](STDD.md) — 可作为项目规则加载到无 Skill 系统的平台 / Loadable as project rules on platforms without skill systems

## License

MIT
