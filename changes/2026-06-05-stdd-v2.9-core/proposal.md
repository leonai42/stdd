# STDD V2.9 核心引擎升级

<!-- STDD-MARKER: title — 变更标题，同时作为 change 目录名的基础 -->

## Why

<!-- STDD-MARKER: why — 问题陈述，用户视角 -->

V2.8 在 TStrategy 项目试用中暴露出三类问题：

1. **阻塞性 Bug**：`stdd experience list` 在新项目报错（`_save_index` 向不存在的目录写锁文件）；`canon verify` DC-HASH 验证失败（Human View 先生成导致 source_hash 缺失）
2. **版本升级断层**：STDD 源码升级到 V2.8 后，各项目内的 skills/config 仍是旧版本。没有 CLI 工具可以检查版本差异、执行升级、或批量管理多项目版本状态
3. **流程粒度单一**：V2.8 的 6 Phase 流程对微小变更（1-3 文件、<50 行）过于沉重。用户倾向于对小变更跳过 STDD，导致代码变更失控

## What Changes

<!-- STDD-MARKER: what_changes — 每项为一条变更描述，bullet list -->

**Bug 修复（P0）**：
- 修复 `stdd experience list` 新项目报错 — 空目录时优雅降级返回空列表
- 修复 `canon verify` DC-HASH 缺失 — 调整生成顺序（先 YAML → 再 Human View）

**版本升级系统（P1）**：
- 新增 `stdd upgrade` CLI 命令（check / upgrade / lock / unlock / --all）
- 新增 `.stdd/version.yaml` 项目版本文件
- 新增 `~/.stdd/projects.yaml` 全局注册表
- 新增 CLI 启动时版本检测（非阻塞提示）
- 重构 `init.py` 提取共享常量供 upgrade 复用

**轻量模式（P3）**：
- 新增复杂度评分模型（Phase 1 末尾 AI 自动计算，Gate 1 用户确认模式）
- 新增 `.stdd.yaml` 模式标记（lightweight / standard / thorough）
- Phase 2-6 按模式三档缩放（TDD 底线保留 — 轻量也写 RED→GREEN）
- 新增批次目录管理 `stdd batch` CLI + `changes/_batch/{period}-{date}/` 结构
- 新增非代码 task_type 支持（documentation / configuration / data-migration / dependency-upgrade）

## Capabilities

<!-- STDD-MARKER: capabilities -->

### New Capabilities

<!-- STDD-MARKER: new_capabilities — 格式: - **<名称>**：<描述> -->
- **version-upgrade**：`stdd upgrade` CLI — 检测版本差异、执行升级、版本锁定、跨项目批量管理
- **lightweight-mode**：复杂度评分 + 三档模式缩放 + Gate 1 模式确认
- **batch-management**：`stdd batch` CLI — 轻量变更批次创建/追加/闭合/归档

### Modified Capabilities

<!-- STDD-MARKER: modified_capabilities — 格式: - **<名称>**：<描述> -->
- **experience-list**：新项目空 experiences 目录时优雅降级，返回空列表
- **canon-verify**：先生成 Canonical YAML，再从 YAML 渲染 Human View，确保 source_hash 完整
- **project-init**：init.py 提取 DIRS / FILES_TO_COPY / PLATFORMS 为模块常量
- **change-state**：`.stdd.yaml` 增加 mode / task_type / complexity_score 字段

## Impact

<!-- STDD-MARKER: impact — 按层面分类的受影响文件/资源清单 -->

**代码层面**：
- 新建 2 个 CLI 命令模块：`stdd/cli/commands/upgrade.py` (~250 行)、`stdd/cli/commands/batch.py` (~150 行)
- 修改 5 个现有模块：`__init__.py`、`utils.py`、`init.py`、`experience.py`、`canon.py`、`new.py`
- 更新 6 个 Skill 源文件：`.stdd/skills/*.md`（增加轻量模式路径和缩放逻辑）

**配置层面**：
- 新增 `.stdd/config.d/lite.yaml`（轻量模式配置：评分阈值、批次策略）
- 新增 `~/.stdd/projects.yaml`（全局项目注册表）
- 新增 `.stdd/version.yaml`（项目级版本文件）

**基础设施**：
- 无需新服务或新 API
- 与现有 CLI 架构兼容（沿用 argparse + subparser 模式）

## Constraints

<!-- STDD-MARKER: constraints — 技术/资源/时间约束 -->
- **向后兼容**：无 `.stdd/version.yaml` 的旧项目回退读取 `project.yaml` 中的版本号
- **不阻塞执行**：启动版本检测仅打印提示，任何异常不中断命令
- **TDD 底线保留**：轻量模式不能跳过 RED→GREEN，差异在测试数量而非有无
- **Phase 1 不缩放**：模式决定在 Phase 1 结束时（Gate 1），因此 Phase 1 本身不使用缩放表

## Stakeholders

<!-- STDD-MARKER: stakeholders — 受影响方或相关角色 -->
- STDD 用户（开发者）— 受益于版本升级自动化和轻量模式
- STDD 项目维护者 — 受益于 init.py 常量化
- 团队管理者 — 受益于项目注册表和版本矩阵

## Risk Areas

<!-- STDD-MARKER: risk_areas — 格式: - capability: <name> — <风险描述> -->
- capability: version-upgrade — 升级过程中文件覆盖可能导致项目级配置被意外改写；缓解：project.yaml 合并策略（仅覆盖结构键，保留身份键）+ 备份机制
- capability: lightweight-mode — 复杂度评分可能误判（将中型变更评为 lightweight）；缓解：preliminary 标记 + Phase 2 可上调模式
- capability: batch-management — 批次目录命名冲突（同日闭合再新建）；缓解：日期 + 小时后缀防冲突

## NonGoals

<!-- STDD-MARKER: non_goals — 明确不在此变更范围内的事项 -->
- **不包含 Skill 层同步**（P2）：Canonical 步骤、Phase Context、Context Budget、rules 加载 — 这些属于 Change 2
- **不包含 CLI 改进**（P4）：canon init 默认目录调整、structure delta/merge — 这些属于 Change 2
- **不包含强制门**（P5）：`stdd guard` CLI、跨平台 hook 部署 — 远期目标
- **不修改 Git 提交策略或 CI/CD 配置**

## Critical

<!-- STDD-MARKER: critical — 是否关键变更 -->
- [x] 非关键变更（默认）
- [ ] 关键变更 — 涉及安全/金融/核心基础设施，需 L3/L4 锚定

## Risk Assessment

<!-- STDD-MARKER: risk_assessment — 风险分类评估 -->
- **safety_critical**：false（不涉及认证/授权/加密）
- **financial**：false（不涉及金融交易）
- **cross_system**：false（不涉及多系统协调，改动均在 STDD CLI 内部）

## Anchoring

<!-- STDD-MARKER: anchoring — 锚定策略 -->
- **level**：L1（行为锚定 — 基于已有的 CLI 命令模式和 Skill 定义修改）
- **reference_changes**：无
- **anchor_implementations**：无

## Success Criteria

<!-- STDD-MARKER: success_criteria — 可验证的完成条件 -->
- [ ] `stdd experience list` 在新项目（无 experiences 目录）返回空列表 `[]`，不报错
- [ ] `canon verify` 在规范生成后 DC-HASH 和 DC-FIELD 均通过
- [ ] `stdd upgrade --check` 能正确检测版本差异并显示（旧版项目 → 新版源）
- [ ] `stdd upgrade --dry-run` 展示完整升级计划，不修改文件系统
- [ ] `stdd upgrade` 完成升级后 `.stdd/version.yaml` 版本号更新，备份目录创建
- [ ] `stdd upgrade --lock` 锁定后启动不再提示版本更新
- [ ] `stdd upgrade --all --check` 显示全局注册表版本矩阵
- [ ] Phase 1 末尾 AI 能根据 proposal 计算复杂度评分并建议模式
- [ ] lightweight 模式：Phase 3 SLICE 跳过，Phase 4 BUILD 仅写 1-2 聚焦测试
- [ ] 两个轻量变更自动追加到同一批次目录 `changes/_batch/YYYY-MM-DD/`
- [ ] `stdd batch close` 手动闭合批次后，新变更创建新批次（目录名不冲突）
- [ ] standard 模式流程与 V2.8 行为一致（无退化）
