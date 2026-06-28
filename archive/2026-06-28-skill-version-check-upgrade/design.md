# 技能层版本自检 + Skill-Only 升级路径 - 技术设计

## Context

当前 STDD 有两层架构：
- **技能引擎层**：`~/.config/opencode/skills/stdd-*/SKILL.md`（或 `.claude/skills/stdd-*/SKILL.md`），负责流程控制
- **静态资源层**：项目 `.stdd/`（skills/templates/configs/standards/experiences），负责资源配置

Python CLI 的 `stdd upgrade` 可同步两层，但 skill-only 用户无 CLI 路径。GitHub Issue #5 报告了此问题：用户通过 AI 对话升级了全局技能到 v2.9.2，但项目 `.stdd/` 仍停留在 v2.4。需在技能文件内部实现：① 版本感知 ② 升级通路。

## Decisions

### 1. 版本号嵌入位置

**方案**：YAML frontmatter `stdd_version` 字段

**为什么**：现有技能已用 frontmatter 存储 `name`/`description`，保持一致性。AI 可通过 Read 工具直接读取 frontmatter 获取版本号，无需解析正文。

**备选方案及排除原因**：
- 备选 A：正文内嵌 `<!-- STDD_VERSION: 2.9.5 -->` 注释 → 排除，不同平台对 HTML 注释解析不统一
- 备选 B：单独 `version.txt` 文件 → 排除，增加文件数量，与 skill 文件分离易遗漏

### 2. 版本自检实现方式

**方案**：共享片段 `_shared/version-check.md`

**为什么**：6 个阶段技能各引用一次，版本号变化时只改一处。与现有 `_shared/confirm-gate.md` 模式一致，降低维护成本。

**备选方案及排除原因**：
- 备选 A：每个技能内联检查逻辑 → 排除，6 处冗余，更新版本号时易遗漏
- 备选 B：创建 main dispatcher skill 统一检查 → 排除，当前无统一入口，引入新耦合

### 3. 版本比较逻辑

**方案**：自然语言指令描述语义版本比较规则

**为什么**：指令中给定比较规则（去 `v`/`V` 前缀 → 按 `.` 分割 → 逐段转整数比较），AI 可在不执行代码的情况下完成比较。与 Python `compare_versions()` 逻辑等价。

**备选方案及排除原因**：
- 备选 A：要求 AI 执行 `python -c "..."` → 排除，skill-only 用户可能无 Python 环境
- 备选 B：引用 Python CLI 的 `compare_versions` → 排除，skill-only 用户无 CLI

### 4. 升级机制

**方案**：AI 驱动的 GitHub 拉取 + 本地写入

**为什么**：`/stdd-upgrade` 技能指导 AI 用 WebFetch 从 GitHub raw URL 拉取文件，用 Write 写入项目。完全不依赖 Python CLI。

**备选方案及排除原因**：
- 备选 A：要求用户先安装 Python CLI → 排除，正是要解决的问题
- 备选 B：npm/pip 包分发 → 排除，引入额外依赖管理

### 5. 平台检测

**方案**：检查平台目录存在性

**为什么**：与 `_detect_installed_platforms()` 逻辑一致：检查 `.claude/skills/`、`.opencode/skills/`、`.cursor/rules/stdd.md` 等目录/文件是否存在。简单可靠。

**备选方案及排除原因**：
- 备选 A：检查环境变量 → 排除，不同平台无统一环境变量约定

### 6. 入口策略

**方案**：各阶段技能独立自检，不引入统一 dispatcher

**为什么**：当前无统一 dispatcher skill，每个阶段 skill 独立被调用。在各 phase skill 的 Step 0 加入自检是最小改动方案，不引入新的路由耦合。

**备选方案及排除原因**：
- 备选 A：创建 `stdd/SKILL.md` 作为统一入口 → 排除，改变用户调用习惯，增加迁移成本

## Architecture

### 版本自检流程

```
用户调用 /stdd-spec
        ↓
AI 读取 .claude/skills/stdd-spec/SKILL.md
        ↓
Step 0: 读取 .stdd/skills/_shared/version-check.md
        ↓
  读取 .stdd/version.yaml → 提取 stdd_version
  从当前 skill frontmatter 提取 stdd_version
  比较: 项目版本 vs 技能版本
        ↓
  项目 < 技能 → ⚠️ 告警 + 提示 /stdd-upgrade → 继续执行
  项目 >= 技能 → 静默继续
  无 .stdd/ → 跳过（非 STDD 项目）
        ↓
Step 1-N: 正常阶段流程
```

### 升级链路

```
用户调用 /stdd-upgrade
        ↓
Step 1: 检测平台（检查 .claude/skills/ .opencode/skills/ 等）
Step 2: 备份当前 .stdd/ → .stdd/backup/<old_version>-<timestamp>/
Step 3: 从 GitHub raw 拉取最新 .stdd/skills/*.md + templates/ + configs/
Step 4: 写入项目 .stdd/（project.yaml 合并保留项目标识）
Step 5: 更新 .stdd/version.yaml（stdd_version + upgraded_at）
Step 6: 按平台重装技能文件（重新生成 SKILL.md 含新版本号）
Step 7: 输出升级摘要
```

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|----------|
| 版本号格式不一致导致误报 | 比较规则容错：去 v/V 前缀、支持两段/三段格式、非数字段忽略 |
| GitHub raw 网络不可用 | 升级技能提供 GitHub API 和 raw 两个源，失败时给出手动下载指引 |
| 技能文件版本号遗漏更新 | install.py 自动注入当前源版本号，减少手动维护面 |
| 升级过程中文件写入冲突 | 先备份当前 `.stdd/` 到 `.stdd/backup/`，再覆盖写入 |
