# STDD Playground — 交互式体验页面

<!-- STDD-MARKER: title -->

## Why

STDD 的核心理念「模糊需求 → 6 阶段流程 → 高质量交付」用文字描述门槛高。潜在用户需要在 5 分钟内，无需安装任何东西，直观感受 STDD 的实际工作方式。Playground 是降低认知门槛、驱动转化的关键入口。

## What Changes

<!-- STDD-MARKER: what_changes -->

- 新建 `website/playground/` 目录，包含 Playground 入口页和两个演示场景
- 实现分步导览交互（Phase 区滚动 + Gate 节点交互）
- 场景一「API 限流」：展示技术后端型需求的完整 6 阶段流程
- 场景二「用户购买升级Pro」：展示业务功能型需求的完整 6 阶段流程（含多 capability 协作）
- 复用官网设计语言（配色/字体/卡片），保持视觉一致性

## Capabilities

### New Capabilities

<!-- STDD-MARKER: new_capabilities -->

- **playground-page**：Playground 主页面 — 场景选择入口 + 分步导览框架（Phase 区 + Gate 标记 + CTA）
- **playground-api-rate-limit**：场景一「API 限流」— 6 个 Phase 的预渲染内容（data.js），展示令牌桶算法、中间件架构、限流策略
- **playground-user-pro-upgrade**：场景二「用户购买升级Pro」— 6 个 Phase 的预渲染内容（data.js），展示支付流程、状态机、多 capability 协作
- **playground-shared**：共享组件 — 终端模拟样式（terminal.css）、Gate 标记样式（badge.css）、分步导览逻辑（stepper.js）

### Modified Capabilities

- **website-nav**：官网导航栏增加 Playground 入口链接

## Impact

<!-- STDD-MARKER: impact -->

**代码层面**：
- `website/playground/index.html`（新增，~80 行）— Playground 入口页
- `website/playground/shared/terminal.css`（新增，~100 行）— 终端模拟样式
- `website/playground/shared/badge.css`（新增，~60 行）— Gate 标记样式
- `website/playground/shared/stepper.js`（新增，~200 行）— 分步导览逻辑
- `website/playground/api-rate-limit/data.js`（新增，~300 行）— 场景一内容
- `website/playground/api-rate-limit/style.css`（新增，~50 行）
- `website/playground/user-pro-upgrade/data.js`（新增，~350 行）— 场景二内容
- `website/playground/user-pro-upgrade/style.css`（新增，~50 行）
- `website/index.html`（修改，+3 行）— 导航栏增加链接

**配置层面**：
- 无

**基础设施**：
- 无（纯静态 HTML/CSS/JS，无框架依赖）
- 代码高亮：Prism.js（轻量 CDN，按需加载语言）

## Success Criteria

<!-- STDD-MARKER: success_criteria -->

- [ ] Playground 入口页可在浏览器中正常渲染，两个场景选择卡片可见
- [ ] 场景一分步导览完整展示 6 个 Phase + 3 道 Gate，内容与 LAUNCH_PLAN.md Section 2.3 一致
- [ ] 场景二分步导览完整展示 6 个 Phase + 3 道 Gate，内容与 LAUNCH_PLAN.md Section 2.4 一致
- [ ] Gate 1/2/3 交互节点可点击交互（勾选确认 / 按钮确认）
- [ ] 终端代码块有语法高亮
- [ ] 导航栏「Playground」链接正确跳转
- [ ] 移动端响应式：Phase 区堆叠显示，Gate 标记可视
- [ ] 页面加载性能：首次内容绘制 < 1.5s（纯静态，无外部依赖）
