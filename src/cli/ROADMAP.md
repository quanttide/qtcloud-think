# ROADMAP

## 已完成

- [x] 实现 `config.rs`，从环境变量读取 journal 路径
- [x] 实现 `repo.rs`，以 journal 结构（world → period → domain）为存储格式
- [x] 支持按 world、period、domain 查询（`worlds()`、`periods()`、`domains()`、`load()`）
- [x] 以 `quanttide-think`（Rust）和 `quanttide-agent`（Rust）为数据模型和基础设施
- [x] 实现 `analyze.rs`，追踪领域演化轨迹（`track_evolution()`）
- [x] 实现数据一致性描述（`describe()`）

## 待实现

### Phase 1: 意向查询（从实验代码迁移）

- [ ] `Repo::intentions(world, period, domain)` - 查询指定 world/period/domain 的意向
- [ ] `Repo::all_intentions(world, priority, risk, level)` - 多条件过滤查询所有意向
- [ ] `Repo::intention_by_id(world, id)` - 按 UUID 查询意向详情

### Phase 2: 分析功能扩展

- [ ] `analyze::diff(repo, world, period_a, period_b)` - 跨周差异分析
- [ ] `analyze::drift(repo, world, domain, period_a, period_b)` - 优先级/风险漂移检测
- [ ] `analyze::evolution_table(repo, world, domain)` - 意图演化矩阵

### Phase 3: LLM 集成

- [ ] `report::relate_llm(repo, world, period)` - LLM 推理情境间关系
- [ ] `report::generate_weekly(repo, world, period)` - 生成结构化周报

### Phase 4: CLI 二进制

- [ ] 创建 `bin/main.rs`，实现命令行参数解析
- [ ] 支持子命令：`weeks`、`show`、`landscape`、`explore`、`report`、`diff`、`relate`
- [ ] 支持意向子命令：`intentions`、`filter`、`trace`、`drift`、`evolve`

## 数据模型扩展

### 待添加类型

```rust
// model.rs

/// 意向查询结果
pub struct IntentionQueryResult {
    pub world: String,
    pub period: String,
    pub domain: String,
    pub intention: Intention,
}

/// 跨周差异
pub struct PeriodDiff {
    pub period_a: String,
    pub period_b: String,
    pub added: Vec<String>,
    pub removed: Vec<String>,
    pub modified: Vec<String>,
}

/// 优先级/风险漂移
pub struct IntentionDrift {
    pub intention_id: String,
    pub title: String,
    pub period_a: String,
    pub period_b: String,
    pub priority_change: Option<String>,
    pub risk_change: Option<String>,
}
```

## 优先级

1. **Phase 1** - 意向查询（核心功能，从实验代码迁移）
2. **Phase 2** - 分析功能扩展（增强分析能力）
3. **Phase 3** - LLM 集成（高级功能）
4. **Phase 4** - CLI 二进制（用户界面）
