# V1.2.1+V1.3 测试方案与详细案例

> 版本：V1.2.1+V1.3
> 创建日期：2026-05-14
> 对应 Phase 2 Spec：specs/cli/spec.md, specs/state/spec.md, specs/template/spec.md

## 一、测试策略

### 1.1 测试金字塔

本次变更以手动集成测试为主（CLI 端到端行为验证），辅以文件内容检查（模板、配置）。原因：
- CLI 命令的输入输出是核心验证目标，当前无自动化测试框架
- 大部分变更为已有逻辑的修正，回归风险低
- CLI 自动化测试框架待 V2.0 引入

### 1.2 测试原则

- 每个 Spec Scenario 至少对应 1 个测试案例
- Bug 修复案例验证"修复前行为已消除 + 修复后行为符合预期"
- 向后兼容案例：已有 change 目录操作不受影响

### 1.3 已有测试资产

| 测试文件 | 用例数 | 类型 | 覆盖范围 |
|----------|--------|------|----------|
| 无 | 0 | — | CLI 当前零测试覆盖 |

## 二、详细测试案例

### 功能 1：archive 目录名修复

#### 案例 1.1 — archive 使用完整日期目录名

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-001 |
| **对应 Spec** | cli/spec.md → Scenario: 用户使用短名称归档 change |
| **优先级** | P0 |
| **预置条件** | changes/2026-05-14-test-fix/ 存在，含有效 .stdd.yaml |
| **输入** | `python bin/stdd archive test-fix --yes` |
| **预期结果** | 归档目录为 archive/2026-05-14-test-fix/（含日期前缀）；原 changes/ 下目录已删除 |
| **当前状态** | ❌ 测试缺（修复前归档到 archive/test-fix/） |

#### 案例 1.2 — archive 操作顺序：合并失败时保护源目录

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-002 |
| **对应 Spec** | cli/spec.md → Scenario: specs 合并失败时保护源目录 |
| **优先级** | P0 |
| **预置条件** | change 目录存在，specs/ 父目录设为只读（模拟合并失败） |
| **输入** | `python bin/stdd archive test-fix --yes` |
| **预期结果** | 报告合并失败；change 目录保持在 changes/；以非零退出码退出 |
| **当前状态** | ❌ 测试缺 |

### 功能 2：validate 正则逻辑修复

#### 案例 2.1 — 多 GIVEN（AND）不产生误报

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-003 |
| **对应 Spec** | cli/spec.md → Scenario: 一个 Scenario 有多个 GIVEN |
| **优先级** | P0 |
| **预置条件** | spec 文件包含 1 个 Scenario、2 个 GIVEN、1 个 WHEN、1 个 THEN |
| **输入** | `python bin/stdd validate` |
| **预期结果** | 不报告 GIVEN 不匹配警告；如无其他问题则显示验证通过 |
| **当前状态** | ❌ 测试缺（修复前误报告警） |

#### 案例 2.2 — 缺少 GIVEN 时正确报警

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-004 |
| **对应 Spec** | cli/spec.md → Scenario: Scenario 缺少 GIVEN |
| **优先级** | P1 |
| **预置条件** | spec 文件包含 1 个 Scenario、0 个 GIVEN |
| **输入** | `python bin/stdd validate` |
| **预期结果** | 报告 GIVEN 数量少于 Scenario 数量的警告 |
| **当前状态** | ❌ 测试缺 |

### 功能 3：trace 搜索范围扩展

#### 案例 3.1 — trace 搜索主 specs/ 目录

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-005 |
| **对应 Spec** | cli/spec.md → Scenario: TC-ID 存在于主 specs/ 目录 |
| **优先级** | P1 |
| **预置条件** | specs/test-plan.md 包含 TC-TEST-001，changes/ 中无此 TC-ID |
| **输入** | `python bin/stdd trace TC-TEST-001` |
| **预期结果** | 找到并显示 TC-TEST-001 的追溯信息 |
| **当前状态** | ❌ 测试缺（修复前仅搜索 changes/） |

### 功能 4：init --force 选项

#### 案例 4.1 — --force 覆盖已存在文件

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-006 |
| **对应 Spec** | cli/spec.md → Scenario: 使用 --force 覆盖已存在文件 |
| **优先级** | P1 |
| **预置条件** | 项目已初始化，模板文件已存在 |
| **输入** | `python bin/stdd init --force` |
| **预期结果** | 模板文件被覆盖为 STDD 源版本；提示文件已更新 |
| **当前状态** | ❌ 测试缺 |

#### 案例 4.2 — 默认行为不覆盖

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-007 |
| **对应 Spec** | cli/spec.md → Scenario: 默认行为保持静默跳过 |
| **优先级** | P1 |
| **预置条件** | 项目已初始化，模板文件已存在且内容不同于源 |
| **输入** | `python bin/stdd init`（不带 --force） |
| **预期结果** | 已存在文件保持原有内容不变 |
| **当前状态** | ❌ 测试缺 |

### 功能 5：new 格式验证

#### 案例 5.1 — 合法名称通过

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-008 |
| **对应 Spec** | cli/spec.md → Scenario: 合法的 change_name |
| **优先级** | P1 |
| **预置条件** | 无同名 change 目录 |
| **输入** | `python bin/stdd new fix-login-bug` |
| **预期结果** | 正常创建 changes/<today>-fix-login-bug/（回归验证） |
| **当前状态** | ✅ 已有行为，验证不退化 |

#### 案例 5.2 — 含空格名称被拒绝

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-009 |
| **对应 Spec** | cli/spec.md → Scenario: 包含空格的 change_name |
| **优先级** | P1 |
| **预置条件** | 无 |
| **输入** | `python bin/stdd new "fix login bug"` |
| **预期结果** | 报告格式错误；以非零退出码退出 |
| **当前状态** | ❌ 测试缺 |

#### 案例 5.3 — 含特殊字符被拒绝

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-010 |
| **对应 Spec** | cli/spec.md → Scenario: 包含特殊字符的 change_name |
| **优先级** | P2 |
| **预置条件** | 无 |
| **输入** | `python bin/stdd new feature/rate-limit` |
| **预期结果** | 报告格式错误；以非零退出码退出 |
| **当前状态** | ❌ 测试缺 |

### 功能 6：install 源文件检查

#### 案例 6.1 — 源文件不存在时报告错误

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-011 |
| **对应 Spec** | cli/spec.md → Scenario: 平台源文件不存在 |
| **优先级** | P2 |
| **预置条件** | 目标平台的 skills 源目录不存在 |
| **输入** | `python bin/stdd install unsupported-platform` |
| **预期结果** | 报告源文件/平台不支持错误；以非零退出码退出 |
| **当前状态** | ❌ 测试缺 |

#### 案例 6.2 — 源文件存在时正常安装

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-012 |
| **对应 Spec** | cli/spec.md → Scenario: 平台源文件存在 |
| **优先级** | P2 |
| **预置条件** | .stdd/platforms/claude-code/skills/ 目录存在 |
| **输入** | `python bin/stdd install claude-code` |
| **预期结果** | 正常安装 skills；报告安装数量（回归验证） |
| **当前状态** | ✅ 已有行为，验证不退化 |

### 功能 7：status 显示模式

#### 案例 7.1 — 长程模式显示

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-013 |
| **对应 Spec** | cli/spec.md → Scenario: 长程模式状态显示 |
| **优先级** | P2 |
| **预置条件** | .stdd.yaml 中 `long_range.mode: full_auto` |
| **输入** | `python bin/stdd status` |
| **预期结果** | 显示"🚀 全自动长程模式" |
| **当前状态** | ❌ 测试缺 |

#### 案例 7.2 — 未设置模式显示默认

| 字段 | 内容 |
|------|------|
| **ID** | TC-CLI-014 |
| **对应 Spec** | cli/spec.md → Scenario: 未设置模式时显示默认 |
| **优先级** | P2 |
| **预置条件** | .stdd.yaml 中无 long_range 字段 |
| **输入** | `python bin/stdd status` |
| **预期结果** | 显示"📋 普通交互模式（默认）" |
| **当前状态** | ❌ 测试缺 |

### 功能 8：.stdd.yaml version 字段

#### 案例 8.1 — 新建 change 带 version

| 字段 | 内容 |
|------|------|
| **ID** | TC-STATE-001 |
| **对应 Spec** | state/spec.md → Scenario: 新建 change 生成带 version 的状态文件 |
| **优先级** | P0 |
| **预置条件** | 无 |
| **输入** | `python bin/stdd new version-test` |
| **预期结果** | 生成的 .stdd.yaml 包含 `version: "1.2"` |
| **当前状态** | ❌ 测试缺 |

#### 案例 8.2 — 旧格式兼容（无 version 字段不报错）

| 字段 | 内容 |
|------|------|
| **ID** | TC-STATE-002 |
| **对应 Spec** | state/spec.md → Scenario: 读取旧格式状态文件 |
| **优先级** | P0 |
| **预置条件** | .stdd.yaml 不含 version 字段（手动删除 version 行后） |
| **输入** | `python bin/stdd status` |
| **预期结果** | 正常显示状态，不报错 |
| **当前状态** | ❌ 测试缺 |

### 功能 9：模板增强

#### 案例 9.1 — spec.md 含 AND 示例

| 字段 | 内容 |
|------|------|
| **ID** | TC-TMPL-001 |
| **对应 Spec** | template/spec.md → Scenario: 模板包含 AND 示例 |
| **优先级** | P2 |
| **预置条件** | 无 |
| **输入** | 检查 .stdd/templates/spec.md 内容 |
| **预期结果** | 包含 AND 用法注释示例 |
| **当前状态** | ❌ 测试缺 |

#### 案例 9.2 — tasks.md 含优先级和依赖示例

| 字段 | 内容 |
|------|------|
| **ID** | TC-TMPL-002 |
| **对应 Spec** | template/spec.md → Scenario: 模板包含优先级和依赖关系示例 |
| **优先级** | P2 |
| **预置条件** | 无 |
| **输入** | 检查 .stdd/templates/tasks.md 内容 |
| **预期结果** | 包含 P0/P1/P2 优先级标注和（依赖 #N）示例 |
| **当前状态** | ❌ 测试缺 |

### 功能 10：版本号统一

#### 案例 10.1 — config.yaml 版本号

| 字段 | 内容 |
|------|------|
| **ID** | TC-CONF-001 |
| **对应 Spec** | —（config 修正） |
| **优先级** | P0 |
| **预置条件** | 无 |
| **输入** | 检查 config.yaml 中 stdd_version |
| **预期结果** | `stdd_version: "1.2.1"` |
| **当前状态** | ❌ 当前为 "1.0.0" |

### 功能 11：README/STDD.md 去重

#### 案例 11.1 — README 六阶段为简要表格

| 字段 | 内容 |
|------|------|
| **ID** | TC-DOCS-001 |
| **对应 Spec** | template/spec.md → Scenario: README 简要引用六阶段 |
| **优先级** | P2 |
| **预置条件** | 无 |
| **输入** | 检查 README.md 六阶段部分 |
| **预期结果** | 为简要表格或列表形式；包含指向 STDD.md 的引用 |
| **当前状态** | ❌ 当前 README 重复完整流程描述 |

## 三、测试执行矩阵

| 功能模块 | 手动验证 | 状态 |
|----------|----------|------|
| archive 修复（TC-CLI-001/002） | CLI 命令 + 文件系统检查 | 🟡 手动 |
| validate 修复（TC-CLI-003/004） | CLI 命令 | 🟡 手动 |
| trace 修复（TC-CLI-005） | CLI 命令 | 🟡 手动 |
| init --force（TC-CLI-006/007） | CLI 命令 + 文件内容检查 | 🟡 手动 |
| new 格式验证（TC-CLI-008~010） | CLI 命令 | 🟡 手动 |
| install 检查（TC-CLI-011/012） | CLI 命令 | 🟡 手动 |
| status 模式（TC-CLI-013/014） | CLI 命令 | 🟡 手动 |
| version 字段（TC-STATE-001/002） | CLI 命令 + YAML 内容检查 | 🟡 手动 |
| 模板增强（TC-TMPL-001/002） | 文件内容检查 | 🟡 手动 |
| 版本号（TC-CONF-001） | 文件内容检查 | 🟡 手动 |
| 文档去重（TC-DOCS-001） | 文件内容检查 | 🟡 手动 |

## 四、回归风险矩阵

| 风险区域 | V1.2.1+V1.3 改动 | 已有回归保护 | 风险等级 |
|----------|-----------------|-------------|---------|
| archive 命令 | 目录名修正 + 操作顺序 | 手动验证 | 🟡 中 |
| validate 命令 | 正则逻辑变更 | 手动验证 | 🟢 低 |
| trace 命令 | 搜索路径增加 | 手动验证 | 🟢 低 |
| init 命令 | 增加 --force 选项 | 手动验证 | 🟢 低 |
| new 命令 | 增加格式验证 | 手动验证 | 🟡 中 |
| install 命令 | 增加存在性检查 | 手动验证 | 🟢 低 |
| status 命令 | 增加模式显示 | 手动验证 | 🟢 低 |
| .stdd.yaml 格式 | 增加 version 字段 | 手动验证 | 🟢 低 |
| 现有 change 目录 | 无直接改动 | 手动验证 | 🟢 低 |

## 五、建议补充顺序

1. **第一优先**（变更完成后立即验证）：TC-CLI-001~005, TC-STATE-001~002, TC-CONF-001（P0 Bug 修复 + 兼容性）
2. **第二优先**（变更完成后验证）：TC-CLI-006~014（P1/P2 新功能和增强）
3. **第三优先**（后续补充）：TC-TMPL-001~002, TC-DOCS-001（模板和文档验证）
