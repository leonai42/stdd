# V2.3 切片执行计划

| # | 优先级 | TC 覆盖 | 实现目标 | 依赖 |
|---|--------|---------|---------|------|
| 1 | P0 | TC-MLANG-001~005 | 创建 4 个语言规范文件（java/go/rust/typescript.md） | 无 |
| 2 | P0 | TC-CONFIG-001~005 | 修改 3 个配置文件（quality/project/long_range.yaml） | 无 |
| 3 | P0 | TC-SKILL-001~002 | `.stdd/skills/` 6 文件添加 frontmatter | 无 |
| 4 | P0 | TC-SYNC-001, 003 | workbuddy 6 文件同步到 V2.2 | 无 |
| 5 | P0 | TC-SYNC-002, 003 | trae 6 文件同步到 V2.2 | 无 |
| 6 | P1 | TC-CURSOR-001, TC-COPILOT-001, TC-AIDER-001 | 新平台适配（cursor/copilot/aider） | 无 |
| 7 | P1 | TC-SKILL-003 | 跨平台一致性验证 + YAML 语法校验 | 1, 2, 3, 4, 5, 6 |

> 切片 1-6 无相互依赖，可任意顺序执行。切片 7 依赖所有前序切片完成。
