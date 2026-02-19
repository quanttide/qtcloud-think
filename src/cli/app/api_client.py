import os
from typing import Any

import httpx

PROVIDER_URL = os.getenv("PROVIDER_URL", "http://localhost:8000")


class APIClient:
    def __init__(self, base_url: str = PROVIDER_URL):
        self.base_url = base_url
        self.client = httpx.Client(timeout=60.0)

    def close(self):
        self.client.close()

    def is_available(self) -> bool:
        try:
            response = self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False

    def reflect(self, original: str) -> str:
        response = self.client.post(
            f"{self.base_url}/api/v1/clarify/reflect",
            json={"original": original},
        )
        response.raise_for_status()
        return response.json()["reflection"]

    def summarize(self, conversation: list[dict[str, Any]]) -> dict:
        response = self.client.post(
            f"{self.base_url}/api/v1/clarify/summarize",
            json={"conversation": conversation},
        )
        response.raise_for_status()
        return response.json()

    def continue_dialogue(self, conversation: list[dict[str, Any]]) -> str:
        response = self.client.post(
            f"{self.base_url}/api/v1/clarify/continue",
            json={"conversation": conversation},
        )
        response.raise_for_status()
        return response.json()["response"]

    def create_note(
        self,
        original: str,
        content: str,
        summary: str,
        status: str = "received",
        session_record: dict | None = None,
        session_id: str | None = None,
        rejection_reason: str | None = None,
    ) -> dict:
        response = self.client.post(
            f"{self.base_url}/api/v1/notes",
            json={
                "original": original,
                "content": content,
                "summary": summary,
                "status": status,
                "session_record": session_record,
                "session_id": session_id,
                "rejection_reason": rejection_reason,
            },
        )
        response.raise_for_status()
        return response.json()

    def list_pending(self, workspace: str = "default") -> list[dict]:
        response = self.client.get(
            f"{self.base_url}/api/v1/notes/pending",
            params={"workspace": workspace},
        )
        response.raise_for_status()
        return response.json()["notes"]

    def update_note_status(
        self,
        note_id: str,
        status: str,
        rejection_reason: str | None = None,
        workspace: str = "default",
    ) -> dict:
        response = self.client.put(
            f"{self.base_url}/api/v1/notes/{note_id}/status",
            json={
                "status": status,
                "rejection_reason": rejection_reason,
            },
            params={"workspace": workspace},
        )
        response.raise_for_status()
        return response.json()

    def analyze_meta(self, workspace: str = "default") -> dict:
        response = self.client.post(
            f"{self.base_url}/api/v1/meta/analyze",
            params={"workspace": workspace},
        )
        response.raise_for_status()
        return response.json()


def get_client() -> APIClient:
    return APIClient()
