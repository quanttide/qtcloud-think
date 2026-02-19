from infrastructure.storage import Storage


class ExpressSkill:
    """E - 表达技能：导出知识到外部格式"""

    def __init__(self, storage: Storage):
        self.storage = storage

    def execute(self, content: str, format: str = "markdown") -> str:
        # TODO: 实现导出逻辑
        return ""
