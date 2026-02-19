from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.meta import Meta

router = APIRouter()


class MetaRequest(BaseModel):
    context: dict


class MetaResponse(BaseModel):
    result: str


@router.post("/meta", response_model=MetaResponse)
def meta(request: MetaRequest):
    """Meta - 元认知反思"""
    agent = Meta()
    result = agent.run(request.context)
    return MetaResponse(result=result)
