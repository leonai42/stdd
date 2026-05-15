# Rust 开发规范

> 适用版本：Rust 1.75+ (Edition 2021)
> 最后更新：2026-05-15
> 标记：Initial version — validated on Python patterns, language-specific review needed

## 一、代码风格

### 1.1 格式化

- 使用 `rustfmt` 自动格式化（`cargo fmt`）
- 行宽：100 字符
- 缩进：4 空格（禁止 Tab）
- 文件末尾：一个空行

### 1.2 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块/文件 | snake_case | `message_service.rs` |
| 结构体/枚举/Trait | PascalCase | `MessageService`, `MessageStatus` |
| 函数/方法 | snake_case | `process_message()` |
| 变量 | snake_case | `user_id` |
| 常量/静态变量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 宏 | snake_case 或以 `!` 结尾 | `println!` |
| 测试函数 | snake_case，描述场景 | `test_process_message_invalid_input()` |

### 1.3 Import 顺序

1. 标准库（`std::`）
2. 第三方 crate
3. `crate::` 内部模块
4. `super::` 父模块
5. `self::` 当前模块

每组之间空一行。使用 `rustfmt` 自动排列。

## 二、类型系统

### 2.1 枚举与模式匹配

- 优先使用 `enum` 而非魔法值表示状态
- 所有 `match` 必须是穷举的（或使用 `_ =>` 通配）
- 错误类型使用 `enum` 定义变体

### 2.2 泛型与 Trait

- Trait 定义共享行为，泛型实现代码复用
- Trait bound 使用 `where` 子句提高可读性
- Derive 常用 trait：`Debug`, `Clone`, `Serialize`, `Deserialize`

### 2.3 Ownership

- 优先使用引用（`&T` / `&mut T`）避免不必要的 clone
- 大对象使用 `Arc<T>` 共享所有权
- 遵循 RAII：资源在构造时获取，析构时释放

## 三、并发模型

### 3.1 异步运行时

- 使用 `tokio` 作为异步运行时（全功能）
- 或 `async-std`（轻量场景）
- 异步函数以 `async fn` 声明，调用时加 `.await`

### 3.2 线程安全

- 共享不可变数据：`Arc<T>`
- 共享可变数据：`Arc<Mutex<T>>` / `Arc<RwLock<T>>`
- 消息传递：`tokio::sync::mpsc` / `std::sync::mpsc`
- 避免在锁内做 `.await`（或使用 `tokio::sync::Mutex`）

### 3.3 并发原语

- 简单状态标记使用 `AtomicBool` / `AtomicUsize`
- 一次性初始化使用 `OnceLock` / `LazyLock`

## 四、错误处理

### 4.1 原则

- 可恢复错误使用 `Result<T, E>`
- 不可恢复错误使用 `panic!` 或 `expect()`
- 不在库代码中 `unwrap()`，使用 `?` 传播错误
- 使用 `anyhow`（应用层）/ `thiserror`（库层）管理错误

### 4.2 错误传播

- 使用 `?` 运算符向上传播
- 自定义错误类型实现 `std::error::Error` + `Display`
- 错误上下文：`.context("操作描述")?`（anyhow）

### 4.3 用户可见错误

- 只在 API 入口层将 error 转化为用户消息
- 不在用户消息中暴露文件路径或堆栈

## 五、日志

### 5.1 框架

- 使用 `tracing`（结构化日志 + span）
- 或 `log` + `env_logger`（简单场景）

### 5.2 规则

- 关键业务节点记录 INFO（用户行为、状态变更）
- 异常记录 ERROR 含 span 上下文
- 不在循环中打印 DEBUG 日志
- 格式：`info!(user_id = %id, "操作描述")`

## 六、测试规范

### 6.1 测试框架

- 内置 `#[test]` 属性
- `rstest`（参数化/fixture）
- `proptest`（属性测试）
- `mockall`（mock 生成）

### 6.2 测试文件组织

- 单元测试：与源文件同文件，放在 `#[cfg(test)] mod tests {}` 内
- 集成测试：`tests/` 目录下，每个文件是独立的 crate
- 文档测试：`///` 中的代码块自动作为测试运行

### 6.3 测试命名

```rust
#[test]
fn test_<函数名>_<场景>() { ... }
```

### 6.4 Mock 原则

- 使用 trait 抽象外部依赖，测试中提供 mock 实现
- 或使用 `mockall` 自动生成 mock
- 不要 mock 内部模块间调用
- 集成测试使用真实依赖（数据库可用 testcontainers）

## 七、代码审查检查清单

在 Phase 5 VERIFY 中，逐项检查：

- [ ] 死代码：无 `println!` / `dbg!` 调试输出、注释掉的代码、未使用的 import
- [ ] 命名：名称匹配实际行为（不产生误导）
- [ ] 类型：枚举穷举、无 `unwrap()` 裸调用、Trait 使用合理
- [ ] 并发：无锁内 `.await`、Arc/Mutex 使用正确、channel 正确关闭
- [ ] 安全：无 SQL 注入（参数化）、无 XSS、密钥不硬编码、unsafe 块有注释说明
- [ ] 错误：Result 正确处理、`?` 传播、错误上下文完整
- [ ] 日志：关键节点有日志、无敏感信息泄露
- [ ] 测试：新行为有测试、使用 `cargo test --all-features`
- [ ] 注释：只保留 WHY，删除 WHAT、文档注释使用 `///`
