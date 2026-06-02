# V2.7 任务清单

> 版本：V2.7（V2.6 合并）
> 总计：25 项改动 / 5 个板块 / 7 个切片
> 长程模式：Phase 3-5 自动执行

## 1. Slice 1 — 板块 E：结构化基础（P0 · 先行）

- [ ] 1.1 创建 `canonical/` 目录结构 + `.canon-index.yaml` 格式定义
- [ ] 1.2 实现 proposal.yaml 格式（`stdd/templates/canonical/proposal.yaml`）+ `stdd proposal init/validate` CLI
- [ ] 1.3 实现 agent_spec.yaml 格式（`stdd/templates/canonical/agent_spec.yaml`）
- [ ] 1.4 实现 project-index.yaml 格式 + `stdd index update/show/trace` CLI
- [ ] 1.5 创建 `STDD_ANCHORING.md` 方法论文档（L1-L4 四级锚定体系）
- [ ] 1.6 实现 `stdd canon init/generate` CLI（双轨制基础）
- [ ] 1.7 更新 `.stdd/templates/` 新增 canonical/ + human-view/ 子目录及模板文件
- [ ] 1.8 编写 TC-CANON-001~005, TC-DUAL-001~003 测试

## 2. Slice 2 — 板块 A：锚定落地 + 双轨验证（P0 · 依赖 Slice 1）

- [ ] 2.1 实现锚定评估 Phase 2 集成（spec.md skill 新增 Step 2.4）
- [ ] 2.2 实现 Gate 2 锚定检查项（gates.yaml 扩展 + `stdd gate check --anchoring`）
- [ ] 2.3 实现第 12 类失败模式 (l) 锚定缺失（Phase 5 检查清单 + `stdd ci check-anchoring`）
- [ ] 2.4 实现 `canonical/specs/code/` 与 `canonical/specs/agent/` 分目录逻辑
- [ ] 2.5 实现 Agent 验证管线（`stdd agent verify` CLI + CP 执行器）
- [ ] 2.6 实现 `stdd canon verify` CLI（DC-HASH / DC-FIELD / DC-TIME / DC-TMPL 四项检查）
- [ ] 2.7 创建 `anchors/` 目录结构 + L2/L3/L4 锚定写入逻辑（spec.md skill）
- [ ] 2.8 经验库新增 agent_cp_failure / spec_ambiguity 类别
- [ ] 2.9 编写 TC-ANCH-001~004, TC-CVER-001~002, TC-AGNT-001~003 测试

## 3. Slice 3 — 板块 B：上下文工程（P0 · 依赖 Slice 1）

- [ ] 3.1 创建 phase-context.md 模板（`.stdd/templates/phase-context.md`）
- [ ] 3.2 更新 6 个阶段 skill 添加 phase-context 撰写/读取指令
- [ ] 3.3 重设计 `.stdd.yaml` resume_context + 新增 active_phase / phase_context_file 字段
- [ ] 3.4 更新 `stdd state` CLI 支持新字段（`--resume` 含 phase-context 摘要）
- [ ] 3.5 build.md / verify.md 增加 Step -1 上下文预算检查指令
- [ ] 3.6 实现 `stdd install opencode` CLI（`.opencode/skills/` 部署 + opencode.json 检测）
- [ ] 3.7 编写 TC-CTXT-001~004, TC-OPEN-001 测试

## 4. Slice 4 — 板块 C：工程效能优化（P1 · 依赖 Slice 1）

- [ ] 4.1 6 个阶段 skill 增加 Step -2 模型分层建议
- [ ] 4.2 6 个阶段 skill 末尾增加"阶段完成后的上下文管理"段
- [ ] 4.3 5 个语言规范增加文件大小约束章节
- [ ] 4.4 AGENTS.md 新增 4 个 subagent 定义（security-reviewer / perf-analyzer / compat-checker / planner）
- [ ] 4.5 quality.yaml review.agents 从 3→7 类 + 默认禁用逻辑
- [ ] 4.6 实现 3 个 Python hook 脚本（session-start / pre-compact / session-end）
- [ ] 4.7 实现 `stdd hooks install/status/uninstall` CLI
- [ ] 4.8 编写 TC-EFFI-001~003 测试

## 5. Slice 5 — 板块 C-extra：Skill 生态扩展（P1 · 依赖 Slice 4）

- [ ] 5.1 重构 `.stdd/skills/` 目录结构（平铺→core/languages/workflow/tools 四级分类）
- [ ] 5.2 创建 languages/python-patterns/SKILL.md
- [ ] 5.3 创建 languages/fastapi-patterns/SKILL.md
- [ ] 5.4 创建 languages/go-idioms/SKILL.md
- [ ] 5.5 创建 workflow/search-first/SKILL.md
- [ ] 5.6 创建 workflow/skill-create/SKILL.md
- [ ] 5.7 实现 `stdd skill create` CLI
- [ ] 5.8 编写 TC-SKIL-001~002 测试

## 6. Slice 6 — 板块 D：代码知识积累（P1 · 依赖 Slice 1）

- [ ] 6.1 创建 code-structure-delta.md 模板
- [ ] 6.2 更新 build.md skill 添加 Step N（生成代码结构增量）
- [ ] 6.3 更新 deliver.md skill 添加 delta→index 合并步骤
- [ ] 6.4 实现 `.stdd/code-structure/` 目录初始化 + index.md 累积逻辑
- [ ] 6.5 实现 `stdd structure delta/merge/rebuild/show/graph` CLI
- [ ] 6.6 更新 understand.md / spec.md skill 添加 Step -1（读取代码结构索引）
- [ ] 6.7 经验 YAML 新增 provenance + provenance_weight 字段
- [ ] 6.8 实现 provenance 权重体系 + 自动升级规则
- [ ] 6.9 更新 `stdd experience list/stats` 支持 provenance 过滤
- [ ] 6.10 `.stdd.yaml` 新增 state_freshness 字段块
- [ ] 6.11 实现 `stdd state --resume` 新鲜度检测（git HEAD 对比 + 陈旧警告）
- [ ] 6.12 编写 TC-CSUM-001~003, TC-PROV-001~003, TC-FRSH-001~002 测试

## 7. Slice 7 — 板块 D-extra：关键规则双语注入（P1 · 无依赖）

- [ ] 7.1 STDD.md 增加 "⚠️ 强制性约束 / MANDATORY CONSTRAINTS" 章节（10 条中英对照）
- [ ] 7.2 AGENTS.md 各 subagent 定义增加中英双语约束
- [ ] 7.3 6 个阶段 skill 的 "关键规则" 段增加中英双语强制性约束
- [ ] 7.4 编写 TC-BILI-001 测试

## 8. 集成与回归测试

- [ ] 8.1 全量 pytest 通过（155+ 现有 + 39 新增）
- [ ] 8.2 向后兼容验证（V2.5 格式文件可被 V2.7 正确读取）
- [ ] 8.3 `stdd state --resume` 端到端验证
- [ ] 8.4 `stdd canon init → generate → verify` 端到端验证
