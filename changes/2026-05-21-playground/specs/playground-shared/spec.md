# Capability: Playground 共享组件 (playground-shared)

## ADDED Requirements

### Requirement: 终端模拟样式

系统 SHALL 通过 `shared/terminal.css` 提供模拟终端视觉样式。

#### Scenario: 终端风格代码块渲染

- **GIVEN** 场景页中有一个代码块配置为 `type: "terminal"`
- **WHEN** stepper.js 渲染该代码块
- **THEN** 系统 SHALL 应用深色背景（`#1e1e2e` 或接近色）
- **AND** SHALL 使用等宽字体（Courier New / monospace）
- **AND** SHALL 显示模拟终端提示符（`$` 或 `>`）
- **AND** CSS 光标闪烁动画 SHALL 在最后一个字符后显示

#### Scenario: 语法高亮代码块

- **GIVEN** 场景页中有一个代码块配置了 `language: "python"`
- **WHEN** stepper.js 渲染该代码块
- **THEN** 系统 SHALL 通过 Prism.js 应用 Python 语法高亮
- **AND** Prism.js CDN 不可用时 SHALL 降级为 `<pre>` 标签纯文本
- **AND** 支持 Python、Bash、YAML 三种语言

### Requirement: Gate 标记样式

系统 SHALL 通过 `shared/badge.css` 提供 Gate 标记的统一样式。

#### Scenario: Gate 视觉区分

- **GIVEN** 场景页中有 3 道 Gate 标记
- **WHEN** badge.css 应用样式
- **THEN** Gate 1 SHALL 显示为 🔒 图标 + 黄色边框（确认 scope）
- **AND** Gate 2 SHALL 显示为 ⭐ 图标 + 金色边框（最关键分水岭）
- **AND** Gate 3 SHALL 显示为 🏁 图标 + 绿色边框（质量终审）
- **AND** 已通过的 Gate SHALL 显示为绿色填充 + ✓ 标记
- **AND** 未通过的 Gate SHALL 显示为灰色边框 + 锁定图标

#### Scenario: Gate 弹窗动画

- **GIVEN** 用户触发了 Gate 交互
- **WHEN** Gate 弹窗显示
- **THEN** 弹窗 SHALL 从底部滑入（`transform: translateY` 过渡）
- **AND** 背景 SHALL 叠加半透明遮罩（`rgba(0,0,0,0.5)`）
- **AND** 弹窗在移动端 SHALL 固定在视口底部（`position: fixed; bottom: 0`）

### Requirement: 分步导览引擎

系统 SHALL 通过 `shared/stepper.js` 提供可复用的分步导览逻辑。

#### Scenario: 数据驱动渲染

- **GIVEN** 一个包含 6 个 Phase 的 SCENARIO_DATA 对象
- **WHEN** 调用 `Stepper.init(containerId, SCENARIO_DATA)`
- **THEN** 系统 SHALL 在指定容器内渲染全部 Phase 的 DOM 结构
- **AND** Phase 区按顺序排列，ID 为 `phase-{id}`
- **AND** Gate 交互区嵌入在对应 Phase 末尾

#### Scenario: 阶段导航

- **GIVEN** Stepper 已初始化，当前在 Phase 2
- **WHEN** 用户点击「下一阶段」或滚动到 Phase 3
- **THEN** Phase 3 SHALL 从半透明变为完全不透明
- **AND** 导航指示器 SHALL 更新当前位置

#### Scenario: 零依赖运行

- **GIVEN** stepper.js 被加载到任意场景页
- **WHEN** 检查其依赖
- **THEN** stepper.js SHALL 不依赖任何第三方 JS 库
- **AND** SHALL 仅使用标准 DOM API 和 Intersection Observer API
