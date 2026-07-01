# Codex 平台适配 + 多语言规范扩展（JS/C++/Kotlin/Swift/Dart）

<!-- STDD-MARKER: title — 变更标题，同时作为 change 目录名的基础 -->

## Why

STDD 当前支持 **7 个 AI 编程平台**（Claude Code、Cursor、Copilot、Aider、WorkBuddy、Trae、OpenCode）和 **5 门语言**（Python、Java、Go、Rust、TypeScript）。存在两个系统性缺口：

1. **OpenAI Codex CLI 缺失**：Codex CLI 是 OpenAI 推出的终端 AI 编码代理（对标 Claude Code），使用 `AGENTS.md` 指令文件 + `~/.codex/config.toml` 配置，已纳入 Linux Foundation 的 Agentic AI Foundation 标准。STDD 尚未提供 Codex 平台适配，损失 OpenAI 生态用户。

2. **语言覆盖不足**：缺少 JavaScript（纯 JS，非 TS）、C/C++（系统级）、Kotlin（Android）、Swift（iOS）、Dart/Flutter（跨平台移动端）五大常用语言规范，限制 STDD 在移动端和系统级开发场景的应用。

参考先例：V2.3（`archive/2026-05-15-stdd-foundation-improvements/`）曾一次性新增 3 平台 + 4 语言，本次变更遵循相同模式。

## What Changes

<!-- STDD-MARKER: what_changes — 每项为一条变更描述，bullet list -->
- 新增 **OpenAI Codex CLI** 平台适配（`stdd install codex`），部署 STDD 6 阶段 skill 到 Codex 可识别路径
- 新增 **JavaScript** 开发规范（`.stdd/standards/javascript.md`），独立于 TypeScript，覆盖 Node.js 生态
- 新增 **C/C++** 开发规范（`.stdd/standards/c.md`），覆盖系统级开发场景
- 新增 **Kotlin** 开发规范（`.stdd/standards/kotlin.md`），覆盖 Android 生态
- 新增 **Swift** 开发规范（`.stdd/standards/swift.md`），覆盖 iOS/macOS 生态
- 新增 **Dart/Flutter** 开发规范（`.stdd/standards/dart.md`），覆盖跨平台移动端
- 更新 `install.py` platform_map + `EXTENDING.md` + `AGENTS.md` 文档

## Capabilities

### New Capabilities

<!-- STDD-MARKER: new_capabilities — 格式: - **<名称>**：<描述> -->
- **platform-codex**：OpenAI Codex CLI 平台适配器，`stdd install codex` 部署 6 阶段 skill
- **lang-javascript**：JavaScript 开发规范（Node.js 生态，Jest + ESLint）
- **lang-c**：C/C++ 开发规范（GTest/Catch2 + clang-tidy/clang-format）
- **lang-kotlin**：Kotlin 开发规范（JUnit5 + ktlint/detekt）
- **lang-swift**：Swift 开发规范（XCTest + SwiftLint）
- **lang-dart**：Dart/Flutter 开发规范（flutter test + dart analyze）

### Modified Capabilities

<!-- STDD-MARKER: modified_capabilities — 格式: - **<名称>**：<描述> -->
- **platform-sync**：`install.py` platform_map 扩展 + `EXTENDING.md` 平台列表更新

## Impact

<!-- STDD-MARKER: impact — 按层面分类的受影响文件/资源清单 -->

**代码层面**：
- 新建 6 个语言规范文件（`.stdd/standards/{javascript,c,kotlin,swift,dart}.md`，约 150 行/文件）
- 新建 1 个平台适配目录（`.stdd/platforms/codex/`，含 6 个 skill 文件）
- 修改 `stdd/cli/commands/install.py`（添加 codex 到 platform_map）
- 修改 `EXTENDING.md`（更新平台列表）
- 修改 `AGENTS.md`（更新平台数量描述）
- 预计：~12 个新建文件，~3 个修改文件，~1200 行

**配置层面**：
- `project.yaml` 无需变更（语言为项目级设置，新语言由用户按需选用）

**基础设施**：
- 无新服务/API 需求

## Constraints

<!-- STDD-MARKER: constraints — 技术/资源/时间约束 -->
- 不修改现有 5 门语言规范的内容（增量添加新语言）
- 不修改现有 7 个平台的适配逻辑（仅增量添加 Codex）
- Codex 适配复用 `stdd install` 框架，不新增独立 CLI 命令
- Codex skill 格式需 Phase 2 调研确认（directory-per-skill vs single-file vs AGENTS.md 指令注入）

## Stakeholders

<!-- STDD-MARKER: stakeholders — 受影响方或相关角色 -->
- STDD 用户（OpenAI 生态开发者）
- 移动端开发者（Android/iOS/Flutter）
- 系统级/C++ 开发者
- STDD 维护者

## Risk Areas

<!-- STDD-MARKER: risk_areas — 格式: - capability: <name> — <风险描述> -->
- capability: platform-codex — Codex CLI 的 skill 系统可能与 Claude Code 格式不完全兼容，需要 Phase 2 先调研 Codex skill 格式，决定 directory-per-skill vs single-file 方案
- capability: lang-c — C 和 C++ 是两个独立语言，合并在一个规范文件中可能导致覆盖不完整，Phase 2 评估是否拆分为两个文件

## NonGoals

<!-- STDD-MARKER: non_goals — 明确不在此变更范围内的事项 -->
- 不修改现有 5 门语言规范内容
- 不修改现有 7 个平台的适配逻辑
- 不为 Codex 开发独立 CLI 命令
- 不在此变更中增加其他平台（如 Gemini CLI、Windsurf 等）
- 不添加 Rust 已覆盖之外的系统级语言（如 Zig、Nim 等）

## Critical

<!-- STDD-MARKER: critical — 是否关键变更（V2.6新增）。true 时 Phase 2 须通过锚定评估 -->
- [x] 非关键变更（默认）
- [ ] 关键变更 — 涉及安全/金融/核心基础设施，需 L3/L4 锚定

## Risk Assessment

<!-- STDD-MARKER: risk_assessment — 风险分类评估（V2.6新增） -->
- **safety_critical**：false（不涉及认证/授权/加密/数据保护）
- **financial**：false（不涉及金融交易或资金流转）
- **cross_system**：false（不涉及多系统协调）

## Anchoring

<!-- STDD-MARKER: anchoring — 锚定策略（V2.6新增） -->
- **level**：L2（接口锚定 — 参考现有平台适配和语言规范的接口模式）
- **reference_changes**：无
- **anchor_implementations**：`archive/2026-05-15-stdd-foundation-improvements/`（V2.3 多平台+多语言先例）、`.stdd/platforms/opencode/`（最新平台适配模式）、`.stdd/standards/python.md`（规范模板）

## Success Criteria

<!-- STDD-MARKER: success_criteria — 可验证的完成条件 -->
- [ ] `stdd install codex` 执行成功，Codex CLI 可识别并加载 STDD 6 阶段 skill
- [ ] `.stdd/standards/javascript.md` 存在，覆盖代码风格/类型/异步/错误处理/测试/审查清单 6 维度
- [ ] `.stdd/standards/c.md` 存在，覆盖 C/C++ 双语言，同上 6 维度
- [ ] `.stdd/standards/kotlin.md` 存在，覆盖同上 6 维度 + Android 特有约定
- [ ] `.stdd/standards/swift.md` 存在，覆盖同上 6 维度 + iOS/macOS 特有约定
- [ ] `.stdd/standards/dart.md` 存在，覆盖同上 6 维度 + Flutter widget 测试约定
- [ ] `install.py` 支持 `codex` 平台选项，`--help` 中可见
- [ ] `EXTENDING.md` 平台列表包含 Codex

---

> **复杂度评分**：6/17 → **standard** 模式 | **锚定等级**：L2（接口锚定）
> **先例参考**：`archive/2026-05-15-stdd-foundation-improvements/`（V2.3 多平台+多语言）
