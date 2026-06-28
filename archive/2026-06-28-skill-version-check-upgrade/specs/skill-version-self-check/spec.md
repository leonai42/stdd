# skill-version-self-check — 行为规格

> Capability: skill-version-self-check (New)
> Change: skill-version-check-upgrade
> Confidence: high

## REQ-VC-001: 技能文件携带版本元数据并自检

任何 STDD 阶段技能启动时自动比对自身版本与项目 `.stdd/version.yaml`，版本落后时主动告警并引导升级。不阻断执行。

### Scenario: SC-VC-001 — 版本落后告警

- **GIVEN** 项目 `.stdd/version.yaml` 中 `stdd_version: 2.4.0`，当前技能的 frontmatter 中 `stdd_version: 2.9.5`
- **WHEN** AI 执行 Step 0 版本自检
- **THEN** AI SHALL 向用户显示告警消息，包含项目当前版本、技能期望版本、以及 `/stdd-upgrade` 升级建议
- **AND** AI SHALL NOT 阻断后续步骤的执行

### Scenario: SC-VC-002 — 版本一致静默

- **GIVEN** 项目 `.stdd/version.yaml` 中 `stdd_version: 2.9.5`，技能 `stdd_version: 2.9.5`
- **WHEN** AI 执行 Step 0 版本自检
- **THEN** AI SHALL NOT 显示任何版本告警消息

### Scenario: SC-VC-003 — 项目版本更新时静默

- **GIVEN** 项目 `.stdd/version.yaml` 中 `stdd_version: 3.0.0`，技能 `stdd_version: 2.9.5`
- **WHEN** AI 执行 Step 0 版本自检
- **THEN** AI SHALL NOT 显示版本告警（技能落后于项目属于正常回滚或未升级场景）

### Scenario: SC-VC-004 — 版本格式容错

- **GIVEN** 项目版本为 `v2.4`（带前缀 + 两段格式），技能版本为 `2.9.5`（无前缀 + 三段格式）
- **WHEN** AI 执行版本比较
- **THEN** AI SHALL 正确识别 `v2.4` < `2.9.5`（去除 `v`/`V` 前缀，短版本号补零为 `2.4.0`，逐段比较）

### Scenario: SC-VC-005 — 非 STDD 项目静默跳过

- **GIVEN** 项目根目录不存在 `.stdd/` 目录
- **WHEN** AI 执行 Step 0 版本自检
- **THEN** AI SHALL 静默跳过，不显示任何版本相关消息

### Scenario: SC-VC-006 — 锁定项目告警

- **GIVEN** 项目 `.stdd/version.yaml` 中 `stdd_version: 2.4.0` 且 `locked: true`，技能 `stdd_version: 2.9.5`
- **WHEN** AI 执行 Step 0 版本自检
- **THEN** AI SHALL 显示版本落后告警，并额外说明"项目已锁定在版本 2.4.0，使用 `stdd upgrade --unlock` 解锁后再升级"
- **AND** AI SHALL NOT 阻断后续步骤
