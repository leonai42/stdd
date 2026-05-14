# STDD 变更日志

## V2.0 (2026-05-14) — 架构升级

### CLI 架构
- 模块化拆分：`bin/stdd` 单文件（687行）→ `stdd/cli/` 包（8个模块）
- 引入 pytest 测试框架，54 个测试案例，覆盖率 ≥ 80%
- `--dry-run` 全局选项：预览操作但不修改文件系统
- `--verbose` / `-v` 分级日志（Python logging 模块）

### 新命令
- `stdd rollback <name>`：从 archive 恢复已归档的 change
- `stdd diff <name>`：显示 Spec Scenario ↔ TC 案例 ↔ 测试函数 ↔ 源码 的覆盖差异表
- `stdd abort <name>`：放弃变更并移至 archive/aborted/

### Skill 系统
- 核心 Skill 作为唯一来源，`stdd install` 自动生成平台 Skill（含 frontmatter）
- `_shared/` 目录：确认门、模式选择、长程授权等共享片段 DRY
- 长程模式中途退出：输入"切换普通模式"可降级
- Skill-CLI 桥接：CLI 操作前后检查可用性和退出码

### 配置
- `config.yaml` 拆分为 `config.d/{project,gates,long_range,quality}.yaml`
- 向后兼容：config.d/ 优先，自动 fallback 到 config.yaml
- `_find_change_dir` 模糊匹配时输出提示信息

### 验证增强
- validate 检查 AND 数量上限（≤ 5 条）
- trace 逐行分段解析（不再依赖 DOTALL 正则）
- archive 合并 specs 时检测重复 Requirement 并输出冲突警告

### 文档
- 新增 CHANGELOG.md、TROUBLESHOOTING.md、EXTENDING.md
- 新增 examples/hello-stdd/ 示例项目

---

## V1.4 (2026-05-14) — Skill 版本同步

- Skill 版本号同步至 V1.4.0
- README.md 中 ASCII 流程图替换为文本引用
- AGENTS.md 更新规则链接

---

## V1.2.1 + V1.3 (2026-05-14) — 关键修复与质量提升

### 修复
- archive 命令使用 `change_dir.name`（含日期前缀）而非 `args.name`
- archive 操作顺序：合并 specs → 更新状态 → 移动目录（修复移动后状态更新失败）
- validate 正则修复：GIVEN/WHEN/THEN 数量检查使用正确比较符
- trace 扩展搜索范围到 `specs/` 目录

### 改进
- change 名称正则验证：`^[a-zA-Z0-9][-a-zA-Z0-9_.]{1,49}\Z`
- 所有 8 个公开函数添加类型注解
- `main()` 调度增加 try/except 异常捕获
- init 命令支持 `--force` 覆盖
- install 增加源文件存在性检查
- status 显示长程模式状态
- .stdd.yaml 增加 version 字段
- 模板增加 AND 使用示例和优先级依赖示例

---

## V1.2 (2026-05-08) — 验证增强

- Phase 5 新增 E2E 测试支持
- 覆盖率诊断（不阻断，仅报告）
- 多 Python 版本兼容性测试
- 2 项故障检测：e2e_test_failure、coverage_low

---

## V1.1 (2026-05-06) — 长程开发

- 长程模式：Phase 3-5 连续自动执行
- 预授权清单（流程决策 + 操作授权）
- 4 项故障检测：design_deviation、technical_blocker、iteration_cap、quality_regression

---

## V1.0 (2026-05-03) — 初始版本

- 6 阶段 STDD 流程：UNDERSTAND → SPEC → SLICE → BUILD → VERIFY → DELIVER
- CLI 工具：init、new、validate、status、archive、trace、install（7 个命令）
- 6 个核心 Skill（Markdown 指令）
- 3 道强制确认门（Gate 1/2/3）
- 模板系统：proposal、design、spec、test-plan、tasks、slices、test-report
- 3 平台支持：Claude Code、WorkBuddy、Trae
- Python 开发规范
- 5 类初始故障模式检查
