# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2026-02-18

### Added
- Meta 模块：系统自省分析，观察思考云自身并提出改进建议
- Workspace 隔离：支持 default 和 meta 工作空间
- Session 记录：保存会话过程数据（轮次、耗时、API 调用）
- Conversation 保存：保存对话历史用于语义分析
- 系统提示词：AI 知道自己的身份和能力
- 模块检查器：使用 LLM 分析模块职责和依赖

### Changed
- Meta 改为手动触发（`collect meta` 命令）
- 重构 CLI 目录结构为 app/ + tests/

### Fixed
- scripts/collect 路由问题

---

## [0.0.1] - 2026-02-18

### Added
- CLI 思维收集与澄清工具原型
- `scripts/collect` 脚本支持从项目根目录运行 CLI
- `data/` 动态数据目录约定
- 开发指南文档 (AGENTS.md)
