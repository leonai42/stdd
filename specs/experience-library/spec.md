# Capability: 自学习经验库 (experience-library)

## ADDED Requirements

### Requirement: 经验数据存储

系统 SHALL 在 `.stdd/experiences/` 目录中以 YAML frontmatter + Markdown body 格式存储经验条目，并通过自动维护的索引文件支持快速查找。

#### Scenario: 创建经验条目

- **GIVEN** `.stdd/experiences/` 目录已存在
- **WHEN** 用户或 AI 执行 `stdd experience add --category cascading_errors --pattern "async 函数裸 except 遗漏 CancelledError"`
- **THEN** 系统 SHALL 在 `.stdd/experiences/` 下创建 `EXP-YYYY-NNNN.md` 文件
- **AND** 文件 SHALL 包含完整的 YAML frontmatter（experience_id, category, pattern, root_cause, detection_trigger, fix_template）
- **AND** experience_id SHALL 按年份和自增序号自动生成（如 EXP-2026-0001）
- **AND** 系统 SHALL 自动更新 `.experience-index.yaml`

#### Scenario: 经验索引自动维护

- **GIVEN** 已有至少 2 条经验条目
- **WHEN** 新增或修改一条经验
- **THEN** `.experience-index.yaml` SHALL 自动更新 by_category / by_language / by_lifecycle / by_severity 分组
- **AND** `last_id` 和 `total` 字段 SHALL 保持正确

#### Scenario: 经验自动记录（Phase 5 触发）

- **GIVEN** Phase 5 VERIFY 的 11 类失败检查已完成
- **AND** 发现一个新的失败模式，与已有经验不匹配
- **WHEN** AI 执行 verify.md Step 3.5
- **THEN** AI SHALL 创建新的 EXP 文件，lifecycle_state 设为 `discovered`
- **AND** 自动填充 category / pattern / root_cause / detection_trigger / fix_template
- **AND** occurrences 初始化为 1

#### Scenario: 经验重现升级

- **GIVEN** 某经验条目 EXP-2026-0001 的 occurrences 为 2，lifecycle_state 为 `discovered`
- **WHEN** 同一项目的新 change 中再次触发相同失败模式
- **THEN** 系统 SHALL 将 occurrences 增加到 3
- **AND** 当 occurrences >= 3 时 SHALL 自动将 lifecycle_state 升级为 `verified`
- **AND** 更新 last_seen 为当前日期

#### Scenario: 索引从文件重建

- **GIVEN** `.experience-index.yaml` 被意外删除
- **WHEN** 执行 `stdd experience list --format json`
- **THEN** 系统 SHALL 扫描所有 EXP 文件的 YAML frontmatter
- **AND** SHALL 重建完整的 `.experience-index.yaml`

### Requirement: 经验 CLI 命令组

系统 SHALL 提供 `stdd experience` 命令组用于管理经验库。

#### Scenario: 列出经验并过滤

- **GIVEN** 经验库中有 Python 和 Go 两类经验
- **WHEN** 用户执行 `stdd experience list --language python --severity high`
- **THEN** 系统 SHALL 仅显示匹配 Python + high severity 的经验
- **AND** 默认以 table 格式输出，支持 `--format json` 和 `--format yaml`

#### Scenario: 添加经验（手动）

- **GIVEN** 用户想手动记录一条经验
- **WHEN** 执行 `stdd experience add --category scope_creep --pattern "超出计划文件改动" --severity medium --language python --tags "refactor,cleanup"`
- **THEN** 系统 SHALL 创建经验文件并更新索引
- **AND** 如果 category 不在 11 类合法值内 SHALL 拒绝并提示有效值

#### Scenario: 统计概览

- **GIVEN** 经验库中有 15 条经验，分布在 4 个 category 中
- **WHEN** 执行 `stdd experience stats`
- **THEN** 系统 SHALL 显示按 category / language / severity / lifecycle 的分布
- **AND** 显示总 occurrence 数和平均 confidence

#### Scenario: 导出脱敏

- **GIVEN** 经验条目中包含文件路径 `/home/user/project/app/main.py`、IP `192.168.1.1`、域名 `api.internal.com`
- **WHEN** 执行 `stdd experience export --format json`
- **THEN** 系统 SHALL 将路径替换为 `<project>/<module>` 占位符
- **AND** SHALL 将 IP 替换为 `<ip-address>` 占位符
- **AND** SHALL 将域名替换为 `<domain>` 占位符
- **AND** 使用 `--no-sanitize` 时 SHALL 保留原始内容

#### Scenario: 社区拉取（V2.5 placeholder）

- **GIVEN** V2.4 版本
- **WHEN** 执行 `stdd experience pull python-pack`
- **THEN** 系统 SHALL 输出提示信息，说明此功能将在 V2.5 正式支持

### Requirement: 经验库配置

系统 SHALL 通过 `.stdd/config.d/experience.yaml` 提供经验库行为配置。

#### Scenario: 读取经验库配置

- **GIVEN** `.stdd/config.d/experience.yaml` 配置了 `auto_record.enabled: true` 和 `lifecycle.verified_threshold: 3`
- **WHEN** Phase 5 AI 或 CLI 读取配置
- **THEN** 经验自动记录 SHALL 按 `auto_record.enabled` 决定是否启用
- **AND** 验证阈值 SHALL 按 `lifecycle.verified_threshold` 的值执行

### Requirement: BUILD 阶段经验加载

系统 SHALL 在 Phase 4 BUILD 开始时自动加载与当前切片匹配的经验。

#### Scenario: 按语言和标签匹配经验

- **GIVEN** 项目语言为 Python，当前切片标签为 ["async", "redis"]
- **AND** 经验库中有 EXP-0001（Python, tags: [async]）和 EXP-0002（Go, tags: [redis]）
- **WHEN** AI 执行 build.md Step 0.5
- **THEN** AI SHALL 加载 EXP-0001（语言匹配 + 标签交集）
- **AND** SHALL 不加载 EXP-0002（语言不匹配）

#### Scenario: 经验检查点植入

- **GIVEN** 已加载匹配经验 EXP-0001（pattern: "async 函数裸 except 遗漏 CancelledError"）
- **WHEN** AI 在 RED 阶段编写测试或 GREEN 阶段编写实现代码
- **THEN** AI SHALL 在相关代码处植入注释检查点 `# STDD-EXP-0001: 注意 CancelledError 处理`
- **AND** Phase 5 VERIFY 时 SHALL 优先检查此历史经验是否被违反

### Requirement: VERIFY 阶段经验集成

系统 SHALL 在 Phase 5 test-report 中包含经验库更新章节。

#### Scenario: test-report 包含经验更新

- **GIVEN** 当前 change 触发了 2 条已有经验（occurrences +1）并新发现 1 条经验
- **WHEN** AI 生成 test-report.md
- **THEN** test-report SHALL 包含"经验库更新"章节
- **AND** SHALL 列出"已有经验更新：2 条"和"新经验记录：1 条"
- **AND** Gate 3 确认时 SHALL 展示经验库变更摘要
---
## V2.9 变更: 2026-06-05-stdd-v2.9-core
- 详见 archive/2026-06-05-stdd-v2.9-core/
