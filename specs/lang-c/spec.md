# Spec: C/C++ 开发规范

> 对应 proposal C3 | 1 个 New Capability
> lang-c

## ADDED Requirements

### Requirement: C/C++ 规范文件存在且结构完整 <!-- confidence: high -->

系统 SHALL 提供 C/C++ 语言开发规范文件，覆盖代码风格、类型系统、并发模型、错误处理、日志、测试规范、审查清单 7 个维度。文件内部按 C 和 C++ 明确分区。

**证据来源**：proposal.md `What Changes > C3` + design.md `Decisions > 4`

#### Scenario: C/C++ 规范文件存在 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/` 目录存在
- **WHEN** Phase 4 Step 0 读取 `project.language == "c"` 的开发规范
- **THEN** 系统 SHALL 读取 `.stdd/standards/c.md` 文件
- **AND** 该文件 SHALL 包含：代码风格（clang-format/clang-tidy/命名）、类型系统（指针/const/类型转换/C++模板/RAII）、并发模型（pthread/std::thread/async）、错误处理（errno/返回码/C++异常）、日志（syslog/spdlog）、测试规范（GTest/Catch2/CMock/mock）、审查清单 共 7 个章节

#### Scenario: C 和 C++ 分区明确 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/c.md` 文件存在
- **WHEN** 开发者阅读规范中的类型系统或错误处理章节
- **THEN** 各章节 SHALL 通过「C 语言约定」和「C++ 语言约定」子标题明确区分两种语言的差异
- **AND** 共享约定（如命名风格、clang-format 配置）SHALL 在章节开头统一说明

---

### Requirement: C/C++ 规范与模板结构一致 <!-- confidence: high -->

C/C++ 规范 SHALL 与其他语言规范共享相同的 7 章顶级结构。

**证据来源**：proposal.md `Success Criteria`

#### Scenario: 七章结构完整 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/python.md` 包含 7 个章节
- **WHEN** 对比 C/C++ 规范和 Python 规范的章节结构
- **THEN** C/C++ 规范 SHALL 包含：代码风格、类型系统、并发模型、错误处理、日志、测试规范、审查清单 共 7 个顶级章节
- **AND** 各章节内容 SHALL 根据 C/C++ 语言特性定制（如手动内存管理、指针安全、模板元编程）
