# Swift 开发规范

> 适用版本：Swift 5.9+ / 6.0+
> 最后更新：2026-07-01
> Initial version — validated on Python patterns, language-specific review needed

## 一、代码风格

### 1.1 格式化

- 使用 SwiftLint + swiftformat 作为 linter 和 formatter
- 行宽：120 字符
- 缩进：4 空格（禁止 Tab）
- 文件末尾：一个空行
- 冒号：类型标注冒号后加空格（`let name: String`），字典冒号前后加空格

### 1.2 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | PascalCase | `MessageService.swift` |
| 类/结构体/枚举/协议 | PascalCase | `MessageService` |
| 函数/方法 | camelCase | `processMessage()` |
| 变量/常量 | camelCase | `userId` |
| 枚举 case | camelCase | `.success`, `.networkError` |
| 静态/类属性 | camelCase | `defaultConfig` |
| 协议名称 | 名词（能力）或 -able/-ible/-ing | `Codable`, `Hashable`, `Requesting` |

### 1.3 代码组织

- 使用 `// MARK: - <Section>` 分隔代码段
- Extension 按协议遵循分组
- 文件内顺序：类型定义 → 初始化 → 公共方法 → 私有方法 → Extension

## 二、类型系统

### 2.1 协议与泛型

- 优先使用协议（Protocol-Oriented Programming）而非继承
- 使用 `associatedtype` 定义协议关联类型
- 泛型约束使用 `where` 子句
- 存在类型使用 `any Protocol`（Swift 5.9+）或 `some Protocol`（opaque type）

### 2.2 Optional 处理

- 使用 `if let` / `guard let` 安全解包
- 避免强制解包（`!`），除非上下文确定非空
- 使用 `??` 提供默认值
- `Optional` 链式调用优先于嵌套 `if let`

### 2.3 枚举

- 关联值枚举用于携带数据（`case success(Data)`）
- Raw value 枚举用于序列化（`enum Status: String`）
- 使用 `Result<T, Error>` 代替 throws 作为显式错误传递
- 使用 `@unknown default` 处理未来可能新增的 case

## 三、并发模型

### 3.1 async/await（Swift 5.5+）

- IO 操作使用 `async` 函数 + `await`
- 使用 `Task` 从同步上下文启动异步操作
- `Task.detached` 仅在需要完全独立上下文时使用
- 主线程 UI 更新使用 `MainActor.run` 或 `@MainActor` 标注

### 3.2 Actor 与 Sendable

- 共享可变状态使用 `actor` 隔离
- 值类型和不可变引用标注 `Sendable`
- 使用 `nonisolated` 标注不需隔离的 actor 成员
- 避免数据竞争：编译器会检查 `Sendable` 一致性

### 3.3 TaskGroup

- 并发任务组使用 `withTaskGroup` / `withThrowingTaskGroup`
- 限制并发数使用 `maxConcurrentTasks` 参数
- 子任务抛出的错误通过 `next()` 传播

## 四、错误处理

### 4.1 规则

- 使用 `throw`/`throws`/`try` 处理可恢复错误
- 使用 `do-catch` 捕获具体错误类型
- 自定义错误类型遵循 `Error` 协议
- 使用 `try?` 将错误转换为 nil（仅在不关心具体错误时）
- 不要使用 `try!` 除非绝对确定不会失败

### 4.2 错误类型设计

```swift
enum ServiceError: LocalizedError {
    case networkUnavailable
    case invalidResponse(statusCode: Int)
    case decodingFailed(underlying: Error)

    var errorDescription: String? {
        switch self {
        case .networkUnavailable: return "网络不可用"
        case .invalidResponse(let code): return "服务器返回异常 (HTTP \(code))"
        case .decodingFailed: return "数据解析失败"
        }
    }
}
```

## 五、日志

### 5.1 规则

- 使用 `os.Logger`（iOS 14+ / macOS 11+）或 SwiftLog
- 级别：debug < info < notice < error < fault
- 关键业务节点记录 info 日志
- 异常记录 error 日志

### 5.2 日志内容

- 必须包含足够的上下文信息
- 格式：`"操作描述: key1=\(value1), key2=\(value2)"`
- 敏感信息（密码、token）不记录到日志
- 使用 `OSLogPrivacy` 控制隐私级别（`.public` / `.private` / `.auto`）

## 六、测试规范

### 6.1 测试框架

- XCTest（Apple 官方框架）
- Swift Testing Framework（Swift 6.0+，新项目推荐）
- Mock：手动协议 mock / Cuckoo / SwiftyMocky

### 6.2 测试文件组织

- 单元测试：`Tests/<Module>Tests/<File>Tests.swift`
- UI 测试：`UITests/`

### 6.3 测试命名

```swift
func test_<method>_<scenario>_<expectedResult>() { }
```

示例：
```swift
func test_processMessage_emptyContent_returnsError() { }
```

### 6.4 Mock 原则

- 通过协议定义依赖接口（面向协议编程）
- 测试中注入 mock 实现
- 使用 `XCTAssert` 家族断言：
  - `XCTAssertEqual`（值比较）
  - `XCTAssertThrowsError`（异常断言）
  - `XCTAssertNoThrow`（确认不抛出）
  - `XCTUnwrap`（解包非空断言）

## 七、iOS/macOS 特有约定

### 7.1 SwiftUI

- View 遵循单一职责：一个 View 只负责一个 UI 区域
- 使用 `@State` 管理 View 局部状态，`@StateObject`/`@ObservedObject` 管理外部状态
- 使用 `@Environment` 读取环境值（而非层层传递）
- Preview 提供多种设备/暗黑模式/动态字体预览

### 7.2 MVVM 模式

- ViewModel 用 `@Observable`（Swift 5.9+）或 `ObservableObject`（传统）
- ViewModel 不持有 View 引用，只暴露 `@Published` 状态
- 网络请求在 ViewModel 的 async 方法中执行

### 7.3 Combine

- 使用 Combine 处理异步事件流
- 操作符链不超过 5 个（过长则提取为方法）
- 使用 `AnyCancellable` 存储订阅，确保适时取消
- 优先使用 Swift Concurrency（async/await）替代 Combine（Swift 5.5+）

## 八、代码审查检查清单

在 Phase 5 VERIFY 中，逐项检查：

- [ ] 死代码：无注释掉的代码、无未使用的 import/变量/函数
- [ ] 命名：名称匹配 Swift API Design Guidelines
- [ ] Optional：无强制解包 `!`，guard let 提前返回
- [ ] 并发：无数据竞争（Sendable 检查）、MainActor 正确标注
- [ ] 安全：无 XSS（WebView）、token 不硬编码、Keychain 存储敏感数据
- [ ] 错误：边界输入验证、外部调用有超时、异常路径有覆盖
- [ ] 日志：关键节点有日志、隐私级别正确、无敏感信息泄露
- [ ] 测试：新行为有测试、异步操作使用 expectation
- [ ] SwiftUI：View 无副作用、Preview 提供多状态
- [ ] 内存：无循环引用（weak self 在闭包中）、instruments 检查无泄漏
- [ ] 注释：只保留 WHY，删除 WHAT
