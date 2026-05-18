# 参与贡献 / Contributing to STDD

> 欢迎贡献！无论是报告 Bug、提出功能建议、新增语言规范或平台适配，你的参与都让 STDD 变得更好。
> Welcome! Whether reporting bugs, suggesting features, or adding language/ platform support, your contributions make STDD better.

---

## 目录 / Table of Contents

- [行为准则 / Code of Conduct](#行为准则--code-of-conduct)
- [如何贡献 / How to Contribute](#如何贡献--how-to-contribute)
- [开发环境搭建 / Development Setup](#开发环境搭建--development-setup)
- [STDD 自身使用 STDD 开发 / STDD Is Built with STDD](#stdd-自身使用-stdd-开发--stdd-is-built-with-stdd)
- [PR 提交规范 / PR Guidelines](#pr-提交规范--pr-guidelines)
- [文档规范 / Documentation Standards](#文档规范--documentation-standards)
- [扩展开发 / Extension Development](#扩展开发--extension-development)

---

## 行为准则 / Code of Conduct

请保持尊重和建设性的交流氛围。我们致力于为所有参与者提供友好、包容的协作环境。

Please maintain a respectful and constructive atmosphere. We are committed to providing a welcoming and inclusive environment for all participants.

---

## 如何贡献 / How to Contribute

### 报告 Bug / Report Bugs

在 GitHub Issues 中提交 Bug 报告，请包含：

1. **环境信息**：操作系统、Python 版本、AI 平台及版本
2. **复现步骤**：清晰的操作步骤
3. **预期行为 vs 实际行为**
4. **相关日志或截图**

### 功能建议 / Feature Requests

1. 先搜索已有 Issues，避免重复
2. 描述使用场景：这个功能解决什么问题？
3. 说明预期行为

### 代码贡献 / Code Contributions

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature-name`
3. 遵循 STDD 流程开发（见下方说明）
4. 确保测试通过：`python -m pytest tests/ -v`
5. 提交 PR 到 `master` 分支

---

## 开发环境搭建 / Development Setup

```bash
# 1. 克隆仓库 / Clone the repo
git clone https://github.com/leonai42/stdd.git
cd stdd

# 2. 安装依赖 / Install dependencies
pip install -r requirements.txt

# 3. 运行测试验证环境 / Run tests to verify
python -m pytest tests/ -v

# 4. （可选）安装到当前项目测试 / (Optional) Test in current project
python bin/stdd init
python bin/stdd install claude-code
```

---

## STDD 自身使用 STDD 开发 / STDD Is Built with STDD

STDD 项目自身使用 STDD 流程开发。当你提交 PR 时：

- **文档变更**（模板、Skill、规范）：至少走 Phase 1 (proposal) + Phase 2 (spec)，清晰描述 Why / What / Impact
- **CLI 代码变更**：走完整六阶段流程，包含测试
- **Bug 修复**：走简化流程（proposal + spec + test + fix）

提交 PR 时，请在描述中链接相关 change 目录的 proposal.md 和 design.md。

---

## PR 提交规范 / PR Guidelines

### Commit Message 格式

```
<类型>: <简短描述>

<详细说明（可选）>

Co-Authored-By: Your Name <email>
```

**类型 / Type**：
- `feat`: 新功能 / New feature
- `fix`: Bug 修复 / Bug fix
- `docs`: 文档变更 / Documentation
- `refactor`: 重构 / Refactoring
- `test`: 测试变更 / Test changes
- `chore`: 构建/工具变更 / Build/tooling changes

### PR 检查清单 / PR Checklist

- [ ] 代码遵循对应语言规范（`.stdd/standards/<language>.md`）
- [ ] 新增行为有测试覆盖
- [ ] 所有测试通过：`python -m pytest tests/ -v`
- [ ] 文档已更新（README、CHANGELOG 等）
- [ ] 相关 spec 已更新或新建
- [ ] 无遗留的调试代码或注释

---

## 文档规范 / Documentation Standards

STDD 文档使用**中英双语**（Chinese + English），遵循以下格式：

- 标题和关键概念：中英并排展示，以 `/` 或 `|` 分隔
- 段落内容：中英各一段，英文段落后标注 `EN` 或使用双语交替
- 表格和代码块：尽量使用双语表头或注释

新增文档模板请参考 `.stdd/templates/` 目录中的现有模板。

---

## 扩展开发 / Extension Development

STDD 设计了三个主要扩展点，详见 [EXTENDING.md](EXTENDING.md)：

1. **新增平台适配** — 在 `stdd/cli/commands/install.py` 中添加平台配置
2. **新增语言规范** — 创建 `.stdd/standards/<language>.md`
3. **新增失败模式检查** — 在 `stdd/cli/commands/validate.py` 中添加检查函数
4. **新增 CLI 命令** — 创建命令模块并在 `__init__.py` 中注册

---

## 许可证 / License

贡献的代码将采用与项目一致的 [MIT License](LICENSE)。

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
