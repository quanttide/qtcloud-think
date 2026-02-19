from app.infrastructure.llm_client import get_client


class ClarifySkill:
    """C - 澄清技能：判断输入是否清晰，通过对话补充关键信息"""

    def __init__(self):
        self.client = get_client()

    def execute(self, original: str) -> str:
        from app.infrastructure.prompts import CLARIFICATION_PROMPT, SYSTEM_PROMPT

        user_msg = CLARIFICATION_PROMPT.format(original=original)
        return self.client.chat_once(SYSTEM_PROMPT + "\n\n" + user_msg, "")
