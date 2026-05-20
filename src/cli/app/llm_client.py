import os

from dotenv import load_dotenv
from quanttide_agent import LLM

load_dotenv()


def _make_messages(
    system: str, user: str, enable_thinking: bool = False
) -> list[dict]:
    messages = [{"role": "system", "content": system}]
    if user:
        messages.append({"role": "user", "content": user})
    return messages


def get_client() -> LLM:
    return LLM(
        model=os.getenv("LLM_MODEL", "qwen3.5-plus"),
        base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.getenv("LLM_API_KEY", ""),
    )


def chat_once(
    system: str,
    user: str = "",
    enable_thinking: bool = False,
    **kwargs,
) -> str:
    return get_client().chat(
        _make_messages(system, user, enable_thinking),
        **kwargs,
    ).content
