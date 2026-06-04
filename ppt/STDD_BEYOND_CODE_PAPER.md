# Spec+Test 双驱动方法论在非编程领域的应用研究

## STDD Beyond Code — From AI Coding Quality to Universal Execution Verification

**小以AI实验室**  
**2026 年 6 月**

---

## 摘要

Spec+Test Driven Development (STDD) 最初作为一种 AI 辅助编程质量保障方法被提出，通过 Spec 先行、TDD 执行、经验自学习的六阶段流程，将模糊需求转化为高质量交付。本文论证 STDD 的核心方法论——定义预期、执行、验证结果、积累经验——不依赖于"代码"这一介质，而适用于任何可以明确描述预期结果的工作场景。本文系统阐述了 STDD 在金融业务（量化交易、风控审计、基金产品上线）、日常工作（官网维护、文档发布、客户交付）、技术运维（部署验证、配置变更）等 13 个非编程场景中的应用模式，并提出了通用 Agent 验证管线作为技术支撑。研究表明，STDD 方法论的适用范围远超出编程领域，本质上是一套通用的"AI 执行质量保障框架"。

**关键词**：Spec+Test 双驱动；AI 执行验证；非编程场景；经验自学习；Agent 验证管线

---

## 1. 引言

2025-2026 年，AI 编程工具经历了从"Vibe Coding"到"Spec-Driven Development"的范式迁移。以 Spec Kit、OpenSpec、Superpowers 为代表的框架达成了共识：在 AI 生成代码之前，应当先与 AI 就"做什么"达成结构化的一致[1]。

STDD 在这一共识之上增加了两个独特维度：**强制 TDD 执行**（而非可选）和**项目级经验自学习**（而非每次从零开始）。这两个维度共同构成了 STDD 的核心循环：定义预期 → 验证结果 → 积累经验 → 下次更精准。

本文的核心论点是：**这个循环不依赖"代码"作为介质**。它依赖的是"可以明确描述预期结果并验证"——而这几乎覆盖了所有需要可靠性的专业工作。

## 2. STDD 方法论的核心抽象

### 2.1 三要素循环

STDD 的方法论可以抽象为三个独立于应用领域的要素：

```
预期定义 (Spec) → 执行 (Build) → 验证 (Verify) → 经验沉淀 (Learn) → 反馈
```

| 要素 | 编程场景 | 非编程场景 |
|------|---------|-----------|
| 预期定义 | GIVEN/WHEN/THEN 行为规格 | 前置条件 / 操作步骤 / 预期结果 |
| 验证方式 | pytest / unittest | Agent 检查点断言 (CLI/HTTP/文件) |
| 经验对象 | 代码失败模式 (11→12类) | 流程失败模式 (可扩展类别) |

关键差异在于**验证方式**的变化：编程场景中验证由测试框架执行，非编程场景中验证由 Agent 验证管线（V2.7 引入的 `stdd agent verify`）执行。这一技术突破使得 STDD 的方法论可以脱离"代码"而独立运作。

### 2.2 六阶段流程的通用性

STDD 的六阶段流程设计之初就考虑了通用性：

| 阶段 | 本质 | 编程场景产出 | 非编程场景产出 |
|------|------|------------|-------------|
| UNDERSTAND | 需求结构化 | proposal.md | proposal.md |
| SPEC | 预期定义 | GIVEN/WHEN/THEN spec | agent_spec.yaml |
| SLICE | 任务分解 | slices.md | 检查点分组 |
| BUILD | 执行 | TDD RED→GREEN | Agent 操作 |
| VERIFY | 验证 | pytest + 覆盖率 | CP 断言验证 |
| DELIVER | 归档学习 | archive + merge | archive + 经验 |

### 2.3 经验自学习：从项目级到领域级

V2.5 引入的 5 态经验生命周期（discovered→verified→deposited→shared→merged）和社区经验共享池（GitHub+Gitee 零后端设计），使得经验的受益范围从"单个项目"扩展到"整个社区"。这是 STDD 区别于所有其他框架的关键优势——没有其他框架具备结构化的经验积累和跨项目复用机制。

## 3. 技术基础：Agent 验证管线

### 3.1 架构

V2.7 引入的 Agent 验证管线提供了非编程场景的技术基础：

```
agent_spec.yaml → CP 解析器 → 逐 CP 执行 → 断言验证 → report
     ↑                                              ↓
  人工定义                                      失败→回溯修复
                                               成功→经验记录
```

### 3.2 agent_spec 格式

```yaml
meta:
  task_id: <任务标识>
  system: <目标系统>
  preconditions: [<前置条件>]
steps:
  - id: CP-1
    description: <检查点描述>
    action: <CLI 命令或 HTTP 请求>
    assertions:
      - type: exit_code | stdout_contains | http_status
        expected: <预期值>
rollback:
  steps: [<回滚步骤>]
```

agent_spec 的设计哲学是"机器可执行，人类可阅读"。它同时服务于两个目的：作为 AI Agent 的**执行指令**，和作为人类审阅者的**标准操作流程文档**。

## 4. 金融业务场景应用

### 4.1 量化交易策略上线

量化策略从回测到实盘的切换是金融领域风险最高的操作之一。传统流程依赖人工 checklist 和口头确认，存在重大操作风险。

**STDD 方案**：定义 5 个关键检查点（CP），覆盖数据完整性、参数合规性、风控规则有效性、订单模拟准确性、绩效指标合理性。每个 CP 有明确的验证标准和失败处理流程。

**实际效果**：TStrategy 量化系统（STDD 案例之一）已迭代至 V4.2，19,500+ 行测试代码，全链路从回测到风控均通过 STDD 管理。每一次策略参数调整走完整的 UNDERSTAND→SPEC→VERIFY 流程，经验库积累了 40+ 条量化特有的失败模式。

### 4.2 风控规则变更审计

金融机构的风控规则变更需要满足监管审计要求。传统的邮件审批流程不可追溯，口头决策无法举证。

**STDD 方案**：完整审计追溯链——`风控需求 → proposal.md → Gate 确认 → test-report.md → archive`。每条风控规则变更有完整的决策记录和验证证据。

### 4.3 基金产品上线

新基金上线涉及托管、备案、销售、清算等 20+ 个外部系统协调。任何环节遗漏都可能导致上线延期或合规问题。

**STDD 方案**：20+ CP 的 agent_spec.yaml 作为标准化上线检查清单，每次新基金上线复用同一份 spec，经验库持续积累跨系统协调的常见问题。

## 5. 日常工作场景应用

### 5.1 官网维护与迭代

STDD 官网本身即采用 STDD 管理。每次迭代走完整六阶段流程，发布前通过 agent_spec.yaml 自动验证链接有效性、中英双语一致性、响应式适配、版本号同步。

### 5.2 技术文档发布

文档发布中常见的链接失效、版本号不一致、代码示例过期等问题，可通过 agent_spec 自动化检查。经验库积累"文档-代码不同步"的高频触发条件。

### 5.3 客户需求管理与交付

客户需求通过微信/邮件碎片化传达是 B2B 软件项目的常见痛点。STDD 的 proposal→Gate 确认→deliver 流程提供结构化的需求锁定和验收机制。

## 6. 方法论适用性边界

STDD 方法论适用于满足以下条件的工作：
1. **可定义预期结果**：能够明确描述"做好是什么样"
2. **可验证**：存在客观方式判断预期是否达成
3. **有重复性**：同类任务会反复出现（经验积累才有意义）

不适用场景：
- 纯创意工作（预期无法精确定义）
- 一次性任务（经验积累无意义）
- 需要实时直觉判断的工作（无法预定义流程）

## 7. 结论与展望

STDD 从"AI 编程质量工具"到"通用 AI 执行验证框架"的扩展，在方法论层面是自然的——因为其核心循环（定义预期→验证→学习）不依赖于代码。在技术层面，V2.7 的 Agent 验证管线为这一扩展提供了工程基础。

未来方向包括：
- **领域经验包**：金融、医疗、法律等垂直领域的预置经验包
- **多系统 Agent 验证**：跨系统的复杂业务流程验证（STDD for TEAM）
- **自适应检查点**：AI 根据历史经验自动生成和优化检查点序列

**STDD 的本质**不是一个编程工具，而是一套**让 AI 的输出从"不确定"变为"可预期"的方法论**。这一方法论适用于任何"AI 能执行、但需要质量保障"的场景。

---

## 参考文献

[1] GitHub. Spec Kit: Spec-Driven Development Toolkit. https://github.com/github/spec-kit, 2026.  
[2] Fission-AI. OpenSpec: Lightweight Specification Framework. https://github.com/Fission-AI/OpenSpec, 2026.  
[3] Vincent, J. Superpowers: Composable Skills for AI Coding Agents. https://github.com/obra/superpowers, 2026.  
[4] Klem, E. EvanFlow: TDD-Driven Iterative Feedback Loop. https://github.com/evanklem/evanflow, 2026.  
[5] BMAD Code Org. BMAD Method: Multi-Agent Agile Framework. https://github.com/bmad-code-org/BMAD-METHOD, 2026.  
[6] Amazon Web Services. Kiro: Agentic AI IDE. https://aws.amazon.com/kiro/, 2026.  
[7] McHenry, C. CodeGraph: Pre-indexed Code Knowledge Graph. https://github.com/colbymchenry/codegraph, 2026.  
[8] affaan-m. ECC: Everything Claude Code. https://github.com/affaan-m/ECC, 2026.  
[9] 小以AI实验室. STDD: Spec+Test Driven Development. https://github.com/leonai42/stdd, 2026.
