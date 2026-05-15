# V2.3 测试方案与详细案例

> 版本：V2.3
> 创建日期：2026-05-15
> 对应 Phase 2 Spec：multi-lang-standards, platform-sync, platform-cursor, platform-copilot, platform-aider, config-system, skill-architecture

## 一、测试策略

### 1.1 测试金字塔

本次为文档/配置变更，无 Python 代码改动。测试以 **静态验证** 为主（Grep 内容检查 + 文件存在性验证），辅以 YAML 语法校验。

- 静态验证：17 个 Grep/文件检查案例
- YAML 语法校验：1 个配置解析案例
- 结构一致性：对比验证案例

### 1.2 测试原则

- 每个 Spec Scenario 至少映射 1 个 TC 案例
- TC 验证方法必须是可自动化的（Grep / Bash / Read）
- 文件存在性检查覆盖所有新建文件
- 内容特征检查覆盖所有关键 V2.2 特征

### 1.3 已有测试资产

| 测试文件 | 用例数 | 类型 | 覆盖范围 |
|----------|--------|------|----------|
| 无 | 0 | — | 本次为纯文档变更，无可复用测试资产 |

## 二、详细测试案例

### 功能 1：multi-lang-standards（多语言规范）

对应 Spec：`specs/multi-lang-standards/spec.md`

#### 案例 1.1 — Java 规范文件存在且结构完整

| 字段 | 内容 |
|------|------|
| **ID** | TC-MLANG-001 |
| **对应 Spec** | multi-lang-standards/spec.md → Scenario: Java 规范文件存在且结构完整 |
| **优先级** | P0 |
| **预置条件** | `.stdd/standards/` 目录存在 |
| **输入** | `Read(.stdd/standards/java.md)` |
| **预期结果** | 文件存在且包含 6 个章节标题：代码风格、类型系统、并发模型、错误处理、测试规范、审查清单 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.2 — Go 规范文件存在且结构完整

| 字段 | 内容 |
|------|------|
| **ID** | TC-MLANG-002 |
| **对应 Spec** | multi-lang-standards/spec.md → Scenario: Go 规范文件存在且结构完整 |
| **优先级** | P0 |
| **预置条件** | `.stdd/standards/` 目录存在 |
| **输入** | `Read(.stdd/standards/go.md)` |
| **预期结果** | 文件存在且包含 6 个章节标题：代码风格、类型系统、并发模型、错误处理、测试规范、审查清单 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.3 — Rust 规范文件存在且结构完整

| 字段 | 内容 |
|------|------|
| **ID** | TC-MLANG-003 |
| **对应 Spec** | multi-lang-standards/spec.md → Scenario: Rust 规范文件存在且结构完整 |
| **优先级** | P0 |
| **预置条件** | `.stdd/standards/` 目录存在 |
| **输入** | `Read(.stdd/standards/rust.md)` |
| **预期结果** | 文件存在且包含 6 个章节标题：代码风格、类型系统、并发模型、错误处理、测试规范、审查清单 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.4 — TypeScript 规范文件存在且结构完整

| 字段 | 内容 |
|------|------|
| **ID** | TC-MLANG-004 |
| **对应 Spec** | multi-lang-standards/spec.md → Scenario: TypeScript 规范文件存在且结构完整 |
| **优先级** | P0 |
| **预置条件** | `.stdd/standards/` 目录存在 |
| **输入** | `Read(.stdd/standards/typescript.md)` |
| **预期结果** | 文件存在且包含 6 个章节标题：代码风格、类型系统、异步模型、错误处理、测试规范、审查清单 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.5 — 四种规范与 Python 规范结构一致

| 字段 | 内容 |
|------|------|
| **ID** | TC-MLANG-005 |
| **对应 Spec** | multi-lang-standards/spec.md → Scenario: 四种规范共享相同的章节结构模板 |
| **优先级** | P0 |
| **预置条件** | 4 个新建规范文件和 python.md 均存在 |
| **输入** | Grep 搜索各文件中的章节标题（`## 一、` `## 二、` 等），对比标题文本 |
| **预期结果** | 5 个文件（python/java/go/rust/typescript）的顶级章节标题一一对应（共 7 章：代码风格/类型系统/异步或并发/错误处理/日志/测试/审查清单） |
| **当前状态** | ❌ 测试缺 |

---

### 功能 2：platform-sync（平台同步）

对应 Spec：`specs/platform-sync/spec.md`

#### 案例 2.1 — workbuddy 6 文件 V2.2 特征计数达标

| 字段 | 内容 |
|------|------|
| **ID** | TC-SYNC-001 |
| **对应 Spec** | platform-sync/spec.md → Scenario: workbuddy skill 文件内容等同 claude-code gold source |
| **优先级** | P0 |
| **预置条件** | workbuddy 6 个文件已同步 |
| **输入** | 对 workbuddy 的 verify.md/build.md/spec.md 三个核心文件执行 Grep，搜索 11 个 V2.2 关键特征关键词 |
| **预期结果** | 每个文件的关键特征计数 ≥ claude-code 对应文件计数的 90%（允许 frontmatter 差异） |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.2 — trae 6 文件 V2.2 特征计数达标

| 字段 | 内容 |
|------|------|
| **ID** | TC-SYNC-002 |
| **对应 Spec** | platform-sync/spec.md → Scenario: trae skill 文件内容等同 claude-code gold source |
| **优先级** | P0 |
| **预置条件** | trae 6 个文件已同步 |
| **输入** | 对 trae 的 verify.md/build.md/spec.md 三个核心文件执行 Grep，搜索 11 个 V2.2 关键特征关键词 |
| **预期结果** | 每个文件的关键特征计数 ≥ claude-code 对应文件计数的 90% |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.3 — 三平台特征计数一致

| 字段 | 内容 |
|------|------|
| **ID** | TC-SYNC-003 |
| **对应 Spec** | platform-sync/spec.md → Scenario: 三平台特征计数一致性 |
| **优先级** | P0 |
| **预置条件** | 三个平台均已同步到 V2.2 |
| **输入** | 对 claude-code / workbuddy / trae 的 verify.md 分别执行 11 个关键特征 Grep |
| **预期结果** | 每个特征在三个平台中的命中次数一致（误差 ±1） |
| **当前状态** | ❌ 测试缺 |

---

### 功能 3：platform-cursor（Cursor 适配）

对应 Spec：`specs/platform-cursor/spec.md`

#### 案例 3.1 — Cursor 规则文件存在且包含 STDD 6 阶段

| 字段 | 内容 |
|------|------|
| **ID** | TC-CURSOR-001 |
| **对应 Spec** | platform-cursor/spec.md → Scenario: Cursor 规则文件存在且内容完整 |
| **优先级** | P1 |
| **预置条件** | `.stdd/platforms/cursor/` 目录存在 |
| **输入** | `Read(.stdd/platforms/cursor/rules/stdd.md)` |
| **预期结果** | 文件包含所有 6 个阶段名称（Understand/Spec/Slice/Build/Verify/Deliver）和 3 个 Gate 说明 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 4：platform-copilot（Copilot 适配）

对应 Spec：`specs/platform-copilot/spec.md`

#### 案例 4.1 — Copilot 指令文件存在且含测试优先原则

| 字段 | 内容 |
|------|------|
| **ID** | TC-COPILOT-001 |
| **对应 Spec** | platform-copilot/spec.md → Scenario: Copilot 指令文件存在且内容完整 |
| **优先级** | P1 |
| **预置条件** | `.stdd/platforms/copilot/` 目录存在 |
| **输入** | `Read(.stdd/platforms/copilot/copilot-instructions.md)` |
| **预期结果** | 文件包含 "test-first" 或 "RED→GREEN→REFACTOR" 关键词、`.stdd/standards/` 引用 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 5：platform-aider（Aider 适配）

对应 Spec：`specs/platform-aider/spec.md`

#### 案例 5.1 — Aider 约定文件和配置存在

| 字段 | 内容 |
|------|------|
| **ID** | TC-AIDER-001 |
| **对应 Spec** | platform-aider/spec.md → Scenario: Aider 约定文件存在且内容完整 |
| **优先级** | P1 |
| **预置条件** | `.stdd/platforms/aider/` 目录存在 |
| **输入** | 检查 `CONVENTIONS.md` 和 `.aider.conf.yml` 是否存在 |
| **预期结果** | 两个文件均存在，`CONVENTIONS.md` 包含编码规范引用，`.aider.conf.yml` 包含 `read` 字段 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 6：config-system（配置补完）

对应 Spec：`specs/config-system/spec.md`

#### 案例 6.1 — typecheck 非 null

| 字段 | 内容 |
|------|------|
| **ID** | TC-CONFIG-001 |
| **对应 Spec** | config-system/spec.md → Scenario: typecheck 配置为非 null 值 |
| **优先级** | P0 |
| **预置条件** | `.stdd/config.d/quality.yaml` 已修改 |
| **输入** | `Grep(typecheck: mypy)` 或 `Read` quality.yaml |
| **预期结果** | `typecheck` 值为字符串（非 null），如 `"mypy app/"` |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.2 — critical_paths 非空数组

| 字段 | 内容 |
|------|------|
| **ID** | TC-CONFIG-002 |
| **对应 Spec** | config-system/spec.md → Scenario: critical_paths 为非空数组 |
| **优先级** | P0 |
| **预置条件** | `.stdd/config.d/quality.yaml` 已修改 |
| **输入** | `Grep(critical_paths)` quality.yaml |
| **预期结果** | `critical_paths` 至少包含 1 个路径元素 |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.3 — source_dir 字段存在

| 字段 | 内容 |
|------|------|
| **ID** | TC-CONFIG-003 |
| **对应 Spec** | config-system/spec.md → Scenario: source_dir 字段存在 |
| **优先级** | P0 |
| **预置条件** | `.stdd/config.d/project.yaml` 已修改 |
| **输入** | `Grep(source_dir)` project.yaml |
| **预期结果** | `source_dir` 字段存在且为非空字符串 |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.4 — long_range.yaml 含 degradation 配置

| 字段 | 内容 |
|------|------|
| **ID** | TC-CONFIG-004 |
| **对应 Spec** | config-system/spec.md → Scenario: degradation 配置段存在且完整 |
| **优先级** | P0 |
| **预置条件** | `.stdd/config.d/long_range.yaml` 已修改 |
| **输入** | `Grep(degradation)` long_range.yaml |
| **预期结果** | `degradation` 段存在，包含 `max_consecutive_failures`、`pass_rate_threshold`、`safety_check` 三个字段 |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.5 — YAML 语法正确

| 字段 | 内容 |
|------|------|
| **ID** | TC-CONFIG-005 |
| **对应 Spec** | config-system/spec.md → 补充：配置文件的 YAML 语法有效性 |
| **优先级** | P0 |
| **预置条件** | 所有配置文件已修改 |
| **输入** | `python -c "import yaml; yaml.safe_load(open('.stdd/config.d/quality.yaml'))"` 等 |
| **预期结果** | 三个修改的 YAML 文件均解析成功，无 YAML 语法错误 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 7：skill-architecture（Skill 标准化）

对应 Spec：`specs/skill-architecture/spec.md`

#### 案例 7.1 — 全部 6 个 master skill 文件含 frontmatter

| 字段 | 内容 |
|------|------|
| **ID** | TC-SKILL-001 |
| **对应 Spec** | skill-architecture/spec.md → Scenario: 所有 master skill 文件含 frontmatter |
| **优先级** | P0 |
| **预置条件** | `.stdd/skills/` 下 6 个文件已修改 |
| **输入** | 对每个文件 `Read` 前 5 行，检查是否以 `---` 开头 |
| **预期结果** | 6 个文件均以 YAML frontmatter（`---`）开头，且含 `name:` 和 `description:` 字段 |
| **当前状态** | ❌ 测试缺 |

#### 案例 7.2 — frontmatter name 与 claude-code 平台一致

| 字段 | 内容 |
|------|------|
| **ID** | TC-SKILL-002 |
| **对应 Spec** | skill-architecture/spec.md → Scenario: frontmatter 格式与 claude-code 平台一致 |
| **优先级** | P0 |
| **预置条件** | master 和 claude-code 文件均已更新 |
| **输入** | 对比 `.stdd/skills/` 和 `.stdd/platforms/claude-code/skills/` 同名文件的 `name` 和 `description` 字段 |
| **预期结果** | 6 对文件的 `name` 完全一致，`description` 完全一致 |
| **当前状态** | ❌ 测试缺 |

#### 案例 7.3 — master→platform 同步一致性可验证

| 字段 | 内容 |
|------|------|
| **ID** | TC-SKILL-003 |
| **对应 Spec** | skill-architecture/spec.md → Scenario: 一致性可验证 |
| **优先级** | P1 |
| **预置条件** | 所有文件已同步 |
| **输入** | Grep 在 master 和 platform 的 verify.md 中搜索 `Step 0`、`十一类`、`强制步骤清单`，对比计数 |
| **预期结果** | 关键特征在 master、claude-code、workbuddy、trae 四个位置的 verify.md 中计数一致（误差 ±1） |
| **当前状态** | ❌ 测试缺 |

## 三、测试执行矩阵

| 功能模块 | 文件存在验证 | 内容特征验证 | 结构一致性 | 状态 |
|----------|-------------|-------------|-----------|------|
| multi-lang-standards | TC-MLANG-001~004 | TC-MLANG-001~004 | TC-MLANG-005 | 🔴 全部缺失 |
| platform-sync | — | TC-SYNC-001~002 | TC-SYNC-003 | 🔴 全部缺失 |
| platform-cursor | TC-CURSOR-001 | TC-CURSOR-001 | — | 🔴 全部缺失 |
| platform-copilot | TC-COPILOT-001 | TC-COPILOT-001 | — | 🔴 全部缺失 |
| platform-aider | TC-AIDER-001 | TC-AIDER-001 | — | 🔴 全部缺失 |
| config-system | TC-CONFIG-001~003 | TC-CONFIG-001~004 | TC-CONFIG-005 | 🔴 全部缺失 |
| skill-architecture | TC-SKILL-001 | TC-SKILL-001~002 | TC-SKILL-003 | 🔴 全部缺失 |

## 四、回归风险矩阵

| 风险区域 | V2.3 改动 | 已有回归保护 | 风险等级 |
|----------|-------------|-------------|---------|
| 语言规范 | 新增 4 个 standards 文件 | 无（纯新增） | 🟢 低 |
| workbuddy 平台 | 6 文件全量覆写 | V2.2 test-report TC-SYNC 系列可复用 | 🟡 中（注意保留 frontmatter） |
| trae 平台 | 6 文件全量覆写 | V2.2 test-report TC-SYNC 系列可复用 | 🟡 中（注意 trae 无 frontmatter 历史） |
| 新平台 (cursor/copilot/aider) | 新增 3 个目录 | 无（纯新增） | 🟢 低 |
| 配置 | 3 个 YAML 文件修改 | YAML 语法校验 TC-CONFIG-005 | 🟢 低（增量添加） |
| Master Skill | 6 文件加 frontmatter | V2.2 test-report TC-VERIFY 系列可复用 | 🟢 低（仅加头部） |
| claude-code 平台 skill | 不修改 | V2.2 已验证 | 🟢 低 |

## 五、建议补充顺序

1. **第一步**（部署前必补 P0）：TC-MLANG-001~005（5个）、TC-SYNC-001~003（3个）、TC-CONFIG-001~005（5个）、TC-SKILL-001~002（2个）共 15 个
2. **第二步**（部署后尽快补 P1）：TC-CURSOR-001、TC-COPILOT-001、TC-AIDER-001、TC-SKILL-003 共 4 个
3. **第三优先**（后续补 P2）：无 — 所有 Scenario 均已覆盖 TC 案例
