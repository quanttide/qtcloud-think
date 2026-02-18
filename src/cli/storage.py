import os
from datetime import datetime
from pathlib import Path


class Storage:
    def __init__(self, notes_dir: str | None = None):
        if notes_dir is None:
            notes_dir = os.getenv("NOTES_DIR", "./notes")
        self.notes_dir = Path(notes_dir)
        self.notes_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self, original: str, clarified: str, summary: str, tags: list[str] | None = None
    ) -> Path:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H%M%S")

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
        return filepath
