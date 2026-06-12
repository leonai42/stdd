# 切片执行计划

## 依赖分析

```
extract (无依赖)     search (无依赖)     share (无依赖, 只需 _sanitize 已存在)
     |                    |                    |
     +--------+-----------+                    |
              |                                |
           review (调用 extract 的输出 + share 的 API)
              |
         VERIFY skill (调用 extract)
```

- extract, search, share: **零内部依赖，可并行开发**
- review: 汇编层，依赖 extract 和 share 的命令存在
- VERIFY skill: 依赖 extract 命令注册

## 切片执行计划

| Slice | Capability | TC数 | 风险 | 工作量 | 并行组 | 说明 |
|-------|-----------|------|------|--------|--------|------|
| S1 | extract + search | 8 | 低 | M | G1 | 纯新代码，无内部依赖，可并行 |
| S2 | share | 5 | 中 | M | G1 | 纯新代码，有外部 API 依赖(mock) |
| S3 | review | 5 | 中 | M | G2 | 依赖 S1+S2 命令存在后才可测试 |
| S4 | 注册+集成 | 0 | 低 | S | G2 | 注册4个子命令，修改 VERIFY skill |

## 执行策略

- G1 (S1+S2): 并行开发 → 实现 extract、search、share
- G2 (S3+S4): 串行组装 → 实现 review + 注册集成

## 每个切片的 Rationale

### S1: extract + search
- 依赖: 无（纯新增函数）
- 风险: 低（全部单元测试，无状态变更）
- 工作量: M（8 个 TC，2 个新命令）
- 目标: `stdd experience extract` 和 `stdd experience search` 可独立运行

### S2: share
- 依赖: `_sanitize()` 函数已存在于 experience.py
- 风险: 中（涉及外部 API，需 mock）
- 工作量: M（5 个 TC）
- 目标: `stdd experience share EXP-xxx` 可运行，脱敏+推送闭环

### S3: review
- 依赖: cmd_extract, cmd_share 已实现
- 风险: 中（交互式输入，需 mock stdin）
- 工作量: M（5 个 TC）
- 目标: `stdd experience review` 交互式确认流程完整

### S4: 注册+集成
- 依赖: S1+S2+S3 完成
- 风险: 低（仅注册和 skill 文本调整）
- 工作量: S（无需新 TC）
- 目标: `stdd experience --help` 显示 13 个子命令（原9+新4）
