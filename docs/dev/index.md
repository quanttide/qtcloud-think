# 开发计划：思维外脑 v0.0.x

## 核心概念：CODE 循环

系统围绕四个核心阶段构建：

| 阶段 | 含义 | 对应模块 |
|------|------|----------|
| C (Clarify) | 澄清：判断输入是否清晰，通过对话补充关键信息 | Clarifier |
| O (Organize) | 联想：寻找想法之间的关联 | 待实现 |
| D (Distill) | 精炼：压缩和遗忘原始想法，形成更精炼的思考 | 待实现 |
| E (Express) | 表达：输出可沉淀的知识 | Storage |

---

## 信息状态

AI 澄清后的输出需经过用户决策才能沉淀：

| 状态 | 含义 | 存储位置 |
|------|------|----------|
| 接收 | 认可澄清结果，存入长期记忆 | `notes/received/` |
| 拒绝 | 不认可，可选择填写原因 | `notes/rejected/` |
| 悬疑 | 暂时无法判断，暂存待定 | `notes/pending/` |

悬疑内容可通过命令召回重新决策。

---

### v0.0.3 - [开发中]

**目标**：增加用户反馈功能 + 信息状态分类

**功能**：AI 澄清后用户可选择接收/拒绝/悬疑，分类存储

---

#### 2.1 Storage 分类存储

修改 `storage.py`，支持按状态分类存储：

```
data/{workspace}/
├── notes/
│   ├── received/   # 接收的笔记
│   ├── pending/   # 悬疑待定
│   └── rejected/  # 拒绝的笔记
└── sessions/
```

- `save()` 方法增加 `status` 参数（received/pending/rejected）
- 新增 `list_pending()` 方法列出待定内容

#### 2.2 Clarifier 结构调整

- `summarize()` 方法返回结构化数据（dict），而非纯文本
- 结构：`{ summary: str, content: str, original: str }`

#### 2.3 Main.collect 用户决策

澄清后询问用户决策：

```
🤖 澄清结果：
[内容展示]

请选择：
1. 接收 - 存入长期记忆
2. 拒绝 - 丢弃（可填写原因）
3. 悬疑 - 暂存待定
```

#### 2.4 Pending 召回命令

新增命令：`pending` 或 `review`

- 列出 pending 目录中的内容
- 支持对每条内容重新决策（接收/拒绝/删除）

#### 2.5 Meta 模块（待定）

观察自己并提出改进建议，优先级取决于开发需求。

---

## 下一步

- [ ] Storage 分类存储
- [ ] Clarifier 返回结构化数据
- [ ] Main.collect 用户决策交互
- [ ] Pending 召回命令

---

## 运行测试

```bash
cd src/cli
uv run python -m pytest tests/
```

## 已知架构问题

### main 模块耦合风险

**问题 1**：main 与 session_recorder 职责耦合
- main 负责多轮问答引导并记录过程
- session_recorder 专门追踪交互轮次
- **状态**：目前合理，main 作为协调者调用 session_recorder

**问题 2**：main 与 storage 边界模糊
- main 提到"保存元数据"
- storage 负责文件持久化
- **状态**：需明确 main 仅调用 storage 而非自行处理

---

详见 [Meta 模块设计](./meta.md)

详见 [Collector 收集器设计](./collector.md)

详见 [信息状态设计](./status.md)
