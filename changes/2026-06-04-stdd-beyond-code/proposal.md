# STDD Beyond Code — 学术论文撰写与对外发布

> 状态：Phase 1 | Gate 1 待确认
> 基线：STDD V2.8 | 类型：非编程 Change（研究/写作/设计）

## Why

### 背景

STDD 从 V1.0 到 V2.8 经历了 13 个版本迭代，方法论和工具链已趋于成熟。但目前的对外认知仍局限在"AI 编程质量工具"的定位上。我们通过 V2.7 的 Agent 验证管线和 V2.8 的实践验证，已经证明 STDD 的核心方法论（定义预期→验证结果→积累经验）不依赖"代码"这一介质。

### 三个需要解决的认知缺口

1. **学术论证空白**：目前市面上没有一篇系统论证"AI 编程方法论可以扩展到非编程领域"的学术论文。Spec Kit、OpenSpec、BMAD 等框架都局限于编程场景。

2. **实践证据分散**：STDD 在量化交易（TStrategy V4.2）、官网维护（website V2.5）、文档管理（AI_CODING_METHODOLOGY_COMPARISON.md）等非编程场景已有实际应用，但缺乏系统整理。

3. **对外传播需要**：一篇高质量的论文 + 一份精美的 PPT 是让外界（学术界、企业决策者、潜在用户）理解 STDD 真正价值的核心物料。

### 为什么这个任务适合用 STDD 管理

这是 STDD 方法论在"研究写作"场景的首次完整应用。任务本身就具有双重价值：既产出论文和 PPT，又验证 STDD 在非编程场景的可行性。

## What Changes

### 主要产出

1. **学术论文**（`ppt/STDD_BEYOND_CODE_PAPER.md`）：数万字级别，完整学术结构
   - 章节：摘要 → 引言 → 文献综述 → 方法论 → 技术实现 → 应用案例 → 效果评估 → 讨论 → 结论 → 参考文献
   - 引用 30+ 篇国内外文献
   - 论证 STDD 方法论从编程到通用执行验证的扩展路径

2. **演示 PPT**（`ppt/beyond-code.html`）：基于论文内容的 25-30 页演示文稿
   - 基于现有 ppt/ 框架（靛蓝瓷主题 + motion.js 动画）
   - 覆盖论文所有核心章节
   - 支持键盘翻页 + 触屏手势 + 响应式

3. **通用场景指南**（`STDD_BEYOND_CODE.md`）：面向用户的实用文档（已有初稿）

### 论文核心论证结构

```
背景与问题 → 可行性分析 → 路径探索 → 方案设计 → 理论与实证支撑 → 效果评估 → 展望 → 结论
```

## Capabilities

### New Capabilities
- **beyond-code-paper**：完整的学术论文，约 3-5 万字
- **beyond-code-ppt**：25-30 页演示文稿

### Modified Capabilities
- **beyond-code-guide**：`STDD_BEYOND_CODE.md` 场景指南（已有初稿，本次定稿归档）

## Impact

**代码/文件层面**：
- `ppt/STDD_BEYOND_CODE_PAPER.md` — 新增（~3000-5000 行）
- `ppt/beyond-code.html` — 新增或替换（~500 行）
- `STDD_BEYOND_CODE.md` — 修改定稿

**时间估算**：
- Phase 1-2（需求+设计）：1h
- Phase 4（论文撰写）：8-12h
- Phase 4（PPT 制作）：3-4h
- Phase 5（审核验证）：2h

**基础设施**：无

## Constraints

- 论文使用 Markdown 格式，便于版本控制和协作
- PPT 使用纯 HTML/CSS/JS，零外部依赖
- 引用文献需标注来源，确保可查证
- 案例数据需真实可追溯（优先使用 STDD 自身案例 + 公开数据）

## Risk Areas

- capability: beyond-code-paper — 论文质量不足可能导致学术可信度受损。缓解：多轮审校 + 引用充足文献
- capability: beyond-code-ppt — PPT 与论文内容脱节。缓解：PPT 严格基于论文结构生成，每页标注对应论文章节

## NonGoals

- 不投递学术期刊（本次仅内部发布 + 官网展示）
- 不做英文版论文（后续可翻译）
- 不做视频/动画演示

## Success Criteria

- [ ] 论文 ≥ 30,000 字（中文）
- [ ] 论文章节完整：摘要/引言/文献综述/方法论/技术/案例/评估/讨论/结论/参考文献
- [ ] 引用 ≥ 30 篇国内外文献
- [ ] 论文包含至少 5 个详细的非编程场景案例分析
- [ ] PPT ≥ 25 页，覆盖论文所有章节
- [ ] PPT 中英文混杂（标题中英双语，正文中文）
- [ ] 论文通过 2 轮人工审校
- [ ] PPT 在 Chrome/Firefox/Edge 中正常显示
- [ ] STDD change 完整归档（proposal → specs → test-report → archive）
