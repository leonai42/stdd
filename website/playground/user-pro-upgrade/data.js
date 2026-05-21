var SCENARIO_DATA = {
  title: "用户购买升级 Pro",
  subtitle: "业务功能型 — 支付流程 + 状态机 + 多 Capability 协作",
  phases: [
    {
      id: "understand",
      title: "Phase 1: UNDERSTAND — 需求理解",
      sections: [
        { type: "input", content: "/stdd-understand 用户想要购买Pro服务，完成支付后自动升级为Pro会员，享受Pro权益" },
        { type: "markdown", title: "proposal.md — 业务需求梳理", content:
          "<p><strong>Why：</strong>免费用户无升级路径，流失率高。需要完整的购买→支付→开通→权益链路。</p>" +
          "<p><strong>业务流程：</strong>下单 → 支付 → 回调 → 开通Pro → 到期降级</p>" +
          "<p><strong>What Changes：</strong></p><ul>" +
          "<li>新增订单管理（创建/查询/过期关闭）</li>" +
          "<li>新增支付集成（对接支付网关，幂等性保障）</li>" +
          "<li>新增会员管理（开通/续费/降级）</li>" +
          "<li>新增权益控制（Pro 专属功能开关）</li></ul>" +
          "<p><strong>关键约束：</strong></p><ul>" +
          "<li>支付幂等性 — 重复回调不重复开通</li>" +
          "<li>回调验签 — 防止伪造支付成功通知</li>" +
          "<li>订单超时关闭 — 30 分钟未支付自动取消</li></ul>"
        }
      ],
      gate: { id: "gate1", type: "checkbox", buttonText: "确认 Proposal → 进入 Phase 2", items: [
        "用户可下单购买 Pro 会员（1月/1年）",
        "支付成功后自动开通 Pro 权益",
        "支付失败或超时订单自动关闭",
        "Pro 到期后自动降级为基础版"
      ]}
    },
    {
      id: "spec",
      title: "Phase 2: SPEC — 规格设计（最关键的阶段）",
      sections: [
        { type: "markdown", title: "4 个 Capability 协作关系", content:
          "<p>用户购买升级 Pro 涉及 4 个 capability 的协作：</p>"
        },
        { type: "cards", items: [
            { icon: "📦", label: "order（订单管理）", desc: "创建订单、查询状态、超时关闭" },
            { icon: "💳", label: "payment（支付集成）", desc: "发起支付、回调处理、幂等验签" },
            { icon: "👤", label: "membership（会员管理）", desc: "开通Pro、续费、到期降级" },
            { icon: "⭐", label: "privilege（权益控制）", desc: "Pro功能开关、权益列表查询" }
          ]
        },
        { type: "markdown", title: "跨 Capability 依赖（GIVEN 链）", content:
          "<p><strong>Scenario: 支付回调开通 Pro</strong></p>" +
          "<p>GIVEN 用户已完成支付（payment）<br>" +
          "WHEN 支付网关发送回调通知<br>" +
          "THEN 系统 SHALL 验证签名后开通 Pro 会员（membership）<br>" +
          "AND 激活 Pro 权益（privilege）</p>" +
          "<p><strong>契约定义（payment → membership 回调字段）：</strong><br>" +
          "<code>{ order_id, transaction_id, amount, payer_id, timestamp, signature }</code></p>" +
          "<p><strong>Scenario: 支付超时关闭订单</strong></p>" +
          "<p>GIVEN 订单已创建超过 30 分钟<br>" +
          "AND 订单状态为 pending<br>" +
          "WHEN 定时任务扫描过期订单<br>" +
          "THEN 订单状态 SHALL 变更为 expired<br>" +
          "AND 如果已发起支付 SHALL 调用退款接口</p>"
        },
        { type: "table", title: "test-plan.md — 覆盖矩阵（部分展示）", headers: ["TC-ID", "Capability", "Scenario", "类型"],
          rows: [
            ["TC-ORDER-001", "order", "创建订单", "单元"],
            ["TC-ORDER-002", "order", "超时关闭", "单元"],
            ["TC-PAY-001", "payment", "发起支付", "集成"],
            ["TC-PAY-002", "payment", "回调幂等", "集成"],
            ["TC-PAY-003", "payment", "回调验签", "单元"],
            ["TC-MEM-001", "membership", "开通Pro", "单元"],
            ["TC-MEM-002", "membership", "到期降级", "单元"],
            ["TC-PRIV-001", "privilege", "权益激活", "集成"]
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
          "<p>约 24 TC → 5 个切片，按依赖拓扑排序：</p>"
        },
        { type: "cards", items: [
            { icon: "1️⃣", label: "S1: order（订单管理）", desc: "4 TC · 零依赖 · 预估 2h" },
            { icon: "2️⃣", label: "S2: payment（支付集成）", desc: "6 TC · 依赖 S1 · 预估 3h" },
            { icon: "3️⃣", label: "S3: membership（会员）", desc: "6 TC · 依赖 S2 · 预估 2h" },
            { icon: "4️⃣", label: "S4: privilege（权益）", desc: "4 TC · 依赖 S3 · 预估 1h" },
            { icon: "5️⃣", label: "S5: 定时任务（降级）", desc: "4 TC · 依赖 S1+S3 · 预估 1.5h" }
          ]
        },
        { type: "markdown", content:
          "<p><strong>并行组：</strong>S1 独立先行 → S2 依赖 S1 → S3 依赖 S2 → S4 可与 S5 并行（均依赖 S3 完成）</p>"
        }
      ]
    },
    {
      id: "build",
      title: "Phase 4: BUILD — TDD 实现",
      sections: [
        { type: "markdown", title: "S2: payment — 关键测试（Mock 支付网关）", content: "" },
        { type: "code", language: "python", title: "🔴 RED — test_payment_callback_idempotent.py", content:
          "def test_callback_idempotent(paid_order):\n" +
          "    \"\"\"重复回调不重复开通会员\"\"\"\n" +
          "    callback_data = {\n" +
          "        \"order_id\": paid_order.id,\n" +
          "        \"transaction_id\": \"TXN-001\",\n" +
          "        \"amount\": 29900,  # 299.00 元\n" +
          "        \"payer_id\": \"USR-42\",\n" +
          "    }\n" +
          "    # 第一次回调 → 开通成功\n" +
          "    result1 = payment.handle_callback(callback_data)\n" +
          "    assert result1.status == \"activated\"\n" +
          "    assert membership.is_pro(\"USR-42\") == True\n" +
          "    # 第二次回调（重复）→ 幂等，不重复开通\n" +
          "    result2 = payment.handle_callback(callback_data)\n" +
          "    assert result2.status == \"duplicate\"\n" +
          "    assert membership.pro_since(\"USR-42\") == result1.timestamp"
        },
        { type: "code", language: "python", title: "🟢 GREEN — payment.py 关键实现", content:
          "class PaymentHandler:\n" +
          "    def handle_callback(self, data: dict) -> CallbackResult:\n" +
          "        # 1. 验签\n" +
          "        if not self._verify_signature(data):\n" +
          "            raise InvalidSignatureError()\n" +
          "        # 2. 幂等检查\n" +
          "        txn = self._find_transaction(data[\"transaction_id\"])\n" +
          "        if txn and txn.status == \"processed\":\n" +
          "            return CallbackResult(status=\"duplicate\")\n" +
          "        # 3. 更新订单 → 开通会员 → 激活权益\n" +
          "        with transaction.atomic():\n" +
          "            order = self._mark_paid(data[\"order_id\"])\n" +
          "            membership.activate_pro(data[\"payer_id\"])\n" +
          "            privilege.sync(data[\"payer_id\"])"
        },
        { type: "markdown", title: "📝 pending-adjustments.md", content:
          "<p><strong>支付超时时间调整：</strong>30 分钟 → 15 分钟</p>" +
          "<p>原因：支付网关统计显示 95% 用户在 5 分钟内完成支付，30 分钟导致过多 pending 订单堆积。</p>"
        }
      ]
    },
    {
      id: "verify",
      title: "Phase 5: VERIFY — 质量验证",
      sections: [
        { type: "code", language: "bash", content:
          "$ pytest tests/ -v --cov=app --cov-report=term\n" +
          "========================== 28 passed in 1.24s ==========================\n" +
          "Name                            Stmts   Miss  Cover\n" +
          "app/billing/order.py               42      2    95%\n" +
          "app/billing/payment.py             86      6    93%\n" +
          "app/billing/membership.py          38      3    92%\n" +
          "app/billing/privilege.py           28      2    92%\n" +
          "TOTAL                             194     13    93%"
        },
        { type: "markdown", title: "重点检查：(k) 契约断层", content:
          "<p>验证 payment → membership 回调字段一致性：</p>" +
          "<p>✓ order_id 字段类型一致（UUID string）<br>" +
          "✓ amount 单位一致（分，int）<br>" +
          "✓ payer_id 命名一致（USR-前缀）<br>" +
          "✓ signature 字段顺序一致</p>"
        }
      ],
      gate: { id: "gate3", type: "button", buttonText: "确认交付" }
    },
    {
      id: "deliver",
      title: "Phase 6: DELIVER — 交付",
      sections: [
        { type: "code", language: "bash", content:
          "$ git commit -m \"feat(billing): add Pro upgrade flow with order/payment/membership/privilege\"\n" +
          "$ git tag v2.0.0\n" +
          "$ stdd archive 2026-05-20-user-pro-upgrade\n" +
          " 归档完成: archive/2026-05-20-user-pro-upgrade"
        },
        { type: "markdown", title: "跨 Capability 追溯链", content:
          "<p><code>stdd trace TC-PAY-002</code></p>" +
          "<p>TC-PAY-002: 回调幂等 → 用户点击购买 → order 创建 → payment 发起 → 支付回调 → membership 开通 → privilege 激活</p>" +
          "<p>完整链路：<strong>order</strong> (订单) → <strong>payment</strong> (支付) → <strong>membership</strong> (会员) → <strong>privilege</strong> (权益)</p>"
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
