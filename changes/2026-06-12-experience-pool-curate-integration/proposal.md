# 经验池收尾：curate review 交互化 + pull 只拉 approved + VERIFY 集成

## Why

上一轮实现了 extract->review->share 闭环，经验可以通过服务器 API 提交到 pending/。但:
1. curate review 仍是非交互式 (auto-approve/reject)
2. pull 拉全量，不区分审核状态
3. VERIFY 未集成 extract

## What Changes

- C1 (modified): curate review 改为真交互式 (A/R/E/S)
- C2 (modified): pull 只从 approved/ 获取
- C3 (modified): VERIFY skill 末尾追加 extract 调用

## Capabilities

### Modified
- **curate-review-interactive**: 展示 pending/ 经验，A批准/R拒绝/E编辑/S跳过
- **pull-only-approved**: pull 只下载 approved/ 内容
- **verify-extract-integration**: VERIFY 末尾调用 extract

## Success Criteria

- [ ] SC1: curate review 交互式 A/R/E/S
- [ ] SC2: A->approved/, R->rejected/
- [ ] SC3: pull 只拉 approved/
- [ ] SC4: VERIFY skill 末尾提示 extract
