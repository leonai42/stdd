# V2.10 切片执行计划

## Dependency Graph Summary

```
所有 7 个 capability 均为零依赖节点，无交叉依赖：

  ┌──────────────────────────────────────────────────────────┐
  │                并行组 1（全部可并行）                       │
  │                                                          │
  │  platform-codex    lang-javascript   lang-c   lang-kotlin │
  │  lang-swift        lang-dart         platform-sync       │
  │                                                          │
  └──────────────────────┬───────────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────────┐
  │  切片 5: 交叉验证（依赖切片 1-4 全部完成）                   │
  │  TC-LANG-006 跨语言一致性 + TC-SYNC-003 回归测试            │
  └──────────────────────────────────────────────────────────┘
```

**并行化说明**：
- 切片 1-4 均为零依赖，可完全并行开发
- 切片 5 依赖切片 1-4 的产出物，串行执行

## Slice Execution Plan

| # | 优先级 | 风险 | 预估工时 | TC 覆盖 | 实现目标 | 依赖 |
|---|--------|------|---------|---------|---------|------|
| 1 | P0 | 🟡 Med | L | TC-CODEX-001~004 | install.py platform_map + `.stdd/platforms/codex/` 6 skill 文件 | 无 |
| 2 | P0 | 🟢 Low | M | TC-LANG-001~003 | `.stdd/standards/{javascript,c,kotlin}.md` | 无 |
| 3 | P0 | 🟢 Low | M | TC-LANG-004~005 | `.stdd/standards/{swift,dart}.md` | 无 |
| 4 | P0 | 🟢 Low | M | TC-SYNC-001~002 | EXTENDING.md + AGENTS.md + STDD.md + README 文档更新 | 无 |
| 5 | P1 | 🟢 Low | S | TC-LANG-006, TC-SYNC-003 | 跨语言一致性检查 + 回归测试 | 1, 2, 3, 4 |

## Rationale

### Slice 1: platform-codex（P0，先行）
- **依赖关系**：零依赖 — 纯增量添加 install.py 条目 + 新建 platform 目录
- **风险分析**：中风险 🟡 — Codex skill 格式是首次实现（新平台模式），经验库提示「contract_gap」风险（字段名不一致）
- **工作量估算**：L — 需修改 1 个核心文件（install.py）+ 创建 6 个 skill 文件 + SKILL_META 扩展
- **实现策略**：先修改 install.py（code 变更），后生成 platform 文件（内容生成）

### Slice 2: 语言规范 Batch 1（P0，可并行）
- **依赖关系**：零依赖 — JavaScript/C/Kotlin 三份独立 markdown 文件
- **风险分析**：低风险 🟢 — 遵循 python.md 模板，C/C++ 分区已确认方案
- **工作量估算**：M — 3 个文件 × ~150 行 ≈ 450 行，纯文档内容编写
- **选组理由**：JavaScript 和 Kotlin 有类型系统相似性（JS+JSDoc ≈ Kotlin+null safety），C 独立

### Slice 3: 语言规范 Batch 2（P0，可并行）
- **依赖关系**：零依赖 — Swift/Dart 两份独立 markdown 文件
- **风险分析**：低风险 🟢 — 遵循 python.md 模板，Flutter/iOS 约定已有明确 spec
- **工作量估算**：M — 2 个文件 × ~150 行 ≈ 300 行
- **选组理由**：Swift 和 Dart 均为移动端语言，Flutter 跨平台与 SwiftUI 有可比性

### Slice 4: platform-sync 文档同步（P0，可并行）
- **依赖关系**：零依赖 — 纯文档编辑，不涉及代码逻辑
- **风险分析**：低风险 🟢 — 简单的数字更新 + 表格添加
- **工作量估算**：M — 5 个文件修改（EXTENDING.md + AGENTS.md + STDD.md + README.md + README_EN.md）
- **实现策略**：先更新 EXTENDING.md（平台表格），再同步更新 AGENTS.md/STDD.md/READMEs 的平台语言计数

### Slice 5: 交叉验证 + 回归（P1，最后执行）
- **依赖关系**：依赖切片 1-4 全部完成 — 需要所有新文件和修改文件就位
- **风险分析**：低风险 🟢 — 机械性检查
- **工作量估算**：S — 运行 grep 验证 + pytest 回归
- **验证内容**：10 个语言规范文件 7 章结构一致性、AGENTS.md vs STDD.md 计数一致、已有平台安装回归
