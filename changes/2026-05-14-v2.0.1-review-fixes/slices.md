# V2.0.1 切片执行计划

| # | 优先级 | TC 覆盖 | 实现目标 | 依赖 |
|---|--------|---------|---------|------|
| 1 | P0 | TC-CLI-001~005 | M1/M5/M6/M7/M3/M4 代码健壮性修复 | 无 |
| 2 | P0 | TC-CLI-006~009 | M8 --dry-run 支持 init/new/rollback/abort | 1 |
| 3 | P0 | TC-CONFIG-001~002, TC-DOCS-001~003 | H3 删除 config.yaml + M16 Skills 引用更新 + H1 README + L16 AGENTS | 无 |

## Slice 1: 代码健壮性修复（6项）

### M1: 异常处理显示 traceback
- `stdd/cli/__init__.py` L133-135 → 使用 `traceback.print_exc()` 替代单行错误消息

### M5: 尾随管道修复
- `stdd/cli/commands/trace.py` L64 → `(.+)` 改为 `([^|]+)` 排除尾随 `|`
- `stdd/cli/commands/diff.py` L49 → `(.+)` 改为 `([^|]+)` 排除尾随 `|`

### M6: 统一案例标题正则
- `stdd/cli/commands/trace.py` L49 → 正则改为同时匹配 em dash 和连字符 `[—\-]`

### M7: finder 精确匹配检查状态文件
- `stdd/cli/finder.py` L13-15 → 精确匹配增加 `.stdd.yaml` 存在性检查

### M3: 移除 install.py 死代码
- `stdd/cli/commands/install.py` L141-142 → 删除无效的 `_shared/` 守卫

### M4: read_config 类型安全
- `stdd/cli/utils.py` L53 → 验证 `yaml.safe_load()` 返回值为 dict 后再合并

## Slice 2: --dry-run 实现（4个命令）

### M8: init/new/rollback/abort 支持 --dry-run
- `stdd/cli/commands/init.py` → 检测 `args.dry_run`，打印操作预览后 return
- `stdd/cli/commands/new.py` → 同上
- `stdd/cli/commands/rollback.py` → 同上
- `stdd/cli/commands/abort.py` → 同上

## Slice 3: 配置与文档修复（5项）

### H3: 删除旧 config.yaml
- 删除 `.stdd/config.yaml`

### M16: Skills 引用 config.d/
- `build.md` L29 → `config.yaml` → `config.d/project.yaml`
- `verify.md` L20, L43 → `config.yaml` → `config.d/quality.yaml`
- `spec.md` L124 → `config.yaml` → `config.d/long_range.yaml`

### H1: README.md 版本更新
- 版本声明 V1.4 → V2.0
- 补充新命令、config.d/、pytest 测试框架

### L16: AGENTS.md 结构更新
- 目录结构图增加 stdd/cli/、config.d/、_shared/
