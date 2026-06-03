# V2.8 测试方案

## 关键 TCs

| ID | 模块 | 场景 | 优先级 |
|----|------|------|:---:|
| TC-PASSK-001 | fix.py | k=3 全部通过 | P0 |
| TC-PASSK-002 | fix.py | pass@1低/pass@3高→歧义检测 | P0 |
| TC-FIX-001 | fix.py | L1 ruff+isort 生效 | P0 |
| TC-FIX-002 | fix.py | L2 检测类型注解缺失 | P1 |
| TC-FIX-003 | fix.py | L3 报告不自动修改 | P1 |
| TC-PAR-001 | new.py | --parallel 创建 worktree | P1 |
| TC-RULE-001 | rules | 目录结构 + auto-load | P1 |
| TC-SKIL-003 | skill | 5 个 Skill 内容完整 | P1 |
| TC-CSUM-004 | structure | delta/merge/rebuild 非 TODO | P0 |
| TC-COV-B1 | state | state_freshness 完整路径 | P0 |
| TC-COV-B2 | canon | verify DC-HASH mismatch | P0 |
| TC-COV-B4 | experience | provenance filter | P0 |
| TC-COV-B5 | ci | check_tc_implementation_coverage | P0 |
| TC-COV-B6 | proposal | show + validate error path | P1 |
| TC-COV-B8 | agent | dry-run boundary | P1 |

## 覆盖目标

| 模块 | 当前 | 目标 |
|------|:---:|:---:|
| state.py | 48% | 80% |
| canon.py | 60% | 80% |
| index.py | 50% | 75% |
| experience.py | 72% | 80% |
| ci.py | 74% | 82% |
| proposal.py | 76% | 85% |
| agent.py | 35% | 55% |
| trace.py | 73% | 85% |
