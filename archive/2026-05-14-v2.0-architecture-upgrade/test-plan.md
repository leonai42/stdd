# V2.0 测试方案与详细案例

> 版本：V2.0
> 创建日期：2026-05-14
> 对应 Phase 2 Spec：specs/cli/spec.md, specs/skill/spec.md, specs/state/spec.md, specs/validate/spec.md, specs/abort/spec.md, specs/docs/spec.md

## 一、测试策略

### 1.1 测试金字塔

V2.0 首次为 CLI 引入自动化测试（pytest）。测试金字塔：
- **单元测试（60%）**：每个命令模块的独立函数测试
- **集成测试（30%）**：CLI 命令端到端测试（用 tmp_path 隔离文件系统）
- **手动验证（10%）**：文档内容、Skill 格式等需人工判断的项

### 1.2 测试原则

- 每个 Spec Scenario 至少对应 1 个测试案例
- CLI 命令测试使用 pytest tmp_path fixture 隔离文件系统
- 向后兼容：已有 change 目录操作不受影响

## 二、详细测试案例

### 功能 1：CLI 模块化拆分

#### 案例 1.1 — bin/stdd 入口兼容性

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-101 |
| **对应 Spec** | cli/spec.md → Scenario: bin/stdd 入口保持兼容 |
| **优先级** | P0 |
| **预置条件** | 拆分后代码部署完成 |
| **输入** | `python bin/stdd --help` |
| **预期结果** | 输出与拆分前一致；退出码 0 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.2 — 子命令模块可独立测试

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-102 |
| **对应 Spec** | cli/spec.md → Scenario: 子命令模块可独立导入测试 |
| **优先级** | P0 |
| **预置条件** | 拆分后代码 |
| **输入** | `from stdd.cli.commands.init import cmd_init` |
| **预期结果** | 导入成功，函数有完整类型注解 |
| **当前状态** | ❌ 测试缺 |

### 功能 2：--dry-run

#### 案例 2.1 — dry-run archive

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-103 |
| **对应 Spec** | cli/spec.md → Scenario: dry-run 模式预览 archive |
| **优先级** | P1 |
| **预置条件** | change 目录存在 |
| **输入** | `stdd --dry-run archive test --yes` |
| **预期结果** | 输出操作步骤；文件系统无变化 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.2 — dry-run init

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-104 |
| **对应 Spec** | cli/spec.md → Scenario: dry-run 模式预览 init |
| **优先级** | P2 |
| **预置条件** | 未初始化目录 |
| **输入** | `stdd --dry-run init` |
| **预期结果** | 列出将创建的文件和目录 |
| **当前状态** | ❌ 测试缺 |

### 功能 3：--verbose

#### 案例 3.1 — 默认简洁输出

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-105 |
| **对应 Spec** | cli/spec.md → Scenario: 默认输出简洁 |
| **优先级** | P2 |
| **预置条件** | 有效 change |
| **输入** | `stdd status` |
| **预期结果** | 仅输出状态信息，无 DEBUG 日志 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.2 — -v 详细输出

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-106 |
| **对应 Spec** | cli/spec.md → Scenario: -v 输出详细信息 |
| **优先级** | P2 |
| **预置条件** | 有效 change |
| **输入** | `stdd -v validate` |
| **预期结果** | 输出检查步骤详情 |
| **当前状态** | ❌ 测试缺 |

### 功能 4：rollback

#### 案例 4.1 — 成功恢复

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-107 |
| **对应 Spec** | cli/spec.md → Scenario: 成功恢复已归档 |
| **优先级** | P1 |
| **预置条件** | archive 中存在目标 change，changes/ 中无同名 |
| **输入** | `stdd rollback my-feature` |
| **预期结果** | 目录移回 changes/；状态更新为 active |
| **当前状态** | ❌ 测试缺 |

#### 案例 4.2 — 冲突拒绝

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-108 |
| **对应 Spec** | cli/spec.md → Scenario: 目标已存在时拒绝恢复 |
| **优先级** | P1 |
| **预置条件** | archive 和 changes/ 下均存在同名目录 |
| **输入** | `stdd rollback my-feature` |
| **预期结果** | 报告冲突；非零退出 |
| **当前状态** | ❌ 测试缺 |

### 功能 5：diff

#### 案例 5.1 — 正常覆盖差异

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-109 |
| **对应 Spec** | cli/spec.md → Scenario: diff 显示覆盖差异表 |
| **优先级** | P1 |
| **预置条件** | change 含 test-plan.md，源码含 TC-ID 引用 |
| **输入** | `stdd diff my-change` |
| **预期结果** | 四列对照表，未覆盖标注 ❌ |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.2 — 无 test-plan

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-110 |
| **对应 Spec** | cli/spec.md → Scenario: 无 test-plan 的 change |
| **优先级** | P2 |
| **预置条件** | change 目录无 test-plan.md |
| **输入** | `stdd diff my-change` |
| **预期结果** | 报告"无 test-plan"；非零退出 |
| **当前状态** | ❌ 测试缺 |

### 功能 6：CLI 单元测试

#### 案例 6.1 — 测试覆盖率达标

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-111 |
| **对应 Spec** | cli/spec.md（测试框架） |
| **优先级** | P0 |
| **预置条件** | 测试文件编写完成 |
| **输入** | `pytest tests/ --cov=stdd --cov-report=term` |
| **预期结果** | 覆盖率 ≥ 70%；全部通过 |
| **当前状态** | ❌ 测试缺 |

### 功能 7：Skill 自动同步

#### 案例 7.1 — Claude Code install 同步

| 字段 | 内容 |
|------|------|
| **ID** | TC-SKILL-001 |
| **对应 Spec** | skill/spec.md → Scenario: install 从核心生成 Claude Code |
| **优先级** | P0 |
| **预置条件** | 核心 Skill 已更新 |
| **输入** | `stdd install claude-code` |
| **预期结果** | 生成的 Skill 内容与核心一致；frontmatter 含 name/description |
| **当前状态** | ❌ 测试缺 |

#### 案例 7.2 — WorkBuddy install 同步

| 字段 | 内容 |
|------|------|
| **ID** | TC-SKILL-002 |
| **对应 Spec** | skill/spec.md → Scenario: install 从核心生成 WorkBuddy |
| **优先级** | P1 |
| **预置条件** | 核心 Skill 已更新 |
| **输入** | `stdd install workbuddy` |
| **预期结果** | 生成的 Skill 含 trigger_keywords frontmatter |
| **当前状态** | ❌ 测试缺 |

### 功能 8：Skill DRY

#### 案例 8.1 — 确认消息模板集中

| 字段 | 内容 |
|------|------|
| **ID** | TC-SKILL-003 |
| **对应 Spec** | skill/spec.md → Scenario: 确认门消息模板集中维护 |
| **优先级** | P2 |
| **预置条件** | _shared/ 目录存在 |
| **输入** | 检查 understand/spec/verify 中确认模板 |
| **预期结果** | 三处引用同一 _shared/confirm-gate.md |
| **当前状态** | ❌ 测试缺 |

### 功能 9：配置拆分

#### 案例 9.1 — config.d/ 优先

| 字段 | 内容 |
|------|------|
| **ID** | TC-STATE-001 |
| **对应 Spec** | state/spec.md → Scenario: config.d/ 优先于 config.yaml |
| **优先级** | P0 |
| **预置条件** | 两者都存在 |
| **输入** | 读取配置 |
| **预期结果** | 以 config.d/ 为准；提示删除旧 config.yaml |
| **当前状态** | ❌ 测试缺 |

#### 案例 9.2 — 旧项目兼容

| 字段 | 内容 |
|------|------|
| **ID** | TC-STATE-002 |
| **对应 Spec** | state/spec.md → Scenario: 旧项目 config.yaml 向后兼容 |
| **优先级** | P0 |
| **预置条件** | 仅有 config.yaml |
| **输入** | 读取配置 |
| **预期结果** | 正常读取，所有配置项可用 |
| **当前状态** | ❌ 测试缺 |

### 功能 10：长程模式退出

#### 案例 10.1 — 中途降级

| 字段 | 内容 |
|------|------|
| **ID** | TC-STATE-003 |
| **对应 Spec** | state/spec.md → Scenario: Phase 4 中途退出长程 |
| **优先级** | P2 |
| **预置条件** | 长程模式执行中 |
| **输入** | 用户输入"切换普通模式" |
| **预期结果** | mode 更新为 normal；当前切片完成后暂停 |
| **当前状态** | ❌ 测试缺（Skill 层面验证） |

### 功能 11：validate AND 检查

#### 案例 11.1 — AND 合规

| 字段 | 内容 |
|------|------|
| **ID** | TC-VAL-001 |
| **对应 Spec** | validate/spec.md → Scenario: AND 数量合规 |
| **优先级** | P2 |
| **预置条件** | spec Scenario 含 3 条 AND |
| **输入** | `stdd validate` |
| **预期结果** | 无 AND 相关警告 |
| **当前状态** | ❌ 测试缺 |

#### 案例 11.2 — AND 超限警告

| 字段 | 内容 |
|------|------|
| **ID** | TC-VAL-002 |
| **对应 Spec** | validate/spec.md → Scenario: AND 数量超限 |
| **优先级** | P2 |
| **预置条件** | spec Scenario 含 6 条 AND |
| **输入** | `stdd validate` |
| **预期结果** | 报告 AND 超限警告 |
| **当前状态** | ❌ 测试缺 |

### 功能 12：trace 重构

#### 案例 12.1 — 标准格式解析

| 字段 | 内容 |
|------|------|
| **ID** | TC-VAL-003 |
| **对应 Spec** | validate/spec.md → Scenario: 标准格式正确解析 |
| **优先级** | P1 |
| **预置条件** | test-plan.md 符合模板 |
| **输入** | `stdd trace TC-XXX-001` |
| **预期结果** | 提取 TC-ID、标题、预期结果 |
| **当前状态** | ❌ 测试缺 |

### 功能 13：archive 冲突检测

#### 案例 13.1 — 重复 Requirement 警告

| 字段 | 内容 |
|------|------|
| **ID** | TC-VAL-004 |
| **对应 Spec** | validate/spec.md → Scenario: 检测到重复 Requirement |
| **优先级** | P1 |
| **预置条件** | specs/ 中已存在同名 Requirement |
| **输入** | `stdd archive my-change --yes` |
| **预期结果** | 输出冲突警告；标注冲突 Requirement |
| **当前状态** | ❌ 测试缺 |

### 功能 14：abort

#### 案例 14.1 — CLI abort 成功

| 字段 | 内容 |
|------|------|
| **ID** | TC-ABORT-001 |
| **对应 Spec** | abort/spec.md → Scenario: CLI 执行 abort |
| **优先级** | P1 |
| **预置条件** | change 目录存在 |
| **输入** | `stdd abort experiment --yes` |
| **预期结果** | 移至 archive/aborted/；退出码 0 |
| **当前状态** | ❌ 测试缺 |

### 功能 15：文档

#### 案例 15.1 — CHANGELOG 完整性

| 字段 | 内容 |
|------|------|
| **ID** | TC-DOCS-001 |
| **对应 Spec** | docs/spec.md → Scenario: CHANGELOG 包含完整版本历史 |
| **优先级** | P2 |
| **预置条件** | 无 |
| **输入** | 检查 CHANGELOG.md |
| **预期结果** | 含 V1.0-V2.0 各版本条目 |
| **当前状态** | ❌ 测试缺 |

#### 案例 15.2 — TROUBLESHOOTING 覆盖

| 字段 | 内容 |
|------|------|
| **ID** | TC-DOCS-002 |
| **对应 Spec** | docs/spec.md → Scenario: 覆盖至少 5 个常见问题 |
| **优先级** | P2 |
| **预置条件** | 无 |
| **输入** | 检查 TROUBLESHOOTING.md |
| **预期结果** | ≥5 个问题；每个有症状+方案 |
| **当前状态** | ❌ 测试缺 |

#### 案例 15.3 — 示例项目可初始化

| 字段 | 内容 |
|------|------|
| **ID** | TC-DOCS-003 |
| **对应 Spec** | docs/spec.md → Scenario: 示例项目可独立初始化 |
| **优先级** | P2 |
| **预置条件** | 无 |
| **输入** | 在 examples/hello-stdd/ 执行 `python ../../bin/stdd init` |
| **预期结果** | 成功初始化 |
| **当前状态** | ❌ 测试缺 |

## 三、测试执行矩阵

| 功能模块 | 自动化 | 手动 | 状态 |
|----------|--------|------|------|
| CLI 模块化 (2 cases) | ✅ pytest | — | 🟡 |
| dry-run/verbose (4 cases) | ✅ pytest | — | 🟡 |
| rollback/diff (4 cases) | ✅ pytest | — | 🟡 |
| CLI 测试覆盖率 (1 case) | ✅ pytest-cov | — | 🟡 |
| Skill 同步 (2 cases) | ✅ pytest | — | 🟡 |
| Skill DRY (1 case) | — | ✅ 内容检查 | 🟡 |
| 配置拆分 (2 cases) | ✅ pytest | — | 🟡 |
| 长程退出 (1 case) | — | ✅ Skill | 🟡 |
| validate 增强 (2 cases) | ✅ pytest | — | 🟡 |
| trace 重构 (1 case) | ✅ pytest | — | 🟡 |
| archive 冲突 (1 case) | ✅ pytest | — | 🟡 |
| abort (1 case) | ✅ pytest | — | 🟡 |
| 文档 (3 cases) | — | ✅ 内容检查 | 🟡 |

## 四、回归风险矩阵

| 风险区域 | V2.0 改动 | 已有回归保护 | 风险等级 |
|----------|----------|-------------|---------|
| CLI 入口 | bin/stdd 委托到包 | 集成测试 | 🟡 中 |
| 现有 7 个命令 | 代码移动无逻辑变更 | 单元+集成测试 | 🟢 低 |
| 配置读取 | 单文件→多文件 | 兼容性测试 | 🟡 中 |
| Skill 安装 | 生成方式变更 | 手动验证 | 🟡 中 |
| 已有 change 目录 | 无改动 | 手动验证 | 🟢 低 |

## 五、建议补充顺序

1. **第一优先**（P0）：CLI 模块化 + 测试覆盖率 + Skill 同步 + 配置拆分 — 架构基础
2. **第二优先**（P1）：dry-run + rollback + diff + trace + archive 冲突 + abort — 功能补全
3. **第三优先**（P2）：其余 — 体验和文档
