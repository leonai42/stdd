# Capability: Playground 入口与导览框架 (playground-page)

## ADDED Requirements

### Requirement: 场景选择入口

系统 SHALL 在 `website/playground/index.html` 提供一个场景选择页面，展示两个演示场景卡片供用户选择。

#### Scenario: 页面加载展示双场景卡片

- **GIVEN** 用户浏览器访问 `/playground/index.html`
- **WHEN** 页面加载完成
- **THEN** 系统 SHALL 展示 Hero 区域（标题 + 副标题）
- **AND** SHALL 展示两个场景选择卡片：「API 限流（技术型）」和「用户购买升级Pro（业务型）」
- **AND** 每个卡片 SHALL 包含场景名称、类型标签、预计体验时间（5 分钟）、简要描述
- **AND** 页面 SHALL 与官网视觉风格一致（深蓝导航栏、绿色主题色、相同字体）

#### Scenario: 用户点击场景卡片跳转

- **GIVEN** 用户在 Playground 入口页
- **WHEN** 用户点击「API 限流」卡片
- **THEN** 系统 SHALL 跳转到 `api-rate-limit/index.html`
- **AND** 用户点击「用户购买升级Pro」卡片时 SHALL 跳转到 `user-pro-upgrade/index.html`

#### Scenario: 导航栏入口链接

- **GIVEN** 官网主页 `website/index.html`
- **WHEN** 用户查看导航栏
- **THEN** 导航栏 SHALL 包含「Playground」链接
- **AND** 点击后 SHALL 跳转到 `playground/index.html`

### Requirement: 分步导览框架

系统 SHALL 在每个场景页中按 Phase 分区展示 STDD 6 阶段流程，并提供 Gate 交互节点。

#### Scenario: Phase 区渲染

- **GIVEN** 用户进入某个场景页
- **WHEN** stepper.js 读取 SCENARIO_DATA 并完成渲染
- **THEN** 页面 SHALL 按 Phase 1 到 Phase 6 的顺序展示至少 6 个分区
- **AND** 每个 Phase 区 SHALL 包含标题和结构化内容
- **AND** 默认仅 Phase 1 处于展开高亮状态，后续 Phase 为半透明

#### Scenario: 滚动推进 Phase

- **GIVEN** 用户在当前 Phase 阅读完毕
- **WHEN** 用户向下滚动页面
- **THEN** 下一 Phase SHALL 通过 Intersection Observer 触发淡入动画
- **AND** 上一 Phase SHALL 保持可见（不折叠）

#### Scenario: Gate 交互 — checkbox 类型

- **GIVEN** 用户到达 Gate 1（Phase 1 结尾）
- **WHEN** Gate 区域进入视口
- **THEN** 系统 SHALL 展示 Success Criteria 勾选列表
- **AND** 用户逐条勾选后 SHALL 可点击「确认」按钮
- **AND** 确认后 Gate 状态 SHALL 变为已通过（视觉标记变化）

#### Scenario: Gate 交互 — button 类型

- **GIVEN** 用户到达 Gate 2（Phase 2 结尾）
- **WHEN** Gate 区域进入视口
- **THEN** 系统 SHALL 展示「确认设计基线」按钮
- **AND** 点击后 SHALL 自动滚动到 Phase 3 并展开后续 Phase

#### Scenario: Gate 状态持久化

- **GIVEN** 用户已完成 Gate 1 确认
- **WHEN** 用户刷新页面
- **THEN** 系统 SHALL 从 sessionStorage 恢复 Gate 1 已通过状态

### Requirement: CTA 终点

系统 SHALL 在场景末尾展示行动号召区域，引导用户进入下一步。

#### Scenario: 场景终点 CTA

- **GIVEN** 用户已完成 Phase 6 内容阅读
- **WHEN** 页面滚动到底部 CTA 区域
- **THEN** 系统 SHALL 展示安装命令（`git clone` + `stdd init` + `stdd install`）
- **AND** SHALL 提供「复制安装命令」和「查看完整教程」按钮
- **AND** 复制按钮点击后 SHALL 将命令复制到剪贴板并显示「已复制」提示
