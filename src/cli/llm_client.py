import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
        )
        self.model = os.getenv("LLM_MODEL", "qwen3.5-plus")

    def chat(
        self, messages: list[dict], enable_thinking: bool = False, **kwargs
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            extra_body={"enable_thinking": enable_thinking},
            **kwargs,
        )
        return response.choices[0].message.content

    def chat_once(
        self, system: str, user: str, enable_thinking: bool = False, **kwargs
    ) -> str:
        return self.chat(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            enable_thinking=enable_thinking,
            **kwargs,
        )


def get_client() -> LLMClient:
    return LLMClient()
