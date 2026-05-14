# STDD V2.0 架构升级 - 技术设计

## Context

STDD V1.4.0 已修复关键 Bug 并完成工程质量基线提升。当前架构：单文件 CLI（700行）、零测试、18 个平台 Skill 手动维护、单文件 config（103行）。V2.0 目标是将 STDD 升级为架构扎实、可测试、可扩展的可靠产品。

**约束条件**：
- 向后兼容：CLI 命令签名不变，已有 change 目录不受影响
- Python 3.10+，不引入重量级依赖（仅 pytest 用于测试）
- `bin/stdd` 入口文件必须保留（用户脚本和文档引用此路径）

## Decisions

### 1. CLI 模块化方案

**方案**：`bin/stdd` 保留为入口文件（~30行），核心逻辑移至 `stdd/cli/` 包。包结构：

```
stdd/cli/
├── __init__.py          # main() 入口
├── finder.py            # _find_change_dir()
├── commands/
│   ├── init.py
│   ├── new.py
│   ├── validate.py
│   ├── status.py
│   ├── archive.py
│   ├── trace.py
│   └── install.py
└── utils.py             # 共享工具（YAML读写、输出格式化）
```

**为什么**：每个命令独立模块，可单独测试和修改。`bin/stdd` 保持单行 `from stdd.cli import main; main()` 入口。

**备选方案**：
- 继续单文件 + 测试 — 排除，700 行单文件测试困难，且未来扩展会加剧问题
- 完全独立脚本（每个命令一个可执行文件）— 排除，用户习惯 `stdd <cmd>` 统一入口

### 2. 测试框架

**方案**：pytest + pytest-cov，测试目录 `tests/` 镜像源码结构。

```
tests/
├── conftest.py              # 共享 fixtures（临时目录、示例 change）
├── test_finder.py
├── commands/
│   ├── test_init.py
│   ├── test_new.py
│   ├── test_validate.py
│   ├── test_status.py
│   ├── test_archive.py
│   ├── test_trace.py
│   └── test_install.py
└── test_utils.py
```

**为什么**：pytest 是 Python 标准测试框架，`conftest.py` 提供文件系统隔离（tmp_path）。

**备选方案**：unittest — 排除，pytest 更简洁且已是 STDD 自身规范推荐的框架。

### 3. --dry-run 实现

**方案**：全局 `--dry-run` flag 传递给各命令。命令内部检查此 flag，输出操作描述但不执行文件系统修改。

**为什么**：每个命令的"危险操作"不同（init 写文件、archive 移动目录），统一在命令内部判断比全局拦截更精确。

**备选方案**：全局 mock 文件系统 — 排除，过于复杂且可能隐藏真实问题。

### 4. --verbose 实现

**方案**：引入 Python `logging` 模块替代 `print()`。默认 WARNING 级别（当前行为），`-v` 提升到 INFO，`-vv` 提升到 DEBUG。

```python
import logging
logger = logging.getLogger("stdd")

def cmd_xxx(args):
    logger.info("开始执行...")
    logger.debug("详细参数: %s", args)
```

**为什么**：标准库 logging 模块无额外依赖，支持分级输出。`print()` 保留用于用户可见的最终结果输出。

### 5. rollback 命令

**方案**：`stdd rollback <name>` 执行 archive → changes 的逆向操作：
1. 查找 `archive/<name>` 目录
2. 检查 `changes/` 下无同名目录
3. 移动回 `changes/`，更新 `.stdd.yaml` status 为 active
4. 提示用户已恢复

**为什么**：直接复用 archive 的逆向逻辑，不引入新概念。

### 6. diff 命令

**方案**：`stdd diff <name>` 读取指定 change 的 `test-plan.md`，输出 TC 覆盖差异表：

```
📊 Spec→Test 覆盖差异: my-feature
Spec Scenario              TC-ID        测试函数           源码
─────────────────────────────────────────────────────────────
Scenario: 纯emoji过滤       TC-CSL-001   test_emoji_filter   ✅ _filter_emoji()
Scenario: 混合文本          TC-CSL-002   —                   ❌ 未覆盖
```

**为什么**：基于 `test-plan.md` + grep 源码中的 TC-ID 引用，不需要额外数据源。

### 7. /stdd-abort 实现

**方案**：核心 Skill 中增加 abort 处理逻辑：
1. 用户输入"放弃"或 `/stdd-abort`
2. 确认后清理 change 目录（或移动到 `archive/aborted/`）
3. 更新状态或直接删除

CLI 层面可选增加 `stdd abort <name>` 命令辅助。

**为什么**：当前无标准取消路径，用户只能手动删除目录。

### 8. Skill 自动同步

**方案**：核心 Skill（`.stdd/skills/`）作为唯一来源。`stdd install` 命令：
1. 读取核心 Skill 内容
2. 根据平台模板添加 frontmatter
3. 写入目标平台目录

不再维护独立的平台 Skill 副本文件（`.stdd/platforms/*/skills/`）。

**为什么**：消除 18 个文件的手动同步负担。平台差异仅在于 frontmatter 格式。

**备选方案**：Git submodule/hook 自动复制 — 排除，增加复杂度且不解决根本问题。

### 9. Skill 内容 DRY

**方案**：提取重复内容为共享片段：

```
.stdd/skills/
├── _shared/
│   ├── confirm-gate.md      # 确认门消息模板
│   ├── mode-selection.md    # 模式选择 UI
│   └── long-range-auth.md   # 长程授权清单
├── understand.md            # 引用 _shared/confirm-gate.md
├── spec.md
├── ...
```

Skill 文件通过 `<!-- include: _shared/confirm-gate.md -->` 引用共享片段。AI 读取 Skill 时展开。

### 10. Skill-CLI 桥接

**方案**：Skill 中涉及 CLI 操作的步骤增加前置检查：
```
执行 CLI 操作前：
1. 检查 `python bin/stdd --help` 返回码 = 0
2. 执行 CLI 命令
3. 检查返回码 = 0，非零则报告错误并暂停
```

**为什么**：轻量级桥接，不需要额外基础设施。

### 11. 配置拆分

**方案**：`config.yaml` 拆分为 `config.d/` 目录：

```
.stdd/config.d/
├── project.yaml       # 项目信息 + 版本 + 路径
├── gates.yaml         # 三道门配置
├── long_range.yaml    # 长程模式配置 + 预授权
└── quality.yaml       # 质量检查（test/lint/e2e/coverage/versions）
```

CLI 优先读取 `config.d/`，不存在时 fallback 到 `config.yaml`（向后兼容）。

**为什么**：每个配置文件职责单一，修改时长程模式配置不会误改质量检查配置。

### 12. 长程模式中途退出

**方案**：在 Phase 3-5 的 Skill 中增加退出检测：用户输入"切换普通模式"或"退出长程"时，更新 `.stdd.yaml` 中 `long_range.mode: normal`，当前操作完成后行为切换为普通交互模式。

**为什么**：用户可能在长程自动执行中发现方向不对，需要中途介入。

### 13. validate AND 数量检查

**方案**：在 `cmd_validate` 中增加对每个 Scenario 的 AND 数量统计，超过 5 条产生警告。检查逻辑：统计 `**AND**` 在相邻 `#### Scenario:` 之间的出现次数。

### 14. trace 正则重构

**方案**：放弃跨行 DOTALL 正则，改用逐行解析 test-plan.md：
1. 按 `#### 案例` 分段
2. 每个案例块内提取 `**ID** | TC-XXX-...` 和 `**预期结果** | ...`
3. 匹配 TC-ID

**为什么**：逐行解析对格式变化更宽容，且逻辑更清晰可测试。

### 15. archive 冲突检测

**方案**：合并 specs 前检测目标文件中是否已存在同名 Requirement（以 `### Requirement:` 标题匹配）。若存在则输出警告并询问用户（merge/skip/abort），而非静默追加。

## Architecture

```
STDD V2.0 架构

bin/stdd ──────────> stdd/cli/ ──────────> stdd/cli/commands/
(入口, 30行)         (main + finder)       (7个命令模块)
                          │
                          ├── utils.py (YAML, logging, output)
                          │
                          ▼
                    tests/ (pytest, 15-25文件)
                    
.stdd/
├── config.d/              ← 新增，替代 config.yaml
│   ├── project.yaml
│   ├── gates.yaml
│   ├── long_range.yaml
│   └── quality.yaml
├── skills/
│   ├── _shared/           ← 新增，DRY 共享片段
│   └── *.md
├── templates/
├── standards/
└── platforms/             ← install 命令生成，不再手动维护
```

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|----------|
| 模块化拆分引入 import 循环 | 单向依赖：commands → utils，不允许反向 |
| 配置拆分后旧项目 config.yaml 不可读 | CLI 读取时 fallback 到 config.yaml |
| Skill 自动同步可能生成错误 frontmatter | install 命令增加 --check 模式验证生成结果 |
| 模块化后 `bin/stdd` 入口需要 PYTHONPATH | `bin/stdd` 中动态添加 `sys.path` |
| 测试依赖 pytest 增加安装步骤 | pytest 仅开发依赖，`requirements.txt` 不变（仅 pyyaml） |
| 23 项变更范围大，可能遗漏 | 按 V1.2.1 经验分切片执行，每个切片独立验证 |
