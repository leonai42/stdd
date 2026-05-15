# STDD 基础配套完善 — 技术设计

## Context

STDD V2.2 当前状态：
- `.stdd/standards/` 仅有 `python.md`（146行，7章节6维度）
- `.stdd/platforms/` 有 3 个平台：claude-code（V2.2完整）、workbuddy（V2.0，缺失11项特性）、trae（V2.0，同workbuddy）
- `.stdd/skills/` 6个master文件无YAML frontmatter，不能作为独立Skill加载
- `quality.yaml` 中 `typecheck: null`、`e2e.critical_paths: []` — Phase 5 的 Step 1d 和 E2E 关键路径检查被跳过
- `project.yaml` 缺少 `source_dir` — 覆盖率诊断无法精确定位变更范围

## Decisions

### 1. 语言规范结构：沿用 python.md 的 6 维度模板

**方案**：Java/Go/Rust/TypeScript 规范均采用 python.md 的 7 章结构（代码风格、类型系统、异步/并发、错误处理、日志、测试、审查清单），每章按语言特性定制。

**为什么**：6维度已在 V2.1/V2.2 实践中验证有效，覆盖了 STDD Phase 4 Step 0 "学习规范"和 Phase 5 Step 2 "Diff审查"所需的所有检查维度。跨语言一致的结构降低 AI 切换语言的认知成本。

**备选方案及排除原因**：
- 每语言独立结构：灵活但失去跨语言一致性，STDD skill 需要额外逻辑判断读哪章
- Google/Microsoft 公开 style guide 引用替代：外部链接不稳定，且不包含 STDD 特有的测试规范和审查清单

### 2. 平台同步策略：以 claude-code 为 gold source 全量覆写

**方案**：workbuddy/trae 的 skill 文件以 claude-code 平台版本为基准全量同步内容，仅保留各平台独有的 YAML frontmatter 格式差异（workbuddy 有 `version` 和 `trigger_keywords` 字段，trae 无 frontmatter）。

**为什么**：当前差异计数 workbuddy/trae 各仅 4 个 V2.2 特征 vs claude-code 15 个，差异过大无法做增量 diff。全量覆写最高效且保证一致性。

**备选方案及排除原因**：
- 逐项 diff 手动合并：12 个文件 × 每个文件多处差异，人工出错概率高
- 自动脚本同步：需要额外维护脚本逻辑，且目前平台数量少（3个），全量覆写即可

### 3. 新平台适配方式：最小化适配，渐进增强

**方案**：三个新平台（Cursor/Copilot/Aider）各提供最小可用适配文件，不追求首次即覆盖所有 STDD 特性。Cursor 提供 `.cursor/rules/stdd.md` 规则文件，Copilot 提供 `.github/copilot-instructions.md`，Aider 提供 `CONVENTIONS.md`。后续按用户反馈增量改进。

**为什么**：新平台的实际使用模式需要通过实践验证，过早做完整适配可能方向错误。最小化适配确保可工作 + 可演进。

**备选方案及排除原因**：
- 一次性做完整的 6 阶段适配（如 claude-code）：工作量大且缺乏实际使用反馈，可能做无用功
- 只做 README 说明不做实际文件：没有可用产出，不符合 "platform support" 承诺

### 4. 配置补完值选择：项目级通用默认值

**方案**：
- `typecheck: "mypy app/"` — Python 项目默认，非 Python 项目覆盖
- `critical_paths: ["tests/e2e/test_critical_flow.py"]` — 示例路径，项目初始化时替换
- `source_dir: "app"` — Python 项目默认源码目录
- `degradation` 段提取到 `long_range.yaml`，增加 `safety_check: true` 和 `pass_rate_threshold: 0.95`

**为什么**：这些值使 Phase 5 的各检查步骤有实际可执行的命令而非 null/[]，消除 "跳过步骤" 的系统性盲区。

**备选方案及排除原因**：
- 保持 null/[] 作为"需用户配置"的信号：实践中用户不会主动配置，导致 Phase 5 步骤永久跳过
- 每种语言各一套默认值：当前 STDD 主要服务 Python 项目，多语言配置矩阵可以后补

### 5. Master Skill frontmatter 标准化：对齐 claude-code 格式

**方案**：`.stdd/skills/` 下 6 个文件添加 YAML frontmatter，最小字段集 `name` + `description`，与 claude-code 平台版本保持一致。不引入 `version`、`trigger_keywords` 等扩展字段（保持最小兼容）。

**为什么**：claude-code 是 STDD 的主要运行平台，master 与 primary platform 格式一致是最低摩擦选择。其他平台可通过各自 frontmatter 扩展。

**备选方案及排除原因**：
- 使用 workbuddy 格式（含 version + trigger_keywords）：workbuddy 不是主平台，且 `trigger_keywords` 在其他平台无意义
- 自定义独立 frontmatter 格式：增加不必要的格式分歧

## Architecture

```
.stdd/
├── standards/                    # 语言规范（本次重点）
│   ├── python.md                 # [已有] Python 规范
│   ├── java.md                   # [新增] Java 规范
│   ├── go.md                     # [新增] Go 规范
│   ├── rust.md                   # [新增] Rust 规范
│   └── typescript.md             # [新增] TypeScript 规范
│
├── platforms/                    # 平台适配（本次重点）
│   ├── claude-code/skills/       # [已有] V2.2 完整 → gold source
│   ├── workbuddy/skills/         # [修改] V2.0 → V2.2 同步
│   ├── trae/skills/              # [修改] V2.0 → V2.2 同步
│   ├── cursor/                   # [新增] Cursor 规则适配
│   │   └── rules/
│   │       └── stdd.md
│   ├── copilot/                  # [新增] GitHub Copilot 适配
│   │   └── copilot-instructions.md
│   └── aider/                    # [新增] Aider 适配
│       ├── CONVENTIONS.md
│       └── .aider.conf.yml
│
├── skills/                       # Master Skill（本次重点）
│   ├── understand.md             # [修改] 加 frontmatter
│   ├── spec.md                   # [修改] 加 frontmatter
│   ├── slice.md                  # [修改] 加 frontmatter
│   ├── build.md                  # [修改] 加 frontmatter
│   ├── verify.md                 # [修改] 加 frontmatter
│   └── deliver.md                # [修改] 加 frontmatter
│
└── config.d/                     # 配置（本次重点）
    ├── quality.yaml              # [修改] typecheck + critical_paths
    ├── project.yaml              # [修改] + source_dir
    └── long_range.yaml           # [修改] + degradation 段
```

数据流：`proposal.md` → `design.md`（本文件）→ 各 capability spec → 实现

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|----------|
| 新语言规范缺乏对应语言实战验证 | 标注 "Initial version — validated on Python patterns, language-specific review needed"，后续在实际项目中迭代 |
| workbuddy/trae 全量覆写后可能丢失平台特有配置 | 覆写前对比 frontmatter 差异，仅覆写内容体，保留各平台 frontmatter |
| Cursor/Copilot/Aider 平台规则格式可能随版本变化 | 文件头部标注适配的平台版本和目标格式版本 |
| 4 种语言 × 150 行 ≈ 600 行新内容，质量难以逐一审查 | 每种语言规范按同一模板生成，用 python.md 做交叉校验 |
| `.stdd/skills/` 加 frontmatter 后与现有 frontmatter 的文件形成两个"主版本" | 明确 `.stdd/skills/` 为唯一 master，platform 版本为派生副本 |
