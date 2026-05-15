# Go 开发规范

> 适用版本：Go 1.21+
> 最后更新：2026-05-15
> 标记：Initial version — validated on Python patterns, language-specific review needed

## 一、代码风格

### 1.1 格式化

- 使用 `gofmt` 或 `goimports` 自动格式化
- 缩进：Tab（Go 标准）
- 导入路径使用 `goimports` 自动管理
- 文件末尾：一个空行

### 1.2 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 包 | 小写，简短，无下划线 | `messageservice` |
| 接口 | 单方法接口加 `-er` 后缀 | `Reader`, `Writer` |
| 结构体 | PascalCase（公开）/ camelCase（私有） | `MessageService`, `messageConfig` |
| 方法 | PascalCase（公开）/ camelCase（私有） | `ProcessMessage()`, `validateInput()` |
| 变量 | camelCase | `userId`, `messageCount` |
| 常量 | PascalCase（公开）/ camelCase（私有） | `MaxRetryCount`, `defaultTimeout` |
| 测试函数 | `Test<函数名>_<场景>` | `TestProcessMessage_InvalidInput` |

### 1.3 Import 顺序

1. 标准库
2. 第三方库
3. 项目内部包

每组之间空一行。使用 `goimports` 自动管理。

## 二、类型系统

### 2.1 接口

- 接口应该小而聚焦（1-3 个方法）
- 在使用方定义接口，而非实现方
- 接受接口，返回结构体

### 2.2 结构体

- 字段按字节对齐排列以节省内存
- 嵌入（embedding）时注意命名冲突
- 零值可用：`sync.Mutex` 不需要初始化

### 2.3 泛型（Go 1.18+）

- 用于容器类型和通用算法
- 不要为了"抽象"引入不必要的泛型
- 约束接口命名以 `Constraint` 结尾

## 三、并发模型

### 3.1 Goroutine

- 每个 goroutine 必须有明确的退出路径
- 使用 `context.Context` 传递取消信号和超时
- 不要在新 goroutine 中直接使用循环变量

### 3.2 Channel

- 生产者负责 close channel
- 优先使用 `select` 处理多 channel
- buffered channel 容量必须有理有据

### 3.3 并发安全

- 共享可变状态使用 `sync.Mutex` 或 `sync.RWMutex`
- 简单计数使用 `sync/atomic`
- 复杂编排使用 `golang.org/x/sync/errgroup`

## 四、错误处理

### 4.1 原则

- 不忽略 error：每个 error 都必须处理或显式忽略（`_ =`）
- error 向上传播时用 `fmt.Errorf` 包装上下文
- 使用 `errors.Is` / `errors.As` 做类型判断，不要用 `==`

### 4.2 Sentinel Errors

- 包级别定义常用错误：`var ErrNotFound = errors.New("not found")`
- 调用方使用 `errors.Is(err, pkg.ErrNotFound)` 判断

### 4.3 用户可见错误

- 只在 API 入口层将 error 转化为用户消息
- 不在用户消息中暴露堆栈或内部实现细节

## 五、日志

### 5.1 框架

- 推荐 `slog`（Go 1.21+ 标准库结构化日志）
- 或 `zerolog`（高性能场景）

### 5.2 规则

- 关键业务节点记录 INFO（用户行为、状态变更）
- 异常记录 ERROR 含请求上下文
- 不在循环中打印 DEBUG 日志
- 格式：`slog.Info("操作描述", "key1", val1, "key2", val2)`

## 六、测试规范

### 6.1 测试框架

- 标准库 `testing` 包
- `testify`（assert/suite/mock）
- 表驱动测试（Table-Driven Tests）

### 6.2 测试文件组织

- 单元测试：`*_test.go` 与源文件同目录
- 集成测试：`tests/integration/` 或 `*_integration_test.go`
- 使用 build tag `//go:build integration` 标记集成测试

### 6.3 表驱动测试

```go
tests := []struct {
    name    string
    input   Input
    want    Output
    wantErr bool
}{
    {name: "正常输入", input: ..., want: ..., wantErr: false},
    {name: "无效输入", input: ..., want: ..., wantErr: true},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) { ... })
}
```

### 6.4 Mock 原则

- 单元测试使用接口 + 手写 mock 或 `mockery` 生成
- 集成测试使用 testcontainers-go（真实依赖）
- 使用 `-race` flag 运行测试检测数据竞争

## 七、代码审查检查清单

在 Phase 5 VERIFY 中，逐项检查：

- [ ] 死代码：无 `fmt.Println` / `fmt.Printf` 调试输出、注释掉的代码、未使用的 import
- [ ] 命名：名称匹配实际行为、缩写全大写（URL, HTTP, ID）或全小写
- [ ] 类型：接口小而聚焦、泛型使用合理、无空接口 `interface{}` 滥用
- [ ] 并发：每个 goroutine 有退出路径、channel 正确关闭、无数据竞争
- [ ] 安全：无 SQL 注入（参数化查询）、无 XSS（html/template）、密钥不硬编码
- [ ] 错误：所有 error 已处理、包装含上下文、使用 errors.Is/As
- [ ] 日志：关键节点有日志、无敏感信息泄露
- [ ] 测试：新行为有测试、表驱动测试、使用 `-race` flag
- [ ] 注释：只保留 WHY（非显而易见的约束），删除 WHAT 注释
