# V1.2.1+V1.3 任务清单

## 1. V1.2.1 关键修复（P0）

- [x] 1.1 修复 archive 目录名 Bug（`args.name` → `change_dir.name`）
- [x] 1.2 修复 archive 操作顺序（合并 specs → 更新状态 → 移动目录）
- [x] 1.3 .stdd.yaml 增加 `version: "1.2"` 字段
- [x] 1.4 修复 validate GIVEN/WHEN/THEN 正则逻辑（`!=` → `<`）
- [x] 1.5 修复 trace 搜索范围（增加 `specs/` 目录）
- [x] 1.6 config.yaml 版本号更新为 `"1.2.1"`

## 2. V1.3 CLI 质量提升（P1）

- [x] 2.1 CLI 公共函数增加类型注解
- [x] 2.2 CLI 关键 I/O 操作增加异常处理
- [x] 2.3 init 增加 `--force` 选项
- [x] 2.4 new 增加 change_name 格式验证
- [x] 2.5 install 增加源文件存在性检查
- [x] 2.6 status 增加 long_range 模式显示

## 3. V1.3 模板与文档优化（P2）

- [x] 3.1 spec.md 模板增加 AND 多条件示例
- [x] 3.2 tasks.md 模板增加优先级和依赖示例
- [x] 3.3 README.md 六阶段去重（改为引用 STDD.md）
- [x] 3.4 STDD.md 无需修改（已包含完整流程描述）

## 4. 测试与验证

- [x] 4.1 手动验证 P0 修复（TC-CLI-001~005, TC-STATE-001~002, TC-CONF-001）✅ 全部通过
- [x] 4.2 手动验证 P1 增强（TC-CLI-006~014）✅ 全部通过
- [x] 4.3 手动验证 P2 模板/文档（TC-TMPL-001~002, TC-DOCS-001）✅ 全部通过
