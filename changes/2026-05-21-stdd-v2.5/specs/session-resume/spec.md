# Spec: session-resume — 跨 Session 状态恢复

> Capability: session-resume
> Priority: P0 · 0.5d · 数据模型

## Requirement: .stdd.yaml 恢复上下文字段

`.stdd.yaml` SHALL 支持 4 个新字段，使 Agent 跨 session 后可在 1 轮内恢复上下文。

### Scenario: 写入恢复上下文

GIVEN 当前正在执行 Slice 3/5，刚完成 RED phase
WHEN AI 更新 `.stdd.yaml`
THEN `resume_context` SHALL 包含当前进度的自然语言描述
AND `active_slice` SHALL 包含当前切片标识
AND `last_action` SHALL 包含最后执行的操作描述
AND `last_modified` SHALL 为 ISO 8601 时间戳

### Scenario: 读取恢复上下文

GIVEN `.stdd.yaml` 包含 `resume_context: "Slice 3/5 payment，RED 完成，等待 GREEN"`
WHEN 新 AI session 读取 `.stdd.yaml`
THEN AI SHALL 在 1 轮内理解当前进度
AND 无需翻找 change 目录下的具体文件即可判断下一步动作

### Scenario: 向后兼容

GIVEN 一个 V2.4 格式的 `.stdd.yaml`（无 resume_context 等字段）
WHEN `stdd status` 读取该文件
THEN 新字段 SHALL 默认为 null
AND 现有功能不受影响

### Scenario: 阶段切换时自动更新

GIVEN Phase 4 BUILD 完成，进入 Phase 5 VERIFY
WHEN AI 更新 `.stdd.yaml` 的 `current_phase: verify`
THEN `resume_context` 和 `last_action` SHALL 同时更新为新的阶段上下文
AND `last_modified` SHALL 刷新为当前时间
