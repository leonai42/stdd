# STDD 流程改进 V2.2 测试方案与详细案例

> 版本：V2.2
> 创建日期：2026-05-15
> 对应 Phase 2 Spec：gate-interaction/spec.md, mode-selection/spec.md, long-range-execution/spec.md, verify-completeness/spec.md

## 一、测试策略

### 1.1 测试金字塔

本次变更为 STDD skill 文件（Markdown 文档）和配置文件修改，测试以**内容验证**为主：
- **验证层**（相当于单元）：对每个修改后的文件使用 Grep/Read 验证关键内容存在
- **一致性层**（相当于集成）：验证 3 份 skill 拷贝内容一致
- **人工审查**（相当于 E2E）：人工阅读修改后的 gate 模板确认格式正确

### 1.2 测试原则

- 每个 TC 使用 Grep 或 Read 工具可独立验证
- P0 案例在 Build 完成后立即验证
- 文件一致性在 P0 案例通过后集中检查

### 1.3 已有测试资产

本次是 STDD 自身的流程改进，无已有自动化测试。所有验证通过 Grep/Read + 人工审查完成。

## 二、详细测试案例

### 功能 1：Gate 交互信息展示（gate-interaction）

#### 案例 1.1 — Gate 1 包含 review 结果

| 字段 | 内容 |
|------|------|
| **ID** | TC-GATE-001 |
| **对应 Spec** | gate-interaction/spec.md → Scenario: Gate 1 展示 proposal review 结果 |
| **优先级** | P0 |
| **预置条件** | `.claude/skills/stdd-understand/SKILL.md` 已修改完成 |
| **输入** | `Grep "🔍 自动审查结果"` in understand SKILL.md |
| **预期结果** | 找到匹配行，且上下文包含「审查维度」「发现问题」「审查结论」 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.2 — Gate 2 包含 review 结果

| 字段 | 内容 |
|------|------|
| **ID** | TC-GATE-002 |
| **对应 Spec** | gate-interaction/spec.md → Scenario: Gate 2 展示 design+specs review 结果 |
| **优先级** | P0 |
| **预置条件** | `.claude/skills/stdd-spec/SKILL.md` 已修改完成 |
| **输入** | `Grep "🔍 自动审查结果"` in spec SKILL.md |
| **预期结果** | 找到匹配行，且上下文包含「需求覆盖」「Scenario 完备性」「审查结论」 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.3 — Gate 3 包含 review 结果和步骤确认

| 字段 | 内容 |
|------|------|
| **ID** | TC-GATE-003 |
| **对应 Spec** | gate-interaction/spec.md → Scenario: Gate 3 展示多路并行 review 结果和步骤确认 |
| **优先级** | P0 |
| **预置条件** | `.claude/skills/stdd-verify/SKILL.md` 已修改完成 |
| **输入** | `Grep "三路并行"` and `Grep "步骤完成确认"` in verify SKILL.md |
| **预期结果** | 两处均找到匹配行 |
| **当前状态** | ❌ 测试缺 |

### 功能 2：模式选择强制化（mode-selection）

#### 案例 2.1 — 模式选择标记为强制步骤

| 字段 | 内容 |
|------|------|
| **ID** | TC-MODE-001 |
| **对应 Spec** | mode-selection/spec.md → Scenario: 模式选择不可跳过 |
| **优先级** | P0 |
| **预置条件** | `.claude/skills/stdd-spec/SKILL.md` 已修改完成 |
| **输入** | `Grep "【强制】"` and `Grep "不能跳过"` in spec SKILL.md Step 7 附近 |
| **预期结果** | Step 7 区域包含强制标记和"不能跳过"指令 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.2 — 配置语义改为 recommended

| 字段 | 内容 |
|------|------|
| **ID** | TC-MODE-002 |
| **对应 Spec** | mode-selection/spec.md → Scenario: 模式选择不可跳过 |
| **优先级** | P1 |
| **预置条件** | `.stdd/config.d/long_range.yaml` 已修改 |
| **输入** | `Grep "recommended"` in long_range.yaml |
| **预期结果** | 找到 `recommended: true`，找不到 `default: true` |
| **当前状态** | ❌ 测试缺 |

### 功能 3：长程模式自动化（long-range-execution）

#### 案例 3.1 — 预授权包含权限配置步骤

| 字段 | 内容 |
|------|------|
| **ID** | TC-LONG-001 |
| **对应 Spec** | long-range-execution/spec.md → Scenario: 预授权确认后配置 Claude Code 权限 |
| **优先级** | P0 |
| **预置条件** | `.claude/skills/stdd-spec/SKILL.md` 已修改完成 |
| **输入** | `Grep "settings.local.json"` in spec SKILL.md |
| **预期结果** | Step 7a 区域包含对 settings.local.json 的 Edit 操作说明 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.2 — Build 末尾有自动衔接指令

| 字段 | 内容 |
|------|------|
| **ID** | TC-LONG-002 |
| **对应 Spec** | long-range-execution/spec.md → Scenario: Build 完成后自动进入 Verify |
| **优先级** | P0 |
| **预置条件** | `.claude/skills/stdd-build/SKILL.md` 已修改完成 |
| **输入** | `Grep "自动调用.*stdd-verify\|自动进入.*Phase 5\|自动进入.*VERIFY"` in build SKILL.md |
| **预期结果** | 找到长程模式下的自动衔接指令 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.3 — Build 包含长程运行协议

| 字段 | 内容 |
|------|------|
| **ID** | TC-LONG-003 |
| **对应 Spec** | long-range-execution/spec.md → Scenario: Build 阶段无交互执行 |
| **优先级** | P1 |
| **预置条件** | `.claude/skills/stdd-build/SKILL.md` 已修改完成 |
| **输入** | `Grep "长程模式运行协议"` in build SKILL.md |
| **预期结果** | 找到协议章节，包含无交互、批量执行、降级检测等规则 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.4 — Verify 包含长程运行协议

| 字段 | 内容 |
|------|------|
| **ID** | TC-LONG-004 |
| **对应 Spec** | long-range-execution/spec.md → Scenario: Verify 阶段无交互执行 |
| **优先级** | P1 |
| **预置条件** | `.claude/skills/stdd-verify/SKILL.md` 已修改完成 |
| **输入** | `Grep "长程模式运行协议"` in verify SKILL.md |
| **预期结果** | 找到协议章节 |
| **当前状态** | ❌ 测试缺 |

### 功能 4：Verify 完整性保障（verify-completeness）

#### 案例 4.1 — Verify 开头有强制步骤清单

| 字段 | 内容 |
|------|------|
| **ID** | TC-VERIFY-001 |
| **对应 Spec** | verify-completeness/spec.md → Scenario: 6 个强制步骤全部执行后才能进入 Gate 3 |
| **优先级** | P0 |
| **预置条件** | `.claude/skills/stdd-verify/SKILL.md` 已修改完成 |
| **输入** | `Grep "强制步骤清单"` in verify SKILL.md |
| **预期结果** | 找到 6 步清单表格（Step 0-5），每步有名称和完成标志 |
| **当前状态** | ❌ 测试缺 |

#### 案例 4.2 — Gate 3 模板有步骤完成确认表

| 字段 | 内容 |
|------|------|
| **ID** | TC-VERIFY-002 |
| **对应 Spec** | verify-completeness/spec.md → Scenario: Gate 3 展示步骤完成确认表 |
| **优先级** | P0 |
| **预置条件** | `.claude/skills/stdd-verify/SKILL.md` 已修改完成 |
| **输入** | `Grep "Step 0.*已完成\|Step 0.*✅"` in verify SKILL.md Gate 3 区域 |
| **预期结果** | Gate 3 模板包含 6 行步骤状态确认（Step 0-5 各标记 ✅/N/A） |
| **当前状态** | ❌ 测试缺 |

## 三、测试执行矩阵

| 功能模块 | 内容验证（Grep/Read） | 一致性验证（跨文件对比） | 人工审查 | 状态 |
|----------|----------------------|-------------------------|---------|------|
| gate-interaction | TC-GATE-001~003 | 3份拷贝一致 | Gate模板格式 | 🔴 待实现 |
| mode-selection | TC-MODE-001~002 | 3份拷贝一致 | AskUserQuestion用法 | 🔴 待实现 |
| long-range-execution | TC-LONG-001~004 | 3份拷贝一致 | 权限配置安全性 | 🔴 待实现 |
| verify-completeness | TC-VERIFY-001~002 | 3份拷贝一致 | 清单完整性 | 🔴 待实现 |

## 四、回归风险矩阵

| 风险区域 | V2.2 改动 | 已有回归保护 | 风险等级 |
|----------|-----------|-------------|---------|
| Gate 消息模板 | 增加 review 块，不改变原有确认逻辑 | 人工对比修改前后 | 🟢 低 |
| 模式选择流程 | 从可跳过改为强制 | 人工验证每次出现 | 🟡 中 |
| 长程权限配置 | 修改 settings.local.json | 检查修改范围限于项目级 | 🟡 中 |
| Skill 文件结构 | 增加章节，调整措辞 | 人工审查不影响原有流程 | 🟢 低 |
| 3 份 skill 拷贝 | 同步修改 12+ 文件 | 逐文件 Grep 验证关键内容 | 🟡 中 |

## 五、建议补充顺序

1. **第一优先**（Build 阶段每切片完成后立即验证）：TC-GATE-001, TC-GATE-002, TC-GATE-003, TC-MODE-001, TC-LONG-001, TC-LONG-002, TC-VERIFY-001, TC-VERIFY-002
2. **第二优先**（全部 P0 通过后验证）：TC-MODE-002, TC-LONG-003, TC-LONG-004
3. **第三优先**（全部通过后人工审查）：3 份拷贝一致性、Gate 模板格式、权限配置安全性
