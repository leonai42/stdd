# 技能层版本自检 + Skill-Only 升级路径 — 测试方案与详细案例

> 版本：2.9.5
> 创建日期：2026-06-28
> 对应 Phase 2 Spec：skill-version-self-check, skill-only-upgrade, platform-skill-install

## 一、测试策略

### 1.1 测试金字塔

此变更为 **代码（Python CLI）+ 文档（技能 Markdown）** 混合型：
- **单元测试**（Python）：验证 install.py 的 SKILL_META 和 frontmatter 生成逻辑
- **行为验证**（AI 驱动）：技能文件版本自检行为、升级流程端到端
- **审查**：diff 审查所有修改的技能文件，确保版本号一致性

### 1.2 测试原则

- Python 代码变更必须通过 pytest 单元测试
- 技能 Markdown 变更通过手动/AI 行为验证（AI 按 spec Scenario 逐条执行）
- 跨平台兼容性通过多平台 dry-run install 验证

### 1.3 已有测试资产

| 测试文件 | 用例数 | 类型 | 覆盖范围 |
|----------|--------|------|----------|
| `tests/commands/test_install.py` | 14 | 单元 | install 命令核心逻辑 |
| `tests/commands/test_upgrade.py` | 14 | 单元 | upgrade 命令核心逻辑 |

## 二、详细测试案例

### 功能 1：技能版本自检 (skill-version-self-check)

对应 spec: `specs/skill-version-self-check/spec.md` — REQ-VC-001

#### 案例 1.1 — 版本落后告警

| 字段 | 内容 |
|------|------|
| **ID** | TC-VC-001 |
| **对应 Spec** | skill-version-self-check/spec.md → SC-VC-001 |
| **优先级** | P0 |
| **预置条件** | 项目 `.stdd/version.yaml` 中 `stdd_version: 2.4.0`；技能 SKILL.md frontmatter `stdd_version: 2.9.5` |
| **输入** | 用户调用任意 STDD 阶段技能（如 `/stdd-understand`） |
| **预期结果** | AI 输出明确告警消息，包含："当前项目版本 2.4.0"、"技能版本 2.9.5"、"建议运行 /stdd-upgrade"；技能继续正常执行 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.2 — 版本一致静默

| 字段 | 内容 |
|------|------|
| **ID** | TC-VC-002 |
| **对应 Spec** | skill-version-self-check/spec.md → SC-VC-002 |
| **优先级** | P0 |
| **预置条件** | 项目版本 `2.9.5` = 技能版本 `2.9.5` |
| **输入** | 用户调用任意 STDD 阶段技能 |
| **预期结果** | AI 不输出任何版本告警 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.3 — 项目版本更新时静默

| 字段 | 内容 |
|------|------|
| **ID** | TC-VC-003 |
| **对应 Spec** | skill-version-self-check/spec.md → SC-VC-003 |
| **优先级** | P1 |
| **预置条件** | 项目版本 `3.0.0` > 技能版本 `2.9.5` |
| **输入** | 用户调用任意 STDD 阶段技能 |
| **预期结果** | AI 不输出版本告警 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.4 — 版本格式容错

| 字段 | 内容 |
|------|------|
| **ID** | TC-VC-004 |
| **对应 Spec** | skill-version-self-check/spec.md → SC-VC-004 |
| **优先级** | P0 |
| **预置条件** | 测试矩阵 — (a) 项目 `v2.4` vs 技能 `2.9.5` → 告警 (b) 项目 `2.4.0` vs 技能 `2.9.5` → 告警 (c) 项目 `2.9` vs 技能 `2.9.5` → 告警 (d) 项目 `v2.9.5` vs 技能 `2.9.5` → 静默 |
| **输入** | 逐行执行测试矩阵 |
| **预期结果** | 所有 case 的比较结果正确 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.5 — 非 STDD 项目静默

| 字段 | 内容 |
|------|------|
| **ID** | TC-VC-005 |
| **对应 Spec** | skill-version-self-check/spec.md → SC-VC-005 |
| **优先级** | P1 |
| **预置条件** | 项目根目录无 `.stdd/` 目录 |
| **输入** | 用户调用任意 STDD 阶段技能 |
| **预期结果** | AI 不输出任何版本相关消息 |
| **当前状态** | ❌ 测试缺 |

#### 案例 1.6 — 锁定项目告警

| 字段 | 内容 |
|------|------|
| **ID** | TC-VC-006 |
| **对应 Spec** | skill-version-self-check/spec.md → SC-VC-006 |
| **优先级** | P1 |
| **预置条件** | 项目版本 `2.4.0`、`locked: true`；技能版本 `2.9.5` |
| **输入** | 用户调用任意 STDD 阶段技能 |
| **预期结果** | AI 输出版本落后告警 + "项目已锁定"提示，不阻断执行 |
| **当前状态** | ❌ 测试缺 |

---

### 功能 2：技能升级 (skill-only-upgrade)

对应 spec: `specs/skill-only-upgrade/spec.md` — REQ-UP-001 ~ REQ-UP-004

#### 案例 2.1 — 升级技能入口

| 字段 | 内容 |
|------|------|
| **ID** | TC-UP-001 |
| **对应 Spec** | skill-only-upgrade/spec.md → SC-UP-001 |
| **优先级** | P0 |
| **预置条件** | STDD 已安装到当前平台 |
| **输入** | 用户输入 `/stdd-upgrade` |
| **预期结果** | AI 识别为有效技能并开始执行升级流程 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.2 — 平台检测

| 字段 | 内容 |
|------|------|
| **ID** | TC-UP-002 |
| **对应 Spec** | skill-only-upgrade/spec.md → SC-UP-002, SC-UP-003, SC-UP-004 |
| **优先级** | P0 |
| **预置条件** | (a) Claude Code: `.claude/skills/` 存在 (b) OpenCode: `.opencode/skills/` 存在 (c) 多平台: 两者均存在 |
| **输入** | 在各环境执行升级技能平台检测步骤 |
| **预期结果** | 各 case 检测结果与预期平台匹配；多平台 case 列出所有平台 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.3 — 资源同步

| 字段 | 内容 |
|------|------|
| **ID** | TC-UP-005 |
| **对应 Spec** | skill-only-upgrade/spec.md → SC-UP-005, SC-UP-006, SC-UP-007 |
| **优先级** | P0 |
| **预置条件** | 网络可达 GitHub raw；项目 `.stdd/` 为旧版本 |
| **输入** | 执行 `/stdd-upgrade` |
| **预期结果** | `.stdd/skills/` 文件全部更新；`.stdd/config.d/` 更新且 `project.yaml` 保留项目标识；`.stdd/templates/` 全部更新 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.4 — 网络降级

| 字段 | 内容 |
|------|------|
| **ID** | TC-UP-008 |
| **对应 Spec** | skill-only-upgrade/spec.md → SC-UP-008 |
| **优先级** | P1 |
| **预置条件** | 模拟 GitHub raw 不可达 |
| **输入** | 执行 `/stdd-upgrade` |
| **预期结果** | AI 提示网络错误 + 提供手动下载 URL 和步骤 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.5 — 版本文件更新

| 字段 | 内容 |
|------|------|
| **ID** | TC-UP-009 |
| **对应 Spec** | skill-only-upgrade/spec.md → SC-UP-009 |
| **优先级** | P0 |
| **预置条件** | 源版本 `2.9.5`，项目版本 `2.4.0`，资源同步完成 |
| **输入** | 升级流程写入版本信息 |
| **预期结果** | `.stdd/version.yaml` 中 `stdd_version: 2.9.5`，`upgraded_at` 为当前时间 |
| **当前状态** | ❌ 测试缺 |

#### 案例 2.6 — 平台重装

| 字段 | 内容 |
|------|------|
| **ID** | TC-UP-010 |
| **对应 Spec** | skill-only-upgrade/spec.md → SC-UP-010 |
| **优先级** | P0 |
| **预置条件** | 平台 `claude-code`，源版本 `2.9.5`，资源同步完成 |
| **输入** | 升级流程执行平台重装 |
| **预期结果** | `.claude/skills/stdd-*/SKILL.md` frontmatter 均含 `stdd_version: "2.9.5"` |
| **当前状态** | ❌ 测试缺 |

---

### 功能 3：install.py 修改 (platform-skill-install)

对应 spec: `specs/platform-skill-install/spec.md` — REQ-PSI-001

#### 案例 3.1 — SKILL_META 扩展

| 字段 | 内容 |
|------|------|
| **ID** | TC-PSI-001 |
| **对应 Spec** | platform-skill-install/spec.md → SC-PSI-001 |
| **优先级** | P0 |
| **预置条件** | STDD 源码 `.stdd/skills/upgrade.md` 存在 |
| **输入** | 执行 `stdd install claude-code` |
| **预期结果** | `SKILL_META["upgrade"]` 存在且字段完整；`stdd-upgrade/SKILL.md` 出现在安装目标 |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.2 — frontmatter 版本号注入

| 字段 | 内容 |
|------|------|
| **ID** | TC-PSI-002 |
| **对应 Spec** | platform-skill-install/spec.md → SC-PSI-002 |
| **优先级** | P0 |
| **预置条件** | STDD 源版本 `2.9.5` |
| **输入** | 执行 `stdd install claude-code`，读取生成的任意 SKILL.md |
| **预期结果** | YAML frontmatter 包含 `stdd_version: "2.9.5"` |
| **当前状态** | ❌ 测试缺 |

#### 案例 3.3 — 跨平台一致性

| 字段 | 内容 |
|------|------|
| **ID** | TC-PSI-003 |
| **对应 Spec** | platform-skill-install/spec.md → SC-PSI-003 |
| **优先级** | P0 |
| **预置条件** | 6 个已支持平台 |
| **输入** | 对每个平台执行 `stdd install <platform> --dry-run` |
| **预期结果** | upgrade 技能出现在每个平台的安装输出中 |
| **当前状态** | ❌ 测试缺 |

## 三、测试执行矩阵

| 功能模块 | 单元测试 | 行为验证 | 审查 | 状态 |
|----------|---------|----------|------|------|
| version-check.md 片段 | — | TC-VC-001~006 | ✅ diff review | 🟡 待实现 |
| upgrade.md 技能 | — | TC-UP-001,002,005,008,009,010 | ✅ diff review | 🟡 待实现 |
| install.py 修改 | TC-PSI-001~003 | — | ✅ diff review | 🟡 待实现 |

## 四、回归风险矩阵

| 风险区域 | V2.9.5 改动 | 已有回归保护 | 风险等级 |
|----------|-------------|-------------|---------|
| 现有 phase skill 行为 | 各文件头部新增 Step 0 版本自检引用 | 手动验证所有 phase 仍正常执行 | 🟡 中 |
| install.py | 新增 upgrade meta + frontmatter 版本号注入 | `tests/commands/test_install.py` (14 cases) | 🟢 低 |
| upgrade CLI | 无改动 | `tests/commands/test_upgrade.py` (14 cases) | 🟢 低 |
| _shared/ 目录 | 新增 version-check.md | 确认不影响现有 confirm-gate.md | 🟢 低 |

## 五、建议补充顺序

1. **第一优先**（开发阶段必过）：TC-PSI-001~003（单元测试）、TC-VC-001~004（版本自检行为验证）
2. **第二优先**（合并前必过）：TC-UP-001,002,005,009,010（升级流程端到端）
3. **第三优先**（后续补）：TC-VC-005~006（边界场景）、TC-UP-008（网络降级）
