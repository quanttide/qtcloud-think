# 开发计划：思维外脑 v0.0.x

## 核心概念：CODE 循环

系统围绕四个核心阶段构建：

| 阶段 | 含义 | 对应模块 |
|------|------|----------|
| C (Clarify) | 澄清：判断输入是否清晰，通过对话补充关键信息 | Clarifier ✅ |
| O (Organize) | 联想：寻找想法之间的关联 | Organizer (v0.0.4) |
| D (Distill) | 精炼：压缩和遗忘原始想法，形成更精炼的思考 | Distiller (v0.0.5) |
| E (Express) | 表达：输出可沉淀的知识 | Storage ✅ |

---

## 信息状态

AI 澄清后的输出需经过用户决策才能沉淀：

| 状态 | 含义 | 存储位置 |
|------|------|----------|
| 接收 | 认可澄清结果，存入长期记忆 | `notes/received/` ✅ |
| 拒绝 | 不认可，可选择填写原因 | `notes/rejected/` ✅ |
| 悬疑 | 暂时无法判断，暂存待定 | `notes/pending/` ✅ |

悬疑内容可通过命令召回重新决策。

---

## 模块架构

| 模块 | 技术 | 职责 |
|------|------|------|
| CLI | Python | 命令行交互界面 |
| Studio | Flutter | 移动端应用 |
| Provider | FastAPI | API 服务，为 CLI 和 Studio 提供后端 |

---

### v0.0.4 - [待开发]

**目标**：封装 Organizer（联想）

**功能**：
- 分析已接收的想法，寻找其中的联系
- 展示想法之间的关联（可视图或列表）
- 支持 meta 反思（观察联想过程并提出改进）

**设计**：见 docs/dev/organizer.md

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

详见 [参考借鉴](./reference.md)

详见 [CLI 重构计划](./refactor-cli-to-provider.md)
