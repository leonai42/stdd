# STDD V2.8：质量度量升级 + 遗留补齐 + 覆盖率提升

> 状态：Phase 1 ✅ | Gate 1 已通过（2026-06-03）
> 基线：V2.7（184 tests / 70% coverage）
> 变更粒度：19 项（合理范围 < 20）

## Why

V2.7 完成了结构化基础、锚定+双轨制、上下文工程、工程效能优化。但存在三个缺口：

1. **质量度量维度单一**。V2.7 的验证是"通过/失败"二元判断，缺少统计质量度量（pass@k）、缺少自动修复能力（Plankton）、缺少大型 change 的并行启动支持（Two-Instance Kickoff）。

2. **V2.7 遗留骨架待补齐**。5 个 Skill 的 SKILL.md 内容未写、代码结构摘要系统 structure.py 5 个函数全是 TODO。

3. **测试覆盖率不均衡**。新模块测试覆盖差异大（hook 94% / skill 100%，但 state 48% / canon 60% / ci 74%），复盘 P1/P2 共 13 项待补。

## What Changes

**板块 A · V2.8 原规划（6 项）**：
- A1：pass@k 质量度量 — `stdd verify --pass-k 3`，Phase 5 支持 k 次重复验证，自动检测 Spec 歧义
- A2：Plankton 多级自动修复 — `stdd fix --level 1|2|3`，L1 静默/L2 建议/L3 报告
- A3：Two-Instance Kickoff — `stdd new <name> --parallel`，大型 change 双 Agent 并行
- A4：Rules 目录结构 — `.stdd/rules/common/` + `.stdd/rules/<lang>/`，build.md 自动加载
- A5：5 个 Skill 内容补齐 — python-patterns / fastapi-patterns / go-idioms / search-first / skill-create
- A6：代码结构摘要实现 — structure.py TODO→完整实现，`.stdd/code-structure/` 自动累积

**板块 B · 测试覆盖提升 P1（9 项）**：
- B1：state.py 覆盖率 48%→80%
- B2：canon.py 覆盖率 60%→80%
- B3：index.py 覆盖率 50%→75%
- B4：experience.py 覆盖率 72%→80%
- B5：ci.py 覆盖率 74%→82%
- B6：proposal.py 覆盖率 76%→85%
- B7：锚定评估 spec.md 集成测试
- B8：agent.py 覆盖率 35%→55%
- B9：trace.py 覆盖率 73%→85%

**板块 C · P2 改进（4 项）**：
- C1：并行切片合并验证步骤（build.md 指令）
- C2：设计偏离关联 TC 追踪（模板字段）
- C3：phase-context.md 自动生成逻辑
- C4：非代码 change 自动检测（project_type 检测）

## Capabilities

### New Capabilities

- **pass-k-verification**：pass@k 统计验证引擎 — k 次重复验证，可配置 k 值，输出 pass@k 报告，自动检测 Spec 歧义
- **plankton-auto-fix**：三级自动修复 — L1 静默(r ruff/isort) / L2 建议(类型/异常) / L3 报告(安全/性能)
- **two-instance-kickoff**：双 Agent 并行启动 — `stdd new --parallel`，Agent A 探索 + Agent B 调研
- **rules-directory**：`.stdd/rules/` 始终在线规则 — common/ + 5 语言，build.md 自动加载
- **skill-contents**：5 个标准 Skill 完整内容
- **code-structure-engine**：代码结构摘要引擎 — delta/merge/rebuild/show/graph 全实现

### Modified Capabilities

- **verify-phase**：Phase 5 增加 pass@k + Plankton L1 自动修复
- **build-phase**：Phase 4 Step 0.5 增加 rules 自动加载
- **new-command**：`stdd new` 增加 `--parallel` 选项
- **test-coverage**：10 个模块覆盖提升（目标 70%→78%+）

## Impact

**代码层面**：
- `stdd/cli/commands/` — 新增 fix.py；修改 verify.py + new.py + structure.py
- `.stdd/rules/` — 新增 common/ + python/ + go/ + java/ + rust/ + typescript/
- `.stdd/skills/languages/` — 3 个新 SKILL.md；`.stdd/skills/workflow/` — 2 个新 SKILL.md
- `.stdd/code-structure/` — 新增目录 + 实现逻辑
- 测试文件 — 新增 25-35 个测试

**配置层面**：
- `.stdd/config.d/quality.yaml` — 新增 pass_k + fix 配置段
- `.stdd/templates/` — 新增 rules 模板

**基础设施**：无新增外部依赖

## Constraints

- 增量改动，不破坏 V2.7 向后兼容
- pass@k 复用 pytest 重复运行
- Plankton L1 依赖 ruff/isort（已安装）
- Two-Instance Kickoff 仅 Claude Code 平台

## NonGoals

- 不做 pass@k CI 集成
- 不做 Plankton L3 自动修复（安全/架构需人工决策）
- Two-Instance 不做 3+ Agent 复杂编排
- 不做跨项目 rules 共享

## Critical

- [x] 非关键变更

## Risk Assessment

- **safety_critical**：false
- **financial**：false
- **cross_system**：false

## Anchoring

- **level**：L2（接口锚定 — CLI 命令有明确参数和输出格式）

## Success Criteria

- [ ] `stdd verify --pass-k 3` 可用，输出 pass@k 报告
- [ ] `stdd fix --level 1` 可用（ruff format + isort + 尾随空格）
- [ ] `stdd fix --level 2` 可用（类型注解/异常处理检测）
- [ ] `stdd new <name> --parallel` 可用
- [ ] `.stdd/rules/` 目录就位（common/+5 语言）
- [ ] 5 个 Skill 的 SKILL.md 完整内容就位
- [ ] `stdd structure *` 全部可用（无 TODO）
- [ ] 10 模块覆盖率达标（state 80% / canon 80% / index 75% / exp 80% / ci 82% / proposal 85% / agent 55% / trace 85%）
- [ ] 新增 25+ 测试用例
- [ ] 184 现有测试全部通过
