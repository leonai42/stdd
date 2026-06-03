# STDD V2.5 测试方案

> 版本：V1.0
> 创建日期：2026-05-21
> 对应 Spec：8 个 Capability，52 Scenarios

## 一、测试策略

- **单元测试**（pytest）：CLI 命令的输入/输出验证，数据模型的状态转换正确性
- **集成测试**（pytest）：CLI + 文件系统的完整链路
- **技能验证**（目视）：AI 读取 skill 文件后的行为是否正确（无法自动化）

## 二、详细测试案例

### 功能 1：experience-lifecycle（经验生命周期）

对应 Spec：experience-lifecycle

| TC-ID | Capability | Scenario | 类型 | 验证方法 |
|-------|-----------|----------|------|---------|
| TC-EXP-LC-001 | experience-lifecycle | 新经验创建为 discovered | 单元 | `experience add` → 断言 lifecycle_state=discovered + 索引包含 |
| TC-EXP-LC-002 | experience-lifecycle | 手动验证经验 | 单元 | `experience add` → `experience verify` → 断言 lifecycle_state=verified |
| TC-EXP-LC-003 | experience-lifecycle | 自动提升为 verified | 单元 | 创建 occurrences=2, confidence=0.7 的经验 → 触发状态检查 → 断言 verified |
| TC-EXP-LC-004 | experience-lifecycle | 沉淀为 deposited | 单元 | 创建 verified + occurrences=3 + confidence=0.8 → 触发状态检查 → 断言 deposited |
| TC-EXP-LC-005 | experience-lifecycle | 导出为 shared | 集成 | verified 经验 → `experience export --publish` → 断言 state=shared + 脱敏输出 |
| TC-EXP-LC-006 | experience-lifecycle | 废弃经验 | 单元 | 任意状态 → `experience retire --reason "..."` → 断言 state=retired + reason 字段 |
| TC-EXP-LC-007 | experience-lifecycle | retired 默认不显示 | 单元 | 创建 retired 经验 → `experience list` → 断言不包含 → `experience list --all` → 断言包含 |
| TC-EXP-LC-008 | experience-lifecycle | 状态迁移拒绝 | 单元 | discovered 经验 → `experience deposit` → 断言返回错误 + 状态不变 |
| TC-EXP-LC-009 | experience-lifecycle | 索引同步更新 | 单元 | `experience verify` → 断言 .experience-index.yaml 的 by_lifecycle 已更新 |

### 功能 2：ci-check-enhanced（CI 检查增强）

对应 Spec：ci-check-enhanced

| TC-ID | Capability | Scenario | 类型 | 验证方法 |
|-------|-----------|----------|------|---------|
| TC-CI-ENH-001 | ci-check-enhanced | 正常范围检测 | 单元 | `ci check-scope` → 断言 PASS + 退出码 0 |
| TC-CI-ENH-002 | ci-check-enhanced | 检测到范围蔓延 | 单元 | `ci check-scope` with 超范围文件 → 断言 WARN + 退出码 0 |
| TC-CI-ENH-003 | ci-check-enhanced | proposal 无 capability 声明 | 单元 | 无 STDD-MARKER 的 proposal → 断言 SKIP |
| TC-CI-ENH-004 | ci-check-enhanced | 覆盖正常 | 单元 | mock coverage.json 90% → `ci check-coverage` → 断言 PASS |
| TC-CI-ENH-005 | ci-check-enhanced | 覆盖不足 | 单元 | mock coverage.json 62% → `ci check-coverage` → 断言 FAIL + 退出码 1 |
| TC-CI-ENH-006 | ci-check-enhanced | 无 coverage 数据 | 单元 | 无 coverage.json → `ci check-coverage` → 断言 SKIP |
| TC-CI-ENH-007 | ci-check-enhanced | 契约一致 | 单元 | 字段匹配的 spec → `ci check-contracts` → 断言 PASS |
| TC-CI-ENH-008 | ci-check-enhanced | 契约断层 | 单元 | 字段不匹配 → `ci check-contracts` → 断言 FAIL + 错误信息含字段名 |
| TC-CI-ENH-009 | ci-check-enhanced | 无跨 capability 引用 | 单元 | 单 capability change → `ci check-contracts` → 断言 SKIP |
| TC-CI-ENH-010 | ci-check-enhanced | check-failures 全量聚合 | 集成 | `ci check-failures` → 断言 7 段检查全部执行 + 汇总行 |

### 功能 3：session-resume（跨 Session 状态恢复）

对应 Spec：session-resume

| TC-ID | Capability | Scenario | 类型 | 验证方法 |
|-------|-----------|----------|------|---------|
| TC-SR-001 | session-resume | 写入恢复上下文 | 单元 | 更新 .stdd.yaml → 断言 4 字段写入正确 |
| TC-SR-002 | session-resume | 向后兼容 | 单元 | 读取 V2.4 格式 .stdd.yaml → 断言新字段为 null + 不报错 |
| TC-SR-003 | session-resume | 阶段切换时自动更新 | 集成 | 模拟阶段切换 → 断言 resume_context 刷新 |
| TC-SR-004 | session-resume | 读取恢复上下文 | 单元 | 读取含恢复字段的 .stdd.yaml → 断言状态解析正确 |

### 功能 4：community-experience-pool（社区经验共享池）

对应 Spec：community-experience-pool

| TC-ID | Capability | Scenario | 类型 | 验证方法 |
|-------|-----------|----------|------|---------|
| TC-COM-001 | community-experience-pool | 成功下载经验包 | 集成 | `experience pull python` → mock HTTP → 断言解压 + 合并索引 |
| TC-COM-002 | community-experience-pool | 经验包不存在 | 单元 | `experience pull nonexistent` → 断言错误 + 退出码 1 |
| TC-COM-003 | community-experience-pool | 经验去重 | 集成 | 本地已有 EXP-0001 → pull 含相同 ID 的包 → 断言 SKIP + 本地不变 |
| TC-COM-004 | community-experience-pool | 新经验包含投票字段 | 单元 | 创建经验 → 断言 frontmatter 含 community_votes_* + adoption_count |
| TC-COM-005 | community-experience-pool | 自动脱敏 | 单元 | 经验含路径/IP/域名 → export → 断言已替换为占位符 |
| TC-COM-006 | community-experience-pool | 跳过脱敏 | 单元 | `export --no-sanitize` → 断言内容不变 + 警告消息 |
| TC-COM-007 | community-experience-pool | 发布到社区 | 集成 | `export --publish` → 断言 lifecycle_state→shared + 打包输出 |
| TC-COM-008 | community-experience-pool | 主源超时自动 fallback | 集成 | mock GitHub 超时 → `experience pull python` → 断言 fallback 到 Gitee + 输出 [FALLBACK] |
| TC-COM-009 | community-experience-pool | 所有源失败 | 单元 | mock 全部 registry 不可达 → 断言 "all registries unreachable" + 退出码 1 |
| TC-COM-010 | community-experience-pool | 投票数据同步 | 集成 | mock 社区投票数据 → `experience pull python` → 断言本地 votes 字段更新 |
| TC-COM-011 | community-experience-pool | curate pull 拉取全量 | 集成 | `experience curate pull` → mock HTTP 多包下载 → 断言解压到 inbox + 统计报告 |
| TC-COM-012 | community-experience-pool | curate deduplicate 自动合并 | 单元 | inbox 含相似度 >80% 的两条经验 → 断言自动合并 + tags 并集 + occurrences 累加 |
| TC-COM-013 | community-experience-pool | deduplicate 相似度阈值标记 | 单元 | inbox 含相似度 60-80% 的经验 → 断言标记"待人工确认" + 输出详情 |
| TC-COM-014 | community-experience-pool | curate review 逐条审核 | 单元 | mock 交互输入 a/e/m/r/s → 断言 curated 标记 + reject 原因写入 |
| TC-COM-015 | community-experience-pool | curate pack 打包发布 | 集成 | approved 经验 → `experience curate pack python` → 断言 tar.gz + index + frontmatter 字段 |

### 功能 5：parallel-slice-guide（并行切片指南）

对应 Spec：parallel-slice-guide

| TC-ID | Capability | Scenario | 类型 | 验证方法 |
|-------|-----------|----------|------|---------|
| TC-PSG-001 | parallel-slice-guide | skill 文件含并行策略 | — | 目视检查 build.md 包含 parallel_group 执行指南 |

> parallel-slice-guide 是纯 skill 增强，无法用 pytest 验证。实际效果在 AI 执行时体现。

### 功能 6：gate-file-confirm（Gate 文件确认）

对应 Spec：gate-file-confirm

| TC-ID | Capability | Scenario | 类型 | 验证方法 |
|-------|-----------|----------|------|---------|
| TC-GF-001 | gate-file-confirm | CLI 确认 Gate 1 | 单元 | `gate approve` → 断言 .stdd.yaml 写入 confirmed_at |
| TC-GF-002 | gate-file-confirm | 重复确认幂等 | 单元 | 已确认 → `gate approve` → 断言 not modified |
| TC-GF-003 | gate-file-confirm | Gate 顺序校验 | 单元 | 跨过 Gate 1 确认 Gate 2 → 断言错误 + 退出码 1 |
| TC-GF-004 | gate-file-confirm | 无效 Gate 编号 | 单元 | `gate approve --gate 4` → 断言错误 |
| TC-GF-005 | gate-file-confirm | 文件 token 确认 | 集成 | 创建 GATE2_APPROVED → `stdd status` → 断言 Gate 2 已确认 |
| TC-GF-006 | gate-file-confirm | 文件 token 与 CLI 等效 | 单元 | 文件确认后 → `gate approve` → 断言 "already confirmed" |
| TC-GF-007 | gate-file-confirm | 配置化确认通道 | 单元 | gates.yaml channels=[file_token,cli] → 断言 dialog 不启用 |

### 功能 7：extract-proposal-extended（proposal 扩展提取）

对应 Spec：extract-proposal-extended

| TC-ID | Capability | Scenario | 类型 | 验证方法 |
|-------|-----------|----------|------|---------|
| TC-EPE-001 | extract-proposal-extended | 提取 Constraints | 单元 | `extract-proposal --format json` → 断言 constraints 字段 |
| TC-EPE-002 | extract-proposal-extended | 提取 Stakeholders | 单元 | `extract-proposal --format json` → 断言 stakeholders 字段 |
| TC-EPE-003 | extract-proposal-extended | 提取 RiskAreas（结构化） | 单元 | `extract-proposal --format json` → 断言 risk_areas[0] 含 capability+risk |
| TC-EPE-004 | extract-proposal-extended | 提取 NonGoals | 单元 | `extract-proposal --format json` → 断言 non_goals 字段 |
| TC-EPE-005 | extract-proposal-extended | 新字段不存在时不报错 | 单元 | V2.4 格式 proposal → 断言新字段为空数组 + 退出码 0 |
| TC-EPE-006 | extract-proposal-extended | 旧字段不变 | 单元 | 断言 why/what_changes/capabilities/success_criteria 与 V2.4 一致 |
| TC-EPE-007 | extract-proposal-extended | 模板含新字段标记 | 单元 | `stdd new` → 断言生成模板含 Constraints 等段落 |

### 功能 8：non-code-change-support（非代码类 Change 支持）

对应 Spec：non-code-change-support

| TC-ID | Capability | Scenario | 类型 | 验证方法 |
|-------|-----------|----------|------|---------|
| TC-NCC-001 | non-code-change-support | 经验自动标记 project_type | 单元 | 创建经验（python change） → 断言 project_type=python |
| TC-NCC-002 | non-code-change-support | 混合项目标记 | 单元 | 创建经验（static_site change） → 断言 project_type=static_site |
| TC-NCC-003 | non-code-change-support | 纯文档项目 | 单元 | 创建经验（docs change） → 断言 project_type=docs |
| TC-NCC-004 | non-code-change-support | project_type 过滤加载 | 单元 | 加载 static_site 经验 → 断言 python 经验被过滤 |
| TC-NCC-005 | non-code-change-support | project_type 向后兼容 | 单元 | 加载无 project_type 的经验 → 断言正常加载（通配） |

> verify.md 的非代码检查清单是 AI 行为指令，目视验证。

## 三、测试执行矩阵

| 功能模块 | 单元测试 | 集成测试 | 技能目视 | TC 合计 |
|---------|---------|---------|---------|--------|
| experience-lifecycle | 7 | 2 | — | 9 |
| ci-check-enhanced | 9 | 1 | — | 10 |
| session-resume | 3 | 1 | — | 4 |
| community-experience-pool | 8 | 7 | — | 15 |
| parallel-slice-guide | — | — | 1 | 1 |
| gate-file-confirm | 6 | 1 | — | 7 |
| extract-proposal-extended | 7 | — | — | 7 |
| non-code-change-support | 5 | — | 2 | 7 |
| **合计** | **45** | **12** | **3** | **60** |

## 四、回归风险矩阵

| 风险区域 | 改动 | 已有回归保护 | 风险等级 |
|----------|------|-------------|---------|
| experience.py 现有命令 | 新增子命令 verify/deposit/retire | 13 个已有测试 | 🟢 低 |
| ci.py 现有 check-failures | 扩展检查注册表 | 14 个已有测试 | 🟡 中 |
| extract_proposal.py 现有逻辑 | 新增 4 字段解析 | 7 个已有测试 | 🟢 低 |
| 现有 15 个 CLI 命令 | 无改动 | 154 个已有测试 | 🟢 零 |
| state.py（.stdd.yaml 读写） | 新增字段读取 | E2E 测试 | 🟡 中 |
