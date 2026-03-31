# CLI 设计文档

## 概述

量潮思考云 CLI 是一个基于 Python 的命令行工具，用于思维收集与澄清。当前版本为 v0.1.0，支持想法捕捉、澄清对话、状态管理和元认知分析等功能。

## 命令结构

### 主要命令

| 命令 | 功能 | 选项 |
|------|------|------|
| `collect` | 收集并澄清想法 | `-w, --workspace` 指定工作空间 |
| `pending` | 列出悬疑待定内容 | `-w, --workspace` 指定工作空间 |
| `review` | 对悬疑待定内容重新决策 | `-w, --workspace` 指定工作空间 |
| `meta` | 触发 Meta 自省分析 | `-w, --workspace` 指定工作空间 |
| `tui` | 启动 TUI 界面 | （待实现） |

### 使用示例

```bash
# 收集想法
qtcloud collect

# 指定工作空间
qtcloud collect -w my-workspace

# 查看待定内容
qtcloud pending

# 审查待定内容
qtcloud review

# Meta 分析
qtcloud meta
```

## 模块架构

### 核心模块

```
src/cli/app/
├── main.py           # CLI 入口和命令定义
├── clarifier.py      # 澄清器：负责想法澄清和对话
├── storage.py        # 存储：负责文件持久化
├── workspace.py      # 工作空间：管理目录结构
├── session_recorder.py  # 会话记录：追踪交互过程
├── llm_client.py     # LLM 客户端：与 AI 模型交互
├── api_client.py     # API 客户端：与 Provider 服务通信
├── meta.py           # Meta 模块：元认知分析
└── prompts.py        # 提示词：AI 对话提示词模板
```

### 模块职责

#### 1. main.py
- 定义 CLI 命令和参数
- 协调各模块完成用户请求
- 处理用户交互流程
- 管理离线/在线模式切换

#### 2. clarifier.py
- **Clarifier 类**：核心澄清逻辑
  - `reflect()`: 复述用户想法
  - `summarize()`: 生成总结
  - `continue_dialogue()`: 继续对话
  - `run()`: 完整澄清流程

#### 3. storage.py
- **Storage 类**：文件持久化
  - `save()`: 保存想法到文件系统
  - `save_conversation()`: 保存对话记录
  - `list_pending()`: 列出待定内容
  - `move_file()`: 移动文件状态
  - 支持 YAML frontmatter 元数据

#### 4. workspace.py
- 管理工作空间目录结构
- 提供不同状态的目录路径
  - `notes/received/`: 已接收
  - `notes/pending/`: 待定
  - `notes/rejected/`: 已拒绝
  - `sessions/`: 会话记录

#### 5. session_recorder.py
- 记录会话过程
- 追踪轮次和 API 调用
- 生成会话统计

#### 6. llm_client.py / api_client.py
- **离线模式**：使用本地 Clarifier
- **在线模式**：调用 Provider API
- 自动降级机制

## 数据流

### 想法收集流程

```
用户输入
    ↓
[read_multiline] 读取多行输入
    ↓
[Clarifier.reflect] AI 复述想法
    ↓
用户选择：补充/结束/换说法
    ↓
循环澄清对话
    ↓
[Clarifier.summarize] 生成总结
    ↓
用户决策：接收/拒绝/悬疑
    ↓
[Storage.save] 持久化存储
```

### 数据模型

#### 想法笔记 (Markdown + Frontmatter)
```markdown
---
id: uuid
created: 2026-03-31T12:00:00
status: received|pending|rejected
summary: 摘要
tags: [tag1, tag2]
original: 原始输入
rejection_reason: 拒绝原因（可选）
---

# 摘要

内容详情
```

#### 会话记录 (JSON)
```json
{
  "session_id": "uuid",
  "start_time": "2026-03-31T12:00:00",
  "end_time": "2026-03-31T12:05:00",
  "rounds": 3,
  "api_calls": 5,
  "user_abandoned": false,
  "storage_success": true
}
```

#### 对话记录 (JSON)
```json
{
  "session_id": "uuid",
  "created": "2026-03-31T12:00:00",
  "summary": "摘要",
  "conversation": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

## 技术栈

### 核心依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | >=3.11 | 运行环境 |
| typer | >=0.12.0 | CLI 框架 |
| openai | >=1.0.0 | LLM 交互 |
| httpx | >=0.28.0 | HTTP 客户端 |
| python-dotenv | >=1.0.0 | 环境变量管理 |

### 开发依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| black | >=24.0.0 | 代码格式化 |
| ruff | >=0.1.0 | 代码检查 |
| mypy | >=1.0.0 | 类型检查 |

### 可选依赖（TUI）

| 依赖 | 版本 | 用途 |
|------|------|------|
| textual | >=0.40.0 | TUI 框架 |
| rich | >=13.0.0 | 富文本渲染 |

## 工作空间结构

```
workspace/
├── notes/
│   ├── received/     # 已接收的想法
│   ├── pending/      # 待定的想法
│   └── rejected/     # 已拒绝的想法
├── sessions/
│   ├── session_*.json    # 会话记录
│   └── conversation_*.json  # 对话记录
└── meta/
    └── analysis_*.json   # Meta 分析报告
```

## 运行模式

### 在线模式
- 连接 Provider API
- 使用云端 AI 模型
- 需要网络连接

### 离线模式
- 使用本地 Clarifier
- 基于规则的澄清逻辑
- 无需网络连接
- 设置环境变量：`OFFLINE_MODE=true`

## 环境配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OFFLINE_MODE` | 启用离线模式 | `false` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | - |
| `OPENAI_BASE_URL` | OpenAI API 基础 URL | - |
| `PROVIDER_URL` | Provider 服务地址 | - |

### .env 文件示例
```env
OFFLINE_MODE=false
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
```

## 当前实现状态

### 已实现功能
- ✅ 想法收集和澄清对话
- ✅ 多轮对话支持
- ✅ 状态管理（接收/拒绝/悬疑）
- ✅ 文件持久化
- ✅ 会话记录
- ✅ Meta 自省分析
- ✅ 离线/在线模式切换
- ✅ 工作空间管理

### 待实现功能
- 🔄 TUI 界面（设计中）
- 🔄 Organizer 联想功能
- 🔄 Distiller 精炼功能
- 🔄 Exporter 导出功能
- 🔄 想法关联可视化
- 🔄 搜索和过滤
- 🔄 多工作空间切换

## 测试

### 运行测试
```bash
cd src/cli
uv run python -m pytest tests/
```

### 测试结构
```
tests/
├── test_clarifier.py
├── test_storage.py
├── test_workspace.py
└── test_integration.py
```

## 已知问题

### 架构问题
1. **main 与 session_recorder 耦合**
   - main 负责多轮问答引导并记录过程
   - 状态：目前合理，main 作为协调者调用 session_recorder

2. **main 与 storage 边界模糊**
   - main 提到"保存元数据"
   - 状态：需明确 main 仅调用 storage 而非自行处理

### 待优化
- Clarifier 提示词优化
- 错误处理增强
- 性能优化（大量数据场景）
- 用户体验改进

## 后续规划

### v0.0.4 目标
- 封装 Organizer（联想）功能
- 分析已接收想法的关联
- 展示想法关联图谱

### v0.0.5 目标
- 实现 Distiller（精炼）功能
- 想法压缩和遗忘机制
- 知识沉淀优化

### 长期目标
- 完整的 CODE 技能体系
- 多模态支持（语音、图像）
- 跨平台同步
- 社区生态建设

---

**文档版本**：v1.0  
**创建日期**：2026-03-31  
**最后更新**：2026-03-31  
**维护者**：量潮团队