# Capability: multi-lang-standards

## NEW Requirements

### Requirement: Java 开发规范

系统 SHALL 提供 Java 语言开发规范文件，覆盖代码风格、命名约定、类型系统、并发模型、错误处理、测试规范、审查清单 6 个维度，参考 Python 规范的结构模板。

#### Scenario: Java 规范文件存在且结构完整

- **GIVEN** `.stdd/standards/` 目录存在
- **WHEN** Phase 4 Step 0 读取 `project.language == "java"` 的开发规范
- **THEN** 系统 SHALL 读取 `.stdd/standards/java.md` 文件
- **AND** 该文件 SHALL 包含：代码风格（格式化/命名/Import）、类型系统（泛型/注解/空安全）、并发模型（虚拟线程/CompletableFuture）、错误处理（受检异常/非受检异常）、测试规范（JUnit5/Mockito/ParametrizedTest）、审查清单 共 6 个章节

#### Scenario: Java 规范与 Python 规范结构一致

- **GIVEN** `.stdd/standards/python.md` 存在且包含 7 个章节
- **WHEN** 对比 Java 规范和 Python 规范的章节结构
- **THEN** Java 规范 SHALL 与 Python 规范共享相同的顶级章节结构（代码风格/类型系统/异步或并发/错误处理/日志/测试/审查清单）
- **AND** 各章节的具体内容 SHALL 根据 Java 语言特性定制

---

### Requirement: Go 开发规范

系统 SHALL 提供 Go 语言开发规范文件，覆盖代码风格、命名约定、类型系统、并发模型、错误处理、测试规范、审查清单 6 个维度。

#### Scenario: Go 规范文件存在且结构完整

- **GIVEN** `.stdd/standards/` 目录存在
- **WHEN** Phase 4 Step 0 读取 `project.language == "go"` 的开发规范
- **THEN** 系统 SHALL 读取 `.stdd/standards/go.md` 文件
- **AND** 该文件 SHALL 包含：代码风格（gofmt/goimports/命名）、类型系统（接口/结构体/泛型）、并发模型（goroutine/channel/select/errgroup）、错误处理（error wrapping/sentinel errors）、测试规范（testing包/表驱动测试/mock）、审查清单 共 6 个章节

---

### Requirement: Rust 开发规范

系统 SHALL 提供 Rust 语言开发规范文件，覆盖代码风格、命名约定、类型系统、并发模型、错误处理、测试规范、审查清单 6 个维度。

#### Scenario: Rust 规范文件存在且结构完整

- **GIVEN** `.stdd/standards/` 目录存在
- **WHEN** Phase 4 Step 0 读取 `project.language == "rust"` 的开发规范
- **THEN** 系统 SHALL 读取 `.stdd/standards/rust.md` 文件
- **AND** 该文件 SHALL 包含：代码风格（rustfmt/clippy/命名）、类型系统（枚举/match/泛型/trait）、并发模型（tokio/async/Arc-Mutex/channel）、错误处理（Result/Option/anyhow/thiserror）、测试规范（#[test]/proptest/mock）、审查清单 共 6 个章节

---

### Requirement: TypeScript 开发规范

系统 SHALL 提供 TypeScript 语言开发规范文件，覆盖代码风格、命名约定、类型系统、异步模型、错误处理、测试规范、审查清单 6 个维度。

#### Scenario: TypeScript 规范文件存在且结构完整

- **GIVEN** `.stdd/standards/` 目录存在
- **WHEN** Phase 4 Step 0 读取 `project.language == "typescript"` 的开发规范
- **THEN** 系统 SHALL 读取 `.stdd/standards/typescript.md` 文件
- **AND** 该文件 SHALL 包含：代码风格（prettier/eslint/命名）、类型系统（interface/type/泛型/类型守卫）、异步模型（Promise/async-await/AbortController）、错误处理（Result类型/Error子类/边界捕获）、测试规范（Vitest/Jest/Testing Library/mock）、审查清单 共 6 个章节

---

### Requirement: 跨语言规范一致性

所有语言规范文件 SHALL 遵循统一的 6 维度模板，确保 STDD skill 在切换语言时无需改变检查逻辑。

#### Scenario: 四种规范共享相同的章节结构模板

- **GIVEN** `.stdd/standards/` 下存在 python.md / java.md / go.md / rust.md / typescript.md
- **WHEN** AI 读取任意语言规范用于 Phase 4 Step 0 或 Phase 5 Step 2
- **THEN** 每个规范文件 SHALL 包含：代码风格、类型系统、异步或并发、错误处理、日志、测试规范、审查清单 共 7 个顶级章节
- **AND** 各章节的二级标题（命名约定/格式化/测试命名/Fixtures等）SHALL 与 python.md 保持对应关系
