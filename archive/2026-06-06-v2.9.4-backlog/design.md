# V2.9.4 Backlog 收尾 — 技术设计

## S1: batch add git diff 检查

**位置：** `batch.py:_cmd_batch_add()`

**逻辑：**
1. 找到当前 open batch
2. `git diff --name-only HEAD` 统计修改文件数
3. 如果 >3 → print 警告 + return（不调用 _close 也不崩溃）
4. 否则正常 add

**注意：** git diff 在无 git 项目时会抛异常，需要 try/except 兜底。

## S2: batch max_items 20→5

**位置：** `batch.py:_create_batch()`

**改动：** 第 94 行 `"max_items": 20` → `"max_items": 5`

## S3: batch open 检查 active change

**位置：** `batch.py:_cmd_batch_open()`

**逻辑：**
1. 在创建 batch 之前 调用 `_find_active_change()`（复用 guard.py 的逻辑或重新导入）
2. 如果存在 active change 且 phase 在 build/verify：
   - 打印警告："检测到进行中的 change '<name>' (phase: build)。建议在此 change 中完成修改。"
3. 不阻止，继续创建 batch

## S4-S5: 设计文档

两个 markdown 文件，纯文档，不改代码。
- `docs/design/schema-verify.md`
- `docs/design/cross-platform-guard.md`
