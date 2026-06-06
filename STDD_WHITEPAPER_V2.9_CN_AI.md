# STDD V2.9.3 白皮书（AI 检索版）

> 从人类版压缩生成。紧凑格式，供 AI 大模型快速检索关键信息。
> 详细内容见 `STDD_WHITEPAPER_V2.9_CN.md`。

---

## 速查索引

### 命令速查
| 命令 | 子命令 | 关键参数 | Phase | 功能 |
|------|--------|---------|-------|------|
| `init` | | `--force` | — | 初始化项目 |
| `new` | | `<name>`, `--parallel` | P1 | 创建 change |
| `validate` | | `[name]` | — | 验证 change 结构 |
| `status` | | `[name]` | — | 工件完成状态 |
| `archive` | | `<name>`, `--yes`, `--skip-specs` | P6 | 归档 change |
| `trace` | | `<tc-id>` | — | 追溯 spec↔test↔code |
| `install` | | `<platform>` | — | 安装 Skills 到平台 |
| `rollback` | | `<name>` | — | 恢复归档 change |
| `diff` | | `[name]` | — | 覆盖差异表 |
| `abort` | | `<name>`, `--yes` | — | 放弃变更 |
| `extract-proposal` | | `[name]`, `--format json\|yaml` | P2 | 结构化提取 proposal |
| `dependency-graph` | | `[name]`, `--format text\|json\|dot` | P3 | 依赖图 |
| `ci` | `init`,`generate`,`check-*` | `<target>`,`[name]` | P5 | CI/CD 管理 |
| `experience` | `list`,`add`,`stats`,`export`,`pull`,`verify`,`deposit`,`retire`,`curate` | 多参数 | P5 | 经验库 |
| `state` | | `[name]`,`--resume`,`--compact`,`--set` | 通用 | 跨 Session 状态 |
| `gate` | `approve` | `--gate 1\|2\|3` | P1/2/5 | Gate 确认 |
| `proposal` | `init`,`validate`,`show` | `[change_name]` | P1 | Canonical proposal |
| `canon` | `init`,`generate`,`verify` | `--change`,`--type`,`--all` | P2/6 | 双轨文档 |
| `index` | `update`,`show`,`trace` | `[target]`,`<file>` | 通用 | 项目索引 |
| `agent` | `verify` | `[task]`,`--cp` | P5 | Agent 验证 |
| `hooks` | `install`,`status`,`uninstall` | `--force` | 通用 | 生命周期 Hooks |
| `structure` | `delta`,`merge`,`rebuild`,`show`,`graph` | `<change>` | P4 | 代码结构 |
| `skill` | `create` | `[name]`,`--type` | 通用 | Skill 创建 |
| `fix` | | `--level 1\|2\|3` | P5 | 自动修复 |
| `upgrade` | | `--check`,`--all`,`--lock`,`--unlock`,`--yes` | 通用 | 版本升级 |
| `batch` | `open`,`add`,`close`,`archive`,`list`,`status` | `"描述"`,`--strategy` | P4 | 批次管理 |
| `guard` | `check`,`status`,`init`,`disable`,`enable` | `--platform`,`--strict`,`--quiet` | 通用 | 智能门禁 |

### 配置速查
| 文件 | 关键字段 |
|------|---------|
| `project.yaml` | `stdd_version`, `project.{name,language}`, `enforce_stdd`, `allow_bypass` |
| `gates.yaml` | `gates.phase{1,2,5}`, `confirmation.channels` |
| `long_range.yaml` | `long_range.{recommended,pre_auth,degradation}` |
| `quality.yaml` | `verify`, `review`, `test`, `quality`, `pass@k` |
| `experience.yaml` | `experience.{auto_record,auto_load}`, `lifecycle`, `community` |
| `lite.yaml` | `scoring.{dimensions,thresholds}`, `scaling`, `batch`, `task_types` |
| `version.yaml` | `stdd_version`, `locked`, `installed_at`, `upgraded_at`, `source_path` |

### Gate 速查
| Gate | Phase | 确认内容 | 通道 |
|------|-------|---------|------|
| 1 | P1结束 | proposal: 范围/边界/成功标准 | dialog / file_token / cli |
| 2 | P2结束 | design + spec: 技术决策 | dialog / file_token / cli |
| 3 | P5结束 | test-report + 设计调整 | dialog / file_token / cli |

Gate 顺序强制，不可跳过。三道通道等价。

### Mode 速查
| 模式 | 评分 | P2 | P3 | P4 | P5 | P6 |
|------|------|----|----|----|----|----|
| lightweight | 0-3 | 简化 | 跳过 | 简化TDD | 1代理+5模式 | 批次追加 |
| standard | 4-7 | 完整 | 智能切片 | 完整TDD | 3代理+12模式 | 完整归档 |
| thorough | 8+ | 完整+高级 | 并行化 | TDD+pass@k | 3代理+安全+性能 | 完整+发行说明 |
| **TDD基线** | **全部** | | | **RED→GREEN必须** | | |

### task_type 速查
| type | SPEC产出 | VERIFY策略 |
|------|---------|-----------|
| `code` | spec.yaml + agent_spec.yaml | pytest+coverage+lint |
| `documentation` | agent_spec.yaml | content+references |
| `configuration` | agent_spec.yaml | config_validation |
| `data-migration` | agent_spec.yaml | data_integrity |
| `dependency-upgrade` | agent_spec.yaml | compatibility |

### 失败模式速查 (a-l)
| ID | 名称 | 检测触发 |
|----|------|---------|
| (a) | 幻觉动作 | grep找不到引用的路径/变量 |
| (b) | 范围蔓延 | git diff --stat 超出声明文件 |
| (c) | 级联错误 | 裸except Exception/空列表默认值 |
| (d) | 上下文丢失 | 代码 vs spec交叉对比 |
| (e) | 工具误用 | 命令语法错误/版本不匹配 |
| (f) | 运行时偏差 | 测试覆盖够但E2E失败 |
| (g) | 管道断裂 | 数据流不完整 |
| (h) | 内容质量 | 输出格式不符spec |
| (i) | 指令衰减 | 对比prompt指令vs实际产出 |
| (j) | 覆盖真空 | coverage 0% |
| (k) | 契约断层 | API定义vs实际调用不一致 |
| (l) | 锚定不足 | anchoring评估结果不够 |

轻量仅 (a)(b)(c)(e)(f)。

### 锚定速查 (L1-L4)
| 等级 | 内容 | 适用 |
|------|------|------|
| L1 | THEN中SHALL强制行为，≥1 Scenario | 所有变更（默认） |
| L2 | 函数签名/API契约/数据schema | 跨系统接口 |
| L3 | 引用已验证的实现模式 | 安全关键 |
| L4 | 参考实现代码（baseline） | 金融/合规 |

---

## 核心流程（压缩版）

### Phase 1: UNDERSTAND
```
问题探索→读模板→起草proposal.yaml→自动审查→复杂度评分→Gate1确认
```
产出: proposal.yaml, .stdd.yaml。复杂度: 6维度0-17分。0-3=轻量,4-7=标准,8+=彻底。

### Phase 2: SPEC
```
CLI提取→经验加载(≤10条)→design.md→spec.yaml+agent_spec.yaml→锚定→test-plan.md→Gate2+模式选择
```
coding: spec.yaml(Scenario: GIVEN/WHEN/THEN/AND)+agent_spec.yaml。non-coding: agent_spec.yaml(CP即规格)。Gate2锁定mode。

### Phase 3: SLICE
```
读spec→5步分析(依赖/风险/工作量/分组/并行)→拓扑排序→slices.md+tasks.md
```
轻量跳过。长程自动进P4。

### Phase 4: BUILD
```
Step-1:上下文预算(>80%提示)→Step0:加载标准/规则/phase-context/经验/structure delta→Step1:逐切片RED→GREEN→REFACTOR→Step1.4:切片验证(TC覆盖100%)→Step1.5:并行合并
```
偏离: minor→auto_record, major→暂停。pending-adjustments.yaml记录。

### Phase 5: VERIFY
```
Step-1:上下文→Step0:多代理审查(security/perf/compat)→Step1:pytest/coverage/ruff/mypy/multi-version/E2E→Step2:diff→Step3:12失败模式→Step4:adjustments汇总→Step5:Gate3
```
迭代上限: 轻量3/标准5/彻底10。

### Phase 6: DELIVER
```
archive→合并specs→合并canon YAML→canon verify→structure merge→git tag
```
轻量:批次追加, 标准:完整归档, 彻底:+发行说明。

---

## 关键机制

### Guard 四级分类器
micro(<3分): fix,bug,typo...→建议batch | small(3-9): 优化,UI...→batch OK | medium(10-19): 重构,模块...→batch警告 | large(≥20): 重写,架构,API...→batch拒绝→full STDD
文件>5警告,>10阻止。打开>2h警告。exit 0=允许 2=阻止。

### Batch
`open(含scope校验)→编辑(guard放行)→add→close→archive`。策略: monthly/weekly/count_based。碰撞:同日→+HHMM。

### 双轨文档
Canonical YAML(AI)→canon generate→Human View MD(人)。5 YAML+1 .canon-index.yaml。单向生成。DC-HASH嵌入。

### 经验库 5态
discovered→verified(occur≥2,conf≥0.7)→deposited(occur≥3,conf≥0.8)→shared→merged。retired(730d)。权重: human=0.95 ci=0.85 ai=0.60 community=0.50。

### Hooks
SessionStart(输出active change)→PreCompact(保存last_modified)→Stop(经验库统计)。`stdd hooks install --force`。

### 长程模式
Gate2后→P3-5预授权→Gate3强制。降级: 3次连续失败|<95%通过率。

### 复杂度评分
6维度×3权重(文档×2),0-17分。0-3轻量,4-7标准,8-17彻底。

### 上下文工程
phase-context.md(≤200行)。`stdd state --resume --compact`→1行恢复。git HEAD对比→FRESH/STALE。

### 平台
Claude Code: PreToolUse硬门禁+SessionStart/PreCompact/Stop。Cursor/Windsurf/Copilot: 规则注入软约束。

---

## Canonical YAML Schema（全字段）

### proposal.yaml
```
meta:{change_id,title,created,status,version} why:{problem} what_changes:[{description}]
capabilities:{new:[],modified:[]} constraints:[] stakeholders:[] risk_areas:[]
non_goals:[] critical:[] anchoring:{level,justification} success_criteria:[]
```

### spec.yaml
```
meta:{capability,change_id,created,confidence} requirements:[{id:REQ-XXX,description,
scenarios:[{id:SC-XXX,confidence,evidence,given,when,then(SHALL),and[]}]}]
```

### agent_spec.yaml
```
meta:{task_id,change_id,created,task_type,system,description} preconditions:[]
steps:[{id:CP-XX,description,action,assertions:[{type,expect}]}]
```

### pending-adjustments.yaml
```
meta:{change_id,updated_at} adjustments:[{id:ADJ-XXX,original,actual,reason,severity,impact_scope,recorded_at}]
```

### design-adjustments.yaml
```
meta:{change_id,generated_at,requires_re_spec} summary:{total_adjustments,minor,major}
categories:[] adjustments:[{id,original,adjusted,reason,severity,resolved_in_phase}]
```

### .canon-index.yaml
```
version:"2.9" proposals:{} designs:{} specs:{code:{},agent:{}}
```

---

## .stdd.yaml 完整字段

| 字段 | 类型 | 默认 | 写 | 读 |
|------|------|------|----|-----|
| change_id | str | — | new | 全局 |
| status | str | active | new,archive,abort,rollback | guard,validate |
| current_phase | str | understand | new,state | guard,status,state |
| task_type | str | code | new,user | guard,spec |
| mode | str | standard | new,Gate2 | build,verify |
| complexity_score | int\|null | null | understand | spec |
| score_confidence | str\|null | null | understand | spec |
| phases.<p>.status | str | pending | phases | 全局 |
| phases.<p>.confirmed_at | str\|null | null | gate | validate |
| long_range.enabled | bool | false | Gate2 | build,verify |
| traceability.{spec_scenarios,tc_cases,test_functions} | int | 0 | spec,build | validate,trace |
| design_adjustments.count | int | 0 | build,verify | verify |
| resume_context | str\|null | null | state | state |
| active_slice | str\|int\|null | null | state | state |
| last_action | str\|null | null | state,hooks | state |
| last_modified | str\|null | null | state,hooks | state |
| active_phase | str\|null | null | state | state |
| phase_context_file | str\|null | null | state | state |
| state_freshness.{verified_at,git_head} | str\|null | null | hooks | state |

---

## 版本演进

| 版本 | 核心 |
|------|------|
| V1.0 | 6-Phase+7CLI |
| V2.0 | CLI模块化+10命令+测试 |
| V2.4 | 经验库+CI+依赖图+提取 |
| V2.5 | 跨Session状态+Gate CLI+锚定 |
| V2.7 | 上下文工程+双轨+Agent验证+Skill+Hooks |
| V2.8 | Plankton+结构摘要+pass@k+12模式 |
| V2.9 | 轻量+复杂度+批次+升级+task_type |
| V2.9.2 | Canonical扩展+强制门+YAML-First |
| V2.9.3 | 智能门禁+batch open/add/archive+Hooks deploy+--compact |

---

> **AI 检索版**，从 `STDD_WHITEPAPER_V2.9_CN.md` 压缩生成（Stage B）。
