---
name: stdd-upgrade
description: "STDD 技能层升级 — 同步项目 .stdd/ 快照与全局技能版本，无需 Python CLI"
stdd_version: "2.9.5"
---
# STDD Upgrade — 技能层版本同步

## 阶段目标

无需 Python CLI，通过 AI 对话将项目的 `.stdd/` 静态资源同步到与当前技能一致的最新版本。解决 GitHub Issue #5 报告的版本漂移问题。

## 前置条件

- 项目已初始化 STDD（存在 `.stdd/` 目录）
- 网络可访问 GitHub（`https://raw.githubusercontent.com/leonai42/stdd/master/`）

## 执行流程

### Step 1: 版本检查

1. 读取项目 `.stdd/version.yaml`
2. 显示当前项目版本和技能版本
3. 如果项目版本 >= 技能版本：提示"项目已是最新版本"，询问是否仍要强制同步
4. 如果项目版本 < 技能版本：确认升级

### Step 2: 平台检测

检查以下目录/文件的存在性，确定当前平台：

| 平台 | 检测标志 |
|------|---------|
| Claude Code | `.claude/skills/` 目录存在 |
| OpenCode | `.opencode/skills/` 目录存在 |
| Cursor | `.cursor/rules/stdd.md` 文件存在 |
| WorkBuddy | `.workbuddy/skills/` 目录存在 |
| Trae | `.trae/skills/` 目录存在 |

提示用户检测到的平台列表。

### Step 3: 备份当前版本

1. 创建备份目录：`.stdd/backup/<old_version>-<timestamp>/`
2. 复制当前 `.stdd/skills/`、`.stdd/templates/`、`.stdd/config.d/`、`.stdd/version.yaml` 到备份目录

### Step 4: 同步静态资源

从 GitHub raw 拉取最新文件并写入项目 `.stdd/`：

**技能文件**（拉取自 `.stdd/skills/`）：
- `understand.md`、`spec.md`、`slice.md`、`build.md`、`verify.md`、`deliver.md`
- `_shared/confirm-gate.md`、`_shared/version-check.md`、`_shared/mode-selection.md`、`_shared/long-range-auth.md`
- `upgrade.md`

**配置文件**（拉取自 `.stdd/config.d/`）：
- `gates.yaml`、`quality.yaml`、`long_range.yaml`、`lite.yaml`、`experience.yaml`
- `project.yaml`：**特殊处理** — 覆盖时保留 `project` 和 `paths` 字段的原有值

**模板文件**（拉取自 `.stdd/templates/` 和 `.stdd/templates/canonical/`）

**GitHub Raw URL 模式**：
```
https://raw.githubusercontent.com/leonai42/stdd/master/.stdd/skills/<filename>
https://raw.githubusercontent.com/leonai42/stdd/master/.stdd/config.d/<filename>
https://raw.githubusercontent.com/leonai42/stdd/master/.stdd/templates/<filename>
https://raw.githubusercontent.com/leonai42/stdd/master/.stdd/templates/canonical/<filename>
```

### Step 5: 更新版本标记

更新 `.stdd/version.yaml`：
```yaml
stdd_version: "<new_version>"
upgraded_at: "<current_iso_timestamp>"
```

### Step 6: 重装平台技能

对 Step 2 检测到的每个平台，重新生成技能文件：
1. 读取 `.stdd/skills/` 下最新的技能文件
2. 为每个技能生成对应平台的 SKILL.md（包含 name / description / stdd_version 的 YAML frontmatter）
3. 写入到目标平台目录

**Claude Code / OpenCode 重装**：
- `.claude/skills/stdd-<phase>/SKILL.md` 或 `.opencode/skills/stdd-<phase>/SKILL.md`
- 每个文件 = YAML frontmatter + `.stdd/skills/<phase>.md` 内容

**Cursor 重装**：
- 重装 `.cursor/rules/stdd.md`（如果存在 Cursor 适配器 `.stdd/platforms/cursor/`）

### Step 7: 输出升级摘要

```
✅ STDD 升级完成
  项目版本: <old_version> → <new_version>
  同步文件: <N> 个
  重装平台: <platform_list>
  备份位置: .stdd/backup/<old_version>-<timestamp>/
```

## 错误处理

| 场景 | 处理 |
|------|------|
| GitHub raw 不可达（超时/403） | 提示网络错误，提供手动下载 URL：`https://github.com/leonai42/stdd` |
| `.stdd/` 目录不存在 | 提示"当前项目未初始化 STDD，请先运行 stdd init" |
| 项目已锁定 | 提示"项目已锁定在版本 X.X.X，使用 stdd upgrade --unlock 解锁后再升级" |

## 产出物

- 更新后的 `.stdd/skills/`、`.stdd/templates/`、`.stdd/config.d/`
- `.stdd/version.yaml`（版本号和时间戳更新）
- `.stdd/backup/<old_version>-<timestamp>/`（升级前备份）
- 重装后的平台技能文件

## 质量检查

完成前确认：
- [ ] 所有拉取的文件成功写入
- [ ] `.stdd/version.yaml` 版本号正确更新
- [ ] 备份目录包含升级前的文件快照
- [ ] 平台技能文件 frontmatter 包含新版本号
