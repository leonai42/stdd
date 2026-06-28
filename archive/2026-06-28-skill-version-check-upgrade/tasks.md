# 技能层版本自检 + Skill-Only 升级路径 — 任务清单

> 版本：2.9.5
> 创建日期：2026-06-28
> 对应 Slices：slices.md

## 1. Slice 1: Foundation（P0）

- [ ] 1.1 创建 `.stdd/skills/_shared/version-check.md`（版本自检共享片段）
- [ ] 1.2 修改 `stdd/cli/commands/install.py`：`_make_claude_code_frontmatter()` / `_make_workbuddy_frontmatter()` / `_make_trae_frontmatter()` 各函数增加 `stdd_version` 参数和字段注入
- [ ] 1.3 修改 `stdd/cli/commands/install.py`：`cmd_install()` 调用 frontmatter 函数时传入 `stdd_version`（从 `get_source_version()` 获取）

## 2. Slice 2: Phase Skills Update（P0，依赖 #1）

- [ ] 2.1 修改 `.stdd/skills/understand.md`：frontmatter 增加 `stdd_version`，新增 Step 0 引用 `version-check.md`
- [ ] 2.2 修改 `.stdd/skills/spec.md`：同上
- [ ] 2.3 修改 `.stdd/skills/slice.md`：同上
- [ ] 2.4 修改 `.stdd/skills/build.md`：同上
- [ ] 2.5 修改 `.stdd/skills/verify.md`：同上
- [ ] 2.6 修改 `.stdd/skills/deliver.md`：同上

## 3. Slice 3: Upgrade Skill（P0，依赖 #1）

- [ ] 3.1 创建 `.stdd/skills/upgrade.md`（skill-only 升级技能，~120 行）
- [ ] 3.2 修改 `stdd/cli/commands/install.py`：`SKILL_META` 字典增加 `"upgrade"` 条目（name/description/keywords）
- [ ] 3.3 修改 `stdd/cli/commands/init.py`：`FILES_TO_COPY` 增加 `.stdd/skills/upgrade.md`

## 4. Slice 4: Unit Tests（P0，依赖 #1, #3）

- [ ] 4.1 新增 `tests/commands/test_install.py` 测试：验证 `SKILL_META["upgrade"]` 存在且字段完整
- [ ] 4.2 新增测试：验证安装生成的 SKILL.md frontmatter 包含 `stdd_version` 字段
- [ ] 4.3 新增测试：验证 6 个平台的 dry-run install 输出中均包含 upgrade 技能
- [ ] 4.4 运行 `pytest tests/commands/test_install.py -v` 确认全部通过

## 5. Slice 5: E2E Verification（P1，依赖 #1, #2, #3, #4）

- [ ] 5.1 行为验证：版本落后场景告警（TC-VC-001, TC-VC-006）
- [ ] 5.2 行为验证：版本一致/更新/非STDD场景静默（TC-VC-002, TC-VC-003, TC-VC-005）
- [ ] 5.3 行为验证：版本格式容错（TC-VC-004）
- [ ] 5.4 行为验证：升级技能入口 + 平台检测（TC-UP-001, TC-UP-002）
- [ ] 5.5 行为验证：升级资源同步 + 版本更新 + 平台重装（TC-UP-005, TC-UP-009, TC-UP-010）
- [ ] 5.6 行为验证：网络降级处理（TC-UP-008）
- [ ] 5.7 运行全量回归 `pytest tests/ -v` 确认 0 失败
- [ ] 5.8 Diff review：确认所有修改文件版本号一致性

<!--
优先级说明：
- P0：阻塞性任务，完成前无法进入下一阶段
- P1：重要任务，应在当前阶段完成
- P2：可延后到后续版本的任务
依赖标注：(依赖 #N.M) 表示此任务依赖第 N 组第 M 个任务完成后才能开始
-->
