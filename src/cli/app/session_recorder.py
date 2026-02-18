from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SessionRecord:
    session_id: str
    start_time: datetime = field(default_factory=datetime.now)

    rounds: int = 0
    end_time: datetime | None = None

    first_intent_captured: bool | None = None

    storage_success: bool = False
    file_path: str = ""

    user_abandoned: bool = False

    api_calls: int = 0

    errors: list[dict[str, str]] = field(default_factory=list)

    @property
    def duration(self) -> float:
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()


class SessionRecorder:
    def __init__(self, session_id: str):
        self.record = SessionRecord(session_id=session_id)

    def record_round(self) -> None:
        self.record.rounds += 1

    def record_api_call(self) -> None:
        self.record.api_calls += 1

    def record_intent_captured(self, captured: bool) -> None:
        if self.record.first_intent_captured is None:
            self.record.first_intent_captured = captured

    def record_storage(self, success: bool, file_path: str = "") -> None:
        self.record.storage_success = success
        self.record.file_path = file_path

    def record_user_abandoned(self) -> None:
        self.record.user_abandoned = True

    def record_error(self, error_type: str, message: str) -> None:
        self.record.errors.append({"type": error_type, "message": message})

    def end_session(self) -> SessionRecord:
        self.record.end_time = datetime.now()
        return self.record
