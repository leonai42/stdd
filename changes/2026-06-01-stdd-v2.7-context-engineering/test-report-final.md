# STDD V2.7 — 最终测试报告

> 日期：2026-06-03 | 版本：V2.7（完整交付）  
> 测试轮次：2 轮（Round 1: Verbose / Round 2: Coverage）  
> 测试标准：pytest + pytest-cov

---

## 一、测试执行摘要

| 指标 | Round 1 | Round 2 | 一致性 |
|------|:---:|:---:|:---:|
| 总测试数 | 164 | 164 | ✅ |
| 通过 | 164 | 164 | ✅ |
| 失败 | 0 | 0 | ✅ |
| 错误 | 0 | 0 | ✅ |
| 耗时 | 3.72s | 7.15s | — |
| 覆盖率 | — | 66% | — |
| Python 版本 | 3.12.7 | 3.12.7 | ✅ |

**结论：两轮测试 100% 一致，164/164 通过，零失败。**

---

## 二、覆盖率分析

### 2.1 总体覆盖

| 指标 | 数值 |
|------|------|
| 总语句 | 3,024 |
| 已覆盖 | 2,006 |
| 未覆盖 | 1,018 |
| 覆盖率 | **66%** |

### 2.2 按模块分组

#### 🟢 高覆盖 (≥90%)

| 模块 | 语句 | 覆盖 | 说明 |
|------|:---:|:---:|------|
| new.py | 50 | 100% | ✅ 完美 |
| rollback.py | 60 | 97% | ✅ |
| validate.py | 82 | 95% | ✅ |
| finder.py | 22 | 95% | ✅ |
| dependency_graph.py | 122 | 94% | ✅ |
| diff.py | 95 | 94% | ✅ |
| utils.py | 59 | 93% | ✅ |
| init.py | 67 | 91% | ✅ |
| install.py | 92 | 91% | ✅ |
| extract_proposal.py | 87 | 91% | ✅ |
| status.py | 51 | 90% | ✅ |
| gate.py | 82 | 89% | ✅ |

#### 🟡 中覆盖 (60-89%)

| 模块 | 覆盖 | 未覆盖主要区域 |
|------|:---:|------|
| ci.py | 74% | curate/pack 子命令 |
| proposal.py | 76% | show 命令 |
| experience.py | 72% | curate 子命令、pull 网络逻辑 |
| trace.py | 73% | 边界情况 |
| archive.py | 68% | 冲突处理 |

#### 🟠 待提升 (30-59%)

| 模块 | 覆盖 | 原因 |
|------|:---:|------|
| canon.py | 60% | generate/verify 完整流程未测试 |
| index.py | 50% | trace/show 边界情况 |
| state.py | 48% | V2.7 新增 state_freshness 逻辑未测试 |
| agent.py | 35% | subprocess 执行路径未测试 |
| curate.py | 36% | 网络相关子命令 |

#### 🔴 零覆盖（V2.7 新增，待补测试）

| 模块 | 语句 | 说明 |
|------|:---:|------|
| hooks.py | 53 | V2.7 新增 — 需测试 install/status/uninstall |
| skill.py | 24 | V2.7 新增 — 需测试 create 命令 |
| structure.py | 25 | V2.7 新增 — 需测试骨架命令 |
| cli/__init__.py | 169 (4%) | 主入口 parser — 低覆盖正常 |

---

## 三、功能验证矩阵

| 功能域 | 测试文件 | 用例数 | 状态 | 覆盖状态 |
|--------|---------|:---:|:---:|:---:|
| 初始化 | test_init.py | 3 | ✅ | ✅ |
| 创建 Change | test_new.py | 5 | ✅ | ✅ |
| 校验 | test_validate.py | 8 | ✅ | ✅ |
| 状态管理 | test_state.py | 4 | ✅ | ⚠️ V2.7 新逻辑待补 |
| Gate 确认 | test_gate.py | 7 | ✅ | ✅ |
| 归档 | test_archive.py | 4 | ✅ | ✅ |
| 回滚 | test_rollback.py | 5 | ✅ | ✅ |
| 放弃 | test_abort.py | 4 | ✅ | ✅ |
| 状态查询 | test_status.py | 4 | ✅ | ✅ |
| 追溯 | test_trace.py | 4 | ✅ | ✅ |
| Diff | test_diff.py | 5 | ✅ | ✅ |
| CI 检查 | test_ci.py | 23 | ✅ | ✅ |
| 安装 | test_install.py | 6 | ✅ | ✅ |
| 经验库 | test_experience.py | 31 | ✅ | ✅ |
| 依赖图 | test_dependency_graph.py | 10 | ✅ | ✅ |
| 提案提取 | test_extract_proposal.py | 13 | ✅ | ✅ |
| 社区维护 | test_curate.py | 3 | ✅ | ⚠️ |
| **V2.7 新增** | test_canon.py | 9 | ✅ | ✅ |
| **V2.7 新增** | hooks.py | — | 0 | ❌ 待补 |
| **V2.7 新增** | skill.py | — | 0 | ❌ 待补 |
| **V2.7 新增** | structure.py | — | 0 | ❌ 待补 |
| 工具函数 | test_utils.py | 8 | ✅ | ✅ |
| 文件查找 | test_finder.py | 8 | ✅ | ✅ |

---

## 四、失败模式检查结果（12 类）

| ID | 检查项 | 类型 | Round 1 | Round 2 |
|----|--------|------|:---:|:---:|
| (a) | 文件存在性 | CLI | ✅ | ✅ |
| (b) | 范围蔓延 | CLI | ✅ | ✅ |
| (c) | 级联错误 | CLI | ✅ | ✅ |
| (d) | TC-ID 唯一性 | CLI | ✅ | ✅ |
| (e) | — | — | — | — |
| (f) | SHALL 关键字 | CLI | ✅ | ✅ |
| (g) | AND 数量 | CLI | ✅ | ✅ |
| (h) | — | — | — | — |
| (i) | — | — | — | — |
| (j) | 覆盖率检测 | CLI | ✅ | ✅ |
| (k) | 契约一致性 | CLI | ✅ | ✅ |
| (l) | 锚定缺失 | CLI | ✅ | ✅ |
| TC实现覆盖 | test-plan vs 实际 | CLI | ✅ | ✅ |
| 切片完成 | 进度验证 | CLI | ✅ | ✅ |

---

## 五、已知问题与改进建议

### 5.1 零覆盖模块（V2.7 遗留）

| 模块 | 优先级 | 建议 |
|------|:---:|------|
| hooks.py | P1 | 新增 test_hooks.py（install/status/uninstall） |
| skill.py | P1 | 新增 test_skill.py（create 命令） |
| structure.py | P2 | 新增 test_structure.py（V2.8 实现后） |

### 5.2 覆盖不足模块

| 模块 | 当前 | 目标 | 关键未覆盖路径 |
|------|:---:|:---:|------|
| state.py | 48% | 80% | state_freshness 检查 + --resume 新输出 |
| agent.py | 35% | 70% | CP 执行 + 断言验证 |
| canon.py | 60% | 80% | generate --all + verify 完整路径 |
| index.py | 50% | 75% | trace + show 边界情况 |

### 5.3 测试环境限制

| 限制 | 影响模块 | 说明 |
|------|---------|------|
| 无网络环境 | experience.py pull | 社区经验池下载无法测试 |
| 无 Docker | agent.py | CP 执行器需真实 shell 环境 |
| Windows CRLF | 全部 | 文件写入测试需关注行尾 |

---

## 六、结论

**V2.7 测试状态：✅ 通过**

- 两轮测试 164/164 全部通过，结果一致
- 总体覆盖率 66%，核心模块覆盖良好（12 个模块 ≥90%）
- V2.7 新增 9 个测试（test_canon.py），覆盖 5 个新 CLI 命令
- 3 个新 CLI 模块（hooks/skill/structure）待补测试，规划到 V2.8

**建议**：V2.8 中补全 hooks/skill/structure 测试，将总体覆盖率提升到 75%+。
