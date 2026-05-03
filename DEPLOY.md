# STDD 部署与使用指南

> STDD (Spec+Test Driven Development) V1.0
> 适用平台：Claude Code / WorkBuddy / Trae / Cursor / Windsurf / GitHub Copilot

## 一、系统要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.10+ | 仅 CLI 辅助脚本需要 |
| PyYAML | 6.0+ | `pip install pyyaml` |
| Git | 2.0+ | 版本管理 |
| AI 编程平台 | — | Claude Code / WorkBuddy / Trae / Cursor 等 |

## 二、安装方式

### 方式一：在当前项目初始化（推荐）

```bash
# 1. 克隆 STDD 仓库
git clone <stdd-repo-url> /path/to/stdd-project

# 2. 进入你的项目目录
cd /path/to/your-project

# 3. 运行 STDD 初始化
python /path/to/stdd-project/bin/stdd init
```

### 方式二：手动安装

```bash
# 1. 创建目录结构
mkdir -p .stdd/skills .stdd/templates .stdd/standards
mkdir -p .stdd/platforms/claude-code/skills
mkdir -p .stdd/platforms/workbuddy/skills
mkdir -p .stdd/platforms/trae/skills
mkdir -p changes specs archive

# 2. 复制 STDD 核心文件到 .stdd/
cp /path/to/stdd-project/.stdd/config.yaml .stdd/
cp /path/to/stdd-project/.stdd/skills/*.md .stdd/skills/
cp /path/to/stdd-project/.stdd/templates/*.md .stdd/templates/
cp /path/to/stdd-project/.stdd/standards/*.md .stdd/standards/
cp /path/to/stdd-project/STDD.md .
cp /path/to/stdd-project/AGENTS.md .
```

### 方式三：安装到 AI 平台

```bash
# 安装到 Claude Code
python /path/to/stdd-project/bin/stdd install claude-code

# 安装到 WorkBuddy
python /path/to/stdd-project/bin/stdd install workbuddy

# 安装到 Trae
python /path/to/stdd-project/bin/stdd install trae

# 安装到 Cursor（作为项目规则）
python /path/to/stdd-project/bin/stdd install cursor
```

## 三、安装后验证

```bash
# 检查目录结构
ls -la .stdd/
ls -la .stdd/skills/
ls -la .stdd/templates/

# 验证 CLI
python /path/to/stdd-project/bin/stdd --help
python /path/to/stdd-project/bin/stdd status
```

## 四、使用流程

### 4.1 启动新变更

在 AI 编程平台中输入（以 Claude Code 为例）：

```
/stdd-understand 我们需要为 API 增加速率限制功能
```

系统将引导你完成 Phase 1（需求理解），生成 `proposal.md` 并等待确认。

### 4.2 六阶段流程

```
Phase 1: /stdd-understand  →  需求理解 → proposal.md → 用户确认
Phase 2: /stdd-spec        →  规格设计 → design.md + specs + test-plan.md → 用户确认
Phase 3-5: /stdd-continue  →  自动迭代：切片 → TDD实现 → 质量验证 → 用户确认
Phase 6: /stdd-continue    →  交付：归档 + 合并 specs + git tag
```

### 4.3 常用命令

| 命令 | 说明 |
|------|------|
| `/stdd-understand <需求>` | Phase 1: 启动需求理解 |
| `/stdd-spec` | Phase 2: 进入规格设计 |
| `/stdd-continue` | 继续执行（Phase 3-6） |
| `/stdd-status` | 查看当前变更状态 |

### 4.4 CLI 辅助命令

```bash
# 创建新 change
stdd new feature-rate-limit

# 查看变更状态
stdd status feature-rate-limit

# 验证变更结构
stdd validate feature-rate-limit

# 归档已完成变更
stdd archive feature-rate-limit

# 追溯 spec↔test↔code
stdd trace TC-RATE-001
```

## 五、目录结构

```
你的项目/
├── .stdd/                          # STDD 系统目录
│   ├── config.yaml                 # 项目配置
│   ├── skills/                     # 6 个阶段 Skill
│   ├── templates/                  # 8 个文档模板
│   ├── standards/                  # 开发规范
│   │   └── python.md               # Python 开发规范
│   └── platforms/                  # 多平台适配
│       ├── claude-code/skills/
│       ├── workbuddy/skills/
│       └── trae/skills/
├── changes/                        # 活跃变更
│   └── <YYYY-MM-DD>-<name>/
│       ├── .stdd.yaml              # 变更状态
│       ├── proposal.md
│       ├── design.md
│       ├── specs/
│       │   └── <capability>/spec.md
│       ├── test-plan.md
│       ├── tasks.md
│       ├── slices.md (可选)
│       ├── pending-adjustments.md
│       ├── design-adjustments.md
│       └── test-report.md
├── specs/                          # 主规范（合并后）
│   └── <capability>/spec.md
├── archive/                        # 已完成变更
├── STDD.md                         # 通用流程指引
└── AGENTS.md                       # 项目记忆文件
```

## 六、平台适配说明

### 6.1 Claude Code

Skills 安装到 `.claude/skills/`，通过 `/stdd-xxx` 斜杠命令调用。

```bash
python /path/to/stdd-project/bin/stdd install claude-code
```

### 6.2 WorkBuddy

Skills 安装到 `~/.workbuddy/skills/`，通过关键词匹配触发。每个 Skill 包含 YAML frontmatter 和 `trigger_keywords`。

```bash
python /path/to/stdd-project/bin/stdd install workbuddy
# 重启 WorkBuddy 或在对话框中输入 /reload stdd
```

### 6.3 Trae

Skills 安装到 `.trae/skills/`，通过 `/stdd-xxx` 调用。

```bash
python /path/to/stdd-project/bin/stdd install trae
```

### 6.4 Cursor / Windsurf / Copilot

这些平台没有 Skill 系统，STDD 作为项目规则安装：

```bash
# Cursor: 规则文件
python /path/to/stdd-project/bin/stdd install cursor

# Windsurf: 手动复制
cp .stdd/STDD.md .windsurfrules

# GitHub Copilot: 手动复制
cp .stdd/STDD.md .github/copilot-instructions.md
```

## 七、配置说明

`.stdd/config.yaml` 中的关键配置项：

```yaml
# 项目信息
project:
  name: my-project
  language: python          # 开发语言（影响规范加载）

# 强制确认门（不可关闭）
gates:
  phase1_understand:
    required: true          # Phase 1 必须用户确认
  phase2_spec:
    required: true          # Phase 2 必须用户确认
  phase5_verify:
    required: true          # Phase 5 必须用户确认

# 质量检查命令
quality:
  test: "pytest tests/ -v"
  lint: "ruff check app/ tests/"
  typecheck: null           # 暂不启用

# TC-ID 规则
tc_id:
  pattern: "TC-{CAPABILITY}-{NNN}"
```

## 八、开发规范的使用

Phase 4 (BUILD) 开始前，Skill 会自动读取 `.stdd/standards/<language>.md`。

当前支持的开发规范：
- `python.md` — Python 3.10+ 开发规范

后续计划：
- `java.md` — Java / Spring Boot
- `rust.md` — Rust / Cargo
- `go.md` — Go 标准布局

## 九、常见问题

### Q: 如何在已有项目中引入 STDD？

```bash
cd existing-project
python /path/to/stdd-project/bin/stdd init
```

### Q: 已有 OpenSpec 项目如何迁移？

将 `openspec/specs/` 复制到 `specs/`，将 `openspec/changes/` 中的活跃变更复制到 `changes/`。目录结构兼容。

### Q: 如何切换开发语言？

修改 `.stdd/config.yaml` 中的 `project.language`，然后创建对应的 `.stdd/standards/<language>.md`。

### Q: CLI 脚本报 Unicode 错误（Windows）？

设置环境变量：`set PYTHONIOENCODING=utf-8`，或使用 Windows Terminal（而非 cmd.exe）。
