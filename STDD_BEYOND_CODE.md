# STDD：不止于代码 — 通用场景应用指南

> 版本：V2.5+ | 日期：2026-06-04
> STDD 方法论从"AI 编程质量工具"扩展到"AI 执行验证工具"

---

## 一、为什么 STDD 天生适合非编程场景

STDD 的核心是一个三要素循环：

```
定义预期 → 执行 → 验证结果 → 记录经验 → 下次更精准
   ↑                                              ↓
   └──────────────────── 反馈 ←────────────────────┘
```

这个循环**不依赖"代码"这个介质**。它依赖的是"可以明确描述预期结果"——而这几乎覆盖了所有需要可靠性的工作。

| 维度 | 编程场景 | 非编程场景 |
|------|---------|-----------|
| 预期定义 | GIVEN/WHEN/THEN | 前置条件/操作/预期结果 |
| 验证方式 | pytest 测试 | 检查点断言 (CLI/HTTP/文件) |
| 经验对象 | 代码失败模式 | 流程失败模式 |
| 质量门 | Gate 1/2/3 | 同样适用 |

**关键差异**：V2.7 的 Agent 验证管线（`stdd agent verify`）已经为"非代码验证"提供了技术基础——对任意操作序列执行检查点断言。

---

## 二、金融业务场景

### 2.1 量化交易策略上线流程

**痛点**：策略从回测到实盘，涉及数据完整性、参数校验、风控规则、仓位计算等多个环节。任何一个环节出错，损失的不是代码质量，是真金白银。

**STDD 方案**：

```
Phase 1: UNDERSTAND
  proposal.md — 策略变更的范围描述
  例: "新增多空双向策略，基于 RSRS 信号 + 波动率过滤"

Phase 2: SPEC  
  agent_spec.yaml — 上线前检查点
  CP-1: 回测数据完整性 (品种数量/时间跨度/缺失值率)
  CP-2: 参数合规性 (止损比例/仓位上限/信号冷却期)
  CP-3: 风控规则有效性 (日亏损熔断/连亏降仓)
  CP-4: 订单模拟准确性 (滑点/手续费/成交率)
  CP-5: 绩效指标合理性 (夏普>0.8 / 最大回撤<25%)

Phase 4: BUILD
  AI 执行检查点 → 产生验证报告

Phase 5: VERIFY
  5 个 CP 全部通过 → 可以上线
  任一 CP 失败 → 回到 Phase 2 修改参数

经验库:
  EXP-量化-001: "回测数据包含未来函数 → 信号曲线异常平滑"
  EXP-量化-002: "参数过拟合 → 样本外表现断崖"
  EXP-量化-003: "未考虑交易成本 → 实盘收益低于回测 40%"
```

**为什么 STDD 适合**：量化策略上线本质上是一个"多条件校验流程"，天然匹配 STDD 的"定义预期→逐条验证"模式。

---

### 2.2 风控规则变更审计

**痛点**：金融机构的风控规则变更需要多级审批和审计追溯。口头沟通容易遗漏，邮件审批不可追溯。

**STDD 方案**：

```
Phase 1: UNDERSTAND
  proposal.md — 风控变更的因果分析
  例: "日亏损限制从 5% 调整为 3%，原因：近期市场波动率上升 40%"

Phase 2: SPEC
  specs/risk-rule-change/spec.md
  Scenario 1: 日亏损达 3% — THEN 系统 SHALL 触发熔断
  Scenario 2: 日亏损达 3% 后恢复 — THEN 系统 SHALL 在次日开盘前解除熔断
  Scenario 3: 人工干预 — THEN 系统 SHALL 记录完整审计日志

Phase 4: BUILD
  AI 生成配置变更 + 测试 Case

Phase 5: VERIFY
  逐条验证 + 审计日志完整性

Phase 6: DELIVER
  归档 → 审计追溯链完整
```

**审计追溯链**：`风控需求 REQ-001 → change 2026-06-04-risk-limit → Gate 1/2/3 确认记录 → test-report.md`

**为什么 STDD 适合**：金融合规的核心是"可追溯的决策链"。STDD 的 Gate 确认 + 归档体系天然满足这个需求。

---

### 2.3 数据报表生成与验证

**痛点**：金融报表（净值报告、风控日报、监管报表）数据来源多、计算逻辑复杂，人工核对容易遗漏。

**STDD 方案**：

```
agent_spec.yaml — 日报生成验证
CP-1: 数据源完整性 (行情/交易/资金数据文件存在且非空)
CP-2: 关键指标交叉验证 (计算净值 vs 托管净值偏差 < 0.1%)
CP-3: 异常值检测 (单日收益率 > 10% → 标记人工复核)
CP-4: 格式合规 (报表字段/单位/小数位符合监管要求)
CP-5: 发送确认 (邮件/API 发送成功)

经验库:
  EXP-报表-001: "分红除权导致净值跳空 → 需人工标注"
  EXP-报表-002: "非交易日数据未过滤 → 统计偏差"
```

---

### 2.4 基金产品上线检查

**痛点**：新基金上线涉及托管、备案、销售、清算等多个外部系统协调。

**STDD 方案**：

```
agent_spec.yaml — 基金上线检查清单 (20+ CP)
CP-01: 基金合同备案号已获取
CP-02: 托管账户已开立且测试转账成功
CP-03: TA 系统基金代码已配置
CP-04: 销售渠道产品信息已同步
CP-05: 风险揭示书模板已审核
CP-06: 净值计算脚本验证通过
...
CP-20: 7×24 监控告警已配置

每次新基金上线 → 复用同一份 agent_spec → 逐项确认
经验库积累: 每只基金上线遇到的问题自动沉淀
```

**为什么 STDD 适合**：跨系统协调流程长、步骤多、容易遗漏。STDD 的 checklist 模式让每个步骤都有明确的 owner 和验证方式。

---

## 三、日常工作场景

### 3.1 官网维护与迭代

**痛点**：官网改动频繁（内容更新、SEO优化、双语同步），但没有流程约束，容易出现链接断裂、版本信息过期、中英文不同步。

**STDD 方案（立即可用）**：

```
Phase 1: UNDERSTAND
  /stdd-understand "官网 Hero 更新至 V2.8，新增用户案例"
  → proposal.md (Why / What Changes / Impact)

Phase 2: SPEC
  agent_spec.yaml — 官网发布前检查
  CP-1: 所有链接有效 (内部 href + 外部 URL)
  CP-2: 中英双语 key 完整 (zh/en 键值数量一致)
  CP-3: 移动端响应式正常 (宽度 375px/768px/1200px)
  CP-4: 版本号与 CHANGELOG 一致
  CP-5: 百度统计代码存在
  CP-6: 页面加载 < 3s

Phase 4: BUILD
  AI 修改 HTML → 本地预览

Phase 5: VERIFY
  stdd agent verify website-deploy
  全部 CP 通过 → 上传部署

Phase 6: DELIVER
  归档 → specs/website/ 合并
```

**为什么出彩**：这是马上能跑的。官网的"发布前检查清单"用 agent_spec.yaml 管理，每次迭代走完整流程，积累"链接失效"、"i18n遗漏"等经验。

---

### 3.2 技术文档发布

**痛点**：README、CHANGELOG、API 文档经常出现"代码改了但文档没改"、"版本号不一致"、"链接指向旧版本"等问题。

**STDD 方案**：

```
agent_spec.yaml — 文档发布检查
CP-1: 版本号一致性 (README/CHANGELOG/pyproject.toml 一致)
CP-2: 内部链接有效性 (所有相对路径可访问)
CP-3: 代码示例可执行 (Python/Shell 代码块能跑通)
CP-4: 拼写检查通过 (英文拼写 + 中文错别字)
CP-5: 中英段落对应 (每个章节两语言都有)

经验库:
  EXP-文档-001: "新增 CLI 命令但忘记更新 --help 输出"
  EXP-文档-002: "修改默认值但文档示例未同步更新"
```

---

### 3.3 会议决策追踪

**痛点**：技术决策会议的结论依赖口头传达或聊天记录，过两周就没人记得"当时为什么选这个方案"。

**STDD 方案**：

```
Phase 1: UNDERSTAND
  proposal.md — 会议决策记录
  例: "技术选型: 消息队列选 Kafka 而非 RabbitMQ"
  Why: "需支持 10万/秒 吞吐，RabbitMQ 在 5万/秒 时延迟线性增长"
  What Changes: 架构中引入 Kafka 集群

Phase 2: SPEC
  design.md — 决策的详细论证
  对比矩阵、性能测试数据、成本估算

Phase 4: BUILD (可选)
  如果是"暂缓决策" → 标记为 pending
  如果是"采纳决策" → 关联到具体 change

Phase 6: DELIVER
  归档 → 决策可追溯
```

**为什么出彩**：技术决策的可追溯性——半年后新同事问"为什么用 Kafka"，不是翻聊天记录，是看 design.md。

---

### 3.4 新人入职 Onboarding

**痛点**：新人入职需要配置几十个工具、申请十几个权限、学习多个内部系统。通常靠"老人带"或者一份过时的 Wiki。

**STDD 方案**：

```
agent_spec.yaml — 新人入职检查清单
CP-01: 公司邮箱已开通
CP-02: VPN 账号已配置
CP-03: GitHub SSH Key 已添加
CP-04: Python/JDK/Node 已安装指定版本
CP-05: 本地 STDD 已初始化
CP-06: 代码仓库权限已授予 (至少 3 个项目)
CP-07: CI/CD 流水线可触发
...
CP-15: 新人第一个 change 已完成 (Hello STDD)

经验库:
  EXP-Onboard-001: "Windows WSL2 网络配置导致 VPN 冲突"
  EXP-Onboard-002: "M1 Mac 上特定 Python 包需要 Rosetta"
```

**价值**：每入职一个人，经验库就更完善一点。第 10 个新人入职时，checklist 已经非常成熟。

---

### 3.5 客户需求管理与交付

**痛点**：客户需求通过微信/邮件/会议碎片化传达，开发团队收到的需求是"二手信息"，容易理解偏差。

**STDD 方案**：

```
Phase 1: UNDERSTAND
  客户原始需求 → proposal.md (Why / What / Success Criteria)
  Gate 1: 客户确认 proposal → 锁定需求范围

Phase 2: SPEC
  技术团队出方案 → design.md + specs
  Gate 2: 客户确认方案 → 锁定交付标准

Phase 3-5: BUILD → VERIFY (内部)
  开发 + 测试

Phase 6: DELIVER
  交付 + 归档
  客户验收对照 proposal 的 Success Criteria 逐项确认
```

**为什么出彩**：客户需求变更的追溯、交付验收的客观标准、减少"你当初不是这么说的"。

---

## 四、场景速查表

| 场景 | 适用度 | 关键 agent_spec 检查点 | 预估收益 |
|------|:---:|------|:---:|
| 量化策略上线 | ⭐⭐⭐⭐⭐ | 数据完整性/参数合规/风控验证/绩效 | 避免实盘损失 |
| 风控规则变更 | ⭐⭐⭐⭐⭐ | 审计日志/回滚方案/影响范围 | 合规审计 |
| 基金产品上线 | ⭐⭐⭐⭐⭐ | 20+ CP 跨系统协调 | 零遗漏 |
| 数据报表生成 | ⭐⭐⭐⭐ | 数据源/交叉验证/异常检测/格式 | 减少人工核对 |
| **官网维护** | ⭐⭐⭐⭐⭐ | 链接/双语/响应式/版本号/性能 | **立刻可用** |
| 技术文档发布 | ⭐⭐⭐⭐ | 版本号/链接/代码示例/拼写 | 减少文档债 |
| 会议决策追踪 | ⭐⭐⭐ | 论证/对比/结论归档 | 决策可追溯 |
| 新人 Onboarding | ⭐⭐⭐⭐ | 15+ CP 标准化流程 | 经验复利 |
| 客户需求管理 | ⭐⭐⭐⭐ | 需求锁定/验收标准/变更追溯 | 减少纠纷 |
| 部署运维 | ⭐⭐⭐⭐⭐ | 健康检查/日志/回滚 | V2.7 已支持 |
| 安全审计 | ⭐⭐⭐⭐ | OWASP/CVE/权限/加密 | 合规 |
| 内容翻译 | ⭐⭐⭐ | 术语一致性/链接/完整度 | 质量保障 |
| 配置变更 | ⭐⭐⭐⭐ | 影响范围/回滚/验证 | 减少事故 |

---

## 五、如何开始：官网维护场景实战模板

### 5.1 创建第一个非代码 Change

```bash
# 1. 创建 change
stdd new website-update-v2.5-hero

# 2. 写 proposal
# Why: 升级官网 Hero 区到 V2.5
# What Changes: Hero 重写 / 竞品对比表 / 中英双语

# 3. 写 agent_spec.yaml
cat > canonical/specs/agent/website-deploy.yaml << 'EOF'
meta:
  task_id: website-deploy
  system: production-web-server
steps:
  - id: CP-1
    description: "所有链接有效"
    action: "find website/ -name '*.html' | xargs grep -oP 'href=\"([^\"]+)\"' | ... "
    assertions:
      - type: exit_code
        expected: 0
  - id: CP-2
    description: "中英双语键值一致"
    action: "node check-i18n.js website/index.html"
    assertions:
      - type: exit_code
        expected: 0
  - id: CP-3
    description: "版本号一致"
    action: "grep -c 'V2.5' website/index.html"
    assertions:
      - type: stdout_contains
        expected: "V2.5"
rollback:
  steps:
    - "cp website/index.html.bak website/index.html"
EOF

# 4. 验证
stdd agent verify website-deploy

# 5. 发布
# 上传 index.html 到服务器

# 6. 归档
stdd archive website-update-v2.5-hero
```

### 5.2 经验库管理

```bash
# 记录官网维护经验
stdd experience add \
  --category pipeline_break \
  --pattern "官网更新后链接失效" \
  --root-cause "外部链接变更未及时发现" \
  --detection-trigger "agent verify CP-1 失败" \
  --fix-template "每次发布前运行 agent verify website-deploy" \
  --language docs \
  --severity medium \
  --tags "website,deploy,link-check"
```

---

## 六、关键原则

1. **Spec 先行，永不跳过**：即使是最小的任务（更新一个链接），也应该先定义"改什么、怎么验证"
2. **验证自动化**：能用 `agent_spec.yaml` 自动检查的，不要依赖人工目视
3. **经验复利**：每次失误都沉淀为经验条目，下次自动加载提醒
4. **文档即流程**：非编程场景中，agent_spec 本身就是 SOP（标准操作流程）
5. **一个 Change 一件事**：不要像 V2.7 开发那样塞 25 项（我们已经付过学费了）

---

> **下一步**：用 STDD 管理 STDD 官网的下一次迭代，建立第一个非代码 Change 的完整闭环。
