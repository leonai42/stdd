---
name: stdd-deliver
description: "STDD Phase 6: 交付 — 归档变更、合并规范、创建版本标签"
stdd_version: "2.9.6"
---
# STDD Phase 6: DELIVER — 交付

## 阶段目标

归档变更、合并规范、创建版本标签。

### Step 0: 版本自检

先读取并执行版本自检步骤：`.stdd/skills/_shared/version-check.md`

> 检查项目 `.stdd/version.yaml` 与技能版本是否一致。落后时告警但不阻断执行。

---

## 前置条件

- Phase 5 已完成（test-report.md 经用户确认）
- `.stdd.yaml` 中 `phases.verify.confirmed_at` 已设置

## 执行流程

### Step 1: 归档变更

**V2.9 轻量模式**：如果 `.stdd.yaml` 中 `mode: lightweight`，将变更追加到当前批次目录 `changes/_batch/<id>/items/`，而非独立归档。

**标准模式**：
1. 将 `changes/<date>-<name>/` 移动到 `archive/<date>-<name>/`
2. 更新 `.stdd.yaml`（status: archived）

### Step 2: 合并规范

**V2.9: Canonical YAML 合并**（先于 Human View 合并）：

1. 将 `changes/<change>/canonical/proposals/<change>.yaml` 合并到 `canonical/proposals/`
2. 将各 capability 的 `agent_spec.yaml` 合并到 `canonical/specs/agent/`
3. 执行 `python bin/stdd canon verify <change>` 验证双轨一致性
4. 更新 `.canon-index.yaml` 索引

**Human View 合并**：

对于变更中的每个 capability spec：

1. 如果是 **NEW** capability：
   - 复制 `changes/<date>-<name>/specs/<capability>/spec.md` → `specs/<capability>/spec.md`
   - 如果 `specs/<capability>/` 已存在，合并新增的 Requirements

2. 如果是 **MODIFIED** capability：
   - 将 changes 中的 spec 新增/修改的 Requirements 合并到 `specs/<capability>/spec.md`
   - 保留合并记录（在 spec 文件中标注变更日期和 change 名称）

### Step 2.5: 代码结构摘要合并（V2.9）

执行 `python bin/stdd structure merge <change>` 将本 change 的 delta 合并到项目索引。

### Step 2.8: 经验自动上传（V2.9.6）

在完成归档和规范合并后，自动将本次 change 中沉淀的经验上传到社区 git 库。

1. **扫描待上传经验**：执行 `python bin/stdd experience list --lifecycle deposited --format json`
   - 筛选 `lifecycle_state == "deposited"` 且 `source_change` 包含当前 change 名称的经验
2. **逐条上传**：对每条待上传经验执行 `python bin/stdd experience share <EXP-ID>`
   - 成功 → 经验 `lifecycle_state` 自动更新为 `shared`
   - 失败 → 记录错误原因，继续处理下一条
3. **结果汇总**：
   - 全部成功：`✅ N 条经验已上传到社区`
   - 部分失败：`⚠️ N 条上传成功, M 条失败（可稍后手动 retry: stdd experience share <EXP-ID>）`
   - 无经验：跳过此步骤，输出 `ℹ️ 本次无新增经验`

**降级策略**：上传失败不阻断 DELIVER 流程。失败的 EXP-ID 记录在完成摘要中，提示用户手动重试。

### Step 3: 版本标记

1. 展示建议的 commit message 和 tag 名称，等待用户确认
2. 用户确认后执行 git 操作（不自动 push，由用户决定何时 push）

### Step 4: 部署（如需要）

如果项目有部署流程：
1. 读取项目的部署文档或配置
2. 按部署流程执行
3. 如部署需要用户操作，指导用户完成

## 产出物

- `archive/<date>-<name>/` — 归档的完整变更记录
- 更新后的 `specs/<capability>/spec.md` — 合并后的主规范
- Git commit + tag

## 质量检查

- 所有变更文件已提交
- specs 已合并更新，无遗漏
- Git tag 已创建
- `.stdd.yaml` 状态已更新为 archived

## 完成

Phase 6 完成后，整个 STDD 流程结束：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STDD 流程完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 变更已归档: archive/<date>-<name>/
✅ 规范已合并: specs/
✅ 经验上传: <N 条上传成功 / 无新增经验 / ⚠️ M 条失败>
✅ 版本标记: <tag>

📁 归档目录包含完整的：
  - proposal.md / design.md
  - specs / test-plan.md
  - tasks.md / test-report.md
  - design-adjustments.md (如有)

🚀 可以 push 到远程仓库进行部署。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
