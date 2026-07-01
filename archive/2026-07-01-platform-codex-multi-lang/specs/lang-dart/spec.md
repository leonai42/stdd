# Spec: Dart/Flutter 开发规范

> 对应 proposal C6 | 1 个 New Capability
> lang-dart

## ADDED Requirements

### Requirement: Dart/Flutter 规范文件存在且结构完整 <!-- confidence: high -->

系统 SHALL 提供 Dart/Flutter 语言开发规范文件，覆盖代码风格、类型系统、并发模型、错误处理、日志、测试规范、审查清单 7 个维度，包含 Flutter widget 测试约定。

**证据来源**：proposal.md `What Changes > C6`

#### Scenario: Dart 规范文件存在 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/` 目录存在
- **WHEN** Phase 4 Step 0 读取 `project.language == "dart"` 的开发规范
- **THEN** 系统 SHALL 读取 `.stdd/standards/dart.md` 文件
- **AND** 该文件 SHALL 包含：代码风格（dart format/dart analyze/lints/命名）、类型系统（空安全/sealed class/extension type/Record/Pattern）、并发模型（Future/async-await/Stream/Isolate）、错误处理（try-catch/Result 模式/Error vs Exception）、日志（package:logging/Flutter DevTools）、测试规范（flutter test/WidgetTester/Golden test/mock/Mocktail）、审查清单 共 7 个章节

#### Scenario: Flutter 特有约定 <!-- confidence: high -->

- **GIVEN** 项目为 Flutter 项目（`project.language == "dart"` 且框架为 Flutter）
- **WHEN** Phase 4 Step 0 读取 Dart 规范
- **THEN** 规范 SHALL 包含 Flutter 特有章节：Widget 树约定（const 构造/StatelessWidget 优先）、状态管理（Riverpod/Bloc 推荐模式）、BuildContext 使用约定、Flutter 测试金字塔（Unit/Widget/Integration）

---

### Requirement: Dart 规范与模板结构一致 <!-- confidence: high -->

Dart 规范 SHALL 与其他语言规范共享相同的 7 章顶级结构。

**证据来源**：proposal.md `Success Criteria`

#### Scenario: 七章结构完整 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/python.md` 包含 7 个章节
- **WHEN** 对比 Dart 规范和 Python 规范的章节结构
- **THEN** Dart 规范 SHALL 包含：代码风格、类型系统、并发模型、错误处理、日志、测试规范、审查清单 共 7 个顶级章节
- **AND** 各章节内容 SHALL 根据 Dart/Flutter 生态定制
