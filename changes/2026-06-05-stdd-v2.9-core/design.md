# STDD V2.9 核心引擎升级 - 技术设计

## Context

STDD V2.8 CLI 架构：入口 `bin/stdd` → 调度器 `stdd/cli/__init__.py` → 27 个命令模块 `stdd/cli/commands/*.py`。命令注册使用 `subparsers.add_parser()` + `commands` 字典映射。Python 3.10+，无外部依赖（仅标准库 yaml/json/argparse）。配置文件在 `.stdd/config.d/*.yaml`，Skill 源文件在 `.stdd/skills/*.md`。

本次变更涉及：新增 2 个 CLI 模块、修改 5 个现有模块、新增 2 个配置文件、更新 6 个 Skill 源文件。

## Decisions

### 1. upgrade 命令设计：flat flags 而非子命令

**方案**：`stdd upgrade --check/--lock/--unlock/--all` 使用互斥标志，而非 `stdd upgrade check/lock/unlock` 子命令模式。

**为什么**：upgrade 的操作（检查/锁定/升级/批量）是同一领域的正交维度，不是独立子领域。flat flags 实现更简单（参考 `fix.py` 的 `--level` 模式），用户心智模型更清晰（都是 upgrade 的修饰）。

**备选方案及排除原因**：
- 子命令模式（如 `canon.py`）：适合操作差异大的命令（init vs verify），但对 upgrade 这种同类操作过于冗余
- 单独命令（`stdd version-check`、`stdd version-upgrade`）：命令列表膨胀，不符合现有架构

### 2. 版本存储：新增 version.yaml 而非修改 project.yaml

**方案**：新建 `.stdd/version.yaml` 作为项目版本状态文件，包含版本号、锁定状态、安装时间等升级专用字段。`project.yaml` 中的 `stdd_version` 作为旧项目回退。

**为什么**：
- 关注点分离：project.yaml 是项目元数据，version.yaml 是升级状态
- 向后兼容：旧项目无 version.yaml 时回退读取 project.yaml
- 锁定状态不适合放在 project.yaml（后者是 STDD 源模板，合并升级时会冲突）

**备选方案及排除原因**：
- 扩展 project.yaml：lock 状态在 upgrade 合并时需要特殊处理，逻辑复杂
- 全局注册表代替项目版本文件：跨项目共享问题，一个项目升级不应影响其他项目

### 3. 轻量模式：Phase 1 末尾决定模式，Phase 2 起执行缩放

**方案**：Phase 1 UNDERSTAND 不缩放（统一流程），在 Phase 1 末尾计算复杂度评分、AI 建议模式、Gate 1 用户确认。Phase 2 SPEC 开始按模式执行不同深度。复杂度评分标记 `preliminary`，Phase 2 可上调不可下调。

**为什么**：
- Phase 1 是探索阶段，在完成之前无法确定复杂度
- 模式需要在 Gate 1 与 proposal 一起确认，作为后续 Phase 的契约
- 可上调机制防止 premature optimization（初步评为轻量，深入后发现复杂可升级）

**备选方案及排除原因**：
- Phase 2 决定模式：Gate 2 太迟，用户期望在 Gate 1 就知道后续流程
- Phase 1 缩放：循环依赖 — 你需要知道模式来决定 Phase 1 深度，但你需要 Phase 1 探索来决定模式

### 4. 批次目录：创建日期防冲突

**方案**：批次目录命名为 `changes/_batch/{period}-{first_create_date}/`，如 `2026-06-05/`。同日闭合再新建时追加小时后缀 `2026-06-05-14/`。

**为什么**：
- 日期天然不重复，无需额外计数器
- 一眼可见批次时间范围
- 小时后缀覆盖极端情况（同日多次闭合）

**备选方案及排除原因**：
- 纯周期标识（`2026-06/`）：手动闭合后新批次同名冲突
- 序号法（`2026-06-001/`）：需要状态文件记录最后序号，增加复杂度

### 5. TDD 在轻量模式中保留

**方案**：轻量模式 BUILD 仍执行 RED（写 1-2 聚焦测试）→ GREEN（最小实现），仅跳过 REFACTOR。

**为什么**：
- Bug 修复本质是测试逃逸 — 旧测试没覆盖才导致逃逸，不写新测试无法防止回归
- 小优化的新行为可能不被已有测试覆盖
- TDD 是 STDD 的质量底线，轻量模式差异在测试数量而非有无

**备选方案及排除原因**：
- 轻量模式完全跳过测试：失去 STDD 核心价值，等同于非受控修改

### 6. 启动版本检测：fire-and-forget

**方案**：在 `main()` 中命令分发前插入 `_try_version_check()`，仅打印提示，任何异常不阻塞。

**为什么**：
- 不阻塞用户正常使用
- 不过度打扰（锁定项目跳过）
- 与 upgrade 命令互斥（`stdd upgrade` 时不再显示 "运行 upgrade 查看"）

## Architecture

```
新增命令调用链：
  bin/stdd → stdd/cli/__init__.py → main()
    ├── _try_version_check()          ← 启动检测（新增）
    ├── cmd_upgrade()                  ← upgrade 命令（新增）
    │     ├── _read_version_yaml()     → .stdd/version.yaml
    │     ├── _read_registry()         → ~/.stdd/projects.yaml
    │     ├── _backup_project_files()  → .stdd/backup/<ver>-<ts>/
    │     ├── _sync_files()            复用 init.py 的 FILES_TO_COPY
    │     └── _reinstall_platforms()   复用 install.py 逻辑
    └── cmd_batch()                    ← batch 命令（新增）
          ├── _get_current_batch()     → changes/_batch/<id>/
          ├── _create_batch()
          └── _close_batch()

修改模块：
  experience.py: _cmd_list() → exp_dir 不存在时优雅降级
  canon.py:      cmd_canon_generate() → 先 YAML 再 Human View
  init.py:       提取 DIRS/FILES_TO_COPY/PLATFORMS 为模块常量
  new.py:        .stdd.yaml 增加 mode/task_type/complexity_score
  utils.py:      增加 get_source_version/get_project_version/compare_versions
  __init__.py:   注册 upgrade + batch 命令，插入启动检测

配置新增：
  .stdd/config.d/lite.yaml     ← 轻量模式配置
  .stdd/version.yaml           ← 项目版本状态（每个项目一份）
  ~/.stdd/projects.yaml         ← 全局注册表（用户级）

Skill 更新：
  .stdd/skills/understand.md   ← Step 3.5 复杂度评分 + Gate 1 模式确认
  .stdd/skills/spec.md         ← 轻量模式路径
  .stdd/skills/slice.md        ← 轻量模式跳过
  .stdd/skills/build.md        ← 轻量 RED→GREEN 缩放
  .stdd/skills/verify.md       ← 核心 5 类失败模式
  .stdd/skills/deliver.md      ← 批次追加归档
```

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|----------|
| upgrade 覆盖 project.yaml 时误删项目特定配置 | merge 策略：仅覆盖结构键，保留 name/language/paths/source_dir |
| 复杂度评分误判中型变更为 lightweight | preliminary 标记 + Phase 2 可上调不可下调 |
| 批次目录同日多次闭合产生冲突 | 日期 + 小时后缀 |
| 全局注册表在并发写入时可能损坏 | CLI 单用户使用，原子写入（write tmp → rename） |
| 旧项目无 version.yaml 时版本检测失败 | 回退读取 project.yaml 的 stdd_version 字段 |
| 轻量模式跳过太多步骤导致质量问题 | TDD 底线保留 + Gate 3 强制确认 |
