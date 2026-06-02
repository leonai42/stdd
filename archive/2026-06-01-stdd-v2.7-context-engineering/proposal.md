# STDD V2.7：结构化基础 + 锚定落地 + 双轨验证 + 上下文工程 + 工程效能优化

> 状态：Phase 1 ✅ | Phase 2 就绪 | Gate 1 已通过（2026-06-03）
> 版本基线：V2.5 → V2.7（V2.6 合并入 V2.7，不再单独发布）
> 关联：VISION.md 第十章 + ECC vs STDD 对比分析 + CodeGraph vs STDD 对比分析

## Why

V2.5 已完成 18 个 CLI 命令、155 个测试用例、5 语言规范、6 平台适配、经验库 5 态 FSM、社区经验池基础设施。但存在三层次缺口需要 V2.7 填补：

**基础层（原 V2.6 规划）**：proposal/spec 仍是纯 Markdown——人类可读但机器不可解析。锚定方法论只有概念定义，缺少格式支撑和工具集成。双轨制（Canonical YAML + Human View MD）只有概念，缺少目录结构、生成 CLI、一致性验证。

**能力层（原 V2.7 板块 A）**：锚定评估未集成到 Phase 2 Gate 检查中。双轨制缺少验证管线。Agent 行为验证只有格式定义，缺少执行引擎。

**效能层（ECC/CodeGraph 借鉴 · 2026-06-02 识别）**：上下文工程缺失（phase-context / 预算检查 / opencode 适配）。工程效能可优化（Token / Agent / Hooks / Skill）。代码知识无法跨 change 复用。经验库缺少可信度溯源。

**合并理由**：V2.6 的结构化格式是 V2.7 锚定+双轨制的前置依赖，分开做会导致 V2.6 做完后 V2.7 回头重改。板块 B/C/D 的详细设计已投入（详见已写入的 design.md），拆分浪费。25 项按 5 个板块独立切片，板块内高内聚、板块间依赖清晰。

## What Changes

**板块 E · 结构化基础（原 V2.6，5 项）**：
- E1：proposal.yaml Canonical 格式定义 + CLI 读写支持
- E2：agent_spec.yaml 格式定义（单系统 Agent 验证规格）
- E3：Spec 锚定法 L1 方法论文档 + spec 写作规范增强（skill 指令）
- E4：project-index.yaml 格式定义
- E5：双轨制文档基础：canonical/ 目录结构 + `stdd canon generate` CLI

**板块 A · 锚定落地 + 双轨验证（原 V2.7 板块 A，8 项）**：
- A1：锚定评估 Phase 2 集成（Step 2.4 自由度评估 + Gate 2 检查项）
- A2：第 12 类失败模式 (l) 锚定缺失
- A3：Canonical Source 目录标准化（canonical/ 顶层目录）
- A4：specs/code/ 与 specs/agent/ 分目录
- A5：单系统 Agent 验证管线（CP 检查点执行 + 断言验证）
- A6：`stdd canon verify` CLI（双轨一致性检查）
- A7：anchors/ 目录 + L2/L3/L4 锚定支持
- A8：经验库扩展：新增 agent_cp_failure / spec_ambiguity 经验类别

**板块 B · 上下文工程与平台扩展（4 项）**：
- B1：phase-context.md 阶段交接摘要机制
- B2：resume_context 重新定位（指针 vs 摘要分工）
- B3：上下文预算检查（build.md / verify.md 软检查）
- B4：`stdd install opencode` 平台适配器

**板块 C · ECC 借鉴（工程效能优化，4 项）**：
- C1：Token 优化策略体系（模型分层 + 阶段间重置 + 文件大小约束）
- C2：Agent 颗粒度细化（4 个新 subagent + review 配置 3→7 类）
- C3：Hooks 生命周期增强（3 个 hooks + `stdd hooks install` CLI）
- C4：Skill 生态扩展（5 个新 Skill + 目录重构 + `stdd skill create`）

**板块 D · CodeGraph 借鉴（代码知识积累，4 项）**：
- D1：代码结构摘要系统（BUILD → delta → DELIVER → index.md 自积累）
- D2：经验 provenance 字段（ci-detected / ai-inferred / human-reported / community-imported）
- D3：状态新鲜度校验（.stdd.yaml state_freshness + git HEAD 对比）
- D4：关键规则双语注入（10 条强制性约束中英对照）

## Capabilities

### New Capabilities

**数据模型层（板块 E）**：
- **canonical-proposal**：proposal.yaml 格式定义——结构化版本（YAML，AI 消费），包含 Why / What Changes / Capabilities / Constraints / Stakeholders / Risk Areas / NonGoals / Success Criteria / Anchoring / Risk Assessment
- **canonical-agent-spec**：agent_spec.yaml 格式定义——Agent 任务的行为规格（GIVEN 前置状态 / WHEN 操作序列 / THEN 检查点 + 断言）
- **canonical-project-index**：project-index.yaml 格式定义——项目级索引（changes 列表、specs 目录、capabilities 清单、模块映射）
- **dual-track-foundation**：双轨制基础——canonical/ 目录结构 + `stdd canon generate` CLI（Canonical YAML → Human View MD 单向生成，CLI 调用 AI 完成转换）
- **anchoring-methodology**：Spec 锚定法 L1 方法论文档 + spec 写作规范 skill 指令增强

**锚定与验证层（板块 A）**：
- **anchoring-phase2-integration**：锚定评估集成到 Phase 2 Step 2.4 + Gate 2 检查项（critical Change 锚定等级不足 → Gate 阻塞）
- **failure-mode-l**：第 12 类失败模式 (l) 锚定缺失——critical Change 未达最低锚定等级（< L3）
- **canonical-standardization**：Canonical Source 目录标准化（canonical/ 顶层目录 + specs/code/ 与 specs/agent/ 分目录）
- **agent-verification-pipeline**：单系统 Agent 验证管线——CP 检查点执行 + 断言验证（不依赖外部系统）
- **canon-verify-cli**：`stdd canon verify` CLI——双轨一致性检查（源哈希校验 + 字段完整性）
- **anchors-directory**：anchors/ 目录 + L2接口锚定 / L3模式锚定 / L4基准锚定 三级锚定支持
- **experience-new-categories**：经验库新增 agent_cp_failure（Agent CP 失败）/ spec_ambiguity（Spec 歧义）两个经验类别

**上下文工程层（板块 B）**：
- **phase-context**：阶段间结构化交接摘要——每 phase 结束时 AI 撰写对应章节，累积文件，新 session Agent 优先读取
- **context-budget-check**：build.md / verify.md Step 0 前上下文预算软检查——超阈值建议重置 session
- **opencode-platform-adapter**：`stdd install opencode` 命令——STDD skill 部署到 OpenCode 可识别路径（.opencode/skills/ + .claude/skills/ 双路径）

**工程效能层（板块 C）**：
- **token-optimization**：模型分层建议（Phase 1-2→Haiku/Sonnet / Phase 3-4→Sonnet / Phase 5→Opus/Sonnet）+ 阶段间上下文重置指导 + 各语言规范文件大小约束
- **agent-granularity**：4 个新 subagent（security-reviewer / perf-analyzer / compat-checker / planner）+ review 配置从 3 类扩展到 7 类
- **lifecycle-hooks**：3 个 Claude Code hooks（session-start 自动加载状态 / pre-compact 保存关键上下文 / stop 持久化经验）+ `stdd hooks install` CLI
- **skill-ecosystem**：5 个新 Skill（python-patterns / fastapi-patterns / go-idioms / search-first / skill-create）+ 目录结构从平铺重构为 core/languages/workflow/tools 四级分类

**代码知识层（板块 D）**：
- **code-structure-summary**：Phase 4 BUILD 后 AI 生成 code-structure-delta.md → Phase 6 DELIVER 合并到 .stdd/code-structure/index.md（自积累代码结构知识库）
- **experience-provenance**：经验 YAML 新增 provenance 字段（ci-detected=0.85 / ai-inferred=0.60 / human-reported=0.95 / community-imported=0.50）+ 自动升级规则
- **state-freshness**：.stdd.yaml 新增 state_freshness 字段块（verified_at / git_head / key_files_hash）+ `stdd state --resume` 自动对比 git HEAD
- **bilingual-rules**：10 条强制性约束中英双语重复注入 STDD.md / AGENTS.md / 各阶段 skill

### Modified Capabilities

- **proposal-format**：proposal 从纯 Markdown 扩展为双轨（proposal.yaml Canonical + proposal-brief.md Human View）——纯 Markdown 模式保持向后兼容
- **spec-format**：spec 从纯 Markdown 扩展为双轨（specs/code/*.yaml + spec-summary.md）——纯 Markdown 模式保持向后兼容
- **session-resume**：resume_context 从"一句话摘要"退为"指针 + phase_context_file 引用"，与 phase-context.md 分工协作
- **review-config**：quality.yaml review.agents 从 3 类扩展为 7 类（新增 security / performance / compatibility / architecture）
- **skill-directory**：.stdd/skills/ 从平铺 6 个 .md 文件扩展为 core/ + languages/ + workflow/ + tools/ 四级分类目录树
- **experience-model**：经验 YAML frontmatter 增加 provenance / provenance_weight / project_type 字段；.experience-index.yaml 增加按 provenance 过滤维度
- **stdd-state**：.stdd.yaml 增加 active_phase / phase_context_file / state_freshness 字段块
- **build-skill**：build.md 增加 token 优化建议 + 文件大小约束 + 代码结构 delta 生成步骤 + 经验按 project_type 过滤加载
- **verify-skill**：verify.md 增加上下文预算检查 + Plankton 风格分级修复（Level 1 静默修复：格式化/import排序）+ 非代码类 change 替代检查清单
- **language-standards**：5 个语言规范（python.md / java.md / go.md / rust.md / typescript.md）增加文件大小约束章节
- **gates-config**：gates.yaml Gate 2 检查项增加锚定评估（critical Change 锚定等级 < L3 → 阻塞）

## Impact

**代码层面**：
- `stdd/cli/commands/` — 新增 canon.py / hooks.py / structure.py；扩展 experience.py / state.py / proposal.py / ci.py
- `stdd/cli/` — 新增 canon / hooks / structure 子命令模块
- `.stdd/skills/` — 目录重构（core/ + languages/ + workflow/ + tools/），新增 5+ 个 Skill 的 SKILL.md + examples/
- `.stdd/templates/` — 新增 canonical/ 子目录（proposal.yaml / design.yaml / agent_spec.yaml / test-plan.yaml 等 11 个模板）+ human-view/ 子目录 + code-structure-delta.md 模板
- `.stdd/standards/` — 5 个语言规范各增加文件大小约束章节
- `.stdd/rules/` — 新增目录：common/（TDD规范/安全基线/Git工作流）+ <lang>/（语言特有规则）
- `.stdd/code-structure/` — 新增目录：index.md + .structure-index.yaml + deltas/
- `.stdd/hooks/` — 新增目录：session-start.py / pre-compact.py / session-end.py
- `AGENTS.md` — 新增 4 个 subagent 定义
- `STDD.md` — 新增 10 条关键规则中英双语段
- 测试文件 — 预估新增 40-60 个测试用例（canon / hooks / structure / provenance / freshness / 扩展的 experience）

**配置层面**：
- `.stdd/config.d/experience.yaml` — 新增 provenance.weights + 自动升级规则配置段
- `.stdd/config.d/quality.yaml` — review.agents 从 3→7 类；新增 token.model_tiering / token.file_size 配置段
- `.stdd/config.d/gates.yaml` — Gate 2 新增 anchoring.min_level 检查项
- `.stdd/config.d/project.yaml` — 新增 canonical.enabled / dual_track.enabled 配置段
- `.claude/settings.json` — 新增 3 个 hooks 配置（仅 Claude Code 平台）

**基础设施**：
- 无新增外部服务依赖
- 新增 Python 依赖：无（hooks 用 Python 实现复用 bin/stdd 现有生态，不引入 Node.js）
- canonical/ 目录为项目本地目录，无需服务器
- 社区经验池（GitHub + Gitee）已在 V2.5 配置，V2.7 无需改动

## Constraints

- **双轨制渐进**：V2.7 的 canonical/ 是过渡方案。`stdd canon generate` 通过 CLI 调用 AI 生成 Human View，非模板引擎自动渲染。V3.0 时升级为完整自动生成引擎
- **向后兼容**：所有现有 change 的纯 Markdown 格式继续可用。canonical/ 目录可选——不创建 canonical/ 的项目行为与 V2.5 完全一致
- **平台适配**：Hooks 仅 Claude Code 平台使用原生机制，其他 5 个平台降级为 skill 指令中的手动步骤
- **不引入新语言/框架依赖**：hooks 脚本用 Python 实现，不引入 Node.js。不改动 STDD 核心的 Python-only 约束
- **板块独立可交付**：5 个板块按依赖顺序独立切片、独立验证。板块 E→A 有强依赖（E 的格式定义为 A 的验证管线提供基础），板块 B/C/D 与 E/A 弱依赖可并行
- **Token 优化是建议性的**：模型分层建议不强制，用户可自行选择。文件大小约束是软约束
- **Agent 默认禁用**：新增 subagent 全部默认禁用，用户通过 quality.yaml 按需启用
- **代码结构摘要是辅助性产物**：AI 生成，置信度 0.70，与源代码不一致时以源代码为准
- **双语规则仅覆盖强制性约束**：约 10-15 条，不做全文档双语

## Stakeholders

- STDD 开源版用户（个人开发者 + 中小团队）
- 使用 OpenCode 平台的 STDD 用户
- 关注 AI 编程工程效能的开发者（Token 优化 / Agent 细化）
- ECC 社区（Skill 格式兼容 + search-first 方法论借鉴）
- CodeGraph 社区（代码知识图谱互补 + Trust Signal 借鉴）
- STDD for TEAM 未来用户（V2.7 的 canonical 基础是 TEAM 版前置依赖）

## Risk Areas

- capability: canonical-proposal — 双轨制增加文件数量，用户可能困惑"该看哪个"。缓解：Human View 头部声明"从 Canonical 生成，以 Canonical 为准"；纯 Markdown 模式保持可用
- capability: anchoring-phase2-integration — 锚定评估可能误判 spec 自由度。缓解：AI 评估 + Gate 2 人工确认双重机制；评估标注置信度
- capability: dual-track-foundation — Canonical 和 Human View 可能不同步。缓解：架构保障单向生成 + 源哈希校验（`stdd canon verify`）
- capability: phase-context — AI 撰写的摘要可能遗漏关键决策。缓解：章节末尾附"完整上下文文件清单"，Agent 可回溯原文
- capability: code-structure-summary — AI 生成的代码结构描述可能不准确。缓解：标注置信度 0.70 + 注明"以源代码为准" + 附带 git commit 便于溯源
- capability: agent-granularity — 过多 subagent 定义增加认知负担和配置复杂度。缓解：全部默认禁用，用户按需启用
- capability: skill-ecosystem — 示范 Skill 质量不足可能降低用户信心。缓解：前 3 个 Skill（python-patterns / fastapi-patterns / search-first）作为标杆精心编写
- capability: lifecycle-hooks — hooks 脚本需要 Python 环境，纯前端项目可能缺少。缓解：hooks 仅在 Claude Code 平台使用，其他平台降级为手动步骤
- capability: experience-provenance — 用户可能不理解不同 provenance 的权重差异。缓解：CLI 输出明确显示 provenance 标签和权重
- capability: state-freshness — git HEAD 快速变化时可能产生大量误报警告。缓解：仅在 `stdd state --resume` 时执行校验，不在每次工具调用时检查
- capability: bilingual-rules — 中英文规则版本可能随迭代产生偏差。缓解：双语规则写在相邻位置，更新时强制同步

## NonGoals

- 不做自动上下文压缩（Agent 运行时的事，STDD 是 skill 层）
- 不做 token 精确计数 CLI（需要模型 API 感知，超出 STDD 边界）
- 不做 MCP 服务器的 token 预算监控
- 不做 Agent 运行时调度框架（Claude Code / 平台的事）
- 不做跨平台通用 hooks 抽象层（V3.0 的事）
- 不做 Skill 市场/商店机制（V3.0 的事）
- 不做自动化 tree-sitter 代码解析（CodeGraph 的事，STDD 聚焦 AI 撰写的意图级摘要）
- 不做全文档多语言（V3.0 国际化的事）
- **V2.7 不做双轨制自动生成引擎**——`stdd canon generate` 通过 CLI 调用 AI 生成 Human View，非模板引擎自动渲染。V3.0 升级
- **V2.7 不做跨系统 Agent 验证**——那是 TEAM 版（V1.0）的事
- **不改变现有 6 阶段流程结构**——只增强各阶段的内部步骤，不改变 Phase 1→6 的宏观流程
- **不改变 3 道 Gate 的定位**——Gate 1/2/3 的确认时机和强制性不变

## Critical

- [x] 关键变更 — 涉及 STDD 核心架构（数据模型升级 + 目录结构变更 + 6 个阶段流程增强 + 6 个平台适配影响），需 L3/L4 锚定

## Risk Assessment

- **safety_critical**：false — 不涉及认证/授权/加密/数据保护
- **financial**：false — 不涉及金融交易或资金流转
- **cross_system**：true — 涉及 Claude Code / OpenCode / Cursor / Copilot / Aider / Trae 6 个平台的适配改动

## Anchoring

- **level**：L3（模式锚定——参照 V2.5 的 skill 架构模式、ECC 的 Skill 格式规范与 subagent 模式、CodeGraph 的 freshness 与 trust signal 模型）
- **reference_changes**：2026-05-21-stdd-v2.5, 2026-05-21-v2.4-experience-and-ai-enhance

## Success Criteria

- [ ] 25 项改动按 5 个板块独立切片、独立验证、独立交付
- [ ] canonical/ 目录结构可用，`stdd canon generate` 可基于 proposal.yaml 生成 proposal-brief.md
- [ ] agent_spec.yaml 格式定义完成，可用于单系统 Agent CP 验证
- [ ] 锚定评估集成到 Phase 2 Step 2.4，critical Change 的 Gate 2 可通过锚定检查
- [ ] 第 12 类失败模式 (l) 锚定缺失定义完成并集成到 Phase 5 检查清单
- [ ] phase-context.md 模板 + skill 指令完成，新 session Agent 读取后可在 1 轮内恢复完整上下文
- [ ] build.md / verify.md 包含上下文预算检查逻辑
- [ ] `stdd install opencode` 命令可用，OpenCode 能发现并触发 STDD skill
- [ ] code-structure-delta.md → .stdd/code-structure/index.md 自积累机制可用
- [ ] 经验 provenance 字段 + 权重体系 + 自动升级规则可用
- [ ] .stdd.yaml state_freshness 字段可用，`stdd state --resume` 输出新鲜度状态
- [ ] 6 个阶段 skill 均包含模型分层建议；5 个语言规范均包含文件大小约束
- [ ] 4 个新 subagent 定义完成；review.agents 扩展为 7 类
- [ ] `stdd hooks install` / `stdd skill create` / `stdd canon verify` 三个新 CLI 命令可用
- [ ] 5 个新 Skill（python-patterns / fastapi-patterns / go-idioms / search-first / skill-create）完成
- [ ] 10 条关键规则中英双语注入 STDD.md / AGENTS.md / 各阶段 skill
- [ ] 所有现有测试（155+）继续通过（向后兼容）
- [ ] 新增 40-60 个测试用例（覆盖新增 CLI 命令 + 数据模型 + hooks）
