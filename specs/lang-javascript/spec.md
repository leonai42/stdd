# Spec: JavaScript 开发规范

> 对应 proposal C2 | 1 个 New Capability
> lang-javascript

## ADDED Requirements

### Requirement: JavaScript 规范文件存在且结构完整 <!-- confidence: high -->

系统 SHALL 提供 JavaScript 语言开发规范文件，覆盖代码风格、类型系统、异步模型、错误处理、日志、测试规范、审查清单 7 个维度，遵循 python.md 的模板结构。

**证据来源**：proposal.md `What Changes > C2` + design.md `Decisions > 3`

#### Scenario: JavaScript 规范文件存在 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/` 目录存在
- **WHEN** Phase 4 Step 0 读取 `project.language == "javascript"` 的开发规范
- **THEN** 系统 SHALL 读取 `.stdd/standards/javascript.md` 文件
- **AND** 该文件 SHALL 包含：代码风格（Prettier/ESLint/命名）、类型系统（JSDoc/TypeScript 互操作）、异步模型（Promise/async-await/EventEmitter）、错误处理（Error 子类/async 错误传播）、日志（winston/pino）、测试规范（Jest/Mocha/Supertest/mock）、审查清单 共 7 个章节

#### Scenario: 与 TypeScript 规范的关系 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/typescript.md` 和 `.stdd/standards/javascript.md` 同时存在
- **WHEN** 项目 `project.language == "javascript"`（纯 JS 项目）
- **THEN** 系统 SHALL 读取 `javascript.md` 而非 `typescript.md`
- **AND** `javascript.md` SHALL 在类型系统章节说明与 TypeScript 的差异（JSDoc 类型注解 vs TS 类型系统）
- **AND** 两文件 SHALL 在异步模型和错误处理章节保持一致

---

### Requirement: JavaScript 规范与模板结构一致 <!-- confidence: high -->

JavaScript 规范 SHALL 与其他语言规范共享相同的 7 章顶级结构，确保 STDD skill 在切换语言时无需改变检查逻辑。

**证据来源**：proposal.md `Success Criteria` + design.md `Decisions > 3`

#### Scenario: 七章结构完整 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/python.md` 包含 7 个章节
- **WHEN** 对比 JavaScript 规范和 Python 规范的章节结构
- **THEN** JavaScript 规范 SHALL 包含：代码风格、类型系统、异步或并发、错误处理、日志、测试规范、审查清单 共 7 个顶级章节
- **AND** 各章节内容 SHALL 根据 JavaScript/Node.js 生态定制
