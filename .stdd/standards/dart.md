# Dart / Flutter 开发规范

> 适用版本：Dart 3.0+ / Flutter 3.16+
> 最后更新：2026-07-01
> Initial version — validated on Python patterns, language-specific review needed

## 一、代码风格

### 1.1 格式化

- 使用 `dart format` + `dart analyze` 作为 formatter 和 linter
- 行宽：80 字符（Dart 默认）
- 缩进：2 空格（禁止 Tab）
- 尾随逗号：启用（有助于 diff 可读性和自动格式化）
- 文件末尾：一个空行
- 使用 `flutter_lints` 或 `very_good_analysis` 包

### 1.2 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | snake_case | `message_service.dart` |
| 类/枚举/混入 | PascalCase | `MessageService` |
| 函数/方法/变量 | camelCase | `processMessage()` |
| 常量 | camelCase（Dart 风格）或 UPPER_SNAKE_CASE（团队统一） | `maxMsgSize` |
| 私有成员 | 前缀 `_` | `_cache` |
| 扩展名 | PascalCase | `StringValidation` |

### 1.3 Import 顺序

1. `dart:` 内置库
2. `package:flutter/` Flutter 库
3. `package:` 第三方库
4. `package:` 项目内包
5. 相对路径（`../`）

每组之间空一行。不导入未使用的包。

## 二、类型系统

### 2.1 空安全

- Dart 3.0+ 强制空安全
- 优先使用非空类型，使用 `?` 明确标注可空类型
- 使用 `?.`、`??`、`!`（仅当确定非空）
- 避免 `late` 变量（除非延迟初始化确定发生）
- 使用 `required` 标注必须的命名参数

### 2.2 密封类与模式匹配（Dart 3.0+）

```dart
sealed class Result<T> {
  const Result();
}
class Success<T> extends Result<T> {
  final T data;
  const Success(this.data);
}
class Error<T> extends Result<T> {
  final String message;
  const Error(this.message);
}

// Pattern matching
switch (result) {
  Success(data: final d) => print('OK: $d'),
  Error(message: final m) => print('Error: $m'),
}
```

### 2.3 扩展类型与 Record

- 使用 `extension type`（Dart 3.3+）包装基本类型增加类型安全
- 使用 Record（`(String, int)`）返回多个值（函数返回值）
- 使用 `typedef` 定义函数类型别名

## 三、并发模型

### 3.1 Future 与 async/await

- IO 操作使用 `Future` + `async/await`
- 外部 HTTP 调用使用 `package:http` 或 `dio`
- 避免在 `build()` 方法中调用 `async` 操作
- 使用 `Future.wait` 并发多个异步操作

### 3.2 Stream

- UI 事件流使用 `Stream` / `StreamController`
- 使用 `StreamBuilder` 在 Widget 中响应流数据
- 关闭 `StreamController` 在 `dispose()` 中

### 3.3 Isolate

- CPU 密集操作使用 `Isolate` 或 `compute()`
- 避免在主 Isolate 中执行耗时计算
- 大文件处理、图片压缩等使用 `compute(function, data)`

## 四、错误处理

### 4.1 规则

- 使用 `try/catch/finally` 处理异常
- 捕获具体异常类型（`on FormatException catch (e)`）
- 避免 `catch (e)` 后不处理
- 使用 `rethrow` 保留原始堆栈

### 4.2 用户可见错误

- UI 层通过状态驱动错误展示：

```dart
// 使用 sealed class 或 freezed
@freezed
sealed class UiState<T> with _$UiState<T> {
  const factory UiState.loading() = Loading;
  const factory UiState.success(T data) = Success;
  const factory UiState.error(String message) = Error;
}
```

## 五、日志

### 5.1 规则

- 使用 `package:logging` + Flutter DevTools
- Debug 模式使用 `debugPrint`
- Release 模式使用 Crashlytics 等崩溃收集服务

### 5.2 日志内容

- 关键业务节点记录 INFO 日志
- 异常记录 ERROR 日志（含 `stackTrace`）
- 格式：`'操作描述: key1=$value1, key2=$value2'`
- 敏感信息不记录到日志

## 六、Flutter 特有约定

### 6.1 Widget 树

- `const` 构造：优先使用 const 构造函数（性能优化）
- `StatelessWidget` 优先：无内部状态时使用 StatelessWidget
- Widget 拆分：build 方法不超过 50 行，超过则提取子 Widget
- Key：列表项使用 `ValueKey` 或 `ObjectKey`（不用 index 做 key）
- 避免在 `build()` 中创建复杂对象（移到 `initState()` 或 DI）

### 6.2 状态管理

- 推荐方案：Riverpod（首选）或 flutter_bloc
- Provider 用于简单依赖注入
- 状态提升：子 Widget 通过回调通知父 Widget
- 避免 `setState` 触发不必要的重建

### 6.3 BuildContext 使用

- 不在异步回调中使用 BuildContext（先检查 `mounted`）
- 不在 `dispose()` 后使用 BuildContext
- `Navigator.of(context)` 确保在正确的 Navigator context 中调用

### 6.4 性能

- 使用 `const` Widget 减少重建
- 使用 `RepaintBoundary` 隔离重绘区域
- 列表使用 `ListView.builder`（而非 `ListView(children: [])`）
- 图片使用 `cached_network_image` 缓存
- 使用 DevTools Performance 检查帧率

## 七、测试规范

### 7.1 测试金字塔（Flutter）

| 层次 | 工具 | 占比 | 速度 |
|------|------|------|------|
| Unit（单元） | `flutter test` | 70% | 快 |
| Widget（组件） | `testWidgets()` | 20% | 中 |
| Integration（集成） | `integration_test` | 10% | 慢 |

### 7.2 单元测试

```dart
test('processMessage with empty content returns error', () {
  final service = MessageService();
  final result = service.processMessage('');
  expect(result, isA<Error>());
});
```

### 7.3 Widget 测试

```dart
testWidgets('shows error message on failure', (tester) async {
  await tester.pumpWidget(MyApp());
  await tester.tap(find.text('Submit'));
  await tester.pump();
  expect(find.text('请输入内容'), findsOneWidget);
});
```

### 7.4 Mock 原则

- 使用 `mocktail` 或 `mockito` mock 依赖
- 单元测试 mock Repository/API
- Widget 测试使用 mock ViewModel/Provider
- Golden 测试：`matchesGoldenFile()` 用于视觉回归

## 八、代码审查检查清单

在 Phase 5 VERIFY 中，逐项检查：

- [ ] 死代码：无注释掉的代码、无未使用的 import/变量/函数
- [ ] 命名：名称匹配实际行为（不产生误导）
- [ ] 空安全：无不必要的 `!` 操作、`late` 延迟初始化确定发生
- [ ] 异步：IO 操作使用 async/await、Future 错误有处理
- [ ] 安全：无 XSS（WebView）、token 不硬编码、使用 flutter_secure_storage
- [ ] 错误：边界输入验证、外部调用有超时、异常路径有覆盖
- [ ] 日志：关键节点有日志、无敏感信息泄露
- [ ] Widget：const 构造使用、build 方法简洁、列表有 Key
- [ ] 状态管理：状态提升正确、`mounted` 检查、`setState` 影响范围合理
- [ ] 性能：无不必要的重建、大列表使用 builder、图片有缓存
- [ ] 测试：新行为有测试、Widget 测试覆盖关键交互
- [ ] 注释：只保留 WHY，删除 WHAT
