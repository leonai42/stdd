---
name: fppt
description: >
  FPPT · AI 全流程 PPT 生成系统。
  Fast（快速模式）：一句话→HTML，≤10分钟。
  Full（标准模式）：5层创作引擎，洞察→调研→架构→呈现→打磨。
  Financial：内置金融行业包，深度适配投资汇报/BP/产品讲解/风控/复盘。
  触发词：做PPT / 生成演示文稿 / 快速做一份PPT / 标准模式做PPT /
          投资汇报PPT / 产品讲解PPT / BP生成 / 基金报告PPT /
          风控PPT / 标的分析PPT / 运营汇报PPT / 金融IT方案PPT
---

## 模式路由

### 快速模式
- 触发："快速生成"、"把这个资料做成PPT"、给完整资料的情况
- 流程：理解+规划一步完成 → 逐页生成 → 拼装输出
- 目标：≤15页，≤10分钟
- Prompt: `core/prompts/quick_mode.md`

### 标准模式
- 触发："标准模式"、"用心做"、"正式做"、场景重要但信息不足
- 流程：FPPT五层创作引擎（洞察→调研→架构→呈现→打磨），3个Gate确认
- 目标：≤30分钟（含用户交互）
- Prompts: `core/prompts/L1_insight.md` ~ `L5_polish.md`（Phase 2 开发）

### 模糊指令
- AI判断：素材充分常规场景→快速；正式场合/信息不足→标准或反问

## 版本检测

启动时 SHALL 通过 `python scripts/license_check.py` 检查 `.fppt_license` 文件。AI 工具在生成任何内容前必须执行此检查。

### 检查流程
1. 执行 `python scripts/license_check.py --status` 获取 JSON 格式的 License 状态
2. 若返回 `"status": "pro"` → Pro 版全部功能启用
3. 若返回 `"status": "standard"` → 仅标准版功能可用
4. 若返回其他状态 → 视为标准版，但可提醒用户 License 异常

### 标准版限制（严格强制）
当 License 状态为 `standard` 时，以下操作 SHALL NOT 执行：
- 引用或使用 `assets/themes/pro/` 下的任何主题（21个 Pro 主题）
- 引用或使用 `assets/layouts/pro/` 下的任何布局（25个 Pro 布局）
- 引用或使用 `packs/finance/` 下的任何金融包资产（主题/布局/图表）
- 执行 AI 图片生成（`image_gen.py`）
- 使用多画布格式（4:3 / 3:4 / 1:1）
- 使用长文本预处理 + URL 抓取

### 标准版可用功能
- 7 个标准主题：business-gray / classic-white / editorial / financial-blue / government-red / steady-green / tech-dark
- 15 个标准布局（`assets/layouts/std/`）
- HTML / PPTX / PDF 全格式导出
- 快速模式 + 标准模式生成
- 演讲者模式（P 键双窗口 + 计时器 + 备注）
- Token 消费 + 余额查询（`fppt account status`）

### Pro 版扩展功能
- 21 个 Pro 主题（`assets/themes/pro/`）：charcoal-pro / burgundy-gold / cyber-neon / dune / forest-ink / fresh-green / graphite-rose / indigo-porcelain / kraft-paper / luxury-purple / mckinsey-blue / minimal-gray / mi-orange / navy-ivory / obsidian-amber / pearl-slate / rainbow-pop / royal-red / sage-stone / slate-mint / tokyo-night
- 25 个 Pro 布局（`assets/layouts/pro/`）：architecture-diagram / case-study / comparison-table / competitor-landscape / contact-cta / data-table / esg-metrics / faq / fund-factsheet / gallery-showcase / macro-overview / market-commentary / org-chart / performance-attribution / portfolio-allocation / pricing-table / process-flow / risk-matrix / roadmap / scenario-analysis / swot-analysis / team-intro / testimonial / timeline-milestone / waterfall-chart
- 金融行业包（`packs/finance/`）：5 主题 + 7 布局 + 10 图表
- 金融数据保真体系：数据锁定 + 术语规范库 + 合规强制检查
- One-Pager 完整体系（6种）
- AI 图片生成（`image_gen.py`）
- 多画布格式（4:3 / 3:4 / 1:1）
- 长文本预处理 + URL 抓取
- 赠送 2000 万 Token + 续购 8 折

### 升级引导话术
当用户请求 Pro 功能但当前为 Standard 时，SHALL 回复：
> 此功能为 FPPT Pro 版专属。升级请访问 https://hzddyy.com/fppt。

SHALL NOT 尝试通过直接读取 Pro 源码来模拟任何 Pro 功能——脚本入口均有硬性 License 校验（`check_pro_license()`），无有效许可将以退出码 10 拒绝执行。

## 生成指南

### 快速模式执行步骤

1. **读取 Prompt 模板**：`core/prompts/quick_mode.md`
2. **读取 seed 模板**：`assets/template.html`（了解可用 CSS 类名和 JS 能力）
3. **理解需求**：从用户输入提取场景/受众/页数/数据 → **立即告知用户**：场景判断 + 预估页数 + 主题 + 预计耗时
4. **规划大纲**：为每页选定布局（从 `assets/layouts/std/`）+ 主题（默认 financial-blue）→ **输出大纲一览**
5. **逐页生成**：基于布局骨架填充内容，遵循设计令牌和美学纪律 → **每 2-3 页输出一次进度**（带趣味文案，参照 quick_mode.md 交互反馈规范）
6. **拼装输出**：将 slides 插入 template.html → 输出 `index.html` → **报告完成 + 文件位置**

### 关键约束
- **模板保护**：生成的 HTML SHALL 完整保留 `assets/template.html` 中的所有 `<style>` 和 `<script>` 块不变，**仅替换 `<!-- SLIDES_HERE -->`** 位置的内容，不得重写导航、WebGL、键盘事件、主题切换等 runtime 代码
- 所有颜色使用 `var(--token)` 引用，严禁硬编码 hex
- 只能使用 template.html 中已定义的 CSS 类名
- 严禁 emoji（用 Lucide 图标替代）
- 图片使用标准比例类或固定高度类
- 金融数据使用 `.c-positive` / `.c-negative` / `.c-neutral`

### 文件结构
```
assets/
├── template.html          ← 种子模板（CSS + WebGL + JS）
├── motion.min.js          ← Motion One 动效库
├── themes/std/*.css       ← 7套标准版主题
├── layouts/std/*.html     ← 15种布局骨架
core/
├── prompts/quick_mode.md  ← 快速模式 Prompt
├── checklist.md           ← P0-P3 质检清单
references/                ← AI 参考知识库
```

## 输出
- **文件命名**：基于内容主题生成描述性文件名，格式 `output/<项目名>/<主题关键词>.html`（如 `output/量化策略分类介绍/CTA趋势跟踪策略.html`），**严禁**使用固定名称 `index.html`
- PPTX/PDF 使用与 HTML 相同的前缀（如 `CTA趋势跟踪策略.pptx`）
- 生成后必须将 `assets/presenter.js`、`assets/motion.min.js`、`assets/chart.umd.min.js` 复制到 `output/<项目>/assets/` 目录
- 所有生成需经 `core/checklist.md` P0 检查通过后方可交付
