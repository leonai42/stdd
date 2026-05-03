# Python 开发规范

> 适用版本：Python 3.10+
> 最后更新：2026-05-03

## 一、代码风格

### 1.1 格式化

- 使用 ruff 作为 linter 和 formatter
- 行宽：100 字符
- 缩进：4 空格（禁止 Tab）
- 文件末尾：一个空行

### 1.2 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块/文件 | snake_case | `message_service.py` |
| 类 | PascalCase | `MessageService` |
| 函数/方法 | snake_case | `process_message()` |
| 变量 | snake_case | `user_id` |
| 常量 | UPPER_SNAKE_CASE | `WELCOME_MSG` |
| 私有成员 | 前缀 `_` | `_filter_casual_message()` |
| 内部实现 | 前缀 `__` | `__init_core()` |

### 1.3 Import 顺序

1. 标准库
2. 第三方库
3. 本地模块

每组之间空一行。禁止 `from xxx import *`。

## 二、类型注解

### 2.1 强制要求

- 所有公共函数/方法必须有完整类型注解（参数 + 返回值）
- 私有函数建议但不强制

### 2.2 示例

```python
from typing import Dict, Any, Optional, List

async def process_message(
    self,
    message: Dict[str, Any],
    user_id: int,
    state: Optional[str] = None
) -> Optional[str]:
    ...
```

## 三、异步编程

### 3.1 规则

- IO 操作优先使用 async/await
- 数据库操作使用 aiosqlite（不要用同步 sqlite3）
- 外部 API 调用使用 httpx.AsyncClient（不要用 requests）
- 不要在 async 函数中调用 time.sleep()，使用 asyncio.sleep()

### 3.2 并发安全

- 共享可变状态使用 asyncio.Lock 保护
- 不要在锁内做 IO 操作

## 四、错误处理

### 4.1 规则

- 只在系统边界捕获异常（API 入口、消息处理入口）
- 内部函数让异常向上传播
- 捕获具体异常类型，禁止裸 `except:`
- 记录完整 traceback：`logger.error("msg", exc_info=True)`

### 4.2 用户可见错误

- 抛出业务异常时 message 应为中文用户友好信息
- 不在用户消息中暴露堆栈信息

## 五、日志

### 5.1 规则

- 使用结构化日志记录器
- 关键业务节点记录 INFO 日志（用户行为、状态变更）
- 异常记录 ERROR 日志
- 不在循环中打印 DEBUG 日志

### 5.2 日志内容

- 必须包含足够的上下文信息（user_id, openid, 关键参数）
- 格式：`f"操作描述: key1=value1, key2=value2"`

## 六、测试代码规范

### 6.1 测试文件组织

- 单元测试：`tests/unit/test_<module>.py`
- 集成测试：`tests/integration/test_<feature>.py`
- 测试文件镜像源码模块结构

### 6.2 测试命名

```
test_<被测方法>_<场景>_<预期结果>
```

示例：`test_get_user_by_openid_not_exist`

### 6.3 Fixtures

- 共享 fixture 放在 `tests/conftest.py`
- 模块专属 fixture 放在模块测试文件内
- 数据库测试使用 SQLite 内存数据库

### 6.4 Mock 原则

- 单元测试 mock 外部依赖（LLM API、微信 API、Embedding API）
- 集成测试不 mock 数据库
- 使用 AsyncMock mock 异步函数
- PropertyMock mock @property 属性
- 测试断言验证行为（WHAT），不验证实现细节（HOW）

### 6.5 Parametrize

- 同类场景多输入变体使用 `@pytest.mark.parametrize`
- 每个参数集应测试不同的边界条件

## 七、代码审查检查清单

在 Phase 5 VERIFY 中，逐项检查：

- [ ] 死代码：无 print、注释掉的代码、未使用的 import
- [ ] 命名：名称匹配实际行为（不产生误导）
- [ ] 类型：公共函数有完整类型注解
- [ ] 异步：IO 操作使用 async/await
- [ ] 安全：无 SQL 注入、无 XSS、token 不硬编码
- [ ] 错误：边界输入验证、外部调用有超时
- [ ] 日志：关键节点有日志、无敏感信息泄露
- [ ] 测试：新行为有测试、断言验证行为而非实现
- [ ] 注释：只保留 WHY，删除 WHAT
