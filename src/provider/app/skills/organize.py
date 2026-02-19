from infrastructure.llm_client import get_client


class OrganizeSkill:
    """O - 联想技能：寻找想法之间的关联"""

    def __init__(self):
        self.client = get_client()

    def execute(self, notes: list[dict]) -> str:
        # TODO: 实现联想逻辑
        return ""
