from __future__ import annotations

from app.agents.base import Agent
from app.skills.clarify import ClarifySkill
from app.skills.organize import OrganizeSkill
from app.skills.distill import DistillSkill
from app.skills.express import ExpressSkill
from app.infrastructure import SessionRecorder, Storage

from app.agents.observer import Observer


class Sower(Agent):
    """启发者智能体

    围绕上下文选择必要的技能（CODE）来处理思维：
    - C (Clarify): 澄清需求
    - O (Organize): 联想关联
    - D (Distill): 精炼思考
    - E (Express): 表达导出

    可注入 Observer 接收客观指标反馈
    """

    def __init__(
        self,
        recorder: SessionRecorder | None = None,
        storage: Storage | None = None,
        observer: "Observer | None" = None,
    ):
        self.recorder = recorder
        self.storage = storage
        self.observer = observer
        self.skills = {
            "C": ClarifySkill(),
            "O": OrganizeSkill(),
            "D": DistillSkill(),
            "E": ExpressSkill(storage) if storage else None,
        }

    def run(self, input_text: str, skill_code: str = "C") -> str:
        """根据 skill_code 选择对应技能执行"""
        skill = self.skills.get(skill_code)
        if not skill:
            raise ValueError(f"Unknown skill code: {skill_code}")
        return skill.execute(input_text)

    def clarify(self, input_text: str) -> str:
        return self.skills["C"].execute(input_text)

    def organize(self, notes: list[dict]) -> str:
        return self.skills["O"].execute(notes)

    def distill(self, content: str) -> str:
        return self.skills["D"].execute(content)

    def express(self, content: str, format: str = "markdown") -> str:
        skill = self.skills["E"]
        if not skill:
            raise ValueError("Express skill requires storage to be initialized")
        return skill.execute(content, format)
