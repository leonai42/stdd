# V2.7 测试方案与详细案例

> 版本：V2.7（V2.6 合并）
> 创建日期：2026-06-03
> 对应 Phase 2 Spec：13 个 spec 文件（见下方 TC 映射表）

## 一、测试策略

### 1.1 测试金字塔

```
E2E:         ~10  cases  ← agent verify / canon generate 端到端
集成测试:     ~30  cases  ← CLI 命令组合 / 文件系统操作 / YAML 解析
单元测试:     ~50  cases  ← 数据模型校验 / 字段解析 / 状态转换
```

### 1.2 测试原则

- 新增 CLI 命令每个命令至少 2 个用例（正常路径 + 异常路径）
- 数据模型变更必须有向后兼容测试（V2.5 格式文件可被 V2.7 正确读取）
- Hooks 脚本测试在隔离的临时目录中进行（不修改真实 `.claude/settings.json`）
- Spec 中每个 SHALL 声明的行为至少对应 1 个 TC

### 1.3 已有测试资产

| 测试文件 | 用例数 | 类型 | 覆盖范围 |
|----------|--------|------|----------|
| tests/commands/test_experience.py | 31 | 单元+集成 | 经验库 CRUD / 生命周期 / 社区池 |
| tests/commands/test_state.py | ~15 | 单元 | 状态读写 |
| tests/commands/test_validate.py | ~10 | 单元 | spec 校验 |
| tests/commands/test_ci.py | ~10 | 单元 | CI 检查 |
| 其他现有测试 | ~90 | 单元+集成 | CLI / CLI finder / utils |

## 二、详细测试案例

### 功能 1：Canonical 数据模型（E1/E2/E4）

对应 Spec：`canonical-data-model/spec.md`

#### 案例 1.1 — proposal.yaml 生成

| 字段 | 内容 |
|------|------|
| **ID** | TC-CANON-001 |
| **对应 Spec** | canonical-data-model → Scenario: 从 proposal.md 生成 proposal.yaml |
| **优先级** | P0 |
| **预置条件** | 存在经 Gate 1 确认的 proposal.md |
| **输入** | `stdd proposal init` |
| **预期结果** | `canonical/proposals/<id>.yaml` 生成，所有 STDD-MARKER 字段正确映射 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.2 — proposal.yaml 校验（缺失必填字段）

| 字段 | 内容 |
|------|------|
| **ID** | TC-CANON-002 |
| **对应 Spec** | canonical-data-model → Scenario: 校验 proposal.yaml 完整性 |
| **优先级** | P0 |
| **预置条件** | 存在缺少 `why.problem` 的 proposal.yaml |
| **输入** | `stdd proposal validate` |
| **预期结果** | 非零退出码 + 错误信息 "Missing required field: why.problem" |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.3 — agent_spec.yaml 格式校验

| 字段 | 内容 |
|------|------|
| **ID** | TC-CANON-003 |
| **对应 Spec** | canonical-data-model → Scenario: 定义单系统 Agent 验证规格 |
| **优先级** | P0 |
| **预置条件** | 创建包含 CP-1/CP-2 及断言的 agent_spec.yaml |
| **输入** | `stdd agent verify <task> --dry-run` |
| **预期结果** | 展示所有 CP 的 action 和预期断言，无错误 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.4 — project-index 生成与追溯

| 字段 | 内容 |
|------|------|
| **ID** | TC-CANON-004 |
| **对应 Spec** | canonical-data-model → Scenario: 扫描项目生成索引 |
| **优先级** | P0 |
| **预置条件** | 项目有 3 个 changes + 5 个 capabilities |
| **输入** | `stdd index update` |
| **预期结果** | project-index.yaml 包含 changes/capabilities/module_index 三个顶层字段 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.5 — 向后兼容：无 canonical 目录

| 字段 | 内容 |
|------|------|
| **ID** | TC-CANON-005 |
| **对应 Spec** | canonical-data-model → Scenario: 纯 Markdown 模式向后兼容 |
| **优先级** | P0 |
| **预置条件** | 项目未创建 canonical/ 目录 |
| **输入** | `stdd state` |
| **预期结果** | 正常输出状态，无错误（行为与 V2.5 一致） |
| **当前状态** | ❌ 测试缺 |

---

### 功能 2：双轨制基础（E5）

对应 Spec：`dual-track-foundation/spec.md`

#### 案例 2.1 — canon init 创建目录

| 字段 | 内容 |
|------|------|
| **ID** | TC-DUAL-001 |
| **对应 Spec** | dual-track-foundation → Scenario: 初始化 canonical 目录 |
| **优先级** | P0 |
| **预置条件** | 项目已安装 STDD V2.7，canonical/ 不存在 |
| **输入** | `stdd canon init` |
| **预期结果** | canonical/proposals/ / designs/ / specs/code/ / specs/agent/ 四个目录创建，.canon-index.yaml 生成 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.2 — canon generate 生成 Human View

| 字段 | 内容 |
|------|------|
| **ID** | TC-DUAL-002 |
| **对应 Spec** | dual-track-foundation → Scenario: 生成 Human View |
| **优先级** | P0 |
| **预置条件** | canonical/proposals/test.yaml 存在 |
| **输入** | `stdd canon generate test --type proposal` |
| **预期结果** | changes/test/proposal.md 生成，头部含 source_hash 和 generated_at |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.3 — Canonical 修改后过时检测

| 字段 | 内容 |
|------|------|
| **ID** | TC-DUAL-003 |
| **对应 Spec** | dual-track-foundation → Scenario: Canonical 修改后 Human View 过时检测 |
| **优先级** | P1 |
| **预置条件** | YAML 的 last_modified > MD 的 generated_at |
| **输入** | `stdd canon verify test` |
| **预期结果** | ⚠️ 警告信息，但非零退出码（DC-TIME 不阻断） |
| **当前状态** | ❌ 测试缺 |

---

### 功能 3：锚定体系（E3/A1/A2/A7）

对应 Spec：`anchoring-system/spec.md`

#### 案例 3.1 — critical Change 锚定评估

| 字段 | 内容 |
|------|------|
| **ID** | TC-ANCH-001 |
| **对应 Spec** | anchoring-system → Scenario: critical Change 触发锚定评估 |
| **优先级** | P0 |
| **预置条件** | proposal.critical=true, safety_critical=true |
| **输入** | Phase 2 Step 2.4 |
| **预期结果** | AI 执行自由度评估，输出评估结果（通过/需补充锚定） |
| **当前状态** | ❌ 测试缺（AI 行为测试，需模拟 Phase 2 流程） |

#### 案例 3.2 — Gate 2 锚定阻断（等级不足）

| 字段 | 内容 |
|------|------|
| **ID** | TC-ANCH-002 |
| **对应 Spec** | anchoring-system → Scenario: Gate 2 锚定阻断 |
| **优先级** | P0 |
| **预置条件** | critical=true, safety_critical=true（需L3），anchoring.level=L1 |
| **输入** | Gate 2 检查 |
| **预期结果** | 阻塞，提示 "锚定等级不足：当前 L1，最低要求 L3" |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.3 — 非 critical Change 跳过锚定

| 字段 | 内容 |
|------|------|
| **ID** | TC-ANCH-003 |
| **对应 Spec** | anchoring-system → Scenario: 非 critical Change 跳过锚定评估 |
| **优先级** | P1 |
| **预置条件** | proposal.critical=false, risk_assessment 全 false |
| **输入** | Phase 2 执行 |
| **预期结果** | Step 2.4 被跳过，直接进入 Gate 2 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.4 — 第 12 类失败模式检测

| 字段 | 内容 |
|------|------|
| **ID** | TC-ANCH-004 |
| **对应 Spec** | anchoring-system → Scenario: Phase 5 自动检测锚定缺失 |
| **优先级** | P1 |
| **预置条件** | critical Change 锚定等级不满足要求 |
| **输入** | `stdd ci check-anchoring <change-name>` |
| **预期结果** | 输出 "(l) 锚定缺失 — 当前等级 L{n}，要求 L{m}" |
| **当前状态** | ❌ 测试缺 |

---

### 功能 4：Canonical 标准化 + 验证（A3/A4/A6）

对应 Spec：`canon-standardization/spec.md`

#### 案例 4.1 — canon verify 源哈希一致

| 字段 | 内容 |
|------|------|
| **ID** | TC-CVER-001 |
| **对应 Spec** | canon-standardization → Scenario: 源哈希校验通过 |
| **优先级** | P0 |
| **预置条件** | YAML 未修改，MD 的 source_hash 匹配 |
| **输入** | `stdd canon verify test` |
| **预期结果** | "✅ DC-HASH 源哈希一致"，零退出码 |
| **当前状态** | ❌ 测试缺 |

#### 案例 4.2 — canon verify 字段引用错误

| 字段 | 内容 |
|------|------|
| **ID** | TC-CVER-002 |
| **对应 Spec** | canon-standardization → Scenario: 字段引用校验 |
| **优先级** | P0 |
| **预置条件** | MD 模板引用了 YAML 中不存在的字段 |
| **输入** | `stdd canon verify test` |
| **预期结果** | "❌ DC-FIELD 引用到不存在的字段: <path>"，非零退出码 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 5：Agent 验证管线（A5）

对应 Spec：`agent-verification/spec.md`

#### 案例 5.1 — agent verify 全部 CP 通过

| 字段 | 内容 |
|------|------|
| **ID** | TC-AGNT-001 |
| **对应 Spec** | agent-verification → Scenario: 执行全部检查点 |
| **优先级** | P0 |
| **预置条件** | agent_spec.yaml 定义 2 个 CP，所有断言可满足 |
| **输入** | `stdd agent verify <task>` |
| **预期结果** | CP-1 PASS, CP-2 PASS，零退出码，生成 agent-verification-report.md |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.2 — agent verify CP 失败记录

| 字段 | 内容 |
|------|------|
| **ID** | TC-AGNT-002 |
| **对应 Spec** | agent-verification → Scenario: CP 断言失败记录 |
| **优先级** | P0 |
| **预置条件** | CP-2 http_status 断言期望 200，实际 503 |
| **输入** | `stdd agent verify <task>` |
| **预期结果** | CP-1 PASS, CP-2 FAILED (expected 200, got 503)，非零退出码 |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.3 — agent verify dry-run

| 字段 | 内容 |
|------|------|
| **ID** | TC-AGNT-003 |
| **对应 Spec** | agent-verification → Scenario: 预览模式 |
| **优先级** | P1 |
| **预置条件** | agent_spec.yaml 就绪 |
| **输入** | `stdd agent verify <task> --dry-run` |
| **预期结果** | 展示所有 CP action 和预期断言，不实际执行 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 6：上下文工程（B1/B2/B3）

对应 Spec：`context-engineering/spec.md`

#### 案例 6.1 — phase-context.md 生成

| 字段 | 内容 |
|------|------|
| **ID** | TC-CTXT-001 |
| **对应 Spec** | context-engineering → Scenario: Phase 完成时 AI 撰写摘要 |
| **优先级** | P0 |
| **预置条件** | Phase 1 完成，Gate 1 确认 |
| **输入** | AI 检测到 phase 切换 (1→2) |
| **预期结果** | phase-context.md 中追加 "Phase 1: UNDERSTAND" 章节（含关键决策/产出物/文件清单） |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.2 — 新 session 恢复上下文

| 字段 | 内容 |
|------|------|
| **ID** | TC-CTXT-002 |
| **对应 Spec** | context-engineering → Scenario: 新 session Agent 恢复上下文 |
| **优先级** | P0 |
| **预置条件** | phase-context.md 含 Phase 1-4 所有章节 |
| **输入** | Agent 读取 `.stdd.yaml` → 发现 phase_context_file → 读取 phase-context.md |
| **预期结果** | Agent 在 1 轮 Read 内获取完整上下文 |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.3 — 上下文预算超阈值

| 字段 | 内容 |
|------|------|
| **ID** | TC-CTXT-003 |
| **对应 Spec** | context-engineering → Scenario: 超阈值建议重置 |
| **优先级** | P1 |
| **预置条件** | 对话 > 80 轮 |
| **输入** | Phase 4 Step -1 上下文预算检查 |
| **预期结果** | AI 输出重置建议 + `stdd state --resume` 输出 |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.4 — resume_context V2.5 格式向后兼容

| 字段 | 内容 |
|------|------|
| **ID** | TC-CTXT-004 |
| **对应 Spec** | context-engineering → Scenario: 旧格式向后兼容 |
| **优先级** | P1 |
| **预置条件** | `.stdd.yaml` 为 V2.5 格式（无 phase_context_file） |
| **输入** | V2.7 Agent 读取 |
| **预期结果** | 识别 phase_context_file=null，按旧逻辑从产物文件重建上下文 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 7：OpenCode 适配（B4）

对应 Spec：`platform-opencode/spec.md`

#### 案例 7.1 — stdd install opencode

| 字段 | 内容 |
|------|------|
| **ID** | TC-OPEN-001 |
| **对应 Spec** | platform-opencode → Scenario: 安装到项目目录 |
| **优先级** | P1 |
| **预置条件** | 项目已安装 STDD V2.7 |
| **输入** | `stdd install opencode` |
| **预期结果** | .opencode/skills/ 创建，6 个 SKILL.md 就位，opencode.json 未被修改 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 8：工程效能优化（C1/C2/C3）

对应 Spec：`engineering-efficiency/spec.md`

#### 案例 8.1 — 模型分层建议注入

| 字段 | 内容 |
|------|------|
| **ID** | TC-EFFI-001 |
| **对应 Spec** | engineering-efficiency → Scenario: Phase 开始时输出模型建议 |
| **优先级** | P1 |
| **预置条件** | Phase 4 BUILD 开始 |
| **输入** | AI 读取 build.md Step -2 |
| **预期结果** | AI 输出推荐模型（Sonnet）+ 备选（Haiku）+ 理由 |
| **当前状态** | ❌ 测试缺 |

#### 案例 8.2 — review.agents 7 类配置

| 字段 | 内容 |
|------|------|
| **ID** | TC-EFFI-002 |
| **对应 Spec** | engineering-efficiency → Scenario: review.agents 扩展为 7 类 |
| **优先级** | P1 |
| **预置条件** | STDD V2.7 quality.yaml |
| **输入** | 读取 review.agents 配置 |
| **预期结果** | 7 个 agent 定义（3 原有 enabled + 4 新增 disabled） |
| **当前状态** | ❌ 测试缺 |

#### 案例 8.3 — stdd hooks install

| 字段 | 内容 |
|------|------|
| **ID** | TC-EFFI-003 |
| **对应 Spec** | engineering-efficiency → Scenario: stdd hooks install CLI |
| **优先级** | P1 |
| **预置条件** | 项目存在 .claude/settings.json |
| **输入** | `stdd hooks install` |
| **预期结果** | settings.json 注入 3 个 hook 定义，.stdd/hooks/ 下 3 个 .py 脚本就位 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 9：Skill 生态（C4）

对应 Spec：`skill-ecosystem/spec.md`

#### 案例 9.1 — Skill 目录结构

| 字段 | 内容 |
|------|------|
| **ID** | TC-SKIL-001 |
| **对应 Spec** | skill-ecosystem → Scenario: 目录结构升级 |
| **优先级** | P1 |
| **预置条件** | STDD V2.7 已安装 |
| **输入** | 检查 .stdd/skills/ 目录 |
| **预期结果** | core/ / languages/ / workflow/ / tools/ 四个子目录存在 |
| **当前状态** | ❌ 测试缺 |

#### 案例 9.2 — stdd skill create

| 字段 | 内容 |
|------|------|
| **ID** | TC-SKIL-002 |
| **对应 Spec** | skill-ecosystem → Scenario: skill-create 引导创建新 Skill |
| **优先级** | P1 |
| **预置条件** | STDD V2.7 |
| **输入** | `stdd skill create test-skill --type language` |
| **预期结果** | languages/test-skill/SKILL.md 生成，YAML frontmatter 正确 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 10：代码结构摘要（D1）

对应 Spec：`code-structure-summary/spec.md`

#### 案例 10.1 — delta 生成

| 字段 | 内容 |
|------|------|
| **ID** | TC-CSUM-001 |
| **对应 Spec** | code-structure-summary → Scenario: 生成 delta 文件 |
| **优先级** | P0 |
| **预置条件** | Phase 4 BUILD 完成，有新增模块 |
| **输入** | AI 执行 build.md Step N |
| **预期结果** | code-structure-delta.md 生成，含置信度 0.70 标注 |
| **当前状态** | ❌ 测试缺 |

#### 案例 10.2 — DELIVER 合并到索引

| 字段 | 内容 |
|------|------|
| **ID** | TC-CSUM-002 |
| **对应 Spec** | code-structure-summary → Scenario: 合并 delta 到索引 |
| **优先级** | P0 |
| **预置条件** | delta 已生成，.stdd/code-structure/ 不存在（首次） |
| **输入** | `stdd deliver` |
| **预期结果** | .stdd/code-structure/ 创建，index.md + .structure-index.yaml 包含 delta 内容 |
| **当前状态** | ❌ 测试缺 |

#### 案例 10.3 — 索引过时警告

| 字段 | 内容 |
|------|------|
| **ID** | TC-CSUM-003 |
| **对应 Spec** | code-structure-summary → Scenario: 索引过时时输出警告 |
| **优先级** | P1 |
| **预置条件** | index.md last_updated > 7 天 |
| **输入** | Phase 1 读取 index.md |
| **预期结果** | ⚠️ 警告 "代码结构索引可能过时，建议重建" |
| **当前状态** | ❌ 测试缺 |

---

### 功能 11：经验溯源（D2/A8）

对应 Spec：`experience-provenance/spec.md`

#### 案例 11.1 — 新经验自动标记 provenance

| 字段 | 内容 |
|------|------|
| **ID** | TC-PROV-001 |
| **对应 Spec** | experience-provenance → Scenario: 新经验自动标记 provenance |
| **优先级** | P0 |
| **预置条件** | Phase 5 CI 自动检测到失败模式 |
| **输入** | AI 创建经验 |
| **预期结果** | YAML 含 provenance=ci-detected, provenance_weight=0.85 |
| **当前状态** | ❌ 测试缺 |

#### 案例 11.2 — 按 provenance 过滤

| 字段 | 内容 |
|------|------|
| **ID** | TC-PROV-002 |
| **对应 Spec** | experience-provenance → Scenario: 按 provenance 过滤 |
| **优先级** | P0 |
| **预置条件** | 经验库含 3 条 ci-detected + 5 条 ai-inferred |
| **输入** | `stdd experience list --provenance ci-detected` |
| **预期结果** | 仅列出 3 条 ci-detected |
| **当前状态** | ❌ 测试缺 |

#### 案例 11.3 — 旧经验向后兼容

| 字段 | 内容 |
|------|------|
| **ID** | TC-PROV-003 |
| **对应 Spec** | experience-provenance → Scenario: 旧经验向后兼容 |
| **优先级** | P0 |
| **预置条件** | V2.5 经验条目无 provenance 字段 |
| **输入** | `stdd experience list --format json` |
| **预期结果** | provenance 默认显示 ai-inferred（0.60），原始文件未被修改 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 12：状态新鲜度（D3）

对应 Spec：`state-freshness/spec.md`

#### 案例 12.1 — FRESH 状态显示

| 字段 | 内容 |
|------|------|
| **ID** | TC-FRSH-001 |
| **对应 Spec** | state-freshness → Scenario: 状态新鲜度显示 |
| **优先级** | P1 |
| **预置条件** | state_freshness.verified_at 为 2 小时前 |
| **输入** | `stdd state --resume` |
| **预期结果** | 输出含 "🟢 FRESH — 最近更新于 2 小时前" |
| **当前状态** | ❌ 测试缺 |

#### 案例 12.2 — STALE 警告

| 字段 | 内容 |
|------|------|
| **ID** | TC-FRSH-002 |
| **对应 Spec** | state-freshness → Scenario: Git HEAD 变更时输出警告 |
| **优先级** | P1 |
| **预置条件** | git_head != 当前 HEAD（+2 commits） |
| **输入** | `stdd state --resume` |
| **预期结果** | "🟡 STALE — Git HEAD 已变更（+2 commits）" |
| **当前状态** | ❌ 测试缺 |

---

### 功能 13：双语规则（D4）

对应 Spec：`bilingual-rules/spec.md`

#### 案例 13.1 — STDD.md 双语规则表

| 字段 | 内容 |
|------|------|
| **ID** | TC-BILI-001 |
| **对应 Spec** | bilingual-rules → Scenario: STDD.md 中的双语规则表 |
| **优先级** | P1 |
| **预置条件** | STDD V2.7 STDD.md |
| **输入** | 读取 STDD.md |
| **预期结果** | "⚠️ 强制性约束 / MANDATORY CONSTRAINTS" 章节存在，10 条中英对照规则 |
| **当前状态** | ❌ 测试缺 |

---

## 三、测试执行矩阵

| 功能模块 | 单元测试 | 集成测试 | 状态 |
|----------|:---:|:---:|:---:|
| Canonical 数据模型 | TC-CANON-001~005 | — | 🔴 |
| 双轨制基础 | TC-DUAL-001~003 | — | 🔴 |
| 锚定体系 | TC-ANCH-004 (CLI) | TC-ANCH-001~003 (流程) | 🔴 |
| Canonical 验证 | TC-CVER-001~002 | — | 🔴 |
| Agent 验证管线 | TC-AGNT-003 (dry-run) | TC-AGNT-001~002 | 🔴 |
| 上下文工程 | TC-CTXT-004 (兼容) | TC-CTXT-001~003 (流程) | 🔴 |
| OpenCode 适配 | TC-OPEN-001 | — | 🔴 |
| 工程效能 | TC-EFFI-002~003 (配置) | TC-EFFI-001 (流程) | 🔴 |
| Skill 生态 | TC-SKIL-001~002 | — | 🔴 |
| 代码结构摘要 | TC-CSUM-001~003 | — | 🔴 |
| 经验溯源 | TC-PROV-001~003 | TC-PROV-001 (集成) | 🔴 |
| 状态新鲜度 | TC-FRSH-001~002 | — | 🔴 |
| 双语规则 | TC-BILI-001 | — | 🔴 |

## 四、回归风险矩阵

| 风险区域 | V2.7 改动 | 已有回归保护 | 风险等级 |
|----------|----------|:---:|:---:|
| 经验库数据结构 | 新增 provenance/provenance_weight 字段 | ✅ 31 个测试 | 🟢 低 |
| .stdd.yaml 格式 | 新增 active_phase/state_freshness 字段 | ✅ state 测试 | 🟢 低 |
| Skill 目录结构 | 平铺→分类树重构 | ❌ 无 | 🟡 中 |
| quality.yaml | review.agents 3→7 类 | ✅ 配置测试 | 🟢 低 |
| STDD.md / AGENTS.md | 新增双语规则段 | ❌ 无 | 🟢 低 |
| build.md / verify.md | 新增 token 建议/预算检查/结构摘要步骤 | ❌ 无 | 🟡 中 |
| canonical/ 目录 | 新增可选目录 | ❌ 无 | 🟢 低（可选） |
| Phase 2 流程 | 新增 Step 2.4 锚定评估（条件触发） | ❌ 无 | 🟡 中 |
| Gate 2 检查 | 新增锚定阻断项 | ❌ 无 | 🟡 中 |

## 五、建议补充顺序

| 优先级 | TC 范围 | 预估数量 | 理由 |
|:---:|------|:---:|------|
| **P0** | TC-CANON-001~005, TC-DUAL-001~002, TC-CVER-001~002, TC-AGNT-001~002, TC-CTXT-001~002, TC-CSUM-001~002, TC-PROV-001~003, TC-ANCH-001~002 | ~21 | 核心新功能，缺失则无法验证 V2.7 主体 |
| **P1** | TC-DUAL-003, TC-ANCH-003~004, TC-AGNT-003, TC-CTXT-003~004, TC-OPEN-001, TC-EFFI-001~003, TC-SKIL-001~002, TC-CSUM-003, TC-FRSH-001~002, TC-BILI-001 | ~18 | 辅助功能/边界条件/兼容性 |
| **P2** | 性能测试 / 大规模项目测试 / 6 平台兼容性测试 | ~10 | 非功能性验证 |
| **合计** | 49 个 TC | | 其中 ~39 个需新写，~10 个可复用现有测试 |
