# Java 开发规范

> 适用版本：Java 17+
> 最后更新：2026-05-15
> 标记：Initial version — validated on Python patterns, language-specific review needed

## 一、代码风格

### 1.1 格式化

- 使用 Google Java Format 或 Spotless 作为 formatter
- 行宽：120 字符
- 缩进：4 空格（禁止 Tab）
- 大括号：K&R 风格（左括号不换行）
- 文件末尾：一个空行

### 1.2 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 包 | 小写，点分隔，无下划线 | `com.example.message.service` |
| 类/接口 | PascalCase | `MessageService`, `MessageRepository` |
| 方法 | camelCase | `processMessage()` |
| 变量 | camelCase | `userId`, `messageCount` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 枚举 | PascalCase（值 UPPER_SNAKE_CASE） | `Status.PENDING` |
| 测试方法 | camelCase，可加下划线 | `shouldReturnUser_whenOpenidExists()` |

### 1.3 Import 顺序

1. 静态导入（`import static`）
2. `java.*` 包
3. `javax.*` 包
4. 第三方库
5. 项目内部包

每组之间空一行。禁止 `import xxx.*`（通配符导入）。

## 二、类型系统

### 2.1 泛型

- 公共 API 优先使用泛型，避免原始类型（raw type）
- 通配符：Producer Extends, Consumer Super（PECS 原则）

### 2.2 注解

- 所有 `@Override` 方法必须加注解
- 函数式接口加 `@FunctionalInterface`
- 弃用方法加 `@Deprecated` 并指明替代方式

### 2.3 空安全

- 公共方法返回值优先返回 `Optional<T>` 而非 null
- 参数可空时加 `@Nullable` 注解
- 禁止返回 null 集合，返回空集合

## 三、并发模型

### 3.1 虚拟线程（Java 21+）

- IO 密集型任务使用虚拟线程 `Thread.startVirtualThread()`
- 不要池化虚拟线程，它们是即用即弃的

### 3.2 CompletableFuture

- 异步编排使用 `CompletableFuture` 链式调用
- 超时：`orTimeout()` 和 `completeOnTimeout()`
- 异常处理：`exceptionally()` / `handle()`

### 3.3 线程安全

- 共享可变状态使用 `synchronized` 或 `ReentrantLock`
- 高并发读多写少使用 `ReadWriteLock`
- 集合类优先使用 `ConcurrentHashMap`、`CopyOnWriteArrayList`

## 四、错误处理

### 4.1 原则

- 只在系统边界捕获异常（Controller、消息入口）
- 内部方法让异常向上传播
- 捕获具体异常类型，禁止裸 `catch (Exception e)`（除系统边界外）
- 日志记录完整堆栈：`log.error("msg", e)`

### 4.2 异常分层

| 层 | 异常类型 | 示例 |
|----|---------|------|
| Controller | 不抛异常，返回错误码 | `Result.error(CODE, msg)` |
| Service | 业务异常 `BusinessException` | `throw new BusinessException("用户不存在")` |
| Repository | 包装为 `DataAccessException` | `throw new DataAccessException(e)` |

### 4.3 用户可见错误

- 业务异常 message 为中文用户友好信息
- 不在用户消息中暴露堆栈或 SQL

## 五、日志

### 5.1 框架

- 使用 SLF4J + Logback
- Lombok `@Slf4j` 简化 Logger 声明

### 5.2 规则

- 关键业务节点记录 INFO（用户行为、状态变更）
- 异常记录 ERROR 含完整上下文
- 不在循环中打印 DEBUG 日志
- 格式：`log.info("操作描述: key1={}, key2={}", val1, val2)`

## 六、测试规范

### 6.1 测试框架

- JUnit 5（Jupiter）
- Mockito（mock）
- AssertJ（流畅断言）
- ParameterizedTest（参数化）

### 6.2 测试文件组织

- 单元测试：`src/test/java/.../unit/<ClassName>Test.java`
- 集成测试：`src/test/java/.../integration/<Feature>IT.java`
- 测试文件镜像源码包结构

### 6.3 测试命名

```
should<预期结果>_when<条件>
```

示例：`shouldReturnUser_whenOpenidExists()`

### 6.4 Mock 原则

- 单元测试 mock 外部依赖（数据库、API、文件系统）
- 集成测试使用 Testcontainers（真实数据库）
- 使用 `@ExtendWith(MockitoExtension.class)`

## 七、代码审查检查清单

在 Phase 5 VERIFY 中，逐项检查：

- [ ] 死代码：无 `System.out.println`、注释掉的代码块、未使用的 import
- [ ] 命名：名称匹配实际行为（不产生误导）
- [ ] 类型：无 raw type、泛型使用正确、Optional 使用恰当
- [ ] 并发：线程安全集合使用正确、无共享可变状态未保护
- [ ] 安全：无 SQL 注入（PreparedStatement）、无 XSS、密钥不硬编码
- [ ] 错误：边界输入验证、外部调用有超时、异常不吞掉
- [ ] 日志：关键节点有日志、无敏感信息泄露
- [ ] 测试：新行为有测试、断言使用 AssertJ、集成测试用 Testcontainers
- [ ] 注释：只保留 WHY，删除 WHAT
