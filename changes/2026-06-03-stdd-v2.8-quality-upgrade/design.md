# STDD V2.8 — 技术设计

> 对应 proposal：19 项（A 6 / B 9 / C 4）
> V2.7 设计模式复用：CLI 命令采用 cmd_* / _dispatch 模式，测试采用 pytest fixture

## A1: pass@k 质量度量

**方案**：Phase 5 增加 `--pass-k N` 参数（默认 1 = 当前行为）。k>1 时重复运行 pytest N 次，统计每次通过/失败。

**实现**：扩展 `stdd/cli/commands/verify.py`（如存在）或新增逻辑到 ci.py。核心逻辑：

```python
def run_pass_k(test_command: str, k: int = 3) -> dict:
    results = []
    for i in range(k):
        result = subprocess.run(test_command, shell=True, capture_output=True)
        results.append(result.returncode == 0)
    return {
        "pass_count": sum(results),
        "total": k,
        "pass_at_1": 1.0 if results[0] else 0.0,
        "pass_at_k": sum(results) / k,
        "details": results,
    }
```

**配置**：`quality.yaml` 新增：
```yaml
pass_k:
  enabled: false
  default_k: 3
  scope: p0_only
```

## A2: Plankton 多级自动修复

**方案**：新增 `stdd/cli/commands/fix.py`。

- L1：`ruff format . && ruff check --fix . && isort .`
- L2：分析 git diff，检测类型注解缺失/异常处理不完整 → 输出建议 diff
- L3：读取 design-adjustments.yaml → 生成修复建议报告

**CLI**：`stdd fix --level 1|2|3 [--dry-run]`

## A3: Two-Instance Kickoff

**方案**：`stdd new <name> --parallel` 创建两个 worktree + 输出启动指令。

```bash
git worktree add .claude/worktrees/<name>-explore
git worktree add .claude/worktrees/<name>-research
```

输出双 Agent 启动指令（供用户在新终端中执行）。不自动启动 Agent（那是 Claude Code 调度器的事）。

## A4: Rules 目录结构

**方案**：创建 `.stdd/rules/common/` + `.stdd/rules/<lang>/`。build.md Step 0.5 增强：

```markdown
### Step 0.5: 加载匹配规则（V2.8 rules-directory）
1. 读取 .stdd/rules/common/ 下所有 .md 文件
2. 根据 project.language 读取 .stdd/rules/<lang>/ 下匹配的规则
3. 注入到 AI 上下文
```

## A5-A6 + B1-B9 + C1-C4

遵循 V2.7 既有设计模式，关键实现点：
- A5：5 个 SKILL.md 文件，每个 80-120 行
- A6：structure.py 实现文件系统操作 + index.md 合并逻辑
- B1-B9：pytest 测试函数，覆盖边界/错误路径
- C1-C4：skill 指令/模板修改
