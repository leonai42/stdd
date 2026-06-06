# V2.9.4 Backlog — 收尾

## Why

1. batch 在当前使用中被滥用：6 个代码改动（含新增 CLI 命令和 3 个测试文件）通过 batch 速通，跳过了 change 的 Gate 流程。需要从工具层面限制 batch 的适用范围。
2. backlog 中数据契约校验和跨平台 Guard 两项需要先出方案设计，暂不实现代码。

## What Changes

### 代码改动（3 项）

**1. batch add 增加 git diff 检查**
- 在 `_cmd_batch_add` 中，调用 `git diff --name-only HEAD` 统计从 batch open 以来修改的文件数
- 如果已修改 >3 个不同文件 → 拒绝添加新 item，提示："已修改 N 个文件，超出 batch 适用范围。请用 stdd new 创建 change 走完整流程。"
- 不影响 item 本身添加的成功（只是前置检查）

**2. batch max_items 从 20 降到 5**
- `_create_batch()` 中 `max_items` 默认值改为 5
- `_cmd_batch_add` 中满额提示改为 "批次已满 (5 项)，请升级为 change 或先 close 再 open"

**3. batch open 增加 active change 检查**
- `_cmd_batch_open` 中，在创建 batch 之前检查是否存在 active change（phase 为 build 或 verify）
- 如果存在 → 打印警告："检测到进行中的 change '<name>' (phase: build)。建议在此 change 中完成修改，而非单独开 batch。"
- 不阻止，仅警告（因为确实存在合理场景：change 做主要工作，batch 做个顺手小修）

### 设计文档（2 篇）

**4. 数据契约校验方案**
- 文档位置：`docs/design/schema-verify.md`
- 内容：定义 .stdd.yaml 的 canonical 字段名列表、读写端校验机制、`stdd schema verify` 命令设计

**5. 跨平台 Guard Hook 适配方案**
- 文档位置：`docs/design/cross-platform-guard.md`
- 内容：各平台（Cursor/Windsurf/Cline/Copilot）的 Hook 等价机制调研、适配方案、优先级排序

## Success Criteria
- [ ] `stdd batch add` 在改动 >3 文件时拒绝
- [ ] batch 最大 items 数为 5
- [ ] `stdd batch open` 检测到 active change 时警告
- [ ] `docs/design/schema-verify.md` 文档完整
- [ ] `docs/design/cross-platform-guard.md` 文档完整
