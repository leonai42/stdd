# V2.4：自学习经验库 + AI 辅助增强 + CI/CD 集成

## Why

STDD V2.3 建立了 11 类失败模式的**静态分类**体系。但核心问题未解决：AI 今天在项目 A 中犯的错误（如 async 函数裸 except 遗漏 CancelledError），明天在同一个项目的不同 change 中会再次犯同样的错误。缺乏**跨 change 的经验积累和复用机制**。

同时，当前 Phase 2（SPEC）和 Phase 3（SLICE）高度依赖 AI 从零开始理解和生成，缺少从已有结构化数据（proposal 字段、历史经验）中自动推导的能力，导致：(1) 生成耗时长、容易遗漏；(2) 用户需要从"审阅者"变成"写作者"，负担重。

此外，STDD 的质量检查（validate / pytest / diff / 11 类失败检查）目前只能在 AI 对话中手动触发，缺少与标准 CI/CD 流程（GitHub Actions / pre-commit hook / PR Bot）的集成，导致质量门难以嵌入团队现有工程流程。

## What Changes

### 模块一：自学习经验库 v1
- 新增 `.stdd/experiences/` 目录，存储结构化的经验条目（YAML frontmatter + Markdown body）
- 新增 `stdd experience` CLI 命令组（list / add / stats / pull / export）
- Phase 5 VERIFY 完成后自动检测新失败模式，创建经验条目
- Phase 4 BUILD 开始前自动加载匹配当前切片上下文的经验
- 经验生命周期管理：发现 → 记录 → 验证 → 沉淀（V2.5 扩展到共享/融合/退场）

### 模块二：Spec 自动补全（Phase 2 增强）
- Phase 2 新增自动提取步骤：从 proposal.md 的结构化字段中提取 Capabilities / What Changes / Success Criteria，自动生成 spec 草稿
- 每个生成项标注置信度（✓ 高 / ⚠ 低）
- 用户角色从「写 spec」变为「审 spec」
- 新增 `stdd extract-proposal` CLI 辅助命令

### 模块三：智能切片推荐（Phase 3 增强）
- Phase 3 切片逻辑从简单分组升级为五步分析：依赖图构建 → 风险评分 → 工作量预估 → 智能分组 → 并行化建议
- slices.md 模板增强，增加风险等级、预估工时、并行组、理由列
- 新增 `stdd dependency-graph` CLI 辅助命令

### 模块四：CI/CD 集成
- 新增 `stdd ci` CLI 命令组（init / generate workflow|pre-commit|pr-template / check-failures）
- 生成 GitHub Actions workflow 模板（validate → pytest --cov → diff → lint → 失败检查）
- 生成 Pre-commit hook 配置模板
- 生成 PR Bot 自动评论模板
- `stdd ci check-failures`：CLI 版的 11 类失败检查（确定性子集，覆盖约 60% 结构性问题）

## Capabilities

### Modified Capabilities

- **Phase 2 SPEC 技能**：替换 Step 2-3（手动生成 design.md + specs）为自动提取 + 置信度标注 + 用户审核流程
- **Phase 3 SLICE 技能**：替换 Step 2（简单分组）为五步智能切片分析
- **Phase 4 BUILD 技能**：新增 Step 0.5（加载匹配经验）和 RED/GREEN 中的经验检查点
- **Phase 5 VERIFY 技能**：新增 Step 3.5（自动记录/更新经验），test-report 增加经验库更新章节
- **proposal.md 模板**：关键字段增加结构化提取标记
- **slices.md 模板**：增加 risk/effort/parallel_group/rationale 列
- **test-report.md 模板**：增加经验库更新章节
- **spec.md 模板**：增加置信度标注标记

### New Capabilities

- **经验库 CLI**：`stdd experience list|add|stats|pull|export` — 管理项目级 AI 经验
- **提案提取 CLI**：`stdd extract-proposal` — 从 proposal.md 提取结构化 JSON/YAML
- **依赖图 CLI**：`stdd dependency-graph` — 从 specs 构建 capability 依赖关系图
- **CI/CD CLI**：`stdd ci init|generate|check-failures` — 生成 CI 配置并运行检查
- **经验库配置**：`.stdd/config.d/experience.yaml` — 经验库行为配置
- **经验索引**：`.stdd/experiences/.experience-index.yaml` — 快速查找索引

## Impact

**代码层面**：
- 新增 4 个 CLI 命令模块：`stdd/cli/commands/experience.py`, `extract_proposal.py`, `dependency_graph.py`, `ci.py`
- 修改 `stdd/cli/__init__.py`（注册 4 个新命令）
- 新增 4 个测试文件：`tests/commands/test_experience.py`, `test_extract_proposal.py`, `test_dependency_graph.py`, `test_ci.py`
- 新增测试文件

**配置层面**：
- 新增 `.stdd/config.d/experience.yaml`
- 修改 `.stdd/config.d/project.yaml`（增加 experiences_dir）
- 修改 `.stdd/config.d/quality.yaml`（增加 ci 配置段）

**模板层面**：
- 新增 5 个模板：`spec-draft.md`, `github-actions-workflow.yml`, `pre-commit-config.yaml`, `pr-comment.md`, `failure-check-report.md`
- 修改 4 个模板：`proposal.md`, `slices.md`, `test-report.md`, `spec.md`

**技能层面**：
- 修改 4 个技能文件：`spec.md`, `slice.md`, `build.md`, `verify.md`
- 新增 `_shared/` 片段（可选，用于避免技能膨胀）

**基础设施**：
- 新增 `.stdd/experiences/` 目录（项目级经验存储）

## Success Criteria

- [ ] **SC-1**：`stdd experience add --category cascading_errors --pattern "test"` 成功创建经验条目，`stdd experience list` 正确过滤和显示
- [ ] **SC-2**：`stdd experience export --format json` 输出有效 JSON 且路径/IP/域名已被脱敏
- [ ] **SC-3**：`stdd extract-proposal <change> --format json` 从 proposal.md 正确提取 capabilities / what_changes / success_criteria 结构化数据
- [ ] **SC-4**：`stdd dependency-graph <change> --format json` 正确输出 capability 依赖图（nodes + edges + zero_dependency）
- [ ] **SC-5**：`stdd ci init` 生成 `.github/workflows/stdd-quality.yml` 和 `.pre-commit-config.yaml`，YAML 语法有效
- [ ] **SC-6**：`stdd ci check-failures` 对已知问题的 change 至少检测出 60% 以上的问题
- [ ] **SC-7**：Phase 2 技能增强后，AI 能根据 proposal 自动生成带 ✓/⚠ 置信度标签的 spec 草稿
- [ ] **SC-8**：Phase 3 技能增强后，AI 能输出包含风险等级、预估工时、并行组、理由列的 slices.md
- [ ] **SC-9**：Phase 4 技能增强后，AI 在执行 BUILD 前自动加载并引用匹配的经验
- [ ] **SC-10**：Phase 5 技能增强后，11 类失败检查完成后自动创建/更新经验条目，并更新 `.experience-index.yaml`
- [ ] **SC-11**：全量现有测试通过（`pytest tests/ -v`），现有 11 个 CLI 命令不受影响
- [ ] **SC-12**：新增 4 个命令的测试全部通过（target: 35+ 用例）
