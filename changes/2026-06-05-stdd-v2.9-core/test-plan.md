# STDD V2.9 核心引擎升级 - 测试方案

## 1. 测试策略

### 测试金字塔

```
        ┌─────┐
        │ E2E │  集成测试：实际项目执行 upgrade + batch 命令
        ├─────┤
        │ INT │  单元测试：每个 CLI 命令模块的独立测试
        ├─────┤
        │UNIT │  Python 标准库 unittest/pytest
        └─────┘
```

### 测试原则

- 每个 spec Scenario 至少 1 个 TC 案例
- Bug 修复先写复现测试（RED），再修复
- CLI 命令测试使用 tmp_path fixture 模拟项目环境
- 不依赖外部 STDD 源——使用 mock/fake 源目录

### 已有测试资产

- `tests/commands/` 下已有 27 个命令模块的测试
- `tests/` 使用 pytest 框架
- 覆盖率目标：73%（V2.8 基线），目标 ≥80%

## 2. 详细测试案例

### TC-UPGRADE（version-upgrade）

| TC-ID | Scenario | 优先级 | 测试方法 |
|-------|----------|--------|---------|
| TC-UPGRADE-001 | 旧版本项目检测到差距 | P0 | `test_upgrade_check_shows_gap` — 模拟旧 version.yaml + 新源 project.yaml |
| TC-UPGRADE-002 | 项目已是最新版本 | P0 | `test_upgrade_check_at_latest` — 版本号相同 |
| TC-UPGRADE-003 | 旧项目无 version.yaml 回退 project.yaml | P1 | `test_upgrade_fallback_project_yaml` — 删除 version.yaml，设置 project.yaml 版本 |
| TC-UPGRADE-004 | 成功升级并创建备份 | P0 | `test_upgrade_creates_backup` — 验证 backup 目录内容 |
| TC-UPGRADE-005 | 升级 project.yaml 使用合并策略 | P0 | `test_upgrade_merges_project_yaml` — 验证项目字段保留 |
| TC-UPGRADE-006 | 锁定项目拒绝升级 | P0 | `test_upgrade_locked_project_skipped` |
| TC-UPGRADE-007 | 升级使用 dry-run 模式 | P0 | `test_upgrade_dry_run_no_changes` — 验证文件系统无变化 |
| TC-UPGRADE-008 | 锁定项目 | P1 | `test_lock_sets_lock_flag` |
| TC-UPGRADE-009 | 解锁项目 | P1 | `test_unlock_removes_lock` |
| TC-UPGRADE-010 | 批量检查所有注册项目 | P1 | `test_upgrade_all_check_shows_matrix` |
| TC-UPGRADE-011 | 批量升级跳过锁定和最新项目 | P1 | `test_upgrade_all_skips_locked_and_latest` |
| TC-UPGRADE-012 | 启动时检测到新版本 | P0 | `test_startup_version_check_prompts` |
| TC-UPGRADE-013 | 启动时项目已锁定 | P1 | `test_startup_check_locked_skips` |
| TC-UPGRADE-014 | 非 STDD 项目不检查 | P1 | `test_startup_check_non_stdd_project_skips` |

### TC-LITE（lightweight-mode）

| TC-ID | Scenario | 优先级 | 测试方法 |
|-------|----------|--------|---------|
| TC-LITE-001 | 微小变更评为 lightweight | P0 | 验证复杂度评分函数返回 0-3 |
| TC-LITE-002 | 中型变更评为 standard | P1 | 验证复杂度评分函数返回 4-7 |
| TC-LITE-003 | 大型变更评为 thorough | P1 | 验证复杂度评分函数返回 >=8 |
| TC-LITE-004 | Gate 1 用户确认 AI 建议模式 | P0 | 验证 .stdd.yaml 写入 mode 字段 |
| TC-LITE-005 | 用户调整为更高级别模式 | P1 | 验证用户选择覆盖 AI 建议 |
| TC-LITE-006 | lightweight Phase 2 跳过 design/test-plan | P0 | 验证 Phase 2 跳过步骤 |
| TC-LITE-007 | lightweight Phase 3 跳过切片 | P1 | 验证 Phase 3 使用隐式切片 |
| TC-LITE-008 | lightweight Phase 4 聚焦 TDD | P0 | 验证 RED(1-2 测试)→GREEN，无 REFACTOR |
| TC-LITE-009 | lightweight Phase 5 核心检查 | P0 | 验证单 agent review + 5 类失败模式 |
| TC-LITE-010 | standard 模式行为不变 | P0 | 回归测试：V2.8 行为无变化 |
| TC-LITE-011 | Phase 2 中上调模式 | P1 | 验证 preliminary → confirmed 升级 |
| TC-LITE-012 | 文档任务使用 markdownlint | P2 | 验证 task_type: documentation 的验证策略 |
| TC-LITE-013 | 配置任务使用 yamllint | P2 | 验证 task_type: configuration 的验证策略 |

### TC-BATCH（batch-management）

| TC-ID | Scenario | 优先级 | 测试方法 |
|-------|----------|--------|---------|
| TC-BATCH-001 | 首次轻量变更创建新批次 | P0 | 验证目录创建 + .stdd.yaml 写入 |
| TC-BATCH-002 | 后续变更追加到已有批次 | P0 | 验证编号递增 + 不创建新目录 |
| TC-BATCH-003 | weekly 策略使用周标识 | P2 | 验证目录名 YYYY-Www-MMDD |
| TC-BATCH-004 | count_based 达阈值自动闭合 | P2 | 验证 max_items 触发闭合 |
| TC-BATCH-005 | 手动闭合批次 | P0 | 验证 archive-summary.md + closed_at |
| TC-BATCH-006 | 闭合后新变更创建不同名批次 | P0 | 验证日期不同 → 目录名不同 |
| TC-BATCH-007 | 同日闭合再新建追加小时后缀 | P1 | 验证 2026-06-05-14 格式 |
| TC-BATCH-008 | 查看当前批次状态 | P1 | `stdd batch status` 输出验证 |
| TC-BATCH-009 | 查看所有批次 | P2 | `stdd batch list` 输出验证 |
| TC-BATCH-010 | deliver 时归档已闭合批次 | P1 | 验证 archive/ 移动 |

### TC-EXP（experience-list）

| TC-ID | Scenario | 优先级 | 测试方法 |
|-------|----------|--------|---------|
| TC-EXP-001 | 新项目无 experiences 目录 | P0 | 验证返回 []，无异常 |
| TC-EXP-002 | experiences 目录存在但为空 | P0 | 验证显示 0 条，无异常 |
| TC-EXP-003 | 正常有数据不退化 | P0 | 回归测试：与 V2.8 行为一致 |
| TC-EXP-004 | _save_index 自动创建目录 | P0 | 验证 _ensure_dir 在 _save_index 之前调用 |

### TC-CANON（canon-verify）

| TC-ID | Scenario | 优先级 | 测试方法 |
|-------|----------|--------|---------|
| TC-CANON-001 | 先生成 YAML 再生成 Human View | P0 | 验证生成顺序 + source_hash 一致性 |
| TC-CANON-002 | 生成后 DC-HASH 通过 | P0 | `canon verify` 两项检查均通过 |
| TC-CANON-003 | source_hash 不一致时 detect | P1 | 手动改 Human View，验证检测失败 |

### TC-INIT（project-init）

| TC-ID | Scenario | 优先级 | 测试方法 |
|-------|----------|--------|---------|
| TC-INIT-001 | upgrade.py 导入 FILES_TO_COPY | P0 | 验证常量值与 init.py 内联列表一致 |
| TC-INIT-002 | upgrade.py 导入 DIRS | P1 | 验证目录列表完整性 |
| TC-INIT-003 | upgrade.py 导入 PLATFORMS | P1 | 验证平台列表 |
| TC-INIT-004 | cmd_init 行为不变 | P0 | 回归测试：`stdd init` 输出不变 |
| TC-INIT-005 | CONFIG_MERGE_FILES 包含 project.yaml | P1 | 验证常量值 |
| TC-INIT-006 | CONFIG_ALL_FILES 包含所有 config | P1 | 验证常量值 |

### TC-STATE（change-state）

| TC-ID | Scenario | 优先级 | 测试方法 |
|-------|----------|--------|---------|
| TC-STATE-001 | lightweight 变更的 .stdd.yaml | P0 | 验证 mode/task_type/complexity_score 字段 |
| TC-STATE-002 | standard 变更的 .stdd.yaml | P1 | 验证 mode: standard |
| TC-STATE-003 | 非代码任务的 .stdd.yaml | P2 | 验证 task_type: documentation |
| TC-STATE-004 | 读取旧格式 .stdd.yaml | P0 | 验证向后兼容：无 mode → standard |

## 3. 测试执行矩阵

| Capability | 单元测试 | 集成测试 | P0 合计 | P1 合计 | P2 合计 |
|-----------|---------|---------|---------|---------|---------|
| version-upgrade | 12 | 2 | 5 | 8 | 0 |
| lightweight-mode | 11 | 2 | 5 | 5 | 3 |
| batch-management | 8 | 2 | 4 | 3 | 3 |
| experience-list | 4 | 0 | 4 | 0 | 0 |
| canon-verify | 3 | 0 | 2 | 1 | 0 |
| project-init | 4 | 2 | 1 | 5 | 0 |
| change-state | 4 | 0 | 2 | 1 | 1 |
| **总计** | **46** | **8** | **23** | **23** | **7** |

## 4. 回归风险矩阵

| 改动区域 | 风险等级 | 影响范围 | 回归策略 |
|---------|---------|---------|---------|
| `experience.py` — 空目录处理 | 低 | 仅 list/add/stats 子命令 | 全量 experience 测试 |
| `canon.py` — 生成顺序 | 中 | init/generate/verify 三个子命令 | 全量 canon 测试 |
| `init.py` — 常量提取 | 低 | cmd_init 内部逻辑 | `stdd init` 回归测试 |
| `__init__.py` — 启动检测 | 中 | 所有 CLI 命令的启动路径 | 全命令冒烟测试 |
| `utils.py` — 版本函数 | 低 | 仅 upgrade 调用 | 隔离测试 |
| `upgrade.py`（新） | 高 | 不涉及现有模块 | 独立测试套件 |
| `batch.py`（新） | 中 | 不涉及现有模块 | 独立测试套件 |
| `.stdd/skills/*.md` | 低 | AI 行为变化 | 手动验证（不可自动化） |

## 5. 建议补充顺序

### P0 — 阻塞性（必须全部通过才能交付）
1. TC-EXP-001~004 — Bug 修复验证
2. TC-CANON-001~002 — Bug 修复验证
3. TC-UPGRADE-001~002,004~007,012 — 核心 upgrade 流程
4. TC-LITE-001,004,006,008~010 — 核心轻量模式
5. TC-BATCH-001~002,005~006 — 核心批次管理
6. TC-INIT-001,004 — init 回归
7. TC-STATE-001,004 — state 基础 + 向后兼容

### P1 — 重要（发布前应通过）
1. TC-UPGRADE-003,008~011,013~014 — 边界情况
2. TC-LITE-002~003,005,007,011 — 模式判断和上调
3. TC-BATCH-007~008,010 — 批次防冲突 + 归档
4. TC-CANON-003 — source_hash 不一致检测
5. TC-INIT-002~003,005~006 — 常量验证
6. TC-STATE-002 — standard 模式

### P2 — 增强（可后续迭代）
1. TC-LITE-012~013 — 非代码任务
2. TC-BATCH-003~004,009 — weekly/count_based/list
3. TC-STATE-003 — 文档任务 type
