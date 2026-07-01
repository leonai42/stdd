# Codex 平台适配 + 多语言规范扩展 — 技术设计

## Context

STDD V2.9.4 当前状态：
- **平台**：7 个 AI 编程平台适配（Claude Code、Cursor、Copilot、Aider、WorkBuddy、Trae、OpenCode）
- **语言规范**：5 门语言（Python、Java、Go、Rust、TypeScript），均遵循 python.md 的 7 章 6 维度模板
- **平台安装**：`stdd install <platform>` 通过 `install.py` 的 `platform_map` 分发，支持 3 种模式（directory-per-skill / flat-skills / single-file）
- **Codex CLI**：OpenAI 的终端 AI 编码代理，使用 `AGENTS.md` 指令文件体系 + `~/.codex/config.toml` 配置，已纳入 Linux Foundation Agentic AI Foundation 标准。支持 `~/.codex/skills/` 自定义 skill 目录。
- **新增语言需求**：JavaScript（纯 JS）、C/C++（系统级）、Kotlin（Android）、Swift（iOS）、Dart/Flutter（跨平台移动端）

## Decisions

### 1. Codex 平台适配方式：directory-per-skill → `.codex/skills/`

**方案**：采用与 Claude Code / OpenCode 相同的 directory-per-skill 格式，`stdd install codex` 将 6 阶段 skill 部署为 `.codex/skills/stdd-<phase>/SKILL.md`。同时确保项目根目录 `AGENTS.md` 包含 STDD 工作流引用。

**为什么**：
- Codex CLI 支持自定义 skill 目录（`~/.codex/skills/` 和项目级 `.codex/skills/`），markdown + YAML frontmatter 格式与 Claude Code 高度兼容
- `AGENTS.md` 是 Codex 的 auto-load 指令文件，STDD 已生成该文件，Codex 用户可立即受益
- directory-per-skill 模式与 Claude Code / OpenCode 保持一致，降低维护成本
- 复用现有 `_make_claude_code_frontmatter` 生成 frontmatter（Codex 兼容此格式）

**备选方案及排除原因**：
- **Single-file（如 Cursor）**：Codex 支持 skill 系统，single-file 未充分利用平台能力，且与 STDD 6 阶段分离架构不匹配
- **仅依赖 AGENTS.md**：AGENTS.md 有 32 KiB 上限，嵌入完整 6 阶段 skill 内容会超限；且 skill 分离加载更灵活
- **全局安装（`~/.codex/skills/`）**：作为 `--global` 选项补充，默认安装到项目目录

### 2. Codex frontmatter 格式：复用 claude-code 格式

**方案**：Codex skill 的 YAML frontmatter 使用与 Claude Code 相同的格式（`name` + `description` + 可选 `stdd_version`）。

**为什么**：Codex CLI 的 skill 系统使用标准 YAML frontmatter，字段名与 Claude Code 一致。已验证 OpenCode 使用相同格式无问题。

**备选方案及排除原因**：
- 自定义 Codex 特有字段：Codex 未要求特有 frontmatter 字段，增加字段只会制造不必要的格式分歧
- 无 frontmatter（纯 markdown）：丢失 skill 元数据，Codex 无法正确识别和索引 skill

### 3. 语言规范结构：沿用 python.md 的 7 章 6 维度模板

**方案**：JavaScript / C / Kotlin / Swift / Dart 五种语言规范均采用 python.md 的 7 章结构（代码风格、类型系统、异步或并发、错误处理、日志、测试规范、审查清单），每章按语言特性定制。

**为什么**：7 章 6 维度已在 Python/Java/Go/Rust/TypeScript 5 门语言中验证有效，覆盖了 STDD Phase 4 Step 0 "学习规范"和 Phase 5 Step 2 "Diff 审查"所需的所有检查维度。跨语言一致的结构降低 AI 切换语言的认知成本。

**备选方案及排除原因**：
- 每语言独立结构：灵活但失去跨语言一致性，STDD skill 需要额外逻辑判断
- 引用外部 style guide（如 Google JS Guide、Apple Swift Guide）：外部链接不稳定，缺少 STDD 特有的测试规范和审查清单

### 4. C 和 C++ 是否拆分：单文件 `c.md`，内部明确分区

**方案**：C 和 C++ 共用 `.stdd/standards/c.md`，内部通过「C 语言约定」和「C++ 语言约定」子章节明确区分。每章中 C 和 C++ 的差异内容分别标注。

**为什么**：
- C 和 C++ 共享大量语法基础和工具链（GCC/Clang、GDB、Make/CMake），合并可减少重复内容
- 实际项目中 C 和 C++ 常混合使用（如嵌入式、系统编程）
- 如果后续用户反馈需要拆分，从合并文件拆分比从两个文件合并更容易

**备选方案及排除原因**：
- 拆分为 `c.md` + `cpp.md`：C 和 C++ 确实有显著差异（类/模板/RAII/异常 vs 纯函数/手动内存管理），但首次实现先合并观察使用情况，在 proposal 中已识别此风险

### 5. 新增平台适配方式：最小化适配 + 渐进增强

**方案**：Codex 首次适配提供最小可用版本 — 6 阶段 skill 文件 + `AGENTS.md` 引用。后续按用户反馈增量改进（如添加 Codex 特有配置、memory 集成等）。

**为什么**：遵循 V2.3 确立的"最小化适配，渐进增强"原则（Decision 3）。新平台的实际使用模式需要通过实践验证，过早做完整适配可能方向错误。

**备选方案及排除原因**：
- 一次性完整适配（含 Codex memory、config.toml 自动配置等）：工作量大且缺乏实际使用反馈
- 只更新 AGENTS.md 引用不做 skill 部署：没有充分利用 Codex 的 skill 系统

### 6. STDD.md 全局文件格式：双轨制同步更新

**方案**：在项目根 `STDD.md` 和 `AGENTS.md` 中同步更新平台数量（7→8）和语言数量（5→10），保持双轨文档一致性。

**为什么**：`STDD.md` 是通用 fallback（Cursor/Copilot 等单文件平台引用），`AGENTS.md` 是 Codex 的 auto-load 指令文件。两者描述的项目元信息必须一致。

**备选方案及排除原因**：
- 只更新一个文件：造成文档不一致，用户困惑

## Architecture

```
.stdd/
├── standards/                          # 语言规范（本次扩展）
│   ├── python.md                       # [已有] Python
│   ├── java.md                         # [已有] Java
│   ├── go.md                           # [已有] Go
│   ├── rust.md                         # [已有] Rust
│   ├── typescript.md                   # [已有] TypeScript
│   ├── javascript.md                   # [新增] JavaScript (Node.js)
│   ├── c.md                            # [新增] C/C++
│   ├── kotlin.md                       # [新增] Kotlin (Android)
│   ├── swift.md                        # [新增] Swift (iOS/macOS)
│   └── dart.md                         # [新增] Dart/Flutter
│
├── platforms/                          # 平台适配（本次扩展）
│   ├── claude-code/skills/             # [已有] V2.9.4
│   ├── workbuddy/skills/               # [已有]
│   ├── trae/skills/                    # [已有]
│   ├── cursor/rules/                   # [已有]
│   ├── copilot/                        # [已有]
│   ├── aider/                          # [已有]
│   ├── opencode/skills/                # [已有] (spec exists, dir pending)
│   └── codex/skills/                   # [新增] OpenAI Codex CLI
│       ├── stdd-understand/SKILL.md
│       ├── stdd-spec/SKILL.md
│       ├── stdd-slice/SKILL.md
│       ├── stdd-build/SKILL.md
│       ├── stdd-verify/SKILL.md
│       └── stdd-deliver/SKILL.md
│
├── skills/                             # Master Skill（不变）
└── config.d/                           # 配置（不变）
```

**数据流**：
```
proposal.md → design.md（本文件）
  → specs/platform-codex/spec.md        → install.py 适配实现
  → specs/lang-javascript/spec.md       → .stdd/standards/javascript.md
  → specs/lang-c/spec.md                → .stdd/standards/c.md
  → specs/lang-kotlin/spec.md           → .stdd/standards/kotlin.md
  → specs/lang-swift/spec.md            → .stdd/standards/swift.md
  → specs/lang-dart/spec.md             → .stdd/standards/dart.md
  → specs/platform-sync/spec.md         → install.py + EXTENDING.md + AGENTS.md 更新
```

**Codex 安装流程**：
```
stdd install codex
  → 读取 .stdd/skills/*.md (master)
  → 注入 _make_claude_code_frontmatter (name + description + stdd_version)
  → 写入 .codex/skills/stdd-<phase>/SKILL.md (6 个 phase)
  → 检查 AGENTS.md 是否包含 STDD 引用
  → 输出使用提示
```

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|----------|
| Codex skill 格式与 Claude Code 不完全兼容 | Phase 2 调研确认：Codex 使用标准 YAML frontmatter + markdown body，与 Claude Code 格式一致；如有差异在实现阶段微调 frontmatter 函数 |
| C/C++ 单文件覆盖不完整 | 规范内部按「C 语言约定」/「C++ 语言约定」明确分区；如用户反馈需要拆分，后续迭代处理 |
| 5 门新语言规范缺乏对应语言实战验证 | 标注 "Initial version — validated on Python patterns, language-specific review needed"，后续在实际项目中迭代 |
| 语言规范内容质量（每门 ~150 行）难以逐一深度审查 | 每门语言规范按同一模板生成，用 python.md 做交叉校验；Phase 5 阶段逐文件检查 |
| Codex CLI 版本更新导致 skill 路径变化 | 适配文件中标注目标版本（Codex CLI 2026.x），`stdd upgrade` 时同步更新 |
| STDD.md 和 AGENTS.md 的平台/语言数量描述不一致 | 在 test-plan 中加入一致性检查 TC，Phase 5 验证阶段自动检测 |
