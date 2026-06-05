# version-upgrade — 版本升级 CLI

<!-- confidence: high -->
<!-- evidence: proposal.md "版本升级系统（P1）" + V2.9_PLAN.md Part A -->

## Requirement: 检测版本差异

UPGRADE-REQ-001: SHALL 比较项目版本与 STDD 源版本，报告差异。

### Scenario: 旧版本项目检测到差距

<!-- confidence: high -->
GIVEN 项目的 `.stdd/version.yaml` 中 `stdd_version: "2.5.0"`
AND STDD 源的 `project.yaml` 中 `stdd_version: "2.9.0"`
WHEN 用户执行 `stdd upgrade --check`
THEN 输出 SHALL 包含 "新版本可用: 2.9.0 (当前: 2.5.0)"
AND 命令退出码为 0

### Scenario: 项目已是最新版本

<!-- confidence: high -->
GIVEN 项目的版本等于 STDD 源版本
WHEN 用户执行 `stdd upgrade --check`
THEN 输出 SHALL 包含 "已是最新版本"
AND 命令退出码为 0

### Scenario: 旧项目无 version.yaml 回退 project.yaml

<!-- confidence: medium -->
GIVEN 项目无 `.stdd/version.yaml`
AND `.stdd/config.d/project.yaml` 中 `stdd_version: "2.3.0"`
WHEN 用户执行 `stdd upgrade --check`
THEN SHALL 读取 project.yaml 中的版本号作为当前版本
AND 正常显示版本差异

## Requirement: 执行升级

UPGRADE-REQ-002: SHALL 将项目 STDD 文件从源版本升级到最新版本。

### Scenario: 成功升级并创建备份

<!-- confidence: high -->
GIVEN 项目版本为 2.5.0，源版本为 2.9.0
AND 项目未锁定
WHEN 用户确认执行 `stdd upgrade`
THEN SHALL 在 `.stdd/backup/2.5.0-<timestamp>/` 创建备份
AND SHALL 同步 skills/templates/standards/config 文件
AND SHALL 重新安装已使用的平台 skills
AND SHALL 写入 `.stdd/version.yaml` 且 `stdd_version: "2.9.0"`
AND SHALL 更新 `~/.stdd/projects.yaml` 注册表

### Scenario: 升级 project.yaml 使用合并策略

<!-- confidence: high -->
GIVEN 项目的 project.yaml 有 `project.name: "TStrategy"` 和 `project.language: "python"`
AND 源的 project.yaml 有新的 `experience.yaml` 配置
WHEN 执行升级
THEN SHALL 保留 project.name 和 project.language
AND SHALL 新增 experience.yaml 相关配置
AND SHALL 更新 stdd_version 为源版本

### Scenario: 锁定项目拒绝升级

<!-- confidence: high -->
GIVEN `.stdd/version.yaml` 中 `locked: true`
WHEN 用户执行 `stdd upgrade`
THEN 输出 SHALL 包含 "项目已锁定在版本 X.X.X"
AND 不执行任何文件操作
AND 命令退出码为 0

### Scenario: 升级使用 dry-run 模式

<!-- confidence: high -->
GIVEN 项目版本与源版本不同
WHEN 用户执行 `stdd upgrade --dry-run`
THEN SHALL 展示完整升级计划（备份路径、将复制的文件列表、将安装的平台）
AND 不修改文件系统

## Requirement: 版本锁定

UPGRADE-REQ-003: SHALL 支持锁定/解锁项目版本。

### Scenario: 锁定项目

<!-- confidence: high -->
GIVEN 项目当前版本为 2.5.0
AND `.stdd/version.yaml` 不存在或 `locked: false`
WHEN 用户执行 `stdd upgrade --lock`
THEN SHALL 写入/更新 `.stdd/version.yaml` 且 `locked: true`
AND SHALL 在启动检测时静默跳过

### Scenario: 解锁项目

<!-- confidence: high -->
GIVEN `.stdd/version.yaml` 中 `locked: true`
WHEN 用户执行 `stdd upgrade --unlock`
THEN SHALL 设置 `locked: false`
AND 后续启动检测正常提示版本更新

## Requirement: 批量项目管理

UPGRADE-REQ-004: SHALL 支持跨项目的版本管理和矩阵查看。

### Scenario: 批量检查所有注册项目

<!-- confidence: medium -->
GIVEN `~/.stdd/projects.yaml` 注册了 3 个项目
AND 其中 1 个锁定、2 个可升级
WHEN 用户执行 `stdd upgrade --all --check`
THEN SHALL 显示版本矩阵表格（项目名、当前版本、最新版本、锁定状态）
AND 锁定项目标注 [LOCKED]

### Scenario: 批量升级跳过锁定和已是最新的项目

<!-- confidence: medium -->
GIVEN 注册了 3 个项目（1 锁定、1 最新、1 需升级）
WHEN 用户执行 `stdd upgrade --all --yes`
THEN SHALL 跳过锁定项目
AND SHALL 跳过已是最新的项目
AND SHALL 仅升级需要升级的项目

## Requirement: 启动版本检测

UPGRADE-REQ-005: SHALL 在任何 CLI 命令执行前检测版本差距并提示。

### Scenario: 启动时检测到新版本

<!-- confidence: high -->
GIVEN 项目版本低于源版本
AND 项目未锁定
AND 当前命令不是 `upgrade`
WHEN 执行任意 STDD CLI 命令
THEN SHALL 打印 `[STDD] 有新版本可用: X.X.X (当前: Y.Y.Y)`
AND SHALL 打印 `运行 'stdd upgrade --check' 查看详情`
AND 不阻塞命令执行

### Scenario: 启动时项目已锁定

<!-- confidence: high -->
GIVEN `.stdd/version.yaml` 中 `locked: true`
WHEN 执行任意 STDD CLI 命令
THEN 不打印版本提示

### Scenario: 非 STDD 项目不检查

<!-- confidence: high -->
GIVEN 当前目录无 `.stdd/` 目录
WHEN 执行任意 STDD CLI 命令
THEN 不打印版本提示
