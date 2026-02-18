# 开发者文档

## 文件划分

| 文件 | 内容 |
|------|------|
| [index.md](./index.md) | 主开发文档：产品愿景、版本目标、核心流程、技术选型 |
| [meta.md](./meta.md) | Meta 模块设计（v0.0.2） |
| [collector.md](./collector.md) | Collector 收集器设计：为 meta 采集数据 |
| [workspace.md](./workspace.md) | Workspace 隔离设计：数据分部门/用途隔离 |

## 组织原则

- **index.md**: 存放长期稳定的内容，如产品愿景、技术选型、项目结构
- **功能模块设计**: 单独文件，如 meta.md，便于独立演进
- **版本规划**: 记录在 ROADMAP.md

## 新增模块文档

1. 在 `docs/dev/` 下创建 `{module}.md`
2. 在 `index.md` 末尾添加链接引用
3. 更新本 README 的文件划分表
