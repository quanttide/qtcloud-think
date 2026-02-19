# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2026-02-19

### Added
- 信息状态分类：AI 澄清后用户可选择接收/拒绝/悬疑，分类存储到不同目录
- 换一个说法：用户可要求 AI 重新思考和表达
- 继续对话：澄清后用户可继续补充信息
- AI 智能追问：AI 根据内容判断是否需要追问，碰撞而非盘问
- 多行输入支持：支持编辑器模式输入长文本
- 总结修改：澄清后支持修改摘要和内容

### Changed
- 提示词改为服务创造性认知，AI 作为思考催化剂
- AI 只复述并问一个问题，不再持续追问，用户自行决定是否补充

---

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
