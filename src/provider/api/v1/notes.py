from typing import Any
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException

from core.storage import Storage
from core.workspace import Workspace

router = APIRouter(prefix="/notes", tags=["notes"])


class NoteCreate(BaseModel):
    original: str
    content: str
    summary: str
    status: str = "received"
    tags: list[str] | None = None
    session_record: dict | None = None
    rejection_reason: str | None = None
    session_id: str | None = None


class NoteUpdateStatus(BaseModel):
    status: str
    rejection_reason: str | None = None


@router.get("")
def list_notes(workspace: str = "default") -> dict[str, list[dict[str, Any]]]:
    """列出所有笔记"""
    ws = Workspace(workspace)
    storage = Storage(ws)

    notes = []
    for status_dir in [
        ws.get_received_dir(),
        ws.get_pending_dir(),
        ws.get_rejected_dir(),
    ]:
        for filepath in status_dir.glob("*.md"):
            content = filepath.read_text(encoding="utf-8")
            frontmatter, _ = storage._parse_frontmatter(content)
            notes.append(
                {
                    "id": frontmatter.get("id", filepath.stem),
                    "summary": frontmatter.get("summary", ""),
                    "status": frontmatter.get("status", ""),
                    "created": frontmatter.get("created", ""),
                    "filepath": str(filepath),
                }
            )

    return {"notes": notes}


@router.post("")
def create_note(note: NoteCreate, workspace: str = "default") -> dict:
    """保存笔记"""
    ws = Workspace(workspace)
    storage = Storage(ws)

    filepath = storage.save(
        original=note.original,
        clarified=note.content,
        summary=note.summary,
        tags=note.tags,
        session_record=note.session_record,
        status=note.status,
        rejection_reason=note.rejection_reason,
    )

    if note.session_id:
        conversation = []
        storage.save_conversation(conversation, note.summary, note.session_id)

    return {
        "id": filepath.stem,
        "filepath": str(filepath),
    }


@router.get("/pending")
def list_pending(workspace: str = "default") -> dict[str, list[dict[str, Any]]]:
    """列出待定笔记"""
    ws = Workspace(workspace)
    storage = Storage(ws)

    pending_notes = storage.list_pending()
    return {"notes": pending_notes}


@router.put("/{note_id}/status")
def update_note_status(
    note_id: str,
    update: NoteUpdateStatus,
    workspace: str = "default",
) -> dict:
    """更新笔记状态"""
    ws = Workspace(workspace)
    storage = Storage(ws)

    pending_dir = ws.get_pending_dir()
    received_dir = ws.get_received_dir()
    rejected_dir = ws.get_rejected_dir()

    source_dir = None
    if (pending_dir / f"{note_id}.md").exists():
        source_dir = pending_dir
    elif (received_dir / f"{note_id}.md").exists():
        source_dir = received_dir
    elif (rejected_dir / f"{note_id}.md").exists():
        source_dir = rejected_dir
    else:
        raise HTTPException(status_code=404, detail="笔记不存在")

    storage.move_file(
        note_id,
        source_dir,
        update.status,
        update.rejection_reason,
    )

    return {"success": True}
