# 变更提案: V2.0.1 评审问题修复

> 基于 V2.0 全面技术评审报告（39项发现）的统一修复

## Why

V2.0 架构升级整体成功，但三路并行审查发现了 1个严重问题、3个高危问题、16个中等问题。这些问题影响可用性（模板缺失）、可维护性（死代码）、健壮性（异常吞没）和文档准确性。

## What Changes

### 一、严重/高危修复（4项）
- **C1**: 创建缺失的4个模板文件：tasks.md、slices.md、design-adjustments.md、test-report.md
- **H1**: 更新 README.md 到 V2.0（新命令、config.d/、pytest框架）
- **H2**: 重新安装 Claude Code Skills（同步 V2.0 Skill 更新）
- **H3**: 删除旧的 config.yaml 避免版本不一致

### 二、代码健壮性修复（7项）
- **M1**: `__init__.py` 异常处理增加 traceback 输出
- **M2**: `archive.py` 合并前先备份，减少部分失败影响
- **M3**: 移除 `install.py` 中的死代码 _shared 守卫
- **M4**: `read_config` 增加 YAML 类型检查（拒绝非 dict 返回值）
- **M7**: `finder.py` 精确匹配增加 `.stdd.yaml` 存在性检查
- **M5**: 修复 trace.py / diff.py 中 Markdown 表格尾随管道捕获
- **M6**: 统一 trace.py 和 diff.py 的案例标题正则

### 三、--dry-run 实现（1项）
- **M8**: 为 init、new、rollback、abort 命令实现 --dry-run

### 四、测试补充（4项）
- **M12**: 补充 validate 未覆盖的 6 个验证路径测试
- **M13**: 补充 WorkBuddy 安装测试
- **M14**: 补充 status 输出内容断言
- **M11**: 补充 CLI 集成测试（通过 main() 入口）

### 五、文档修复（2项）
- **M16**: 更新 Skills 中 config.yaml 引用为 config.d/
- **L16**: 更新 AGENTS.md 项目结构图

## Impact

- 修改文件：~15 个 Python 文件 + 5 个 Skill 文件 + 3 个文档 + 4 个新模板
- 新增测试：~10 个测试函数
- 无破坏性变更

## Success Criteria

- [ ] 4 个缺失模板文件创建完毕
- [ ] README.md 版本号更新为 V2.0
- [ ] old config.yaml 已删除
- [ ] 所有中高危问题代码修复完成
- [ ] 测试覆盖率维持在 ≥80%
- [ ] 全部测试通过
- [ ] Claude Code Skills 已更新
