# 经验池核心闭环：自动提取 → 交互审核 → 一键共享 → 全文搜索

## Why

当前 STDD 经验池系统存在三个断裂：
1. **录入断裂**：Phase 5 VERIFY 发现的失败模式无法自动沉淀为经验，用户需手动填 10+ 字段才能录入一条经验，门槛极高；
2. **共享断裂**：从本地经验到社区可用需要 6 步操作（add → verify → deposit → export --publish → 手动上传 GitHub Release），其中 2 步离开 CLI，且需额外配置 GitHub Token；
3. **发现断裂**：用户无法搜索已有经验，只能按分类/语言筛选，缺乏全文检索能力。

## What Changes

- **C1 (new)**：新增  命令 — 从 test-report.md + 测试输出自动提取经验草稿
- **C2 (new)**：新增  命令 — 交互式确认（S 沉淀+共享 / L 仅本地 / D 跳过 / A 全部共享）
- **C3 (new)**：新增  命令 — 方案D混合模式一键共享（gh CLI 优先，服务器 API fallback）
- **C4 (new)**：新增  命令 — 全文搜索 pattern + root_cause + body
- **C5 (modified)**：升级 VERIFY skill — Phase 5 末尾自动调用 extract，提示用户 review

## Capabilities

### New Capabilities

- **experience-extract**：从 test-report.md + 测试输出中自动提取失败模式/异常/优化建议，筛选 severity ≥ medium 或 occurrences ≥ 2，生成 lifecycle=discovered 的经验草稿
- **experience-review**：逐条展示草稿，展示 category / pattern / severity / occurrences，用户选择 [S] 沉淀+共享 / [L] 仅本地沉淀 / [D] 跳过，选 S 后 lifecycle → deposited → shared 并自动触发 share
- **experience-share**：自动脱敏（路径→<project>/<module>，IP→<ip-address>，域名→<domain>）→ 检测 gh CLI 是否可用 → 可用则用用户账号 git push → 不可用则 POST 到 https://hzddyy.com/stdd/api/share-experience
- **experience-search**：全文检索 pattern + root_cause + body 字段，支持 --category / --language / --severity 过滤，按 relevance_score（词频+匹配度）+ confidence + adoption_count 排序

### Modified Capabilities

- **experience-cli**：新增 extract / review / share / search 4 个子命令注册

## Impact

**代码层面**：
- ：新增 ~300 行（cmd_extract, cmd_review, cmd_share, cmd_search）
- ：新增 ~200 行（4 类测试 × 3-5 用例）
- ：注册 4 个新子命令

**配置层面**：
- 服务器 API URL 硬编码在 share 函数中（https://hzddyy.com/stdd/api/share-experience）

**基础设施**：
- 依赖服务器端 API 服务（已部署于 /var/www/ddyy/stdd-api/server-api.py，已验证通过）

## Constraints

- Python 3.10+，stdd 标准库 + requests
- 服务器 API 端点 https://hzddyy.com/stdd/api/share-experience（已部署验证通过）
- extract 筛选条件：severity ≥ medium 或 occurrences ≥ 2
- share 自动脱敏：调用现有 _sanitize() 函数
- 不依赖第三方 NLP 库（搜索使用纯文本匹配 + 简单评分）

## Stakeholders

- STDD 用户（AI 编程实践者）— 使用 extract/review/share/search
- STDD 维护者（经验审核员）— 后续使用 curate review

## Risk Areas

- capability: experience-extract — 自动提取的 pattern/root_cause 质量可能不高
  - mitigation: 草稿 lifecycle=discovered，必须通过 review 才能推进到 verified
- capability: experience-share — gh CLI 检测在 Windows/Linux/macOS 表现可能不一致
  - mitigation: 使用 shutil.which() 跨平台检测 + 明确 fallback 到服务器 API
- capability: experience-share — 服务器 API 不可用时分享失败
  - mitigation: 失败时报错提示，不阻塞本地沉淀（选 S 时先 deposit 再尝试 share）

## NonGoals

- 不改变现有 experience FSM 生命周期状态定义（discovered→verified→deposited→shared→merged→retired）
- 不实现社区双池结构（pending/approved/rejected）— 单独后续实现
- 不实现团队私有经验池 — STDD for Team 版本功能

## Critical

- [x] 非关键变更（默认）
- [ ] 关键变更

## Risk Assessment

- **safety_critical**：false
- **financial**：false
- **cross_system**：true（依赖外部服务器 API 端点）

## Anchoring

- **level**：L2（接口锚定：基于现有 experience.py CLI 接口模式）
- **reference_changes**：无
- **anchor_implementations**：无

## Success Criteria

- [ ] SC1:  能从 test-report.md 中提取至少 12 类失败模式和测试异常的草稿
- [ ] SC2:  交互式展示草稿，支持 S/L/D/A/Q 选择，选 S 后自动推进 lifecycle → shared
- [ ] SC3:  在 gh CLI 可用时使用用户账号提交；不可用时走服务器 API fallback
- [ ] SC4:  自动脱敏（路径→<project>/<module>，IP→<ip-address>，域名→<domain>）
- [ ] SC5:  支持关键词全文检索，按 relevance_score 排序
- [ ] SC6: 所有新增命令通过单元测试，与现有 36 个经验测试不冲突
