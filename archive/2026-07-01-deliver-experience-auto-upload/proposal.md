# DELIVER 经验自动上传 + V2.9.6 版本升级

## Why

STDD 的经验闭环（Phase 5 extract → review → deposit → share）目前止步于本地。`stdd experience share` 已实现单条经验上传到社区 git 库，但 DELIVER 阶段没有集成自动上传，开发者需手动执行 CLI 命令，实际执行率极低。

## What Changes

- DELIVER skill 新增 **Step 2.8: 经验自动上传**，扫描 deposited 经验 → 批量 share → 结果汇总
- 版本号 **2.9.5 → 2.9.6**

## Capabilities

### Modified Capabilities

- **skill-deliver**：DELIVER skill 新增经验自动上传步骤
- **version-upgrade**：版本号 2.9.5 → 2.9.6

## Impact

**代码层面**：修改 `.stdd/skills/deliver.md`（~20 行），修改 `.stdd/version.yaml`（1 行），修改 `stdd/__init__.py`（如有版本常量）
**配置层面**：无变更
**基础设施**：依赖已有 `stdd experience share`（gh CLI 或 API fallback）

## Success Criteria

- [ ] `stdd/skills/deliver.md` 包含 Step 2.8 经验自动上传
- [ ] `.stdd/version.yaml` 版本号为 `2.9.6`
- [ ] 上传成功的经验 `lifecycle_state` 更新为 `shared`
- [ ] 上传失败不阻断 DELIVER，降级 warn + 提示手动重试

> 复杂度：2/17 → **lightweight** | 锚定：L1
