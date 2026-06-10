# ROADMAP

## 阶段一：存储层（Storage）

- [ ] 实现 `storage.rs`，以 journal 结构（world → period → domain）为存储格式
- [ ] 支持按 world、period、domain 查询
- [ ] 以 `quanttide-think`（Rust）和 `quanttide-agent`（Rust）为数据模型和基础设施

目标：替换 project-11 的手动 YAML 加载，统一数据入口。

## 阶段二：CLI 重写

- [ ] 基于 storage 层重建 CLI 命令：显示/查询/分析/探索
- [ ] 自然语言交互（复用 project-11 验证过的意图分类器模式）
- [ ] LLM 集成（复用 quanttide-agent）

目标：project-11 退役，功能整合到 qtcloud-think CLI。

## 阶段三：协作

- [ ] world 概念落地：多 world 数据隔离与共享
- [ ] 团队协作场景验证

目标：从单人工具进化到团队认知平台。

## 里程碑

- `v0.1.0`：storage.rs + 基础查询，journal v0.1.0 兼容
- `v0.2.0`：CLI 重写完成，project-11 可退役
- `v0.3.0`：多 world 支持，协作验证
