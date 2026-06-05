# Spec: non-code-change-support — 非代码类 Change 支持

> Capability: non-code-change-support
> Priority: P1 · 0.7d · Skill + 数据模型

## Requirement: verify.md 非代码检查清单

当 change 不包含代码文件时，`verify.md` SHALL 使用替代检查维度。

### Scenario: 检测非代码 change

GIVEN change 目录仅包含 `.html`, `.css`, `.js`, `.md` 文件
AND 不包含 `.py`, `.go`, `.java`, `.rs`, `.ts` 文件
WHEN Phase 5 VERIFY 开始
THEN AI SHALL 切换到"非代码类替代检查清单"

### Scenario: 替代检查 — 链接有效性

GIVEN 非代码 change 包含对外部资源的引用（CDN、图片 URL、href 链接）
WHEN AI 执行替代检查 (a) 幻觉行为
THEN AI SHALL 逐个验证所有外部引用链接是否可达（HEAD request 或 URL 格式检查）
AND 不可达的链接 SHALL 标记为潜在问题

### Scenario: 替代检查 — 文件范围一致性

GIVEN proposal.md 声明了变更范围
AND `git diff --stat` 显示实际变更的文件列表
WHEN AI 执行替代检查 (b) 范围蔓延
THEN AI SHALL 对比两者的文件数量
AND 若 `git diff` 显示的文件数远超 proposal 声明，SHALL 标记为范围蔓延

### Scenario: 替代检查 — 内部引用可达性

GIVEN change 包含 HTML 页面，其中有 `<a href="../shared/stepper.js">`
WHEN AI 执行替代检查 (g) 管线断链
THEN AI SHALL 检查所有内部 `<a href>` / `<link href>` / `<script src>` 引用是否指向存在的文件
AND 断链 SHALL 标记为错误

### Scenario: 替代检查 — 内容完整性

GIVEN test-plan.md 定义了 18 个 TC
WHEN AI 执行替代检查 (h) 内容质量偏差
THEN AI SHALL 逐项对照 spec 和 test-plan，确认每个 TC 有对应的验证记录
AND 缺失验证记录的 TC SHALL 标记为覆盖缺口

### Scenario: 替代检查 — TC 目视验证覆盖

GIVEN test-plan.md 定义了 TC-SHARED-001 ~ TC-SHARED-005
WHEN AI 执行替代检查 (j) 覆盖真空
THEN AI SHALL 确认 test-report.md 中每个 TC 都有对应的 PASS/FAIL 记录
AND 无验证记录的 TC SHALL 标记为覆盖真空

### Scenario: 代码 change 仍使用原有检查

GIVEN change 包含 `.py` 文件
WHEN Phase 5 VERIFY 开始
THEN AI SHALL 使用现有 11 类失败模式检查
AND 替代检查清单不被加载

## Requirement: 经验 project_type 标签

经验条目 SHALL 包含 `project_type` 字段，用于加载时过滤。

### Scenario: 经验自动标记 project_type

GIVEN change 的文件分布为 `*.py: 80%, *.md: 20%`
WHEN Phase 5 VERIFY 创建经验条目
THEN 经验的 `project_type` SHALL 自动设为 `python`

### Scenario: 混合项目标记为多类型

GIVEN change 的文件分布为 `*.html: 40%, *.css: 30%, *.js: 30%`
WHEN Phase 5 VERIFY 创建经验条目
THEN 经验的 `project_type` SHALL 设为 `static_site`

### Scenario: 纯文档项目

GIVEN change 仅包含 `.md` 文件
WHEN Phase 5 VERIFY 创建经验条目
THEN 经验的 `project_type` SHALL 设为 `docs`

### Scenario: 经验加载时按 project_type 过滤

GIVEN 当前 change 的 `project_type: static_site`
AND 经验库中有 `project_type: python` 的经验 EXP-0001 和 `project_type: static_site` 的经验 EXP-0042
WHEN Phase 4 BUILD Step 0.5 加载匹配经验
THEN EXP-0042（static_site）SHALL 被加载
AND EXP-0001（python）SHALL 被跳过
AND AI SHALL 被告知"已加载 1 条匹配经验（static_site），过滤 1 条不匹配"

### Scenario: project_type 向后兼容

GIVEN 一条 V2.4 格式的经验（无 `project_type` 字段）
WHEN AI 加载经验
THEN 该经验 SHALL 被加载（`project_type: null` 视为通配，匹配所有类型）
AND 不影响现有功能
