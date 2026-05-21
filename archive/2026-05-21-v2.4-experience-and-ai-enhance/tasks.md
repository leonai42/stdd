# V2.4 任务清单

## 1. 经验库核心（P0）

- [x] 1.1 创建 `.stdd/config.d/experience.yaml` 配置文件
- [x] 1.2 添加 `experiences_dir` 路径到 `.stdd/config.d/project.yaml`
- [x] 1.3 创建 `.stdd/experiences/.gitkeep` 目录种子
- [x] 1.4 实现 `stdd/cli/commands/experience.py` — `cmd_experience` 主调度
- [x] 1.5 实现 `stdd experience add` 子命令（含 category 校验、ID 自动生成、索引更新）
- [x] 1.6 实现 `stdd experience list` 子命令（含过滤和 table/json/yaml 格式）
- [x] 1.7 实现 `stdd experience stats` 子命令
- [x] 1.8 实现 `stdd experience export` 子命令（含脱敏逻辑）
- [x] 1.9 实现 `stdd experience pull` 子命令（V2.5 placeholder）
- [x] 1.10 实现 `.experience-index.yaml` 自动维护逻辑（重建、增量更新）
- [x] 1.11 实现经验索引重建（从 EXP 文件扫描恢复）

## 2. 经验库测试（P0）

- [x] 2.1 创建 `tests/commands/test_experience.py` — TC-EXP-001~011
- [x] 2.2-2.11 全部 13 个测试用例通过

## 3. 经验库技能集成（P1）

- [x] 3.1 修改 `.stdd/skills/build.md` — 新增 Step 0.5 经验加载
- [x] 3.2 修改 `.stdd/skills/build.md` — RED/GREEN 步骤中植入经验检查点
- [x] 3.3 修改 `.stdd/skills/verify.md` — 新增 Step 3.5 自动记录/更新经验
- [x] 3.4 修改 `.stdd/templates/test-report.md` — 新增"经验库更新"章节
- [x] 3.5 手工审查 build.md 和 verify.md 增强文本一致性

## 4. Spec 自动补全 CLI（P0）

- [x] 4.1 实现 `stdd/cli/commands/extract_proposal.py` — `cmd_extract_proposal`
- [x] 4.2 实现 proposal.md 结构化字段解析（capabilities / what_changes / success_criteria / impact）
- [x] 4.3 实现 JSON 和 YAML 格式输出
- [x] 4.4 修改 `.stdd/templates/proposal.md` — 增加提取标记注释

## 5. Spec 自动补全测试（P0-P1）

- [x] 5.1 创建 `tests/commands/test_extract_proposal.py` — 7 个测试用例
- [x] 5.2-5.4 全部测试通过

## 6. Spec 自动补全技能（P1）

- [x] 6.1 创建 `.stdd/templates/spec-draft.md` — 带置信度标注的 spec 草稿模板
- [x] 6.2 修改 `.stdd/skills/spec.md` — 替换 Step 2-3 为 auto-extract 流程
- [x] 6.3 修改 `.stdd/skills/spec.md` — 新增 Step 2 经验交叉检查
- [x] 6.4 修改 `.stdd/skills/spec.md` — Step 6 用户角色从"写 spec"变为"审 spec"
- [ ] 6.5 修改 `.stdd/templates/spec.md` — 增加置信度标注标记（改用 spec-draft.md）

## 7. 智能切片 CLI（P0）

- [x] 7.1 实现 `stdd/cli/commands/dependency_graph.py` — `cmd_dependency_graph`
- [x] 7.2 实现 spec GIVEN 子句解析 → capability 依赖匹配
- [x] 7.3 实现拓扑排序 + 循环依赖检测
- [x] 7.4 实现 JSON / DOT / TEXT 三种输出格式

## 8. 智能切片测试（P0-P1）

- [x] 8.1 创建 `tests/commands/test_dependency_graph.py` — 10 个测试用例
- [x] 8.2-8.6 全部测试通过

## 9. 智能切片技能（P1）

- [x] 9.1 修改 `.stdd/skills/slice.md` — 替换 Step 2 为五步分析流程
- [x] 9.2 五步分析：2a 依赖图、2b 风险评分、2c 工作量预估、2d 智能分组、2e 并行化
- [x] 9.3 修改 `.stdd/templates/slices.md` — 增加风险/预估工时/并行组/理由列

## 10. CI/CD CLI（P0）

- [x] 10.1 实现 `stdd/cli/commands/ci.py` — `cmd_ci` 主调度
- [x] 10.2 实现 `stdd ci init` — 交互式生成所有 CI 文件
- [x] 10.3 实现 `stdd ci generate workflow` — GitHub Actions workflow 生成
- [x] 10.4 实现 `stdd ci generate pre-commit` — pre-commit hook 生成
- [x] 10.5 实现 `stdd ci generate pr-template` — PR 评论模板生成
- [x] 10.6 实现 `stdd ci check-failures` — 确定性失败检查（约 60% 覆盖）
- [ ] 10.7 创建 `.stdd/templates/github-actions-workflow.yml`（嵌入在 ci.py 中）
- [ ] 10.8 创建 `.stdd/templates/pre-commit-config.yaml`（嵌入在 ci.py 中）
- [ ] 10.9 创建 `.stdd/templates/pr-comment.md`（嵌入在 ci.py 中）
- [ ] 10.10 创建 `.stdd/templates/failure-check-report.md`（嵌入在 ci.py 中）
- [x] 10.11 修改 `.stdd/config.d/quality.yaml` — 增加 `ci` 配置段

## 11. CI/CD 测试（P0-P1）

- [x] 11.1 创建 `tests/commands/test_ci.py` — 14 个测试用例
- [x] 11.2-11.9 全部测试通过

## 12. 集成与回归（P0）

- [x] 12.1 修改 `stdd/cli/__init__.py` — 注册 4 个新命令
- [x] 12.2 全量回归测试：109 用例全部通过
- [ ] 12.3 更新 `CHANGELOG.md` 增加 V2.4 条目
- [ ] 12.4 更新 `AGENTS.md` 版本号
- [ ] 12.5 更新 `STDD.md` 版本号
