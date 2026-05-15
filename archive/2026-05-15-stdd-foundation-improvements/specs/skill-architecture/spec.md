# Capability: skill-architecture

## MODIFIED Requirements

### Requirement: Master Skill 文件 frontmatter 标准化

`.stdd/skills/` 下的 6 个 master skill 文件 SHALL 包含 YAML frontmatter（`name` + `description`），使其能够被 Skill 工具独立加载，不再仅是"纸面备份"。

#### Scenario: 所有 master skill 文件含 frontmatter

- **GIVEN** `.stdd/skills/` 目录存在 6 个文件（understand/spec/slice/build/verify/deliver）
- **WHEN** Skill 工具尝试加载 `.stdd/skills/understand.md`
- **THEN** 该文件 SHALL 以 YAML frontmatter（`---` 包裹）开头
- **AND** frontmatter SHALL 至少包含 `name` 和 `description` 两个字段
- **AND** `name` 字段 SHALL 与文件名一致（如 `name: stdd-understand`）
- **AND** `description` 字段 SHALL 描述该阶段的用途和产出

#### Scenario: frontmatter 格式与 claude-code 平台一致

- **GIVEN** `.stdd/skills/` 和 `.stdd/platforms/claude-code/skills/` 中的对应文件
- **WHEN** 对比两处同名文件的 frontmatter
- **THEN** `name` 字段值 SHALL 完全一致
- **AND** `description` 字段值 SHALL 完全一致

---

### Requirement: Master-Platform 同步一致性标准

系统 SHALL 建立 master→platform 的同步一致性标准：`.stdd/skills/` 为唯一主版本，platform 目录为派生副本，master 文件修改后 platform 副本 SHALL 同步更新。

#### Scenario: master 修改后 platform 同步

- **GIVEN** `.stdd/skills/` 为唯一 master 版本
- **WHEN** 对 master 文件进行内容修改（如新增步骤、修改 Gate 模板）
- **THEN** 所有 platform 目录下的对应文件 SHALL 同步修改
- **AND** 同步 SHALL 保持各平台的 frontmatter 格式不变

#### Scenario: 一致性可验证

- **GIVEN** master 和 platform 文件均已更新
- **WHEN** Phase 5 Step 0 的 docs_skills 审查代理检查文件一致性
- **THEN** 审查 SHALL 使用 Grep 对比 master 和 platform 文件的关键特征计数
- **AND** 差异超过阈值（>2）SHALL 标记为文档不一致问题
