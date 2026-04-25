# 用户使用指南

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

## 许可证

MIT License