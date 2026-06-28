# 技能层版本自检 + Skill-Only 升级路径

## Why

STDD 存在两层架构 —— 全局技能（流程引擎）和项目 `.stdd/`（静态资源）。当用户通过 AI 对话从 GitHub 升级全局技能后，项目的 `.stdd/` 快照不会自动同步，导致版本漂移（GitHub Issue #5 报告）。Python CLI 的 `stdd upgrade` 能解决此问题，但 skill-only 用户（OpenCode / 纯对话安装）无法触达 CLI 升级路径。

**现状**：
- V2.9 的 `try_version_check` 仅在 Python CLI 启动时运行
- 技能文件内部无版本标识，无法自检
- 没有任何 `/stdd-upgrade` 技能供 skill-only 用户使用

**动机**：确保所有平台的 STDD 用户（无论是否安装 Python CLI）都能感知版本漂移并完成升级。

## What Changes

| ID | 变更 | 类型 | 说明 |
|----|------|------|------|
| C1 | 技能 frontmatter 增加 `stdd_version` 字段 | modified | 6 个阶段技能 + `_shared/` 共享片段均嵌入版本号 |
| C2 | 新增 `_shared/version-check.md` | new | 版本自检共享片段，被所有阶段技能引用 |
| C3 | 所有阶段技能增加 Step 0 版本自检 | modified | understand/spec/slice/build/verify/deliver 启动时读取 `.stdd/version.yaml`，落后则提示 |
| C4 | 新增 `stdd-upgrade` 技能 | new | 纯对话式升级：从 GitHub 拉取最新 `.stdd/` 资源 → 同步到项目 → 重装平台技能 |
| C5 | `install.py` 注册 `stdd-upgrade` 技能 | modified | 将新技能纳入平台安装清单 |
| C6 | `SKILL_META` 增加 `upgrade` 条目 | modified | 安装框架识别新技能 |

## Capabilities

### New Capabilities

- **skill-version-self-check**：任何 STDD 技能启动时自动比对自身版本与项目 `.stdd/version.yaml`，版本落后于技能时主动告警并引导升级
- **skill-only-upgrade**：通过 `/stdd-upgrade` 命令，无需 Python CLI 即可从 GitHub 同步最新 `.stdd/` 资源和重装平台技能

### Modified Capabilities

- **platform-skill-install**：`stdd install` 安装技能时同步注入版本号到 frontmatter
- **skill-metadata**：SKILL_META 扩展支持 upgrade 技能

## Impact

**代码层面**：
- `.stdd/skills/_shared/version-check.md` — 新增（~30 行）
- `.stdd/skills/upgrade.md` — 新增（~120 行）
- `.stdd/skills/understand.md` — 修改（+15 行，增加版本自检步骤）
- `.stdd/skills/spec.md` — 修改（+15 行）
- `.stdd/skills/slice.md` — 修改（+15 行）
- `.stdd/skills/build.md` — 修改（+15 行）
- `.stdd/skills/verify.md` — 修改（+15 行）
- `.stdd/skills/deliver.md` — 修改（+15 行）
- `stdd/cli/commands/install.py` — 修改（+10 行，新增 upgrade 到 SKILL_META）

**配置层面**：
- `.stdd/version.yaml` — 结构不变，作为版本自检的比对基准

**基础设施**：
- 无新服务/新 API 依赖
- `stdd-upgrade` 技能通过 GitHub raw URL 获取文件（需网络访问）

## Constraints

- 版本自检不能阻断技能执行（告警即可，与 Python CLI 的 `try_version_check` 行为一致）
- `stdd-upgrade` 技能必须能在无 Python CLI 环境下独立运行
- 兼容 6 个平台：Claude Code / Cursor / Copilot / Aider / WorkBuddy / Trae / OpenCode
- 不改变现有 `.stdd/version.yaml` 结构

## Stakeholders

- OpenCode 平台用户（skill-only，无 Python CLI）
- 所有通过对话安装 STDD 的用户
- 现有 CLI 用户（受益于更早的版本漂移感知）

## Risk Areas

- capability: skill-version-self-check — 若版本号格式不一致（如 `v2.9` vs `2.9.4`），比对可能失败或误报。缓解：复用 `compare_versions` 逻辑，在技能指令中给出容错比较规则
- capability: skill-only-upgrade — GitHub API 限流或网络不可用导致升级失败。缓解：技能内包含重试指引和手动下载替代方案

## NonGoals

- 不在本次变更中实现内容 hash 校验（P2，后续迭代）
- 不修改 `stdd upgrade` CLI 核心逻辑
- 不改变现有 confirmation gate 机制
- 不实现自动后台升级（仅主动告警 + 手动触发）

## Critical

- [x] 非关键变更（默认）

## Risk Assessment

- **safety_critical**：false
- **financial**：false
- **cross_system**：false

## Anchoring

- **level**：L1（行为锚定 — 新增技能行为，无跨系统依赖）
- **reference_changes**：无
- **anchor_implementations**：无

## Success Criteria

- [ ] SC1：任意 STDD 阶段技能启动时，若 `.stdd/version.yaml` 中 `stdd_version` < 技能 frontmatter 中的 `stdd_version`，向用户展示明确告警
- [ ] SC2：版本一致或项目版本更新时不产生误报
- [ ] SC3：项目不存在 `.stdd/` 目录时静默跳过（非 STDD 项目不打扰）
- [ ] SC4：`/stdd-upgrade` 技能执行后，项目 `.stdd/` 的 skills/templates/configs/standards 与 GitHub 源一致
- [ ] SC5：`/stdd-upgrade` 执行后自动重装当前平台技能（Claude Code / OpenCode / Cursor 等）
- [ ] SC6：`stdd install` 安装技能时 frontmatter 正确携带 `stdd_version`
- [ ] SC7：`stdd upgrade` CLI 升级后同步更新已安装平台技能的 `stdd_version` 字段
