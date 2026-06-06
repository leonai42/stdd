# 跨平台 Guard Hook 适配 — 设计方案

## 问题

当前 Guard 的 PreToolUse 自动拦截仅 Claude Code 支持。其他平台（Cursor/Windsurf/Cline/Copilot）只能通过规则文件做软约束，无法真正阻止未授权的编辑。

## 各平台 Hook 能力调研

| 平台 | 编辑前拦截 | 等价机制 | 可行性 |
|------|----------|---------|--------|
| **Claude Code** | ✅ PreToolUse Hook | `stdd guard check` exit 2 | 已实现 |
| **Cursor** | ❌ | `.cursorrules` + AI Rules 注入提示 | 软约束，依赖 AI 遵守 |
| **Windsurf** | ❌ | Cascade Rules 注入 | 软约束 |
| **Cline (VS Code)** | ⚠️ Plan/Act 模式 | Plan 模式要求先检查 | 可注入 Plan 步骤 |
| **Copilot** | ❌ | `.github/copilot-instructions.md` | 软约束 |
| **Aider** | ⚠️ | `--edit-format` + conventions | 有限约束 |
| **OpenCode** | ❌ | 自定义命令 | 软约束 |

## 适配方案（按优先级）

### P0: Claude Code（已完成）
PreToolUse Hook → `stdd guard check --platform claude-code`。

### P1: Cursor + Windsurf（规则注入增强）
在现有规则注入基础上，添加更明确的 guard 指令：
```
# .cursorrules / .windsurfrules
BEFORE ANY Edit/Write operation:
1. Run `stdd guard check --platform cursor`
2. If exit code 2, STOP. Ask user to open a batch or change.
3. If exit code 0, proceed.
```
**局限**：AI 可能不遵守，无硬件强制。

### P2: Cline（Plan 模式集成）
在 Cline 的 Plan 模式中注入 STDD 检查步骤：
```
Plan Step 0: Run stdd guard check
  - If blocked → present options to user
  - If allowed → continue
```
**优势**：Plan 模式天然需要用户确认。

### P3: 通用方案（git pre-commit hook）
不依赖 AI 平台，在 git 层面拦截：
```bash
# .git/hooks/pre-commit
stdd guard check --platform git --strict
if [ $? -eq 2 ]; then
  echo "STDD Guard blocked. Use stdd batch open or stdd new."
  exit 1
fi
```
**优势**：全平台通用，但只在 commit 时拦截（非编辑时）。

## 推荐策略

短期：P1（Cursor/Windsurf 规则增强）+ P3（git pre-commit 兜底）
长期：等各平台开放 PreToolUse 级 Hook API

## 状态

V2.9.4 设计方案，待 V2.9.5+ 实现 P1 和 P3。
