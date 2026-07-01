# Kotlin 开发规范

> 适用版本：Kotlin 1.9+ / 2.0+
> 最后更新：2026-07-01
> Initial version — validated on Python patterns, language-specific review needed

## 一、代码风格

### 1.1 格式化

- 使用 ktlint 或 detekt 作为 linter 和 formatter
- 行宽：120 字符
- 缩进：4 空格（禁止 Tab）
- 文件末尾：一个空行
- 尾随逗号：启用（`trailingComma: true`）

### 1.2 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | PascalCase | `MessageService.kt` |
| 类/接口 | PascalCase | `MessageService` |
| 函数/方法 | camelCase | `processMessage()` |
| 变量/参数 | camelCase | `userId` |
| 常量（顶层/object 内） | UPPER_SNAKE_CASE | `MAX_MSG_SIZE` |
| 扩展函数 | camelCase | `String.isValid()` |
| 伴生对象成员 | 同常量或 camelCase | |

### 1.3 Import 顺序

1. Kotlin 标准库
2. Android / JDK 包
3. 第三方库
4. 项目内包

不要使用通配符 import（`import com.example.*`），IDE 自动管理。

## 二、类型系统

### 2.1 空安全

- 优先使用非空类型，只在必须时使用可空类型（`?`）
- 使用 `?.`（安全调用）、`?:`（Elvis 操作符）、`!!`（仅当确定非空）
- 避免在公共 API 中返回 `null`，使用 `Result<T>` 或 sealed class 表示可能的失败
- 平台类型（来自 Java）必须显式标注为可空或非空

### 2.2 数据类与密封类

- 纯数据载体使用 `data class`
- 有限状态/结果类型使用 `sealed class` 或 `sealed interface`
- 使用 `value class`（inline class）包装基本类型

```kotlin
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val code: Int, val message: String) : Result<Nothing>()
}
```

### 2.3 扩展函数

- 优先使用扩展函数而非 Utils 类
- 扩展函数应为纯函数或无副作用的转换
- 避免滥用扩展函数隐藏核心逻辑

## 三、并发模型

### 3.1 协程

- IO 操作使用 `suspend` 函数 + 协程
- 在 `viewModelScope` 或 `lifecycleScope`（Android）中启动协程
- 使用 `Dispatchers.IO` 进行 IO 操作，`Dispatchers.Default` 进行 CPU 密集操作
- 禁止在 suspend 函数中使用 `runBlocking`

### 3.2 Flow

- 冷数据流使用 `Flow`，热数据流使用 `StateFlow` / `SharedFlow`
- UI 状态管理使用 `StateFlow`（配合 `stateIn()`）
- 一次性事件使用 `Channel` 或 `SharedFlow`（`replay = 0`）

### 3.3 并发安全

- 使用 `Mutex` 保护共享可变状态（替代 `synchronized`）
- 使用 `Semaphore` 限流并发协程数
- 避免在 `withContext(NonCancellable)` 中进行长时间操作
- 确保协程取消传播正确（不吞 `CancellationException`）

## 四、错误处理

### 4.1 规则

- 使用 `Result<T>` 或自定义 sealed class 封装可能失败的操作
- 异常只在真正的异常情况抛出（不用于控制流）
- 捕获具体异常类型，禁止 `catch(e: Exception)` 后不处理
- 协程中异常通过 `CoroutineExceptionHandler` 或 `supervisorScope` 管理

### 4.2 用户可见错误

- 错误消息应为用户友好信息（中文或 i18n key）
- UI 层通过 sealed class 状态驱动错误展示：

```kotlin
sealed class UiState<out T> {
    data object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}
```

## 五、日志

### 5.1 Android

- 使用 `Timber`（Debug 树 + Release 树）
- 关键业务节点记录 INFO 日志（用户行为、状态变更）
- 异常记录 ERROR 日志

### 5.2 非 Android（Ktor / 后端）

- 使用 SLF4J + Logback
- 结构化日志：`logger.info("操作描述: key1={}", value1)`

### 5.3 日志内容

- 必须包含足够的上下文信息（userId, requestId）
- 敏感信息（密码、token）不记录到日志

## 六、测试规范

### 6.1 测试框架

- 单元测试：JUnit5 + MockK
- 协程测试：kotlinx-coroutines-test
- Flow 测试：Turbine
- Android UI 测试：Compose UI Test / Robolectric

### 6.2 测试文件组织

- 单元测试：`src/test/kotlin/<package>/<Module>Test.kt`
- Android 测试：`src/androidTest/kotlin/<package>/`

### 6.3 测试命名

```kotlin
// 方法名 + 场景 + 预期
@Test
fun `processMessage with empty content returns error`() = runTest {
    // ...
}
```

### 6.4 Mock 原则

- 单元测试 mock 外部依赖（Repository、API、Database）
- 使用 `mockk` 的 `coEvery`/`coVerify` 处理 suspend 函数
- 集成测试使用内存数据库（Room.inMemoryDatabaseBuilder）或 TestContainer

## 七、Android 特有约定

### 7.1 Jetpack Compose

- `@Composable` 函数使用 PascalCase 命名
- State hoisting：状态提升到调用方，子组件无状态
- Preview 函数标注 `@Preview`，多个 Preview 展示不同状态
- 避免在 Composable 中进行副作用操作，使用 `LaunchedEffect` / `SideEffect`

### 7.2 ViewModel 模式

- ViewModel 暴露 `StateFlow<UiState>` 给 UI
- 用户操作通过 ViewModel 方法处理（`onEvent()` 模式）
- ViewModel 不应持有 Context 引用（使用 `AndroidViewModel` 时小心）

### 7.3 依赖注入

- 使用 Hilt（推荐）或 Koin 进行依赖注入
- `@HiltAndroidApp`、`@AndroidEntryPoint`、`@HiltViewModel`
- 测试中使用 `@UninstallModules` 替换生产依赖为测试 mock

## 八、代码审查检查清单

在 Phase 5 VERIFY 中，逐项检查：

- [ ] 死代码：无注释掉的代码、无未使用的 import/函数/变量
- [ ] 命名：名称匹配实际行为（不产生误导）
- [ ] 空安全：无不必要的 `!!` 操作、平台类型已标注可空性
- [ ] 协程：suspend 函数在正确的 Dispatcher 中运行、无 `runBlocking`
- [ ] 安全：无 SQL 注入、无 XSS、token 不硬编码、ProGuard 已配置
- [ ] 错误：边界输入验证、外部调用有超时、协程取消有正确处理
- [ ] 日志：关键节点有日志、无敏感信息泄露
- [ ] 测试：新行为有测试、UI 状态覆盖 Loading/Success/Error
- [ ] Compose：无副作用在 Composable 函数体中、State hoisting 正确
- [ ] DI：依赖通过构造函数注入、无 Service Locator 反模式
- [ ] 注释：只保留 WHY，删除 WHAT
