# V2.9.4 → V2.10 测试方案与详细案例

> 版本：V2.10
> 创建日期：2026-07-01
> 对应 Phase 2 Spec：platform-codex, lang-javascript, lang-c, lang-kotlin, lang-swift, lang-dart, platform-sync

## 一、测试策略

### 1.1 测试金字塔

本变更属于 **文档+配置类** 变更（新建语言规范 + 平台适配 + 代码修改），测试重点：

- **单元测试（70%）**：install.py platform_map 扩展、frontmatter 生成逻辑、文件存在性检查
- **集成测试（20%）**：`stdd install codex` 端到端流程、语言规范加载验证
- **E2E（10%）**：Codex CLI 实际加载 STDD skill（需 Codex CLI 环境，标记为 P2）

### 1.2 测试原则

- 平台适配测试复用现有 `test_install.py` 的测试模式（参考 OpenCode 测试案例）
- 语言规范测试验证文件存在性 + 结构完整性（7 章 + 审查清单 checkbox）
- 文档一致性测试使用 grep/ripgrep 做跨文件交叉验证
- 新增平台不破坏现有 5 个平台的安装逻辑（回归测试）

### 1.3 已有测试资产

| 测试文件 | 用例数 | 类型 | 覆盖范围 |
|----------|--------|------|----------|
| `tests/commands/test_install.py` | ~15 | 单元 | install.py 所有平台安装逻辑 |
| `tests/commands/test_init.py` | ~8 | 单元 | 项目初始化 |
| `tests/test_cli.py` | ~10 | 集成 | CLI 入口调度 |

## 二、详细测试案例

### 功能 1：platform-codex — stdd install codex

对应 spec: `platform-codex/spec.md`

#### 案例 1.1 — platform_map 注册 codex

| 字段 | 内容 |
|------|------|
| **ID** | TC-CODEX-001 |
| **对应 Spec** | platform-codex/spec.md → Scenario: platform_map 包含 codex 条目 |
| **优先级** | P0 |
| **预置条件** | `install.py` 的 `platform_map` 已更新 |
| **输入** | 读取 `platform_map.keys()` |
| **预期结果** | `"codex"` 在 `platform_map` 中；配置包含 `target_base: ".codex/skills"`, `is_dir_per_skill: True`, `skill_filename: "SKILL.md"` |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.2 — stdd install codex 创建正确目录结构

| 字段 | 内容 |
|------|------|
| **ID** | TC-CODEX-002 |
| **对应 Spec** | platform-codex/spec.md → Scenario: 安装到项目目录 |
| **优先级** | P0 |
| **预置条件** | 临时项目目录，已执行 `stdd init` |
| **输入** | `stdd install codex` |
| **预期结果** | `.codex/skills/` 目录存在；6 个子目录 `stdd-{understand,spec,slice,build,verify,deliver}/` 各含 `SKILL.md`；每个 SKILL.md 含 YAML frontmatter |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.3 — codex skill frontmatter 格式验证

| 字段 | 内容 |
|------|------|
| **ID** | TC-CODEX-003 |
| **对应 Spec** | platform-codex/spec.md → Scenario: frontmatter 格式与 claude-code 一致 |
| **优先级** | P0 |
| **预置条件** | `stdd install codex` 已执行成功 |
| **输入** | 读取 `.codex/skills/stdd-understand/SKILL.md` 的 YAML frontmatter |
| **预期结果** | frontmatter 包含 `name: stdd-understand`、`description` 非空、`stdd_version` 字段存在 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.4 — 不支持平台的错误提示

| 字段 | 内容 |
|------|------|
| **ID** | TC-CODEX-004 |
| **对应 Spec** | platform-codex/spec.md → Scenario: 不支持的平台错误 |
| **优先级** | P1 |
| **预置条件** | `codex` 不在 platform_map 中（模拟） |
| **输入** | `stdd install codex` |
| **预期结果** | 输出 "不支持的平台: codex" + 列出支持平台列表；退出码 != 0 |
| **当前状态** | ❌ 测试缺（复用已有平台错误测试模式） |

---

### 功能 2-6：语言规范文件存在性验证

对应 specs: `lang-javascript`, `lang-c`, `lang-kotlin`, `lang-swift`, `lang-dart`

#### 案例 2.1 — JavaScript 规范文件结构验证

| 字段 | 内容 |
|------|------|
| **ID** | TC-LANG-001 |
| **对应 Spec** | lang-javascript/spec.md → Scenario: JavaScript 规范文件存在 |
| **优先级** | P0 |
| **预置条件** | STDD 源码仓库 |
| **输入** | 读取 `.stdd/standards/javascript.md` |
| **预期结果** | 文件存在；包含 7 个章节标题（代码风格/类型系统/异步或并发/错误处理/日志/测试规范/审查清单）；审查清单包含 checkbox 格式的检查项（`- [ ]`） |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.2 — C/C++ 规范文件结构验证

| 字段 | 内容 |
|------|------|
| **ID** | TC-LANG-002 |
| **对应 Spec** | lang-c/spec.md → Scenario: C/C++ 规范文件存在 |
| **优先级** | P0 |
| **预置条件** | STDD 源码仓库 |
| **输入** | 读取 `.stdd/standards/c.md` |
| **预期结果** | 文件存在；包含 7 个章节标题；在类型系统和错误处理章节包含「C 语言约定」和「C++ 语言约定」子标题 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.3 — Kotlin 规范文件结构验证

| 字段 | 内容 |
|------|------|
| **ID** | TC-LANG-003 |
| **对应 Spec** | lang-kotlin/spec.md → Scenario: Kotlin 规范文件存在 |
| **优先级** | P0 |
| **预置条件** | STDD 源码仓库 |
| **输入** | 读取 `.stdd/standards/kotlin.md` |
| **预期结果** | 文件存在；包含 7 个章节；包含 Android 特有约定（Jetpack Compose/ViewModel/Hilt） |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.4 — Swift 规范文件结构验证

| 字段 | 内容 |
|------|------|
| **ID** | TC-LANG-004 |
| **对应 Spec** | lang-swift/spec.md → Scenario: Swift 规范文件存在 |
| **优先级** | P0 |
| **预置条件** | STDD 源码仓库 |
| **输入** | 读取 `.stdd/standards/swift.md` |
| **预期结果** | 文件存在；包含 7 个章节；包含 iOS/macOS 特有约定（SwiftUI/MVVM/Combine） |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.5 — Dart/Flutter 规范文件结构验证

| 字段 | 内容 |
|------|------|
| **ID** | TC-LANG-005 |
| **对应 Spec** | lang-dart/spec.md → Scenario: Dart 规范文件存在 |
| **优先级** | P0 |
| **预置条件** | STDD 源码仓库 |
| **输入** | 读取 `.stdd/standards/dart.md` |
| **预期结果** | 文件存在；包含 7 个章节；包含 Flutter 特有约定（Widget 树/状态管理/BuildContext） |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.6 — 所有语言规范章节结构一致性

| 字段 | 内容 |
|------|------|
| **ID** | TC-LANG-006 |
| **对应 Spec** | 各 lang-* spec → Scenario: 七章结构完整 |
| **优先级** | P1 |
| **预置条件** | 所有 10 个语言规范文件存在 |
| **输入** | 遍历 `.stdd/standards/*.md`，提取各文件的一级标题 |
| **预期结果** | 每个文件包含 7 个顶级章节：代码风格、类型系统、异步或并发、错误处理、日志、测试规范、审查清单 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 7：platform-sync — 文档同步更新

对应 spec: `platform-sync/spec.md`

#### 案例 3.1 — EXTENDING.md 包含 Codex

| 字段 | 内容 |
|------|------|
| **ID** | TC-SYNC-001 |
| **对应 Spec** | platform-sync/spec.md → Scenario: EXTENDING.md 包含 Codex 条目 |
| **优先级** | P0 |
| **预置条件** | `EXTENDING.md` 已更新 |
| **输入** | grep "Codex" `EXTENDING.md` |
| **预期结果** | 在「现有平台参考」表格中找到 Codex 行，包含格式描述和特点说明 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.2 — AGENTS.md 与 STDD.md 平台/语言计数一致

| 字段 | 内容 |
|------|------|
| **ID** | TC-SYNC-002 |
| **对应 Spec** | platform-sync/spec.md → Scenario: 平台和语言计数更新 |
| **优先级** | P0 |
| **预置条件** | `AGENTS.md` 和 `STDD.md` 已更新 |
| **输入** | grep 平台数量描述（"适配.*大.*平台"）和语言数量描述（"支持.*门语言"） |
| **预期结果** | AGENTS.md 显示 8 大平台 + 10 门语言；STDD.md 显示相同数量；README.md 和 README_EN.md 同步更新 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.3 — 旧平台安装不受影响（回归）

| 字段 | 内容 |
|------|------|
| **ID** | TC-SYNC-003 |
| **对应 Spec** | platform-sync/spec.md → Scenario: platform_map 包含 codex 条目（隐式回归保护） |
| **优先级** | P0 |
| **预置条件** | install.py platform_map 已添加 codex |
| **输入** | 执行 `stdd install claude-code`、`stdd install cursor`、`stdd install opencode` |
| **预期结果** | 所有已有平台安装成功，输出与变更前一致（除版本号外） |
| **当前状态** | ✅ 已有测试覆盖（`test_install.py` 中现有平台测试） |

---

## 三、测试执行矩阵

| 功能模块 | 单元测试 | 集成测试 | E2E | 状态 |
|----------|---------|----------|-----|------|
| platform-codex (install) | TC-CODEX-001,003,004 | TC-CODEX-002 | — | 🔴 全缺 |
| lang-javascript | TC-LANG-001 | — | — | 🔴 全缺 |
| lang-c | TC-LANG-002 | — | — | 🔴 全缺 |
| lang-kotlin | TC-LANG-003 | — | — | 🔴 全缺 |
| lang-swift | TC-LANG-004 | — | — | 🔴 全缺 |
| lang-dart | TC-LANG-005 | — | — | 🔴 全缺 |
| 跨语言一致性 | TC-LANG-006 | — | — | 🔴 全缺 |
| platform-sync (文档) | TC-SYNC-001,002 | — | — | 🔴 全缺 |
| 回归（已有平台） | TC-SYNC-003 | — | — | 🟢 已有 |

## 四、回归风险矩阵

| 风险区域 | V2.10 改动 | 已有回归保护 | 风险等级 |
|----------|-------------|-------------|---------|
| install.py platform_map | 新增 codex 条目 | `test_install.py` 遍历 platform_map 测试 | 🟢 低 |
| 已有平台 skill 安装 | 未改动已有平台配置 | `test_install.py` 平台安装测试 | 🟢 低 |
| .stdd/standards/ 目录 | 新增 5 个文件 | 无（新增目录条目，不修改已有文件） | 🟢 低 |
| AGENTS.md / STDD.md | 更新平台/语言计数 | 无自动化测试 | 🟡 中 |
| EXTENDING.md | 新增 Codex 行 | 无自动化测试 | 🟢 低 |
| Codex frontmatter 兼容性 | 复用 claude-code frontmatter | 无 Codex CLI 环境验证 | 🟡 中 |

## 五、建议补充顺序

1. **第一优先**（Phase 4 实现前必补）：TC-CODEX-001, TC-CODEX-002, TC-CODEX-003, TC-LANG-001~005, TC-SYNC-001, TC-SYNC-002
2. **第二优先**（实现后尽快补）：TC-CODEX-004, TC-LANG-006
3. **第三优先**（后续补）：Codex CLI E2E 加载验证（需实际 Codex CLI 环境）
