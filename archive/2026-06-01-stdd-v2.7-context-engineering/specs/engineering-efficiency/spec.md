# Spec: 工程效能优化（Engineering Efficiency）

> 对应板块 C（C1/C2/C3）| 3 个 New Capabilities
> token-optimization / agent-granularity / lifecycle-hooks

## ADDED Requirements

### Requirement: Token 优化策略体系 <!-- confidence: high -->

STDD SHALL 在每个阶段 skill 中注入模型分层建议，并在语言规范中增加文件大小约束。

**证据来源**：proposal.md `Capabilities > New > token-optimization`

#### Scenario: Phase 开始时输出模型建议 <!-- confidence: high -->

- **GIVEN** Phase 4 BUILD 即将开始
- **WHEN** AI 读取 build.md skill 的 Step -2
- **THEN** AI SHALL 输出当前阶段的推荐模型和备选模型
- **AND** 推荐 SHALL 包含理由（如"代码生成主力，需要准确性和速度平衡"）
- **AND** 备选 SHALL 包含降级条件（如"简单切片可降级到 Haiku"）

#### Scenario: 阶段间上下文重置提示 <!-- confidence: high -->

- **GIVEN** Phase N 已完成
- **WHEN** skill 末尾的"阶段完成后的上下文管理"段被渲染
- **THEN** AI SHALL 输出 `/clear` 建议和 `stdd state --resume` 命令
- **AND** 如果对话 > 80 轮 SHALL 标记为 "强烈建议"

#### Scenario: 文件大小约束指导 <!-- confidence: high -->

- **GIVEN** Phase 4 BUILD 中 AI 即将生成一个 Python 模块
- **WHEN** 预估代码行数 > 400 行
- **THEN** AI SHALL 提示："建议拆分为多个模块（当前预估 N 行，建议上限 300 行）"
- **AND** 拆分建议 SHALL 为可操作的具体方案

#### Scenario: 建议性不强制 <!-- confidence: high -->

- **GIVEN** 用户明确选择忽略模型建议（使用 Haiku 执行复杂 Phase 2）
- **WHEN** AI 在 Step -2 输出了推荐模型但用户不采纳
- **THEN** 流程 SHALL 继续进行，不阻断

---

### Requirement: Agent 颗粒度细化 <!-- confidence: high -->

STDD SHALL 新增 4 个专项 subagent 定义，并将 review 配置从 3 类扩展到 7 类。

**证据来源**：proposal.md `Capabilities > New > agent-granularity`

#### Scenario: 新增 subagent 定义可用 <!-- confidence: high -->

- **GIVEN** STDD V2.7 已安装
- **WHEN** AI 读取 AGENTS.md
- **THEN** 文件 SHALL 包含 4 个新 subagent 定义：security-reviewer / perf-analyzer / compat-checker / planner
- **AND** 每个定义 SHALL 包含 ID、推荐模型、工具列表、触发条件、职责清单

#### Scenario: review.agents 扩展为 7 类 <!-- confidence: high -->

- **GIVEN** `quality.yaml` 的 review.agents 需要扩展
- **WHEN** 用户查看默认配置
- **THEN** 配置 SHALL 包含 7 类 agent（原有 code/test_config/docs_skills + 新增 security/performance/compatibility/architecture）
- **AND** 新增 4 类 SHALL 默认 disabled（用户按需启用）

#### Scenario: Planner agent 独立化 <!-- confidence: medium -->

- **GIVEN** `quality.yaml` 中 `agents.planner.enabled == true`
- **WHEN** Phase 2 SPEC 开始
- **THEN** AI SHALL 切换为 spec-writer 角色，读取由 planner agent 产出的 design.md
- **AND** 如果 design.md 不存在 → 回退到 V2.5 行为（一个 Agent 完成全部 Phase 2）

---

### Requirement: Hooks 生命周期增强 <!-- confidence: high -->

STDD SHALL 提供 3 个 Claude Code 生命周期 hooks 和对应的 Python 脚本。

**证据来源**：proposal.md `Capabilities > New > lifecycle-hooks`

#### Scenario: SessionStart 自动加载状态 <!-- confidence: high -->

- **GIVEN** `.claude/settings.json` 已配置 session-start hook
- **WHEN** 新 Claude Code session 启动且当前目录为 STDD 项目
- **THEN** hook 脚本 SHALL 读取 `.stdd.yaml` 获取 active_phase
- **AND** 输出结构化恢复提示（change_name、当前阶段、最后动作、phase-context 路径）

#### Scenario: PreCompact 保存关键上下文 <!-- confidence: high -->

- **GIVEN** 上下文即将被压缩
- **WHEN** PreCompact hook 触发
- **THEN** hook 脚本 SHALL 确保 `.stdd.yaml` 和 `phase-context.md` 已更新至最新状态
- **AND** 输出 "状态已保存到文件系统" 的确认信息

#### Scenario: Stop hook 持久化经验 <!-- confidence: medium -->

- **GIVEN** session 正在结束且当前 phase 为 4 或 5
- **WHEN** Stop hook 触发
- **THEN** hook 脚本 SHALL 提示："建议运行 stdd experience curate 提取经验"
- **AND** 输出当前经验库统计摘要

#### Scenario: 非 Claude Code 平台降级 <!-- confidence: medium -->

- **GIVEN** 用户使用 Cursor / Copilot / Aider 等非 Claude Code 平台
- **WHEN** 平台不支持原生 hooks
- **THEN** skill 指令中 SHALL 包含等效的手动步骤提示
- **AND** 用户 SHALL 手动执行状态保存和恢复操作

#### Scenario: stdd hooks install CLI <!-- confidence: high -->

- **GIVEN** 项目为 Claude Code 平台
- **WHEN** 执行 `stdd hooks install`
- **THEN** 系统 SHALL 读取 `.claude/settings.json`（不存在则创建）
- **AND** 在 hooks 字段中注入 3 个 STDD hook 定义
- **AND** 将 Python hook 脚本复制到 `.stdd/hooks/` 目录
- **AND** 不覆盖用户已有的其他 hooks 配置
