import json
from datetime import datetime
from pathlib import Path
from typing import Any

from workspace import Workspace


class Storage:
    def __init__(self, workspace: Workspace | None = None):
        self.workspace = workspace or Workspace()
        self.notes_dir = self.workspace.get_notes_dir()
        self.sessions_dir = self.notes_dir.parent / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        original: str,
        clarified: str,
        summary: str,
        tags: list[str] | None = None,
        session_record: dict | None = None,
    ) -> Path:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H%M%S")

        # 保存笔记
        filename = f"thought_{date_str}_{time_str}.md"
        filepath = self.notes_dir / filename

        tags_str: str = ", ".join(tags) if tags else ""

        content = f"""---
created: {now.isoformat()}
status: clarified
summary: "{summary}"
tags: [{tags_str}]
original: "{original}"
---

# {summary}

{clarified}
"""
        filepath.write_text(content, encoding="utf-8")

        # 保存会话记录
        if session_record:
            session_filename = f"session_{date_str}_{time_str}.json"
            session_filepath = self.sessions_dir / session_filename
            session_filepath.write_text(
                json.dumps(session_record, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        return filepath

    def save_conversation(
        self,
        conversation: list[dict[str, Any]],
        summary: str,
        session_id: str,
    ) -> Path:
        """保存对话历史"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H%M%S")

        conversation_filename = f"conversation_{date_str}_{time_str}.json"
        conversation_filepath = self.sessions_dir / conversation_filename

        data = {
            "session_id": session_id,
            "created": now.isoformat(),
            "summary": summary,
            "conversation": conversation,
        }

        conversation_filepath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return conversation_filepath
