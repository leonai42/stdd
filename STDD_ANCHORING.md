# STDD Spec 锚定法

> 版本：V2.7 | STDD 方法论核心文档之一

## 为什么需要锚定

LLM 的根本属性：相同输入不保证相同输出。但根因不是"AI 不稳定"——是 **spec 给了 AI 太多自由发挥的空间**。当 spec 精确到"AI 没有发挥空间"时，不可重复性自然消失。

**核心逻辑**：不事后验证 AI 有没有跑偏（Pass@k），而是事前不让 AI 有跑偏的空间（Spec 锚定法）。

## 四级锚定体系

| 锚定等级 | 方法 | 成本 | 适用场景 |
|---------|------|------|---------|
| **L1 · 行为锚定** | spec 的 THEN 用 SHALL 写死所有强制行为 | 无额外成本 | **所有 Change 默认要求** |
| **L2 · 接口锚定** | spec 中附加精确的函数签名/API 契约/数据 schema | 低（多写几行） | 涉及多模块协作的 Change |
| **L3 · 模式锚定** | spec 中引用参考实现模式（如「参照 Change-1 的 TokenSystem 模式」） | 低（引用已有） | 有成熟模式的重复性工作 |
| **L4 · 基准锚定** | spec 中附加一条参考实现代码（Anchor Implementation） | 中（人工编写参考代码） | **关键 Change、安全/金融场景** |

## L1 · 行为锚定（所有 Change 必须满足）

### 要求

1. 每个 Requirement 至少 1 个 Scenario
2. 每个 Scenario 的 THEN 必须包含 **SHALL**（大写），表示强制性行为
3. 所有边界条件必须有对应的 Scenario 覆盖

### 示例

```markdown
### Requirement: API 速率限制

#### Scenario: 超限拒绝
- **GIVEN** 客户端在 60 秒窗口内已发送 100 次请求
- **WHEN** 客户端发送第 101 次请求
- **THEN** 系统 SHALL 返回 HTTP 429 Too Many Requests
- **AND** 响应体 SHALL 包含 `{"error": "rate_limit_exceeded", "retry_after": <seconds>}`
```

## L2 · 接口锚定

### 要求

在 L1 基础上，spec 中附加精确的函数签名、API 契约或数据 schema。

### 示例

```yaml
# anchors/L2-interfaces/<change-name>/api-contract.yaml
endpoints:
  - method: GET
    path: /api/v1/rate-limit/status
    auth: Bearer Token
    response:
      200:
        body:
          remaining: int
          limit: int
          reset_at: string (ISO 8601)
      429:
        body:
          error: string
          retry_after: int
```

## L3 · 模式锚定

### 要求

在 L1/L2 基础上，引用已有 Change 的实现模式。

### 示例

```markdown
> **锚定参考**：参照 Change `2026-05-14-api-rate-limit` 的 `TokenBucket` 实现模式。
> 该模式已在本项目 3 个 Change 中使用，成熟度已验证。
```

## L4 · 基准锚定

### 要求

在 L1/L2/L3 基础上，附加一条完整的参考实现代码。

### 示例

```python
# anchors/L4-baselines/<change-name>/anchor-impl.py
# 参考实现：TokenBucket 令牌桶限流器
import time
from threading import Lock

class TokenBucket:
    """令牌桶限流器 — Anchor Implementation for rate-limit capability."""
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = float(capacity)
        self.refill_rate = refill_rate
        self.last_refill = time.monotonic()
        self.lock = Lock()

    def consume(self, tokens: int = 1) -> bool:
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
```

## 流程集成

在 Phase 2 SPEC 中新增 Step 2.4（锚定评估），仅对 critical Change 触发：

```
- safety_critical=true → 至少 L3；financial=true → 至少 L4
- proposal.anchoring.level ≥ 最低需求 → 通过
- proposal.anchoring.level < 最低需求 → Gate 2 阻塞
```

## 反模式

- ❌ **过度锚定**：一个简单 bug fix 使用 L4 → 浪费
- ❌ **锚定不足**：critical 安全功能使用 L1 → 危险
- ❌ **锚定形式化**：写了 L4 但参考代码与 spec 矛盾 → 形同虚设
