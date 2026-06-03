# Go 编码规则

1. 错误处理：`if err != nil` 不可省略，error 必须被处理或显式忽略
2. 并发：使用 `context.Context` 传递取消信号
3. JSON tag：所有对外 API 结构体显式写 `json:"field_name"`
4. 命名：导出符号 PascalCase，非导出 camelCase
