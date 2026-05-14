# Capability: GREETER — 问候功能

## NEW Requirements

### Requirement: 基本问候

系统 SHALL 接受用户名参数，根据当前时间输出对应问候语。

#### Scenario: 早上时段问候

- **GIVEN** 当前时间在 06:00-11:59 之间
- **WHEN** 用户执行 `python src/greeter.py Alice`
- **THEN** 系统 SHALL 输出 "早上好, Alice!"

#### Scenario: 下午时段问候

- **GIVEN** 当前时间在 12:00-17:59 之间
- **WHEN** 用户执行 `python src/greeter.py Bob`
- **THEN** 系统 SHALL 输出 "下午好, Bob!"

#### Scenario: 深夜时段通用问候

- **GIVEN** 当前时间在 22:00-05:59 之间
- **WHEN** 用户执行 `python src/greeter.py Charlie`
- **THEN** 系统 SHALL 输出 "你好, Charlie!"

### Requirement: 正式问候模式

系统 SHALL 支持 `--formal` 选项切换到正式问候格式。

#### Scenario: 正式问候

- **GIVEN** 用户添加 `--formal` 选项
- **WHEN** 用户执行 `python src/greeter.py Alice --formal`
- **THEN** 系统 SHALL 输出 "尊敬的 Alice，早上好！"
