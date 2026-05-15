# STDD 流程改进 - 技术设计

## Context

STDD 系统当前由三层 skill 文件组成：
- `.claude/skills/stdd-*/SKILL.md` — Claude Code 运行时加载的版本（含 frontmatter）
- `.stdd/skills/*.md` — 主版本
- `.stdd/platforms/claude-code/skills/stdd-*.md` — Claude Code 平台适配版本

外加配置文件（`.stdd/config.d/`）和模板文件（`.stdd/templates/`）。本次修改涉及 4 个 capability，均为模板文本和配置项调整。

技术约束：
- Skill 文件是 Markdown 格式，修改限于文本模板和指令措辞
- Claude Code 权限通过 `.claude/settings.local.json` 的 `permissions.allow` 数组控制
- 3 份 skill 拷贝需要同步修改，保持内容一致

## Decisions

### 1. Gate 模板增加 review 结果展示

**方案**：在现有 gate 确认消息模板中插入 `🔍 自动审查结果` 段落，格式统一为：审查维度列表 + 发现问题数/自动修复数 + 审查结论。

**为什么**：最小的模板改动，不改变 gate 的交互逻辑。用户一眼看清 review 执行情况，信息密度高。

**备选方案及排除原因**：
- 备选 A：用单独的 AskUserQuestion 展示 review 结果 → 增加一次交互，打断流程
- 备选 B：仅在 test-report 中记录 review 结果 → 用户 gate 决策时看不到

### 2. 模式选择强制化

**方案**：`long_range.default: true` → `recommended: true`，删除 `⏱ 10 秒后默认选择长程模式`，Step 7 标记 `【强制】`，增加 `必须使用 AskUserQuestion` 指令。

**为什么**：`default: true` + `10秒默认` 的语义让 AI 有理由跳过询问。`recommended` 语义精确表达"推荐但不强制"，配合 `【强制】` 标记确保不跳过。

**备选方案及排除原因**：
- 备选 A：直接删除 default 配置 → 失去推荐偏好，用户可能困惑

### 3. 长程模式权限落地

**方案**：预授权确认后增加 Step 7a.5，使用 Edit 工具修改 `.claude/settings.local.json` 的 `permissions.allow` 数组，添加 pytest/ruff/python/pip/git 等 Bash 规则，以及 Write/Edit 规则覆盖 changes/、app/、tests/ 目录。

**为什么**：STDD 的概念性预授权在 Claude Code 中无效，必须配置实际工具权限才能消除交互框。仅修改项目级 settings.local.json，不污染全局配置。

**备选方案及排除原因**：
- 备选 A：使用 `update-config` skill → 可能不如直接 Edit 精确
- 备选 B：修改全局 `~/.claude/settings.json` → 影响其他项目，不安全

### 4. 阶段自动衔接 + 长程运行协议

**方案**：
- build 末尾和 slice 末尾增加 `长程模式下立即自动调用下一阶段 Skill` 指令
- build 和 verify 开头增加 `长程模式运行协议` 章节，定义：无交互、批量执行、自动降级检测、进度汇报、阶段自动衔接

**为什么**：将长程模式行为规范内嵌到每个 skill 文件中，AI 在加载 skill 时就能看到完整的执行约束，而不需要"记住"预授权时的承诺。

**备选方案及排除原因**：
- 备选 A：仅在 spec Step 7a 中说明 → AI 可能在长上下文中忘记

### 5. Verify 强制步骤清单

**方案**：verify 开头增加 `⚠️ 强制步骤清单` 表格（6 步），Gate 3 模板增加步骤完成确认表。双重保障。

**为什么**：入口声明让 AI 在进入 verify 时就知道不可跳过步骤；出口检查（Gate 3 时必须汇报每步完成状态）防止悄悄跳过。

**备选方案及排除原因**：
- 备选 A：仅在 Gate 3 检查 → 发现问题时已太晚
- 备选 B：用代码脚本检查 → 过度工程，skill 文件修改不需要

## Architecture

数据流：用户发起需求 → Phase 1 → Gate 1（含 review）→ Phase 2 → Gate 2（含 review）→ 【强制模式选择】→ 长程/普通分支 → Phase 3 → Phase 4（含协议）→ Phase 5（含强制清单）→ Gate 3（含 review + 步骤确认）

长程模式权限配置流：
```
用户确认预授权 → Step 7a.5: Read settings.local.json
  → Edit settings.local.json（添加 permissions.allow 规则）
  → 更新 .stdd.yaml（long_range.pre_auth_completed = true）
  → Phase 3 自动启动 → Phase 4 自动启动 → Phase 5 自动启动
  → Gate 3（强制确认）
```

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|----------|
| 权限配置过宽导致安全风险 | 仅修改项目级 `settings.local.json`，规则限定于开发工具命令 |
| 3 份 skill 拷贝不同步 | 本次修改逐文件同步；后续可考虑自动化一致性检查脚本 |
| 长程模式自动衔接可能掩盖问题 | 保留全部降级条件，测试通过率 < 95% 或连续修复失败 3 次仍会暂停 |
| mode-selection 强制化增加一次交互 | 这是有意为之 — 模式选择本身就应该是显式决策 |
