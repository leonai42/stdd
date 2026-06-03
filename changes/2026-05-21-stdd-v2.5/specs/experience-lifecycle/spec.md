# Spec: experience-lifecycle — 经验库生命周期

> Capability: experience-lifecycle
> Priority: P0 · 2d · CLI + 数据模型

## Requirement: 经验状态机

经验条目 SHALL 支持 5 种生命周期状态，按规则自动或手动迁移。

### Scenario: 新经验创建为 discovered

GIVEN Phase 5 发现一个新的失败模式
WHEN AI 调用 `stdd experience add` 创建经验
THEN 经验条目 SHALL 以 `lifecycle_state: discovered` 创建
AND `.experience-index.yaml` 的 `by_lifecycle.discovered` SHALL 包含该经验 ID

### Scenario: 手动验证经验

GIVEN 一条 `discovered` 状态的经验 EXP-0001
WHEN 用户执行 `stdd experience verify EXP-0001`
THEN EXP-0001 的 `lifecycle_state` SHALL 变更为 `verified`
AND `.experience-index.yaml` 的索引 SHALL 同步更新

### Scenario: 自动提升为 verified

GIVEN 一条 `discovered` 状态的经验，其 `occurrences >= 2`
AND 其 `confidence >= 0.7`
WHEN Phase 5 触发经验状态检查
THEN 该经验 SHALL 自动提升为 `verified`
AND 提升事件 SHALL 记录到 test-report.md 的"经验库更新"章节

### Scenario: 沉淀为 deposited

GIVEN 一条 `verified` 状态的经验，其 `occurrences >= 3`
AND 其 `confidence >= 0.8`
WHEN Phase 5 触发经验状态检查
THEN 该经验 SHALL 自动提升为 `deposited`
AND 状态变更原因 SHALL 记录到经验文件的 body 中

### Scenario: 导出为 shared

GIVEN 一条 `verified` 或 `deposited` 状态的经验
WHEN 用户执行 `stdd experience export EXP-0001 --publish`
THEN 经验 SHALL 脱敏后导出为可发布的格式
AND 其 `lifecycle_state` SHALL 变更为 `shared`
AND 导出文件 SHALL 不包含路径、IP、域名、业务专有名词

### Scenario: 社区融合为 merged

GIVEN 一条 `shared` 状态的经验被 3+ 个其他项目 pull 并标记 useful
WHEN CI job 同步社区投票数据
THEN 该经验的 `lifecycle_state` SHALL 变更为 `merged`
AND 经验 SHALL 被标记为官方候选

### Scenario: 废弃经验

GIVEN 一条任意状态的经验
WHEN 用户执行 `stdd experience retire EXP-0001 --reason "Python 3.12 修复了此问题"`
THEN 其 `lifecycle_state` SHALL 变更为 `retired`
AND `reason` 字段 SHALL 记录废弃原因
AND retired 经验在 `experience list` 中默认不显示（`--all` 可查看）

### Scenario: 状态迁移拒绝

GIVEN 一条 `discovered` 状态的经验
WHEN 用户执行 `stdd experience deposit EXP-0001`
THEN CLI SHALL 返回错误："experience EXP-0001 is in state 'discovered', must be 'verified' before 'deposited'"
AND 状态不改变
