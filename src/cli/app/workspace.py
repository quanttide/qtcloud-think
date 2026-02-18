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

    def get_received_dir(self) -> Path:
        received_dir = self.get_notes_dir() / "received"
        received_dir.mkdir(parents=True, exist_ok=True)
        return received_dir

    def get_pending_dir(self) -> Path:
        pending_dir = self.get_notes_dir() / "pending"
        pending_dir.mkdir(parents=True, exist_ok=True)
        return pending_dir

    def get_rejected_dir(self) -> Path:
        rejected_dir = self.get_notes_dir() / "rejected"
        rejected_dir.mkdir(parents=True, exist_ok=True)
        return rejected_dir

    def __str__(self) -> str:
        return self.name
