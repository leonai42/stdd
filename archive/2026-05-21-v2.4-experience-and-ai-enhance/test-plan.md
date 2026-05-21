# V2.4 测试方案与详细案例

> 版本：V2.4
> 创建日期：2026-05-21
> 对应 Phase 2 Spec：experience-library / spec-auto-complete / smart-slice / ci-integration

## 一、测试策略

### 1.1 测试金字塔

```
        ┌─────┐
        │ E2E │  2 个（完整 change 走 V2.4 增强流程）
        ├─────┤
        │集成 │  12 个（CLI + 技能联动）
        ├─────┤
        │单元 │  30+ 个（每个 CLI 子命令 + 工具函数）
        └─────┘
```

### 1.2 测试原则

- 所有 CLI 命令遵循现有测试模式：`temp_project` fixture → `argparse.Namespace` → `monkeypatch.chdir` → 断言文件系统或 `capsys`
- 技能文件的增强通过手工审查验证（技能是纯 Markdown，不可自动测试）
- CI 生成的文件通过 YAML 语法校验
- 经验库操作测试使用真实文件系统（`tmp_path`）

### 1.3 已有测试资产

| 测试文件 | 用例数 | 类型 | 覆盖范围 |
|----------|--------|------|----------|
| tests/commands/test_init.py | 3 | 单元 | init 命令 |
| tests/commands/test_new.py | 5 | 单元 | new 命令 |
| tests/commands/test_validate.py | 7 | 单元 | validate 命令 |
| tests/commands/test_status.py | 4 | 单元 | status 命令 |
| tests/commands/test_archive.py | 4 | 单元 | archive 命令 |
| tests/commands/test_rollback.py | 5 | 单元 | rollback 命令 |
| tests/commands/test_abort.py | 4 | 单元 | abort 命令 |
| tests/commands/test_diff.py | 5 | 单元 | diff 命令 |
| tests/commands/test_trace.py | 4 | 单元 | trace 命令 |
| tests/test_utils.py | 6 | 单元 | 工具函数 |
| tests/test_finder.py | 8 | 单元 | change 查找 |
| **总计** | **55** | | |

## 二、详细测试案例

### 功能 1：经验数据存储与索引

对应 spec：experience-library → 经验数据存储

#### 案例 1.1 — 创建经验条目

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-001 |
| **对应 Spec** | experience-library/spec.md → Scenario: 创建经验条目 |
| **优先级** | P0 |
| **预置条件** | `.stdd/experiences/` 目录已存在 |
| **输入** | `stdd experience add --category cascading_errors --pattern "async 函数裸 except 遗漏 CancelledError" --language python --severity high` |
| **预期结果** | 创建 `EXP-2026-0001.md`，YAML frontmatter 包含所有指定字段，`.experience-index.yaml` 已更新 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.2 — 索引自动更新

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-002 |
| **对应 Spec** | experience-library/spec.md → Scenario: 经验索引自动维护 |
| **优先级** | P0 |
| **预置条件** | 已有 2 条经验条目 |
| **输入** | 新增第 3 条经验 |
| **预期结果** | `.experience-index.yaml` 的 `last_id: 3`, `total: 3`，各分组列表包含新 ID |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.3 — occurrences 升级 lifecycle

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-003 |
| **对应 Spec** | experience-library/spec.md → Scenario: 经验重现升级 |
| **优先级** | P1 |
| **预置条件** | EXP-0001 的 occurrences=2，lifecycle_state=discovered |
| **输入** | 模拟再次触发相同失败模式 |
| **预期结果** | occurrences=3，lifecycle_state 自动升级为 verified，confidence 提升 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.4 — 索引重建

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-004 |
| **对应 Spec** | experience-library/spec.md → Scenario: 索引从文件重建 |
| **优先级** | P1 |
| **预置条件** | `.experience-index.yaml` 被删除，但 EXP 文件仍存在 |
| **输入** | `stdd experience list --format json` |
| **预期结果** | 系统重新扫描所有 EXP 文件，重建完整索引 |
| **当前状态** | ❌ 测试缺 |

### 功能 2：经验 CLI 命令组

对应 spec：experience-library → 经验 CLI 命令组

#### 案例 2.1 — 过滤列出

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-005 |
| **对应 Spec** | experience-library/spec.md → Scenario: 列出经验并过滤 |
| **优先级** | P0 |
| **预置条件** | 经验库中有 Python 和 Go 经验各 3 条，不同 severity |
| **输入** | `stdd experience list --language python --severity high` |
| **预期结果** | 仅显示匹配 Python + high severity 的经验 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.2 — JSON 格式输出

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-006 |
| **对应 Spec** | experience-library/spec.md → Scenario: 列出经验并过滤 |
| **优先级** | P1 |
| **预置条件** | 经验库中有数据 |
| **输入** | `stdd experience list --format json` |
| **预期结果** | 输出有效 JSON 数组，每个元素包含完整 frontmatter 字段 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.3 — 无效 category 拒绝

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-007 |
| **对应 Spec** | experience-library/spec.md → Scenario: 添加经验（手动） |
| **优先级** | P1 |
| **预置条件** | 经验库已初始化 |
| **输入** | `stdd experience add --category invalid_cat --pattern "test"` |
| **预期结果** | 系统拒绝，提示有效 category 列表（11 个合法值），退出码 1 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.4 — 统计输出

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-008 |
| **对应 Spec** | experience-library/spec.md → Scenario: 统计概览 |
| **优先级** | P1 |
| **预置条件** | 15 条经验分布在 4 个 category |
| **输入** | `stdd experience stats` |
| **预期结果** | 显示按 category/language/severity/lifecycle 分布 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.5 — 导出脱敏

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-009 |
| **对应 Spec** | experience-library/spec.md → Scenario: 导出脱敏 |
| **优先级** | P0 |
| **预置条件** | 经验中包含路径 `/home/user/project/app/main.py` 和 IP `192.168.1.1` |
| **输入** | `stdd experience export --format json` |
| **预期结果** | 路径替换为 `<project>/<module>`，IP 替换为 `<ip-address>`，域名替换为 `<domain>` |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.6 — 不脱敏导出

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-010 |
| **对应 Spec** | experience-library/spec.md → Scenario: 导出脱敏 |
| **优先级** | P1 |
| **预置条件** | 同上 |
| **输入** | `stdd experience export --format json --no-sanitize` |
| **预期结果** | 保留原始路径、IP、域名 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.7 — Pull placeholder

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-011 |
| **对应 Spec** | experience-library/spec.md → Scenario: 社区拉取（V2.5 placeholder） |
| **优先级** | P2 |
| **预置条件** | V2.4 版本 |
| **输入** | `stdd experience pull python-pack` |
| **预期结果** | 输出提示 "此功能将在 V2.5 正式支持"，退出码 0 |
| **当前状态** | ❌ 测试缺 |

### 功能 3：BUILD/VERIFY 经验集成

对应 spec：experience-library → BUILD 阶段经验加载 + VERIFY 阶段经验集成

#### 案例 3.1 — 语言匹配加载

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-012 |
| **对应 Spec** | experience-library/spec.md → Scenario: 按语言和标签匹配经验 |
| **优先级** | P1 |
| **预置条件** | 经验库：EXP-0001（Python, tags:[async]），EXP-0002（Go, tags:[redis]） |
| **输入** | AI 执行 build.md Step 0.5，当前项目语言=Python，切片标签=[async] |
| **预期结果** | 加载 EXP-0001，不加载 EXP-0002 |
| **当前状态** | ❌ 测试缺（手工审查 build.md 技能文本） |

#### 案例 3.2 — test-report 经验章节

| 字段 | 内容 |
|------|------|
| **ID** | TC-EXP-013 |
| **对应 Spec** | experience-library/spec.md → Scenario: test-report 包含经验更新 |
| **优先级** | P1 |
| **预置条件** | 当前 change 触发 2 条已有经验 + 1 条新经验 |
| **输入** | AI 生成 test-report.md |
| **预期结果** | 包含"经验库更新"章节，列出已有更新和新记录 |
| **当前状态** | ❌ 测试缺（手工审查 verify.md 技能文本） |

### 功能 4：Proposal 结构化提取

对应 spec：spec-auto-complete → Proposal 结构化提取

#### 案例 4.1 — 提取完整 proposal

| 字段 | 内容 |
|------|------|
| **ID** | TC-SAC-001 |
| **对应 Spec** | spec-auto-complete/spec.md → Scenario: 提取完整 proposal |
| **优先级** | P0 |
| **预置条件** | change 目录中包含完整 proposal.md |
| **输入** | `stdd extract-proposal <change> --format json` |
| **预期结果** | 输出 JSON 包含 title, capabilities(new/modified), what_changes, success_criteria, impact 字段 |
| **当前状态** | ❌ 测试缺 |

#### 案例 4.2 — 自动选择最新 change

| 字段 | 内容 |
|------|------|
| **ID** | TC-SAC-002 |
| **对应 Spec** | spec-auto-complete/spec.md → Scenario: 自动选择最新 change |
| **优先级** | P1 |
| **预置条件** | 多个 change 目录 |
| **输入** | `stdd extract-proposal --format yaml`（不指定名称） |
| **预期结果** | 自动选择最近修改的 change，输出有效 YAML |
| **当前状态** | ❌ 测试缺 |

#### 案例 4.3 — proposal 缺失

| 字段 | 内容 |
|------|------|
| **ID** | TC-SAC-003 |
| **对应 Spec** | spec-auto-complete/spec.md → Scenario: proposal.md 缺失处理 |
| **优先级** | P1 |
| **预置条件** | 指定 change 中没有 proposal.md |
| **输入** | `stdd extract-proposal <change>` |
| **预期结果** | 错误信息 "proposal.md 不存在"，退出码 1 |
| **当前状态** | ❌ 测试缺 |

### 功能 5：依赖图构建 CLI

对应 spec：smart-slice → 依赖图构建 CLI

#### 案例 5.1 — 构建依赖图（JSON）

| 字段 | 内容 |
|------|------|
| **ID** | TC-SLI-001 |
| **对应 Spec** | smart-slice/spec.md → Scenario: 构建无环依赖图 |
| **优先级** | P0 |
| **预置条件** | 3 个 capability spec，其中 rate-limit 的 GIVEN 引用 auth |
| **输入** | `stdd dependency-graph <change> --format json` |
| **预期结果** | JSON 包含 3 个 nodes（id, label）和 1 个 edge（from, to, reason） |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.2 — 零依赖节点识别

| 字段 | 内容 |
|------|------|
| **ID** | TC-SLI-002 |
| **对应 Spec** | smart-slice/spec.md → Scenario: 识别零依赖节点 |
| **优先级** | P0 |
| **预置条件** | auth 的 GIVEN 均不引用其他 capability |
| **输入** | `stdd dependency-graph --format text` |
| **预期结果** | zero_dependency 列表包含 auth |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.3 — 循环依赖警告

| 字段 | 内容 |
|------|------|
| **ID** | TC-SLI-003 |
| **对应 Spec** | smart-slice/spec.md → Scenario: 循环依赖警告 |
| **优先级** | P1 |
| **预置条件** | A 引用 B，B 引用 A |
| **输入** | `stdd dependency-graph` |
| **预期结果** | 输出警告 "检测到循环依赖：A ↔ B" |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.4 — DOT 格式输出

| 字段 | 内容 |
|------|------|
| **ID** | TC-SLI-004 |
| **对应 Spec** | smart-slice/spec.md → Scenario: DOT 格式输出 |
| **优先级** | P1 |
| **预置条件** | 标准依赖图数据 |
| **输入** | `stdd dependency-graph --format dot` |
| **预期结果** | 输出有效 DOT 格式文本，零依赖节点标记为绿色 |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.5 — 无 spec 目录处理

| 字段 | 内容 |
|------|------|
| **ID** | TC-SLI-005 |
| **对应 Spec** | smart-slice/spec.md → Scenario: 构建无环依赖图（边界情况） |
| **优先级** | P2 |
| **预置条件** | change 目录中无 specs/ 子目录 |
| **输入** | `stdd dependency-graph <change>` |
| **预期结果** | 友好提示 "specs 目录不存在，无法构建依赖图"，退出码 1 |
| **当前状态** | ❌ 测试缺 |

### 功能 6：CI 文件生成

对应 spec：ci-integration → CI 文件生成

#### 案例 6.1 — 交互式初始化

| 字段 | 内容 |
|------|------|
| **ID** | TC-CI-001 |
| **对应 Spec** | ci-integration/spec.md → Scenario: 交互式初始化所有 CI 文件 |
| **优先级** | P0 |
| **预置条件** | 项目根目录无 `.github/workflows/` |
| **输入** | `stdd ci init`（非交互模式自动确认） |
| **预期结果** | 创建 `.github/workflows/stdd-quality.yml`、`.pre-commit-config.yaml`、`.github/stdd-pr-comment.md` |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.2 — 单独生成 workflow

| 字段 | 内容 |
|------|------|
| **ID** | TC-CI-002 |
| **对应 Spec** | ci-integration/spec.md → Scenario: 单独生成工作流文件 |
| **优先级** | P0 |
| **预置条件** | 无已有 CI 文件 |
| **输入** | `stdd ci generate workflow` |
| **预期结果** | 仅创建 `.github/workflows/stdd-quality.yml`，不创建 pre-commit 或 PR 模板 |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.3 — 根据 quality.yaml 调整

| 字段 | 内容 |
|------|------|
| **ID** | TC-CI-003 |
| **对应 Spec** | ci-integration/spec.md → Scenario: 根据质量配置调整生成内容 |
| **优先级** | P1 |
| **预置条件** | quality.yaml 中 coverage_target=85，python_version="3.12" |
| **输入** | `stdd ci generate workflow` |
| **预期结果** | 生成的 YAML 中使用 `python-version: "3.12"` 和 `--cov-fail-under=85` |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.4 — dry-run 预览

| 字段 | 内容 |
|------|------|
| **ID** | TC-CI-004 |
| **对应 Spec** | ci-integration/spec.md → Scenario: dry-run 预览 |
| **优先级** | P1 |
| **预置条件** | 无已有 CI 文件 |
| **输入** | `stdd ci init --dry-run` |
| **预期结果** | 输出所有将要创建的文件内容和路径，不实际创建文件 |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.5 — 已有文件覆盖提示

| 字段 | 内容 |
|------|------|
| **ID** | TC-CI-005 |
| **对应 Spec** | ci-integration/spec.md → Scenario: 生成 pre-commit hook（已有配置） |
| **优先级** | P1 |
| **预置条件** | 已有 `.pre-commit-config.yaml` |
| **输入** | `stdd ci generate pre-commit`（非交互模式） |
| **预期结果** | 检测到已有文件，提示确认后追加 STDD hook 段 |
| **当前状态** | ❌ 测试缺 |

### 功能 7：CI 失败模式检查

对应 spec：ci-integration → CI 失败模式检查

#### 案例 7.1 — 运行确定性检查（通过）

| 字段 | 内容 |
|------|------|
| **ID** | TC-CI-006 |
| **对应 Spec** | ci-integration/spec.md → Scenario: 运行确定性检查子集 |
| **优先级** | P0 |
| **预置条件** | change 中 proposal/specs/test-plan 完整且正确 |
| **输入** | `stdd ci check-failures` |
| **预期结果** | 逐项显示通过结果，退出码 0 |
| **当前状态** | ❌ 测试缺 |

#### 案例 7.2 — 检测到问题

| 字段 | 内容 |
|------|------|
| **ID** | TC-CI-007 |
| **对应 Spec** | ci-integration/spec.md → Scenario: 运行确定性检查子集 |
| **优先级** | P0 |
| **预置条件** | change 中 TC-ID 存在重复，某 spec 的 THEN 缺少 SHALL |
| **输入** | `stdd ci check-failures` |
| **预期结果** | 报告 TC-ID 重复（类别 d）和 SHALL 缺失（类别 f），退出码 1 |
| **当前状态** | ❌ 测试缺 |

#### 案例 7.3 — 覆盖边界提示

| 字段 | 内容 |
|------|------|
| **ID** | TC-CI-008 |
| **对应 Spec** | ci-integration/spec.md → Scenario: 明确标注覆盖边界 |
| **优先级** | P2 |
| **预置条件** | 标准 change |
| **输入** | `stdd ci check-failures` |
| **预期结果** | 输出结尾包含"确定性检查覆盖约 60%"提示和未覆盖模式列表 |
| **当前状态** | ❌ 测试缺 |

## 三、测试执行矩阵

| 功能模块 | 单元测试 | 集成测试 | E2E | 状态 |
|----------|---------|----------|-----|------|
| 经验数据存储与索引 | TC-EXP-001~004 | — | — | 🔴 待实现 |
| 经验 CLI 命令组 | TC-EXP-005~011 | — | — | 🔴 待实现 |
| BUILD/VERIFY 经验集成 | — | TC-EXP-012~013 | 手工审查 | 🔴 待实现 |
| Proposal 结构化提取 | TC-SAC-001~003 | — | — | 🔴 待实现 |
| 依赖图构建 CLI | TC-SLI-001~005 | — | — | 🔴 待实现 |
| CI 文件生成 | TC-CI-001~005 | — | — | 🔴 待实现 |
| CI 失败模式检查 | TC-CI-006~008 | — | — | 🔴 待实现 |
| 技能文件增强 | — | — | 手工审查 | 🔴 待实现 |
| CLI __init__.py 注册 | — | — | 全量回归 | 🔴 待实现 |
| 模板变更 | — | — | 手工审查 | 🔴 待实现 |

## 四、回归风险矩阵

| 风险区域 | V2.4 改动 | 已有回归保护 | 风险等级 |
|----------|-------------|-------------|---------|
| CLI __init__.py | 注册 4 个新命令 | 无（需全量回归测试） | 🟡 |
| stdd validate | 无直接改动 | 7 个用例 | 🟢 |
| stdd status/diff/trace | 无直接改动 | 13 个用例 | 🟢 |
| stdd archive/rollback/abort | 无直接改动 | 13 个用例 | 🟢 |
| stdd init/new | 无直接改动 | 8 个用例 | 🟢 |
| 技能文件 spec.md | 大幅重写 Step 2-3 | 无（手工审查） | 🟡 |
| 技能文件 slice.md | 大幅重写 Step 2 | 无（手工审查） | 🟡 |
| 技能文件 build.md | 新增 Step 0.5 | 无（手工审查） | 🟢 |
| 技能文件 verify.md | 新增 Step 3.5 | 无（手工审查） | 🟢 |
| 模板文件 | 结构修改 | 无（手工审查） | 🟢 |
| 配置文件 | 新增字段 | 6 个 utils 用例 | 🟢 |

## 五、建议补充顺序

1. **第一优先**（部署前必补）：TC-EXP-001, TC-EXP-002, TC-EXP-005, TC-EXP-009, TC-SAC-001, TC-SLI-001, TC-SLI-002, TC-CI-001, TC-CI-002, TC-CI-006, TC-CI-007 — 共 11 个 P0 用例
2. **第二优先**（部署后尽快补）：TC-EXP-003~004, TC-EXP-006~008, TC-EXP-010, TC-EXP-012~013, TC-SAC-002~003, TC-SLI-003~004, TC-CI-003~005 — 共 17 个 P1 用例
3. **第三优先**（后续补）：TC-EXP-011, TC-SLI-005, TC-CI-008 — 共 3 个 P2 用例 + 技能文件手工审查
