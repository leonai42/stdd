# V2.0 开发切片（Slices）

> 23 项改动，6 个切片，按依赖关系排序

## 切片总览

```
Slice 1: 基础设施        ──► Slice 2: 现有命令测试 + dry-run
                                    │
                                    ├──► Slice 3: rollback + diff 新命令
                                    │       │
                                    ├────── Slice 4: abort + validate 增强
                                    │
                                    ├──► Slice 5: finder + 长程 + Skill 系统
                                    │
                                    └──► Slice 6: 文档生态
```

---

## Slice 1: 基础设施（CLI 模块化 + 配置拆分 + logging）

**依赖**：无
**预估**：~4h，8 个文件

### 变更清单

| # | 项 | 类型 | 对应 TC |
|---|-----|------|---------|
| 1.1 | 创建 `stdd/cli/` 包结构 (`__init__.py`, `utils.py`, `finder.py`) | 新建 | TC-CLI-102 |
| 1.2 | 拆分 7 个子命令到 `stdd/cli/commands/{init,new,validate,status,archive,trace,install}.py` | 重构 | TC-CLI-101 |
| 1.3 | 重写 `bin/stdd` 入口（~30行，委托到 `stdd/cli/main()`） | 重构 | TC-CLI-101 |
| 1.4 | 引入 logging 模块替代 print()；实现 `-v` / `-vv` 分级 | 新增 | TC-CLI-105, TC-CLI-106 |
| 1.5 | `config.yaml` 拆分为 `config.d/{project,gates,long_range,quality}.yaml` | 重构 | TC-STATE-001, TC-STATE-002 |
| 1.6 | 配置读取实现 config.d/ 优先 + config.yaml fallback | 重构 | TC-STATE-001, TC-STATE-002 |
| 1.7 | `init` 命令适配：新项目生成 config.d/ 而非 config.yaml | 修改 | TC-STATE-001 |
| 1.8 | 创建 `tests/conftest.py`（tmp_path fixtures, 示例 change 夹具） | 新建 | TC-CLI-111 |

### 验收标准
- `python bin/stdd --help` 输出与 V1.4.0 一致
- 所有 7 个命令可从 `stdd.cli.commands` 独立导入
- `config.d/` 优先于 `config.yaml`
- `-v` / `-vv` 输出不同级别日志

---

## Slice 2: 现有命令测试 + --dry-run

**依赖**：Slice 1
**预估**：~3h，10-12 个文件

### 变更清单

| # | 项 | 类型 | 对应 TC |
|---|-----|------|---------|
| 2.1 | `tests/commands/test_init.py`：正常 init + --force + 自定义模板 | 测试 | TC-CLI-111 |
| 2.2 | `tests/commands/test_new.py`：正常 new + 名称校验 | 测试 | TC-CLI-111 |
| 2.3 | `tests/commands/test_validate.py`：合规 / 不合规 / 缺失文件 | 测试 | TC-CLI-111 |
| 2.4 | `tests/commands/test_status.py`：正常 status + 模糊匹配 | 测试 | TC-CLI-111 |
| 2.5 | `tests/commands/test_archive.py`：正常 archive + 缺失 change | 测试 | TC-CLI-111 |
| 2.6 | `tests/commands/test_trace.py`：TC-ID 存在 / 不存在 | 测试 | TC-CLI-111 |
| 2.7 | `tests/commands/test_install.py`：claude-code / workbuddy / 未知平台 | 测试 | TC-CLI-111 |
| 2.8 | `tests/test_finder.py`：精确匹配 / 模糊匹配 / 无匹配 | 测试 | TC-CLI-111 |
| 2.9 | `tests/test_utils.py`：YAML 读写 / 输出格式化 | 测试 | TC-CLI-111 |
| 2.10 | 为所有 7+ 个命令添加 `--dry-run` 分支逻辑 | 新增 | TC-CLI-103, TC-CLI-104 |

### 验收标准
- `pytest tests/ --cov=stdd --cov-report=term` 覆盖率 ≥ 70%
- `--dry-run` 对每个命令输出操作预览但不修改文件系统

---

## Slice 3: rollback + diff 新命令

**依赖**：Slice 1
**预估**：~2.5h，4 个文件

### 变更清单

| # | 项 | 类型 | 对应 TC |
|---|-----|------|---------|
| 3.1 | 新增 `stdd/cli/commands/rollback.py`：查找 archive/ → 检查冲突 → 移回 | 新增 | TC-CLI-107, TC-CLI-108 |
| 3.2 | 新增 `tests/commands/test_rollback.py`：成功恢复 + 冲突拒绝 + 不存在 | 测试 | TC-CLI-107, TC-CLI-108 |
| 3.3 | 新增 `stdd/cli/commands/diff.py`：解析 test-plan.md → grep 源码 TC-ID → 四列表 | 新增 | TC-CLI-109, TC-CLI-110 |
| 3.4 | 新增 `tests/commands/test_diff.py`：有 plan + 无 plan + TC 全部覆盖 | 测试 | TC-CLI-109, TC-CLI-110 |

### 验收标准
- `stdd rollback my-feature` 从 archive 恢复到 changes/
- `stdd diff my-feature` 输出四列覆盖差异表

---

## Slice 4: abort + validate 增强

**依赖**：Slice 1（abort 也依赖 Slice 1 的模块结构）
**预估**：~2.5h，5 个文件

### 变更清单

| # | 项 | 类型 | 对应 TC |
|---|-----|------|---------|
| 4.1 | 新增 `stdd/cli/commands/abort.py`：移动 change → archive/aborted/ | 新增 | TC-ABORT-001 |
| 4.2 | 在核心 Skill 中增加 `/stdd-abort` 处理逻辑 | 新增 | TC-ABORT-001 |
| 4.3 | 新增 `tests/commands/test_abort.py`：成功 abort + 取消操作 | 测试 | TC-ABORT-001 |
| 4.4 | `cmd_validate` 增加 AND 数量统计（Scenario 间分段统计 `**AND**`） | 修改 | TC-VAL-001, TC-VAL-002 |
| 4.5 | `cmd_trace` 重构：逐行分段解析替代 DOTALL 正则 | 重构 | TC-VAL-003 |
| 4.6 | `cmd_archive` 增加合并冲突检测（同名 `### Requirement:`） | 修改 | TC-VAL-004 |
| 4.7 | 更新 `tests/commands/test_validate.py`：AND 合规 + AND 超限 | 测试 | TC-VAL-001, TC-VAL-002 |
| 4.8 | 更新 `tests/commands/test_trace.py`：标准格式 + 非标准降级 | 测试 | TC-VAL-003 |
| 4.9 | 更新 `tests/commands/test_archive.py`：无冲突 + 有冲突 | 测试 | TC-VAL-004 |

### 验收标准
- `stdd abort experiment --yes` 移至 archive/aborted/
- `stdd validate` 对 ≥6 条 AND 的 Scenario 报告警告
- `stdd trace TC-XXX-001` 不依赖 DOTALL 正则
- `stdd archive` 检测到重复 Requirement 时输出冲突警告

---

## Slice 5: finder 透明化 + 长程退出 + Skill 系统

**依赖**：Slice 1
**预估**：~2.5h，5-7 个文件

### 变更清单

| # | 项 | 类型 | 对应 TC |
|---|-----|------|---------|
| 5.1 | `_find_change_dir` 增加模糊匹配提示输出 | 修改 | TC-STATE-003* |
| 5.2 | 在 Phase 3-5 Skill 中增加长程退出检测逻辑 | 修改 | TC-STATE-003* |
| 5.3 | 创建 `_shared/{confirm-gate,mode-selection,long-range-auth}.md` 共享片段 | 新建 | TC-SKILL-003 |
| 5.4 | 修改 6 个核心 Skill 引用 `_shared/` 片段 | 重构 | TC-SKILL-003 |
| 5.5 | 重写 `cmd_install`：从核心 Skill 读取内容 → 添加平台 frontmatter → 写目标 | 重构 | TC-SKILL-001, TC-SKILL-002 |
| 5.6 | 在 Skill-CLI 桥接处增加 CLI 可用性检查 + 退出码检查 | 修改 | TC-SKILL-003* |

> *注：TC-STATE-003 为 finder 透明化用例（test-plan 中归类在 STATE 下）。Skill-CLI 桥接无独立 TC，属于 SKILL spec 的 Requirement 3。

### 验收标准
- `_find_change_dir` 模糊匹配时输出 "📋 匹配到 change: xxx"
- 长程模式中输入"切换普通模式"可降级
- `stdd install claude-code` 从核心 Skill 生成内容一致
- 确认门模板仅 `_shared/confirm-gate.md` 一处维护

---

## Slice 6: 文档生态

**依赖**：无（独立）
**预估**：~2h，4 个文件 + 1 个目录

### 变更清单

| # | 项 | 类型 | 对应 TC |
|---|-----|------|---------|
| 6.1 | 创建 `CHANGELOG.md`（V1.0 ~ V2.0 版本历史） | 新建 | TC-DOCS-001 |
| 6.2 | 创建 `TROUBLESHOOTING.md`（≥5 个常见问题） | 新建 | TC-DOCS-002 |
| 6.3 | 创建 `EXTENDING.md`（3 个扩展点说明） | 新建 | TC-DOCS-003* |
| 6.4 | 创建 `examples/hello-stdd/` 完整示例项目 | 新建 | TC-DOCS-003* |

> *注：TC-DOCS-003 对应示例项目，EXTENDING.md 在 test-plan 中无独立 TC（属于 spec 的 Requirement 3）。

### 验收标准
- CHANGELOG.md 含 V1.0, V1.1, V1.2, V1.4, V2.0 条目
- TROUBLESHOOTING.md ≥5 个问题，每个有症状+方案
- EXTENDING.md 覆盖平台/语言/失败模式
- `examples/hello-stdd/` 可独立执行 `python ../../bin/stdd init`

---

## 执行顺序 & 依赖图

```
Slice 1 (基础)
  ├─► Slice 2 (测试 + dry-run)
  ├─► Slice 3 (rollback + diff)
  ├─► Slice 4 (abort + validate)
  ├─► Slice 5 (finder + skill)
  └─► Slice 6 (文档，可与 2-5 并行)
```

**并行机会**：Slice 2/3/4/5/6 均可并行开发（均仅依赖 Slice 1），但建议按序推进以逐步积累测试覆盖。

## 回归风险提示

| 切片 | 风险 | 缓解 |
|------|------|------|
| Slice 1 | 模块化破坏 CLI 入口 | 保留 bin/stdd，所有命令签名不变 |
| Slice 1 | 配置拆分导致旧项目不可读 | config.yaml fallback 机制 |
| Slice 4 | trace 重构改变输出格式 | 保持输出格式兼容，仅改内部解析 |
| Slice 5 | Skill 自动同步覆盖手动修改 | install 前备份，增加 --check 模式 |
