# STDD V2.9 白皮书

<!-- STDD-MARKER: title -->

## Why

STDD 的细节分散在 33 个 Python CLI 源文件、6 个 Skill 文件、6 个配置模块、13 个文档模板、多个 Markdown 文档中。用户和 AI 代理对 STDD 的全貌都存在认知盲区。

需要一份**详尽、结构化、自包含**的白皮书，把 V2.9 的所有功能、命令、概念、流程、配置全部记录清楚。V2.9 版本先自用，V3.0 时随正式发布对外公开。

## What Changes

- 新增 `STDD_WHITEPAPER_V2.9_CN.md`：中文人类阅读版（~5000 行，11 Parts，~64 章）
- 新增 `STDD_WHITEPAPER_V2.9_CN_AI.md`：中文 AI 优化版（AI 工具从人类版提取生成）
- 新增 `STDD_WHITEPAPER_V2.9_EN.md`：英文人类版（中文定稿后翻译）
- 新增 `STDD_WHITEPAPER_V2.9_EN_AI.md`：英文 AI 优化版

## Capabilities

### New
- **白皮书文档体系**：覆盖 STDD 全部 28 个 CLI 命令、6 阶段流程、智能门禁、batch 系统、Canonical YAML、经验库、配置系统、平台适配等
- **双轨白皮书**：人类版（详尽）+ AI 版（紧凑），对人类版做 `canon generate` 式的压缩

## Impact
- **文档**：新增 4 个白皮书文件到项目根目录
- **无代码变更**：纯文档任务

## Constraints
- 中文版先行，英文版在中文定稿后翻译
- AI 版由 AI 工具生成，非人工重写
- V2.9 范围锁定（不涉及 V3.0 规划内容）

## Success Criteria
- [ ] 白皮书覆盖所有 28 个 CLI 命令
- [ ] 白皮书覆盖所有 6 阶段流程细节
- [ ] 白皮书覆盖所有配置模块
- [ ] 中文人类版完成
- [ ] 中文 AI 版生成
- [ ] 英文人类版完成
- [ ] 英文 AI 版生成
