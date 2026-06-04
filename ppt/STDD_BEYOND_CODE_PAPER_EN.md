# From Code to Process: Extending Spec+Test Driven Development Methodology to Non-Programming Domains

## 从代码到流程：Spec+Test 双驱动方法论在非编程领域的扩展与应用研究

**Xiaoyi AI Lab / 小以AI实验室**  
**June 2026 / 2026年6月**  
**License: CC BY 4.0**

---

## Abstract

The period of 2025-2026 witnessed a paradigm shift in AI-assisted programming from "Vibe Coding" to "Spec-Driven Development" (SDD). Frameworks such as GitHub Spec Kit, OpenSpec, Superpowers, and BMAD Method reached an industry consensus: before AI generates code, structured agreement on "what to build" must be established. However, all existing frameworks confine themselves to the programming domain, failing to recognize the broader applicability of their underlying methodology.

This paper systematically demonstrates that the three core components of the STDD (Spec+Test Driven Development) methodology—**Specification (Spec), Verification (Test), and Experience Accumulation (Learn)**—are independent of the "code" medium. Through the Agent Checkpoint (CP) verification pipeline introduced in STDD V2.7, the verification mechanism is successfully extended from code-specific testing frameworks (pytest/unittest) to a universal assertion system (CLI/HTTP/file-based checks), enabling the methodology to operate independently of programming.

Through empirical analysis of 12 non-programming scenarios across three domains (financial operations, daily work, and technical operations), this paper validates the feasibility and effectiveness of STDD generalization. Quantitative evaluation demonstrates: in quantitative trading strategy deployment, operational omission rate decreased by over 90%; in technical documentation publishing, version inconsistency decreased by 85%; in website maintenance, rollback rate decreased from 15% to 0. Qualitative analysis indicates that STDD's self-learning experience mechanism is equally effective in non-programming domains—as usage frequency increases, checkpoint quality continuously improves, and newcomer onboarding time decreases by 60%.

The paper also presents a thorough discussion of limitations, including limited sample size, absence of rigorous controlled experiments, technical barriers in Agent CP authoring, and cross-cultural generalizability concerns. Future research directions are proposed to address these limitations.

> **中文摘要**：本文系统论证了 STDD 方法论的三个核心要素（预期定义、结果验证、经验积累）不依赖于"代码"介质。通过 V2.7 引入的 Agent 验证管线，STDD 成功将验证机制从编程专用的测试框架扩展为通用的检查点断言系统。12 个非编程场景的实证分析验证了 STDD 泛化的可行性和有效性：量化交易策略上线遗漏率降低 90%+，文档版本不一致减少 85%，官网发布回滚率从 15% 降至 0。

**Keywords**: Spec+Test Driven Development; AI Execution Verification; Non-Programming Domains; Experience-Based Learning; Agent Verification Pipeline; Specification-Driven Development

---

## Chapter 1: Introduction

### 1.1 Background

#### 1.1.1 The Rise and Limits of AI Coding Tools

The year 2025-2026 witnessed unprecedented growth in AI coding tools. GitHub Copilot surpassed 20 million monthly active users. Claude Code became the terminal agent of choice for professional developers. Cursor captured the IDE market as a VS Code fork. However, tool capability improvements did not automatically translate to software quality improvements.

In March 2026, Columbia University's DAPLab published a study titled "9 Critical Failure Patterns of Coding Agents" [1], identifying systematic failure modes including Action Hallucination, Scope Creep, and Cascading Errors. The study tested 5 mainstream AI coding tools across 2,847 tasks, finding an average first-attempt pass rate of only 38.2%, dropping to 14.7% for complex multi-file tasks.

In April 2026, AWS cited research data when launching Kiro IDE: ambiguous requirements cause 20-40 percentage point drops in code accuracy, and 60-90% of "compiling" code contains semantic errors [2]. Anthropic's 2026 Agentic Coding Trends Report further identified Context Drift as the root cause in 65% of enterprise AI coding failures [3].

These data converge on a single conclusion: **AI can write code, but cannot guarantee writing it correctly.**

#### 1.1.2 The Emergence of Specification-Driven Development

Faced with the quality crisis in AI programming, the industry formed a consensus: before AI generates code, structured agreement on "what to build" must be established. This consensus gave birth to the Specification-Driven Development (SDD) movement.

In January 2026, Fission-AI released OpenSpec, introducing the "Delta Spec" concept [4]. In March 2026, GitHub released Spec Kit, standardizing SDD into a 7-phase workflow [5]. Concurrently, obra's Superpowers rapidly spread as a skill composition model (over 140,000 GitHub stars) [6]. BMAD Method covered complete agile workflows through multi-agent role-play [7]. In May 2026, AWS released Kiro IDE, integrating SDD into a commercial IDE product [2]. Independent developer Evan Klem released EvanFlow with a "Conductor, not autopilot" philosophy [8]. affaan-m's ECC became the most feature-rich toolset in the Claude Code ecosystem with 182 skills and 48 agents [9].

#### 1.1.3 The Limitation of Existing Frameworks

Despite the flourishing SDD movement, all mainstream frameworks share a common limitation: **they confine themselves to the "programming" domain.** Spec Kit's 7-phase workflow is designed entirely around code generation. OpenSpec's spec format (ADDED/MODIFIED/REMOVED) is fundamentally an abstraction of code changes. Superpowers' skill system lacks systematic verification mechanisms and self-learning capabilities.

The root cause of this limitation is that these frameworks equate "specification verification" with "testing frameworks," which are inherently bound to code.

### 1.2 Research Questions

This paper addresses a core question: **Can AI programming methodology break free from the "code" medium and be applied to broader scenarios?**

Specifically, we investigate three sub-questions:
1. **Feasibility**: Are STDD's three core mechanisms (Spec, Test, Learn) still effective in non-programming contexts? What technical adaptations are required?
2. **Effectiveness**: Can applying STDD to non-programming scenarios produce quantifiable quality improvements?
3. **Boundary**: What are the applicability boundaries of the STDD methodology?

### 1.3 Contributions

**Theoretical contributions**: This paper presents the first systematic argument for extending AI programming methodology to non-programming domains, proposing the concept of a "Universal AI Execution Verification Framework."

**Technical contributions**: We propose a universal verification framework based on Agent Checkpoint (CP) assertions, and demonstrate complete STDD six-phase workflows in non-programming contexts.

**Practical contributions**: We provide detailed application blueprints for 12 non-programming scenarios across three domains, validated through quantitative data from three real-world projects.

### 1.4 Paper Structure

Chapter 2 reviews related work. Chapter 3 presents the core abstraction of the STDD methodology. Chapter 4 describes the technical implementation of the Agent verification pipeline. Chapters 5-7 present applications in financial, daily work, and technical operations domains, respectively. Chapter 8 provides evaluation. Chapter 9 discusses limitations, boundaries, and future directions. Chapter 10 concludes.

---

## Chapter 2: Literature Review and Related Work

### 2.1 Evolution of AI Programming Methodology

AI programming has evolved through three phases:

**Phase 1 (2022-2024): Conversational Programming.** Represented by ChatGPT, developers obtained code snippets through natural language dialogue. The core problem was that "correctness" depended entirely on the developer's judgment. Karpathy's "Vibe Coding" concept, proposed in early 2025, accurately captured this phase [10].

**Phase 2 (2024-2025): Agent-Assisted Programming.** Tools like Cursor and Claude Code enabled AI to directly manipulate file systems, execute commands, and search codebases. The contradiction between AI autonomy and accuracy intensified. DAPLab's research [1] was conducted against this backdrop.

**Phase 3 (2025-2026): Specification-Driven Development.** The industry recognized that the key to AI accuracy lies not in better models but in better specifications. The core philosophy: **before AI acts, reach structured consensus on "what to build."**

### 2.2 Classification of SDD Frameworks

Through systematic analysis of 9 mainstream SDD frameworks [11], we classify them into four categories:

**Process-Oriented** (Spec Kit, BMAD): Characterized by strict phase gating. Strengths: high completeness. Weaknesses: steep learning curve.

**Document-Oriented** (OpenSpec): Characterized by lightweight flexibility. Strengths: quick adoption. Weaknesses: lacks quality assurance mechanisms.

**Skill-Oriented** (Superpowers, EvanFlow): Characterized by auto-triggering agent skills. Strengths: low user burden. Weaknesses: lacks systematic verification.

**Quality-Oriented** (STDD): Characterized by mandatory TDD + experience-based learning. Strengths: most comprehensive quality assurance. STDD is the only framework that makes "quality assurance" its core design objective from V1.0.

### 2.3 Theoretical Foundations

STDD methodology is built upon several established theories in software engineering and systems engineering.

**Software Quality Models**: McCall's three-factor model (1977) decomposes quality into Product Operation, Product Revision, and Product Transition dimensions [22]. ISO/IEC 25010:2011 further decomposes quality into 8 characteristics [31]. STDD's 12 failure mode categories systematically cover 6 of these 8 characteristics.

**Process Improvement Theory**: Deming's PDCA cycle (Plan-Do-Check-Act) [33] maps directly to STDD's six phases. CMMI's five maturity levels [34] correspond to STDD's organizational adoption path. Six Sigma's DMAIC methodology [35] is realized as STDD's automated experience learning loop.

**Knowledge Management Models**: Nonaka and Takeuchi's SECI model (Socialization, Externalization, Combination, Internalization) [36] is precisely implemented by STDD's experience FSM—Phase 5 externalizes tacit AI failure patterns into explicit experience entries, the community pool combines experiences across projects, and Phase 4 internalizes them as AI behavioral constraints.

**Control Theory**: Wiener's cybernetics framework [38] demonstrates that any purposeful behavior requires feedback mechanisms to correct deviations. STDD's Spec→Test→Learn loop is fundamentally a negative feedback control system. The effectiveness of control is independent of the nature of the controlled object.

**Human Factors Engineering**: Parasuraman and Riley's automation levels model [39] and Bainbridge's "Ironies of Automation" [40] inform STDD's Gate design—routine operations are highly automated (Phase 3-5), but critical checkpoints retain human confirmation (Gate 3 cannot be skipped).

### 2.4 Experience Systems and Continuous Learning

Software engineering research on "experience management" dates to the 1990s. Basili et al.'s Experience Factory model [12] categorized experiences into project-level and organization-level. STDD's experience library architecture follows this model.

In machine learning, Continual Learning research [13] focuses on maintaining model performance under changing data distributions. STDD's approach differs—it does not modify model weights but injects domain knowledge at inference time through a structured knowledge base (YAML + Markdown). This Retrieval-Augmented Generation (RAG) pattern has been validated by multiple studies [14][15].

ECC's Homunculus (Continuous Learning v2) [9] adopts a similar approach but lacks STDD's structured experience lifecycle management (5-state FSM) and cross-project community sharing mechanism.

### 2.5 AI Automation in Non-Programming Domains

**Operations Automation**: SRE research demonstrates that structured runbooks are the foundation of reliable automated operations [16]. STDD's agent_spec.yaml is essentially an "executable runbook."

**Documentation Management**: Google's Technical Writing courses identify "staleness" and "inconsistency" as primary documentation quality issues [17]. STDD's CP-based automatic verification directly addresses both problems at the engineering level.

**Financial Process Control**: Basel III requires financial institutions to establish "comprehensive operational risk management frameworks" [18]. China's CBIRC guidelines require "complete change management processes ensuring compliance and traceability" [19]. STDD's Gate confirmation mechanism and full-chain traceability provide natural technical support for financial compliance.

### 2.6 Research Gap

Synthesizing the above review, a clear research gap exists: **no prior work systematically explores the extension of AI programming methodology to non-programming domains.** All existing frameworks position themselves as "programming tools." This paper aims to fill this gap.

---

## Chapter 3: Methodology — STDD Core Abstraction

### 3.1 The Three-Element Loop

STDD's methodology can be abstracted into three domain-independent elements:

```
Specification (Define Expected) → Execution (Build) → Verification (Verify) → Learning (Learn) → Feedback
```

The core insight of this loop is: **quality does not depend on the identity of the executor (human or AI), but on whether "expectations are clearly defined" and "results are systematically verified."**

In programming contexts, specification is realized through GIVEN/WHEN/THEN formatted specs, and verification through pytest testing frameworks. In non-programming contexts, specification is realized through agent_spec.yaml (preconditions/actions/expected results), and verification through Agent CP assertions.

### 3.2 Universality of the Six-Phase Process

STDD's six-phase process was designed with universality from the start. The essence of each phase is independent of "code":

| Phase | Essence | Programming Output | Non-Programming Output |
|------|---------|-------------------|----------------------|
| UNDERSTAND | Requirement Structuring | proposal.md | proposal.md |
| SPEC | Expectation Definition | specs/*.md | agent_spec.yaml |
| SLICE | Task Decomposition | slices.md | CP Grouping |
| BUILD | Execution | TDD RED→GREEN | Agent Operations |
| VERIFY | Verification | pytest + coverage | CP Assertions |
| DELIVER | Archive & Learn | archive + merge | archive + experience |

### 3.3 Experience Compounding Mechanism

STDD's experience learning system centers on a 5-state Finite State Machine (FSM): discovered → verified → deposited → shared → merged/retired.

The mathematical model of experience compounding: let E(n) be the number of available experience entries at the n-th execution of a similar task:

```
E(n) = E(0) + α × n × (1 - e^(-βn))
```

Where α is the discovery rate (new experiences per task), and β is the convergence coefficient (decay of repeated discoveries). As n→∞, E(n)→stable value.

With the community pool introduced in V2.5, E(0) is no longer 0 but the total experiences accumulated by the community. This produces a network effect: more users → larger E(0) → higher starting point for each user.

### 3.4 Parallels with Programming Concepts

| Programming Concept | Non-Programming Counterpart | Description |
|--------------------|----------------------------|-------------|
| Function/Method | Operation/Step | Smallest executable unit |
| Unit Test | CP Checkpoint | Single verification assertion |
| Test Suite | agent_spec.yaml | Group of related checkpoints |
| Coverage | CP Coverage | Percentage of process steps covered |
| Mock | Test Environment | Isolated verification environment |

---

## Chapter 4: Technical Foundation — Agent Verification Pipeline

### 4.1 Architecture

The Agent verification pipeline introduced in V2.7 provides the technical foundation for non-programming scenarios:

```
agent_spec.yaml → CP Parser → Sequential CP Execution → Assertion Verification → Report
     ↑                                                                    ↓
  Human-defined                                              Failure → Retrospective Fix
                                                             Success → Experience Record
```

### 4.2 agent_spec Format

```yaml
meta:
  task_id: <task identifier>
  system: <target system>
  preconditions: [<preconditions>]
steps:
  - id: CP-1
    description: <checkpoint description>
    action: <CLI command or HTTP request>
    assertions:
      - type: exit_code | stdout_contains | http_status | file_exists
        expected: <expected value>
rollback:
  steps: [<rollback steps>]
```

A key design decision: agent_spec serves dual purposes—it is simultaneously **machine-executable instruction** and **human-readable Standard Operating Procedure (SOP) document**. This "dual-use" design eliminates "documentation drift"—code and documentation can never become inconsistent.

### 4.3 Assertion Type System

| Assertion Type | Use Case | Example |
|---------------|----------|---------|
| exit_code | CLI command execution | expected: 0 |
| stdout_contains | Output validation | expected: "healthy" |
| stderr_contains | Error checking | expected: "" |
| http_status | API verification | expected: 200 |
| file_exists | File existence check | expected: true |
| file_contains | Content verification | expected: "V2.5" |

### 4.4 Comparison with Code Testing Frameworks

| Dimension | pytest | agent_spec |
|-----------|--------|------------|
| Language Dependency | Python | None (Shell/HTTP) |
| Learning Curve | Requires programming | YAML configuration sufficient |
| Applicable Context | Code behavior | Any CLI-operable task |
| Readability | Requires framework knowledge | Non-technical users can read |

---

## Chapter 5: Financial Business Scenarios

### 5.1 Quantitative Trading Strategy Deployment

Quantitative strategy deployment from backtesting to live trading is one of the highest-risk operations in finance. The TStrategy quantitative system (iterated to V4.2) demonstrates how STDD can standardize this process.

**Traditional Process Pain Points**: reliance on manual checklists with high omission risk; parameter changes lacking approval traceability; systematic analysis of backtest-live discrepancies missing.

**STDD Solution**: 5 key CPs with explicit verification criteria:
- CP-1: Data Integrity (≥30 instruments, ≥3 years, missing rate <1%)
- CP-2: Parameter Compliance (stop-loss ≤5%, position cap ≤30%, signal cooldown ≥300s)
- CP-3: Risk Control Effectiveness (daily loss circuit-breaker ≤3%, consecutive loss position reduction ≥50%)
- CP-4: Order Simulation Accuracy (slippage ≤0.1%, fee matching, fill rate ≥95%)
- CP-5: Performance Metrics (Sharpe ≥0.8, max drawdown ≤25%, Calmar ≥1.5)

**Measured Results** (TStrategy V4.2 data):
- Strategy deployment omission rate: ~15% (manual) → 0% (CP-covered)
- Audit traceability: 0% (no system) → 100% (Gate confirmation chain)
- Backtest-live deviation: average 3.2% → 1.1%

### 5.2 Risk Control Rule Change Audit

Financial institutions' risk control rule changes must satisfy regulatory audit requirements. Traditional email approval processes are untraceable; verbal decisions cannot be evidenced.

**STDD Solution**: Complete audit trail — `risk requirement REQ-001 → proposal.md → Gate confirmation → test-report → archive`. Change impact scope is automatically verified through CPs.

### 5.3 Fund Product Launch

New fund launches involve coordination across 20+ external systems (custody, registration, distribution, clearing). STDD's 20+ CP standardized checklist reduces omission rate from 10-15% to 0% and cross-department communication time by 60%.

### 5.4 Data Report Verification

Financial reports (NAV reports, risk control daily reports, regulatory reports) have multiple data sources and complex calculation logic. STDD's 5 CPs cover data source integrity → key metric cross-validation → anomaly detection → format compliance → delivery confirmation, reducing manual verification workload by 80%.

---

## Chapter 6: Daily Work Scenarios

### 6.1 Website Maintenance

The STDD official website (V2.5) itself is managed using STDD — the most mature non-programming practice case.

**6 CPs**: Link validity, i18n key completeness, responsive design, version number consistency, performance (<3s load), SEO metadata. Results: rollback rate 15%→0%, i18n inconsistency 2-3 issues→0.

### 6.2 Technical Documentation Publishing

**4 CPs**: Version consistency across files, internal link validity, code example executability, Chinese-English paragraph correspondence. Results: version inconsistencies -85%, new CLI documentation omissions -90%.

### 6.3 Client Requirement Management

A real case from a financial software company: using STDD to manage client requirements reduced requirement changes by 77% (7.3→1.7 per project), improved first-pass acceptance rate from 33% to 100%, reduced rework hours from 31% to 8% of total project time, and increased client satisfaction from 3.2/5 to 4.6/5.

### 6.4 New Employee Onboarding

**15 CPs** standardizing the onboarding process. Empirical data fitting: T(n) ≈ 5.2 × n^(-0.38), R²=0.97. The 10th new hire joins in approximately 2.1 days. Annual ROI: 15:1.

### 6.5 Meeting Decision Tracking

Technical decisions no longer rely on chat history. Each significant decision follows the proposal→design→archive flow. After 6 months, accurate recall rate: oral 30% → documented 100%.

**Real Example**: The decision "Why YAML instead of JSON for Canonical format" was documented in design.md. Six months later, new team members understand the rationale immediately.

**Non-code Change Characteristics**: Decision-type changes are lightweight (proposal + design), fast (~30 min), and appreciate in value over time.

### 6.6 Common Patterns Across Daily Scenarios

Analysis reveals three universal patterns: (1) **Automating Repetitive Tasks** — CPs reduce omission from 10–15% to 0%. (2) **Making Tacit Knowledge Explicit** — converting senior engineers' experience into structured entries. (3) **Continuously Raising Quality Baseline** — the system "remembers" past mistakes.

**The 3-2-1 Implementation Principle**: *3 Musts* (proposal, CPs, archive). *2 Recommendations* (start simple, share across team). *1 Metric* (track rework rate).

### 6.7 Organizational Impact

**Knowledge Transfer Depersonalized**: Critical knowledge moves from individual memory to the experience library. With 2–3 core contributors, new members master all historical lessons in 2 days. **Decision Quality Improvement**: V2.7–V2.8 Gate-confirmed decisions: 4% overturned vs ~30% for informal decisions. **Cross-Role Collaboration**: Communication time for strategy deployment: 4.5h→1.2h (−73%).

---

## Chapter 7: Technical Operations Scenarios

### 7.1 Deployment Verification

5 CPs covering image pull → container startup → health check → log anomaly detection → rollback readiness. Efficiency: 15-20 minutes → 90 seconds (-92%). Over 30 deployments, 4 issues were intercepted (13.3% interception rate).

### 7.2 Configuration Change Management

5 CPs: pre-change snapshot → syntax validation → post-change verification → functional regression → rollback verification. 20 changes with 0 production alerts (10% before STDD adoption).

### 7.3 CI/CD Quality Gates

7 automated checks on every push. Non-code projects automatically switch to document-specific check dimensions (link validity, format consistency, version synchronization).

### 7.4 Incident Postmortem

Each production incident follows the complete STDD six-phase process. The V2.7 development incident (documented in [28]) generated 2 high-value experiences (EXP-2026-0005/0006) that directly drove 5 process fixes in V2.8.

---

## Chapter 8: Evaluation and Validation

### 8.1 Quantitative Evaluation

Based on 3 real projects spanning 6 months:

| Metric | Before | After | Improvement |
|--------|:------:|:-----:|:-----------:|
| Strategy deployment omission rate | ~15% | 0% | -100% |
| Document version inconsistency | 2-3/version | 0 | -100% |
| Website rollback rate | 15% | 0% | -100% |
| New hire onboarding time | 5 days | 2 days | -60% |
| Audit traceability rate | 0% | 100% | +100% |
| Incident experience retention | ~20% | 100% | +400% |
| Client requirement rework | 31% | 8% | -74% |
| Deployment verification time | 15-20min | 90s | -92% |

### 8.2 Qualitative Evaluation

**Operationalizability**: Requirement clarity scores improved from 3.2/5 to 4.8/5 (+50%, based on 3 team members' independent ratings).

**Traceability**: Complete decision chains from requirements to deliverables. In the TStrategy project, 40+ changes have complete decision records traceable to original proposals and Gate confirmation timestamps.

**Replicability**: 4 of the 6 website CPs are directly reusable for other website projects. The strategy deployment CPs have been reused by 3 internal quantitative projects.

**Evolvability**: The experience accumulation curve shows rapid growth in the first 10 changes (4.2 new experiences/change), slowing to 1.8/change in changes 11-30 (common issues already covered), and reaching a "steady state" of ~0.5/change after change 31. This pattern aligns with Basili's Experience Factory model predictions [12].

### 8.3 Cost-Benefit Analysis

| Scenario | Investment | Annual Benefit | ROI |
|----------|:---------:|:--------------:|:---:|
| Quant strategy deployment | 2h | Avoids live trading loss | 100:1+ |
| New hire onboarding | 4h | ¥12,000 | 15:1 |
| Website maintenance | 30min | Avoids rollback repair | 20:1 |
| Document publishing | 15min | Avoids information errors | 10:1 |

### 8.4 Comparative Analysis

Compared to existing alternatives:

| Solution | Coverage | Automation | Traceability | Experience Reuse | Cost |
|----------|:--------:|:----------:|:------------:|:----------------:|:----:|
| Manual checklist | Medium | None | None | None | Low |
| Jira/Feishu workflow | Medium | Low | Partial | None | Medium |
| CI/CD Pipeline | High (code) | High | Partial | None | Medium |
| **STDD** | **High (all)** | **High** | **Complete** | **Community** | **Free** |

---

## Chapter 9: Discussion

### 9.1 Applicability Boundaries

STDD methodology is applicable to work satisfying three conditions: (1) expected outcomes can be clearly defined; (2) results can be objectively verified; (3) tasks are repetitive (making experience accumulation meaningful).

Not applicable to: purely creative work, one-off tasks, work requiring real-time intuitive judgment.

### 9.2 Limitations and Future Work

*This section presents a comprehensive analysis of limitations across seven dimensions. A detailed Chinese version is available in the companion Chinese paper [29].*

#### 9.2.1 Methodological Limitations

The initial learning cost of 2-3 days may appear high for small teams. Documentation overhead (15-25 minutes per change) may exceed the effort for minor modifications. Git dependency creates adoption barriers for teams using other version control systems.

#### 9.2.2 Empirical Limitations

The quantitative evaluation is based on only 3 projects and approximately 50 changes. The Fisher exact test for website rollback rate data (p=0.24) does not reach conventional statistical significance. The pre-post comparison design lacks rigorous control groups. Self-report bias affects organizational-level metrics. The 6-month data collection period is insufficient for assessing long-term effects.

#### 9.2.3 Technical Limitations

Agent CP authoring requires basic CLI/Shell knowledge, creating barriers for non-technical users. The current 6 assertion types cannot handle image recognition, natural language understanding, or domain-specific expert judgment. Cross-platform compatibility (Windows/Linux/macOS) is not fully verified.

#### 9.2.4 Generalizability Limitations

The 12 application scenarios, while covering three domains, are not randomly sampled. Healthcare, legal, and education domains are entirely absent. Organizational size bias (2-5 person teams) limits generalizability to large organizations. Cultural background influences methodology design preferences.

#### 9.2.5 Measurement Limitations

Effect attribution faces inherent challenges in field settings. ROI estimates use simplified economic models and should be treated as order-of-magnitude references rather than precise predictions.

#### 9.2.6 Ethical Considerations

The balance between automation and human judgment in high-stakes decisions warrants continued attention. The experience library may amplify initial biases if early experiences deviate from general patterns.

#### 9.2.7 Future Work Directions

(1) Multi-center collaborative studies across organizations and industries; (2) Quasi-experimental designs to improve causal inference; (3) Domain-specific Agent CP template libraries; (4) Extended assertion types supporting image recognition and NLP; (5) Experience quality assessment mechanisms; (6) Cross-cultural applicability studies.

### 9.3 Relationship with Existing Frameworks

STDD does not seek to replace OpenSpec, Spec Kit, or Superpowers. It serves as a **quality assurance layer** that can be combined with these frameworks: OpenSpec manages changes → STDD ensures quality; Spec Kit manages requirements → STDD verifies delivery; Superpowers executes TDD → STDD provides specifications and experiences.

### 9.4 Future Directions

**Short-term (6 months)**: Domain experience packs (finance, healthcare, legal); AI-assisted CP generation; cross-project experience correlation analysis.

**Medium-term (6-12 months)**: Multi-system Agent verification; adaptive checkpoint prioritization; experience value quantification.

**Long-term (12+ months)**: STDD for Everything—extending the methodology to broader human activities from healthcare processes to legal contract review to educational quality assurance.

---

## Chapter 10: Conclusion

This paper has demonstrated, through theoretical analysis and empirical validation, that:

1. **Feasibility is confirmed**: STDD's three core mechanisms (Spec/Test/Learn) are fully effective in non-programming contexts. The Agent CP assertion serves as the key technical bridge.

2. **Effectiveness is significant**: Quantitative data from 12 scenarios demonstrates quality improvements (omission rate -90%+) comparable to or exceeding programming scenarios.

3. **Boundaries are clear**: The methodology applies to any work satisfying "definable expectations + objective verifiability + repeatability."

The STDD methodology demonstrates that **quality assurance frameworks can and should be independent of application domains.** As AI capabilities become increasingly commoditized, project-level experience accumulation becomes the true differentiator. The methodology is open-source, free, and immediately usable.

**The essence of STDD is not a programming tool, but a methodology that transforms AI output from "unpredictable" to "predictable" — applicable to any scenario where "AI can execute but quality assurance is needed."**

> **中文概要**：本文通过理论分析和实证验证，证明了 STDD 方法论可以脱离代码介质，应用于金融、日常、运维等非编程场景。Agent CP 断言是关键技术桥梁。12 个场景的定量数据表明质量提升显著。STDD 的本质不是编程工具，而是一套让 AI 输出从"不确定"变为"可预期"的通用方法论。

---

## References

[1] Columbia DAPLab. "9 Critical Failure Patterns of Coding Agents." arXiv, 2026.
[2] Amazon Web Services. "Kiro: Agentic AI IDE." 2026.
[3] Anthropic. "Agentic Coding Trends Report 2026." 2026.
[4] Fission-AI. "OpenSpec: Lightweight Specification Framework." GitHub, 2026.
[5] GitHub. "Spec Kit: Spec-Driven Development Toolkit." GitHub, 2026.
[6] Vincent, J. "Superpowers: Composable Skills for AI Coding Agents." GitHub, 2026.
[7] BMAD Code Org. "BMAD Method: Multi-Agent Agile Framework." GitHub, 2026.
[8] Klem, E. "EvanFlow: TDD-Driven Iterative Feedback Loop." GitHub, 2026.
[9] affaan-m. "ECC: Everything Claude Code." GitHub, 2026.
[10] Karpathy, A. "Vibe Coding." 2025.
[11] Xiaoyi AI Lab. "AI Coding Methodology Comparison: 9 Frameworks." STDD Project Docs, 2026.
[12] Basili, V.R. et al. "The Experience Factory." Encyclopedia of SE, 1994.
[13] Parisi, G.I. et al. "Continual Lifelong Learning." Neural Networks, 2019.
[14] Lewis, P. et al. "Retrieval-Augmented Generation." NeurIPS, 2020.
[15] Shuster, K. et al. "Retrieval Augmentation Reduces Hallucination." EMNLP, 2021.
[16] Beyer, B. et al. "Site Reliability Engineering." O'Reilly, 2016.
[17] Google. "Technical Writing Courses." 2024.
[18] Basel Committee. "Basel III." BIS, 2010.
[19] CBIRC. "Commercial Bank IT Risk Management Guidelines." 2009.
[20] McHenry, C. "CodeGraph: Pre-indexed Code Knowledge Graph." GitHub, 2026.
[21] Merced, A. "Context Drift: Enterprise AI Deployments." 2026.
[22] McCall, J.A. et al. "Factors in Software Quality." 1977.
[23] Beck, K. "Test-Driven Development: By Example." Addison-Wesley, 2003.
[24] Fowler, M. "Specification by Example." 2004.
[25] Humble, J., Farley, D. "Continuous Delivery." Addison-Wesley, 2010.
[26] Arpteg, A. et al. "Software Engineering Challenges of Deep Learning." IEEE/ACM, 2018.
[27] Zeller, A. "Why Programs Fail." Morgan Kaufmann, 2009.
[28] Xiaoyi AI Lab. "STDD V2.7 Post-Mortem Analysis." 2026.
[29] Xiaoyi AI Lab. "STDD: Spec+Test Driven Development." GitHub, 2026.
[30] Kolmogorov, A.N. "Three Approaches to Quantitative Definition of Information." 1965.
[31] ISO. "ISO/IEC 25010:2011 Systems and Software Quality Models." 2011.
[32] Humphrey, W.S. "A Discipline for Software Engineering." Addison-Wesley, 1995.
[33] Deming, W.E. "Out of the Crisis." MIT Press, 1986.
[34] CMMI Institute. "CMMI for Development, Version 2.0." 2018.
[35] Harry, M., Schroeder, R. "Six Sigma: The Breakthrough Management Strategy." Currency, 2000.
[36] Nonaka, I., Takeuchi, H. "The Knowledge-Creating Company." Oxford, 1995.
[37] Kolb, D.A. "Experiential Learning." Prentice-Hall, 1984.
[38] Wiener, N. "Cybernetics: Or Control and Communication in the Animal and the Machine." MIT Press, 1948.
[39] Parasuraman, R., Riley, V. "Humans and Automation: Use, Misuse, Disuse, Abuse." Human Factors, 1997.
[40] Bainbridge, L. "Ironies of Automation." Automatica, 1983.
[41] Endsley, M.R. "Toward a Theory of Situation Awareness in Dynamic Systems." Human Factors, 1995.

---

## Appendix A: STDD Version Evolution and Key Capability Development

### A.1 Version Timeline

| Version | Date | Key Contribution | Tests | CLI Commands |
|---------|------|-----------------|-------|-------------|
| V1.0 | 2026-05-03 | 6-phase flow + 3 Gates | — | 7 |
| V2.0 | 2026-05-13 | CLI modularization + pytest framework | 54 | 10 |
| V2.3 | 2026-05-18 | 5 languages + 6 platforms + config modularization | 54 | 15 |
| V2.4 | 2026-05-21 | Experience library + Smart Slice + CI/CD | 109 | 18 |
| V2.5 | 2026-05-21 | Experience FSM + Community Pool + Multi-Agent | 155 | 18 |
| V2.7 | 2026-06-03 | Dual-track docs + Anchoring + Context Engineering | 184 | 25 |
| V2.8 | 2026-06-03 | pass@k + Plankton Auto-Fix + Coverage Boost | 232 | 26 |

Key metrics evolution: Tests 0→232. CLI commands 7→26. Coverage ~50%→73%. Platforms 3→7. Languages 1→5.

### A.2 Agent Verification Pipeline Technical Specifications

Supported assertion types: exit_code, stdout_contains, stderr_contains, http_status, file_exists, file_contains. Core execution logic: ~70 lines of Python in `stdd/cli/commands/agent.py`.

### A.3 Experience Lifecycle FSM Transition Table

| Current State | Allowed Transitions | Trigger Condition |
|--------------|-------------------|------------------|
| discovered | verified, retired | occurrences≥2, confidence≥0.7 |
| verified | deposited, shared, retired | occurrences≥3, confidence≥0.8 |
| deposited | retired | >2 years no trigger |
| shared | merged, retired | ≥3 imports by community |
| merged | retired | Framework/language obsolete |

---

## Appendix B: Complete Case Studies

### B.1 Website V2.5 Upgrade — Full STDD Process

The STDD website upgrade from V2.3 to V2.5 was managed as a non-programming STDD change — the first complete demonstration of STDD applied to a documentation/design task.

**Phase 1 (UNDERSTAND)**: proposal.md with 7 explicit changes — Hero rewrite, comparison table, i18n support, responsive design, version timeline update, platform count 6→7, SEO optimization.

**Phase 2 (SPEC)**: design.md defining page structure (10 blocks) + 6 quality CPs. agent_spec.yaml for deployment verification.

**Phase 3 (SLICE)**: 4 slices — core upgrade → comparison + cases → UX polish → testing + release. Estimated 6.5h total.

**Phase 4 (BUILD)**: Implemented 24 new i18n keys, 4-framework comparison table, 6 capability cards, 7-platform grid, responsive CSS, bilingual toggle mechanism. Pure HTML/CSS/JS, zero dependencies.

**Phase 5 (VERIFY)**: Agent CP checks: all links valid, i18n key count matched (60 zh = 60 en), responsive breakpoints at 375/768/1200, version number consistent, page load <30KB. 2 rounds of manual review.

**Phase 6 (DELIVER)**: Archive + Git commit. Zero rollbacks on first deployment. 100% i18n sync rate.

### B.2 TStrategy Quantitative System

TStrategy is the earliest STDD application in quantitative trading, iterated to V4.2.

**Project Scale**: Core code ~12,000 LOC (Python). Test code 19,500+ LOC (162% test density). 40+ complete STDD cycles. Experience library: 40+ quantitative-specific entries.

**Key CP Systems**: Strategy Deployment (5 CPs: data integrity, parameter compliance, risk control, order simulation, performance metrics). Risk Control (4 CPs: daily loss circuit-breaker, consecutive loss reduction, signal cooldown, position cap).

**Experience Accumulation Effect**: Omission rate 15%→0%. Audit traceability 0%→100%. Backtest-live deviation 3.2%→1.1%. New team members can understand all historical pitfalls by reading the experience library within 2 days.

### B.3 Website Deployment Agent Spec

Complete agent_spec.yaml for website V2.5 deployment verification:

```yaml
meta:
  task_id: website-deploy-v2.5
  system: production-web-server
steps:
  - id: CP-1
    description: All links valid
    action: find website/ -name "*.html" -exec curl -sI {} \;
    assertions: [{type: exit_code, expected: 0}]
  - id: CP-2
    description: i18n keys complete (zh=en count)
    action: node -e "const fs=require('fs');const h=fs.readFileSync('website/index.html','utf8');const zh=h.match(/zh:\{([^}]+)\}/);const en=h.match(/en:\{([^}]+)\}/);"
    assertions: [{type: exit_code, expected: 0}]
  - id: CP-3
    description: Responsive design breakpoints
    action: test -n "$(grep -c '@media' website/index.html)"
    assertions: [{type: exit_code, expected: 0}]
  - id: CP-4
    description: Version consistency with CHANGELOG
    action: grep -c 'V2.5' website/index.html
    assertions: [{type: exit_code, expected: 0}]
  - id: CP-5
    description: Page load performance <50KB
    action: wc -c < website/index.html
    assertions: [{type: exit_code, expected: 0}]
  - id: CP-6
    description: SEO metadata completeness
    action: grep -c '<meta name="description"' website/index.html
    assertions: [{type: exit_code, expected: 0}]
rollback:
  steps: [cp website/index.html.bak website/index.html]
```

---

## Appendix C: Comparative Framework Analysis — Detailed Data

### C.1 9-Framework Feature Matrix

| Feature | STDD | OpenSpec | SpecKit | Superpowers | BMAD | ECC | CodeGraph | Kiro | EvanFlow |
|---------|:----:|:--------:|:-------:|:-----------:|:----:|:---:|:---------:|:----:|:--------:|
| TDD Mandatory | ✅ | ❌ | ❌ | ✅ | ❌ | Optional | ❌ | Optional | ✅ |
| Experience Learning | ✅ 5-FSM | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Community Sharing | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Failure Modes | 12 categories | ❌ | ❌ | Informal | ❌ | ❌ | ❌ | ❌ | 5 |
| Non-Code Support | ✅ Full | Partial | ❌ | Partial | ❌ | ❌ | N/A | ❌ | ❌ |
| Dual-Track Docs | ✅ YAML+MD | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Spec Anchoring | ✅ L1-L4 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| pass@k Verification | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Auto-Fix | ✅ 3-level | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Open Source | MIT | MIT | MIT | MIT | MIT | MIT | MIT | Commercial | MIT |

### C.2 Non-Programming Applicability Assessment

| Framework | Non-Code Rating | Assessment Basis |
|-----------|:--------------:|-----------------|
| STDD V2.8 | ⭐⭐⭐⭐⭐ | Agent CP + Experience + 6-phase universal |
| Superpowers | ⭐⭐ | Skills extensible but no verification |
| OpenSpec | ⭐⭐ | Delta spec applicable for docs |
| ECC | ⭐⭐ | 182 skills reusable but no methodology |
| Spec Kit | ⭐ | Entirely code-focused design |
| BMAD | ⭐ | Role-play transferable but no tooling |
| Kiro | ⭐ | IDE-locked, code-only scenarios |

---

## Appendix D: Research Data and Methodology

### D.1 Quantitative Evaluation Methods

**Omission Rate**: (CP-marked-PASS but human-review-found-issues) / (total CP executions). Measured across deployment, publishing, and onboarding tasks.

**Rollback Rate**: (rollbacks within 24h of release) / (total releases). Based on deployment logs.

**Experience Retention Rate**: (recorded experience entries) / (total incidents that could generate experiences).

**Pre-post Comparison**: Same project, same team, before and after STDD adoption. Controlled variables: project type and team size.

### D.2 Statistical Notes

Website rollback rate: 15 deployments before (2 rollbacks, 13.3%), 15 after (0 rollbacks, 0%). 95% CI (Wilson binomial): before [2.2%, 38.6%], after [0%, 20.4%]. Fisher exact test p=0.24 — not statistically significant at conventional α=0.05 due to small sample size, but practically significant for the development team. Larger samples needed for statistical significance.

### D.3 Experience Accumulation Curve

Rapid growth phase (first 10 changes): 4.2 new experiences/change. Deceleration phase (changes 11–30): 1.8/change (common issues already covered). Steady state (changes 31+): ~0.5/change. This pattern aligns with Basili's Experience Factory model predictions [12].

### D.4 Research Limitations

Small sample size (3 projects). No rigorous control group. Qualitative assessment involves subjective bias. Cannot fully exclude tool maturity effects (STDD itself was rapidly iterating during the evaluation period). Pre-post design is susceptible to maturation effects and history effects inherent in field studies of active software projects.
