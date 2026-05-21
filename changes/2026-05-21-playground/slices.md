# Playground 切片执行计划

## Dependency Graph Summary

```
依赖拓扑排序：

Slice A: playground-shared (P0) — 零依赖
    │
    └──→ Slice B: playground-page (P0) — 依赖 A
              │
              ├──→ Slice C: api-rate-limit (P0) — 依赖 B ──┐
              │                                              ├─ 并行组 2
              ├──→ Slice D: user-pro-upgrade (P0) — 依赖 B ──┘
              │
              └──→ Slice E: nav-integration (P1) — 依赖 B
```

**并行化说明**：
- 并行组 1：无（仅 A 独立）
- 并行组 2：Slice C + Slice D（均依赖 B 完成，互不依赖，可并行）
- Slice E 可与 C/D 并行

## Slice Execution Plan

| # | 优先级 | 风险 | 预估工时 | 并行组 | TC 覆盖 | 实现目标 | 依赖 |
|---|--------|------|---------|--------|---------|---------|------|
| **A** | P0 | 🟢 Low | 1.5h (S) | — | TC-SHARED-001~005 | terminal.css + badge.css + stepper.js | 无 |
| **B** | P0 | 🟢 Low | 1h (S) | — | TC-PAGE-001~009 | playground/index.html + 场景页 HTML 模板 | A |
| **C** | P0 | 🟡 Med | 2h (M) | 组2 | TC-RATE-001~004 | api-rate-limit/data.js + style.css | B |
| **D** | P0 | 🟡 Med | 2h (M) | 组2 | TC-PRO-001~002 | user-pro-upgrade/data.js + style.css | B |
| **E** | P1 | 🟢 Low | 0.2h (XS) | 组2 | TC-PAGE-003 | website/index.html 导航栏 +1 链接 | B |

## Rationale

### Slice A: 共享组件（P0，先行）
- **零外部依赖**：纯 CSS/JS 文件，可独立开发和浏览器预览
- **低风险**：CSS 样式和 JS 逻辑均独立，不依赖页面结构
- **包含所有共享 TC**：terminal/badge/stepper 全覆盖

### Slice B: 页面框架（P0）
- **依赖 A 完成**：需要 terminal.css + badge.css + stepper.js 就绪才能写 HTML
- **低风险**：入口页结构简单（双卡片 + Hero），场景页模板仅加载 A 的资源

### Slice C+D: 场景内容（P0，可并行）
- C（API 限流）和 D（用户购买升级Pro）都是 data.js 填充工作
- 均依赖 B 的页面模板
- **并行组 2**：可同时开发，内容独立
- **中风险**：内容量大（~300-350 行/场景），需对照 LAUNCH_PLAN.md 逐 Phase 填写

### Slice E: 导航集成（P1）
- 依赖 B（入口页存在才能验证跳转）
- 工作量极小（1 行 `<a>` 标签），可与其他切片并行
