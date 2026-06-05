# STDD V2.5 技术设计

> Change: 2026-05-21-stdd-v2.5
> 版本目标：V2.4 → V2.5
> 设计日期：2026-05-21

## Context

V2.4 引入经验库（discover/record 两阶段）、CI check-failures（~60% 覆盖）、extract-proposal（4 字段提取）。V2.5 在两件事上深化：(1) 经验库从"记录"升级到完整生命周期闭环；(2) STDD 从深度绑定单 AI 对话，适配多 Agent/多 session/可并行的现代范式。

## Decisions

### 1. 经验生命周期状态机

**当前**：V2.4 经验只有 `lifecycle_state: discovered` 一种状态。

**方案**：5 状态有限状态机：

```
discovered ──(verify)──→ verified ──(3+ occurrences)──→ deposited
    │                          │
    │ (insufficient evidence)  │ (export)
    └──→ retired               └──→ shared ──(imported by others)──→ merged
                                                         │
                                                     (obsolete)
                                                         │
                                                     retired
```

- **discovered → verified**：`stdd experience verify <id>` 手动确认，或同项目中出现 2+ 次自动提升
- **verified → deposited**：同项目出现 3+ 次，`confidence >= 0.8`，自动标记
- **verified → shared**：用户执行 `stdd experience export --publish`，脱敏后发布
- **shared → merged**：被其他项目 pull 且标记 useful ≥ 3 次
- **任一 → retired**：`stdd experience retire <id> --reason "..."`
- **迁移**：V2.4 现有经验（lifecycle_state: discovered）无需迁移，自然升级

**状态存储**：`.experience-index.yaml` 的 `by_lifecycle` 映射自动更新。经验文件 frontmatter 的 `lifecycle_state` 字段同步。

### 2. CI check-failures 扩展架构

**当前**：`check-failures` 是 `ci.py` 中的一个函数，执行 4 项检查后打印报告。

**方案**：保持 `check-failures` 作为总入口，3 个新检查各为独立函数，通过注册表聚合：

```python
# ci.py 内部
CHECKS = [
    check_files_exist,        # 已有
    check_tcid_unique,        # 已有
    check_shall_keyword,      # 已有
    check_and_count,          # 已有
    check_scope_creep,        # 新增 (b)
    check_coverage_vacuum,    # 新增 (j)
    check_contract_gap,       # 新增 (k)
]
```

**check_scope_creep**：读取 proposal.md 中 STDD-MARKER 声明的 capability 列表 → `git diff --stat <base>` 获取变更文件 → 交叉对比标记超出范围的文件。纯静态分析，不依赖 pytest。

**check_coverage_vacuum**：解析 `pytest --cov-report=json` 输出 → 提取 `"summary": {"percent_covered": ...}` → 低于 `quality.yaml` 阈值（默认 80%）标记。如果没有 pytest 输出文件则跳过（graceful degradation，适用于非代码 change）。

**check_contract_gap**：依赖 `dependency-graph` 的输出 → 对每条依赖边（A → B），检查 A 的 spec 中引用的 B 字段是否在 B 的 spec 中定义。基于 spec 文件的 `GIVEN.*from <capability>` 模式匹配。

### 3. 社区经验池：零后端设计 + 双源镜像 + curate 工具链

**问题**：`stdd experience pull` 需要后端存储和 API，且国内用户访问 GitHub 受限。

**方案**：不需要后端。利用 GitHub Releases + Gitee 镜像作为存储层。新增 `experience curate` 命令组供 STDD 官方维护者整理官方经验包。

#### 3.1 双源镜像与自动 fallback

```
stdd experience pull python

  1. 尝试主源（GitHub Releases）
     └── 5 秒内无响应 → 自动切换

  2. 自动 fallback 到镜像源（Gitee Release）
     └── 下载同一文件
```

`experience.yaml` 配置：
```yaml
community:
  registries:
    - name: github
      url: "https://github.com/leonai42/stdd-experiences/releases/latest/download"
      priority: 1
    - name: gitee
      url: "https://gitee.com/leonai42/stdd-experiences/releases/latest/download"
      priority: 2
  fallback_timeout: 5
  packs:
    - name: python
      version: "v1.0.0"
    - name: go
      version: "v1.0.0"
```

#### 3.2 贡献流程（开发者端）

```
$ stdd experience export EXP-0042 --publish
  → 脱敏（路径/IP/域名/密钥 → 占位符）
  → 打包为 EXP-0042.tar.gz
  → lifecycle_state → shared
  → 输出 PR 提交指引

开发者 Fork leonai42/stdd-experiences → 放入 experiences/<language>/ → 提 PR → CI 校验 → 合并
```

#### 3.3 官方整理流程（维护者端）

新增 `stdd experience curate` 命令组：

```
$ stdd experience curate pull
  → 从所有 registry 下载全量 .tar.gz
  → 解压到 .stdd/curation/inbox/
  → 统计输出（按语言/来源/severity 分布）

$ stdd experience curate deduplicate
  → 按 pattern 关键词重叠率匹配疑似重复（相似度 >80% = 自动合并，60-80% = 待人工）
  → 合并策略：保留最完整的条目，tags 并集，occurrences 累加，confidence 取 max

$ stdd experience curate review
  → 交互式逐条审核：[a]pprove / [e]dit / [m]erge / [r]eject / [s]kip
  → 淘汰规则：occurrences < 2 且 confidence < 0.5 → 建议 reject
  → 过期规则：last_seen > 2 年 → 建议 retired
  → 补充规则：root_cause/fix_template 为空 → 建议 edit

$ stdd experience curate pack python
  → 将 approved 条目打包为 experience-python-v1.0.0.tar.gz
  → 写入 frontmatter: pack_version / curated: true / curated_by / curated_date
  → 上传到 GitHub + Gitee Release
```

#### 3.4 架构总览

```
贡献侧                            官方维护侧                        消费侧
────────                         ──────────                       ────────

开发者 export --publish          维护者 curate pull/dedup           用户 pull python
       │                               │                                │
       │  PR 提交                       │  全量拉取                       │  主源: GitHub
       └──→ stdd-experiences ───────────┘──→ 去重合并                     │  fallback: Gitee
           inbox/ (社区提交)             │   逐条审核                      │
           packs/ (官方包 ← CI 构建)  ←──┘   打包上传                      │
                                                                         │
                                    GitHub Actions 自动镜像 → Gitee ──────┘
```

#### 3.5 新增资产

| 新增项 | 说明 |
|--------|------|
| `curate.py` CLI | `experience curate pull/deduplicate/review/pack` 子命令 |
| `experience.yaml` 双源配置 | registries 列表 + fallback_timeout |
| stdd-experiences 仓库 | GitHub + Gitee 各一个，Actions 自动镜像 |
| `--publish` 导出流程 | `experience export` 的增强 flag |

**不需要**：后端服务器、数据库、Web 前端、用户注册、CDN、API 服务。

### 4. Gate 文件确认

**方案**：新增 `stdd gate approve` CLI + 文件 token 机制。不需要修改现有 skill 的对话确认流程，两种方式独立且等效。

```
# CLI 方式（新增）
stdd gate approve 2026-05-21-stdd-v2.5 --gate 1

# 文件方式（新增，等价）
touch changes/2026-05-21-stdd-v2.5/GATE1_APPROVED

# 底层操作（不变）
# → .stdd.yaml 写入 phases.understand.confirmed_at: "2026-05-21T14:30:00Z"
```

`gates.yaml` 新增配置：
```yaml
confirmation:
  channels:
    - dialog        # 对话确认（现有）
    - file_token    # 文件 token（新增）
    - cli           # CLI 命令（新增）
  file_token_dir: "{change_dir}"  # GATE<N>_APPROVED 文件存放位置
```

### 5. extract-proposal 扩展

**方案**：扩展 `_parse_section()` 识别 proposal.md 中新增的 STDD-MARKER 字段。模板 `proposal.md` 增加标记注释。

新增提取字段：
- `Constraints`：从 `## Constraints` 段落提取列表项
- `Stakeholders`：从 `## Stakeholders` 段落提取
- `RiskAreas`：从 `## Risk Areas` 段落提取，映射到具体 capability
- `NonGoals`：从 `## NonGoals` 段落提取

JSON 输出格式向后兼容，新字段为新增 key，旧 key 不变。

### 6. 非代码 change 支持

**方案**：纯 skill 指令增强 + 一个数据字段，不新增 CLI。

`verify.md` Step 3（11 类失败检查）后增加条件分支：
```
IF change 目录不包含 *.py/*.go/*.java/*.rs/*.ts 文件：
  使用"非代码类替代检查清单"（5 项）
ELSE：
  使用现有 11 类失败模式检查
```

经验 `project_type` 字段：
- 经验创建时自动检测 change 的文件类型分布（主力语言）
- 存储为 frontmatter `project_type: python|go|static_site|docs|config`
- 经验加载时（build.md Step 0.5）按 `project_type` 过滤：只加载同类型或 `all` 的经验

## Architecture

```
V2.4 已有（不变）：
  stdd/bin/ → cli/commands/{__init__, experience, ci, extract_proposal, dependency_graph, ...}.py
  .stdd/skills/{understand, spec, slice, build, verify, deliver}.md
  .stdd/config.d/{project, gates, long_range, quality, experience}.yaml
  .stdd/experiences/.experience-index.yaml + EXP-*.md

V2.5 变更：
  cli/commands/
    ├── ci.py                  → +check_scope_creep, +check_coverage_vacuum, +check_contract_gap
    ├── experience.py          → +cmd_verify, +cmd_deposit, +cmd_retire, +cmd_pull, +cmd_export 增强
    ├── extract_proposal.py    → 扩展 _parse_section 识别 Constraints/Stakeholders/RiskAreas/NonGoals
    ├── gate.py                → [NEW] cmd_approve
    └── state.py               → 读写 resume_context/active_slice/last_action/last_modified

  .stdd/skills/
    ├── build.md               → Step 0.5 增加 project_type 过滤, +并行执行策略
    └── verify.md              → Step 3 后增加非代码 change 分支

  .stdd/config.d/
    ├── experience.yaml        → +community 配置段
    └── gates.yaml             → +confirmation.channels 配置段

  .stdd/templates/
    └── proposal.md            → +Constraints/Stakeholders/RiskAreas/NonGoals 的 STDD-MARKER 标记
```

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| 经验状态机状态不一致（文件 vs 索引不同步） | `_save_index()` 已有 O_CREAT\|O_EXCL 文件锁，状态变更操作封装为原子方法 |
| `check-coverage` 依赖 pytest JSON 输出，非代码项目不存在 | graceful degradation：跳过并输出 `[SKIP] no coverage data found` |
| `check-contract-gap` 的 GIVEN 模式匹配精度有限 | 仅匹配 `GIVEN.*from <capability>` 中的 capability 名，不做 NLP 模糊匹配 |
| 社区经验池 GitHub Release 可能被限流 | `experience pull` 首次下载全量包，后续增量更新（If-Modified-Since header） |
| 非代码检查清单的检查项太主观 | 检查清单仅作为 AI 的维度引导，不做自动化判定 |
