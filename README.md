# STDD — Spec+Test Driven Development

<p align="center">
  <b>为高质量 AI 编程而生 | Built for High-Quality AI Coding</b>
</p>

<p align="center">
  <b>V2.3</b> &nbsp;·&nbsp; MIT License &nbsp;·&nbsp; Python 3.10+
</p>

---

> **AI 编程不只是"写代码"，而是"写出正确的代码"** — 当工程实践遇见 AI 辅助开发。
> **AI coding isn't just about "writing code" — it's about "writing correct code"** — engineering practices meet AI-assisted development.
>
> STDD 是一套 **Spec 先行 + TDD 执行** 的 AI 辅助研发流程系统。6 个有序阶段 + 3 道强制确认门 + 11 类失败模式检查 + 双向可追溯链，将模糊需求转化为高质量交付。支持 5 门语言（Python / Java / Go / Rust / TypeScript），适配 6 大 AI 编程平台。

---

## 目录 / Table of Contents

- [什么是 STDD / What is STDD](#什么是-stdd--what-is-stdd)
- [为什么选择 STDD / Why STDD](#为什么选择-stdd--why-stdd)
- [六阶段流程 / Six-Phase Flow](#六阶段流程--six-phase-flow)
- [核心能力 / Core Features](#核心能力--core-features)
- [快速开始 / Quick Start](#快速开始--quick-start)
- [CLI 命令 / CLI Commands](#cli-命令--cli-commands)
- [支持的平台 / Supported Platforms](#支持的平台--supported-platforms)
- [多语言规范 / Multi-Language Standards](#多语言规范--multi-language-standards)
- [项目结构 / Project Structure](#项目结构--project-structure)
- [实战案例 / Case Studies](#实战案例--case-studies)
- [版本演进 / Version History](#版本演进--version-history)
- [文档导航 / Documentation](#文档导航--documentation)
- [参与贡献 / Contributing](#参与贡献--contributing)
- [许可证 / License](#许可证--license)

---

## 什么是 STDD / What is STDD

**STDD (Spec+Test Driven Development)** 是一套 AI 辅助的研发流程方法论与工具系统。它的核心思想是：**先定义行为（Spec），再编写测试（Test），最后实现代码** — 通过 6 个有序阶段和 3 道强制用户确认门，确保 AI 生成的每一行代码都有据可查、有测可验。

**STDD (Spec+Test Driven Development)** is an AI-assisted development methodology and tool system. Its core idea: **define behavior first (Spec), write tests second (Test), implement code last** — 6 ordered phases and 3 mandatory user confirmation gates ensure every line of AI-generated code is traceable and verifiable.

### 核心理念 / Core Philosophy

| 原则 / Principle | 说明 / Description |
|-----------------|-------------------|
| **Spec 先行 / Spec First** | 先定义行为（GIVEN/WHEN/THEN 格式），再写代码，杜绝需求歧义 |
| **TDD 执行 / TDD Execution** | RED → GREEN → REFACTOR，按垂直切片推进，每个切片可独立验证 |
| **设计调整可追溯 / Traceable** | 实现中对设计的任何偏离必须记录到 design-adjustments.md，Gate 3 统一审核 |
| **用户确认驱动 / User-Confirmed** | 3 道强制确认门（需求→设计→质量），关键节点不可跳过 |

### 三道强制确认门 / Three Mandatory Gates

```
Gate 1 ── Phase 1 结束 ── 用户确认 proposal.md（范围、边界、成功标准）
Gate 2 ── Phase 2 结束 ── 用户确认 design.md + specs + test-plan.md（最关键的分水岭）
Gate 3 ── Phase 5 结束 ── 用户确认 test-report.md + design-adjustments.md（质量终审）
```

Gate 2 之后可选择**全自动长程模式**：一次性预授权后，Phase 3-5 连续自动执行，仅 Gate 3 等待确认。也可选择**普通交互模式**，每阶段按需暂停。

---

## 为什么选择 STDD / Why STDD

### 适合谁 / Who Is It For

| 场景 / Scenario | 为什么适用 / Why |
|----------------|-----------------|
| **金融 / 医疗 IT 团队** | 需要高可靠性、强合规性、全链路追溯的高风险领域。内置风控规则校验、审计日志、精度约束 |
| **AI 编程实践者** | 经常遇到"AI 跑偏"问题？STDD 的 11 类失败模式检查系统性堵住 AI 常见错误 |
| **技术团队 Leader** | 想引入 AI 辅助研发，需要保证代码质量和可追溯性。3 道确认门让你掌控关键决策 |
| **开源项目维护者** | 接受 AI 贡献代码，但担心不可追溯、质量不可控。Spec 先行确保贡献符合预期 |

### STDD 解决的 AI 编程核心问题 / Problems STDD Solves

1. **需求歧义 → Spec 先行**：GIVEN/WHEN/THEN 格式将模糊需求转化为可验证的行为规格
2. **AI 跑偏 → 11 类失败检查**：系统性检测幻觉行为、范围蔓延、级联错误、指令衰减等 AI 特有问题
3. **质量不可控 → TDD 执行**：先写测试再写代码，测试通过才是完成
4. **过程黑箱 → 双向追溯**：Scenario → TC-ID → 测试函数 → 源码，完整映射链可查询
5. **设计偏离 → 强制记录**：任何设计偏离自动记录，Gate 3 统一审核，绝不静默

---

## 六阶段流程 / Six-Phase Flow

| 阶段 / Phase | 触发 / Trigger | 产出物 / Artifacts | 确认门 / Gate |
|-------------|---------------|-------------------|--------------|
| **P1: UNDERSTAND** | `/stdd-understand <需求>` | proposal.md | **Gate 1** · 强制用户确认 |
| **P2: SPEC** | `/stdd-spec` | design.md + specs/\*.md + test-plan.md | **Gate 2** · 强制用户确认（最关键） |
| **P3: SLICE** | 自动 / Auto | tasks.md + slices.md | 无（Gate 2 后可长程自动） |
| **P4: BUILD** | 自动 / Auto | TDD RED→GREEN→REFACTOR | 仅阻塞时暂停 |
| **P5: VERIFY** | 自动 / Auto | test-report.md + design-adjustments.md | **Gate 3** · 强制用户确认 |
| **P6: DELIVER** | `/stdd-continue` | archive + merge specs + git tag | 无 |

### 各阶段详解 / Phase Details

**Phase 1: UNDERSTAND — 需求理解**
将模糊需求转化为清晰、可验证的变更提案（proposal.md）。包含 Why / What Changes / Capabilities / Impact / Success Criteria。确认前不生成文件。

**Phase 2: SPEC — 规格设计** ⭐ *最关键阶段*
将 proposal 转化为精确的技术规格和测试方案。产出技术设计（design.md）、行为规格（specs/\*.md，GIVEN/WHEN/THEN 格式）、测试方案（test-plan.md，含 TC-ID 映射与覆盖矩阵）。Gate 2 确认后锁定设计基线。

**Phase 3: SLICE — 切片规划**
将测试方案拆分为可独立实现的垂直切片（1 个 spec Scenario → 1+ 测试 → 1 个实现单元）。按依赖关系拓扑排序，P0 优先。

**Phase 4: BUILD — TDD 实现**
逐切片执行 RED → GREEN → REFACTOR 循环。先写测试（RED），再写最小实现（GREEN），最后重构（REFACTOR）。设计偏离自动记录到 pending-adjustments.md。

**Phase 5: VERIFY — 质量验证**
全量测试 + 覆盖率诊断 + 多版本测试 + E2E 测试 + Lint + Diff 审查 + **11 类失败模式检查**。普通模式最多 5 轮迭代，长程模式最多 10 轮。汇总设计调整到 design-adjustments.md。

**Phase 6: DELIVER — 交付**
归档变更到 archive/ → 合并 specs 到 specs/ → Git commit + tag。

> 完整流程详解见 [STDD.md](STDD.md)，系统设计见 [DESIGN.md](DESIGN.md)

---

## 核心能力 / Core Features

| 能力 / Feature | 说明 / Description |
|---------------|-------------------|
| **Spec 先行** | GIVEN/WHEN/THEN 格式定义行为，THEN 中 SHALL 标记强制行为，杜绝需求歧义 |
| **3 道强制确认门** | 需求→设计→质量三处不可跳过。Gate 2 是分水岭，之后可选全自动长程模式 |
| **长程无人值守** | Gate 2 后一次性预授权，Phase 3-5 全自动连续执行，90%+ 操作无需人工干预 |
| **双向可追溯** | Scenario → TC-ID → 测试函数 → 源码，`stdd trace` 命令一键追溯完整映射链 |
| **11 类故障检查** | 幻觉行为、范围蔓延、级联错误、上下文丢失、工具误用、运行时偏差、管线断链、内容质量偏差、指令衰减、覆盖真空、契约断层 |
| **覆盖差异分析** | `stdd diff` 输出 spec 与测试之间的覆盖缺口对比表，一目了然 |
| **设计调整追溯** | 实现过程中的任何设计偏离自动记录到 design-adjustments.md，Gate 3 统一审核 |
| **11 命令 CLI 工具** | init / install / new / validate / status / archive / trace / diff / rollback / abort + `--dry-run` |
| **内置 Review 审查** | V2.1 起内置代码审查能力，AI 实现后自动 Review，确保质量一致性 |

### 11 类失败模式 / Eleven Failure Modes

| # | 模式 / Mode | 检测内容 / What It Detects | 引入版本 |
|---|------------|---------------------------|---------|
| (a) | 幻觉行为 / Hallucinated actions | 编造的文件路径、环境变量、函数名、库 API | V1.0 |
| (b) | 范围蔓延 / Scope creep | 超出计划文件的改动 | V1.0 |
| (c) | 级联错误 / Cascading errors | 异常被静默吞掉、空数组 fallback 掩盖问题 | V1.0 |
| (d) | 上下文丢失 / Context loss | 与 proposal/design/spec 决策矛盾 | V1.0 |
| (e) | 工具误用 / Tool misuse | 错误的工具选择或参数 | V1.0 |
| (f) | 运行时行为偏差 / Runtime deviation | 静态结构正确但动态行为异常 | V1.1 |
| (g) | 管线断链 / Pipeline chain break | 多步转换链路缺失步骤或隐式假定 | V1.1 |
| (h) | 内容质量偏差 / Content quality | 数据不一致、长度越界、引用缺失 | V1.1 |
| (i) | 指令衰减 / Instruction decay | Prompt 明确写了但 AI 未充分执行 | V1.1 |
| (j) | 覆盖真空 / Coverage vacuum | 某 capability 零自动化测试覆盖 | V1.2 |
| (k) | 契约断层 / Contract gap | 跨 capability API 字段名/header 不一致 | V1.2 |

---

## 快速开始 / Quick Start

### 前置要求 / Prerequisites

- Python 3.10+（仅 CLI 脚本需要 / CLI only）
- PyYAML 6.0+ (`pip install pyyaml`)
- pytest 7.0+ (`pip install pytest`)
- Git 2.0+
- 至少一个支持的 AI 编程平台

### 安装 / Installation

```bash
# 1. 克隆 STDD 仓库 / Clone the repository
git clone https://github.com/leonai42/stdd.git /path/to/stdd-project

# 2. 进入你的目标项目 / Enter your target project
cd /path/to/your-project

# 3. 初始化 STDD 目录结构 / Initialize STDD
python /path/to/stdd-project/bin/stdd init

# 4. 安装技能到 AI 平台（以 Claude Code 为例）/ Install skills to AI platform
python /path/to/stdd-project/bin/stdd install claude-code

# 也支持其他平台 / Also supports other platforms
python /path/to/stdd-project/bin/stdd install cursor
python /path/to/stdd-project/bin/stdd install copilot
python /path/to/stdd-project/bin/stdd install aider
```

### 开始第一个需求 / Start Your First Change

在 AI 编程平台中输入：

```
/stdd-understand 我们需要为 API 增加速率限制功能
```

系统将引导你完成 Phase 1（需求理解），生成 proposal.md 并等待确认。确认后继续：

```
/stdd-spec        # Phase 2: 规格设计与测试方案
/stdd-continue    # Phase 3-6: 自动迭代 → 交付
```

---

## CLI 命令 / CLI Commands

| 命令 / Command | 说明 / Description |
|---------------|-------------------|
| `stdd init` | 初始化 STDD 目录结构 / Initialize STDD directory structure |
| `stdd install <platform>` | 安装 skills 到目标 AI 平台 / Install skills to target AI platform |
| `stdd new <name>` | 创建新 change 目录骨架 / Create new change directory scaffold |
| `stdd validate [name]` | 验证 change 结构完整性 + spec 格式 + TC-ID 唯一性 |
| `stdd status [name]` | 查看变更当前阶段与状态 / View current phase and status |
| `stdd archive <name>` | 归档已完成变更并合并 specs / Archive completed change and merge specs |
| `stdd trace <tc-id>` | 追溯 spec↔test↔code 双向映射链 / Trace bidirectional mapping chain |
| `stdd diff [name]` | 显示 spec↔test 覆盖差异表 / Show spec↔test coverage gap table |
| `stdd rollback <name>` | 从 archive 恢复已归档变更 / Restore archived change |
| `stdd abort <name>` | 放弃变更并归档 / Abort change and archive |
| `--dry-run` | 全局选项：预览操作但不修改文件系统 / Preview without modifying filesystem |
| `--verbose` / `-v` | 分级日志输出 / Verbose logging |

---

## 支持的平台 / Supported Platforms

| 平台 / Platform | 安装方式 / Install | 调用方式 / Invocation |
|----------------|-------------------|----------------------|
| **Claude Code** | `stdd install claude-code` | `/stdd-xxx` 斜杠命令 |
| **Cursor** | `stdd install cursor` | 项目规则自动加载 |
| **GitHub Copilot** | `stdd install copilot` | `.github/copilot-instructions.md` |
| **Aider** | `stdd install aider` | `.aider.conf.yml` |
| **WorkBuddy** | `stdd install workbuddy` | 关键词匹配触发 |
| **Trae** | `stdd install trae` | `/stdd-xxx` 斜杠命令 |

> 对于 Windsurf 等无自动安装支持的平台，可将 `STDD.md` 手动复制为 `.windsurfrules`。

---

## 多语言规范 / Multi-Language Standards

Phase 4 开始前自动加载对应语言的开发规范。V2.3 已覆盖 5 大主流语言：

| 语言 / Language | 测试框架 / Test Framework | Lint 工具 | 引入版本 |
|---------------|--------------------------|----------|---------|
| **Python** | pytest | ruff | V1.0 |
| **Java** | JUnit 5 + Mockito | Checkstyle | V2.3 |
| **Go** | testing + testify | golangci-lint | V2.3 |
| **Rust** | cargo test | clippy + rustfmt | V2.3 |
| **TypeScript** | Jest | ESLint + Prettier | V2.3 |

---

## 项目结构 / Project Structure

```
STDD 项目仓库 / STDD Repo                 你的项目（安装后）/ Your Project (after init)
├── .stdd/                                ├── .stdd/
│   ├── skills/          # 6 阶段 Skill   │   ├── skills/templates/standards/
│   ├── skills/_shared/  # DRY 共享片段   │   ├── config.d/        # 模块化配置
│   ├── templates/       # 9 文档模板     │   └── platforms/       # 多平台适配
│   ├── standards/       # 5 语言规范     ├── specs/               # 主规范 / Master specs
│   ├── config.d/        # 模块化配置     ├── changes/             # 活跃变更 / Active changes
│   └── platforms/       # 6 平台适配     ├── archive/             # 已完成 / Archived
├── stdd/cli/            # CLI 模块       ├── STDD.md
├── bin/stdd             # CLI 入口       └── AGENTS.md
├── tests/               # STDD 自身测试
├── STDD.md              # 通用流程指引
├── DESIGN.md            # 系统设计文档
├── DEPLOY.md            # 部署与使用指南
├── EXTENDING.md         # 扩展开发指南
├── TROUBLESHOOTING.md   # 故障排除指南
├── CHANGELOG.md         # 变更日志
├── CONTRIBUTING.md      # 参与贡献指南
└── README.md
```

---

## 实战案例 / Case Studies

### FPPT — AI 驱动 PPT 生成系统

基于 STDD V1.2 流程，5 天从 0 到可发布产品。

| 指标 | 数据 |
|------|------|
| 代码行数 | 27,826 行（不含 node_modules） |
| 测试通过率 | 100%（326 个可执行用例） |
| AI 自动化率 | 90%+（Phase 3-5 长程模式） |
| 规格文件 | 41 份 spec.md，319+ 个 Scenarios |
| 测试密度 | 每 2.4 行业务代码对应 1 行测试代码 |
| 人效比 | 1,400 行/人时 |

### TStrategy — 量化交易系统

基于 STDD 方法论的中短线趋势策略系统，已迭代至 V4.2 稳定版。19,500+ 行测试代码，多层评分决策体系 + 多级风控防护。完整的 changes/ + specs/ 目录，每次策略迭代走完整六阶段流程。

### Visio Flowchart Skill — 小型项目

1 小时以内，完整 STDD 六阶段流程，271 行核心交付件，29 TC 100% 通过率。证明 STDD 不只适用于中大型项目 — 小型任务同样能从中获益，质量不因规模而妥协。

---

## 版本演进 / Version History

| 版本 | 日期 | 核心变更 |
|------|------|---------|
| **V2.3** | 2026-05-18 | 基础配套完善：5 语言规范 + 6 平台扩展 + 配置模块化 + Skill 标准化 |
| **V2.2** | 2026-05-15 | 流程体验优化：Gate 交互信息完善 + 长程模式可靠性提升 |
| **V2.1** | 2026-05-14 | 方法论增强：全面修复 80 项评审问题 + 内置 Review 能力 |
| **V2.0** | 2026-05-13 | 架构升级：CLI 模块化拆分 + 11 命令 + pytest 测试框架 |
| **V1.x** | 2026-05 | 基础建设：6 阶段流程 → 长程模式 → 11 类失败模式 → E2E + 覆盖率 |

详见 [CHANGELOG.md](CHANGELOG.md)

---

## 文档导航 / Documentation

| 文档 / Document | 内容 / Content |
|----------------|---------------|
| [STDD.md](STDD.md) | 通用流程指引，可作为项目规则加载到无 Skill 系统的 AI 平台 |
| [DESIGN.md](DESIGN.md) | 完整系统设计：架构、状态机、跨平台设计、用户交互协议 |
| [DEPLOY.md](DEPLOY.md) | 部署与使用指南：安装方式、配置说明、平台适配、FAQ |
| [EXTENDING.md](EXTENDING.md) | 扩展开发指南：新增平台/语言规范/失败模式/CLI 命令 |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | 故障排除：常见问题与解决方案 |
| [CHANGELOG.md](CHANGELOG.md) | 完整版本变更日志 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 参与贡献指南 |

---

## 参与贡献 / Contributing

我们欢迎社区贡献！无论是报告 Bug、提出功能建议、新增语言规范或平台适配，请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细流程。

We welcome community contributions! Whether reporting bugs, suggesting features, adding language standards or platform adapters, please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 许可证 / License

[MIT License](LICENSE)

Copyright (c) 2026 杭州大道一以科技有限公司

---

<p align="center">
  <b>Spec 先行，TDD 执行，质量不靠运气，靠系统。</b><br>
  <sub>Spec First, TDD Execution — quality comes from the system, not luck.</sub>
</p>
