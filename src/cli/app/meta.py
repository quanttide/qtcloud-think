from pathlib import Path

from session_recorder import SessionRecord
from workspace import Workspace


class Meta:
    def __init__(self, workspace: Workspace | None = None):
        self.workspace = workspace or Workspace("meta")
        self.meta_dir = self.workspace.root
        self.analysis_result: dict = {}

    def analyze(self, record: SessionRecord) -> dict:
        issues = []
        suggestions = []

        if record.rounds > 5:
            issues.append(f"澄清轮次过多: {record.rounds}")
            suggestions.append("建议优化首轮意图识别，减少澄清轮次")

        if record.duration > 120:
            issues.append(f"耗时过长: {record.duration:.1f}s")
            suggestions.append("建议检查 LLM 响应速度")

        if record.api_calls > 10:
            issues.append(f"API 调用过多: {record.api_calls}")
            suggestions.append("建议合并 API 调用或优化逻辑")

        if record.errors:
            issues.append(f"发生错误: {len(record.errors)} 个")
            for err in record.errors:
                suggestions.append(f"错误: {err['type']} - {err['message']}")

        if record.first_intent_captured is False:
            suggestions.append("首轮意图识别未抓住核心，建议优化 prompt")

        if record.user_abandoned:
            issues.append("用户中断对话")
            suggestions.append("追问方式可能不够友好，需要优化")

        if not record.storage_success:
            issues.append("存储失败")
            suggestions.append("检查存储路径和权限")

        self.analysis_result = {
            "session_id": record.session_id,
            "date": record.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "rounds": record.rounds,
            "duration": record.duration,
            "api_calls": record.api_calls,
            "issues": issues,
            "suggestions": suggestions,
        }
        return self.analysis_result

    def save(self, record: SessionRecord, analysis: dict | None = None) -> Path:
        if analysis is None:
            analysis = self.analyze(record)

        date_str = record.start_time.strftime("%Y-%m-%d")
        filepath = self.meta_dir / f"{date_str}.md"

        # 汇总数据（如果 analysis 包含）
        session_count = analysis.get("session_count", 1)
        avg_rounds = analysis.get("avg_rounds", record.rounds)
        avg_api_calls = analysis.get("avg_api_calls", record.api_calls)
        avg_duration = analysis.get("avg_duration", record.duration)
        issues = analysis.get("issues", [])
        suggestions = analysis.get("suggestions", [])

        content = f"""---
date: {date_str}
session_count: {session_count}
avg_rounds: {avg_rounds:.1f}
avg_api_calls: {avg_api_calls:.1f}
avg_duration: {avg_duration:.1f}s
---

# Meta 自省报告

## 汇总统计
- 会话总数: {session_count}
- 平均澄清轮次: {avg_rounds:.1f}
- 平均 API 调用: {avg_api_calls:.1f}
- 平均耗时: {avg_duration:.1f}s

## 发现问题
"""

        if issues:
            for issue in issues:
                content += f"- {issue}\n"
        else:
            content += "- 运行正常\n"

        content += "\n## 改进建议\n"
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                content += f"{i}. {suggestion}\n"
        else:
            content += "- 无\n"

        filepath.write_text(content, encoding="utf-8")
        return filepath
