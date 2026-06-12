# 实现任务清单

## Slice 1: extract + search (并行开发)

- [ ] S1.1: 实现 `cmd_extract()` — 解析 test-report.md，提取失败模式
- [ ] S1.2: 实现 `_parse_test_report()` — 解析12类失败检查表格
- [ ] S1.3: 实现 `_filter_patterns()` — 筛选 severity>=medium or occurrences>=2
- [ ] S1.4: 实现 `_generate_draft()` — 生成 EXP-*.md 草稿
- [ ] S1.5: 实现 `cmd_search()` — 全文搜索
- [ ] S1.6: 实现 `_search_score()` — 相关性评分算法
- [ ] S1.7: 编写 TC-EXT-001/002/003 + TC-SEA-001/002/003/004/005

## Slice 2: share

- [ ] S2.1: 实现 `cmd_share()` — 主流程
- [ ] S2.2: 实现 `_detect_gh()` — 检测 gh CLI 可用性
- [ ] S2.3: 实现 `_share_via_gh()` — gh CLI 路径
- [ ] S2.4: 实现 `_share_via_api()` — 服务器 API 路径
- [ ] S2.5: 复用 `_sanitize()` — share 前自动脱敏
- [ ] S2.6: 编写 TC-SHA-001/002/003/004/005

## Slice 3: review

- [ ] S3.1: 实现 `cmd_review()` — 交互式主循环
- [ ] S3.2: 实现 `_display_draft()` — 格式化展示单条草稿
- [ ] S3.3: 实现 S/L/D/A/Q 选择处理
- [ ] S3.4: S 路径: 调用 cmd_deposit + cmd_share
- [ ] S3.5: L 路径: 调用 cmd_verify + cmd_deposit
- [ ] S3.6: 编写 TC-REV-001/002/003/004/005

## Slice 4: 注册 + 集成

- [ ] S4.1: 在 `__init__.py` 注册 extract/review/share/search 子命令
- [ ] S4.2: 在 VERIFY skill 末尾添加 `stdd experience extract` 调用
- [ ] S4.3: 运行全量经验测试 确保无回归
