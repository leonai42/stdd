# V2.4 切片执行计划

## Dependency Graph Summary

```
依赖拓扑排序（按依赖关系）

Slice A: experience-core (P0)
    │
    ├──→ Slice B: experience-skill (P1)
    │
    ├──→ Slice C: spec-auto-cli (P0) ──→ Slice D: spec-auto-skill (P1)
    │
    ├──→ Slice E: smart-slice-cli (P0) ──→ Slice F: smart-slice-skill (P1)
    │
    └─── Slice G: ci-integration (P0) ─── (独立，可并行)
              │
              └──→ Slice H: integration (P0)
```

**并行化说明**：
- 并行组 1：Slice C + Slice E + Slice G（均依赖 A 完成后可并行进行）
- 并行组 2：Slice D + Slice F（分别依赖 C 和 E 完成后可并行进行）
- H 在所有切片完成后执行

## Slice Execution Plan

| # | 优先级 | 风险 | 预估工时 | 并行组 | TC 覆盖 | 实现目标 | 依赖 |
|---|--------|------|---------|--------|---------|---------|------|
| **A** | P0 | 🟢 Low | 3h (M) | — | TC-EXP-001~011 | experience.py CLI + config + 数据模型 + 索引 | 无 |
| **B** | P1 | 🟡 Med | 1.5h (S) | — | TC-EXP-012~013 | build.md Step 0.5 + verify.md Step 3.5 + test-report 模板 | A |
| **C** | P0 | 🟢 Low | 2h (S) | 组1 | TC-SAC-001~003 | extract_proposal.py CLI + proposal.md 模板标记 | A |
| **D** | P1 | 🟡 Med | 1.5h (S) | 组2 | — | spec.md 技能增强 + spec-draft.md 模板 + spec.md 模板标记 | C |
| **E** | P0 | 🟢 Low | 2h (S) | 组1 | TC-SLI-001~005 | dependency_graph.py CLI | A |
| **F** | P1 | 🟡 Med | 1.5h (S) | 组2 | — | slice.md 技能增强 + slices.md 模板增强 | E |
| **G** | P0 | 🟢 Low | 3h (M) | 组1 | TC-CI-001~008 | ci.py CLI + 4 个模板 + quality.yaml | 无 |
| **H** | P0 | 🟡 Med | 1h (S) | — | 全量回归 | __init__.py 接线 + 全量 pytest + 文档更新 | B, D, F, G |

## Rationale

### Slice A: 经验库核心（P0，先行）
- **零外部依赖**：纯数据层 + CLI，是后续所有切片的基礎
- **低风险**：遵循现有 CLI 模式，YAML 操作使用标准库
- **包含所有 P0 经验测试**：list/add/stats/export 全覆盖

### Slice B: 经验库技能集成（P1）
- **依赖 A 完成**：需要经验数据模型和 CLI 就绪后才能写技能集成文本
- **中风险**：技能文件是核心敏感路径，修改需谨慎

### Slice C+E: CLI 工具对（P0，可并行）
- C（extract-proposal）和 E（dependency-graph）都是独立的 CLI 模块
- 均依赖 A（需要经验库数据层），但彼此独立
- **并行组 1**：可同时开发

### Slice D+F: 技能增强对（P1，可并行）
- D 依赖 C 完成（需要 extract-proposal CLI 就绪）
- F 依赖 E 完成（需要 dependency-graph CLI 就绪）
- **并行组 2**：可同时开发

### Slice G: CI/CD 集成（P0，可并行）
- **零上游依赖**：纯增量功能，不依赖经验库或技能变更
- 可与组 1 并行开发
- 包含所有 P0 CI 测试

### Slice H: 集成（P0，最后）
- 依赖所有功能切片完成
- CLI __init__.py 一次性接线 4 个新命令
- 全量回归测试确保无破坏
