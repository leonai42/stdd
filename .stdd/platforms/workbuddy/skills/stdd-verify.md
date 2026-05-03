---
name: stdd-verify
description: STDD Phase 5: 质量验证
version: "1.0"
trigger_keywords: ["stdd-verify", "stdd verify", "spec-driven", "tdd"]
---
# STDD Phase 5: VERIFY — 质量验证

## 阶段目标

全量质量检查，生成测试报告，追溯设计调整，等待用户最终确认。

## 前置条件

- Phase 4 已完成（所有切片实现完毕）
- `.stdd.yaml` 中 `phases.build.status == "completed"`

## 执行模式

**迭代检查循环，最多 5 轮。完成后必须等待用户确认。**

## 执行流程

### 迭代循环（最多 5 轮）

每轮执行以下步骤，有失败则修复后重新开始：

---

#### Step 1: 运行全量质量检查

读取 `.stdd/config.yaml` 中的 `quality` 配置，执行：

1. **全量测试**：`pytest tests/ -v`
2. **Lint 检查**：`ruff check app/ tests/`
3. **类型检查**（如配置了 mypy/pyright）

→ 有失败：修复 → 重新运行直到全部通过
→ 全部通过：进入 Step 2

---

#### Step 2: Diff 审查

检查 git diff 的每个变更文件，逐项检查：

- **死代码**：print 调试语句、注释掉的代码块、未使用的 import/变量
- **命名**：名称是否匹配实际行为（不产生误导）
- **Deletion test**：每个新模块是否值得存在？移除它复杂度会集中在调用方吗？
- **Magic strings/numbers**：应该是常量或枚举
- **错误处理**：边界输入是否验证、外部调用是否包装
- **类型安全**：是否有需要收敛的宽类型
- **安全**：认证/授权/注入防护是否到位
- **测试断言正确性**：每个断言，如果实现中有一个字符的 bug，它能否检测到？
- **范围蔓延**：diff 中有没有超出 Phase 2 计划的改动？
- **注释**：只保留 WHY（非显而易见的约束、微妙的不变性），删掉 WHAT 注释

→ 发现问题：修复 → 回到 Step 1
→ 无问题：进入 Step 3

---

#### Step 3: 五类失败模式检查

对 diff 进行以下专项检查：

**(a) 幻觉行为** — 编造的文件路径、环境变量、函数名、库 API
- 检查：引用的文件路径是否存在？环境变量是否在 config 中定义？

**(b) 范围蔓延** — 超出计划文件的改动、打包进来的重构
- 检查：diff 中的每个文件是否在 Phase 1 proposal 的 Impact 中？
- 如果有额外改动：是否必要？应该拆分到独立的 change 吗？

**(c) 级联错误** — 静默吞掉的异常、空数组 fallback 掩盖问题
- 检查：每个 try/catch 是否在正确的层级？是否有 `return []` 掩盖了真错误？
- 原则：只在系统边界捕获异常

**(d) 上下文丢失** — 与 proposal/design/spec 决策矛盾
- 检查：实现是否与 Phase 2 的设计文档一致？
- 如果不一致：是有意调整（应记录在 pending-adjustments），还是无意偏离？

**(e) 工具误用** — 错误的工具选择或参数
- 检查：文件操作是否用了专用工具而不是 shell 命令？

---

#### Step 4: 汇总设计调整

1. 检查 `pending-adjustments.md`（Phase 3-4 期间记录的偏离）
2. 对比最终实现与 Phase 2 原始文档的差异
3. 识别以下类型的调整：
   - spec Scenario 增删改
   - design 技术方案变更
   - test-plan TC 案例调整
   - 实现中发现的边界情况补充

如果有任何调整，读取模板 `.stdd/templates/design-adjustments.md` 并生成 `design-adjustments.md`

---

#### Step 5: 生成测试报告

读取模板：`.stdd/templates/test-report.md`

生成 `test-report.md`，包含：
1. **总体概况**：总数/通过/失败/跳过/通过率/耗时
2. **按模块统计**：每个测试文件的详细统计
3. **失败项详细分析**（如有）：根因 + 影响 + 结论
4. **功能/测试覆盖对照**：功能-实现-测试三方对照
5. **设计调整说明**：引用 design-adjustments.md（如有）
6. **修复确认记录**：Phase 5 迭代中发现并修复的问题
7. **结论**：总体评估和部署建议

---

### 停止条件

**正常停止**（全部满足）：
- 全量测试通过（排除已知环境问题）
- Lint 通过
- Diff 审查无新问题
- 五类失败模式无命中
- design-adjustments.md 已生成（如有调整）
- test-report.md 已生成

**硬上限停止**：
- 达到 5 轮迭代仍未全部通过
- 向用户报告剩余问题，由用户决定：继续迭代 or 回到 Phase 2

### Step 6: 用户确认（强制门）

向用户展示测试结果和设计调整后，**必须等待用户明确确认**：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD Phase 5: VERIFY — 等待确认
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 产出物：
  ✅ test-report.md — 测试报告

📊 测试结果：
  - 总数: N / 通过: N / 失败: N / 跳过: N
  - 通过率: N%

📝 设计调整（如有）：
  <design-adjustments.md 摘要>

⚠️ 请确认：
  - 测试结果是否满意？
  - 设计调整是否合理？
  - 是否可以进入交付阶段？

👉 确认继续，或提出需要调整的地方。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

- 用户确认 → 进入 Phase 6
- 用户有异议或变更需求 → 回到 Phase 2 修订

## 产出物

- `test-report.md` — 测试执行报告
- `design-adjustments.md` — 设计调整说明（如有）
- 更新 `.stdd.yaml`（phase: verify → completed）

## 质量检查

完成前确认：
- 通过率计算正确（通过 / (总数 - 跳过) × 100%）
- 失败项都有根因分析和结论（区分代码 bug vs 环境问题）
- 功能覆盖表与 test-plan.md 的执行矩阵一致
- 设计调整（如有）已完整记录

## 下一阶段

Phase 5 用户确认 → 进入 Phase 6: DELIVER（交付）
Phase 5 用户有异议 → 回到 Phase 2: SPEC（修订规格）
