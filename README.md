# 量潮思考云 (`qtcloud-think`)

思维外脑 - 思维收集与澄清工具

## 什么是思维外脑？

当人类处于默认神经网络状态时，帮助人类承载需要切换到任务正向网络的任务，使人类可以专注于放松。

核心功能：收集人类思维流，澄清想法念头，记录清晰的知识结构。

## 快速开始

```bash
# 克隆项目
git clone https://github.com/quanttide/qtcloud-think.git
cd qtcloud-think

# 运行 CLI
./scripts/collect
# 或
cd src/cli && uv run python main.py
```

## 功能

- **思维收集**：输入你的想法，AI 判断清晰度
- **多轮澄清**：模糊想法通过对话逐步澄清
- **结构化存储**：保存为 Markdown 格式

## 用法示例

```
你的想法是什么？> 我想学编程但是不知道从哪开始

正在分析想法清晰度...

💭 发现问题: 目标不够具体

🤖 你提到"想学编程"，能具体说说是想学习哪门编程语言吗？比如 Python、JavaScript？还是想解决某个具体问题？

请补充信息（输入 '完成' 结束澄清）> 完成

✅ 想法已澄清！
✅ 已保存到: data/cli/notes/xxx.md

摘要: 明确学习 Python 编程的目标，计划从基础语法入门
```

## 环境要求

- Python 3.11+
- macOS / Linux（Windows 推荐使用 WSL）

## 🤝 贡献

欢迎提交 Issue 或 PR！请先阅读 [贡献指南](CONTRIBUTING.md)。

## 许可证

MIT License
