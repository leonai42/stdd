# Spec: 锚定体系（Anchoring System）

> 对应板块 E（E3）+ 板块 A（A1/A2/A7）| 4 个 New Capabilities
> anchoring-methodology / anchoring-phase2-integration / failure-mode-l / anchors-directory

## ADDED Requirements

### Requirement: Spec 锚定法 L1 方法论文档 <!-- confidence: high -->

STDD SHALL 提供独立的方法论文档定义四级锚定体系及 L1 行为锚定的写作规范。

**证据来源**：proposal.md `Capabilities > New > anchoring-methodology`

#### Scenario: 方法论文档可用 <!-- confidence: high -->

- **GIVEN** STDD V2.7 已安装
- **WHEN** 开发者打开 `STDD_ANCHORING.md`
- **THEN** 文档 SHALL 包含 L1-L4 四级锚定定义、适用场景、成本评估、流程集成说明
- **AND** L1 行为锚定的写作规范 SHALL 包含：THEN 用 SHALL 写死强制性行为、每个 Requirement ≥1 个 Scenario、边界值完整

---

### Requirement: 锚定评估 Phase 2 集成 <!-- confidence: high -->

STDD SHALL 在 Phase 2 SPEC 流程中新增锚定评估步骤（Step 2.4），对 critical Change 进行自由度评估。

**证据来源**：proposal.md `Capabilities > New > anchoring-phase2-integration`

#### Scenario: critical Change 触发锚定评估 <!-- confidence: high -->

- **GIVEN** proposal.critical == true 或 risk_assessment 中有任意 true
- **WHEN** Phase 2 SPEC 执行到 Step 2.3（生成 specs 完成）之后
- **THEN** AI SHALL 执行 Step 2.4 锚定评估：检查 spec 的 SHALL 覆盖度、多实现可能性、关键决策点锁定度
- **AND** 评估结果 SHALL 输出 "自由度 ≤ 阈值（通过）" 或 "自由度 > 阈值（需补充锚定）"

#### Scenario: 非 critical Change 跳过锚定评估 <!-- confidence: high -->

- **GIVEN** proposal.critical == false 且 risk_assessment 全部为 false
- **WHEN** Phase 2 SPEC 执行
- **THEN** Step 2.4 SHALL 被跳过，直接进入 Gate 2

#### Scenario: Gate 2 锚定阻断 <!-- confidence: high -->

- **GIVEN** proposal.critical == true 且 safety_critical == true（需至少 L3）
- **WHEN** proposal.anchoring.level == L1（不满足最低要求）
- **THEN** Gate 2 SHALL 阻塞，提示："锚定等级不足：当前 L1，最低要求 L3"
- **AND** 用户 SHALL 必须补充锚定（升级到 L3+）或明确降级为非 critical 后才能通过 Gate 2

---

### Requirement: 第 12 类失败模式 (l) 锚定缺失 <!-- confidence: high -->

STDD SHALL 新增第 12 类失败模式 (l) 锚定缺失，并在 Phase 5 VERIFY 检查清单中加入此项检查。

**证据来源**：proposal.md `Capabilities > New > failure-mode-l`

#### Scenario: Phase 5 自动检测锚定缺失 <!-- confidence: high -->

- **GIVEN** critical Change 的 proposal.anchoring.level < required_level
- **WHEN** Phase 5 VERIFY 执行 12 类失败模式检查
- **THEN** 系统 SHALL 在 (l) 锚定缺失项标记为 FAIL
- **AND** test-report.md 中 SHALL 记录："(l) 锚定缺失 — 当前等级 L{n}，要求 L{m}"

#### Scenario: Phase 5 回溯检测 spec 歧义 <!-- confidence: medium -->

- **GIVEN** Phase 4 BUILD 中产生了 3+ 次设计偏离
- **WHEN** Phase 5 VERIFY 执行失败模式检查
- **THEN** AI SHALL 回溯标记："spec 锚定可能不足 — 3+ design-adjustments recorded"
- **AND** 建议用户在下次类似 Change 时提升锚定等级

---

### Requirement: anchors/ 目录 + L2/L3/L4 锚定支持 <!-- confidence: high -->

STDD SHALL 创建 `anchors/` 目录存放锚定参考物，按 L2/L3/L4 三级组织。

**证据来源**：proposal.md `Capabilities > New > anchors-directory`

#### Scenario: 创建 L2 接口锚定 <!-- confidence: high -->

- **GIVEN** proposal.anchoring.level >= L2
- **WHEN** Phase 2 SPEC 执行
- **THEN** AI SHALL 在 `anchors/L2-interfaces/<change-name>/` 下创建 api-contract.yaml
- **AND** 接口定义 SHALL 包含精确的函数签名、请求/响应 schema、字段类型和约束

#### Scenario: 创建 L3 模式锚定 <!-- confidence: high -->

- **GIVEN** proposal.anchoring.level == L3
- **WHEN** Phase 2 SPEC 执行
- **THEN** AI SHALL 在 `anchors/L3-patterns/<change-name>/` 下创建参考索引
- **AND** 索引 SHALL 引用已有 Change 的 spec 摘要，注明可复用的设计模式

#### Scenario: 创建 L4 基准锚定 <!-- confidence: high -->

- **GIVEN** proposal.anchoring.level == L4 且 anchor_implementations 非空
- **WHEN** Phase 2 SPEC 执行
- **THEN** AI SHALL 在 `anchors/L4-baselines/<change-name>/` 下编写参考实现代码
- **AND** spec.md 开头 SHALL 注明 "Anchor Implementation: anchors/L4-baselines/<name>/"
