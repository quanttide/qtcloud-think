import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from core.workspace import Workspace


class Storage:
    def __init__(self, workspace: Workspace | None = None):
        self.workspace = workspace or Workspace()
        self.notes_dir = self.workspace.get_notes_dir()
        self.sessions_dir = self.workspace.get_sessions_dir()

    def save(
        self,
        original: str,
        clarified: str,
        summary: str,
        tags: list[str] | None = None,
        session_record: dict | None = None,
        status: str = "received",
        rejection_reason: str | None = None,
    ) -> Path:
        note_id = str(uuid.uuid4())
        now = datetime.now()
        tags_str = ", ".join(tags) if tags else ""

        normalized_summary, normalized_content = self._normalize_content(
            summary, clarified
        )

        frontmatter_dict = {
            "id": note_id,
            "created": now.isoformat(),
            "status": status,
            "summary": normalized_summary,
            "tags": f"[{tags_str}]",
            "original": original,
        }
        if rejection_reason:
            frontmatter_dict["rejection_reason"] = rejection_reason

        frontmatter = self._build_frontmatter(frontmatter_dict)
        content = frontmatter + f"\n\n# {normalized_summary}\n\n{normalized_content}"

        if status == "received":
            target_dir = self.workspace.get_received_dir()
        elif status == "pending":
            target_dir = self.workspace.get_pending_dir()
        elif status == "rejected":
            target_dir = self.workspace.get_rejected_dir()
        else:
            target_dir = self.notes_dir

        filepath = target_dir / f"{note_id}.md"
        filepath.write_text(content, encoding="utf-8")

        if session_record:
            session_filename = f"session_{note_id}.json"
            session_filepath = self.sessions_dir / session_filename
            session_filepath.write_text(
                json.dumps(session_record, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        return filepath

    def _normalize_content(self, summary: str, content: str) -> tuple[str, str]:
        if content.strip().startswith("{"):
            try:
                parsed = json.loads(content.strip())
                if isinstance(parsed, dict):
                    extracted_summary = parsed.get("summary", summary)
                    extracted_content = parsed.get("content", content)
                    if extracted_summary != summary:
                        return extracted_summary, extracted_content
            except json.JSONDecodeError:
                pass
        return summary, content

    def save_conversation(
        self,
        conversation: list[dict[str, Any]],
        summary: str,
        session_id: str,
    ) -> Path:
        conversation_filename = f"conversation_{session_id}.json"
        conversation_filepath = self.sessions_dir / conversation_filename

        data = {
            "session_id": session_id,
            "created": datetime.now().isoformat(),
            "summary": summary,
            "conversation": conversation,
        }

        conversation_filepath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return conversation_filepath

    def list_pending(self) -> list[dict[str, Any]]:
        pending_dir = self.workspace.get_pending_dir()
        pending_notes = []

        for filepath in pending_dir.glob("*.md"):
            content = filepath.read_text(encoding="utf-8")
            frontmatter, _ = self._parse_frontmatter(content)
            pending_notes.append(
                {
                    "id": frontmatter.get("id", filepath.stem),
                    "filepath": filepath,
                    "summary": frontmatter.get("summary", ""),
                    "original": frontmatter.get("original", ""),
                    "created": frontmatter.get("created", ""),
                }
            )

        return pending_notes

    def move_file(
        self,
        note_id: str,
        from_dir: Path,
        to_status: str,
        rejection_reason: str | None = None,
    ) -> Path:
        source_path = from_dir / f"{note_id}.md"
        if not source_path.exists():
            raise FileNotFoundError(f"文件不存在: {source_path}")

        content = source_path.read_text(encoding="utf-8")
        frontmatter, body = self._parse_frontmatter(content)

        if to_status == "received":
            target_dir = self.workspace.get_received_dir()
        elif to_status == "rejected":
            target_dir = self.workspace.get_rejected_dir()
        elif to_status == "pending":
            target_dir = self.workspace.get_pending_dir()
        else:
            raise ValueError(f"无效状态: {to_status}")

        frontmatter["status"] = to_status
        if rejection_reason:
            frontmatter["rejection_reason"] = rejection_reason
        elif "rejection_reason" in frontmatter:
            del frontmatter["rejection_reason"]

        new_content = self._build_frontmatter(frontmatter) + "\n" + body
        target_path = target_dir / f"{note_id}.md"
        target_path.write_text(new_content, encoding="utf-8")

        source_path.unlink()

        return target_path

    def _parse_frontmatter(self, content: str) -> tuple[dict[str, str], str]:
        lines = content.split("\n")
        if not lines or lines[0].strip() != "---":
            return {}, content

        frontmatter_lines = []
        body_lines = []
        in_frontmatter = True
        found_closing = False

        for line in lines[1:]:
            if line.strip() == "---" and not found_closing:
                found_closing = True
                in_frontmatter = False
                continue
            if in_frontmatter:
                frontmatter_lines.append(line)
            else:
                body_lines.append(line)

        frontmatter = {}
        for line in frontmatter_lines:
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip('"')

        return frontmatter, "\n".join(body_lines)

    def _build_frontmatter(self, frontmatter: dict[str, str]) -> str:
        lines = ["---"]
        for key, value in frontmatter.items():
            lines.append(f"{key}: {value}")
        lines.append("---")
        return "\n".join(lines)
