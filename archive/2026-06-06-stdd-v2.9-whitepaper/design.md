# STDD V2.9 白皮书 — 详细大纲（Phase 2 SPEC）

## 文档信息
- 版本：V2.9.3
- 输出：`STDD_WHITEPAPER_V2.9_CN.md`
- 预计规模：~64 章，~5000 行 Markdown

---

## Part 0: 前置

### Ch00 版本声明与文档约定
- V2.9.3 版本锁定、V3.0 公开发布声明
- 目标读者、阅读约定

### Ch01 术语表
- 60+ 核心术语中英对照

---

## Part 1: 总论

### Ch02 STDD 是什么
- 定义、解决的三个核心问题、与 TDD/BDD/DDD 的关系

### Ch03 九大核心原则
- Spec-first / TDD execution / 可追溯调整 / Gate 确认驱动 / 模板先行 / 垂直切片 / 强制测试 / 行为测试 / 自学习

### Ch04 六阶段流程总览
- 状态机图、各阶段产出物总表、Gate 位置、模式选择点

---

## Part 2: 六阶段详解

### Ch05 Phase 1: UNDERSTAND
- 6 步流程、proposal 字段、复杂度评分（6 维度 0-17 分）、Gate 1 协议

### Ch06 Phase 2: SPEC
- CLI 提取 → 经验加载 → design.md → Canonical YAML 生成 → 锚定评估 → Gate 2

### Ch07 Phase 3: SLICE
- 5 步分析、拓扑排序、并行组、三档模式差异

### Ch08 Phase 4: BUILD
- RED→GREEN→REFACTOR、切片验证、设计偏离处理、三档模式差异

### Ch09 Phase 5: VERIFY
- 多代理审查 → 测试执行 → diff → 12 失败模式 → 调整汇总 → Gate 3

### Ch10 Phase 6: DELIVER
- archive → specs 合并 → canon verify → git tag、三档模式差异

---

## Part 3: 关键机制

### Ch11 三道强制确认门
- Gate 1/2/3 位置、三种确认通道、Gate 顺序强制

### Ch12 三档执行模式
- 轻量/标准/彻底对比表、TDD 基线、task_type 支持

### Ch13 复杂度评分模型
- 6 维度详解、阈值、置信度、边界情况

### Ch14 设计调整追溯
- minor/major 分类、pending-adjustments、Phase 5 汇总

### Ch15 双向追溯链
- Spec→TC→Test→Code、TC-ID 规则、stdd trace/diff

### Ch16 长程模式
- 预授权流程、7 约束、降级条件、双实例启动

### Ch17 批次目录管理
- 三策略、_batch/ 结构、反碰撞设计

### Ch18 上下文工程
- phase-context.md、预算检查、状态新鲜度

### Ch19 生命周期 Hooks
- SessionStart / PreCompact / Stop、install/status/uninstall

### Ch20 智能门禁
- 三层架构、4 级分类器、关键词评分、Guard 操作

---

## Part 4: 质量体系

### Ch21 十二类失败模式
- (a)-(l) 完整目录、检测触发、示例、修复模板

### Ch22 pass@k 统计验证
- k 次重复、歧义检测、模式差异

### Ch23 Plankton 多级自动修复
- L1/L2/L3、stdd fix CLI

### Ch24 Agent 验证管线
- 4 子代理、CP 系统、agent_spec.yaml

### Ch25 CI/CD 集成
- stdd ci 命令树、GitHub Actions、Pre-commit

---

## Part 5: Spec 锚定法

### Ch26 锚定法总论
- 问题：LLM 非确定性来自 Spec 歧义、反模式

### Ch27 L1 行为锚定
- SHALL 强制行为、Scenario 覆盖、示例

### Ch28 L2-L4 高级锚定
- L2 接口/L3 模式/L4 基线、适用标准、成本收益

---

## Part 6: 核心子系统

### Ch29 双轨制文档体系
- Canonical vs Human View、八规则、文件角色分类

### Ch30 Canonical YAML 格式规范
- proposal/spec/agent_spec schema、DC-HASH/DC-FIELD

### Ch31 Human View 生成规则
- YAML→MD 渲染、canon generate

### Ch32 经验库系统
- 5 态 FSM、来源权重、自动记录/加载

### Ch33 社区经验共享
- GitHub+Gitee 设计、export/pull/curate

### Ch34 代码结构摘要
- delta/merge/rebuild、structure CLI

### Ch35 Skill 生态系统
- 6 Phase Skill + _shared/、skill create、平台同步

---

## Part 7: CLI 完整参考

### Ch36 CLI 总览 — 28 命令总表
### Ch37 项目生命周期：init / install / upgrade
### Ch38 变更管理：new / validate / status / archive / rollback / abort / diff
### Ch39 追溯与状态：trace / state / gate / extract-proposal
### Ch40 经验库：experience list/add/stats/export/pull/verify/deposit/retire/curate
### Ch41 双轨制：proposal / canon
### Ch42 工程化：index / agent / hooks / structure / skill
### Ch43 质量与版本：fix / ci / batch / guard
### Ch44 依赖图：dependency-graph

---

## Part 8: 配置系统

### Ch45 配置总览
### Ch46 project.yaml
### Ch47 gates.yaml
### Ch48 long_range.yaml
### Ch49 quality.yaml
### Ch50 experience.yaml
### Ch51 lite.yaml
### Ch52 version.yaml + 全局注册表

---

## Part 9: 平台与规范

### Ch53 平台适配架构
### Ch54 七大平台适配（Claude Code / WorkBuddy / Trae / Cursor / Windsurf / Copilot / OpenCode）
### Ch55 开发规范体系（5 语言标准 + Rules）
### Ch56 模板系统（13 模板 + 约束规则）

---

## Part 10: 版本演进

### Ch57 V1.0→V2.9 完整演进（13 版本）
### Ch58 V2.9 vs 同类工具（13 维度对比）
### Ch59 V3 展望

---

## Part 11: 附录

### AppA 完整目录结构参考
### AppB CLI 命令速查表
### AppC 常见问题 FAQ（30 条）
### AppD .stdd.yaml 完整字段参考
