# 测试方案: 经验池核心闭环

## 测试策略

**金字塔**：单元测试为主（CLI 命令级测试），集成测试为辅（服务器 API mock）。

**原则**：
- 每个 spec Scenario 至少 1 个 TC
- 外部依赖（gh CLI、服务器 API）使用 mock
- 复用现有 temp_project fixture

**已有资产**：`tests/commands/test_experience.py` (32 tests)、`tests/commands/test_curate.py` (3 tests)

## 详细测试案例

### TC-EXT-001: 从12类失败检查提取
- **预置**: temp_project 中有 test-report.md，cascading_errors=FAIL
- **输入**: `stdd experience extract`
- **预期**: 生成 EXP-*.md，category=cascading_errors，lifecycle_state=discovered
- **覆盖**: Scenario "从12类失败检查提取"

### TC-EXT-002: 低价值模式被过滤
- **预置**: test-report.md 中某模式 severity=low, occurrences=1
- **输入**: `stdd experience extract`
- **预期**: 跳过该模式，输出 "X 个低价值模式已跳过"
- **覆盖**: Scenario "筛选低价值模式"

### TC-EXT-003: test-report 不存在时优雅降级
- **预置**: change 目录无 test-report.md
- **输入**: `stdd experience extract`
- **预期**: 输出 "无 test-report.md"，正常退出
- **覆盖**: Scenario "test-report 不存在时优雅降级"

### TC-REV-001: 展示草稿列表
- **预置**: 3 个 lifecycle=discovered 的 EXP-*.md
- **输入**: `stdd experience review` (模拟输入 Q)
- **预期**: 展示 3 条，每条含 category/pattern/severity/occurrences
- **覆盖**: Scenario "展示草稿列表"

### TC-REV-002: 沉淀+共享 (S)
- **预置**: 1 个 discovered 草稿
- **输入**: `stdd experience review` (模拟输入 S)
- **预期**: lifecycle -> shared, 调用了 cmd_share
- **覆盖**: Scenario "用户选择沉淀+共享"

### TC-REV-003: 仅本地沉淀 (L)
- **预置**: 1 个 discovered 草稿
- **输入**: `stdd experience review` (模拟输入 L)
- **预期**: lifecycle -> deposited, 未调用 share
- **覆盖**: Scenario "用户选择仅本地沉淀"

### TC-REV-004: 跳过 (D)
- **预置**: 1 个 discovered 草稿
- **输入**: `stdd experience review` (模拟输入 D)
- **预期**: 草稿文件被删除
- **覆盖**: Scenario "用户选择跳过"

### TC-REV-005: 退出保留草稿 (Q)
- **预置**: 2 个 discovered 草稿
- **输入**: `stdd experience review` (模拟输入 Q)
- **预期**: 退出，草稿保持 discovered 状态
- **覆盖**: Scenario "退出保留草稿"

### TC-SHA-001: 自动脱敏
- **预置**: 经验 body 含 /home/user/project/src/main.py
- **输入**: `stdd experience share EXP-2026-0050` (mock gh 不可用)
- **预期**: 发送到 API 的 content 中路径已替换为 <project>/<module>
- **覆盖**: Scenario "自动脱敏"

### TC-SHA-002: gh CLI 可用时使用用户账号
- **预置**: mock shutil.which("gh") 返回 True
- **输入**: `stdd experience share EXP-2026-0050`
- **预期**: 调用了 gh 相关 git 操作
- **覆盖**: Scenario "gh CLI 可用时使用用户账号"

### TC-SHA-003: gh CLI 不可用时 fallback API
- **预置**: mock shutil.which("gh") 返回 False
- **输入**: `stdd experience share EXP-2026-0050`
- **预期**: 发出了 POST 到 hzddyy.com/stdd/api/share-experience
- **覆盖**: Scenario "gh CLI 不可用时 fallback 到服务器 API"

### TC-SHA-004: API 成功更新状态
- **预置**: mock API 返回 {"success": true}
- **输入**: `stdd experience share EXP-2026-0050`
- **预期**: lifecycle_state=shared
- **覆盖**: Scenario "服务器 API 返回成功"

### TC-SHA-005: gh 和 API 都不可用时优雅降级
- **预置**: mock ("gh")=False, API 返回 ConnectionError
- **输入**: `stdd experience share EXP-2026-0050`
- **预期**: 报错，lifecycle 不变，提示可手动 export
- **覆盖**: Scenario "服务器 API 不可用时优雅降级"

### TC-SEA-001: 关键词全文搜索
- **预置**: 2 条经验的 pattern 含 "超时"，3 条不含
- **输入**: `stdd experience search "超时"`
- **预期**: 返回 2 条，pattern 匹配的排在前面
- **覆盖**: Scenario "关键词搜索"

### TC-SEA-002: 组合过滤
- **预置**: python 经验 3 条 + go 经验 2 条
- **输入**: `stdd experience search "error" --language python`
- **预期**: 只返回 python 匹配结果
- **覆盖**: Scenario "组合过滤"

### TC-SEA-003: 无匹配结果
- **预置**: 经验库不为空
- **输入**: `stdd experience search "xyznotfound"`
- **预期**: "未找到匹配"，exit 0
- **覆盖**: Scenario "无匹配结果"

### TC-SEA-004: JSON 格式输出
- **预置**: 匹配到 2 条经验
- **输入**: `stdd experience search "pattern" --format json`
- **预期**: JSON 数组，含 experience_id/relevance_score
- **覆盖**: Scenario "JSON 格式输出"

### TC-SEA-005: 空经验库
- **预置**: .stdd/experiences/ 无 EXP-*.md
- **输入**: `stdd experience search "anything"`
- **预期**: "经验库为空"
- **覆盖**: Scenario "空经验库"

## 测试执行矩阵

| TC | Capability | 层次 | 优先级 |
|----|-----------|------|--------|
| TC-EXT-001 | extract | 单元 | P0 |
| TC-EXT-002 | extract | 单元 | P0 |
| TC-EXT-003 | extract | 单元 | P1 |
| TC-REV-001 | review | 单元 | P0 |
| TC-REV-002 | review | 单元 | P0 |
| TC-REV-003 | review | 单元 | P0 |
| TC-REV-004 | review | 单元 | P1 |
| TC-REV-005 | review | 单元 | P1 |
| TC-SHA-001 | share | 单元 | P0 |
| TC-SHA-002 | share | 单元 | P0 |
| TC-SHA-003 | share | 单元 | P0 |
| TC-SHA-004 | share | 单元 | P1 |
| TC-SHA-005 | share | 单元 | P1 |
| TC-SEA-001 | search | 单元 | P0 |
| TC-SEA-002 | search | 单元 | P1 |
| TC-SEA-003 | search | 单元 | P1 |
| TC-SEA-004 | search | 单元 | P2 |
| TC-SEA-005 | search | 单元 | P1 |

## 回归风险矩阵

| 改动区域 | 风险 | 缓解 |
|----------|------|------|
| experience.py (新增 4 命令) | 低 | 新增代码，不修改现有 9 个命令 |
| __init__.py (注册子命令) | 低 | 仅新增 4 行注册 |
| VERIFY skill (新增 extract 调用) | 中 | 改为可选步骤，失败不影响 VERIFY 主流程 |
| 现有 CLI 行为 | 极低 | 不改变现有命令签名和逻辑 |
