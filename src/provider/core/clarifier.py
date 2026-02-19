import json

from core.llm_client import get_client
from core.prompts import (
    CLARIFICATION_PROMPT,
    CONTINUE_PROMPT,
    SUMMARIZE_PROMPT,
    SYSTEM_PROMPT,
)
from core.session_recorder import SessionRecorder, SessionRecord


class Clarifier:
    def __init__(self, recorder: SessionRecorder | None = None):
        self.client = get_client()
        self.recorder = recorder or SessionRecorder(session_id="default")

    def reflect(self, original: str) -> str:
        user_msg = CLARIFICATION_PROMPT.format(original=original)
        response = self.client.chat_once(SYSTEM_PROMPT + "\n\n" + user_msg, "")
        if self.recorder:
            self.recorder.record_api_call()
        return response

    def summarize(self, conversation: list[dict]) -> dict:
        system = SYSTEM_PROMPT + "\n\n" + SUMMARIZE_PROMPT
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

    def continue_dialogue(self, conversation: list[dict]) -> str:
        system = SYSTEM_PROMPT + "\n\n" + CONTINUE_PROMPT
        conversation_text = "\n".join(
            [
                f"{'用户' if msg['role'] == 'user' else '助手'}: {msg['content']}"
                for msg in conversation
            ]
        )
        response = self.client.chat_once(system, conversation_text)
        if self.recorder:
            self.recorder.record_api_call()
        return response

    def run(self, input_text: str) -> tuple[dict, str, SessionRecord]:
        conversation = [{"role": "user", "content": input_text}]

        if self.recorder:
            self.recorder.record_round()

        clarified = self.summarize(conversation)
        return clarified, input_text, self.recorder.end_session()
