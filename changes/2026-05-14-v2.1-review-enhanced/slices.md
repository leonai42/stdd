# V2.1 切片执行计划

| # | 优先级 | 涉及需求 | 实现目标 | 依赖 |
|---|--------|---------|---------|------|
| 1 | P0 | CODE-001~010 | 代码高危修复：dry-run/None防护/输出一致性/死代码/异常处理 | 无 |
| 2 | P0 | TEST-001~008 | 测试补充：~15个测试覆盖修复路径 | 1 |
| 3 | P0 | DOCS-001~010 | 文档修复：版本号/config引用/平台Skills/命令补齐 | 无 |
| 4 | P1 | METHOD-001~004 | 方法论增强：VERIFY Review/Phase1审查/Phase2审查/quality.yaml | 无 |

## Slice 1: 代码高危修复（10项需求）

- install.py --dry-run 支持
- yaml.safe_load() None 防护（validate/status/archive/rollback/abort 共6处）
- archive.py dry-run 输出改用 print()
- fix_windows_encoding 防御性检查
- trace.py 移除 specs/ 空操作搜索
- __init__.py 清理重复 import 和 unused Optional import
- diff.py 异常日志记录
- rollback.py 支持 aborted/ 搜索
- archive.py 状态更新顺序修复
- abort.py EOFError 处理

## Slice 2: 测试补充（8项需求）

- 4个 --dry-run 测试（abort/new/rollback/install）
- read_config 类型安全测试
- finder 精确匹配无状态文件测试
- 异常处理 traceback 测试
- validate 6个未覆盖路径测试
- status 输出断言
- WorkBuddy 安装测试

## Slice 3: 文档修复（10项需求）

- DESIGN.md: 版本+config引用+命令表+目录树+版本历史
- DEPLOY.md: 版本+config引用+命令表+FAQ
- 平台 Skills (12文件): config.yaml→config.d/
- long-range-auth.md: config.yaml→config.d/
- 示例项目 AGENTS.md: 结构同步
- AGENTS.md: 绝对路径修复
- TROUBLESHOOTING.md: 移除过时条目
- EXTENDING.md: 路径更新
- 模板计数统一 (8→9)

## Slice 4: 方法论增强（4项需求）

- verify.md: 新增 Step 0 并行 Review
- understand.md: 新增 Step 3.5 Proposal 审查
- spec.md: 新增 Step 4.5 Design/Spec 审查
- quality.yaml: 新增 review 阈值配置
