# STDD V2.8-patch1：覆盖测试补齐 + P2 流程改进

> Gate 1 ✅ | 9 项 / 2 板块 | 基线 V2.8-beta (221 tests / 73%)

## Why

V2.8-beta 核心新功能已完成，剩余 5 个模块的覆盖率未达目标，4 项 P2 流程改进未实施。

## What Changes

- B4: experience.py 73%→80%
- B5: ci.py 79%→82%
- B6: proposal.py 覆盖提升
- B8: agent.py 42%→55%
- B9: trace.py 74%→85%
- C1: build.md 并行切片合并验证
- C2: design-adjustments 模板增加"影响 TC"
- C3: phase-context.md 自动生成指令
- C4: verify.md 非代码 change 检测

## Success Criteria

- [ ] 5 模块覆盖目标达标
- [ ] C1-C4 模板/skill 修改完成
- [ ] 221 现有测试全部通过，新增 10+ 测试
- [ ] 总覆盖率 ≥75%
