# STDD V2.9.2 最终完善

## Why

V2.9.1 完成后仍有缺口：Skill 轻量路径不完整、Phase Context 未全覆盖、无强制门、Canonical YAML 体系不完整、设计偏离记录仍是 MD 无法闭环。

## What Changes

**Skill 补全（#1-4）**：spec/slice/deliver 轻量路径 + 6 Skill Phase Context + verify Context Budget + structure delta 引导

**强制门（#5-7）**：`stdd guard` CLI + Layer1 AI 指令注入 + Claude Code PreToolUse hook

**Canonical YAML 扩展（#8-11）**：新建 spec.yaml / pending-adjustments.yaml / design-adjustments.yaml 模板 + Phase 1-2 Skills 改为 YAML-First

## Capabilities

### New
- **guard-system**：`stdd guard --check/--status/--init`
- **canonical-schemas-v2**：spec.yaml + pending-adjustments.yaml + design-adjustments.yaml 模板
- **yaml-first-workflow**：Phase 1-2 以 YAML 为 AI 主读文档

### Modified
- **skill-lite-paths**：spec/slice/deliver 轻量模式
- **skill-phase-context**：6 Skill 统一生成
- **skill-budget-delta**：verify budget + build structure
- **enforce-layer1**：STDD.md/AGENTS.md 强制策略

## Impact

新建 4 文件（guard.py + 3 YAML 模板），修改 ~20 文件（6 skills + 6 .claude skills + STDD.md + AGENTS.md + __init__.py + settings + install.py）

## Success Criteria

- [ ] spec/slice/deliver 含 lightweight 模式分支
- [ ] 6 Skill 每个 Phase 末尾有 phase-context 生成
- [ ] verify.md Step -1 Context Budget 检查
- [ ] build.md Step 0 structure delta 执行指引
- [ ] `stdd guard --check` exit 0/1 正确
- [ ] `stdd guard --init` 部署 PreToolUse hook
- [ ] STDD.md/AGENTS.md 含 enforce_stdd 策略
- [ ] spec.yaml / pending-adjustments.yaml / design-adjustments.yaml 模板就绪
- [ ] Phase 1-2 Skills 改为 YAML-First
- [ ] 61 tests 无回归
