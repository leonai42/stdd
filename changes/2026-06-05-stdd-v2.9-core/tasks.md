# STDD V2.9 核心引擎升级 — 任务清单

## Slice 1: Bug 修复（P0）

### experience-list
- [ ] 修复 `_save_index` 在目录不存在时崩溃 — 调用前先 `_ensure_dir(exp_dir)`
- [ ] 新增 TC-EXP-001：新项目无 experiences 目录返回空列表
- [ ] 新增 TC-EXP-002：空目录返回 0 条
- [ ] 运行 TC-EXP-003 回归测试确认无退化

### canon-verify
- [ ] 调整生成顺序：`cmd_canon_generate` 中先生成/更新 YAML，计算 source_hash，再渲染 Human View
- [ ] 新增 TC-CANON-001：验证生成后 DC-HASH 通过
- [ ] 新增 TC-CANON-002：验证 DC-FIELD 通过

## Slice 2: 基础层（P0）

### project-init（init.py 重构）
- [ ] 提取 `DIRS` 为模块级常量
- [ ] 提取 `FILES_TO_COPY` 为模块级常量
- [ ] 新增 `CONFIG_MERGE_FILES` 常量
- [ ] 新增 `CONFIG_ALL_FILES` 常量
- [ ] 新增 `PLATFORMS` 常量
- [ ] `cmd_init` 内部改用模块级常量
- [ ] 运行 TC-INIT-004 回归测试确认无退化

### utils.py（版本工具函数）
- [ ] 新增 `get_source_version()` — 从 STDD_SOURCE 读版本
- [ ] 新增 `get_project_version(project_root)` — 读 version.yaml（fallback project.yaml）
- [ ] 新增 `compare_versions(v1, v2)` — 语义版本比较
- [ ] 新增 `_try_version_check(project_root)` — 启动版本检测

### change-state（.stdd.yaml 扩展）
- [ ] `new.py` 中 `.stdd.yaml` 模板增加 `mode`/`task_type`/`complexity_score` 字段
- [ ] 新增 TC-STATE-001：lightweight 写入验证
- [ ] 新增 TC-STATE-004：旧格式向后兼容（无 mode → standard）

## Slice 3: 升级系统（P0）

### upgrade.py（新模块）
- [ ] 实现 `cmd_upgrade(args)` 入口 + flat flags 分发
- [ ] 实现 `_read_version_yaml()` / `_write_version_yaml()`
- [ ] 实现 `_read_registry()` / `_write_registry()` / `_register_project()`
- [ ] 实现 `_backup_project_files()` — 备份到 `.stdd/backup/<ver>-<ts>/`
- [ ] 实现 `_sync_files()` — 复用 init.py 的 FILES_TO_COPY
- [ ] 实现 `_merge_project_yaml()` — 结构键覆盖 + 身份键保留
- [ ] 实现 `_detect_installed_platforms()` / `_reinstall_platforms()`
- [ ] 实现 `_cmd_check_current()`, `_cmd_upgrade_current()`
- [ ] 实现 `_cmd_check_all()`, `_cmd_upgrade_all()`
- [ ] 实现 `_cmd_lock_project()`, `_cmd_unlock_project()`
- [ ] 支持 `--dry-run`, `--yes/-y`

### __init__.py（注册 + 启动检测）
- [ ] 注册 `p_upgrade` subparser
- [ ] 注册 `p_batch` subparser（Slice 4 使用）
- [ ] 添加 `"upgrade"` 到 commands 字典
- [ ] 添加 `"batch"` 到 commands 字典（Slice 4 使用）
- [ ] 在 `main()` 中命令分发前插入 `_try_version_check()`

### 测试
- [ ] TC-UPGRADE-001~014（14 个，已定义在 test-plan.md）

## Slice 4: 轻量系统（P0）

### lite.yaml（新配置文件）
- [ ] 创建 `.stdd/config.d/lite.yaml` — 评分阈值 + 批次策略 + task_type 验证映射

### batch.py（新模块）
- [ ] 实现 `cmd_batch(args)` 入口
- [ ] 实现 `_get_current_batch()` — 查找未闭合批次
- [ ] 实现 `_create_batch()` — 按策略创建批次目录
- [ ] 实现 `_close_batch()` — 生成 archive-summary.md
- [ ] 实现 `_cmd_batch_status()`, `_cmd_batch_list()`, `_cmd_batch_close()`
- [ ] 目录命名防冲突（日期 + 小时后缀）

### .stdd/skills/ 更新（6 个文件）
- [ ] `understand.md` — Step 3.5 复杂度评分 + Gate 1 模式确认
- [ ] `spec.md` — 轻量模式路径 + Gate 2 自动通过
- [ ] `slice.md` — 轻量模式跳过切片
- [ ] `build.md` — 轻量 RED(1-2 聚焦测试)→GREEN，跳过 REFACTOR
- [ ] `verify.md` — 单 agent review + 核心 5 类失败模式
- [ ] `deliver.md` — 批次追加归档

### 测试
- [ ] TC-LITE-001~013 + TC-BATCH-001~010（23 个）
