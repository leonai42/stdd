# STDD 基础配套完善 — 多语言规范 + 平台扩展 + 配置补完 + Skill 标准化

## Why

STDD V2.2 在流程可靠性上已成熟（Gate review 透明化、长程模式权限落地、强制步骤清单），但基础配套存在 4 个系统性缺口：

1. **语言规范仅 Python**：无法支撑 Java/Go/Rust/TypeScript 项目的 STDD 流程
2. **平台同步严重滞后**：workbuddy/trae 停留在 V2.0（缺失 Step 0 并行评审、11 类失败检查 j/k、长程模式协议、强制步骤清单、Gate review 展示等 11 项 V2.2 特性）
3. **配置文件有空洞**：`typecheck: null`、`critical_paths: []` 导致 Phase 5 部分步骤被跳过
4. **Master Skill 不可加载**：`.stdd/skills/` 缺少 YAML frontmatter，无法作为独立 Skill 使用

同时扩充 Cursor、GitHub Copilot、Aider 三个主流 AI 编程平台的适配，扩大 STDD 的覆盖范围。

## What Changes

- 新增 Java / Go / Rust / TypeScript 四语言开发规范文件（参照 python.md 结构）
- workbuddy + trae 平台 12 个 skill 文件从 V2.0 全量同步到 V2.2
- 新增 Cursor + GitHub Copilot + Aider 三个平台的 STDD 适配文件
- 补完 `quality.yaml`（typecheck + critical_paths）、`project.yaml`（source_dir）、`long_range.yaml`（degradation 配置）
- `.stdd/skills/` 下 6 个 master 文件补齐 YAML frontmatter（name + description）

## Capabilities

### Modified Capabilities

- `platform-sync`：workbuddy/trae 平台 skill 从 V2.0 → V2.2 全量同步
- `config-system`：`quality.yaml` + `project.yaml` + `long_range.yaml` 补完缺失配置项
- `skill-architecture`：`.stdd/skills/` 6 文件增加 frontmatter，建立 master→platform 一致性标准

### New Capabilities

- `multi-lang-standards`：Java / Go / Rust / TypeScript 四语言开发规范文件
- `platform-cursor`：Cursor IDE `.cursor/rules/` 格式的 STDD 6 阶段规则
- `platform-copilot`：GitHub Copilot `.github/copilot-instructions.md` 格式的 STDD 指令
- `platform-aider`：Aider `CONVENTIONS.md` + `.aider.conf.yml` 格式的 STDD 适配

## Impact

**代码层面**：
- 新建 4 个语言规范文件（`.stdd/standards/{java,go,rust,typescript}.md`）
- 新建 3 个平台适配目录（cursor/copilot/aider，各含 1-3 个文件）
- 修改 12 个 workbuddy/trae 平台文件（6 skills × 2 platforms）
- 修改 6 个 master skill 文件（添加 frontmatter）
- 修改 3 个配置文件（`quality.yaml`, `project.yaml`, `long_range.yaml`）
- 预计：~10 个新建文件，~20 个修改文件

**配置层面**：
- `quality.yaml`：`typecheck` null → 命令字符串，`critical_paths` [] → 路径列表
- `project.yaml`：增加 `source_dir` 字段
- `long_range.yaml`：增加 `degradation` 配置段
- 均为增量添加，向后兼容

**基础设施**：
- 无新服务/API 需求

## Success Criteria

- [ ] `.stdd/standards/java.md` 存在，覆盖：代码风格、命名、类型、错误处理、测试、审查清单 6 维度
- [ ] `.stdd/standards/go.md` 存在，覆盖同上 6 维度
- [ ] `.stdd/standards/rust.md` 存在，覆盖同上 6 维度
- [ ] `.stdd/standards/typescript.md` 存在，覆盖同上 6 维度
- [ ] workbuddy 6 个 skill 文件与 claude-code 版本在 15 个关键特征上一致
- [ ] trae 6 个 skill 文件与 claude-code 版本在 15 个关键特征上一致
- [ ] `.stdd/platforms/cursor/` 存在且包含 STDD 规则文件
- [ ] `.stdd/platforms/copilot/` 存在且包含 `copilot-instructions.md`
- [ ] `.stdd/platforms/aider/` 存在且包含 `CONVENTIONS.md`
- [ ] `quality.yaml` 中 `typecheck` 非空，`critical_paths` 非空数组
- [ ] `project.yaml` 中 `source_dir` 已定义
- [ ] `.stdd/skills/` 下 6 个文件均含完整 YAML frontmatter（name + description）
- [ ] 所有新建/修改文件格式与 claude-code 版本一致
