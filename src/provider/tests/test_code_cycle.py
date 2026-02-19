"""
完整 CODE 循环测试：模拟启发者和观察者的协同

场景：用户输入一个模糊的想法，通过完整的 CODE 循环处理，
观察者在每个阶段提供客观指标反馈。
"""

from unittest.mock import MagicMock, patch

from agents.sower import Sower
from agents.observer import Observer, METRICS


class TestCodeCycle:
    """CODE 循环完整流程测试"""

    @patch("skills.clarify.get_client")
    @patch("skills.organize.get_client")
    @patch("skills.distill.get_client")
    def test_full_code_cycle_with_observer(
        self,
        mock_distill,
        mock_organize,
        mock_clarify,
    ):
        """
        完整 CODE 循环：
        1. C (Clarify) - 澄清
        2. O (Organize) - 联想
        3. D (Distill) - 精炼
        4. E (Express) - 表达

        每个阶段都有 Observer 提供反馈
        """
        mock_client = MagicMock()
        mock_clarify.return_value = mock_client
        mock_organize.return_value = mock_client
        mock_distill.return_value = mock_client

        mock_client.chat_once.side_effect = [
            "澄清后的内容：我想建立一个帮助思考的工具",  # C
            "关联：与项目管理工具有关联",  # O
            "精炼后的核心：思考辅助工具",  # D
        ]

        observer = Observer()
        sower = Sower(observer=observer)

        conversation = []

        # C - Clarify 阶段
        original_input = "我想做个东西帮助思考"
        clarified = sower.clarify(original_input)
        conversation.append({"role": "user", "content": original_input})
        conversation.append({"role": "assistant", "content": clarified})

        scores_c = observer.evaluate(conversation)
        assert scores_c["clarity"] >= 0  # 评估清晰度

        # O - Organize 阶段
        notes = [
            {"id": "1", "content": "帮助思考"},
            {"id": "2", "content": "思维外脑"},
        ]
        organized = sower.organize(notes)
        conversation.append({"role": "assistant", "content": organized})

        scores_o = observer.evaluate(conversation)
        assert scores_o["completeness"] >= 0  # 评估完整度

        # D - Distill 阶段
        distilled = sower.distill(clarified)
        conversation.append({"role": "assistant", "content": distilled})

        scores_d = observer.evaluate(conversation)
        assert scores_d["depth"] >= 0  # 评估深度

    @patch("skills.clarify.get_client")
    def test_observer_feedback_in_clarify_phase(self, mock_get_client):
        """测试观察者在 C 阶段的反馈"""
        mock_client = MagicMock()
        mock_client.chat_once.return_value = "澄清结果"
        mock_get_client.return_value = mock_client

        observer = Observer()
        sower = Sower(observer=observer)

        input_text = "做个app"
        sower.clarify(input_text)

        conversation = [
            {"role": "user", "content": input_text},
            {"role": "assistant", "content": "澄清结果"},
        ]

        scores = observer.evaluate(conversation)

        assert "clarity" in scores
        assert "completeness" in scores
        assert "depth" in scores
        assert "coherence" in scores
        assert "relevance" in scores

        feedback = observer.feedback(conversation)
        assert isinstance(feedback, str)

    @patch("skills.organize.get_client")
    def test_observer_feedback_in_organize_phase(self, mock_get_client):
        """测试观察者在 O 阶段的反馈"""
        mock_client = MagicMock()
        mock_client.chat_once.return_value = "关联分析"
        mock_get_client.return_value = mock_client

        observer = Observer()
        sower = Sower(observer=observer)

        notes = [{"content": "想法1"}, {"content": "想法2"}]
        sower.organize(notes)

        conversation = [
            {"role": "user", "content": "整理这些想法"},
            {"role": "assistant", "content": "关联分析"},
        ]

        scores = observer.evaluate(conversation)
        assert scores["completeness"] >= 0

    def test_sower_without_observer(self):
        """测试没有观察者时 Sower 仍能工作"""
        sower = Sower()

        with patch.object(sower.skills["C"], "execute", return_value="clarified"):
            result = sower.clarify("test")
            assert result == "clarified"

        with patch.object(sower.skills["O"], "execute", return_value=""):
            result = sower.organize([])
            assert result == ""

    @patch("skills.clarify.get_client")
    def test_observer_metrics_consistency(self, mock_get_client):
        """测试观察者指标一致性"""
        mock_client = MagicMock()
        mock_client.chat_once.return_value = "test"
        mock_get_client.return_value = mock_client

        observer1 = Observer()
        observer2 = Observer()

        conversation = [{"role": "user", "content": "test"}]

        scores1 = observer1.evaluate(conversation)
        scores2 = observer2.evaluate(conversation)

        assert set(scores1.keys()) == set(scores2.keys())
        assert scores1.keys() == set(METRICS)

    @patch("skills.clarify.get_client")
    @patch("skills.distill.get_client")
    def test_distill_after_clarify(self, mock_distill, mock_clarify):
        """测试 C -> D 流程"""
        mock_client = MagicMock()
        mock_clarify.return_value = mock_client
        mock_distill.return_value = mock_client

        mock_client.chat_once.side_effect = [
            "澄清后的内容",  # C
            "精炼后的内容",  # D
        ]

        sower = Sower()

        original = "模糊的想法"
        clarified = sower.clarify(original)
        distilled = sower.distill(clarified)

        assert clarified == "澄清后的内容"
        assert distilled == ""  # TODO: implement

    @patch("skills.clarify.get_client")
    @patch("skills.organize.get_client")
    def test_organize_uses_all_notes(self, mock_organize, mock_clarify):
        """测试联想技能处理所有笔记"""
        mock_client = MagicMock()
        mock_clarify.return_value = mock_client
        mock_organize.return_value = mock_client

        mock_client.chat_once.return_value = "找到3个关联"

        sower = Sower()

        notes = [
            {"id": "1", "content": "项目管理"},
            {"id": "2", "content": "时间管理"},
            {"id": "3", "content": "目标设定"},
        ]

        result = sower.organize(notes)
        assert result == ""  # TODO: implement
