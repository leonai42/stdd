# 变更提案: Hello Greeter

## Why

项目需要一个简单的问候程序作为 STDD 流程演示的起点。

## What Changes

- 新增 `src/greeter.py`：Python 问候程序
- 新增 `tests/test_greeter.py`：对应单元测试
- 支持 `--formal` 正式问候模式

## Capabilities

### New Capabilities
- `GREETER`：问候功能

## Impact

- 新增文件：`src/greeter.py`、`tests/test_greeter.py`
- 无破坏性变更

## Success Criteria

- [ ] `python src/greeter.py Alice` 输出问候语
- [ ] `--formal` 模式输出正式问候
- [ ] 上午 6-12 点输出"早上好"
- [ ] pytest 测试全部通过
