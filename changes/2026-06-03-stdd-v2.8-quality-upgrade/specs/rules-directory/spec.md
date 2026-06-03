# Spec: Rules 目录结构

## ADDED Requirements

### Requirement: .stdd/rules/ 目录

#### Scenario: 初始化 rules 目录
- **GIVEN** STDD V2.8 已安装
- **WHEN** 执行 `stdd init --with-rules` 或手动创建
- **THEN** `.stdd/rules/common/` SHALL 包含 TDD 规范、安全基线、Git 工作流规则
- **AND** `.stdd/rules/<lang>/` SHALL 按语言创建子目录

#### Scenario: Phase 4 自动加载
- **GIVEN** `.stdd/rules/common/tdd.md` 和 `.stdd/rules/python/patterns.md` 存在
- **WHEN** Phase 4 BUILD 开始，project.language=python
- **THEN** AI SHALL 自动读取 common/ + python/ 下所有 .md 文件
- **AND** 注入到编码上下文
