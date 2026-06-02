# Spec: Skill 生态扩展

> 对应板块 C（C4）| 1 个 New Capability + 1 个 Modified Capability
> skill-ecosystem / skill-directory

## ADDED Requirements

### Requirement: Skill 目录结构重构 <!-- confidence: high -->

STDD SHALL 将 `.stdd/skills/` 从平铺 6 个文件重构为按领域分类的四级目录树。

**证据来源**：proposal.md `Capabilities > Modified > skill-directory`

#### Scenario: 目录结构升级 <!-- confidence: high -->

- **GIVEN** STDD V2.7 已安装
- **WHEN** 查看 `.stdd/skills/` 目录
- **THEN** 目录 SHALL 包含 core/（6 个阶段 Skill）、languages/（语言专项 Skill）、workflow/（工作流辅助 Skill）、tools/（工具集成 Skill）四个子目录
- **AND** `_shared/` 目录 SHALL 保留用于共享模板和工具

---

### Requirement: 新增语言专项 Skill <!-- confidence: high -->

STDD SHALL 新增 3 个语言专项 Skill 作为社区示范。

**证据来源**：proposal.md `Capabilities > New > skill-ecosystem`

#### Scenario: python-patterns Skill 激活 <!-- confidence: high -->

- **GIVEN** STDD change 的 project_type 为 python
- **WHEN** Phase 4 BUILD 开始
- **THEN** AI SHALL 自动加载 `languages/python-patterns/SKILL.md`
- **AND** Skill 内容 SHALL 包含 Python 惯用法（类型提示/async模式/错误处理）+ 反模式 + 关联 STDD 经验

#### Scenario: fastapi-patterns Skill 激活 <!-- confidence: medium -->

- **GIVEN** 项目使用了 FastAPI 框架（检测到 `from fastapi import` 或 `FastAPI()` 调用）
- **WHEN** Phase 4 BUILD 生成 API 端点代码
- **THEN** AI SHALL 自动加载 `languages/fastapi-patterns/SKILL.md`
- **AND** Skill 内容 SHALL 包含路由设计/依赖注入/中间件模式/请求验证

#### Scenario: go-idioms Skill 激活 <!-- confidence: high -->

- **GIVEN** STDD change 的语言为 go
- **WHEN** Phase 4 BUILD 开始
- **THEN** AI SHALL 自动加载 `languages/go-idioms/SKILL.md`
- **AND** Skill 内容 SHALL 包含并发模式/错误处理惯用法/接口设计

---

### Requirement: 新增工作流辅助 Skill <!-- confidence: high -->

STDD SHALL 新增 search-first 和 skill-create 两个工作流 Skill。

**证据来源**：proposal.md `Capabilities > New > skill-ecosystem`

#### Scenario: search-first 决策矩阵 <!-- confidence: high -->

- **GIVEN** Phase 2 SPEC 或 Phase 4 BUILD 开始前
- **WHEN** AI 准备为某个 capability 设计实现方案
- **THEN** AI SHALL 执行 search-first 决策矩阵：Adopt（现成方案）→ Extend（扩展已有）→ Compose（组合多个库）→ Build（自己写）
- **AND** 如果选择 Build，SHALL 在 design.md 的 Decisions 中记录理由

#### Scenario: skill-create 引导创建新 Skill <!-- confidence: high -->

- **GIVEN** 用户执行 `stdd skill create my-pattern --type language`
- **WHEN** CLI 交互式收集 Skill 元信息
- **THEN** 系统 SHALL 基于模板在 `languages/my-pattern/` 下生成 `SKILL.md` 骨架
- **AND** 自动关联对应的语言规范文件（`.stdd/standards/<lang>.md`）

---

### Requirement: Skill 格式规范（ECC 兼容）<!-- confidence: medium -->

所有新增 Skill SHALL 遵循 ECC 兼容的 YAML frontmatter + Markdown body 格式。

**证据来源**：design.md `【ECC-4】Skill 生态扩展 > Skill 规范`

#### Scenario: YAML frontmatter 完整性 <!-- confidence: high -->

- **GIVEN** 一个新 Skill 的 SKILL.md 文件
- **WHEN** AI 或 STDD CLI 读取该文件
- **THEN** YAML frontmatter SHALL 包含 name、description、origin（STDD）、version、category、language 字段
- **AND** related_skills 字段 SHALL 为可选的关联 Skill 引用列表
