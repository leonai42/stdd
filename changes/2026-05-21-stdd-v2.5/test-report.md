# STDD V2.5 测试报告

> 测试日期：2026-05-21
> 测试环境：Windows 10 Pro, Python 3.12.7, pytest 9.0.3
> 被测版本：changes/2026-05-21-stdd-v2.5

## 一、总体概况

| 指标 | 数值 |
|------|------|
| 测试用例总数 | 155 |
| 通过 | 155 |
| 失败 | 0 |
| 跳过 | 0 |
| 通过率 | 100% |
| 执行耗时 | 5.41s |

### 1.1 覆盖率诊断（仅变更文件）

| 变更文件 | 行覆盖率 | 状态 |
|----------|----------|------|
| stdd/cli/commands/experience.py | 72% | ✅ |
| stdd/cli/commands/ci.py | 83% | ✅ |
| stdd/cli/commands/extract_proposal.py | 91% | ✅ |
| stdd/cli/commands/gate.py | 89% | ✅ |
| stdd/cli/commands/curate.py | 36% | ⚠️ 低覆盖 |
| stdd/cli/commands/state.py | 35% | ⚠️ 低覆盖 |
| stdd/cli/__init__.py | 5% | N/A (注册代码) |

**低覆盖文件说明**：
- `curate.py` — `cmd_curate_pull` 和 `cmd_curate_review` 依赖外部 HTTP 和交互输入，未在单元测试中覆盖。HTTP mock 测试优先级低（curate 仅维护者使用）。
- `state.py` — `cmd_state` 的 CLI 入口路径未被测试覆盖。`read_resume_context` 和 `write_resume_context` 核心函数已覆盖。

## 二、按模块统计

| 测试模块 | 用例数 | 通过 | 失败 | 说明 |
|----------|--------|------|------|------|
| test_experience.py | 34 | 34 | 0 | 生命周期 + 社区池 + project_type |
| test_ci.py | 23 | 23 | 0 | CI 增强 + check-failures 聚合 |
| test_extract_proposal.py | 13 | 13 | 0 | 扩展 4 字段 + 向后兼容 |
| test_state.py | 4 | 4 | 0 | resume context 读写 |
| test_gate.py | 7 | 7 | 0 | CLI approve + file token |
| test_curate.py | 2 | 2 | 0 | 相似度计算 + 去重检测 |
| 其他已有测试 | 72 | 72 | 0 | 回归验证 |

## 三、CI 失败模式检查结果

| 检查项 | 状态 | 说明 |
|--------|------|------|
| (a) 文件存在 | ✅ PASS | 所有必需文件存在 |
| (d) TC-ID 唯一性 | ✅ PASS | 39 个唯一 TC-ID |
| (f) SHALL 关键字 | ✅ PASS | 所有 THEN 含 SHALL |
| (g) AND 数量 | ✅ PASS | AND 数量正常 |
| (k) 契约一致性 | ✅ PASS | 8 capabilities 契约一致 |
| (b) 范围蔓延 | ⏭ SKIP | proposal 未用 STDD-MARKER 格式 |
| (j) 覆盖真空 | ⏭ SKIP | 无 coverage.json |

## 四、11 类失败模式检查

| # | 模式 | 结果 | 说明 |
|---|------|------|------|
| (a) | 幻觉行为 | ✅ 无命中 | 所有文件路径/API 引用真实存在 |
| (b) | 范围蔓延 | ✅ 无命中 | 15 个变更文件均在 V2.5 scope 内 |
| (c) | 级联错误 | ✅ 无命中 | try/except 仅在系统边界 |
| (d) | 上下文丢失 | ✅ 无命中 | 实现与 design.md 一致 |
| (e) | 工具误用 | ✅ 无命中 | 全部使用 Edit/Write 专用工具 |
| (f) | 运行时行为偏差 | ✅ 无命中 | CLI 工具无 UI 交互 |
| (g) | 管线断链 | ✅ 无命中 | 所有命令通过 __init__.py 正确派发 |
| (h) | 内容质量偏差 | ⚠️ 注意 | curate.py 36%, state.py 35% 覆盖率低 |
| (i) | 指令衰减 | ⚠️ 已记录 | Gate 3 惯性误判 → EXP-2026-0004 |
| (j) | 覆盖真空 | ⚠️ 注意 | 整体 72%，curate review/pull 未覆盖 |
| (k) | 契约断层 | ✅ 无命中 | CI check-contracts 通过 |

## 五、功能/测试覆盖对照

| 功能模块 | 涉及源码 | 测试覆盖 | 缺口 |
|---------|---------|---------|------|
| experience-lifecycle | experience.py | 8 TC | 无 |
| ci-check-enhanced | ci.py | 8 TC | 无 |
| session-resume | state.py | 4 TC | cmd_state CLI 入口 |
| community-experience-pool | experience.py, curate.py | 12 TC | curate pull/review 端到端 |
| gate-file-confirm | gate.py | 7 TC | 无 |
| extract-proposal-extended | extract_proposal.py | 6 TC | 无 |
| non-code-change-support | experience.py, build.md, verify.md | 5 TC | AI 行为目视验证 |
| parallel-slice-guide | build.md | 目视 | AI 执行验证 |

## 六、经验库更新

### 本次新增经验

| 经验ID | 类别 | 模式 | 严重程度 | 发现阶段 |
|--------|------|------|---------|---------|
| EXP-2026-0004 | instruction_decay | AI 行为惯性导致关键决策点未验证源文件 | high | SPEC |

### 经验统计

| 指标 | 数值 |
|------|------|
| 本次新增 | 1 条 |
| 经验库总计 | 4 条 |

## 七、设计调整

无重大设计调整。实现严格按照 design.md 和 specs 执行。

## 八、结论

**155/155 测试全部通过，零回归，CI 检查 5/5 通过。**

| 信号源 | 状态 | 备注 |
|--------|------|------|
| 单元/集成测试 | ✅ | 通过率 100% |
| CI 失败模式检查 | ✅ | 5 PASS, 2 SKIP |
| 覆盖率 | ⚠️ 72% | curate.py 36%, state.py 35% 需后续补充 |
| 11 类失败模式 | ✅ | 3 项注意，已记录经验 |
| Lint | N/A | 未执行 |

**风险评估**：🟢 低风险。所有核心逻辑路径已通过测试验证，curate.py 的未覆盖部分仅影响维护者工具链（不阻塞普通用户使用）。
