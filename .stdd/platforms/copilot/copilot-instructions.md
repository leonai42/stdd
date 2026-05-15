# GitHub Copilot Instructions — STDD 开发规范

> 适配平台：GitHub Copilot
> STDD 版本：V2.2
> 安装：复制此文件到 `.github/copilot-instructions.md`

## 核心原则

You are assisting with development in a project that follows STDD (Spec+Test Driven Development), a 6-phase methodology.

### 1. 测试优先

- **Always write tests before implementation code.**
- Follow the RED→GREEN→REFACTOR cycle:
  - RED: Write a failing test first
  - GREEN: Write the minimal code to pass the test
  - REFACTOR: Clean up while keeping tests green
- Test naming: `test_<method>_<scenario>_<expected_result>`
- Each test function should reference a TC-ID from the test plan

### 2. 编码规范

Read the project's language standard file before generating code:
- Python: `.stdd/standards/python.md`
- Java: `.stdd/standards/java.md`
- Go: `.stdd/standards/go.md`
- Rust: `.stdd/standards/rust.md`
- TypeScript: `.stdd/standards/typescript.md`

Key conventions:
- Use the project's configured formatter and linter
- All public functions must have complete type annotations
- Only catch exceptions at system boundaries
- Log key business events with context
- No debug print statements in production code

### 3. 错误处理

- Only catch exceptions at system boundaries (API entry points, message handlers)
- Let exceptions propagate upward in internal code
- Catch specific exception types, never bare `except:` / `catch (Exception e)`
- User-facing error messages should be in the appropriate human language, never expose stack traces

### 4. Commit 规范

- Commits should describe WHY, not WHAT
- Format: `<type>: <brief description>`
- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

### 5. STDD 流程集成

When a user requests a new feature or change:
1. First, propose a `proposal.md` with Why / What Changes / Capabilities / Impact / Success Criteria
2. Wait for user confirmation before writing any spec or code
3. Design specs in GIVEN/WHEN/THEN format before implementing
4. Generate a test plan before writing implementation code

### 6. 代码审查检查

Before marking code as complete, verify:
- No dead code (print/debug statements, commented-out blocks, unused imports)
- Names match actual behavior
- Error handling at boundaries is correct
- Security: no SQL injection, no XSS, no hardcoded credentials
- Tests cover new behavior with meaningful assertions
- Comments only explain WHY, not WHAT

### References

- STDD methodology: see `.stdd/skills/` for full per-phase instructions
- Language standards: `.stdd/standards/<language>.md`
- Test plan template: `.stdd/templates/test-plan.md`
