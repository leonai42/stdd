# Capability: config-system

## MODIFIED Requirements

### Requirement: Typecheck 配置补完

`quality.yaml` 中的 `quality.typecheck` SHALL 包含可实际执行的类型检查命令，而非 null。

#### Scenario: typecheck 配置为非 null 值

- **GIVEN** `.stdd/config.d/quality.yaml` 存在
- **WHEN** Phase 5 Step 1d 读取 `quality.typecheck` 配置
- **THEN** `quality.typecheck` SHALL 为字符串值（如 `"mypy app/"`）
- **AND** 该命令 SHALL 可在 Python 项目中直接执行

---

### Requirement: Critical Paths 配置补完

`quality.yaml` 中的 `quality.e2e.critical_paths` SHALL 包含至少一个示例 E2E 测试路径，使 Phase 5 的 E2E 关键路径检查有可执行的默认目标。

#### Scenario: critical_paths 为非空数组

- **GIVEN** `.stdd/config.d/quality.yaml` 存在
- **WHEN** Phase 5 Step 1f 读取 `quality.e2e.critical_paths` 配置
- **THEN** `critical_paths` SHALL 为非空数组
- **AND** 默认值 SHALL 包含示例路径（如 `"tests/e2e/test_critical_flow.py"`）

---

### Requirement: Source Directory 配置补完

`project.yaml` SHALL 包含 `project.source_dir` 字段，指明项目源码根目录，供覆盖率诊断和 lint 检查使用。

#### Scenario: source_dir 字段存在

- **GIVEN** `.stdd/config.d/project.yaml` 存在
- **WHEN** Phase 5 Step 1b 覆盖率工具需要限定变更文件范围
- **THEN** `project.source_dir` SHALL 为有效字符串（如 `"app"`）
- **AND** 该字段 SHALL 与 `quality.coverage.scope: changed_files_only` 配合使用

---

### Requirement: 长程模式降级配置

`long_range.yaml` SHALL 包含 `degradation` 配置段，明确定义降级触发条件（连续修复失败次数、测试通过率阈值、安全检查开关）。

#### Scenario: degradation 配置段存在且完整

- **GIVEN** `.stdd/config.d/long_range.yaml` 存在
- **WHEN** Phase 4 或 Phase 5 长程模式运行中检测异常
- **THEN** `degradation.max_consecutive_failures` SHALL 定义连续修复失败上限（默认 3）
- **AND** `degradation.pass_rate_threshold` SHALL 定义测试通过率最低阈值（默认 0.95）
- **AND** `degradation.safety_check` SHALL 定义安全拦截开关（默认 true）
