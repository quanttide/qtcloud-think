import os
from pathlib import Path


class Workspace:
    DEFAULT = "default"

    def __init__(self, name: str | None = None):
        self.name = name or os.getenv("DEFAULT_WORKSPACE", self.DEFAULT)
        self.root = Path(__file__).parent.parent.parent.parent / "data" / self.name

    def get_notes_dir(self) -> Path:
        notes_dir = self.root / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)
        return notes_dir

    def __str__(self) -> str:
        return self.name
