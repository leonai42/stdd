# C/C++ 开发规范

> 适用版本：C11/C17 + C++17/20
> 最后更新：2026-07-01
> Initial version — validated on Python patterns, language-specific review needed

## 一、代码风格

### 1.1 格式化

- 使用 clang-format 作为 formatter（配置 `.clang-format`）
- 行宽：100 字符
- 缩进：4 空格（禁止 Tab）
- 大括号：K&R 风格（函数左括号不换行，控制流左括号不换行）
- 文件末尾：一个空行

### 1.2 命名约定

**C 语言约定**：

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | snake_case | `message_service.c` |
| 函数 | snake_case | `process_message()` |
| 结构体 | snake_case | `message_context` |
| 变量 | snake_case | `user_id` |
| 宏/常量 | UPPER_SNAKE_CASE | `MAX_MSG_SIZE` |
| 全局变量 | 前缀 `g_` | `g_config` |

**C++ 语言约定**：

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | snake_case | `message_service.cpp` |
| 类/结构体 | PascalCase | `MessageService` |
| 函数/方法 | PascalCase 或 snake_case（团队统一） | `ProcessMessage()` |
| 成员变量 | 后缀 `_` | `user_id_` |
| 常量 | kPascalCase 或 UPPER_SNAKE_CASE | `kMaxMsgSize` |
| 命名空间 | snake_case | `message_core` |

### 1.3 Include 顺序

1. 对应的头文件（`message_service.h` 对应 `message_service.c`）
2. C 标准库（`<stdio.h>`, `<stdlib.h>`）
3. C++ 标准库（`<string>`, `<vector>`）
4. 第三方库
5. 项目内头文件

每组之间空一行。使用 `#pragma once`（C++）或传统的 `#ifndef` guard（C）。

## 二、类型系统

### 2.1 通用规则

- 避免隐式类型转换，使用显式 cast
- 指针检查：解引用前必须检查 `NULL`
- 整数类型优先使用 `int32_t`/`uint32_t` 等定宽类型（`<stdint.h>`/`<cstdint>`）

### 2.2 C 语言约定

- 使用 `const` 修饰不修改的指针参数
- 结构体通过指针传递（大结构体避免值拷贝）
- 避免 `void*` 除非实现泛型接口
- 敏感指针释放后置 `NULL`

### 2.3 C++ 语言约定

- 优先使用 `std::optional`（C++17）代替指针表示"可能为空"
- 优先使用 `std::variant` 代替 union
- 使用 `auto` 当类型可从初始化表达式明确推导
- 使用 `nullptr` 而非 `NULL` 或 `0`
- 实现 RAII：资源获取即初始化，析构函数释放资源
- 使用智能指针（`std::unique_ptr`/`std::shared_ptr`）管理堆内存
- Rule of Five：如自定义析构/拷贝/移动之一，全部定义或 `= default`
- 模板元编程保持简洁，避免过度抽象

## 三、并发模型

### 3.1 C 语言约定

- 使用 pthread 库（`<pthread.h>`）或 C11 `atomic` + `threads.h`
- 共享数据使用 `pthread_mutex_t` 保护
- 条件变量配合 mutex 使用（`pthread_cond_t`）
- 避免数据竞争：所有共享可变状态的访问必须同步

### 3.2 C++ 语言约定

- 优先使用 `std::thread` + `std::mutex` + `std::lock_guard`
- 异步任务使用 `std::async` / `std::future`
- 使用 `std::atomic` 进行无锁操作
- 避免死锁：使用 `std::lock` 或 `std::scoped_lock`（C++17）同时锁定多个 mutex
- 线程安全容器：使用 `std::shared_mutex` 实现读写锁

## 四、错误处理

### 4.1 C 语言约定

- 函数通过返回错误码（`int`）表示成功/失败（0 成功，非 0 错误）
- 使用 `errno` 报告系统调用错误
- 使用 `assert()` 捕获不应发生的逻辑错误（仅 Debug 模式）
- 资源清理使用 `goto cleanup` 模式：

```c
int process_data(const char* path) {
    FILE* fp = NULL;
    char* buf = NULL;
    int ret = 0;

    fp = fopen(path, "r");
    if (!fp) { ret = -1; goto cleanup; }
    buf = malloc(BUFSIZE);
    if (!buf) { ret = -2; goto cleanup; }
    // ... process ...
cleanup:
    free(buf);
    if (fp) fclose(fp);
    return ret;
}
```

### 4.2 C++ 语言约定

- 使用异常处理（`throw`/`try`/`catch`）报告可恢复错误
- 捕获具体异常类型，禁止 `catch(...)` 静默忽略
- 析构函数不应抛出异常（标记 `noexcept`）
- `std::error_code` 或 `std::expected`（C++23）用于性能敏感的错误传递
- 构造函数失败抛出异常，RAII 确保已分配资源自动清理

## 五、日志

### 5.1 C 语言约定

- 使用 syslog（POSIX）或项目内轻量日志宏
- 级别：DEBUG < INFO < WARN < ERROR
- 编译时可通过宏开关关闭 DEBUG 日志

### 5.2 C++ 语言约定

- 使用 spdlog 或 Boost.Log 作为结构化日志库
- 关键业务节点记录 INFO 日志
- 异常记录 ERROR 日志（含 `what()` 和上下文信息）
- 敏感信息（密码、密钥）不记录到日志

### 5.3 日志内容

- 格式：`操作描述: key1=value1, key2=value2`
- 系统调用失败记录 errno 描述（`strerror(errno)`）

## 六、测试规范

### 6.1 测试框架

- C++：Google Test (GTest) / Catch2
- C：CMocka 或 Unity Test
- Mock：Google Mock (GMock) / Fake Function Framework (FFF)

### 6.2 测试文件组织

- 单元测试：`tests/unit/test_<module>.cpp`（与源码模块对应）
- 集成测试：`tests/integration/test_<feature>.cpp`

### 6.3 测试命名

```
TEST(<Module>Test, <Method>_<Scenario>_<ExpectedResult>)
```

示例：
```cpp
TEST(MessageServiceTest, ProcessMessage_EmptyContent_ReturnsError)
```

### 6.4 Mock 原则

- 单元测试 mock 外部依赖（IO、网络、硬件）
- 集成测试不 mock 文件系统（使用临时目录）
- 使用依赖注入（接口/函数指针）支持可测试性

## 七、代码审查检查清单

在 Phase 5 VERIFY 中，逐项检查：

- [ ] 死代码：无注释掉的代码、无未使用的函数/变量
- [ ] 命名：名称匹配实际行为（不产生误导）
- [ ] 内存：无内存泄漏（malloc/free 配对，new/delete 配对，智能指针）、无悬空指针
- [ ] 类型：指针解引用前检查 NULL、显式类型转换、无符号/有符号混用警告
- [ ] 并发：共享数据有 mutex 保护、无数据竞争、无死锁风险
- [ ] 安全：无缓冲区溢出（使用安全函数如 `strncpy`/`snprintf`）、无格式化字符串漏洞、输入验证
- [ ] 错误：系统调用返回值已检查、资源分配失败有处理
- [ ] 日志：关键节点有日志、无敏感信息泄露
- [ ] 测试：新行为有测试、边界条件和错误路径有覆盖
- [ ] RAII（C++）：资源在析构函数中释放、异常安全
- [ ] 注释：只保留 WHY，删除 WHAT
