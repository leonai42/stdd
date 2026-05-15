# V2.3 任务清单

## 1. multi-lang-standards（P0）

- [x] 1.1 创建 `.stdd/standards/java.md`（6章节：代码风格/类型系统/并发模型/错误处理/测试规范/审查清单）
- [x] 1.2 创建 `.stdd/standards/go.md`（6章节：代码风格/类型系统/并发模型/错误处理/测试规范/审查清单）
- [x] 1.3 创建 `.stdd/standards/rust.md`（6章节：代码风格/类型系统/并发模型/错误处理/测试规范/审查清单）
- [x] 1.4 创建 `.stdd/standards/typescript.md`（6章节：代码风格/类型系统/异步模型/错误处理/测试规范/审查清单）

## 2. config-system（P0）

- [x] 2.1 修改 `.stdd/config.d/quality.yaml`：typecheck 从 null → `"mypy app/"`，critical_paths 从 [] → 含示例路径
- [x] 2.2 修改 `.stdd/config.d/project.yaml`：增加 `source_dir: "app"`
- [x] 2.3 修改 `.stdd/config.d/long_range.yaml`：增加 degradation 配置段（max_consecutive_failures / pass_rate_threshold / safety_check）

## 3. skill-architecture（P0）

- [x] 3.1 为 `.stdd/skills/understand.md` 添加 YAML frontmatter（name + description）
- [x] 3.2 为 `.stdd/skills/spec.md` 添加 YAML frontmatter
- [x] 3.3 为 `.stdd/skills/slice.md` 添加 YAML frontmatter
- [x] 3.4 为 `.stdd/skills/build.md` 添加 YAML frontmatter
- [x] 3.5 为 `.stdd/skills/verify.md` 添加 YAML frontmatter
- [x] 3.6 为 `.stdd/skills/deliver.md` 添加 YAML frontmatter

## 4. platform-sync — workbuddy（P0）

- [x] 4.1 同步 `.stdd/platforms/workbuddy/skills/stdd-understand.md`（保留 workbuddy frontmatter）
- [x] 4.2 同步 `.stdd/platforms/workbuddy/skills/stdd-spec.md`
- [x] 4.3 同步 `.stdd/platforms/workbuddy/skills/stdd-slice.md`
- [x] 4.4 同步 `.stdd/platforms/workbuddy/skills/stdd-build.md`
- [x] 4.5 同步 `.stdd/platforms/workbuddy/skills/stdd-verify.md`
- [x] 4.6 同步 `.stdd/platforms/workbuddy/skills/stdd-deliver.md`

## 5. platform-sync — trae（P0）

- [x] 5.1 同步 `.stdd/platforms/trae/skills/stdd-understand.md`（添加最小 frontmatter）
- [x] 5.2 同步 `.stdd/platforms/trae/skills/stdd-spec.md`
- [x] 5.3 同步 `.stdd/platforms/trae/skills/stdd-slice.md`
- [x] 5.4 同步 `.stdd/platforms/trae/skills/stdd-build.md`
- [x] 5.5 同步 `.stdd/platforms/trae/skills/stdd-verify.md`
- [x] 5.6 同步 `.stdd/platforms/trae/skills/stdd-deliver.md`

## 6. 新平台适配（P1）

- [x] 6.1 创建 `.stdd/platforms/cursor/rules/stdd.md`（STDD 6 阶段 + 3 Gate 规则文件）
- [x] 6.2 创建 `.stdd/platforms/copilot/copilot-instructions.md`（测试优先 + 规范引用）
- [x] 6.3 创建 `.stdd/platforms/aider/CONVENTIONS.md`（编码规范 + 测试规范）
- [x] 6.4 创建 `.stdd/platforms/aider/.aider.conf.yml`（引用 CONVENTIONS.md）

## 7. 一致性验证（P1）

- [x] 7.1 验证三平台（claude-code/workbuddy/trae）关键特征计数一致
- [x] 7.2 验证 `.stdd/skills/` 与 `claude-code/skills/` frontmatter name/description 一致
- [x] 7.3 验证 `.stdd/config.d/` 三个 YAML 文件语法正确
- [x] 7.4 验证四个语言规范文件章节结构一致
