# V2.2 任务清单

## 1. Gate 1 Review 展示 — stdd-understand（P0）

- [ ] 1.1 修改 `.claude/skills/stdd-understand/SKILL.md` Gate 1 模板（Step 4），增加 `🔍 自动审查结果` 段落
- [ ] 1.2 同步修改 `.stdd/skills/understand.md` 主版本
- [ ] 1.3 同步修改 `.stdd/platforms/claude-code/skills/stdd-understand.md` 平台版本
- [ ] 1.4 TC-GATE-001 验证：Grep "🔍 自动审查结果" 确认 3 份文件均包含

## 2. Gate 2 Review + 模式选择强制 + 权限配置 — stdd-spec（P0）

- [ ] 2.1 修改 `.claude/skills/stdd-spec/SKILL.md`：
  - Gate 2 模板（Step 5）增加 `🔍 自动审查结果` 段落（TC-GATE-002）
  - Step 7 标记 `【强制】`，删除 `10秒默认` 行，增加 `必须使用 AskUserQuestion` 指令（TC-MODE-001）
  - Step 7a 后增加 Step 7a.5 权限配置步骤（TC-LONG-001）
- [ ] 2.2 同步修改 `.stdd/skills/spec.md` 主版本
- [ ] 2.3 同步修改 `.stdd/platforms/claude-code/skills/stdd-spec.md` 平台版本
- [ ] 2.4 修改 `.stdd/config.d/long_range.yaml`：`default: true` → `recommended: true`（TC-MODE-002）
- [ ] 2.5 修改 `.stdd/templates/long-range-auth.md`：增加权限配置说明段落
- [ ] 2.6 TC-GATE-002 / TC-MODE-001 / TC-MODE-002 / TC-LONG-001 验证

## 3. 长程运行协议 + 自动衔接 — stdd-build（P0）

- [ ] 3.1 修改 `.claude/skills/stdd-build/SKILL.md`：
  - 增加 `长程模式运行协议` 章节（TC-LONG-003）
  - Step 3（切片完成后）增加长程模式自动衔接指令（TC-LONG-002）
- [ ] 3.2 同步修改 `.stdd/skills/build.md` 主版本
- [ ] 3.3 同步修改 `.stdd/platforms/claude-code/skills/stdd-build.md` 平台版本
- [ ] 3.4 TC-LONG-002 / TC-LONG-003 验证

## 4. Gate 3 Review + 强制步骤清单 + 长程协议 — stdd-verify（P0）

- [ ] 4.1 修改 `.claude/skills/stdd-verify/SKILL.md`：
  - 增加 `⚠️ 强制步骤清单` 章节（6 步表格）（TC-VERIFY-001）
  - Gate 3 模板（Step 6）增加三路并行 review 结果展示和步骤完成确认表（TC-GATE-003, TC-VERIFY-002）
  - 增加 `长程模式运行协议` 章节（TC-LONG-004）
- [ ] 4.2 同步修改 `.stdd/skills/verify.md` 主版本
- [ ] 4.3 同步修改 `.stdd/platforms/claude-code/skills/stdd-verify.md` 平台版本
- [ ] 4.4 TC-GATE-003 / TC-VERIFY-001 / TC-VERIFY-002 / TC-LONG-004 验证

## 5. 最终一致性验证（P1）

- [ ] 5.1 逐文件对比 `.claude/skills/` 与 `.stdd/skills/` 与 `.stdd/platforms/claude-code/skills/` 关键段落一致
- [ ] 5.2 所有 11 个 TC 案例通过
