import os

from dotenv import load_dotenv
from quanttide_agent import LLM

load_dotenv()


def get_client() -> LLM:
    return LLM(
        model=os.getenv("LLM_MODEL", "qwen3.5-plus"),
        base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.getenv("LLM_API_KEY", ""),
    )


def chat_once(system: str, user: str = "") -> str:
    messages = [{"role": "system", "content": system}]
    if user:
        messages.append({"role": "user", "content": user})
    return get_client().chat(messages).content
