import json
from llm_client import get_client
from session_recorder import SessionRecorder, SessionRecord

SYSTEM_PROMPT = """你是"思维外脑"——一个思维收集与澄清助手。

## 你的身份
- 你是一个 AI 助手，帮助用户理清思路、沉淀思考
- 你的目标是帮助用户把碎片化的想法转化为结构化的知识

## 你的能力
- 判断用户输入是否清晰完整
- 通过对话引导用户补充关键信息
- 将澄清后的想法总结成结构化内容

## 你的原则
- 保持友好、自然的对话风格
- 不给用户压力，像朋友聊天一样帮助他们
- 每次只问 1-2 个关键问题
- 用户不想说时不要追问"""

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
    def __init__(self, recorder: SessionRecorder | None = None):
        self.client = get_client()
        self.recorder = recorder or SessionRecorder(session_id="default")

    def check_clarity(self, text: str) -> dict:
        user_msg = f"请判断以下内容是否清晰：\n\n{text}"
        response = self.client.chat_once(
            SYSTEM_PROMPT + "\n\n" + CLARITY_PROMPT, user_msg
        )
        if self.recorder:
            self.recorder.record_api_call()

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
        response = self.client.chat_once(SYSTEM_PROMPT + "\n\n" + user_msg, "")
        if self.recorder:
            self.recorder.record_api_call()
        return response

    def summarize(self, conversation: list[dict]) -> dict:
        system = (
            SYSTEM_PROMPT
            + """

请根据对话内容，生成一段清晰、连贯的总结。

输出格式（JSON），content 必须是纯文本，不能包含 JSON 或代码块：
{
    "summary": "一句话概括核心观点",
    "content": "澄清后的完整内容（纯文本，不要包含任何 JSON 或 ``` 符号）"
}"""
        )
        conversation_text = "\n".join(
            [
                f"{'用户' if msg['role'] == 'user' else '助手'}: {msg['content']}"
                for msg in conversation
            ]
        )
        response = self.client.chat_once(system, conversation_text)
        if self.recorder:
            self.recorder.record_api_call()

        try:
            result = json.loads(response.strip().strip("```json").strip("```"))
            return result
        except json.JSONDecodeError:
            return {
                "summary": "总结失败",
                "content": response,
            }

    def run(self, input_text: str) -> tuple[dict, str, SessionRecord]:
        conversation = [{"role": "user", "content": input_text}]
        result = self.check_clarity(input_text)

        if self.recorder:
            self.recorder.record_round()
            self.recorder.record_intent_captured(result.get("is_clear", False))

        while not result.get("is_clear", False):
            issues = result.get("issues", ["内容不够清晰"])
            response = self.ask_clarification(input_text, issues)
            conversation.append({"role": "assistant", "content": response})
            conversation.append({"role": "user", "content": "[用户补充中]"})

            if self.recorder:
                self.recorder.record_round()
                self.recorder.record_intent_captured(True)

            result = self.check_clarity(input_text)

        clarified = self.summarize(conversation)
        return clarified, input_text, self.recorder.end_session()
