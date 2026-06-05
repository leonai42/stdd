# STDD V2.9 Skill 同步与完善

## Why

Change 1 完成了 CLI 核心引擎，但 V2.8 反馈中的 Skill 层脱节和 CLI 默认值问题未解决。需将 V2.9 CLI 能力同步到 Skill 指令层，补充测试覆盖。

## What Changes

- **Skill 同步**：spec.md/deliver.md 集成 canonical 步骤；6 个 Skill 增加 phase-context 生成；build.md 增加 rules 加载 + structure delta；build/verify 增加 context budget 检查
- **CLI 改进**：canon init 默认目录改为 change 内部
- **测试补充**：upgrade.py (14 TC) + batch.py (10 TC)

## Capabilities

### Modified Capabilities
- **skill-canonical**：spec/deliver 集成 canonical YAML 生成与归档
- **skill-process**：6 个 Skill 增加 phase-context + context budget + rules 加载
- **canon-init-dir**：默认目录改为 changes/<change>/canonical/
- **test-coverage**：upgrade.py + batch.py 测试覆盖

## Impact

- 代码层面：修改 6 个 .stdd/skills/*.md + 6 个 .claude/skills/stdd-*/SKILL.md + canon.py；新建 test_upgrade.py + test_batch.py
- 配置层面：无
- 基础设施：无

## Success Criteria

- [ ] spec.md Step 7 包含 `stdd proposal init` + `stdd canon init`
- [ ] deliver.md Step 2 包含 canonical 文件合并
- [ ] build.md Step 0 包含 `.stdd/rules/` 加载 + `stdd structure delta`
- [ ] 6 个 Skill 每个 Phase 末尾有 phase-context.md 生成步骤
- [ ] build.md/verify.md 有 context budget 检查
- [ ] `canon init` 默认在 changes/<change>/canonical/ 下创建
- [ ] test_upgrade.py 14 TC 通过
- [ ] test_batch.py 10 TC 通过
