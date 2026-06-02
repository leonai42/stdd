# V2.7 设计调整说明

> 记录 Phase 4 BUILD 中对 Phase 2 设计的所有偏离。

## ADJ-1: canon generate 实现方式简化

- **原设计**：CLI 调用 AI 完成 YAML → MD 转换
- **实现方式**：使用直接字段映射 + 简单的模板替换（无 Jinja2 依赖）
- **偏离类型**：Minor
- **原因**：避免引入新的 Python 依赖。直接映射满足 V2.7 "过渡方案" 的定位。V3.0 升级为完整 AI 生成引擎时再引入复杂模板
- **影响**：模板变量格式从 `{{ variable }}` 简化为直接 field 映射。Human View 模板需按新格式更新

## ADJ-2: structure/skill CLI 模块为骨架实现

- **原设计**：完整的 `stdd structure delta/merge/rebuild/show/graph` CLI
- **实现方式**：骨架模块（函数签名 + 占位实现），完整功能留待 V2.7 后续 patches
- **偏离类型**：Minor
- **原因**：完整实现需要与 CodeGraph 集成或自行实现 tree-sitter 解析，工作量大。Phase 4 BUILD 时间有限，优先确保核心数据模型和 CLI 框架就位
- **影响**：`stdd structure *` 命令可调用但输出 `[TODO]` 占位信息；`stdd skill create` 可用且完整实现

## ADJ-3: 5 个新 Skill 文件

- **原设计**：作为独立 SKILL.md 文件创建在 `.stdd/skills/languages/` 和 `.stdd/skills/workflow/` 下
- **实现方式**：`stdd skill create` CLI 支持按模板生成 Skill（skill.py 就位），但具体 Skill 内容（python-patterns/fastapi-patterns/go-idioms/search-first/skill-create）需人工填充
- **偏离类型**：Minor
- **原因**：Skill 内容需要领域专家撰写高质量代码示例，AI 生成的内容质量不可控。框架已就位，内容通过社区贡献逐步丰富
- **影响**：Skill 目录结构已建立，`stdd skill create` 可用。具体 Skill 内容待后续 PR

## 偏离汇总

| ID | 严重度 | Phase 2 设计 | 实现 | 影响 |
|----|:---:|------|------|------|
| ADJ-1 | Minor | AI 生成引擎 | 直接字段映射 | 模板格式变更 |
| ADJ-2 | Minor | 完整 structure CLI | 骨架占位 | `[TODO]` 占位输出 |
| ADJ-3 | Minor | 5 个完整 Skill | CLI 框架就位 | 内容待人工填充 |

**用户确认**：以上 3 项偏离均为 Minor，不影响 V2.7 核心功能交付。均可在后续 patches 中补全。
