from fastapi import APIRouter

from core.clarifier import Clarifier
from core.session_recorder import SessionRecorder

router = APIRouter(prefix="/clarify", tags=["clarify"])


@router.post("/reflect")
def reflect(original: str) -> dict:
    """首轮反思：复述用户想法"""
    recorder = SessionRecorder(session_id="reflect")
    clarifier = Clarifier(recorder)
    reflection = clarifier.reflect(original)
    return {"reflection": reflection}


@router.post("/summarize")
def summarize(conversation: list[dict]) -> dict:
    """生成总结"""
    recorder = SessionRecorder(session_id="summarize")
    clarifier = Clarifier(recorder)
    result = clarifier.summarize(conversation)
    return result


@router.post("/continue")
def continue_dialogue(conversation: list[dict]) -> dict:
    """继续对话"""
    recorder = SessionRecorder(session_id="continue")
    clarifier = Clarifier(recorder)
    response = clarifier.continue_dialogue(conversation)
    return {"response": response}
