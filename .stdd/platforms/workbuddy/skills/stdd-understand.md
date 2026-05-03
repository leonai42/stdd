---
name: stdd-understand
description: STDD Phase 1: 需求理解与确认
version: "1.0"
trigger_keywords: ["stdd-understand", "stdd understand", "spec-driven", "tdd"]
---
# STDD Phase 1: UNDERSTAND — 需求理解与确认

## 阶段目标

将用户需求转化为清晰、可验证、经用户确认的变更提案（proposal.md）。

## 前置条件

- 用户提出了需求或问题描述
- 项目已初始化 STDD（存在 `.stdd/` 目录）

## 执行流程

### Step 1: 问题探索

1. 仔细阅读用户的需求描述
2. 如果需求涉及现有代码，探索相关代码库：
   - 理解当前系统行为
   - 识别问题边界和影响范围
   - 查找已有的相关 spec（`specs/` 目录）
3. 如果有不明确的地方，向用户提问澄清（不要假设）

### Step 2: 读取模板

先读取模板文件：`.stdd/templates/proposal.md`

严格按照模板的章节结构和字段定义起草 proposal。

### Step 3: 起草 proposal

按以下结构生成 draft proposal 并向用户展示：

- **Why**：问题陈述（用户视角，为什么需要这个变更）
- **What Changes**：变更列表（每项一句话）
- **Capabilities**：涉及的能力域
  - Modified Capabilities：修改哪些已有能力
  - New Capabilities：新增哪些能力
- **Impact**：影响范围评估
  - 代码层面：涉及的文件和范围
  - 配置层面：需要改动的配置
  - 基础设施：是否需要新服务/新 API
- **Success Criteria**：可验证的成功条件（checkbox 列表，每个条件能用是/否回答）

### Step 4: 用户确认（强制门）

向用户展示 draft proposal 后，**必须等待用户明确确认**：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD Phase 1: UNDERSTAND — 等待确认
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 变更提案：

  【Why】...
  【What Changes】...
  【Capabilities】...
  【Impact】...
  【Success Criteria】...

⚠️ 请确认以上内容：
  - 范围和边界是否准确？
  - 成功标准是否可验证？
  - 是否有遗漏或需要调整的地方？

👉 确认无误请回复，或提出修改意见。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

如果用户提出修改意见 → 根据反馈修订 proposal → 重新展示等待确认
如果用户确认 → 锁定 proposal，进入 Step 5

**确认前不生成文件。**

### Step 5: 生成终版 proposal.md

用户确认后：
1. 创建 change 目录：`changes/<YYYY-MM-DD>-<name>/`
2. 写入 `proposal.md`
3. 初始化 `.stdd.yaml` 状态文件（phase: understand → completed）
4. 提示用户：Phase 1 完成，可以执行 `Phase 2: SPEC`

## 产出物

- `changes/<date>-<name>/proposal.md` — 经用户确认的变更提案
- `changes/<date>-<name>/.stdd.yaml` — 变更状态文件

## 质量检查

完成前确认：
- [ ] 每个 Success Criteria 可客观验证（能用是/否回答）
- [ ] 每个 Capability 边界清晰
- [ ] Impact 评估覆盖代码、配置、基础设施三个维度
- [ ] 用户已明确确认 proposal 内容

## 下一阶段

Phase 1 确认完成 → 进入 Phase 2: SPEC（规格设计与测试方案）
