import json
from typing import Literal
from llm_client import get_client

CLARITY_PROMPT = """你是一个思维澄清助手。你的任务是判断用户的输入是否足够清晰，可以被理解和处理。

判断标准（必须全部满足才算"清晰"）：
1. 有明确的主题或意图
2. 逻辑连贯，可以被理解
3. 有足够的信息量，不是碎片化的词语

请严格按以下 JSON 格式返回，不要返回其他内容：
{{
    "is_clear": true/false,
    "reason": "判断理由（简短）",
    "issues": ["问题1", "问题2"]  // 如果 is_clear 为 false，列出具体问题
}}"""

CLARIFICATION_PROMPT = """你是一个思维澄清助手。用户有一个想法需要表达，但目前还不够清晰。

用户的原始想法：{original}

发现的问题：{issues}

请通过对话帮助用户澄清想法。每次只问 1-2 个问题，引导用户补充关键信息。
问题要友好、自然，像朋友聊天一样。
不要给用户压力，而是帮助他们理清思路。

如果用户已经提供了足够的信息，可以结束对话并总结澄清后的内容。"""


class Clarifier:
    def __init__(self):
        self.client = get_client()

    def check_clarity(self, text: str) -> dict:
        user_msg = f"请判断以下内容是否清晰：\n\n{text}"
        response = self.client.chat_once(CLARITY_PROMPT, user_msg)

        try:
            result = json.loads(response.strip().strip("```json").strip("```"))
            return result
        except json.JSONDecodeError:
            return {
                "is_clear": False,
                "reason": "解析失败",
                "issues": ["无法判断清晰度"],
            }

    def ask_clarification(self, original: str, issues: list[str]) -> str:
        user_msg = CLARIFICATION_PROMPT.format(
            original=original, issues=", ".join(issues)
        )
        return self.client.chat_once("你是一个友好的思维对话助手。", user_msg)

    def summarize(self, conversation: list[dict]) -> str:
        system = """请根据对话内容，生成一段清晰、连贯的总结。

输出格式（Markdown）：
---
summary: 一句话概括核心观点
content: 澄清后的完整内容
---"""
        conversation_text = "\n".join(
            [
                f"{'用户' if msg['role'] == 'user' else '助手'}: {msg['content']}"
                for msg in conversation
            ]
        )
        return self.client.chat_once(system, conversation_text)
