# Spec: Swift 开发规范

> 对应 proposal C5 | 1 个 New Capability
> lang-swift

## ADDED Requirements

### Requirement: Swift 规范文件存在且结构完整 <!-- confidence: high -->

系统 SHALL 提供 Swift 语言开发规范文件，覆盖代码风格、类型系统、并发模型、错误处理、日志、测试规范、审查清单 7 个维度，包含 iOS/macOS 特有约定。

**证据来源**：proposal.md `What Changes > C5`

#### Scenario: Swift 规范文件存在 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/` 目录存在
- **WHEN** Phase 4 Step 0 读取 `project.language == "swift"` 的开发规范
- **THEN** 系统 SHALL 读取 `.stdd/standards/swift.md` 文件
- **AND** 该文件 SHALL 包含：代码风格（SwiftLint/swiftformat/命名）、类型系统（Protocol/Extension/Enum associated values/Result 类型/Optional）、并发模型（async-await/Task/MainActor/Sendable/AsyncSequence）、错误处理（throw/try/catch/Error 协议）、日志（os.Logger/SwiftLog）、测试规范（XCTest/XCTestCase/Swift Testing Framework/mock）、审查清单 共 7 个章节

#### Scenario: iOS/macOS 特有约定 <!-- confidence: high -->

- **GIVEN** 项目为 iOS/macOS 项目（`project.language == "swift"`）
- **WHEN** Phase 4 Step 0 读取 Swift 规范
- **THEN** 规范 SHALL 包含平台特有章节：SwiftUI 约定（View 协议/MVVM）、Combine 的使用场景与限制、AppKit/UIKit 桥接约定、Xcode 项目结构

---

### Requirement: Swift 规范与模板结构一致 <!-- confidence: high -->

Swift 规范 SHALL 与其他语言规范共享相同的 7 章顶级结构。

**证据来源**：proposal.md `Success Criteria`

#### Scenario: 七章结构完整 <!-- confidence: high -->

- **GIVEN** `.stdd/standards/python.md` 包含 7 个章节
- **WHEN** 对比 Swift 规范和 Python 规范的章节结构
- **THEN** Swift 规范 SHALL 包含：代码风格、类型系统、并发模型、错误处理、日志、测试规范、审查清单 共 7 个顶级章节
- **AND** 各章节内容 SHALL 根据 Swift/Apple 生态定制
