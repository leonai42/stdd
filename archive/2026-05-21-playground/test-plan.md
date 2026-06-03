# Playground 测试方案与详细案例

> 版本：V1.0
> 创建日期：2026-05-21
> 对应 Phase 2 Spec：playground-page / playground-api-rate-limit / playground-user-pro-upgrade / playground-shared

## 一、测试策略

### 1.1 测试策略

本项目为纯静态前端页面（HTML/CSS/JS），不包含后端逻辑或 Python 代码，因此：
- **视觉验证**（手工）：浏览器中打开页面，逐项检查渲染和交互，占总验证量 ~70%
- **HTML/CSS 语法检查**（工具）：W3C Validator + CSS Lint，占 ~15%
- **JS 功能测试**（手工）：按钮点击、Gate 交互、sessionStorage 持久化，占 ~15%
- 无 pytest 测试（不适用）

### 1.2 测试原则

- 每个 Scenario 的 GIVEN/WHEN/THEN 对应可目视检查的页面状态
- Gate 交互必须验证（checkbox 勾选、button 点击、状态持久化）
- 移动端响应式在至少 3 个断点检查（375px / 768px / 1440px）
- 代码高亮降级场景必须测试（禁用 CDN 后刷新）

### 1.3 已有测试资产

本项目为全新建设，无已有测试资产。

## 二、详细测试案例

### 功能 1：Playground 入口页

对应 Spec：playground-page → Requirement: 场景选择入口

#### 案例 1.1 — 入口页渲染

| 字段 | 内容 |
|------|------|
| **ID** | TC-PAGE-001 |
| **对应 Spec** | playground-page/spec.md → Scenario: 页面加载展示双场景卡片 |
| **优先级** | P0 |
| **预置条件** | 浏览器打开 `website/playground/index.html` |
| **输入** | 页面加载 |
| **预期结果** | Hero 标题可见，两个场景卡片并排显示，每个含名称/标签/时间/描述 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.2 — 场景卡片点击跳转

| 字段 | 内容 |
|------|------|
| **ID** | TC-PAGE-002 |
| **对应 Spec** | playground-page/spec.md → Scenario: 用户点击场景卡片跳转 |
| **优先级** | P0 |
| **预置条件** | 在入口页 |
| **输入** | 点击「API 限流」卡片 |
| **预期结果** | 跳转到 `api-rate-limit/index.html`；同样「用户购买升级Pro」跳转正确 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.3 — 导航栏链接

| 字段 | 内容 |
|------|------|
| **ID** | TC-PAGE-003 |
| **对应 Spec** | playground-page/spec.md → Scenario: 导航栏入口链接 |
| **优先级** | P1 |
| **预置条件** | 在官网主页 `website/index.html` |
| **输入** | 点击导航栏「Playground」 |
| **预期结果** | 跳转到 `playground/index.html` |
| **当前状态** | ❌ 测试缺 |

### 功能 2：分步导览框架

对应 Spec：playground-page → Requirement: 分步导览框架

#### 案例 2.1 — Phase 区渲染

| 字段 | 内容 |
|------|------|
| **ID** | TC-PAGE-004 |
| **对应 Spec** | playground-page/spec.md → Scenario: Phase 区渲染 |
| **优先级** | P0 |
| **预置条件** | 进入任一场景页 |
| **输入** | 页面加载完成 |
| **预期结果** | 6 个 Phase 分区可见，Phase 1 高亮展开，后续 Phase 半透明 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.2 — 滚动推进

| 字段 | 内容 |
|------|------|
| **ID** | TC-PAGE-005 |
| **对应 Spec** | playground-page/spec.md → Scenario: 滚动推进 Phase |
| **优先级** | P1 |
| **预置条件** | 在 Phase 1 底部 |
| **输入** | 向下滚动到 Phase 2 |
| **预期结果** | Phase 2 淡入，Phase 1 保持可见 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.3 — Gate checkbox 交互

| 字段 | 内容 |
|------|------|
| **ID** | TC-PAGE-006 |
| **对应 Spec** | playground-page/spec.md → Scenario: Gate 交互 — checkbox 类型 |
| **优先级** | P0 |
| **预置条件** | 滚动到 Gate 1 区域 |
| **输入** | 逐条勾选 3 项 Success Criteria → 点击确认 |
| **预期结果** | 确认后 Gate 标记变为绿色 + ✓，后续 Phase 解锁 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.4 — Gate button 交互

| 字段 | 内容 |
|------|------|
| **ID** | TC-PAGE-007 |
| **对应 Spec** | playground-page/spec.md → Scenario: Gate 交互 — button 类型 |
| **优先级** | P0 |
| **预置条件** | 滚动到 Gate 2 区域 |
| **输入** | 点击「确认设计基线」按钮 |
| **预期结果** | Gate 标记更新，页面自动滚动到 Phase 3 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.5 — Gate 状态持久化

| 字段 | 内容 |
|------|------|
| **ID** | TC-PAGE-008 |
| **对应 Spec** | playground-page/spec.md → Scenario: Gate 状态持久化 |
| **优先级** | P1 |
| **预置条件** | Gate 1 已通过 |
| **输入** | 刷新页面 |
| **预期结果** | Gate 1 仍显示已通过状态 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.6 — CTA 复制按钮

| 字段 | 内容 |
|------|------|
| **ID** | TC-PAGE-009 |
| **对应 Spec** | playground-page/spec.md → Scenario: 场景终点 CTA |
| **优先级** | P1 |
| **预置条件** | 滚动到页面底部 CTA 区域 |
| **输入** | 点击「复制安装命令」 |
| **预期结果** | 命令复制到剪贴板，按钮文字变为「已复制」 |
| **当前状态** | ❌ 测试缺 |

### 功能 3：场景一 — API 限流内容

对应 Spec：playground-api-rate-limit → Requirement: 场景数据内容

#### 案例 3.1 — Phase 1 内容完整性

| 字段 | 内容 |
|------|------|
| **ID** | TC-RATE-001 |
| **对应 Spec** | playground-api-rate-limit/spec.md → Scenario: Phase 1 UNDERSTAND 内容 |
| **优先级** | P0 |
| **预置条件** | 在场景一页面 |
| **输入** | 查看 Phase 1 内容 |
| **预期结果** | 用户输入终端模拟、proposal.md 结构化内容、Gate 1 的 3 项 SC 勾选 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.2 — Phase 2 SPEC 内容完整性

| 字段 | 内容 |
|------|------|
| **ID** | TC-RATE-002 |
| **对应 Spec** | playground-api-rate-limit/spec.md → Scenario: Phase 2 SPEC 内容 |
| **优先级** | P0 |
| **预置条件** | 在场景一页面 |
| **输入** | 滚动到 Phase 2 |
| **预期结果** | design.md 决策展示、3+ Scenario 的 GIVEN/WHEN/THEN、覆盖矩阵表格、Gate 2 按钮 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.3 — Phase 3-4 BUILD 动画

| 字段 | 内容 |
|------|------|
| **ID** | TC-RATE-003 |
| **对应 Spec** | playground-api-rate-limit/spec.md → Scenario: Phase 3-4 SLICE + BUILD 内容 |
| **优先级** | P0 |
| **预置条件** | Gate 2 已确认 |
| **输入** | 自动播放或手动推进 Phase 3-4 |
| **预期结果** | 切片拆分图、RED→GREEN→REFACTOR 动画、pending-adjustments 记录 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.4 — Phase 5-6 内容完整性

| 字段 | 内容 |
|------|------|
| **ID** | TC-RATE-004 |
| **对应 Spec** | playground-api-rate-limit/spec.md → Scenario: Phase 5 VERIFY 内容 + Phase 6 DELIVER 内容 |
| **优先级** | P0 |
| **预置条件** | 滚动到 Phase 5-6 |
| **输入** | 查看内容 |
| **预期结果** | 测试结果（22 passed）、11 类检查动画、Gate 3、追溯链、CTA |
| **当前状态** | ❌ 测试缺 |

### 功能 4：场景二 — 用户购买升级Pro 内容

对应 Spec：playground-user-pro-upgrade → Requirement: 场景数据内容

#### 案例 4.1 — Phase 1-2 业务内容

| 字段 | 内容 |
|------|------|
| **ID** | TC-PRO-001 |
| **对应 Spec** | playground-user-pro-upgrade/spec.md → Scenario: Phase 1 UNDERSTAND 内容 + Phase 2 SPEC 内容 |
| **优先级** | P0 |
| **预置条件** | 在场景二页面 |
| **输入** | 查看 Phase 1-2 |
| **预期结果** | 业务流程图、支付安全约束、4 个 capability 协作图、契约定义、Gate 1+2 |
| **当前状态** | ❌ 测试缺 |

#### 案例 4.2 — Phase 3-6 内容

| 字段 | 内容 |
|------|------|
| **ID** | TC-PRO-002 |
| **对应 Spec** | playground-user-pro-upgrade/spec.md → Phase 3-6 各 Scenario |
| **优先级** | P0 |
| **预置条件** | Gate 2 确认后 |
| **输入** | 推进到 Phase 3-6 |
| **预期结果** | 5 切片依赖图、Mock 演示、契约断层检查、跨 capability 追溯链、CTA |
| **当前状态** | ❌ 测试缺 |

### 功能 5：共享组件

对应 Spec：playground-shared → 各 Requirement

#### 案例 5.1 — 终端样式渲染

| 字段 | 内容 |
|------|------|
| **ID** | TC-SHARED-001 |
| **对应 Spec** | playground-shared/spec.md → Scenario: 终端风格代码块渲染 |
| **优先级** | P0 |
| **预置条件** | 场景页中有 type:terminal 代码块 |
| **输入** | 查看该代码块 |
| **预期结果** | 深色背景、等宽字体、`$` 提示符、CSS 光标闪烁 |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.2 — 语法高亮

| 字段 | 内容 |
|------|------|
| **ID** | TC-SHARED-002 |
| **对应 Spec** | playground-shared/spec.md → Scenario: 语法高亮代码块 |
| **优先级** | P0 |
| **预置条件** | 场景页中有 Python/Bash/YAML 代码块 |
| **输入** | 查看代码块 |
| **预期结果** | Prism.js 语法高亮生效；CDN 禁用时降级为纯文本 `<pre>` |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.3 — Gate 视觉区分

| 字段 | 内容 |
|------|------|
| **ID** | TC-SHARED-003 |
| **对应 Spec** | playground-shared/spec.md → Scenario: Gate 视觉区分 |
| **优先级** | P0 |
| **预置条件** | 场景页中有 3 道 Gate |
| **输入** | 查看各 Gate |
| **预期结果** | Gate 1 黄色/🔒、Gate 2 金色/⭐、Gate 3 绿色/🏁；通过后绿底+✓ |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.4 — 移动端响应式

| 字段 | 内容 |
|------|------|
| **ID** | TC-SHARED-004 |
| **对应 Spec** | playground-shared → 各 Scenario 移动端行为 |
| **优先级** | P1 |
| **预置条件** | Chrome DevTools 切换为 375px 视口 |
| **输入** | 查看入口页和场景页 |
| **预期结果** | Phase 区单列堆叠、Gate 弹窗固定底部、卡片全宽、字体可读 |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.5 — stepper.js 零依赖

| 字段 | 内容 |
|------|------|
| **ID** | TC-SHARED-005 |
| **对应 Spec** | playground-shared/spec.md → Scenario: 零依赖运行 |
| **优先级** | P1 |
| **预置条件** | 场景页已加载 |
| **输入** | 在 Console 中检查 `Stepper` 对象 |
| **预期结果** | `Stepper.init()` 可调用，不报第三方库缺失错误 |
| **当前状态** | ❌ 测试缺 |

## 三、测试执行矩阵

| 功能模块 | 视觉检查 | 交互测试 | 跨浏览器 | 移动端 | 状态 |
|----------|---------|----------|----------|--------|------|
| 入口页 | 2 TC | 1 TC | Chrome/Firefox/Edge | 375/768px | 🔴 |
| 场景一内容 | 4 TC | Gate 交互 | Chrome/Firefox/Edge | 375/768px | 🔴 |
| 场景二内容 | 2 TC | Gate 交互 | Chrome/Firefox/Edge | 375/768px | 🔴 |
| 共享组件 | 3 TC | 1 TC | Chrome/Firefox/Edge | 375/768px | 🔴 |

## 四、回归风险矩阵

| 风险区域 | 改动 | 已有回归保护 | 风险等级 |
|----------|------|-------------|---------|
| 官网导航栏 | +1 Playground 链接 | 无自动测试 | 🟢 低风险 |
| 现有官网页面 | 无改动 | 无 | 🟢 零风险 |

## 五、建议补充顺序

全部 18 个 TC 均为 P0/P1，无 P2。建议顺序：
1. **第一优先**（实现阶段逐一验证）：TC-SHARED-*（组件先通）→ TC-PAGE-*（框架）→ TC-RATE-* + TC-PRO-*（数据填充）
2. **第二优先**（部署前）：TC-SHARED-004（移动端）+ TC-SHARED-002 降级场景
3. **第三优先**（后续）：跨浏览器兼容性验证
