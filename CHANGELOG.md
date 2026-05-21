# STDD 变更日志 / Changelog

## V2.5 (2026-05-21) — 经验生命周期闭环 + 社区经验池 + 多Agent适配 / Experience Lifecycle + Community Pool + Multi-Agent Support

### 经验生命周期状态机 / Experience Lifecycle FSM
- 5 状态有限状态机：discovered → verified → deposited → shared → merged/retired
- 新增 `experience verify/deposit/retire` 子命令
- 自动提升逻辑：occurrences>=2 + confidence>=0.7 → verified; occurrences>=3 + confidence>=0.8 → deposited
- `experience list` 默认隐藏 retired，`--all` 显示全部

### CI 检查增强 / CI Check Enhanced
- 检查注册表模式：`CHECKS` 列表驱动聚合，7 项检查
- 新增 `check-scope`：proposal capability 声明 vs git diff 范围交叉验证
- 新增 `check-coverage`：pytest JSON 覆盖率 vs quality.yaml 阈值（默认 80%）
- 新增 `check-contracts`：跨 capability 契约字段一致性检查
- 新增子命令：`ci check-scope/check-coverage/check-contracts`
- Graceful degradation：无数据时 SKIP 而非 FAIL

### 跨 Session 状态恢复 / Session Resume
- 新增 `state.py`：`.stdd.yaml` 读写 resume_context/active_slice/last_action/last_modified
- 向后兼容：V2.4 .stdd.yaml 新字段为 null

### Gate 文件确认 / Gate File Confirmation
- 新增 `gate.py` CLI：`stdd gate approve <change> --gate <N>`
- 文件 token 机制：`GATE<N>_APPROVED` 空文件等效于确认
- `gates.yaml` 新增 `confirmation.channels` 配置段（dialog/file_token/cli）

### 社区经验共享池 / Community Experience Pool
- 零后端设计：GitHub Releases (CDN) + Gitee 镜像 + Issues (投票 UI)
- 双源下载 fallback：主源 5 秒超时自动切换镜像
- `experience pull`：全量下载 + 去重 + 投票元数据同步
- `experience export --publish`：脱敏 + 打包 tar.gz + lifecycle→shared
- 新增投票字段：community_votes_useful/unuseful + adoption_count
- 新增 `curate.py`：官方维护者工具链 pull/deduplicate/review/pack
- `experience.yaml` 新增 `community` 配置段

### Proposal 扩展提取 / Extract Proposal Extended
- 新增 4 字段提取：Constraints / Stakeholders / RiskAreas (结构化) / NonGoals
- 向后兼容：V2.4 proposal 缺失字段 → 空数组
- `proposal.md` 模板增加新字段段落

### 非代码 Change 支持 / Non-Code Change Support
- `project_type` 字段：经验创建时自动检测（python/go/static_site/docs/config）
- `build.md` Step 0.5：按 project_type 过滤经验加载
- `verify.md`：非代码 change 替代检查清单（5 项：链接有效/范围一致/内部引用/内容完整/TC 覆盖）
- 向后兼容：project_type=null → 通配加载

### 并行切片指南 / Parallel Slice Guide
- `build.md` 新增并行执行策略：parallel_group 识别 → 子 agent 派发 → 结果合并
- 串行 fallback：无 delegation 能力时按拓扑顺序执行

### 技能系统 / Skill System
- `build.md`：Step 0.5 +project_type 过滤 + 并行执行策略
- `verify.md`：Step 3 后 + 非代码检查清单分支

### 测试 / Tests
- 新增 46 个测试用例
- 全量回归 155/155 通过（零回归）

---

## V2.4 (2026-05-21) — AI 辅助增强 + 自学习经验库 + CI/CD 集成 / AI-Assisted Enhancement + Self-Learning Experience Library + CI/CD Integration

### 自学习经验库 / Self-Learning Experience Library
- 新增 `stdd experience` CLI 命令组：list / add / stats / export / pull（5 子命令）
- 经验数据模型：YAML frontmatter + Markdown body，11 类失败模式分类
- 自动维护 `.experience-index.yaml` 索引（按 category/language/lifecycle/severity 分组）
- 经验自动记录（Phase 5 VERIFY）和智能加载（Phase 4 BUILD）
- 导出脱敏：路径/IP/域名自动替换占位符，支持 `--no-sanitize` 保留原始内容
- 配置：`.stdd/config.d/experience.yaml`

### Spec 自动补全 / Spec Auto-Complete
- 新增 `stdd extract-proposal` CLI：从 proposal.md 提取结构化数据（JSON/YAML）
- `spec.md` 技能增强：自动生成 spec 草稿 + 置信度标签（✓高/⚠低）
- 新增模板：`.stdd/templates/spec-draft.md`
- `proposal.md` 模板增加 STDD-MARKER 提取标记

### 智能切片推荐 / Smart Slice Recommendation
- 新增 `stdd dependency-graph` CLI：构建 spec 依赖图（JSON/DOT/Text 三格式）
- 环检测 + 零依赖节点识别 + 拓扑排序
- `slice.md` 技能增强：五步分析（依赖图 → 风险评分 → 工作量预估 → 智能分组 → 并行化建议）
- `slices.md` 模板增强：增加 risk/effort/parallel_group/rationale 列

### CI/CD 集成 / CI/CD Integration
- 新增 `stdd ci` CLI 命令组：init / generate / check-failures（3 子命令）
- GitHub Actions workflow 模板（validate + test + diff + lint + typecheck + failure-check）
- Pre-commit hook 模板（validate + lint）
- PR comment 模板（质量门禁结果展示）
- CLI 确定性子集检查（~60% 失败模式覆盖：文件存在性/TC-ID 唯一性/SHALL 关键字/AND 计数）

### 技能系统 / Skill System
- `build.md`：新增 Step 0.5 经验加载 + RED/GREEN 经验检查点
- `verify.md`：新增 Step 3.5 经验自动记录/更新 + 步骤从 6 增至 7
- `spec.md`：替换 Step 2-3 为自动提取流程，用户角色从"写 spec"变为"审 spec"
- `slice.md`：替换 Step 2 为五步分析
- 新增模板：`spec-draft.md`（AI 生成 spec 草稿）

### 测试 / Tests
- 新增 45 个测试用例（test_experience: 13, test_extract_proposal: 7, test_dependency_graph: 10, test_ci: 14 + 1）
- 全量回归 109/109 通过（0 回归，现有 11 个命令不受影响）

---

## V2.5 (计划中) — 跨平台适配与工具化增强 / Cross-Platform Adaptation & Tooling Enhancement

> **来源**：Hermes Agent 集成反馈（10 维度对比）+ STDD Playground 首次实战复盘。
> **预估工时**：9.2 人天。详见 VISION.md 第九章。

### P5 工具化：11 类失败模式 CLI 预检扩展（P0）
- 新增 `stdd ci check-scope`：(b) 范围蔓延 — `git diff --stat` 对比 proposal 声明范围
- 新增 `stdd ci check-coverage`：(j) 覆盖真空 — 解析 `pytest --cov` 识别 spec 无覆盖模块
- 新增 `stdd ci check-contracts`：(k) 契约断层 — 校验相邻 capability 字段类型/命名一致性
- 总覆盖率目标：从 ~60% 提升到 ~80%

### 跨 Session 状态恢复（P0）
- `.stdd.yaml` 新增 `resume_context` / `active_slice` / `last_action` / `last_modified` 字段
- 任意 AI session 读取后无歧义恢复，无需翻找 change 目录

### 并行切片执行指南（P1）
- `build.md` skill 增加并行执行策略：同 `parallel_group` 切片可并行派发
- 主 Agent 协调 + 并行切片独立执行 + 统一 REFACTOR

### Gate 确认通道多样化（P1）
- 新增文件式 Gate 确认：创建 `GATE<N>_APPROVED` token 文件即可确认
- CLI：`stdd gate approve <change-name> --gate <N>`
- 与对话确认等价，底层写入 `.stdd.yaml` 时间戳

### 模板填充工具化（P1）
- `extract-proposal` 扩展提取字段：Constraints / Stakeholders / Risk Areas / NonGoals
- 提取结果作为模板变量填充，减少 AI "理解偏差"

### 文件驱动阶段切换（P2）
- 标准化文件信号：`.stdd.yaml` 的 `next_phase` 字段替代斜杠命令
- 任何能读写文件的 AI Agent 都能参与 STDD 流程（去平台依赖）

### 非代码类 Change 支持（P1 · 来自 Playground 实战）
- `verify.md` 增加非代码检查清单：纯前端/文档/Skill 类 change 的 5 项替代检查维度
- 经验库 YAML 增加 `project_type` 字段（python/go/static_site/docs/config），防止跨类型经验污染
- 覆盖 ~30-40% 的非代码长尾 change，让经验库从此类 change 也能正常积累经验

---

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
