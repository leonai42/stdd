# Python 编码规则

## 必须遵守

1. 使用 Python 3.10+ 类型提示语法（`list[str]` 而非 `List[str]`）
2. async 函数单独处理 `asyncio.CancelledError`
3. 使用 `asyncio.TaskGroup` 管理并发任务
4. 异常处理：具体异常 + `from e` 保留上下文
5. 文件大小：单个模块 ≤500 行
