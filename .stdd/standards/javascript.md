# JavaScript 开发规范

> 适用版本：Node.js 18+
> 最后更新：2026-07-01
> Initial version — validated on Python patterns, language-specific review needed

## 一、代码风格

### 1.1 格式化

- 使用 ESLint + Prettier 作为 linter 和 formatter
- 行宽：100 字符
- 缩进：2 空格（禁止 Tab）
- 分号：使用分号（`semi: always`）
- 引号：优先单引号（`'`），模板字符串使用反引号（`` ` ``）
- 文件末尾：一个空行

### 1.2 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | kebab-case | `message-service.js` |
| 类 | PascalCase | `MessageService` |
| 函数/方法 | camelCase | `processMessage()` |
| 变量 | camelCase | `userId` |
| 常量 | UPPER_SNAKE_CASE | `WELCOME_MSG` |
| 私有成员 | 前缀 `_` 或 `#`（私有字段） | `_filterMessage()` / `#cache` |

### 1.3 Import 顺序

1. Node.js 内置模块（`fs`, `path`, `http`）
2. 第三方包（`express`, `lodash`）
3. 本地模块（`./`, `../`）

每组之间空一行。优先使用 ES module（`import`/`export`），避免 `require()`。

## 二、类型系统

### 2.1 JSDoc 类型注解

- 公共函数必须使用 JSDoc 标注参数和返回值类型
- 推荐在 `tsconfig.json` 的 `checkJs: true` 下运行以获取类型检查

### 2.2 示例

```javascript
/**
 * 处理用户消息
 * @param {Object} message - 消息对象
 * @param {string} message.content - 消息内容
 * @param {number} userId - 用户ID
 * @param {string} [state] - 可选状态
 * @returns {Promise<string|null>} 处理结果
 */
async function processMessage(message, userId, state = null) {
    // ...
}
```

### 2.3 与 TypeScript 的关系

- 新项目优先使用 TypeScript（参考 `typescript.md`）
- 存量 JS 项目通过 JSDoc 渐进式提升类型安全
- 避免在 JS 文件中混用 `@ts-check` 和未注解函数

## 三、异步编程

### 3.1 规则

- IO 操作优先使用 `async/await`
- 避免回调嵌套（Callback Hell），使用 Promise 或 util.promisify
- 外部 HTTP 调用使用 `fetch`（Node.js 18+）或 `axios`
- 不要在 async 函数中使用同步阻塞操作（如 `fs.readFileSync`）
- 定时器使用 `setTimeout`/`setInterval`，清理时调用 `clearTimeout`/`clearInterval`

### 3.2 并发安全

- 共享可变状态使用 `Promise.all` 配合不可变数据模式
- EventEmitter 监听器数量超过 10 个时输出警告
- 使用 `AbortController` 取消可中止的异步操作

## 四、错误处理

### 4.1 规则

- 只在系统边界捕获异常（API 入口、消息处理入口）
- 内部函数让异常向上传播
- 捕获具体错误类型，禁止裸 `catch {}` 或 `catch (e) {}` 不处理
- async 函数错误统一通过 try-catch 或 `.catch()` 处理

### 4.2 用户可见错误

- 抛出业务异常时 message 应为用户友好信息
- 不在用户消息中暴露堆栈信息
- 自定义错误类继承 `Error`：

```javascript
class BusinessError extends Error {
    constructor(message, code) {
        super(message);
        this.name = 'BusinessError';
        this.code = code;
    }
}
```

## 五、日志

### 5.1 规则

- 使用结构化日志库（winston / pino）
- 关键业务节点记录 INFO 日志（用户行为、状态变更）
- 异常记录 ERROR 日志（含完整 stack trace）
- 不在循环中打印 DEBUG 日志

### 5.2 日志内容

- 必须包含足够的上下文信息（userId, requestId, 关键参数）
- 格式：`操作描述: key1=value1, key2=value2`
- 敏感信息（密码、token）不记录到日志

## 六、测试规范

### 6.1 测试框架

- 单元测试：Jest 或 Vitest
- HTTP 测试：Supertest（Express/Koa）
- Mock：Jest 内置 mock / Sinon

### 6.2 测试文件组织

- 单元测试：`__tests__/<module>.test.js` 或 `<module>.test.js`（co-located）
- 集成测试：`tests/integration/<feature>.test.js`

### 6.3 测试命名

```
describe('<模块名>', () => {
  it('should <预期行为> when <场景>', () => {
    // ...
  });
});
```

### 6.4 Mock 原则

- Mock 外部依赖（HTTP API、数据库、文件系统）
- 集成测试不 mock 数据库（使用测试数据库）
- 测试断言验证行为（WHAT），不验证实现细节（HOW）

## 七、代码审查检查清单

在 Phase 5 VERIFY 中，逐项检查：

- [ ] 死代码：无 `console.log`、注释掉的代码、未使用的 import
- [ ] 命名：名称匹配实际行为（不产生误导）
- [ ] 类型：公共函数有 JSDoc 类型注解
- [ ] 异步：IO 操作使用 async/await，事件监听有清理
- [ ] 安全：无 SQL 注入、无 XSS、token 不硬编码、依赖无已知 CVE
- [ ] 错误：边界输入验证、外部调用有超时、Promise rejection 有处理
- [ ] 日志：关键节点有日志、无敏感信息泄露
- [ ] 测试：新行为有测试、断言验证行为而非实现
- [ ] 注释：只保留 WHY，删除 WHAT
