## Step 0: 版本自检（V2.9.5+）

> 在继续执行之前，检查项目 STDD 静态资源版本是否与当前技能版本一致。
> 此步骤不阻断执行，仅在版本落后时告警。

1. 尝试读取 `.stdd/version.yaml`
2. 如果文件不存在 → 说明不是 STDD 项目，**静默跳过**，不显示任何版本相关消息
3. 如果文件存在：
   a. 提取 `stdd_version` 字段（记为 `project_version`）
   b. 提取 `locked` 字段（若为 `true`，项目已锁定版本）
   c. 从当前技能文件的 YAML frontmatter 中提取 `stdd_version`（记为 `skill_version`）
4. 比较 `project_version` 与 `skill_version`：
   - 去除 `v`/`V` 前缀
   - 按 `.` 分割为数字段
   - 短版本号末尾补 `0`（如 `2.9` → `2.9.0`）
   - 逐段比较整数大小
5. 判定结果：
   - 若 `project_version < skill_version` 且 `locked: true`：
     → 显示告警：`⚠️ [STDD 版本漂移] 项目 .stdd/ 版本为 {project_version}，但当前技能版本为 {skill_version}。项目已锁定，使用 stdd upgrade --unlock 解锁后再升级。`
   - 若 `project_version < skill_version` 且未锁定：
     → 显示告警：`⚠️ [STDD 版本漂移] 项目 .stdd/ 版本为 {project_version}，当前技能版本为 {skill_version}。建议运行 /stdd-upgrade 同步项目快照。`
   - 若 `project_version >= skill_version`：静默继续
6. **无论何种情况，均不阻断后续步骤的执行。**
