# 技能层版本自检 + Skill-Only 升级路径 — 切片执行计划

## Dependency Graph Summary

```
Slice 1: Foundation (C1+C2)
  ├── .stdd/skills/_shared/version-check.md
  └── install.py: stdd_version frontmatter injection
         │
         ├──────────────────────┐
         ↓                      ↓
Slice 2: Phase Skills (C3)    Slice 3: Upgrade Skill (C4+C5+C6)
  6 phase skill updates        upgrade.md + SKILL_META
         │                      │
         └────────┬─────────────┘
                  ↓
          Slice 4: Unit Tests
            test_install.py
                  │
                  ↓
          Slice 5: E2E Verify
            行为验证 19 TC
```

**并行化说明**：
- 并行组 1：Slice 1（唯一零依赖节点，先行）
- 并行组 2：Slice 2 + Slice 3（均依赖 Slice 1，互相独立，可并行）
- 并行组 3：Slice 4（依赖 Slice 1+3）
- 并行组 4：Slice 5（依赖全部 Slice）

## Slice Execution Plan

| # | 优先级 | 风险 | 预估工时 | 并行组 | TC 覆盖 | 实现目标 | 依赖 |
|---|--------|------|---------|--------|---------|---------|------|
| 1 | P0 | 🟢 Low | S | 组1 | TC-PSI-002 | `_shared/version-check.md` + install.py frontmatter stdd_version 注入 | 无 |
| 2 | P0 | 🟡 Med | M | 组2 | TC-VC-001~006 | 6 个 phase skill 增加 Step 0 + stdd_version | 1 |
| 3 | P0 | 🟡 Med | M | 组2 | TC-UP-001,002,005,009,010, TC-PSI-001,003 | `upgrade.md` 技能 + install.py SKILL_META 扩展 | 1 |
| 4 | P0 | 🟢 Low | S | 组3 | TC-PSI-001~003 | install.py 单元测试 | 1,3 |
| 5 | P1 | 🟡 Med | M | 组4 | TC-VC-001~006, TC-UP-001~010 | 端到端行为验证 | 1,2,3,4 |

## Rationale

### Slice 1: Foundation（P0，先行）
- **依赖关系**：无依赖。`_shared/version-check.md` 是所有后续切片的共享基石；`install.py` 的 `stdd_version` 注入机制是 C1 的核心实现。两者无互相依赖，在同一 Slice 完成。
- **风险分析**：低风险。version-check.md 是纯文档片段，不含可执行代码。install.py 改动仅增加一个 YAML 字段，不改变现有函数签名。
- **工作量估算**：S（2 个文件创建/修改，~40 行）

### Slice 2: Phase Skills Update（P0，可并行于 Slice 3）
- **依赖关系**：依赖 Slice 1（需要 `_shared/version-check.md` 存在 + `stdd_version` 字段约定）。修改 6 个 phase skill 文件的 frontmatter（加 `stdd_version`）和 Step 0（引用 version-check.md）。
- **风险分析**：中风险。6 个文件需保持一致的修改模式，需仔细 diff review 确保无遗漏。每个改动量小（~10 行/文件），但数量多。
- **工作量估算**：M（6 个文件，~60 行修改）

### Slice 3: Upgrade Skill（P0，可并行于 Slice 2）
- **依赖关系**：依赖 Slice 1（version-check.md 的模式 + `stdd_version` 字段）。`upgrade.md` 是全新文件；install.py 的 SKILL_META 扩展是与 Slice 1 install.py 改动的增量叠加（同一文件但不同函数区域）。
- **风险分析**：中风险。upgrade.md 需准确描述平台检测、GitHub 拉取、文件写入等流程，指令措辞影响 AI 执行质量。install.py SKILL_META 改动简单。
- **工作量估算**：M（1 个新文件 ~120 行 + install.py ~8 行）

### Slice 4: Unit Tests（P0）
- **依赖关系**：依赖 Slice 1 和 Slice 3（测试的是 install.py 的 SKILL_META 和 frontmatter 生成逻辑）。
- **风险分析**：低风险。标准 pytest 测试，逻辑简单（验证 dict 条目存在、验证 frontmatter 字符串包含）。
- **工作量估算**：S（~3 个测试函数，~40 行）

### Slice 5: E2E Verification（P1）
- **依赖关系**：依赖所有前序 Slice。通过实际调用技能和检查文件系统来验证 19 个 TC。
- **风险分析**：中风险。行为验证需要实际触发 AI 技能执行，部分 TC（如 SC-UP-008 网络降级）难以自动化。
- **工作量估算**：M（19 TC 手动/AI 辅助验证）
