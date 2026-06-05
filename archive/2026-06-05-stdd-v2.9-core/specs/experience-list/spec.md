# experience-list — 经验列表查询优雅降级

<!-- confidence: high -->
<!-- evidence: proposal.md BUG-01 + experience.py 代码分析 -->

## Requirement: 空目录优雅降级

EXP-REQ-001: 新项目无 experiences 目录时，`stdd experience list` SHALL 返回空列表而非报错。

### Scenario: 新项目无 experiences 目录

<!-- confidence: high -->
GIVEN 项目 `.stdd/` 目录存在
AND `.stdd/experiences/` 目录不存在
WHEN 用户执行 `stdd experience list --language python --format json`
THEN SHALL 返回 `[]`（空 JSON 数组）
AND 退出码为 0
AND 不抛出 FileNotFoundError

### Scenario: experiences 目录存在但为空

<!-- confidence: high -->
GIVEN `.stdd/experiences/` 目录存在
AND 目录中无 `EXP-*.md` 文件
AND 不存在 `.experience-index.yaml`
WHEN 用户执行 `stdd experience list`
THEN SHALL 显示 "经验库 (0/0 条)"
AND 退出码为 0

### Scenario: experiences 目录正常有数据

<!-- confidence: high -->
GIVEN `.stdd/experiences/` 目录存在且有 3 个经验文件
AND `.experience-index.yaml` 正常
WHEN 用户执行 `stdd experience list`
THEN SHALL 正常列出 3 条经验
AND 行为与 V2.8 一致（无退化）

## Requirement: _save_index 容错

EXP-REQ-002: `_save_index` SHALL 在目录不存在时自动创建目录。

### Scenario: 保存索引时自动创建目录

<!-- confidence: high -->
GIVEN `exp_dir` 路径对应的目录不存在
WHEN `_save_index(exp_dir, index)` 被调用
THEN SHALL 先调用 `_ensure_dir(exp_dir)` 创建目录
AND SHALL 成功写入 `.experience-index.yaml` 和锁文件
