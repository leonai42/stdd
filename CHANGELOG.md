# STDD 变更日志 / Changelog

## V2.3 (2026-05-18) — 基础配套完善 / Foundation Completion

### 多语言规范 / Multi-Language Standards
- 新增 Java 开发规范：JUnit 5 + Mockito + Checkstyle
- 新增 Go 开发规范：testing + testify + golangci-lint
- 新增 Rust 开发规范：cargo test + clippy + rustfmt
- 新增 TypeScript 开发规范：Jest + ESLint + Prettier
- 语言规范从 1 门扩展到 5 门（Python / Java / Go / Rust / TypeScript）

### 平台扩展 / Platform Expansion
- 新增 Cursor 平台支持（`stdd install cursor`）
- 新增 GitHub Copilot 平台支持（`stdd install copilot`）
- 新增 Aider 平台支持（`stdd install aider`）
- 平台从 3 个扩展到 6 个（Claude Code / Cursor / Copilot / Aider / WorkBuddy / Trae）

### 配置模块化 / Config Modularization
- `config.yaml` 拆分为 `config.d/{project,gates,long_range,quality}.yaml`
- 向后兼容：`config.d/` 优先，自动 fallback 到 `config.yaml`

### Skill 标准化 / Skill Standardization
- 6 个阶段 Skill 统一 YAML frontmatter 格式
- `_shared/` 目录：确认门、模式选择、长程授权等 DRY 共享片段
- Skill-CLI 桥接：CLI 操作前后检查可用性和退出码

---

## V2.2 (2026-05-15) — 流程体验优化 / Process UX Optimization

### Gate 交互增强 / Gate Interaction Enhancement
- 确认门信息展示完善：结构化展示产出物 + 关键指标 + 确认清单
- 决策依据更清晰，减少用户认知负担

### 长程模式可靠性 / Long-Range Mode Reliability
- 长程模式状态下中途退出机制：输入"切换普通模式"可降级
- 长程预授权流程优化：A.流程决策 + B.操作类授权 + C.降级触发条件
- 降级条件：连续修复失败 3 次 / 测试通过率 <95% / 安全问题 / 预期外情况

---

## V2.1 (2026-05-14) — 方法论增强 + 全面修复 / Methodology Enhancement

### 代码审查 / Code Review (80 项评审问题修复)
- 修复代码质量问题：未使用变量、异常处理、日志级别、类型注解
- 修复文档问题：模板不一致、描述不准确、版本号同步
- 修复配置问题：路径统一、默认值补充

### 内置 Review 能力
- Phase 5 中新增内置 Review 步骤
- 三路并行审查机制（代码审查 / 测试审查 / 文档审查）
- V2.0 评审报告记录在 `review/V2.0-review-report.md`

### 质量体系
- 11 类失败模式检查全面覆盖
- 测试覆盖率诊断增强
- validate 命令检查 AND 数量上限（≤ 5 条）
- trace 命令逐行分段解析

---

## V2.0.1 (2026-05-14) — Review 修复 / Review Fixes

### 代码审查调整
- 17 项代码/文档/配置改进
- 配置路径统一修正
- 文档修复与版本同步

---

## V2.0 (2026-05-13) — 架构升级 / Architecture Upgrade

### CLI 架构
- 模块化拆分：`bin/stdd` 单文件（687行）→ `stdd/cli/` 包（8 个模块 + `__init__` 调度）
- 引入 pytest 测试框架，54 个测试案例，覆盖率 ≥ 80%
- `--dry-run` 全局选项：预览操作但不修改文件系统
- `--verbose` / `-v` 分级日志（Python logging 模块）

### 新命令
- `stdd rollback <name>`：从 archive 恢复已归档的 change
- `stdd diff <name>`：显示 Spec Scenario ↔ TC 案例 ↔ 测试函数 ↔ 源码 的覆盖差异表
- `stdd abort <name>`：放弃变更并移至 archive/aborted/

### Skill 系统
- 核心 Skill 作为唯一来源，`stdd install` 自动生成平台 Skill（含 frontmatter）
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

## V1.4 (2026-05-14) — Skill 版本同步 / Skill Version Sync

- Skill 版本号同步至 V1.4.0
- README.md 中 ASCII 流程图替换为文本引用
- AGENTS.md 更新规则链接

---

## V1.2.1 + V1.3 (2026-05-14) — 关键修复与质量提升 / Critical Fixes & Quality

### 修复 / Fixes
- archive 命令使用 `change_dir.name`（含日期前缀）而非 `args.name`
- archive 操作顺序：合并 specs → 更新状态 → 移动目录（修复移动后状态更新失败）
- validate 正则修复：GIVEN/WHEN/THEN 数量检查使用正确比较符
- trace 扩展搜索范围到 `specs/` 目录

### 改进 / Improvements
- change 名称正则验证：`^[a-zA-Z0-9][-a-zA-Z0-9_.]{1,49}\Z`
- 所有 8 个公开函数添加类型注解
- `main()` 调度增加 try/except 异常捕获
- init 命令支持 `--force` 覆盖
- install 增加源文件存在性检查
- status 显示长程模式状态
- .stdd.yaml 增加 version 字段
- 模板增加 AND 使用示例和优先级依赖示例

---

## V1.2 (2026-05-08) — 验证增强 / Verification Enhancement

- Phase 5 新增 E2E 测试支持（可配置）
- 覆盖率诊断（不阻断，仅报告）
- 多 Python 版本兼容性测试
- 失败模式从 9 类扩展至 11 类：(j) 覆盖真空、(k) 契约断层
- 基于 FPPT 项目验收测试回溯的 16 个实测问题改进

---

## V1.1 (2026-05-06) — 长程开发 / Long-Range Development

- 长程模式：Phase 3-5 连续自动执行
- 预授权清单（流程决策 + 操作授权）
- 失败模式从 5 类扩展至 9 类：(f) 运行时行为偏差、(g) 管线断链、(h) 内容质量偏差、(i) 指令衰减
- 基于 FPPT 项目 Phase 2-5 实测中发现的 4 个 TDD 系统性盲区

---

## V1.0 (2026-05-03) — 初始版本 / Initial Release

- 6 阶段 STDD 流程：UNDERSTAND → SPEC → SLICE → BUILD → VERIFY → DELIVER
- CLI 工具：init、new、validate、status、archive、trace、install（7 个命令）
- 6 个核心 Skill（Markdown 指令）
- 3 道强制确认门（Gate 1/2/3）
- 模板系统：proposal、design、spec、test-plan、tasks、slices、test-report
- 3 平台支持：Claude Code、WorkBuddy、Trae
- Python 开发规范
- 5 类初始故障模式检查
