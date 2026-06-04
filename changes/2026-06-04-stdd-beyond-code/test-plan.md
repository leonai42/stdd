# STDD Beyond Code — 测试方案

> 非编程 Change | 验证方式：Agent CP 断言 + 人工审校

## 测试策略

本 Change 为纯文档产出，不涉及可执行代码。采用**Agent CP 自动化验证 + 人工专家审校**双轨验证。

## 详细测试案例

| TC-ID | 检查项 | 验证方式 | 优先级 | 通过标准 |
|-------|--------|---------|:---:|------|
| TC-PAPER-001 | 字数 ≥30,000 | Agent CP-1 | P0 | wc -m ≥30000 |
| TC-PAPER-002 | 章节完整 (10章) | Agent CP-2 | P0 | grep 确认 |
| TC-PAPER-003 | 引用 ≥30 篇 | Agent CP-3 | P0 | grep 确认 |
| TC-PAPER-004 | 文件非空 | Agent CP-4 | P0 | test -s |
| TC-PPT-001 | 页数 ≥25 | Agent CP-5 | P0 | grep 确认 |
| TC-PPT-002 | 文件非空 | Agent CP-6 | P0 | test -s |
| TC-GUIDE-001 | 指南文件完整 | Agent CP-7 | P0 | test -s |
| TC-REVIEW-001 | 论文逻辑一致性 | 人工审校 | P1 | 2轮通过 |
| TC-REVIEW-002 | 引用真实性 | 人工抽检 | P1 | 5篇抽检 |
| TC-REVIEW-003 | PPT 章节覆盖 | 人工对照 | P1 | 10章全覆盖 |

## 执行计划

1. Phase 4 BUILD 完成后 → 运行 `stdd agent verify paper-quality`
2. CP 全部通过 → 进入人工审校阶段
3. 人工审校通过 → Phase 5 Gate 3 确认
