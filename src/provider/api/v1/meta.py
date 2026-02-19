import json

from fastapi import APIRouter

from core.session_recorder import SessionRecord
from core.workspace import Workspace

router = APIRouter(prefix="/meta", tags=["meta"])


@router.post("/analyze")
def analyze(workspace: str = "default") -> dict:
    """自省分析"""
    target_ws = Workspace(workspace)

    sessions_dir = target_ws.get_sessions_dir()
    if not sessions_dir.exists():
        return {"error": "没有会话数据"}

    sessions = []
    conversations = []

    for f in sessions_dir.glob("session_*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        sessions.append(SessionRecord.from_dict(data))

    for f in sessions_dir.glob("conversation_*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        conversations.append(data)

    if not sessions or not conversations:
        return {"error": "没有会话数据"}

    total_rounds = sum(s.rounds for s in sessions)
    total_api_calls = sum(s.api_calls for s in sessions)
    total_duration = sum(s.duration for s in sessions)
    abandoned_count = sum(1 for s in sessions if s.user_abandoned)
    storage_failed_count = sum(1 for s in sessions if not s.storage_success)

    avg_rounds = total_rounds / len(sessions)
    avg_api_calls = total_api_calls / len(sessions)
    avg_duration = total_duration / len(sessions)

    issues = []
    suggestions = []

    if avg_rounds > 5:
        issues.append(f"平均澄清轮次过多: {avg_rounds:.1f}")
        suggestions.append("建议优化首轮意图识别，减少澄清轮次")

    if avg_duration > 120:
        issues.append(f"平均耗时过长: {avg_duration:.1f}s")
        suggestions.append("建议检查 LLM 响应速度")

    if avg_api_calls > 10:
        issues.append(f"平均 API 调用过多: {avg_api_calls:.1f}")
        suggestions.append("建议合并 API 调用或优化逻辑")

    if abandoned_count > 0:
        issues.append(f"用户中断次数: {abandoned_count}/{len(sessions)}")
        suggestions.append("追问方式可能不够友好，需要优化")

    if storage_failed_count > 0:
        issues.append(f"存储失败次数: {storage_failed_count}/{len(sessions)}")
        suggestions.append("检查存储路径和权限")

    return {
        "session_count": len(sessions),
        "avg_rounds": avg_rounds,
        "avg_api_calls": avg_api_calls,
        "avg_duration": avg_duration,
        "abandoned_count": abandoned_count,
        "storage_failed_count": storage_failed_count,
        "issues": issues,
        "suggestions": suggestions,
    }
