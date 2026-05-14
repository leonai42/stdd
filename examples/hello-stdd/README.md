# Hello STDD — 示例项目

演示 STDD 六阶段开发流程的完整示例。

## 目录结构

```
hello-stdd/
├── README.md           # 本文件
├── proposal.md         # Phase 1: UNDERSTAND 产出
├── design.md           # Phase 2: SPEC 产出
├── specs/              # Phase 2: SPEC 产出
│   └── cli/
│       └── spec.md
├── test-plan.md        # Phase 2: SPEC 产出
├── src/                # Phase 4: BUILD 产出
│   └── greeter.py
├── tests/              # Phase 4: BUILD 产出
│   └── test_greeter.py
├── changes/            # change 目录（init 后创建）
├── specs/              # 合并后的 specs（init 后更新）
└── archive/            # 归档目录
```

## 快速开始

```bash
# 1. 初始化 STDD
python ../../bin/stdd init

# 2. 创建新 change
stdd new hello-greeter

# 3. 启动 STDD 流程
# 在 Claude Code 中: /stdd-understand
```

## 示例说明

本示例实现一个简单的 Python 问候程序 `greeter.py`：
- 接受用户名作为参数
- 根据当前时间返回不同问候语
- 支持 `--formal` 正式问候模式
