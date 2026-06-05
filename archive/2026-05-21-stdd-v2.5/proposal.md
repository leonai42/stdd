# STDD V2.5 变更提案

> Change ID: 2026-05-21-stdd-v2.5
> 版本目标：V2.4 → V2.5
> 范围：P0 + P1（9 项改进，12.2 人天）

## Why

V2.4 首次实战（Playground 项目）和 Hermes Agent 集成反馈，暴露了两个层面的问题：

1. **经验库空洞化**：V2.4 的经验库只做了"发现→记录"，缺乏验证、沉淀、共享的生命周期闭环。Playground 实战中 3 条经验全是初始化占位条目，零有效产出。
2. **平台绑定**：STDD 的阶段切换、Gate 确认、11 类检查都深度绑定单 AI 对话模式。现代 Agent 系统（Hermes / Claude Code 多 Agent）已经是多 session、可并行的范式，STDD 在这些平台上运行时有明显的适配缺口。

V2.5 的目标：让经验库从"记录"升级到"闭环"，让 STDD 从"单平台深度绑定"升级到"跨平台可移植"。

## What Changes

### P0 — 核心闭环（3 项，5.5d）

<!-- STDD-MARKER:capability name="experience-lifecycle" -->
**1. 经验库生命周期完善（O1）**：V2.4 的经验只有 `discovered` 一种生命周期状态。V2.5 增加 verify（置信度自动提升）→ deposit（3+ occurrence 自动标 verified）→ share（导出脱敏）→ merge（社区经验导入）→ retire（标记废弃）五个新状态。每条经验有完整的生命周期追踪。

<!-- STDD-MARKER:capability name="ci-check-enhanced" -->
**2. P5 工具化：CLI 预检扩展（H1）**：新增 3 个子命令 — `ci check-scope`（git diff --stat vs proposal 范围）、`ci check-coverage`（pytest --cov 解析）、`ci check-contracts`（相邻 capability 字段校验）。11 类失败检查覆盖从 ~60% 提升到 ~80%。

<!-- STDD-MARKER:capability name="session-resume" -->
**3. 跨 Session 状态恢复（H2）**：`.stdd.yaml` 新增 `resume_context` / `active_slice` / `last_action` / `last_modified` 字段。Agent 跨 session 后读取即可无歧义恢复。

### P1 — 平台适配 + 覆盖补全（6 项，6.7d）

<!-- STDD-MARKER:capability name="community-experience-pool" -->
**4. 社区经验共享池（O2）**：`stdd experience pull <pack-name>` 从社区下载经验包。经验条目增加投票（useful/unuseful）和采纳次数元数据。导出经验时自动脱敏（路径/IP/域名/专有名词替换为占位符）。

<!-- STDD-MARKER:capability name="parallel-slice-guide" -->
**5. 并行切片执行指南（H3）**：`build.md` skill 增加并行执行策略。同一 `parallel_group` 的切片可并行派发到多个 subagent，主 agent 负责协调和 merge。纯 skill 指令增强，零 CLI 改动。

<!-- STDD-MARKER:capability name="gate-file-confirm" -->
**6. Gate 文件确认通道（H4）**：新增 `stdd gate approve <change-name> --gate <N>` CLI 命令。在 change 目录创建 `GATE<N>_APPROVED` token 文件即可确认 Gate，与对话确认等效。底层统一写入 `.stdd.yaml` 的 `confirmed_at` 时间戳。

<!-- STDD-MARKER:capability name="extract-proposal-extended" -->
**7. extract-proposal 扩展字段（H5）**：从 proposal.md 的 STDD-MARKER 注释中提取 4 个新字段 — Constraints / Stakeholders / RiskAreas / NonGoals。`--format json` 输出包含完整字段集，减少 AI 模板填充时的理解偏差。

<!-- STDD-MARKER:capability name="non-code-change-support" -->
**8. 非代码类 Change 支持（P1+P2）**：`verify.md` 增加条件分支 — 如果 change 不含代码文件，切换 5 项替代检查维度（链接有效性/文件范围一致性/引用可达性/内容完整性/TC 目视验证）。经验库 YAML 增加 `project_type` 字段（python/go/static_site/docs/config），防止跨类型经验污染。

## Capabilities（汇总）

| # | Capability | 优先级 | 工时 | 类型 |
|---|-----------|--------|------|------|
| C1 | experience-lifecycle | P0 | 2d | CLI + 数据模型 |
| C2 | ci-check-enhanced | P0 | 3d | CLI |
| C3 | session-resume | P0 | 0.5d | 数据模型 |
| C4 | community-experience-pool | P1 | 3d | CLI + 数据模型 |
| C5 | parallel-slice-guide | P1 | 0.5d | Skill |
| C6 | gate-file-confirm | P1 | 1.5d | CLI + Skill + Config |
| C7 | extract-proposal-extended | P1 | 1d | CLI |
| C8 | non-code-change-support | P1 | 0.7d | Skill + 数据模型 |

## Success Criteria

1. 经验库支持完整生命周期状态机：discovered → verified → deposited → shared → merged → retired
2. `stdd ci check-failures` 覆盖从 60% 提升到 80%（新增 3 项检查可脚本验证）
3. Agent 读取 `.stdd.yaml` 后可在 1 轮内恢复上下文，无需翻找 change 目录
4. `stdd experience pull python` 可从社区池下载经验包
5. Gate 可通过 `stdd gate approve` 或创建 token 文件确认（非对话通道）
6. `stdd extract-proposal --format json` 输出包含 8 个字段（原 4 + 新增 4）
7. 纯前端/文档类 change 的 verify 阶段使用替代检查清单
8. 经验条目包含 `project_type` 标签，加载时按类型过滤
9. `build.md` 包含并行执行策略，AI 在 `parallel_group` 切片中正确并行派发

## Impact

- **修改 CLI 模块**：`ci.py`（扩增） / `experience.py`（扩增） / `extract_proposal.py`（扩增）
- **新增 CLI 模块**：`gate.py`
- **修改数据模型**：`state.py`（`.stdd.yaml` 读写的字段扩展）
- **修改 Skill 文件**：`build.md` / `verify.md`
- **修改配置文件**：`experience.yaml`（community_pool 配置段） / `gates.yaml`（file_confirm 配置段）
- **修改模板**：`proposal.md`（STDD-MARKER 增加新字段标记）
- **回归风险**：现有 15 个 CLI 命令不受影响，现有 154 个测试保持通过

## NonGoals（明确不做）

- 不做社区经验池后端服务（依赖 GitHub Releases 作为存储，`stdd experience pull` 本质是下载 + 解压）
- 不做经验质量自动评分（社区投票机制已足够）
- 不做 CI profile 切换（非代码 change 不需要 CI）
- P2 官方经验包 v1 + 文件驱动阶段切换 → 下一个 change（V2.5.1）
