# STDD 部署与使用指南 | Deployment & Usage Guide

> STDD (Spec+Test Driven Development) V2.9.6
> 适用平台 / Supported Platforms：Claude Code / Cursor / Copilot / Aider / WorkBuddy / Trae / OpenCode / Codex / Windsurf

---

## 一、系统要求 / System Requirements

| 依赖 / Dependency | 版本要求 / Version | 说明 / Notes |
|------------------|-------------------|-------------|
| Python | 3.10+ | 仅 CLI 辅助脚本需要 / CLI helper only |
| PyYAML | 6.0+ | `pip install pyyaml` |
| Git | 2.0+ | 版本管理 / Version control |
| AI 编程平台 / AI Platform | — | Claude Code / WorkBuddy / Trae / Cursor 等 |

---

## 二、安装方式 / Installation

### 方式一 / Method 1：在当前项目初始化（推荐 / Recommended）

```bash
# 1. 克隆 STDD 仓库 / Clone STDD repo
git clone <stdd-repo-url> /path/to/stdd-project

# 2. 进入你的项目目录 / Enter your project directory
cd /path/to/your-project

# 3. 运行 STDD 初始化 / Run STDD initialization
python /path/to/stdd-project/bin/stdd init
```

### 方式二 / Method 2：手动安装 / Manual Install

```bash
# 1. 创建目录结构 / Create directory structure
mkdir -p .stdd/skills .stdd/templates .stdd/standards
mkdir -p .stdd/platforms/claude-code/skills
mkdir -p .stdd/platforms/workbuddy/skills
mkdir -p .stdd/platforms/trae/skills
mkdir -p changes specs archive

# 2. 复制 STDD 核心文件到 .stdd/ / Copy STDD core files to .stdd/
cp -r /path/to/stdd-project/.stdd/config.d/ .stdd/
cp /path/to/stdd-project/.stdd/skills/*.md .stdd/skills/
cp /path/to/stdd-project/.stdd/templates/*.md .stdd/templates/
cp /path/to/stdd-project/.stdd/standards/*.md .stdd/standards/
cp /path/to/stdd-project/STDD.md .
cp /path/to/stdd-project/AGENTS.md .
```

### 方式三 / Method 3：安装到 AI 平台 / Install to AI Platform

```bash
# 安装到 Claude Code / Install to Claude Code
python /path/to/stdd-project/bin/stdd install claude-code

# 安装到 WorkBuddy / Install to WorkBuddy
python /path/to/stdd-project/bin/stdd install workbuddy

# 安装到 Trae / Install to Trae
python /path/to/stdd-project/bin/stdd install trae

# 安装到 Cursor（作为项目规则 / As project rules）
python /path/to/stdd-project/bin/stdd install cursor

# 安装到 OpenCode / Install to OpenCode
python /path/to/stdd-project/bin/stdd install opencode

# 安装到 OpenAI Codex CLI / Install to OpenAI Codex CLI
python /path/to/stdd-project/bin/stdd install codex
```

---

## 三、安装后验证 / Post-Installation Verification

```bash
# 检查目录结构 / Check directory structure
ls -la .stdd/
ls -la .stdd/skills/
ls -la .stdd/templates/

# 验证 CLI / Verify CLI
python /path/to/stdd-project/bin/stdd --help
python /path/to/stdd-project/bin/stdd status
```

---

## 四、使用流程 / Usage Flow

### 4.1 启动新变更 / Start a New Change

在 AI 编程平台中输入（以 Claude Code 为例）/ Type in your AI coding platform (Claude Code example)：

```
/stdd-understand 我们需要为 API 增加速率限制功能
/stdd-understand We need to add rate limiting to the API
```

系统将引导你完成 Phase 1（需求理解），生成 `proposal.md` 并等待确认。
The system will guide you through Phase 1 (requirement understanding), generate `proposal.md`, and wait for confirmation.

### 4.2 六阶段流程 / Six-Phase Flow

```
Phase 1: /stdd-understand  →  需求理解 / Understand → proposal.md → 用户确认 / User confirm
Phase 2: /stdd-spec        →  规格设计 / Spec design → design.md + specs + test-plan.md → 用户确认 / User confirm
Phase 3-5: /stdd-continue  →  自动迭代 / Auto-iterate：切片 / Slice → TDD实现 / TDD impl → 质量验证(11类失败模式+E2E+覆盖率) / Verify(11 failure modes+E2E+coverage) → 用户确认 / User confirm
Phase 6: /stdd-continue    →  交付 / Deliver：归档 / Archive + 合并 specs / Merge specs + git tag
```

### 4.3 常用命令 / Common Commands

| 命令 / Command | 说明 / Description |
|---------------|-------------------|
| `/stdd-understand <需求>` | Phase 1: 启动需求理解 / Start requirement understanding |
| `/stdd-spec` | Phase 2: 进入规格设计 / Enter spec design |
| `/stdd-continue` | 继续执行（Phase 3-6）/ Continue execution |
| `/stdd-status` | 查看当前变更状态 / View current change status |

### 4.4 CLI 辅助命令 / CLI Helper Commands

```bash
# 创建新 change / Create new change
stdd new feature-rate-limit

# 查看变更状态 / View change status
stdd status feature-rate-limit

# 验证变更结构 / Validate change structure
stdd validate feature-rate-limit

# 归档已完成变更 / Archive completed change
stdd archive feature-rate-limit

# 追溯 spec↔test↔code / Trace spec↔test↔code
stdd trace TC-RATE-001

# 回滚变更 / Rollback change
stdd rollback feature-rate-limit

# 查看变更差异 / View change diff
stdd diff feature-rate-limit

# 中止变更 / Abort change
stdd abort feature-rate-limit
```

---

## 五、目录结构 / Directory Structure

```
你的项目 / Your Project/
├── .stdd/                          # STDD 系统目录 / System directory
│   ├── config.d/                  # 项目配置 / Project config
│   ├── skills/                     # 6 个阶段 Skill / 6 phase skills
│   ├── templates/                  # 9 个文档模板 / 9 document templates
│   ├── standards/                  # 10 语言开发规范 / 10 language dev standards
│   │   ├── python.md               # Python
│   │   └── ...                      # Java, Go, Rust, TypeScript, JavaScript, C/C++, Kotlin, Swift, Dart
│   └── platforms/                  # 多平台适配 / Platform adapters
│       ├── claude-code/skills/
│       ├── codex/skills/
│       ├── workbuddy/skills/
│       ├── trae/skills/
│       └── opencode/skills/
├── changes/                        # 活跃变更 / Active changes
│   └── <YYYY-MM-DD>-<name>/
│       ├── .stdd.yaml              # 变更状态 / Change state
│       ├── proposal.md
│       ├── design.md
│       ├── specs/<capability>/spec.md
│       ├── test-plan.md
│       ├── tasks.md
│       ├── slices.md (可选 / Optional)
│       ├── pending-adjustments.md
│       ├── design-adjustments.md
│       └── test-report.md
├── specs/                          # 主规范（合并后）/ Master specs (merged)
│   └── <capability>/spec.md
├── archive/                        # 已完成变更 / Completed changes
├── STDD.md                         # 通用流程指引 / Universal guide
└── AGENTS.md                       # 项目记忆文件 / Project memory
```

---

## 六、平台适配说明 / Platform Adapter Notes

### 6.1 Claude Code

Skills 安装到 `.claude/skills/<name>/SKILL.md`，通过 `/stdd-xxx` 斜杠命令调用。
Skills installed to `.claude/skills/<name>/SKILL.md`, invoked via `/stdd-xxx` slash commands.

```bash
python /path/to/stdd-project/bin/stdd install claude-code
```

### 6.2 Cursor

STDD 作为项目规则安装，自动加载。
Installed as project rules, auto-loaded.

```bash
python /path/to/stdd-project/bin/stdd install cursor
```

### 6.3 GitHub Copilot

安装为 `.github/copilot-instructions.md`。
Installed as `.github/copilot-instructions.md`.

```bash
python /path/to/stdd-project/bin/stdd install copilot
```

### 6.4 Aider

安装为 `.aider.conf.yml` 配置文件。
Installed as `.aider.conf.yml` config.

```bash
python /path/to/stdd-project/bin/stdd install aider
```

### 6.5 WorkBuddy

Skills 安装到 `~/.workbuddy/skills/`，通过关键词匹配触发。
Skills installed to `~/.workbuddy/skills/`, triggered by keyword matching.

```bash
python /path/to/stdd-project/bin/stdd install workbuddy
# 重启 WorkBuddy 或在对话框中输入 /reload stdd
# Restart WorkBuddy or type /reload stdd in the dialog
```

### 6.6 Trae

Skills 安装到 `.trae/skills/`，通过 `/stdd-xxx` 调用。
Skills installed to `.trae/skills/`, invoked via `/stdd-xxx`.

```bash
python /path/to/stdd-project/bin/stdd install trae
```

### 6.7 OpenCode

Skills 安装到 `.opencode/skills/<name>/SKILL.md`，通过 `/stdd-xxx` 斜杠命令调用。
Skills installed to `.opencode/skills/<name>/SKILL.md`, invoked via `/stdd-xxx` slash commands.

```bash
python /path/to/stdd-project/bin/stdd install opencode
# 重启 OpenCode 或在对话框中输入 /stdd-understand <需求>
# Restart OpenCode or type /stdd-understand <requirement> in the dialog
```

> **注意 / Note**：OpenCode 的 skill 加载机制与 Claude Code 类似，使用相同的 YAML frontmatter 格式和目录结构（一个 skill 一个子目录）。
> OpenCode's skill loading mechanism is similar to Claude Code, using the same YAML frontmatter format and directory structure (one skill per subdirectory).

### 6.8 OpenAI Codex CLI

Skills 安装到 `.codex/skills/<name>/SKILL.md`，通过 `/stdd-xxx` 斜杠命令调用。Codex CLI 启动时自动加载 `.codex/skills/` 目录下的 skills，同时读取项目根 `AGENTS.md` 作为指令文件。
Skills installed to `.codex/skills/<name>/SKILL.md`, invoked via `/stdd-xxx` slash commands. Codex CLI auto-loads skills from `.codex/skills/` on startup, and reads `AGENTS.md` as instruction file.

```bash
python /path/to/stdd-project/bin/stdd install codex
# 重启 Codex CLI 或在对话框中输入 /stdd-understand <需求>
# Restart Codex CLI or type /stdd-understand <requirement> in the dialog
```

> **注意 / Note**：Codex CLI 的 skill 机制与 Claude Code / OpenCode 类似，使用相同的 YAML frontmatter 格式和 directory-per-skill 目录结构（一个 skill 一个子目录）。Codex CLI 也通过 `~/.codex/config.toml` 支持 `project_doc_fallback_filenames` 配置来读取其他平台的指令文件。
> Codex CLI's skill mechanism is similar to Claude Code / OpenCode, using the same YAML frontmatter format and directory-per-skill structure (one skill per subdirectory). Codex CLI also supports `project_doc_fallback_filenames` in `~/.codex/config.toml` to read instruction files from other platforms.

### 6.9 Windsurf（手动 / Manual）

```bash
# 手动复制 STDD.md 为项目规则 / Manually copy as project rules
cp STDD.md .windsurfrules
```

---

## 七、配置说明 / Configuration

`.stdd/config.d/` 中的关键配置项 / Key configuration items in `.stdd/config.d/`：

```yaml
# 项目信息 / Project info
project:
  name: my-project
  language: python          # 开发语言（影响规范加载）/ Language (affects standard loading)

# 强制确认门（不可关闭）/ Mandatory gates (cannot be disabled)
gates:
  phase1_understand:
    required: true          # Phase 1 必须用户确认 / User confirmation required
  phase2_spec:
    required: true          # Phase 2 必须用户确认 / User confirmation required
  phase5_verify:
    required: true          # Phase 5 必须用户确认 / User confirmation required

# 质量检查命令 / Quality check commands
quality:
  test: "pytest tests/ -v"
  lint: "ruff check app/ tests/"
  typecheck: null                     # 暂不启用 / Not yet enabled

  # E2E 测试 / E2E tests (V1.2)
  e2e:
    enabled: false                    # 项目级开关，默认关闭
    runner: playwright                # playwright | cypress | custom_script
    command: null                     # 自定义命令
    scope: critical_only              # critical_only | full

  # 覆盖率诊断 / Coverage diagnostics (V1.2)
  coverage:
    enabled: true                     # 诊断模式，不阻断
    tool: pytest-cov
    fail_under: 0                     # 0 = 不阻断，仅报告
    scope: changed_files_only         # changed_files_only | full

  # 多 Python 版本 / Multi Python versions (V1.2)
  python_versions: []                 # 如 ["3.10", "3.12"]，为空不执行

# TC-ID 规则 / TC-ID rule
tc_id:
  pattern: "TC-{CAPABILITY}-{NNN}"
```

---

## 八、开发规范的使用 / Using Development Standards

Phase 4 (BUILD) 开始前，Skill 会自动读取 `.stdd/standards/<language>.md`。
Before Phase 4 (BUILD) begins, the Skill automatically reads `.stdd/standards/<language>.md`.

当前支持的开发规范 / Currently supported standards（共 10 门语言 / 10 languages total）：
- `python.md` — Python 3.10+ 开发规范（V1.0 起）/ Python dev standard
- `java.md` — Java / Spring Boot（V2.3 新增）
- `go.md` — Go 标准布局（V2.3 新增）
- `rust.md` — Rust / Cargo（V2.3 新增）
- `typescript.md` — TypeScript / Node.js（V2.3 新增）
- `javascript.md` — JavaScript / Node.js（V2.9.6 新增）
- `c.md` — C/C++ 系统级开发（V2.9.6 新增）
- `kotlin.md` — Kotlin / Android（V2.9.6 新增）
- `swift.md` — Swift / iOS/macOS（V2.9.6 新增）
- `dart.md` — Dart / Flutter（V2.9.6 新增）

---

## 九、常见问题 / FAQ

### Q: 如何在已有项目中引入 STDD？/ How to introduce STDD to an existing project?

```bash
cd existing-project
python /path/to/stdd-project/bin/stdd init
```

### Q: 已有 OpenSpec 项目如何迁移？/ How to migrate from an existing OpenSpec project?

将 `openspec/specs/` 复制到 `specs/`，将 `openspec/changes/` 中的活跃变更复制到 `changes/`。目录结构兼容。
Copy `openspec/specs/` to `specs/`, copy active changes from `openspec/changes/` to `changes/`. Directory structures are compatible.

### Q: 如何切换开发语言？/ How to switch the development language?

修改 `.stdd/config.d/` 中的 `project.language`，然后创建对应的 `.stdd/standards/<language>.md`。
Modify `project.language` in `.stdd/config.d/`, then create the corresponding `.stdd/standards/<language>.md`.

### Q: CLI 脚本报 Unicode 错误（Windows）？/ CLI script reports Unicode errors on Windows?

设置环境变量 / Set environment variable：`set PYTHONIOENCODING=utf-8`，或使用 Windows Terminal（而非 cmd.exe）。
Or use Windows Terminal instead of cmd.exe.
