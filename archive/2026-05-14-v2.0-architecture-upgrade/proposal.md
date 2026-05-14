# STDD V2.0 架构升级

> 基于 Hermes 评审 + 独立评审遗留项 + V1.2.1/V1.3 完成后的系统性升级

## Why

V1.2.1+V1.3 修复了关键 Bug 并提升了工程基线质量。但两份评审报告中仍有 23 项中长期的架构和系统化工程改进未覆盖：

1. **CLI 可维护性瓶颈**：单文件 700 行 Python，随功能增长难以维护，零自动化测试，修改风险高
2. **功能缺口**：缺少 rollback（从 archive 恢复）、diff（spec↔test↔code 差异对比）、abort（放弃变更）命令
3. **Skill 系统维护负担**：18 个平台 Skill 文件手动同步，6 个核心 Skill 存在大量重复内容
4. **配置臃肿**：config.yaml 103 行，long_range 配置复杂，缺乏 dry-run/verbose 基础能力
5. **文档体系不完整**：缺 CHANGELOG、故障排除指南、示例项目、扩展开发文档
6. **验证能力不足**：AND 数量未校验、trace 正则脆弱、archive 合并无冲突检测

V2.0 的目标是将 STDD 从一个"设计优秀但实现有改善空间"的工具，升级为"设计优秀且工程质量扎实"的可靠产品。

## What Changes

### 一、CLI 架构重构
- **模块化拆分**：`bin/stdd` 单文件 → `stdd/cli/` 包（commands/、state/、validate/ 子模块）
- **CLI 单元测试**：引入 pytest 测试框架，覆盖全部 7 个子命令
- **`--dry-run` 全局选项**：预览模式，输出将执行的操作但不实际执行
- **`--verbose` / `-v` 全局选项**：分级日志（INFO/DEBUG），替代裸 print()

### 二、新命令
- **`stdd rollback <name>`**：从 archive 恢复已归档的 change 到 changes/
- **`stdd diff <name>`**：对比 spec Scenario ↔ TC 案例 ↔ 测试函数 ↔ 源码的覆盖差异
- **`/stdd-abort`**：放弃当前变更，清理 change 目录并更新状态

### 三、Skill 系统改进
- **核心→平台自动同步**：`stdd install` 命令同步时，自动从核心 Skill 生成平台 Skill（而非手动维护 18 份副本）
- **Skill 内容 DRY**：提取共享内容（确认消息模板、模式选择 UI）为 `_shared/` 引用片段
- **Skill-CLI 桥接**：Skill 执行 CLI 命令前检查 CLI 可用性，执行后检查退出码

### 四、状态与配置
- **配置拆分**：`config.yaml` → `config.d/` 目录（`project.yaml`、`gates.yaml`、`long_range.yaml`、`quality.yaml`）
- **长程模式中途退出**：Phase 4-5 中用户输入"切换普通模式"可降级
- **`_find_change_dir` 透明化**：返回选中目录时输出提示信息

### 五、验证增强
- **validate 检查 AND 数量**：校验每个 Scenario 的 AND ≤ 5 条
- **trace 正则重构**：用结构化解析替代跨行 DOTALL 正则
- **archive 冲突检测**：合并 specs 时检测重复 Requirement，标注而非静默追加

### 六、文档与生态
- **CHANGELOG.md**：独立版本历史文件
- **故障排除指南**：`TROUBLESHOOTING.md`，覆盖 Unicode/路径/权限等常见问题
- **示例项目**：`examples/hello-stdd/` 完整演示项目
- **扩展开发文档**：`EXTENDING.md`，说明如何新增平台/语言规范/失败模式

## Capabilities

### Modified Capabilities
- `CLI`：架构重构（模块化 + 测试 + dry-run/verbose + rollback/diff 命令）
- `SKILL`：平台同步机制 + 内容 DRY + CLI 桥接
- `STATE`：`_find_change_dir` 透明化
- `CONFIG`：配置拆分
- `VALIDATE`：AND 数量校验 + trace 正则重构 + archive 冲突检测

### New Capabilities
- `ROLLBACK`：从 archive 恢复到 changes/
- `DIFF`：spec↔test↔code 差异对比
- `ABORT`：放弃变更命令
- `DOCS`：CHANGELOG + TROUBLESHOOTING + EXTENDING + 示例项目

## Impact

**代码层面**：
- `bin/stdd` → `stdd/cli/` 包拆分（~5-8 个模块文件）
- 新增 `tests/` 目录（CLI 单元测试，预计 15-25 个测试文件）
- 新增 `examples/hello-stdd/` 示例项目
- 新增 `CHANGELOG.md`、`TROUBLESHOOTING.md`、`EXTENDING.md`
- 核心 Skill 文件重构（提取共享内容）
- 平台 Skill 生成逻辑修改（`install` 命令）
- 总变更：约 15-20 个文件，净增 ~800-1200 行

**配置层面**：
- `config.yaml`（103行）拆分为 `config.d/` 下 4 个文件
- 向后兼容：CLI 优先读 `config.d/`，fallback 读 `config.yaml`

**基础设施**：
- 新增依赖：pytest（测试框架）
- Python 版本要求不变（3.10+）

## Success Criteria

**CLI 架构**：
- [ ] `bin/stdd` 入口保留，内部委托到 `stdd/cli/` 包
- [ ] 所有 7 个子命令有独立模块，可单独导入和测试
- [ ] `stdd --dry-run <command>` 输出将执行的操作但不实际修改文件系统
- [ ] `stdd --verbose <command>` 输出 DEBUG 级别详细信息

**测试**：
- [ ] CLI 单元测试覆盖率 ≥ 70%
- [ ] 每个子命令至少 2 个测试案例（正常路径 + 异常路径）
- [ ] `pytest tests/` 全量通过

**新命令**：
- [ ] `stdd rollback my-feature` 从 archive 恢复到 changes/（含日期前缀）
- [ ] `stdd diff my-feature` 显示 TC 覆盖差异表
- [ ] `/stdd-abort` 清理 change 目录并提示用户

**Skill 同步**：
- [ ] 修改核心 Skill 后，`stdd install` 自动同步到平台 Skill
- [ ] 平台 Skill 不再手动维护独立副本

**配置拆分**：
- [ ] `config.d/` 目录下存在 project/gates/long_range/quality 四个 yaml
- [ ] 旧 `config.yaml` 仍可被读取（向后兼容）

**验证增强**：
- [ ] `stdd validate` 对超过 5 条 AND 的 Scenario 产生警告
- [ ] `stdd trace` 使用结构化解析，不依赖跨行正则
- [ ] `stdd archive` 合并 specs 时检测重复 Requirement 并提示用户

**文档**：
- [ ] CHANGELOG.md 包含 V1.0 至 V2.0 的完整版本历史
- [ ] TROUBLESHOOTING.md 覆盖 ≥5 个常见问题
- [ ] EXTENDING.md 覆盖平台/语言/失败模式 3 个扩展点
- [ ] examples/hello-stdd/ 可独立运行演示完整 6 阶段流程
