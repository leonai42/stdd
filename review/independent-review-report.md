# STDD 独立评审报告

> 评审日期：2026-05-14
> 评审人：Claude Code (独立评审)
> 评审对象：STDD V1.2 全量代码、架构、文档
> 评审范围：`bin/stdd` (635行)、6个核心Skill、9个模板、1个开发规范、4份项目文档、3套平台适配

---

## 执行摘要

**总体评价：⭐⭐⭐⭐ (4/5) — 设计优秀，实现有改善空间**

STDD 是一套从实战中提炼的高质量研发流程系统。其核心理念（Spec先行 + TDD + 强制确认门 + 失败模式检查）设计成熟，具有明确的工程价值。主要短板集中在 CLI 代码质量、模板体系一致性、以及部分边界条件处理上。

---

## 一、架构评审

### 1.1 整体架构

```
┌─────────────────────────────────────────┐
│              STDD System                 │
│                                          │
│  Skill Layer (流程控制)                   │
│  ├─ 6 Phase Skills (Markdown)            │
│  └─ 平台适配层 (Claude/WorkBuddy/Trae)    │
│                                          │
│  CLI Layer (结构化操作)                    │
│  └─ bin/stdd (Python 635行)              │
│                                          │
│  Artifact Layer (产物管理)                 │
│  └─ changes/ specs/ archive/ .stdd.yaml  │
└─────────────────────────────────────────┘
```

**评分：8/10**

**亮点**：
- **分层清晰**：Skill层负责"怎么想"（流程决策），CLI层负责"做什么"（文件操作），职责分离合理
- **跨平台抽象**：核心Skill保持平台无关，通过平台适配层对接不同AI平台，设计优雅
- **混合模式合理**：Markdown Skill（AI可读可执行）+ Python CLI（精确操作），互补性强

**问题**：

1. **Skill-CLI 桥接缺失**：Skill 描述"使用 stdd validate 验证"，但没有机制确认 CLI 是否可用、是否成功执行。Skill 和 CLI 之间的契约是隐式的。

2. **配置膨胀风险**：`config.yaml` 已 103 行，`long_range` 配置段尤其复杂（58行），随着功能增加会持续膨胀，建议拆分为独立配置文件。

3. **无插件/扩展机制**：新增平台、语言规范、失败模式都需要修改核心代码。虽然目前规模合适，但设计文档中未说明扩展点。

### 1.2 六阶段流程设计

**评分：9/10**

六阶段流程（UNDERSTAND → SPEC → SLICE → BUILD → VERIFY → DELIVER）逻辑严密，阶段边界清晰。三道强制确认门的位置选择合理——分别在范围确认（P1）、设计确认（P2）、交付确认（P5）三个最关键节点。

**细微问题**：
- Phase 3 (SLICE) 被设计为"自动执行无需确认"，但切片方案的质量直接影响后续 Phase 4-5 的效率。如果 AI 切片不合理，问题要到 Phase 4 甚至 Phase 5 才暴露。
- Phase 6 (DELIVER) 的 Step 2 "合并规范"逻辑过于简单，实际合并冲突场景（多人并行修改同一 capability）未覆盖。

### 1.3 长程模式设计

**评分：9/10**

长程模式是 STDD 最具创新性的设计。一次性预授权模型解决了一个真实痛点：AI 辅助开发中频繁的权限确认打断。

**问题**：
- 预授权模板（`long-range-auth.md`）79 行，conig 中 58 行，总共 137 行配置——对用户认知负担大
- 降级条件中"通过率 < 95%"是硬编码阈值，不可配置
- 缺少"长程模式中途退出"机制：用户如果想在 Phase 4 中途切回普通模式，没有标准路径

---

## 二、代码评审（bin/stdd）

### 2.1 代码结构

**评分：6/10**

| 维度 | 评分 | 说明 |
|------|------|------|
| 可读性 | 7/10 | 单文件结构清晰，但 635 行偏长 |
| 健壮性 | 5/10 | 缺少异常处理、无输入校验 |
| 可测试性 | 3/10 | 零测试，函数紧耦合 |
| 一致性 | 5/10 | 未遵循自身 Python 规范 |
| 安全性 | 7/10 | 无命令注入风险，无敏感操作 |

### 2.2 具体问题

#### 严重问题

**P0-1: `archive` 目录名 Bug**（第 368 行）

```python
archive_dir = project_root / "archive" / args.name  # ❌
# 应为：
archive_dir = project_root / "archive" / change_dir.name  # ✅
```

**P0-2: `archive` 操作非原子性**（第 374-404 行）

```python
shutil.move(str(change_dir), str(archive_dir))  # 步骤1：移动目录
# ... 合并 specs ...
# 如果步骤2失败，change_dir 已不在原位置，状态不一致
```

目录先移动后处理，若 specs 合并或状态更新失败，数据已迁移但状态损坏。建议：先合并 specs，状态更新，最后移动目录。

**P0-3: `.stdd.yaml` 无版本字段**

`cmd_new` 第 149-163 行生成的 `.stdd.yaml` 无版本号。当前格式的任何变更都会破坏已有 change 的兼容性。

#### 中等问题

**P1-1: 自身规范违反**（多个位置）

CLI 脚本未遵循自身 `.stdd/standards/python.md`：

| 规范要求 | 实际状况 |
|----------|----------|
| 公共函数必须完整类型注解 | 无任何类型注解 |
| 使用结构化日志 | 全部用 `print()` |
| Import 顺序：标准库→第三方→本地 | Import 分散在函数内外 |
| 行宽：100 字符 | 部分行超过 |
| 文件末尾一个空行 | 符合 |

**P1-2: stdout 重绑是 hack**（第 21-22 行）

```python
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
```

只处理了 stdout，未处理 stderr。且直接替换全局 stdout 可能影响其他模块。更好的做法是在输出时显式处理编码，或使用 `PYTHONIOENCODING=utf-8` 环境变量。

**P1-3: `_find_change_dir` 的匹配逻辑隐晦**（第 25-49 行）

- 无 `name` 参数时，按 mtime 返回"最近的 change"——用户可能不知道哪个被选中
- 模糊匹配使用 `d.name.endswith(name)`，如果用户输入 `fix` 会匹配到所有含 `fix` 的目录

**P1-4: `trace` 正则过于复杂且脆弱**（第 438-443 行）

```python
block_pattern = re.compile(
    rf'####\s+案例\s+[\d.]+\s*—\s*(.+?)\n'
    rf'.*?\*\*ID\*\*\s*\|\s*{re.escape(tc_id)}.*?'
    rf'\*\*预期结果\*\*\s*\|\s*(.+?)(?:\n|$)',
    re.DOTALL
)
```

跨行正则+mised with `re.DOTALL` 可能匹配到不相关的内容。test-plan.md 格式的任何变化都会破坏此正则。

**P1-5: `validate` 只检查 .md spec 文件**（第 209-210 行）

```python
for spec_file in specs_dir.rglob("*.md"):
```

如果 specs 目录下存在非 spec 的 .md 文件（如 README.md），也会被纳入验证，产生误报。

**P1-6: `archive` 的 specs 合并逻辑可能产生重复**（第 385-393 行）

```python
merge_note = f"\n\n<!-- 合并自 {args.name} -->\n"
combined = existing + merge_note + new_content
```

多次归档同一 capability 的变更时，spec 文件会不断追加内容（包括之前的合并注释），产生累积膨胀。

#### 低优先级问题

**P2-1**: `install` 的 `source_dir.iterdir()` 源不存在时静默无输出（无错误提示）
**P2-2**: `init` 复制文件列表硬编码（第 76-95 行），新增模板需要同步修改代码
**P2-3**: 无法处理的 YAML 异常会被 argparse 默认处理，错误信息不友好
**P2-4**: `trace` 未找到时的错误信息提示不够有帮助
**P2-5**: 缺少 `--dry-run` 全局选项

---

## 三、模板系统评审

### 3.1 整体评估

**评分：6/10**

模板采用"先读后写、章节不可增删、字段不可省略、命名不可变"的四大约束规则，保证了一致性。但模板质量严重不均。

### 3.2 逐模板分析

| 模板 | 行数 | 质量 | 问题 |
|------|------|------|------|
| proposal.md | 37 | ⭐⭐⭐ | 缺乏"假设与约束"章节；Success Criteria 无量化示例 |
| design.md | 32 | ⭐⭐⭐ | 缺"回滚方案"；风险表只有2列过于简略 |
| spec.md | 15 | ⭐⭐ | **极简问题**：无多Scenario示例、无AND用法示例、无边界场景模板 |
| test-plan.md | 59 | ⭐⭐⭐⭐ | 结构完整，但缺"测试数据准备"章节 |
| tasks.md | 12 | ⭐⭐ | **极简问题**：无优先级标注示例、无依赖关系示例 |
| slices.md | 7 | ⭐⭐ | 仅表格模板，缺说明文字、缺工时估算 |
| design-adjustments.md | 27 | ⭐⭐⭐ | 结构合理，"影响范围"字段已包含 |
| test-report.md | 100 | ⭐⭐⭐⭐ | 最详细，但部分表格列过于细分 |
| long-range-auth.md | 79 | ⭐⭐⭐⭐ | 设计完整，但内容更像"表单"而非"模板" |

### 3.3 核心问题

**模板极简主义 vs AI 理解能力**：`spec.md`（15行）和 `tasks.md`（12行）几乎只提供了骨架。虽然 AI 模型通常能自行填充，但模板的首要目的是**约束和引导**，过于简略的模板起不到约束作用。

**建议**：在不破坏简洁性的前提下，每个模板增加 1-2 个内嵌示例（用注释形式，不影响最终文档结构）。

---

## 四、Skill 系统评审

### 4.1 整体评估

**评分：8/10**

六个核心Skill的设计质量很高，阶段目标明确、前置条件清晰、执行流程详细、产出物和质量检查清单完整。

### 4.2 亮点

- **Phase 2 (SPEC) 是真正的核心**，Skill 明确标注"最重要的阶段"并提供了详尽的执行步骤
- **Phase 5 (VERIFY) 的十一类失败模式**每个都有检查方法和典型信号，可操作性强
- **确认消息模板标准化**，Phase 1/2/5 的确认消息格式一致，用户体验统一
- **长程模式集成**，在 Phase 2 Step 7 自然衔接，不增加额外命令

### 4.3 问题

1. **Skill 文件中的命令引用不一致**：核心 Skill 说"运行 pytest"，但未说明是直接执行还是通过 CLI。不同平台的行为可能不同。

2. **缺少 /stdd-abort 或 /stdd-cancel 命令**：如果用户想放弃当前变更，没有标准路径。

3. **/stdd-continue 语义过载**：它同时处理 Phase 3-6 的继续执行，但不同阶段的恢复逻辑完全不同。

4. **Skill 文件存在大量重复内容**：每个 Skill 都独立包含确认消息模板、模式选择说明等，维护时需同步修改多份。

---

## 五、文档评审

### 5.1 整体评估

**评分：7/10**

项目有四份核心文档（README、STDD.md、DESIGN.md、DEPLOY.md）加 AGENTS.md。文档量充足，双语支持到位。

### 5.2 问题

**P1: 版本号不一致**

| 文件 | 版本声明 |
|------|----------|
| README.md | V1.2 |
| DESIGN.md | V1.2 (2026-05-09) |
| DEPLOY.md | V1.2 |
| config.yaml | `stdd_version: "1.0.0"` |

config.yaml 中的版本号停留在 V1.0，与其他文档矛盾。

**P1: 文档重复严重**

STDD.md（123行）与 README.md（149行）大量重复：
- 六阶段流程在两个文件中都有完整描述
- 目录结构、CLI命令列表、支持的平台列表都重复

DESIGN.md（592行）是最权威的信息源，但 README 和 STDD.md 各自维护了一份简化版，增加了维护负担。

**P2: 缺少关键文档**

- 无 CHANGELOG.md：版本历史埋在 DESIGN.md 附录中
- 无 CONTRIBUTING.md：没有说明如何贡献、Skill 编写规范
- 无架构决策记录（ADR）：重大设计决策（如为何选择 Python 而非 Shell 写 CLI）未记录
- 无故障排除指南：常见问题（如 Unicode 错误）只在 DEPLOY.md FAQ 中有简单提及

**P2: DESIGN.md 过于庞大**

592 行的单一设计文档难以导航。建议拆分为：
- `DESIGN.md` — 架构概述（保持 100 行以内）
- `docs/failure-modes.md` — 十一类失败模式详解
- `docs/long-range-mode.md` — 长程模式设计
- `docs/platform-adapters.md` — 平台适配设计

---

## 六、跨平台适配评审

**评分：7/10**

### 现状

三套平台 Skill（claude-code、workbuddy、trae）内容几乎相同，仅 frontmatter 不同：

```yaml
# Claude Code 版本
---
name: stdd-build
description: "..."
---

# WorkBuddy 版本
---
name: stdd-build
description: "..."
version: "1.0"
trigger_keywords: ["stdd-build", "stdd build", "spec-driven", "tdd"]
---
```

### 问题

1. **维护负担**：18 个平台 Skill 文件（3平台 × 6阶段）需要与核心 Skill 保持同步。当前已是手动复制。

2. **平台适配逻辑分散**：部分在 `install` 命令中（Claude Code 用 `SKILL.md` 子目录格式），部分在模板中，部分在 config 中。

3. **Trae 平台适配未经充分验证**：`install` 对 Trae 的处理与 Claude Code 完全相同（都是 `target_base / skill_file.name`），但 Trae 的实际 Skill 加载机制可能与 Claude Code 不同。

---

## 七、开发规范评审

### Python 规范（`standards/python.md`）

**评分：8/10**

146 行的 Python 规范覆盖了格式化、命名、类型注解、异步、错误处理、日志、测试、审查清单，内容扎实。

**问题**：

1. **CLI 自身未遵循**（如前所述）
2. **规范中的"强制要求"不可自动校验**：如"所有公共函数必须有完整类型注解"，但没有 mypy 配置来强制执行
3. **规范引用了 ruff、mypy 等工具，但未提供对应的配置文件模板**

---

## 八、综合风险评估

| 风险 | 严重度 | 可能性 | 缓解建议 |
|------|--------|--------|----------|
| CLI Bug 导致数据丢失（archive） | 高 | 中 | 立即修复 Bug1，增加原子性保护 |
| .stdd.yaml 兼容性断裂 | 中 | 中 | 增加 version 字段和迁移框架 |
| 平台 Skill 与核心不同步 | 中 | 高 | 建立自动同步机制或单一来源 |
| 用户学习曲线过陡 | 中 | 中 | 增加示例项目和快速入门教程 |
| AI 对极简模板的填充偏差 | 低 | 高 | 模板增加内嵌示例 |
| 零 CLI 测试导致回归 | 中 | 中 | 增加 CLI 单元测试 |

---

## 九、改进路线图建议

### 短期（V1.2.1，1-2天）

1. 修复 archive 目录名 Bug
2. .stdd.yaml 增加 version 字段
3. 修复 validate 正则逻辑（统一改为 `<`）
4. 修复 trace 增加 specs/ 搜索
5. 统一版本号（config.yaml 改为 1.2.0）

### 中期（V1.3，1周）

1. CLI 代码质量提升（类型注解、异常处理、日志）
2. 增加 init --force、new 格式验证、install 存在性检查
3. 优化极简模板（spec.md、tasks.md）
4. 增加 /stdd-abort 命令
5. 文档去重和拆分

### 长期（V2.0）

1. CLI 重构为模块化结构
2. 增加 CLI 单元测试
3. 技能自动同步机制（核心→平台）
4. 插件化扩展架构
5. 示例项目和完整教程

---

## 十、结论

STDD 是一套**设计优秀、理念成熟**的研发流程系统。其从 FPPT 实战中提炼的经验（十一类失败模式、长程模式预授权）具有独特的工程价值，这是它区别于其他研发流程工具的核心竞争力。

主要短板在**工程质量**层面：CLI 代码缺乏测试和错误处理、模板质量不均、文档冗余。这些问题不影响系统的核心价值，但会限制其作为独立产品的可靠性和可维护性。

**总评：可推荐使用，建议按短期计划修复关键 Bug 后正式发布。**
