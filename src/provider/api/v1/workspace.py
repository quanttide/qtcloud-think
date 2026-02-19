from fastapi import APIRouter

from core.workspace import Workspace

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.get("")
def get_workspace(workspace: str = "default") -> dict:
    """获取工作空间信息"""
    ws = Workspace(workspace)

    return {
        "name": ws.name,
        "root": str(ws.root),
        "notes_dir": str(ws.get_notes_dir()),
        "received_dir": str(ws.get_received_dir()),
        "pending_dir": str(ws.get_pending_dir()),
        "rejected_dir": str(ws.get_rejected_dir()),
        "sessions_dir": str(ws.get_sessions_dir()),
    }
