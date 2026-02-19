from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.sower import Sower
from app.agents.observer import Observer

router = APIRouter()


class ClarifyRequest(BaseModel):
    text: str


class ClarifyResponse(BaseModel):
    result: str
    metrics: dict | None = None


@router.post("/clarify", response_model=ClarifyResponse)
def clarify(request: ClarifyRequest, enable_observer: bool = False):
    """C - 澄清：判断输入是否清晰"""
    sower = Sower()
    result = sower.clarify(request.text)

    metrics = None
    if enable_observer:
        observer = Observer()
        conversation = [
            {"role": "user", "content": request.text},
            {"role": "assistant", "content": result},
        ]
        metrics = observer.evaluate(conversation)

    return ClarifyResponse(result=result, metrics=metrics)
