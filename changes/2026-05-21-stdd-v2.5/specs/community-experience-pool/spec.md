# Spec: community-experience-pool — 社区经验共享池

> Capability: community-experience-pool
> Priority: P1 · 4.5d · CLI + 数据模型

## Requirement: 经验包下载（双源 fallback）

`stdd experience pull <pack-name>` SHALL 从主 registry 下载，超时自动 fallback。

### Scenario: 从主源成功下载

GIVEN `experience.yaml` 中配置了 `registries` 列表和 python 经验包
WHEN 用户执行 `stdd experience pull python`
THEN CLI SHALL 优先从 `priority: 1` 的 registry 下载
AND 解压到 `.stdd/experiences/`
AND 合并 `.experience-index.yaml`（新增经验条目，不覆盖已有经验）

### Scenario: 主源超时自动 fallback

GIVEN GitHub registry 在 5 秒内无响应
WHEN 执行 `stdd experience pull python`
THEN CLI SHALL 自动切换到 `priority: 2` 的 Gitee registry
AND 从 Gitee 下载同一文件包
AND 输出 SHALL 包含 "[FALLBACK] GitHub timed out, switched to Gitee mirror"

### Scenario: 所有源失败

GIVEN 所有 registry 均不可达
WHEN 执行 `stdd experience pull python`
THEN CLI SHALL 输出错误："all registries unreachable"
AND 退出码为 1

### Scenario: 经验包不存在

GIVEN 配置的 registry 中不存在 `rust` 经验包
WHEN 用户执行 `stdd experience pull rust`
THEN CLI SHALL 输出错误："pack 'rust' not found in registry"
AND 退出码为 1

### Scenario: 经验去重

GIVEN 本地已有 EXP-0001
AND 下载的经验包中也包含 EXP-0001
WHEN 执行 `stdd experience pull`
THEN 本地 EXP-0001 SHALL 保持不变（不覆盖已有经验）
AND 输出 SHALL 包含 "[SKIP] EXP-0001 already exists locally"

## Requirement: 投票元数据

经验条目的 YAML frontmatter SHALL 包含社区投票和采纳计数字段。

### Scenario: 新经验包含投票字段

WHEN 创建一条新经验
THEN frontmatter SHALL 包含以下字段（默认值 0）：
AND `community_votes_useful: 0`
AND `community_votes_unuseful: 0`
AND `adoption_count: 0`

### Scenario: 投票数据同步

GIVEN 经验 EXP-0001 在社区获得 5 个 useful 投票和 1 个 unuseful 投票
WHEN 用户执行 `stdd experience pull python`（增量更新）
THEN 本地 EXP-0001 的 `community_votes_useful` SHALL 更新为 5
AND `community_votes_unuseful` SHALL 更新为 1

## Requirement: 经验导出脱敏

`stdd experience export` SHALL 在导出前自动脱敏。

### Scenario: 自动脱敏

GIVEN 经验 body 中包含 `/home/user/projects/myapp/auth.py` 和 `192.168.1.100`
WHEN 执行 `stdd experience export EXP-0001`
THEN 路径 SHALL 替换为 `<project>/auth.py`
AND IP 地址 SHALL 替换为 `<ip-address>`
AND 域名 SHALL 替换为 `<domain>`
AND 密钥类字符串 SHALL 替换为 `<secret>`

### Scenario: 跳过脱敏

GIVEN 用户需要导出原始内容用于内部审计
WHEN 执行 `stdd experience export EXP-0001 --no-sanitize`
THEN 内容 SHALL 保持原文
AND 输出 SHALL 包含警告："exporting without sanitization — review before sharing"

### Scenario: 发布到社区

GIVEN 经验 EXP-0001 状态为 verified 且已脱敏导出
WHEN 执行 `stdd experience export EXP-0001 --publish`
THEN 导出文件 SHALL 打包为 `EXP-0001.tar.gz`
AND 其 `lifecycle_state` SHALL 变更为 `shared`
AND CLI SHALL 输出上传指引："Upload EXP-0001.tar.gz to GitHub Release or submit PR to stdd-experiences repo"

## Requirement: 官方维护者整理工具（curate）

`stdd experience curate` SHALL 提供 pull/deduplicate/review/pack 四个子命令，供 STDD 官方维护者整理官方经验包。

### Scenario: curate pull 拉取全量

WHEN 维护者执行 `stdd experience curate pull`
THEN CLI SHALL 从所有 registry 下载所有 .tar.gz
AND 解压到 `.stdd/curation/inbox/`
AND 输出统计报告：总条数 / 来源项目数 / 按语言分布

### Scenario: curate deduplicate 自动合并

GIVEN inbox 中有两条 pattern 相似度 >80% 的经验
WHEN 执行 `stdd experience curate deduplicate`
THEN SHALL 自动合并两条经验
AND 保留 root_cause/fix_template 最完整的那条
AND tags 并集，occurrences 累加，confidence 取 max
AND 输出："发现 N 组疑似重复，合并后: X → Y 条"

### Scenario: deduplicate 相似度阈值

GIVEN inbox 中有两条 pattern 相似度在 60-80% 之间的经验
WHEN 执行 `stdd experience curate deduplicate`
THEN SHALL 标记为"待人工确认"
AND 输出含两条经验的详情供维护者判断

### Scenario: curate review 逐条审核

WHEN 执行 `stdd experience curate review`
THEN SHALL 逐条展示经验，每个等待输入：[a]pprove/[e]dit/[m]erge/[r]eject/[s]kip
AND [a]pprove SHALL 添加 `curated: true` + `pack_version` 标记
AND [r]eject SHALL 要求输入淘汰原因，写入经验 body
AND occurrences < 2 且 confidence < 0.5 的经验 SHALL 自动标记"[LOW QUALITY]"建议 reject

### Scenario: curate pack 打包发布

GIVEN 所有 approved 经验已准备好
WHEN 执行 `stdd experience curate pack python`
THEN SHALL 将所有 curated 条目打包为 `experience-python-v1.0.0.tar.gz`
AND 生成完整的 `.experience-index.yaml`
AND 每条经验的 frontmatter SHALL 包含 `pack_version`, `curated: true`, `curated_by`, `curated_date`
AND 输出上传指引："Upload to GitHub + Gitee Release"
