# TypeScript 开发规范

> 适用版本：TypeScript 5.0+ / Node.js 18+
> 最后更新：2026-05-15
> 标记：Initial version — validated on Python patterns, language-specific review needed

## 一、代码风格

### 1.1 格式化

- 使用 Prettier 作为 formatter
- 行宽：100 字符
- 缩进：2 空格（禁止 Tab）
- 分号：不强制（Prettier 默认加）
- 引号：单引号
- 文件末尾：一个空行

### 1.2 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件/目录 | kebab-case 或 camelCase | `message-service.ts` |
| 类/接口/类型 | PascalCase | `MessageService`, `MessageConfig` |
| 函数/方法 | camelCase | `processMessage()` |
| 变量/常量 | camelCase | `userId` |
| 全局常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 私有成员 | 前缀 `_` 或 JS private `#` | `_filterInternal()` |
| 测试文件 | `*.test.ts` / `*.spec.ts` | `message-service.test.ts` |

### 1.3 Import 顺序

1. Node 内置模块（`node:fs`, `node:path`）
2. 第三方库
3. 项目内部模块（`@/` 别名）

每组之间空一行。禁止 `import *`（除命名空间需求外）。

## 二、类型系统

### 2.1 类型 vs 接口

- 优先使用 `interface` 定义对象形状（可扩展）
- 联合类型/元组/映射类型使用 `type`
- 函数签名使用 `type`

### 2.2 泛型

- 泛型命名：单字母 T, K, V 或描述性名称
- 约束：`<T extends SomeType>`
- 使用 `unknown` 替代 `any`，需要时才做类型守卫

### 2.3 类型守卫

- 使用 `typeof`、`instanceof`、`in` 操作符
- 自定义类型守卫：`function isXxx(value: unknown): value is Xxx`
- 使用 `zod` 做运行时类型校验

## 三、异步模型

### 3.1 Promise / async-await

- 异步操作优先使用 `async/await`
- 错误处理：`try/catch` 包裹 await
- 并行请求使用 `Promise.all` / `Promise.allSettled`

### 3.2 取消与超时

- 使用 `AbortController` + `AbortSignal` 取消请求
- 超时封装：`Promise.race([fetch(), timeout(5000)])`

### 3.3 事件驱动

- 使用 `EventEmitter`（Node.js）或 `EventTarget`（浏览器）
- 及时移除事件监听器防止内存泄漏
- 避免回调地狱：大于 2 层回调 → 改为 async/await

## 四、错误处理

### 4.1 原则

- 只在系统边界捕获异常（API 入口、事件处理入口）
- 内部函数让异常向上传播
- 捕获具体 Error 子类，尽量避免裸 `catch (e)`
- 日志记录完整上下文

### 4.2 Result 类型

- 推荐使用 `Result<T, E>` 类型（如 `neverthrow` 库）替代抛异常
- 明确区分业务错误和系统错误

### 4.3 用户可见错误

- 只在 Controller/Handler 层将 error 转化为用户消息
- 不在用户消息中暴露堆栈或内部实现

## 五、日志

### 5.1 框架

- Node.js：`pino`（结构化高性能日志）
- 浏览器：`loglevel` 或自定义 wrapper

### 5.2 规则

- 关键业务节点记录 INFO
- 异常记录 ERROR 含请求 ID
- 不在循环中打印 DEBUG 日志
- 格式：`logger.info({ userId, action }, '操作描述')`

## 六、测试规范

### 6.1 测试框架

- 单元测试：Vitest（推荐）/ Jest
- 组件测试：Testing Library（React/Vue）
- E2E：Playwright

### 6.2 测试文件组织

- 单元测试：`*.test.ts` 与源文件同目录或 `__tests__/` 子目录
- 集成测试：`tests/integration/`
- E2E 测试：`tests/e2e/`

### 6.3 测试命名

```typescript
describe('MessageService', () => {
  it('should return user when openid exists', async () => { ... });
});
```

命名模式：`should<预期结果>_when<条件>`

### 6.4 Mock 原则

- 使用 `vi.mock()` (Vitest) 或 `jest.mock()` mock 外部模块
- 使用 `vi.spyOn()` 对单个方法做 spy
- 集成测试不 mock 数据库，使用测试容器
- 测试断言验证行为（WHAT），不验证实现细节（HOW）

### 6.5 Parametrize

- 同类场景多输入变体使用 `it.each([])` (Jest/Vitest)
- 每个参数集测试不同的边界条件

## 七、代码审查检查清单

在 Phase 5 VERIFY 中，逐项检查：

- [ ] 死代码：无 `console.log` / `console.debug` 调试输出、注释掉的代码块、未使用的 import
- [ ] 命名：名称匹配实际行为（不产生误导）
- [ ] 类型：无 `any` 滥用、严格模式（`strict: true`）、类型守卫完整
- [ ] 异步：async/await 使用正确、Promise 错误已捕获、无竞态条件
- [ ] 安全：无 XSS（DOMPurify/模板转义）、无原型污染、密钥不硬编码
- [ ] 错误：边界输入验证、外部调用有超时和重试限制
- [ ] 日志：关键节点有日志、无敏感信息泄露
- [ ] 测试：新行为有测试、断言验证行为而非实现
- [ ] 注释：只保留 WHY，删除 WHAT、JSDoc 注释仅在公共 API
