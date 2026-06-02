# V2.7 切片执行计划

> 版本：V2.7（V2.6 合并）| 13 specs / 91 Scenarios / 39 TCs
> 切片策略：按板块高内聚拆分，板块间按依赖排序，板块内按数据模型→流程集成→CLI→测试顺序

## Dependency Graph Summary

```
Slice 1: 板块 E (结构化基础)
    │
    ├──→ Slice 2: 板块 A (锚定落地+双轨验证)
    │
    ├──→ Slice 3: 板块 B (上下文工程)     ←── 并行组 2
    ├──→ Slice 4: 板块 C (工程效能)       ←── 并行组 2
    ├──→ Slice 6: 板块 D (代码知识)       ←── 并行组 2
    │
    ├──→ Slice 5: 板块 C-extra (Skill扩展) ←── 并行组 3 (依赖 Slice 4)
    │
    └──→ Slice 7: 板块 D-extra (双语规则)  ←── 并行组 1 (零依赖，可随时执行)
```

**并行化说明**：
- **并行组 1**：Slice 7（双语规则）— 零依赖，可在任何时间执行
- **并行组 2**：Slice 3, 4, 6 — 均依赖 Slice 1，彼此无依赖，可并行
- **并行组 3**：Slice 2 — 依赖 Slice 1（数据模型定义），可和组2并行
- **并行组 4**：Slice 5 — 依赖 Slice 4（Skill 目录结构），需在 Slice 4 之后

## Slice Execution Plan

| # | 板块 | 优先级 | 风险 | 预估工时 | 并行组 | TC 覆盖 | 实现目标 |
|---|------|--------|------|---------|--------|---------|---------|
| 1 | E | P0 | 🟢 Low | M | — | CANON-001~005, DUAL-001~003 | canonical/ 目录 + proposal.yaml + agent_spec.yaml + project-index.yaml + canon init/generate CLI |
| 2 | A | P0 | 🟡 Med | L | 组3 | ANCH-001~004, CVER-001~002, AGNT-001~003 | 锚定评估 Phase 2 集成 + Gate 2 扩展 + 失败模式(l) + canon verify + agent verify |
| 3 | B | P0 | 🟢 Low | M | 组2 | CTXT-001~004, OPEN-001 | phase-context.md + resume_context 重设计 + 预算检查 + opencode 适配 |
| 4 | C | P1 | 🟢 Low | M | 组2 | EFFI-001~003 | Token 优化 + Agent 定义 + Hooks 脚本 + CLI |
| 5 | C+ | P1 | 🟢 Low | M | 组4 | SKIL-001~002 | Skill 目录重构 + 5 个新 Skill + skill create CLI |
| 6 | D | P1 | 🟡 Med | L | 组2 | CSUM-001~003, PROV-001~003, FRSH-001~002 | 代码结构摘要 + 经验 provenance + 状态新鲜度 |
| 7 | D+ | P1 | 🟢 Low | S | 组1 | BILI-001 | 10 条关键规则中英双语注入 |

## Rationale

### Slice 1: 板块 E — 结构化基础（P0 · 先行 · 不可并行）
- **依赖关系**：零前置依赖。它是所有其他板块的基础——没有 proposal.yaml 格式定义，锚定评估无法引用字段；没有 canonical/ 目录，双轨验证无处可查
- **风险分析**：🟢 低风险。纯数据模型定义 + CLI 骨架，不修改现有流程。向后兼容（可选启用）
- **工作量估算**：M（8 个 tasks，~800 行代码 + 200 行模板 + 8 个测试）

### Slice 2: 板块 A — 锚定落地 + 双轨验证（P0 · 依赖 Slice 1）
- **依赖关系**：依赖 Slice 1 的数据模型（proposal.yaml 的 critical/anchoring 字段、agent_spec.yaml 的 CP 格式）。可和 Slice 3/4/6 并行（彼此操作不同文件）
- **风险分析**：🟡 中风险。Phase 2 流程增强涉及 spec.md skill 修改（Step 2.4 新增），需确保非 critical Change 行为不变。Gate 2 阻断逻辑需测试
- **工作量估算**：L（9 个 tasks，~1200 行 CLI + ~400 行 skill 指令 + 9 个测试）

### Slice 3: 板块 B — 上下文工程（P0 · 依赖 Slice 1）
- **依赖关系**：弱依赖 Slice 1（.stdd.yaml 新字段）。与 Slice 4/6 可并行
- **风险分析**：🟢 低风险。phase-context.md 是新增文件，resume_context 重设计保留 V2.5 兼容。预算检查是软建议不阻断
- **工作量估算**：M（7 个 tasks，~600 行代码 + ~300 行 skill 指令 + 5 个测试）

### Slice 4: 板块 C — 工程效能优化（P1 · 依赖 Slice 1）
- **依赖关系**：弱依赖 Slice 1（模板目录结构）。与 Slice 3/6 可并行。Slice 5 依赖本切片
- **风险分析**：🟢 低风险。所有 agent 默认禁用，模型建议是软指导。Hooks 仅在 Claude Code 平台生效
- **工作量估算**：M（8 个 tasks，~500 行代码 + ~400 行 skill/Hook 指令 + 3 个测试）

### Slice 5: 板块 C+ — Skill 生态扩展（P1 · 依赖 Slice 4）
- **依赖关系**：依赖 Slice 4（Skill 目录结构需先建好）。可与 Slice 6/7 并行
- **风险分析**：🟢 低风险。新增 Skill 不影响现有流程，skill create 是独立 CLI
- **工作量估算**：M（8 个 tasks，~300 行 CLI + ~800 行 Skill 内容 + 2 个测试）

### Slice 6: 板块 D — 代码知识积累（P1 · 依赖 Slice 1）
- **依赖关系**：弱依赖 Slice 1（.stdd.yaml 新字段 + 模板目录）。与 Slice 3/4 可并行
- **风险分析**：🟡 中风险。code-structure-summary 是新增文件系统操作（DELIVER 时合并）。经验 provenance 涉及现有数据模型变更（需向后兼容）。state_freshness 需 git 操作
- **工作量估算**：L（12 个 tasks，~800 行 CLI + ~400 行 skill 指令 + 8 个测试）

### Slice 7: 板块 D+ — 关键规则双语注入（P1 · 零依赖）
- **依赖关系**：零依赖。纯文档注入，不涉及代码。可在任何时间执行
- **风险分析**：🟢 低风险。仅追加双语规则表到现有文件，不替换现有内容
- **工作量估算**：S（4 个 tasks，~200 行文档修改 + 1 个测试）
