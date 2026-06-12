# 技术设计: 经验池核心闭环

## Context

当前 `stdd/cli/commands/experience.py` 包含 9 个子命令。本次新增 4 个:
extract、review、share、search。经验存储格式不变，FSM 生命周期不变。
服务器 API 已部署验证通过。

## Decisions

### D1: extract 数据源
- 方案: 从 test-report.md 解析"12 类失败检查"表格 + "测试摘要"章节
- 备选: 解析 pytest JSON -> 格式依赖版本,且无法覆盖非测试类失败模式

### D2: extract 触发时机
- 方案: Phase 5 VERIFY skill 末尾调用,不改变 CLI 独立可用性
- 备选: hook 集成 -> 侵入性大

### D3: review 交互模式
- 方案: 终端逐条展示,单字符 S/L/D/A/Q, S 为默认推荐
- 备选: GUI -> 开发成本高

### D4: share 混合模式(方案D)
- 方案: shutil.which检测 gh CLI -> 可用则用户账号 push -> 不可用则 POST 服务器 API
- 备选A: 仅 gh CLI -> 门槛高。备选B: 仅服务器 -> 匿名化。方案D 兼顾两者

### D5: 服务器 API 通信
- 方案: requests.post(url, json=payload, timeout=30), 已通过验证
- 备选: git push -> 国内服务器网络限制,不可行

### D6: 脱敏时机
- 方案: share 时自动调用 _sanitize(), 本地文件不脱敏
- 备选: 存储时脱敏 -> 丢失本地可用信息

### D7: search 实现
- 方案: 纯 Python, 遍历 EXP-*.md, pattern/root_cause/body 子串匹配 + 词频评分
- 备选: SQLite FTS5 -> 引入新依赖,收益不大

### D8: extract 筛选
- 方案: severity >= medium 或 occurrences >= 2, 过滤低价值问题

## Architecture

Phase 5 VERIFY 完成后:
  extract: test-report.md -> EXP-*.md (discovered)
  review: 展示草稿 -> S(share)/L(local)/D(skip)
    S -> deposit + share (自动脱敏)
    L -> verify + deposit
    D -> 删除草稿
  share: _sanitize() -> gh CLI? YES=用户账号 / NO=POST API
  search: 遍历 EXP-*.md -> 子串匹配 + 评分 -> 排序输出

## Risks

| 风险 | 缓解 |
|------|------|
| test-report.md 格式变化 | 解析容错,失败不阻塞 VERIFY |
| gh CLI 版本差异 | 使用基础命令 |
| 服务器 API 不可用 | share 失败不阻塞本地沉淀 |
| 大量经验导致 search 慢 | 当前<1000条,线性扫描足够 |
