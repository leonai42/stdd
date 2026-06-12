# Spec: experience-share

## Requirement: 一键共享经验到社区

自动脱敏并推送经验到 stdd-experiences/pending/，混合模式（gh CLI 优先，服务器 API fallback）。

### Scenario: 自动脱敏 (confidence: high)
- **GIVEN** 经验 EXP-2026-0050 的 body 包含 `/home/user/project/src/main.py`
- **WHEN** 执行 `stdd experience share EXP-2026-0050`
- **THEN** SHALL 将路径替换为 `<project>/<module>`
- **AND** SHALL 将 IP 地址替换为 `<ip-address>`
- **AND** SHALL 将域名替换为 `<domain>`
- **AND** SHALL 脱敏后的内容用于上传，本地原文件不变

### Scenario: gh CLI 可用时使用用户账号 (confidence: medium)
- **GIVEN** 系统 PATH 中存在 `gh` 命令且 `gh auth status` 返回成功
- **WHEN** 执行 `stdd experience share EXP-2026-0050`
- **THEN** SHALL 使用 gh CLI 克隆 stdd-experiences 仓库
- **AND** SHALL 以用户身份提交并推送
- **AND** SHALL commit message 包含用户 git 用户名

### Scenario: gh CLI 不可用时 fallback 到服务器 API (confidence: high)
- **GIVEN** 系统 PATH 中不存在 `gh` 命令
- **WHEN** 执行 `stdd experience share EXP-2026-0050`
- **THEN** SHALL POST 到 https://hzddyy.com/stdd/api/share-experience
- **AND** SHALL 请求体包含 experience_id, content, author
- **AND** SHALL 超时时间 30s

### Scenario: 服务器 API 返回成功 (confidence: high)
- **GIVEN** POST 到服务器 API
- **WHEN** 服务器返回 `{"success": true, "experience_id": "EXP-2026-0050"}`
- **THEN** SHALL 更新本地 lifecycle_state=shared
- **AND** SHALL 展示: "EXP-2026-0050: 已提交到待审批池"

### Scenario: 服务器 API 不可用时优雅降级 (confidence: medium)
- **GIVEN** gh CLI 不可用且服务器 API 返回 5xx 或超时
- **WHEN** 执行 `stdd experience share EXP-2026-0050`
- **THEN** SHALL 展示错误信息
- **AND** SHALL 不更新 lifecycle_state
- **AND** SHALL 提示用户: "可尝试手动 export --publish 后上传"
