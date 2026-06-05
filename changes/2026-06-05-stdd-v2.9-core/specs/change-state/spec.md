# change-state — .stdd.yaml 模式标记扩展

<!-- confidence: high -->
<!-- evidence: proposal.md ".stdd.yaml 增加 mode / task_type / complexity_score 字段" -->

## Requirement: 模式字段扩展

STATE-REQ-001: `.stdd.yaml` SHALL 支持 mode、task_type、complexity_score 等新字段。

### Scenario: lightweight 变更的 .stdd.yaml

<!-- confidence: high -->
GIVEN Gate 1 用户确认了 lightweight 模式
WHEN 写入 `.stdd.yaml`
THEN SHALL 包含以下字段：
```yaml
mode: lightweight
task_type: code
complexity_score: 2
score_confidence: preliminary
mode_confirmed_by: user
mode_confirmed_at: "<timestamp>"
```

### Scenario: standard 变更的 .stdd.yaml

<!-- confidence: high -->
GIVEN Gate 1 用户确认了 standard 模式
WHEN 写入 `.stdd.yaml`
THEN SHALL 包含 `mode: standard`
AND SHALL 包含 `task_type: code`

### Scenario: 非代码任务的 .stdd.yaml

<!-- confidence: medium -->
GIVEN Gate 1 用户确认了 lightweight 模式
AND 任务类型为 documentation
WHEN 写入 `.stdd.yaml`
THEN SHALL 包含 `mode: lightweight`
AND SHALL 包含 `task_type: documentation`

## Requirement: 向后兼容

STATE-REQ-002: 旧 `.stdd.yaml` 文件（无 mode 字段）SHALL 被视为 standard 模式。

### Scenario: 读取旧格式 .stdd.yaml

<!-- confidence: high -->
GIVEN `.stdd.yaml` 无 mode 字段
AND 文件格式为 V2.8 旧格式
WHEN STDD CLI 或 Skill 读取该文件
THEN SHALL 默认 `mode: standard`
AND 不影响现有功能
