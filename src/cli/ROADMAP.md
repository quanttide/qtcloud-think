# ROADMAP

## 已完成

- [x] 实现 `config.rs`，从环境变量读取 journal 路径
- [x] 实现 `repo.rs`，以 journal 结构（world → period → domain）为存储格式
- [x] 支持按 world、period、domain 查询（`worlds()`、`periods()`、`domains()`、`load()`）
- [x] 以 `quanttide-think`（Rust）和 `quanttide-agent`（Rust）为数据模型和基础设施
- [x] 实现 `analyze.rs`，追踪领域演化轨迹（`track_evolution()`）
- [x] 实现数据一致性描述（`describe()`）

### Phase 1: 意向查询（从实验代码迁移）

- [x] `Repo::intentions(world, period, domain)` - 查询指定 world/period/domain 的意向
- [x] `Repo::all_intentions(world, priority, risk, level)` - 多条件过滤查询所有意向
- [x] `Repo::intention_by_id(world, id)` - 按 UUID 查询意向详情
