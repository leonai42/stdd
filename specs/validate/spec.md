# Capability: VALIDATE — 验证增强

## MODIFIED Requirements

### Requirement: validate 检查 AND 数量上限

validate 命令 SHALL 检查每个 Scenario 的 AND 数量不超过 5 条，超过时产生警告。

#### Scenario: AND 数量合规不产生警告

- **GIVEN** spec 文件的 Scenario 包含 3 条 AND
- **WHEN** 用户执行 `stdd validate`
- **THEN** 系统 SHALL NOT 报告 AND 数量相关警告

#### Scenario: AND 数量超限产生警告

- **GIVEN** spec 文件的 Scenario 包含 6 条 AND
- **WHEN** 用户执行 `stdd validate`
- **THEN** 系统 SHALL 报告"AND 数量 (6) 超过上限 (5)"的警告

### Requirement: trace 使用结构化解析

trace 命令 SHALL 使用逐行分段解析 test-plan.md，而非跨行 DOTALL 正则。

#### Scenario: 标准格式 test-plan 正确解析

- **GIVEN** test-plan.md 格式符合模板规范
- **WHEN** 用户执行 `stdd trace TC-XXX-001`
- **THEN** 系统 SHALL 正确提取 TC-ID、案例标题和预期结果
- **AND** 解析逻辑 SHALL 不依赖跨行正则 DOTALL

#### Scenario: 非标准格式的 test-plan 优雅降级

- **GIVEN** test-plan.md 的格式与模板有偏差（如缺少空行）
- **WHEN** 用户执行 `stdd trace TC-XXX-001`
- **THEN** 系统 SHALL 尽可能匹配 TC-ID
- **AND** 如果无法提取详细信息，SHALL 至少显示"已引用"状态

### Requirement: archive specs 合并冲突检测

archive 合并 specs 时 SHALL 检测目标文件中是否已存在同名 Requirement，存在时警告并询问用户。

#### Scenario: 检测到重复 Requirement

- **GIVEN** specs/ 中已存在 `### Requirement: 用户登录`
- **AND** 待合并的 spec 也包含 `### Requirement: 用户登录`
- **WHEN** 执行 archive 合并
- **THEN** 系统 SHALL 输出冲突警告
- **AND** 系统 SHALL 标注冲突的 Requirement 名称

#### Scenario: 无冲突时正常合并

- **GIVEN** specs/ 中不存在同名 Requirement
- **WHEN** 执行 archive 合并
- **THEN** 系统 SHALL 正常追加或新增 spec 内容
- **AND** 系统 SHALL NOT 输出冲突警告
