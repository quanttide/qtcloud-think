from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.sower import Sower

router = APIRouter()


class DistillRequest(BaseModel):
    content: str


class DistillResponse(BaseModel):
    result: str


@router.post("/distill", response_model=DistillResponse)
def distill(request: DistillRequest):
    """D - 精炼：压缩和遗忘原始想法"""
    sower = Sower()
    result = sower.distill(request.content)
    return DistillResponse(result=result)
