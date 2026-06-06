# 数据契约校验 (Schema Verify) — 设计方案

## 问题

`.stdd.yaml` 被 20+ 个读写端共享，字段名不一致（如 `current_phase` vs `phase`）会导致静默 bug。当前无自动检测机制。

## 方案

### Canonical 字段定义

定义 `.stdd.yaml` 的 canonical schema 文件 `stdd/schema/stdd_yaml_schema.yaml`：

```yaml
fields:
  change_id:        {type: str, required: true,  writers: [new], readers: [all]}
  status:           {type: str, required: true,  writers: [new,archive,abort,rollback], readers: [guard,validate,status]}
  current_phase:    {type: str, required: true,  writers: [new,state,phase], readers: [guard,status,state]}
  task_type:        {type: str, required: false, writers: [new,user], readers: [guard,spec]}
  mode:             {type: str, required: false, writers: [new,gate], readers: [build,verify]}
  complexity_score: {type: int, required: false, writers: [understand], readers: [spec]}
  ...
```

### stdd schema verify 命令

```bash
stdd schema verify                # 校验当前项目的 .stdd.yaml
stdd schema verify --all          # 校验所有 changes/ 和 archive/
stdd schema verify --writers      # 检查写入端是否使用了 canonical 字段名
```

### 校验逻辑

1. **字段名检查**：搜索所有 `data.get("...")` 和 `data["..."]` 调用，比对 canonical 字段名
2. **类型检查**：读取实际 .stdd.yaml 的值类型，比对 schema
3. **必填检查**：required 字段是否存在

## 实现计划

- 新增 `stdd/cli/commands/schema.py`
- 新增 `stdd/schema/stdd_yaml_schema.yaml`
- 注册 `stdd schema verify` 命令
- 在 CI (`stdd ci check-failures`) 中集成 schema verify

## 状态

V2.9.4 设计方案，待 V2.9.5+ 实现。
