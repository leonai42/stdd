# STDD V2.5 任务清单

## 1. Slice A：经验生命周期状态机（P0 · 2.5d）

- [ ] 1.1 `experience.py` 添加 `cmd_verify` 子命令 + `_check_transition()` 状态校验
- [ ] 1.2 `experience.py` 添加 `cmd_deposit` 子命令 + `_auto_promote()` 自动提升逻辑
- [ ] 1.3 `experience.py` 添加 `cmd_retire` 子命令 + `--reason` 参数
- [ ] 1.4 `experience.py` 添加 `experience list` 过滤 retired（默认不显示，`--all` 显示）
- [ ] 1.5 `_save_index()` 状态变更时同步更新 `.experience-index.yaml` 的 `by_lifecycle`
- [ ] 1.6 测试：TC-EXP-LC-001 ~ 009（9 个 TC）（依赖 #1.1 ~ #1.5）
- [ ] 1.7 回归：确保现有 13 个 experience 测试全绿（依赖 #1.6）

## 2. Slice B1：CI 检查增强（P0 · 1.5d）

- [ ] 2.1 `ci.py` 添加 `check_scope_creep()` — proposal capability vs git diff 交叉对比
- [ ] 2.2 `ci.py` 添加 `check_coverage_vacuum()` — 解析 pytest JSON 覆盖率，低于阈值标记
- [ ] 2.3 `ci.py` 添加 `check_contract_gap()` — 依赖图边 A→B 字段引用校验
- [ ] 2.4 三个新检查注册到 `CHECKS` 列表，`check-failures` 聚合输出
- [ ] 2.5 测试：TC-CI-ENH-001 ~ 010（10 个 TC）（依赖 #2.1 ~ #2.4）
- [ ] 2.6 回归：确保现有 14 个 CI 测试全绿（依赖 #2.5）

## 3. Slice B2：跨 Session 状态恢复（P0 · 1.0d）

- [ ] 3.1 `state.py` 添加 `_write_resume_context()` — 写入 4 字段到 `.stdd.yaml`
- [ ] 3.2 `state.py` 添加 `_read_resume_context()` — 读取 + 向后兼容（V2.4 字段为 null）
- [ ] 3.3 阶段切换时自动调用 `_write_resume_context()` 刷新状态
- [ ] 3.4 测试：TC-SR-001 ~ 004（4 个 TC）（依赖 #3.1 ~ #3.3）
- [ ] 3.5 回归：确保现有状态读写测试全绿（依赖 #3.4）

## 4. Slice B3：Gate 文件确认（P1 · 1.5d）

- [ ] 4.1 新建 `gate.py` — `cmd_approve()` CLI + `--gate` 参数 + `_check_gate_order()`
- [ ] 4.2 `gate.py` 添加 `_check_file_token()` — 检测 `GATE<N>_APPROVED` 文件
- [ ] 4.3 `gates.yaml` 添加 `confirmation.channels` 配置段（dialog/file_token/cli）
- [ ] 4.4 CLI 注册：`stdd/bin/` 接线 `gate approve` 子命令（依赖 #4.1）
- [ ] 4.5 测试：TC-GF-001 ~ 007（7 个 TC）（依赖 #4.1 ~ #4.4）

## 5. Slice C：社区经验共享池（P1 · 4.5d）

- [ ] 5.1 `experience.yaml` 添加 `community` 配置段（registries / fallback_timeout / packs）
- [ ] 5.2 `experience.py` 添加 `cmd_pull()` + `_download_with_fallback()` 双源下载
- [ ] 5.3 `experience.py` 添加 `cmd_export()` 增强 + `_sanitize()` 脱敏函数
- [ ] 5.4 `experience.py` 添加 `--publish` flag + 投票字段初始化（community_votes_* / adoption_count）
- [ ] 5.5 新建 `curate.py` — `cmd_curate_pull()` 拉取全量到 inbox
- [ ] 5.6 `curate.py` — `cmd_curate_deduplicate()` 相似度匹配 + 自动合并/标记（依赖 #5.5）
- [ ] 5.7 `curate.py` — `cmd_curate_review()` 交互式逐条审核 a/e/m/r/s（依赖 #5.6）
- [ ] 5.8 `curate.py` — `cmd_curate_pack()` 打包 tar.gz + 生成 .experience-index.yaml（依赖 #5.7）
- [ ] 5.9 CLI 注册：`stdd/bin/` 接线 `experience pull/export` + `experience curate` 子命令（依赖 #5.2 ~ #5.8）
- [ ] 5.10 测试：TC-COM-001 ~ 015（15 个 TC）（依赖 #5.1 ~ #5.9）
- [ ] 5.11 新建 `tests/commands/test_curate.py`（curate 子命令测试）（依赖 #5.5 ~ #5.8）

## 6. Slice D1：proposal 扩展提取（P1 · 1.0d）

- [ ] 6.1 `extract_proposal.py` — `_parse_section()` 扩展识别 Constraints 段落
- [ ] 6.2 `extract_proposal.py` — 扩展识别 Stakeholders / RiskAreas（结构化）/ NonGoals 段落
- [ ] 6.3 JSON 输出新增 4 个 key，向后兼容（缺失字段 → 空数组）
- [ ] 6.4 `proposal.md` 模板添加新字段 STDD-MARKER 标记注释
- [ ] 6.5 测试：TC-EPE-001 ~ 007（7 个 TC）（依赖 #6.1 ~ #6.4）
- [ ] 6.6 回归：确保现有 7 个 extract_proposal 测试全绿（依赖 #6.5）

## 7. Slice D2：非代码类 Change 支持（P1 · 0.7d）

- [ ] 7.1 `experience.py` 添加 `_detect_project_type()` — 自动检测文件分布并标记
- [ ] 7.2 `build.md` Step 0.5 添加 `project_type` 过滤逻辑（匹配加载，不匹配跳过）
- [ ] 7.3 `verify.md` Step 3 后添加非代码检查清单分支（5 项替代检查）
- [ ] 7.4 测试：TC-NCC-001 ~ 005（5 个 TC）（依赖 #7.1 ~ #7.2）

## 8. Slice D3：并行切片指南（P1 · 1.0d）

- [ ] 8.1 `build.md` 添加并行执行策略段落（parallel_group / 子任务派发 / 结果合并）
- [ ] 8.2 `build.md` 添加串行 fallback 说明（无 delegation 能力时）
- [ ] 8.3 目视验证：build.md 包含完整 parallel_group 执行指南

## 9. 集成与收尾

- [ ] 9.1 `stdd/cli/__init__.py` 注册所有新命令（gate / curate / experience 新子命令）
- [ ] 9.2 `stdd/bin/` 入口点接线确认
- [ ] 9.3 全量 pytest 回归（期望所有 154+ 已有测试 + ~60 新测试全绿）
- [ ] 9.4 `CHANGELOG.md` 更新 V2.5 条目
- [ ] 9.5 `VISION.md` 更新 V2.5 状态标记
- [ ] 9.6 Git commit + tag `v2.5.0`
