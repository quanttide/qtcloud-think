# Collector 模块设计

## 定位

Collector（收集器）是思维收集与澄清组件，负责接收用户的想法碎片，通过对话帮助用户理清思路，生成结构化输出。

---

## 核心流程

```
用户输入 → [Collector 判断清晰度] → [不清晰] 追问 → ... → [清晰] 总结 → 存储
```

Collector 在整个思考过程中运行，循环收集和澄清想法碎片。

---

## 模块接口

基于现有 `clarifier.py` 实现：

```python
class Collector:
    def __init__(self):
        self.client = get_client()

    def run(self, input_text: str) -> tuple[Note, SessionRecord]:
        """执行完整收集流程
        返回: (生成的笔记, 会话记录)
        """

    def check_clarity(self, text: str) -> dict:
        """判断输入是否清晰
        返回: {"is_clear": bool, "reason": str, "issues": list[str]}
        """

    def ask_clarification(self, original: str, issues: list[str]) -> str:
        """追问用户，收集更多信息"""

    def summarize(self, conversation: list[dict]) -> str:
        """总结对话，生成结构化内容"""
```

---

## 对话流程

1. 用户输入想法碎片
2. `check_clarity` 判断是否清晰
3. 如不清晰，`ask_clarification` 追问
4. 循环直到清晰
5. `summarize` 生成总结
6. 存储为 Markdown

---

## 数据收集

Collector 的 `run()` 方法返回 `SessionRecord`，供 Meta 模块使用。

需要收集的数据维度：

| 数据维度 | 具体指标 |
|---------|---------|
| 对话效率 | 轮次、耗时 |
| 意图理解 | 首轮是否抓住核心 |
| 澄清结果 | 是否成功存储 |
| 用户反馈 | 满意度/放弃 |
| 成本 | API 调用次数 |
| 错误 | 异常类型/频率 |

详见 [Meta 模块设计](./meta.md)
