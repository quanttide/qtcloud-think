from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.sower import Sower

router = APIRouter()


class OrganizeRequest(BaseModel):
    notes: list[dict]


class OrganizeResponse(BaseModel):
    result: str


@router.post("/organize", response_model=OrganizeResponse)
def organize(request: OrganizeRequest):
    """O - 联想：寻找想法之间的关联"""
    sower = Sower()
    result = sower.organize(request.notes)
    return OrganizeResponse(result=result)
