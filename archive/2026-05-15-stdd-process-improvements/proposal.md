# STDD 流程改进：Gate 交互信息完善 + 长程模式可靠性提升

## Why

STDD V2.1 在实战使用中发现 4 个影响用户体验和流程可靠性的问题：

1. **Gate 交互信息不完整** — understand/spec/verify 三个阶段都有对应的 review 步骤（Step 3.5/4.5/Step0），但三个 gate 的确认消息模板中都没有展示 review 的执行情况和结果，用户无法知晓进行了哪些自动审查、效果如何
2. **模式选择不稳定** — Gate 2 后的长程/普通模式选择有时出现有时不出现，`long_range.default: true` 和 `10秒默认` 的歧义导致 AI 可能跳过询问
3. **长程模式"半自动化"** — 概念性预授权无法落地为 Claude Code 实际权限，导致交互框频繁打断；build 完成后在轮次边界停止等待用户输入才进入 verify；一次性授权交互不稳定
4. **Verify 步骤可能被跳过** — 缺少强制步骤检查机制，出现过只做功能测试（Step 1）就进入 Gate 3 的情况

这些问题降低了 STDD 的可靠性和长程模式"全自动连续执行"的核心价值。

## What Changes

1. Gate 1/2/3 确认消息模板中增加「自动审查结果」段落，展示 review 维度、发现数、修复数、结论
2. Gate 2 后模式选择改为强制步骤，删除 `10秒默认` 自动行为，`default` 配置改为 `recommended`
3. 长程模式预授权后增加 Claude Code 实际权限配置步骤；为 build/verify 增加「长程模式运行协议」和「阶段自动衔接指令」
4. Verify 开头添加强制步骤检查清单；Gate 3 模板增加 6 步完成确认表

## Capabilities

### Modified Capabilities

- `gate-interaction`：3 个确认门的消息模板增加 review 结果展示和步骤完成确认
- `mode-selection`：Gate 2 后模式选择流程强制化，消除跳过歧义
- `long-range-execution`：增加实际权限配置、运行协议、阶段自动衔接指令
- `verify-completeness`：增加强制步骤清单和 Gate 3 完成确认机制

### New Capabilities

无

## Impact

**代码层面**（每项涉及最多 3 份 skill 拷贝需同步修改，共 12+ 文件）：
- `.claude/skills/stdd-understand/SKILL.md` — Gate 1 模板增加 review 结果块
- `.claude/skills/stdd-spec/SKILL.md` — Gate 2 模板 + 模式选择强制化 + 权限配置步骤
- `.claude/skills/stdd-build/SKILL.md` — 长程模式运行协议 + 自动衔接指令
- `.claude/skills/stdd-verify/SKILL.md` — Gate 3 模板 + 长程协议 + 强制步骤清单
- `.stdd/skills/understand.md`, `spec.md`, `build.md`, `verify.md` — 主版本同步
- `.stdd/platforms/claude-code/skills/stdd-understand.md`, `stdd-spec.md`, `stdd-build.md`, `stdd-verify.md` — 平台版本同步
- `.stdd/config.d/long_range.yaml` — `default` → `recommended` + 新增协议配置项
- `.stdd/templates/long-range-auth.md` — 增加权限配置说明

**配置层面**：
- `.stdd/config.d/long_range.yaml`：`default: true` → `recommended: true`，新增 `protocol` 配置项
- `.claude/settings.local.json`：长程模式预授权后自动添加操作权限（运行时修改）

**基础设施**：无

## Success Criteria

- [ ] Gate 1 确认消息包含 proposal review 结果（审查维度、发现数、修复数、结论）
- [ ] Gate 2 确认消息包含 design+specs review 结果
- [ ] Gate 3 确认消息包含 Step 0 三路并行 review 结果 + 6 步强制步骤完成确认表
- [ ] Gate 2 后每次都弹出模式选择交互（不跳过）
- [ ] 长程模式预授权后自动配置 Claude Code 实际权限
- [ ] 长程模式 build 完成后自动进入 verify（不等待用户输入）
- [ ] 长程模式全流程中无意外交互暂停（仅降级条件触发和 Gate 3 例外）
- [ ] Verify 阶段 6 个强制步骤全部执行后才能展示 Gate 3 确认
