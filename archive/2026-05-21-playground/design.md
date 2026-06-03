# STDD Playground - 技术设计

## Context

- 现有官网：`website/index.html`（806 行单文件），深蓝+绿色设计语言，固定导航栏+多 Section 布局
- 技术栈：纯静态 HTML/CSS/JS，零框架，零构建工具
- 目标平台：现代浏览器（Chrome/Firefox/Safari/Edge），移动端响应式
- 双重约束：① 内容需与 LAUNCH_PLAN.md 一致；② 视觉需与官网统一

## Decisions

### 1. 页面架构：入口页 + 按场景分页

**方案**：`playground/index.html` 为场景选择入口，两个场景各独立 `index.html`（`api-rate-limit/` + `user-pro-upgrade/`），共享 CSS/JS 通过 `../shared/` 引用。

**为什么**：(1) 每个场景内容量大（6 个 Phase），单页会过重；(2) 独立 URL 方便分享和统计追踪；(3) 共享资源真正复用。

**备选方案及排除原因**：
- SPA 单页切换：需 JS 路由，增加复杂度
- 全部内联到入口页：单文件过大（1500+ 行），加载慢

### 2. 内容架构：data.js + stepper.js 分离

**方案**：场景内容存储在 `data.js`（结构化 JS 对象），由共享 `stepper.js` 负责渲染和 Gate 交互。

**为什么**：(1) 内容与逻辑分离，加新场景只需新 data.js；(2) data.js 可被非技术人员修改；(3) stepper.js 可复用。

**data.js 结构**：
```
SCENARIO_DATA = {
  title, subtitle,
  phases: [
    { id, title, sections: [{type, content}], gate: {type, items} },
    ...
  ],
  cta: { text, url }
}
```

### 3. 代码高亮：Prism.js CDN

**方案**：Prism.js（unpkg CDN），仅加载 Python + Bash + YAML 三种语言（~15KB gzip）。

**为什么**：(1) 零项目文件负担；(2) 体积小；(3) 降级简单（CDN 不可用时显示纯文本 `<pre>`）。

### 4. 动画：CSS Transition + Intersection Observer

**方案**：Phase 内容显隐用 Intersection Observer + CSS `opacity` 淡入。Gate 弹窗 `position: fixed` + `transform`。

**为什么**：零 JS 动画库，浏览器原生优化，旧浏览器降级为直接显示。

### 5. 移动端响应式

**方案**：桌面 2 列布局，<768px 堆叠为单列。Gate 在移动端固定于视口底部。

### 6. 代码块为静态模拟终端

**方案**：深色背景 + 等宽字体 + CSS 光标动画，不执行任何真实命令。

**为什么**：安全、确定性、零后端依赖。

## Architecture

```
website/
├── index.html                       # 官网主页（修改：+Playground 导航链接）
└── playground/
    ├── index.html                   # 入口（场景选择双卡片）
    ├── api-rate-limit/
    │   ├── index.html               # 场景页（加载 data.js + ../shared/stepper.js）
    │   ├── data.js                  # 6 Phase 结构化数据
    │   └── style.css
    ├── user-pro-upgrade/
    │   ├── index.html
    │   ├── data.js
    │   └── style.css
    └── shared/
        ├── terminal.css             # 终端模拟样式
        ├── badge.css                # Gate 标记样式（🔒/⭐/🏁）
        └── stepper.js               # 渲染引擎 + Gate 交互 + 滚动控制
```

**渲染流程**：
```
用户选择场景 → index.html 跳转 → 场景页加载
  → stepper.js 读取 SCENARIO_DATA → 渲染 DOM
  → 用户滚动/点击 → stepper 切换 visible Phase
  → 遇到 Gate → 弹出交互（checkbox/button）
  → 完成 Gate → 解锁后续 Phase
  → 终点 → CTA（GitHub/教程链接）
```

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| data.js 内容量大维护成本高 | 结构化格式统一，字段名自解释 |
| 移动端 Phase 内容过长滚动疲劳 | 默认仅展开当前+下一 Phase |
| Prism.js CDN 不可用 | `<pre>` 降级，不影响可读性 |
| Gate 交互状态刷新丢失 | `sessionStorage` 保存状态 |
