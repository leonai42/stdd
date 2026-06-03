---
name: stdd-spec
description: "STDD Phase 2: 规格设计 — 将 proposal 转化为可测试的 spec Scenario"
---
---
name: stdd-spec
description: "STDD Phase 2: 规格设计与测试方案 — 将 proposal 转化为精确的技术规格和可执行测试方案"
---
# STDD Phase 2: SPEC — 规格设计与测试方案

## 阶段目标

将 proposal 转化为精确的技术规格和测试方案。**这是整个 STDD 流程中最重要的阶段。**

## 前置条件

- Phase 1 已完成（proposal.md 经用户确认）
- `.stdd.yaml` 中 `phases.understand.status == "completed"`

## 执行流程

### Step 1: 读取 Phase 1 产出 + CLI 结构化提取

1. 读取 `proposal.md`，理解变更范围和边界
2. **执行 CLI 结构化提取**：`python bin/stdd extract-proposal --format json`
   - 获取：`title`, `capabilities` (new + modified), `what_changes`, `success_criteria`, `impact`
   - 后续步骤直接引用提取的结构化数据，不再从 proposal 原文模糊解析
3. 从输出中识别涉及的 Capabilities 列表和 Impact 范围

### Step 2: 加载匹配经验 + 交叉检查

在生成 specs 之前，从经验库加载可能相关的失败模式，用于交叉检查生成的 spec：

1. 执行 `python bin/stdd experience list --language <project.language> --format json`
2. 从输出中筛选与当前 Capabilities 相关的经验（pattern/root_cause 中包含相似关键词）
3. 对匹配的经验，提取 `detection_trigger` 和 `fix_template`，在生成 Scenario 时用作检查清单：
   - 如经验提示"(d) 上下文丢失"→ 确保每个 Scenario 的 GIVEN 与 proposal 明确对应
   - 如经验提示"(k) 契约断层"→ 确保跨 Capability 的接口字段名一致

### Step 3: 生成技术设计（design.md）

先读取模板：`.stdd/templates/design.md`

按模板生成 design.md：
- **Context**：当前技术背景和约束
- **Decisions**：每个技术决策包含：
  - 方案描述
  - 为什么选这个方案
  - 备选方案及排除原因
- **Architecture**：数据流/组件图/调用链
- **Risks / Trade-offs**：风险表和缓解措施

### Step 4: 生成行为规格草稿（specs/*.md）

先读取模板：`.stdd/templates/spec-draft.md`

为每个 Capability 生成一个 spec 草稿文件（`specs/<capability>/spec.md`）：

**自动生成流程**（AI 主导，用户角色从"写 spec"变为"审 spec"）：

1. 从 Step 1 的 `extract-proposal` 输出中提取 capability 名称和描述
2. 按 `spec-draft.md` 模板为每个 capability 生成 spec 草稿
3. **每个 Requirement 和 Scenario 标注置信度标签**：
   - `<!-- confidence: high -->` — 所有 GIVEN/WHEN/THEN 要素可从 proposal 中直接找到
   - `<!-- confidence: medium -->` — 部分要素需从上下文推断
   - `<!-- confidence: low -->` — 几乎完全由 AI 推断，proposal 只提供了能力名称
4. 为每个 Scenario 标注"证据来源"：引用 proposal.md 中支撑此 Scenario 的具体段落
5. 格式规则（不变）：
   - 每个 Requirement 至少 1 个 Scenario
   - 严格使用 GIVEN/WHEN/THEN/AND 格式
   - THEN 中必须包含 SHALL（大写），表示强制行为
   - GIVEN/WHEN/THEN 各一条，AND 可有多条（最多 5 条）

**置信度原则**：
- 高置信度的 Scenario 用户可快速确认
- 低置信度的 Scenario 必须用户详细审核（AI 可能理解有误）

### Step 4.5: 锚定评估（V2.7 anchoring — 条件触发）

**执行条件**：proposal 的 Critical 勾选了"关键变更"或 risk_assessment 中有任意 true。

1. **AI 评估 spec 的自由度**：
   - 是否有 SHALL 未覆盖的行为路径？
   - 是否有"合理但不同"的多种实现可能？
   - 关键决策点是否被锁定？

2. **计算最低锚定等级需求**：
   - safety_critical=true → 至少 L3
   - financial=true → 至少 L4
   - cross_system=true → 至少 L2
   - 默认 critical → 至少 L3

3. **判断**：
   - proposal.anchoring.level ≥ 最低需求 → 通过
   - proposal.anchoring.level < 最低需求 → Gate 2 阻塞
   - 非 critical → 跳过此步骤

4. **输出**：
   - 自由评估结果 + 锚定等级判定
   - 如果阻塞：明确提示用户需补充锚定（升级等级或补充参考实现）

### Step 5: 生成测试方案（test-plan.md）

先读取模板：`.stdd/templates/test-plan.md`

从 specs 映射生成 test-plan.md：

**Spec → Test 映射规则**：
```
spec Scenario            test-plan TC Case
─────────────────────────────────────────
GIVEN: <前置条件>    →   预置条件（Arrange）
WHEN: <触发动作>     →   输入（Act）
THEN: <预期结果>     →   预期结果（Assert）
AND: <附加结果>      →   额外的 Assert
```

**TC-ID 命名规则**：`TC-<CAPABILITY>-<NNN>`
- CAPABILITY 取 capability 名的缩写（如 CASUAL, INTENT, CSM, KM, SOURCE）
- NNN 从 001 递增

**必须包括的章节**：
1. 测试策略（金字塔 + 原则 + 已有资产）
2. 详细测试案例（每个 spec Scenario 至少 1 个 TC）
3. 测试执行矩阵（功能 × 测试层次）
4. 回归风险矩阵（改动区域风险评估）
5. 建议补充顺序（P0 → P1 → P2）

### Step 5.5: 设计审查（自动化文档 Review）

在提交用户确认之前，自动审查 design.md 和 specs 的质量：

1. **需求覆盖检查**：
   - design.md 是否覆盖了 proposal.md 中所有 What Changes？
   - 每个 Capability 是否有对应的 spec 文件？
   - 是否有遗漏的技术决策？

2. **Scenario 完备性检查**：
   - 每个 Requirement 是否至少 1 个 Scenario？
   - 每个 Scenario 是否严格使用 GIVEN/WHEN/THEN/AND 格式？
   - THEN 中是否包含 SHALL（大写）表示强制行为？
   - AND 数量是否在限制内（≤5）？

3. **TC-ID 一致性检查**：
   - test-plan.md 的 TC-ID 是否全局唯一？
   - TC 案例数是否 ≥ Scenario 数？
   - 每个 Scenario 是否至少有 1 个 TC 案例？

4. **文档一致性检查**：
   - design.md 中引用的文件路径是否有效？
   - specs 中的技术术语与 design.md 是否一致？
   - 版本号引用是否正确？

审查发现问题后**自动修复**，然后进入 Step 6 用户确认。

---

### Step 6: 用户确认（强制门 — STDD 最关键的门）

向用户展示完整的 Phase 2 产出后，**必须等待用户明确确认**：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD Phase 2: SPEC — 等待确认
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 产出物：
  ✅ design.md — 技术设计
  ✅ specs/<capability>/spec.md (N 个文件) — 行为规格（AI 草稿）
  ✅ test-plan.md — 测试方案

📊 关键指标：
  - Spec Requirements: N
  - Spec Scenarios: N
  - 置信度分布: ✓高:N ⚠中:N ⚠低:N
  - TC Cases: N
  - P0: N / P1: N / P2: N

🧠 经验库交叉检查（Step 2）：
  匹配经验: N 条 | 命中相关模式: N 条
  （如命中经验提示了某个失败模式，对应的 Scenario 已加入预防措施）

🔍 自动审查结果（Step 5.5 设计审查）：
  审查维度：需求覆盖 / Scenario 完备性 / TC-ID 一致性 / 文档一致性
  发现问题：N 项 | 已自动修复：N 项
  审查结论：✅ 全部通过 / ⚠️ N 项已修复 / ❌ N 项待处理

⚠️ 你的角色：审 spec，不是写 spec：
  1. ✓ 高置信度 Scenario（N 个）— 快速过目即可
  2. ⚠ 低置信度 Scenario（N 个）— **必须详细审核**（AI 可能理解有误）
  3. 技术方案是否合理？（design.md）
  4. 测试覆盖是否充分？（test-plan.md）
  5. TC 案例优先级是否合理？

👉 确认无误请回复，或提出修改意见。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

如果用户提出修改意见 → 根据反馈修订文档 → 重新展示等待确认
如果用户确认 → 锁定所有 Phase 2 文档

**未确认前，绝对不允许进入 Phase 3。**

> 确认门模板参见: `.stdd/skills/_shared/confirm-gate.md`

### Step 7: 写入文件

用户确认后：
1. 写入 `design.md`
2. 写入 `specs/<capability>/spec.md`（每个 capability 一个文件）
3. 写入 `test-plan.md`
4. 更新 `.stdd.yaml`（phase: spec → completed, confirmed_at 时间戳）

### Step 8: 【强制】执行模式选择（Gate 2 之后）

Phase 2 文档已锁定。在进入 Phase 3 之前，**必须**选择 Phase 3-5 的执行模式。此步骤不可跳过。

无论 `.stdd/config.d/long_range.yaml` 中 `recommended` 配置如何，必须使用 AskUserQuestion 向用户展示模式选择：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD Phase 3-5 执行模式选择
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 全自动长程模式 [推荐]
   · 一次性预授权所有交互点（流程决策 + 操作授权）
   · Phase 3-5 连续自动执行，无需交互
   · 仅 Gate 3 结束时等待确认（Gate 3 不自动跳过）

📋 普通交互模式
   · 重大设计偏离时暂停确认
   · 技术阻塞时暂停询问
   · 迭代达到上限时暂停报告
   · Gate 3 等待手动确认
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

→ 用户选择长程模式：进入 Step 8a 一次性预授权流程
→ 用户选择普通模式：进入 Step 8b，直接启动 Phase 3

#### Step 8a: 长程模式 — 一次性预授权

1. 读取模板：`.stdd/templates/long-range-auth.md`
2. **扫描 Phase 3-5 潜在交互点**：
   - 分析 `design.md` 中的技术决策，识别可能的偏离风险点
   - 分析 `test-plan.md` 中的测试范围，识别可能的技术阻塞点
   - 分析项目结构，识别 Phase 3-5 将涉及的操作类型：
     - 目录操作（创建 changes/ 子目录、调整 tests/ 结构）
     - 文件写入（源码、测试、pending-adjustments.md）
     - 命令执行（pytest、ruff、mypy）
     - 脚本执行（管线转换脚本等）
     - 网络访问（pip install 等）
     - 文件读取（templates、config、standards）
     - Git 只读操作（git diff/log/status）
3. 按模板生成授权清单，将扫描结果填入具体项
4. 向用户展示一次性授权清单，等待用户确认：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD 长程模式 — 一次性交互授权
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A. 流程决策授权
  ① 小设计偏离 → 自动记录，继续
  ② 大设计偏离 → 自动记录并继续（在 test-report 中汇总）
  ③ 技术阻塞 → 尝试绕过方案，记录到 pending-adjustments.md
  ④ 迭代上限 → 扩展为 10 轮，达上限后在 test-report 中汇总

B. 操作类授权
  ⑤ 目录操作 → 允许
  ⑥ 文件写入 → 允许
  ⑦ 命令执行（pytest/ruff/mypy）→ 允许
  ⑧ 脚本执行 → 允许
  ⑨ 网络访问 → 允许
  ⑩ 文件读取 → 允许
  ⑪ Git 只读操作 → 允许

C. Gate 确认
  ⑫ Gate 3 → 强制等待用户确认（不自动跳过）

⚠️ 降级条件：连续自动修复 3 次失败 / 测试通过率 < 95% / 安全相关问题

👉 回复「确认全部」进入全自动长程模式
👉 回复「普通模式」切换为常规交互模式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

5. **Step 8a.5: 配置 Claude Code 实际权限**（长程模式关键步骤）：
   - 读取 `.claude/settings.local.json`
   - 使用 Edit 工具在 `permissions.allow` 数组中添加以下规则：
     - Bash 规则：`Bash(pytest *)`, `Bash(ruff *)`, `Bash(python *)`, `Bash(pip *)`, `Bash(git *)`, `Bash(mkdir *)`, `Bash(cp *)`, `Bash(ls *)`
     - 文件规则：`Write(changes/**)`, `Edit(changes/**)`, `Write(app/**)`, `Edit(app/**)`, `Write(tests/**)`, `Edit(tests/**)`, `Write(.stdd/**)`, `Edit(.stdd/**)`, `Write(.claude/skills/**)`, `Edit(.claude/skills/**)`
     - 读取规则：`Read(.stdd/**)`, `Read(**/*.md)`, `Read(**/*.yaml)`, `Read(**/*.py)`, `Read(**/*.json)`
     - 搜索规则：`Glob(**)`, `Grep(**)`
     - Skill 规则：`Skill(stdd-slice)`, `Skill(stdd-build)`, `Skill(stdd-verify)`, `Skill(stdd-deliver)`
   - 此步骤将概念性预授权转化为 Claude Code 的实际工具权限，消除长程模式下的交互框
   - 权限配置仅修改项目级 `settings.local.json`，不影响全局配置
6. 用户确认全部授权后：
   - 更新 `.stdd.yaml`，记录长程模式状态：
     ```yaml
     long_range:
       enabled: true
       mode: "full_auto"
       pre_auth_completed: true
       pre_auth_timestamp: "<当前时间>"
     ```
   - 提示用户："长程模式已启用，Phase 3-5 将全自动连续执行，仅在 Gate 3 等待确认。"
   - 进入 Phase 3: SLICE

#### Step 8b: 普通模式 — 直接启动

1. 更新 `.stdd.yaml`：
   ```yaml
   long_range:
     enabled: false
     mode: "normal"
   ```
2. 提示用户："普通交互模式，Phase 3-5 将在需要时暂停交互。"
3. 进入 Phase 3: SLICE

## 产出物

- `design.md` — 技术设计文档
- `specs/<capability>/spec.md` — 行为规格
- `test-plan.md` — 测试方案（含 TC-ID 映射、覆盖矩阵、回归风险）
- `.stdd.yaml` — 更新状态（含 long_range 模式选择结果）

## 质量检查

完成前确认：
- [ ] design.md 覆盖所有技术决策，包含方案对比和选择理由
- [ ] 每个 spec Requirement 有 ≥1 个 Scenario
- [ ] 每个 Scenario 的 THEN 可客观验证且包含 SHALL
- [ ] test-plan.md 与 specs 的 Scenario 一一对应（无遗漏）
- [ ] TC-ID 全局唯一
- [ ] 回归风险矩阵标注了高/中/低风险区域
- [ ] 用户已明确确认所有 Phase 2 文档
- [ ] 用户已选择 Phase 3-5 执行模式（长程/普通）

## 下一阶段

Phase 2 确认完成 + 模式选择完成 → 进入 Phase 3: SLICE（切片规划）
