# STDD Coding Conventions

> 适配平台：Aider AI
> STDD 版本：V2.2
> 安装：复制此文件到项目根目录，在 `.aider.conf.yml` 中引用

## Testing First (RED → GREEN → REFACTOR)

- Always write tests before implementation code.
- RED: Write a failing test first
- GREEN: Write the minimal code to pass
- REFACTOR: Clean up, keep tests green
- Never write code beyond what the tests cover.

## Naming Conventions

- Python: `snake_case` for functions/variables, `PascalCase` for classes
- Java: `camelCase` for methods/variables, `PascalCase` for classes
- Go: `camelCase` for private, `PascalCase` for public
- Rust: `snake_case` for functions/variables, `PascalCase` for types
- TypeScript: `camelCase` for functions/variables, `PascalCase` for classes/interfaces

## Type Annotations

- Python: All public functions must have complete type annotations (parameters + return)
- TypeScript: Strict mode (`strict: true`), no `any` unless unavoidable
- Java: No raw types, use generics, return `Optional<T>` instead of null
- Go: Use interfaces sparingly, define interfaces at the call site
- Rust: Derive common traits (`Debug`, `Clone`), use `enum` for error types

## Error Handling

- Only catch exceptions at system boundaries (API entry points, message handlers).
- Let errors propagate upward in internal code.
- Catch specific exception types, never bare catch-all patterns.
- User-facing error messages should not expose stack traces or internals.

## Logging

- Log key business events at INFO level with context (user_id, action, parameters).
- Log errors at ERROR level with full context.
- Never log in tight loops.
- Never log sensitive information (passwords, tokens, PII).

## Code Review Checklist

Before completing code, verify:

- [ ] No dead code: debug prints, commented-out code, unused imports
- [ ] Names match actual behavior (no misleading names)
- [ ] Types: complete annotations, no `any` abuse, no raw types
- [ ] Concurrency: correct lock usage, goroutine lifecycle, no data races
- [ ] Security: no injection (SQL/XSS), no hardcoded secrets
- [ ] Errors: boundary validation, timeouts on external calls
- [ ] Logs: key events logged, no sensitive data exposed
- [ ] Tests: new behavior covered, assertions test behavior not implementation
- [ ] Comments: only WHY, delete WHAT comments

## Language-Specific Standards

See `.stdd/standards/` for detailed per-language standards:
- `python.md` — Python (ruff, pytest, async/await, mypy)
- `java.md` — Java (Spotless, JUnit 5, Mockito, virtual threads)
- `go.md` — Go (gofmt, testing, goroutines, errgroup)
- `rust.md` — Rust (rustfmt, tokio, thiserror, cargo test)
- `typescript.md` — TypeScript (Prettier, Vitest, async/await, strict mode)
