import os

from dotenv import load_dotenv
from quanttide_agent import LLM

load_dotenv()


def get_client() -> LLM:
    return LLM(
        model=os.getenv("LLM_MODEL", "deepseek-v4-flash"),
        base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com"),
        api_key=os.getenv("LLM_API_KEY", ""),
    )
