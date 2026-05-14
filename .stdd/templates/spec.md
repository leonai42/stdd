# Capability: <能力名称>

## <ADDED|MODIFIED> Requirements

### Requirement: <需求名称>

<一句话描述：系统 SHALL 做什么>

#### Scenario: <场景名称>

- **GIVEN** <前置条件>
- **WHEN** <触发动作>
- **THEN** 系统 SHALL <预期结果>
- **AND** <附加条件或结果>

<!--
AND 用法说明：
- 一个 Scenario 至少包含 GIVEN/WHEN/THEN 各 1 条
- 可通过 AND 扩展多条件，最多 5 条 AND
- 示例（多 AND）：
  #### Scenario: 用户登录成功跳转到首页
  - **GIVEN** 用户已注册且账号状态正常
  - **AND** 用户当前未登录
  - **WHEN** 用户输入正确的用户名和密码并点击登录
  - **THEN** 系统 SHALL 跳转到首页
  - **AND** 系统 SHALL 显示欢迎消息
  - **AND** 系统 SHALL 设置 session cookie
-->
