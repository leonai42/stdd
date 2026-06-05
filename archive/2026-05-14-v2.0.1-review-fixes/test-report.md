# V2.0.1 测试报告

> 测试日期：2026-05-14
> 测试环境：Windows 10, Python 3.12.7, pytest 9.0.3
> 被测版本：V2.0.1-review-fixes

## 一、总体概况

| 指标 | 数值 |
|------|------|
| 测试用例总数 | 54 |
| 通过 | 54 |
| 失败 | 0 |
| 跳过 | 0 |
| 通过率 | 100% |
| 执行耗时 | 0.47s |

## 二、变更文件清单

| # | 文件 | 修复内容 |
|---|------|---------|
| 1 | `stdd/cli/__init__.py` | M1: 异常处理增加 traceback 输出 |
| 2 | `stdd/cli/commands/trace.py` | M5: 尾随管道修复 + M6: 统一案例标题正则 |
| 3 | `stdd/cli/commands/diff.py` | M5: 尾随管道修复 |
| 4 | `stdd/cli/finder.py` | M7: 精确匹配增加 .stdd.yaml 存在性检查 |
| 5 | `stdd/cli/commands/install.py` | M3: 移除 _shared/ 死代码守卫 |
| 6 | `stdd/cli/utils.py` | M4: read_config YAML 类型检查 |
| 7 | `stdd/cli/commands/init.py` | M8: --dry-run 支持 |
| 8 | `stdd/cli/commands/new.py` | M8: --dry-run 支持 |
| 9 | `stdd/cli/commands/rollback.py` | M8: --dry-run 支持 |
| 10 | `stdd/cli/commands/abort.py` | M8: --dry-run 支持 |
| 11 | `.stdd/config.yaml` | H3: 删除旧配置文件 |
| 12 | `.stdd/skills/build.md` | M16: config.yaml → config.d/project.yaml |
| 13 | `.stdd/skills/verify.md` | M16: config.yaml → config.d/ (2处) |
| 14 | `.stdd/skills/spec.md` | M16: config.yaml → config.d/long_range.yaml |
| 15 | `README.md` | H1: 版本号 V2.0 + 新命令 + 结构更新 |
| 16 | `AGENTS.md` | L16: 目录结构更新 + stdd/cli/、config.d/、_shared/ |
| 17 | `changes/.../slices.md` | 切片执行计划 |

## 三、--dry-run 冒烟测试

| 命令 | 状态 |
|------|------|
| `stdd init --dry-run` | 预览正确，未修改文件系统 |
| `stdd new --dry-run test` | 预览正确，未修改文件系统 |

## 四、结论

全部 54 个回归测试通过，无回归问题。17 项修改覆盖评审报告中 1 严重、3 高危、9 中等问题。

待用户执行: `stdd install claude-code` 同步更新已安装的 Skills（H2）。
