var SCENARIO_DATA = {
  title: "API 限流",
  subtitle: "技术后端型 — 令牌桶算法 + 中间件架构 + 边界条件处理",
  phases: [
    {
      id: "understand",
      title: "Phase 1: UNDERSTAND — 需求理解",
      sections: [
        { type: "input", content: "/stdd-understand 我们需要为 API 增加速率限制功能" },
        { type: "markdown", title: "proposal.md — 变更提案（结构化展示）", content:
          "<p><strong>Why：</strong>客户反馈 API 接口没有速率限制，被爬虫滥用，影响正常用户访问。</p>" +
          "<p><strong>What Changes：</strong></p><ul>" +
          "<li>新增基于 IP + Token 的限流中间件</li>" +
          "<li>新增限流白名单管理</li>" +
          "<li>新增超限响应（429 + 友好提示）</li></ul>" +
          "<p><strong>Capabilities：</strong></p><ul>" +
          "<li><strong>RateLimiter</strong>：令牌桶限流核心逻辑</li>" +
          "<li><strong>WhitelistManager</strong>：白名单 IP 管理</li>" +
          "<li><strong>RateLimitMiddleware</strong>：请求拦截中间件</li></ul>"
        }
      ],
      gate: { id: "gate1", type: "checkbox", buttonText: "确认 Proposal → 进入 Phase 2", items: [
        "单 IP 每分钟不超过 100 次请求",
        "超限后返回 429 状态码 + Retry-After 头部 + 友好提示信息",
        "支持白名单 IP 不限流"
      ]}
    },
    {
      id: "spec",
      title: "Phase 2: SPEC — 规格设计（最关键的阶段）",
      sections: [
        { type: "markdown", title: "design.md — 关键设计决策", content:
          "<ul>" +
          "<li><strong>算法选型：</strong>令牌桶（Token Bucket）— 允许突发流量，平滑限流</li>" +
          "<li><strong>存储方案：</strong>Redis — 令牌桶 + 过期时间，天然支持分布式</li>" +
          "<li><strong>中间件位置：</strong>认证层之后、业务层之前</li>" +
          "<li><strong>降级策略：</strong>Redis 不可用时降级为本地内存计数 + 放行（优先可用性）</li></ul>"
        },
        { type: "markdown", title: "specs/rate-limit/spec.md — 行为规格", content:
          "<p><strong>Scenario: 正常请求放行</strong></p>" +
          "<p>GIVEN 用户 IP 在限流配额内<br>WHEN 用户发送 API 请求<br>THEN 请求 SHALL 被正常转发到业务层<br>AND 不消耗限流配额</p>" +
          "<p><strong>Scenario: 超限拒绝</strong></p>" +
          "<p>GIVEN 单 IP 在 1 分钟内已发送 100 次请求<br>WHEN 同 IP 发送第 101 次请求<br>THEN 返回 429 状态码<br>AND 响应体包含 Retry-After 头部<br>AND 响应体包含友好提示信息</p>" +
          "<p><strong>Scenario: 令牌自动恢复</strong></p>" +
          "<p>GIVEN 超限 IP 已被拒绝请求<br>WHEN 等待 60 秒后再次发送请求<br>THEN 请求 SHALL 被正常放行</p>"
        },
        { type: "table", title: "test-plan.md — 覆盖矩阵", headers: ["TC-ID", "Scenario", "类型", "覆盖"],
          rows: [
            ["TC-RATE-001", "正常放行", "单元", "✓"],
            ["TC-RATE-002", "超限拒绝", "单元", "✓"],
            ["TC-RATE-003", "白名单", "单元", "✓"],
            ["TC-RATE-004", "令牌恢复", "单元", "✓"],
            ["TC-RATE-005", "多 IP 独立", "集成", "✓"],
            ["TC-RATE-006", "分布式一致性", "集成", "✓"]
          ]
        }
      ],
      gate: { id: "gate2", type: "button", buttonText: "确认设计基线，进入自动执行" }
    },
    {
      id: "slice",
      title: "Phase 3: SLICE — 切片规划",
      sections: [
        { type: "markdown", content:
          "<p>test-plan.md（6 TC）→ 按依赖拆分为 3 个垂直切片：</p>"
        },
        { type: "cards", items: [
            { icon: "1️⃣", label: "S1: 认证中间件基础", desc: "2 TC · 低风险 · 零依赖 · 预估 1h" },
            { icon: "2️⃣", label: "S2: 限流核心逻辑", desc: "3 TC · 中风险 · 依赖 S1 · 预估 2h" },
            { icon: "3️⃣", label: "S3: 白名单管理", desc: "1 TC · 低风险 · 依赖 S1 · 预估 0.5h" }
          ]
        },
        { type: "markdown", content:
          "<p><strong>并行化：</strong>S3 可与 S2 并行开发（均仅依赖 S1）。</p>"
        }
      ]
    },
    {
      id: "build",
      title: "Phase 4: BUILD — TDD 实现",
      sections: [
        { type: "markdown", title: "S2: 限流核心 — RED → GREEN → REFACTOR", content: "" },
        { type: "code", language: "python", title: "🔴 RED — test_rate_limit_exceeded.py（先写测试，预期失败）", content:
          "def test_rate_limit_exceeded():\n" +
          "    limiter = RateLimiter(max_req=100, window=60)\n" +
          "    ip = \"192.168.1.100\"\n" +
          "    # 前 100 次请求应放行\n" +
          "    for _ in range(100):\n" +
          "        assert limiter.is_allowed(ip) == True\n" +
          "    # 第 101 次应被拒绝\n" +
          "    assert limiter.is_allowed(ip) == False\n" +
          "    # 验证返回 429 信息\n" +
          "    result = limiter.check(ip)\n" +
          "    assert result.status_code == 429\n" +
          "    assert \"Retry-After\" in result.headers"
        },
        { type: "code", language: "python", title: "🟢 GREEN — rate_limiter.py（最小实现，测试通过）", content:
          "import time\n" +
          "from collections import defaultdict\n\n" +
          "class RateLimiter:\n" +
          "    def __init__(self, max_req=100, window=60):\n" +
          "        self.max_req = max_req\n" +
          "        self.window = window\n" +
          "        self._buckets = defaultdict(list)\n\n" +
          "    def is_allowed(self, ip: str) -> bool:\n" +
          "        now = time.time()\n" +
          "        bucket = self._buckets[ip]\n" +
          "        # 清理过期令牌\n" +
          "        bucket[:] = [t for t in bucket if now - t < self.window]\n" +
          "        if len(bucket) < self.max_req:\n" +
          "            bucket.append(now)\n" +
          "            return True\n" +
          "        return False"
        },
        { type: "markdown", title: "📝 pending-adjustments.md（自动记录）", content:
          "<p>设计偏离：令牌桶容量从 100 调至 120 以应对正常流量突发。</p>" +
          "<p>原因：压测发现峰值 QPS 可达 115/s，原 100/s 阈值导致误杀。</p>"
        }
      ]
    },
    {
      id: "verify",
      title: "Phase 5: VERIFY — 质量验证",
      sections: [
        { type: "code", language: "bash", title: "测试结果", content:
          "$ pytest tests/ -v --cov=app --cov-report=term\n" +
          "========================== 22 passed in 0.85s ==========================\n" +
          "Name                    Stmts   Miss  Cover\n" +
          "app/middleware/rate_limiter.py   68      4    94%\n" +
          "app/middleware/whitelist.py      24      2    91%\n" +
          "TOTAL                            92      6    93%"
        },
        { type: "markdown", title: "11 类失败模式检查", content:
          "<p>(a) 幻觉行为 ✓ · (b) 范围蔓延 ✓ · (c) 级联错误 ✓ · (d) 上下文丢失 ✓ · (e) 工具误用 ✓<br>" +
          "(f) 运行时行为偏差 ✓ · (g) 管线断链 ✓ · (h) 内容质量偏差 ✓ · (i) 指令衰减 ✓<br>" +
          "(j) 覆盖真空 ✓ · (k) 契约断层 ✓</p>"
        }
      ],
      gate: { id: "gate3", type: "button", buttonText: "确认交付" }
    },
    {
      id: "deliver",
      title: "Phase 6: DELIVER — 交付",
      sections: [
        { type: "code", language: "bash", content:
          "$ git commit -m \"feat(rate-limit): add API rate limiting with token bucket\"\n" +
          "$ git tag v1.1.0\n" +
          "$ stdd archive 2026-05-20-api-rate-limit\n" +
          " 归档完成: archive/2026-05-20-api-rate-limit\n" +
          " Specs 已合并到 specs/"
        },
        { type: "markdown", title: "追溯链演示", content:
          "<p><code>stdd trace TC-RATE-002</code></p>" +
          "<p>TC-RATE-002: 超限拒绝 → Spec: specs/rate-limit/spec.md Scenario 2 → Test: test_rate_limit.py::test_exceed → Code: app/middleware/rate_limiter.py:42 → Design: design.md 决策2</p>"
        }
      ]
    }
  ],
  cta: {
    text: "用 STDD 管理你的下一个需求",
    commands: [
      "git clone https://github.com/leonai42/stdd.git",
      "cd your-project",
      "python /path/to/stdd/bin/stdd init",
      "python /path/to/stdd/bin/stdd install claude-code"
    ],
    copyTarget: true,
    tutorialUrl: "https://github.com/leonai42/stdd"
  }
};
