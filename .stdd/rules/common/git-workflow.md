# Git 工作流 / Git Workflow

## 提交规范

- `feat:` 新功能
- `fix:` 修复
- `test:` 测试
- `docs:` 文档
- `refactor:` 重构
- 提交信息使用中文或英文，保持一致

## 分支策略

- `master` — 稳定版本
- feature branches — `feature/<name>`
- 提交前运行 `pytest tests/` 确保全量通过
