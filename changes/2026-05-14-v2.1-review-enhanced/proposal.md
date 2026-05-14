# 变更提案: V2.1 全面修复 + 方法论增强

> V2.0.1 第二轮评审（80项发现）的全面修复 + STDD 方法论内置 Review 能力

## Why

V2.0 和 V2.0.1 两轮修复后，第二轮技术评审仍发现 80 项问题（3C + 18H + 32M + 27L）。这些问题的存在说明：
1. 单轮修复不够彻底，需要多轮 Review-Fix 循环
2. STDD VERIFY 阶段缺少系统化的代码/文档审查机制
3. Phase 1/2 产出物（proposal/design/specs）未经审查就直接进入实现

需要在两个层面解决：修复当前问题 + 建立长期质量防线。

## What Changes

### 一、V2.0.2 问题修复（80项）

**严重 (3)**:
- DESIGN.md 标题 V1.2→V2.0
- DEPLOY.md 标题 V1.2→V2.0
- DESIGN.md 版本历史补充 V1.4/V2.0/V2.0.1

**代码高危 (7)**:
- install.py --dry-run 支持
- yaml.safe_load() None 防护（6处）
- archive.py dry-run 输出一致性
- fix_windows_encoding buffer 存在性检查
- trace.py specs/ 搜索空操作修复
- __init__.py 重复 import 清理

**测试高危 (6)**:
- main() 入口测试
- --dry-run 测试补充（abort/new/rollback/install）
- read_config 类型安全测试
- finder 精确匹配无状态文件测试
- 异常处理 traceback 测试

**文档高危 (5)**:
- 12 个平台 Skill 文件 config.yaml→config.d/
- DESIGN.md 3 处 config.yaml 引用更新
- DEPLOY.md 5 处 config.yaml 引用更新
- long-range-auth.md 模板 config.yaml 引用
- 示例项目 AGENTS.md 结构同步

**中低优先级 (59)**: 代码、测试、配置、文档全部中低问题

### 二、V2.1 方法论增强（3项）

**VERIFY 增加并行 Review (Step 0)**:
- 启动 3 个并行审查代理：代码质量、测试/配置、文档/Skills
- 按 severity 分类 → C/H 自动修复 → M/L 记录
- 迭代直到满足阈值：C=0, H≤3, M≤10（可配置）
- 结果汇总到 test-report.md 新章节

**Phase 1 增加提案审查 (Step 3.5)**:
- 生成 proposal.md 后，自动审查完整性
- 检查：Why 是否清晰、What Changes 是否具体、Success Criteria 是否可验证
- 自动修复问题后再提交用户确认

**Phase 2 增加设计审查 (Step 4.5)**:
- 生成 design.md + specs 后，自动审查
- 检查：需求覆盖完整性、Scenario GIVEN/WHEN/THEN 完备性、TC-ID 一致性
- 自动修复问题后再提交用户确认

## Impact

- 修改 Python 文件：~12 个
- 修改文档文件：~8 个（DESIGN、DEPLOY、STDD、TROUBLESHOOTING、EXTENDING、示例项目）
- 修改 Skill 文件：3 个（verify.md、understand.md、spec.md）
- 修改平台 Skill 文件：12 个（config.yaml→config.d/）
- 修改配置：1 个（quality.yaml 增加 review 阈值）
- 删除文件：12 个过时平台 Skill（重新生成替代）
- 新增测试：~15 个

## Success Criteria

- [ ] 80 项评审问题全部修复或记录为已知限制
- [ ] 代码修复后 54 个回归测试全部通过
- [ ] 新增测试覆盖关键修复路径
- [ ] VERIFY.md 包含并行 Review 步骤
- [ ] understand.md 包含提案审查步骤
- [ ] spec.md 包含设计审查步骤
- [ ] quality.yaml 包含 review 阈值配置
- [ ] 12 个平台 Skill config.yaml 引用全部更新
