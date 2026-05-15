# Capability: long-range-execution

## MODIFIED Requirements

### Requirement: 预授权后 SHALL 配置 Claude Code 实际权限

长程模式的概念性预授权不足以消除 Claude Code 的工具权限提示。确认预授权后，系统 SHALL 将授权落地为实际的 Claude Code 权限配置。

#### Scenario: 预授权确认后配置 Claude Code 权限

- **GIVEN** 用户已确认一次性预授权清单
- **WHEN** 系统执行 Step 7a.5
- **THEN** 系统 SHALL 使用 Edit 工具修改 `.claude/settings.local.json`
- **AND** SHALL 在 `permissions.allow` 数组中添加 pytest/ruff/python/pip/git 等开发工具 Bash 规则
- **AND** SHALL 添加 Write/Edit 规则覆盖 changes/、app/、tests/ 等开发目录

### Requirement: 长程模式阶段 SHALL 自动衔接

长程模式下，Phase 3→4→5 SHALL 在同一轮次内自动衔接，不等待用户输入。

#### Scenario: Slice 完成后自动进入 Build

- **GIVEN** `.stdd.yaml` 中 `long_range.mode == "full_auto"`
- **AND** Phase 3 Slice 已完成所有切片规划和 tasks.md 写入
- **WHEN** Slice 阶段完成
- **THEN** 系统 SHALL 在同一轮次内立即自动调用 `stdd-build` skill
- **AND** SHALL NOT 等待用户输入

#### Scenario: Build 完成后自动进入 Verify

- **GIVEN** `.stdd.yaml` 中 `long_range.mode == "full_auto"`
- **AND** Phase 4 Build 已完成所有切片的 RED→GREEN→REFACTOR
- **WHEN** Build 阶段最后一个切片完成
- **THEN** 系统 SHALL 在同一轮次内立即自动调用 `stdd-verify` skill
- **AND** SHALL NOT 等待用户输入

### Requirement: 长程模式 SHALL 遵循无交互运行协议

长程模式下，Build 和 Verify 阶段 SHALL 遵循专门的无交互运行协议。

#### Scenario: Build 阶段无交互执行

- **GIVEN** 长程模式已启用且 `.stdd.yaml` 中 `long_range.mode == "full_auto"`
- **AND** 系统处于 Phase 4 Build
- **WHEN** 切片正常执行且无降级条件触发
- **THEN** 系统 SHALL NOT 使用 AskUserQuestion
- **AND** SHALL 每个切片完成后仅输出 1 行进度信息
- **AND** SHALL 仅在触发降级条件（连续3次修复失败/通过率<95%/安全问题）时暂停
