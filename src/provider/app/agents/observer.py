from app.agents.base import Agent
from app.infrastructure.llm_client import get_client

METRICS = ["clarity", "completeness", "depth", "coherence", "relevance"]


class Observer(Agent):
    """观察者 - 通过客观指标观察启发者与用户的交互

    围绕可量化指标与启发者沟通：
    - clarity: 思考清晰度
    - completeness: 信息完整度
    - depth: 思考深度
    - coherence: 逻辑连贯性
    - relevance: 与目标的相关性
    """

    def __init__(self):
        self.client = get_client()
        self.metrics = METRICS

    def evaluate(self, conversation: list[dict]) -> dict[str, float]:
        """评估对话的各项指标"""
        # TODO: 实现评估逻辑
        return {metric: 0.0 for metric in self.metrics}

    def feedback(self, conversation: list[dict]) -> str:
        """基于指标生成反馈"""
        self.evaluate(conversation)
        # TODO: 生成具体反馈
        return ""

    def run(self, conversation: list[dict]) -> str:
        return self.feedback(conversation)
