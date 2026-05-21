# V2.4：自学习经验库 + AI 辅助增强 + CI/CD 集成 - 技术设计

## Context

STDD V2.3 系统现状：
- 技能系统：6 个阶段技能文件（纯 Markdown + YAML frontmatter），由 AI 按指令执行
- CLI：11 个命令模块，遵循 `cmd_<name>(args)` 模式，动态导入
- 配置：4 个 `config.d/*.yaml` 文件，由 `read_config()` 合并
- 模板：9 个 Markdown 模板定义产出物结构
- 测试：pytest + fixtures (`temp_project`, `sample_change` 等)
- 缺失：无结构化跨 change 数据存储，无 CI/CD 集成代码，切片/生成逻辑纯文本驱动

## Decisions

### 1. 经验数据格式：YAML frontmatter + Markdown body

**方案**：采用与技能文件相同的混合格式 — YAML frontmatter 存储结构化元数据（category、severity、confidence、occurrences 等），Markdown body 存储 AI 可读的自由文本（详细描述、代码示例）。

**为什么**：(1) 与现有技能文件格式一致，降低认知负担；(2) YAML frontmatter 可被 CLI 快速解析用于索引和过滤；(3) Markdown body 可被 AI 在上下文中直接阅读理解。

**备选方案及排除原因**：
- 纯 JSON/YAML 文件：结构性强但 AI 可读性差，不适合在技能上下文中直接使用
- SQLite 数据库：查询能力强但引入新依赖，且不符合"文件系统即数据库"的 Git 友好哲学

### 2. 经验索引：自动维护的 YAML 索引文件

**方案**：在 `.stdd/experiences/.experience-index.yaml` 中维护一个按 category/language/lifecycle/severity 分组的经验 ID 列表，由 CLI 在 add/update 时自动重写。

**为什么**：(1) 避免每次加载经验时遍历所有文件并解析 YAML frontmatter；(2) 索引文件可被 git diff 清晰展示变更；(3) 索引损坏可从原始文件重建。

### 3. 经验匹配策略：精确 category + 标签交集

**方案**：Phase 4 加载经验时，按当前切片的 language（来自 project.yaml）+ 能力名称作为 tag 进行精确匹配。不做 NLP 语义相似度匹配。

**为什么**：(1) 精确匹配零误报；(2) V2.4 经验库规模小（通常 < 50 条），精确匹配足够；(3) 语义匹配留给 V2.5+ 社区经验池大规模数据场景。

### 4. Spec 自动补全：置信度基于 proposal 字段来源

**方案**：直接从 proposal.md 结构化字段（Why / What Changes / Capabilities / Success Criteria / Impact）提取内容生成 spec 草稿。标记为 ✓（高置信度）当生成项直接对应某个 proposal 字段；标记为 ⚠（低置信度）当是 AI 推断的补充内容。

**为什么**：(1) 置信度有明确审计线索（每个 ✓ 可追溯到 proposal 具体字段）；(2) 用户只需审核 ⚠ 项和确认 ✓ 项，而非从零写 spec。

### 5. 依赖图构建：精确 capability 目录名匹配

**方案**：`stdd dependency-graph` 解析 specs 中每个 Scenario 的 GIVEN 子句，仅当 GIVEN 文本中包含其他 capability 的目录名时才建立依赖边。不使用 NLP 模糊匹配。

**为什么**：(1) 零误报，依赖关系确定性强；(2) 实现简单（正则 + 字符串匹配）；(3) 团队在写 GIVEN 时会自然使用 capability 名称。

**备选方案及排除原因**：
- NLP 语义匹配：误报率高，不适合作为确定性依赖分析工具

### 6. CI 失败检查：CLI 确定性子集 + AI 全量检查

**方案**：`stdd ci check-failures` 实现 11 类失败模式中可确定性检查的子集（文件存在性、TC-ID 唯一性、SHALL 关键字、AND 子句数、覆盖矩阵完整性等约 60%）。剩余需要语义理解的检查（运行时行为偏差、上下文丢失、指令衰减等约 40%）保留在 verify.md 技能中由 AI 执行。

**为什么**：(1) 明确能力边界，避免给用户"CLI 能完全替代 AI 检查"的错觉；(2) CLI 检查可在 CI 流水线中零成本运行，AI 检查在需要深度分析时手动触发。

### 7. CLI 架构：遵循现有模式，不引入新依赖

**方案**：4 个新命令模块完全遵循现有 `cmd_<name>(args: argparse.Namespace) -> None` 模式，注册在 `stdd/cli/__init__.py` 中。所有文件操作使用 Python 标准库（yaml, json, pathlib, re）。不引入新依赖。

**为什么**：(1) 保持 CLI 架构一致性；(2) 零额外依赖降低安装摩擦；(3) 测试可完全复用现有 fixtures。

## Architecture

```
V2.4 新增组件
────────────────────────────────────────────────────

┌─ .stdd/experiences/ ─────────────────────────────┐
│  EXP-YYYY-NNNN.md  (YAML frontmatter + MD body)   │
│  .experience-index.yaml  (auto-generated)         │
└───────────────────────────────────────────────────┘
         ▲ 读写                    ▲ 自动记录
         │                        │
  ┌──────┴──────┐          ┌─────┴──────────────┐
  │ experience  │          │ verify.md Step 3.5 │
  │ CLI (list/  │          │ (auto-record new   │
  │ add/stats/  │          │  experiences)      │
  │ pull/export)│          └────────────────────┘
  └─────────────┘
                             ┌────────────────────┐
  ┌──────────────────┐       │ build.md Step 0.5  │
  │ extract-proposal │       │ (load matching     │
  │ CLI              │       │  experiences)      │
  └──┬───────────────┘       └────────────────────┘
     │ 结构化 JSON/YAML
     ▼
  ┌──────────────────┐       ┌────────────────────┐
  │ spec.md 增强     │       │ slice.md 增强       │
  │ (auto-extract +  │       │ (五步分析 +        │
  │  confidence tags)│       │  dependency-graph) │
  └──────────────────┘       └────────────────────┘

  ┌──────────────────┐
  │ ci CLI           │
  │ (init/generate/  │
  │  check-failures) │
  └──┬───────────────┘
     │ 生成模板
     ▼
  ┌──────────────────────────────────────────────────┐
  │ .github/workflows/stdd-quality.yml               │
  │ .pre-commit-config.yaml                          │
  │ .github/stdd-pr-comment.md                       │
  └──────────────────────────────────────────────────┘
```

**数据流**：
1. proposal.md → `extract-proposal` → 结构化 JSON → spec.md 增强生成 spec 草稿
2. spec.md + test-plan.md → `dependency-graph` → 依赖图 JSON → slice.md 增强生成切片计划
3. Phase 4 BUILD → `build.md Step 0.5` → 读取 `.experience-index.yaml` → 加载匹配经验 → 植入检查点
4. Phase 5 VERIFY → `verify.md Step 3.5` → 检测新失败模式 → 创建 EXP 文件 → 更新索引
5. `stdd ci check-failures` → 读取 spec + test-plan + 源码 → 运行 60% 确定性子集检查 → 输出报告

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| 经验 ID 冲突（多人同时 add） | `.experience-index.yaml` 写入时使用临时文件 + 原子重命名 |
| 依赖图误报（GIVEN 中意外包含 capability 名） | 仅精确匹配 `specs/<name>/` 目录名，非子串匹配 |
| 技能文件膨胀（spec.md / slice.md / build.md / verify.md 均增加内容） | 新行为提取到 `_shared/` 片段中按需引用 |
| CI 失败检查覆盖率有限（60%） | CLI 输出明确标注"这是确定性检查子集，完整检查请使用 /stdd-verify" |
| 置信度标签不准确（AI 可能错标 ✓） | 要求 AI 在每个 ✓ 标签旁注明 proposal 来源字段，用户审核时可直接验证 |
| 经验库文件随项目增长（>1000 条时索引性能下降） | V2.4 规模目标 < 100 条（项目级），V2.5 社区池引入分页和搜索 API |
