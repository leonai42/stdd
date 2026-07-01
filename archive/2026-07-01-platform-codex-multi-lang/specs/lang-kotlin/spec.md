# Spec: Kotlin 开发规范

> 对应 proposal C4 | 1 个 New Capability
> lang-kotlin

## ADDED Requirements

### Requirement: Kotlin 规范文件存在且结构完整 <!-- confidence: high -->

系统 SHALL 提供 Kotlin 语言开发规范文件，覆盖代码风格、类型系统、并发模型、错误处理、日志、测试规范、审查清单 7 个维度，包含 Android 特有约定。

**证据来源**：proposal.md `What Changes > C4`

#### Scenario: Kotlin 规范文件存在 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/` 目录存在
- **WHEN** Phase 4 Step 0 读取 `project.language == "kotlin"` 的开发规范
- **THEN** 系统 SHALL 读取 `.stdd/standards/kotlin.md` 文件
- **AND** 该文件 SHALL 包含：代码风格（ktlint/detekt/命名）、类型系统（数据类/密封类/扩展函数/空安全）、并发模型（Coroutine/Flow/Channel/结构化并发）、错误处理（Result 类型/sealed class/异常传播）、日志（SLF4J/Timber（Android））、测试规范（JUnit5/MockK/Kotest/Turbine）、审查清单 共 7 个章节

#### Scenario: Android 特有约定 <!-- confidence: high -->

- **GIVEN** 项目为 Android 项目（`project.language == "kotlin"` 且 target 包含 Android）
- **WHEN** Phase 4 Step 0 读取 Kotlin 规范
- **THEN** 规范 SHALL 包含 Android 特有章节：Jetpack Compose 约定、ViewModel 模式、依赖注入（Hilt/Koin）、Android 测试（Robolectric/Compose UI Test）

---

### Requirement: Kotlin 规范与模板结构一致 <!-- confidence: high -->

Kotlin 规范 SHALL 与其他语言规范共享相同的 7 章顶级结构。

**证据来源**：proposal.md `Success Criteria`

#### Scenario: 七章结构完整 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/python.md` 包含 7 个章节
- **WHEN** 对比 Kotlin 规范和 Python 规范的章节结构
- **THEN** Kotlin 规范 SHALL 包含：代码风格、类型系统、并发模型、错误处理、日志、测试规范、审查清单 共 7 个顶级章节
- **AND** 各章节内容 SHALL 根据 Kotlin/JVM 生态定制
