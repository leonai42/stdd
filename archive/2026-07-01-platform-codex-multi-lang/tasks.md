# V2.10 任务清单

## 1. platform-codex — OpenAI Codex CLI 平台适配（P0）

- [ ] 1.1 在 `install.py` `platform_map` 中添加 `"codex"` 条目（target_base、frontmatter_fn、is_dir_per_skill、skill_filename）
- [ ] 1.2 在 `install.py` 使用提示中添加 Codex 平台分支（`elif platform == "codex"`）
- [ ] 1.3 创建 `.stdd/platforms/codex/` 目录结构
- [ ] 1.4 生成并验证 `stdd install codex` 安装流程（6 skill 文件 × SKILL.md）
- [ ] 1.5 验证 Codex skill frontmatter 格式与 claude-code 一致（复用 `_make_claude_code_frontmatter`）

## 2. lang-javascript — JavaScript 开发规范（P0）

- [ ] 2.1 创建 `.stdd/standards/javascript.md`
- [ ] 2.2 编写 7 章内容（代码风格/类型系统/异步/错误处理/日志/测试规范/审查清单）
- [ ] 2.3 审查清单包含 checkbox 格式检查项（`- [ ]`）

## 3. lang-c — C/C++ 开发规范（P0）

- [ ] 3.1 创建 `.stdd/standards/c.md`
- [ ] 3.2 编写 7 章内容，类型系统和错误处理章节按「C 语言约定」/「C++ 语言约定」分区
- [ ] 3.3 审查清单包含 checkbox 格式检查项

## 4. lang-kotlin — Kotlin 开发规范（P0）

- [ ] 4.1 创建 `.stdd/standards/kotlin.md`
- [ ] 4.2 编写 7 章内容 + Android 特有约定（Jetpack Compose/ViewModel/Hilt）
- [ ] 4.3 审查清单包含 checkbox 格式检查项

## 5. lang-swift — Swift 开发规范（P0）

- [ ] 5.1 创建 `.stdd/standards/swift.md`
- [ ] 5.2 编写 7 章内容 + iOS/macOS 特有约定（SwiftUI/MVVM/Combine）
- [ ] 5.3 审查清单包含 checkbox 格式检查项

## 6. lang-dart — Dart/Flutter 开发规范（P0）

- [ ] 6.1 创建 `.stdd/standards/dart.md`
- [ ] 6.2 编写 7 章内容 + Flutter 特有约定（Widget 树/状态管理/BuildContext/测试金字塔）
- [ ] 6.3 审查清单包含 checkbox 格式检查项

## 7. platform-sync — 文档同步更新（P0）

- [ ] 7.1 更新 `EXTENDING.md`「现有平台参考」表格（新增 Codex 行）
- [ ] 7.2 更新 `AGENTS.md` 平台数量（6→8）和语言数量（5→10）
- [ ] 7.3 更新 `STDD.md` 平台数量和语言数量（与 AGENTS.md 一致）
- [ ] 7.4 更新 `README.md` 和 `README_EN.md` 平台和语言数量

## 8. 测试与验证（P0-P1）

- [ ] 8.1 编写 `tests/commands/test_install.py` 的 Codex 平台测试（TC-CODEX-001~004）
- [ ] 8.2 编写语言规范文件存在性测试（TC-LANG-001~006）
- [ ] 8.3 编写文档一致性测试（TC-SYNC-001~002）
- [ ] 8.4 运行全量 pytest 确保已有平台回归通过（TC-SYNC-003）
- [ ] 8.5 运行 `ruff check` 确保代码风格一致

<!--
优先级说明：
- P0：阻塞性任务，完成前无法进入 Phase 5 VERIFY
- P1：重要任务，应在 Phase 4 完成
依赖标注：(依赖 #N.M) 表示此任务依赖第 N 组第 M 个任务完成后才能开始
切片映射：Slice 1 = 任务 1 | Slice 2 = 任务 2-4 | Slice 3 = 任务 5-6 | Slice 4 = 任务 7 | Slice 5 = 任务 8
-->
