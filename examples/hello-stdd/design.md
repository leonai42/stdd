# 技术设计: Hello Greeter

## Context

Python 3.10+ 环境，无外部依赖。实现简单的命令行问候工具。

## Decisions

### 1. 问候策略
基于 `datetime.now().hour` 判断时段：
- 6-12: "早上好"
- 12-18: "下午好"
- 18-22: "晚上好"
- 其他: "你好"

### 2. 命令行接口
使用 `argparse` 处理参数：
- 位置参数：`name`（用户名）
- 可选参数：`--formal`（正式模式）

### 3. 测试策略
pytest 单元测试，覆盖：
- 各时段问候语正确性
- `--formal` 模式输出格式
- 边界值（5:59, 6:00, 11:59, 12:00 等）

## Architecture

```
src/greeter.py  ──  命令行入口 + 问候逻辑
tests/test_greeter.py  ──  pytest 测试
```

## Risks

- 无外部依赖，风险极低
