# 测试方案: Hello Greeter

## 测试案例

#### 案例 1 — 早上时段问候

| **ID** | TC-GREETER-001 |
| **优先级** | P0 |
| **预置条件** | 模拟时间为 08:00 |
| **输入** | `python src/greeter.py Alice` |
| **预期结果** | 输出 "早上好, Alice!" |

#### 案例 2 — 下午时段问候

| **ID** | TC-GREETER-002 |
| **优先级** | P0 |
| **预置条件** | 模拟时间为 14:00 |
| **输入** | `python src/greeter.py Bob` |
| **预期结果** | 输出 "下午好, Bob!" |

#### 案例 3 — 深夜通用问候

| **ID** | TC-GREETER-003 |
| **优先级** | P1 |
| **预置条件** | 模拟时间为 23:00 |
| **输入** | `python src/greeter.py Charlie` |
| **预期结果** | 输出 "你好, Charlie!" |

#### 案例 4 — 正式问候

| **ID** | TC-GREETER-004 |
| **优先级** | P1 |
| **预置条件** | 模拟时间为 08:00 |
| **输入** | `python src/greeter.py Alice --formal` |
| **预期结果** | 输出 "尊敬的 Alice，早上好！" |

## 执行矩阵

| 案例 | 自动化 | 状态 |
|------|--------|------|
| TC-GREETER-001 | pytest | 🟢 |
| TC-GREETER-002 | pytest | 🟢 |
| TC-GREETER-003 | pytest | 🟢 |
| TC-GREETER-004 | pytest | 🟢 |
