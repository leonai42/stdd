# Spec: 代码结构摘要系统

> 对应板块 D（D1）| 1 个 New Capability
> code-structure-summary

## ADDED Requirements

### Requirement: BUILD 完成后生成结构增量 <!-- confidence: high -->

STDD SHALL 在 Phase 4 BUILD 完成后、进入 Phase 5 之前，由 AI 自动撰写 code-structure-delta.md。

**证据来源**：proposal.md `Capabilities > New > code-structure-summary`

#### Scenario: 生成 delta 文件 <!-- confidence: high -->

- **GIVEN** Phase 4 BUILD 所有切片 REFACTOR 完成
- **WHEN** AI 执行 build.md 的 Step N（生成代码结构增量）
- **THEN** AI SHALL 撰写 `changes/<name>/code-structure-delta.md`
- **AND** delta SHALL 包含：新增模块（路径/职责/关键符号/上下游依赖）、修改模块（变更内容和影响）、新增 API 端点（如有）、集成点、测试文件
- **AND** 头部 SHALL 标注 "置信度: 0.70 (AI-generated — 以源代码为准)" 和 git commit

#### Scenario: delta 与源代码一致性抽查 <!-- confidence: medium -->

- **GIVEN** code-structure-delta.md 已生成
- **WHEN** Phase 5 VERIFY 执行
- **THEN** AI SHALL 抽查 delta 中列出的文件是否存在、关键符号签名是否匹配
- **AND** 发现偏差时 SHALL 更新 delta

---

### Requirement: DELIVER 时合并到项目索引 <!-- confidence: high -->

STDD SHALL 在 Phase 6 DELIVER 时将 code-structure-delta.md 合并到 `.stdd/code-structure/index.md`。

**证据来源**：proposal.md `Capabilities > New > code-structure-summary`

#### Scenario: 合并 delta 到索引 <!-- confidence: high -->

- **GIVEN** Phase 6 DELIVER 正在执行
- **WHEN** `stdd deliver` 运行
- **THEN** CLI SHALL 复制 delta 到 `.stdd/code-structure/deltas/`
- **AND** 解析 delta 提取结构化数据更新 `.structure-index.yaml`
- **AND** 基于最新 index.yaml 重新生成 index.md（追加新 change 的模块 + 更新修改模块的描述）
- **AND** 更新 index.md 头部的 "最后更新" 时间戳和 git HEAD

#### Scenario: 首次合并时初始化目录 <!-- confidence: high -->

- **GIVEN** 项目首次执行 DELIVER，`.stdd/code-structure/` 不存在
- **WHEN** `stdd deliver` 执行
- **THEN** CLI SHALL 创建 `.stdd/code-structure/` 目录及所有子文件
- **AND** 生成初始的 index.md 和 .structure-index.yaml

---

### Requirement: 新 change 自动读取代码结构索引 <!-- confidence: high -->

STDD SHALL 在新 change 的 Phase 1/2 阶段自动读取 `.stdd/code-structure/index.md` 以加速代码结构理解。

**证据来源**：proposal.md `Capabilities > New > code-structure-summary`

#### Scenario: Phase 1 读取索引辅助 proposal <!-- confidence: medium -->

- **GIVEN** `.stdd/code-structure/index.md` 存在且状态为 FRESH（< 7 天）
- **WHEN** 新 change 的 Phase 1 UNDERSTAND 开始
- **THEN** AI SHALL 在执行 Step -1 时读取 index.md
- **AND** 在 proposal 的 Impact 评估中引用 "相关现有模块"（来自 index.md）

#### Scenario: 索引过时时输出警告 <!-- confidence: medium -->

- **GIVEN** index.md 的 last_updated > 7 天或 git HEAD 不一致
- **WHEN** AI 读取 index.md
- **THEN** AI SHALL 输出 "⚠️ 代码结构索引可能过时"
- **AND** 提示执行 `stdd structure rebuild` 重建索引

#### Scenario: 索引不存在时静默跳过 <!-- confidence: high -->

- **GIVEN** `.stdd/code-structure/` 目录不存在（新项目或未执行过 DELIVER）
- **WHEN** Phase 1 开始
- **THEN** AI SHALL 按照 V2.5 行为正常执行（从头扫描文件系统）
- **AND** 不输出任何错误或警告

---

### Requirement: CLI 命令支持 <!-- confidence: high -->

STDD SHALL 提供代码结构摘要相关的 CLI 命令。

**证据来源**：design.md `【CG-1】代码结构摘要系统 > CLI 命令`

#### Scenario: 全量重建索引 <!-- confidence: medium -->

- **GIVEN** index.md 严重过时或损坏
- **WHEN** 执行 `stdd structure rebuild`
- **THEN** 系统 SHALL 扫描所有 archive/ 中的 delta 文件，全量重建 index.md 和 .structure-index.yaml

#### Scenario: 查看模块结构 <!-- confidence: medium -->

- **GIVEN** index.md 包含 middleware/ 模块的信息
- **WHEN** 执行 `stdd structure show middleware`
- **THEN** 系统 SHALL 输出该模块的职责、关键符号、上下游依赖、变更历史

#### Scenario: 输出依赖关系图 <!-- confidence: medium -->

- **GIVEN** index.md 就绪
- **WHEN** 执行 `stdd structure graph`
- **THEN** 系统 SHALL 输出 ASCII 格式的依赖关系拓扑图
