# V2.7 测试报告

> 版本：V2.7（V2.6 合并）| 日期：2026-06-03
> 对应 test-plan.md：39 TCs planned

## 一、测试结果摘要

| 指标 | 数值 |
|------|------|
| 总测试数 | 164 |
| 通过 | 164 (100%) |
| 失败 | 0 |
| 新增测试 | 9 (test_canon.py) |
| 运行时间 | 3.30s |
| 覆盖率 (changed_files_only) | ~45% |

## 二、新增测试详情

| TC ID | 测试名称 | 状态 |
|-------|---------|:---:|
| TC-CANON-001 | test_proposal_init_generates_yaml | ✅ |
| TC-CANON-002 | test_proposal_validate_missing_field | ✅ |
| TC-CANON-003 | test_agent_spec_format_validation | ✅ |
| TC-CANON-004 | test_project_index_update | ✅ |
| TC-CANON-004b | test_project_index_trace | ✅ |
| TC-CANON-005 | test_pure_markdown_mode_backward_compatible | ✅ |
| TC-DUAL-001 | test_canon_init_creates_directories | ✅ |
| TC-DUAL-002 | test_canon_generate_creates_human_view | ✅ |
| TC-DUAL-003 | test_canon_verify_detects_stale | ✅ |

## 三、11 类失败模式检查

| 类别 | 检查结果 | 备注 |
|------|:---:|------|
| (a) 幻觉行为 | ✅ | — |
| (b) 范围蔓延 | ✅ | — |
| (c) 级联错误 | ✅ | — |
| (d) 上下文丢失 | ✅ | phase-context 机制就绪 |
| (e) 工具误用 | ✅ | — |
| (f) 运行时行为偏差 | ✅ | — |
| (g) 管线断链 | ✅ | — |
| (h) 内容质量偏差 | ✅ | — |
| (i) 指令衰减 | ✅ | bilingual + phase-context 缓解 |
| (j) 覆盖真空 | ✅ | — |
| (k) 契约断层 | ✅ | — |
| **(l) 锚定缺失** | ✅ | 新增（V2.7）— CI check 已实现 |

## 四、设计偏离记录

详见 [design-adjustments.md](design-adjustments.md)

## 五、向后兼容验证

- [x] V2.5 格式 `.stdd.yaml` 可被 V2.7 正确读取
- [x] 无 canonical/ 目录时行为与 V2.5 一致
- [x] 现有 155 个测试全部通过
- [x] CLI 新命令不破坏已有命令
