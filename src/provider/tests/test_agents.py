import pytest
from unittest.mock import MagicMock, patch

from app.agents.base import Agent
from app.agents.sower import Sower
from app.agents.observer import Observer, METRICS
from app.skills.clarify import ClarifySkill
from app.skills.organize import OrganizeSkill
from app.skills.distill import DistillSkill


class TestAgentBase:
    def test_agent_is_abstract(self):
        with pytest.raises(TypeError):
            Agent()


class TestSower:
    def test_sower_initialization(self):
        sower = Sower()
        assert isinstance(sower, Agent)
        assert "C" in sower.skills
        assert "O" in sower.skills
        assert "D" in sower.skills

    @patch("app.skills.clarify.get_client")
    def test_sower_clarify(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.chat_once.return_value = "clarified content"
        mock_get_client.return_value = mock_client

        sower = Sower()
        result = sower.clarify("test input")
        assert result == "clarified content"
        mock_client.chat_once.assert_called_once()

    @patch("app.skills.organize.get_client")
    def test_sower_organize(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.chat_once.return_value = "organized"
        mock_get_client.return_value = mock_client

        sower = Sower()
        notes = [{"content": "note1"}, {"content": "note2"}]
        result = sower.organize(notes)
        assert result == ""  # TODO: implement

    @patch("app.skills.distill.get_client")
    def test_sower_distill(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.chat_once.return_value = "distilled"
        mock_get_client.return_value = mock_client

        sower = Sower()
        result = sower.distill("long content")
        assert result == ""  # TODO: implement

    def test_sower_run_with_skill_code(self):
        sower = Sower()
        with patch.object(sower.skills["C"], "execute", return_value="result") as mock:
            result = sower.run("test", "C")
            assert result == "result"
            mock.assert_called_once_with("test")

    def test_sower_run_unknown_skill(self):
        sower = Sower()
        with pytest.raises(ValueError, match="Unknown skill code"):
            sower.run("test", "X")


class TestObserver:
    def test_observer_initialization(self):
        observer = Observer()
        assert isinstance(observer, Agent)
        assert observer.metrics == METRICS
        assert len(METRICS) == 5

    def test_metrics定义(self):
        expected = ["clarity", "completeness", "depth", "coherence", "relevance"]
        assert METRICS == expected

    @patch("app.agents.observer.get_client")
    def test_observer_evaluate(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        observer = Observer()
        conversation = [{"role": "user", "content": "hello"}]
        result = observer.evaluate(conversation)

        assert isinstance(result, dict)
        for metric in METRICS:
            assert metric in result

    @patch("agents.observer.get_client")
    def test_observer_feedback(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        observer = Observer()
        conversation = [{"role": "user", "content": "hello"}]
        result = observer.feedback(conversation)
        assert isinstance(result, str)


class TestClarifySkill:
    @patch("skills.clarify.get_client")
    def test_clarify_skill_execute(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.chat_once.return_value = "clarified"
        mock_get_client.return_value = mock_client

        skill = ClarifySkill()
        result = skill.execute("原始输入")
        assert result == "clarified"
        mock_client.chat_once.assert_called_once()


class TestOrganizeSkill:
    @patch("skills.organize.get_client")
    def test_organize_skill_execute(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.chat_once.return_value = "organized"
        mock_get_client.return_value = mock_client

        skill = OrganizeSkill()
        notes = [{"content": "note"}]
        result = skill.execute(notes)
        assert result == ""  # TODO: implement


class TestDistillSkill:
    @patch("skills.distill.get_client")
    def test_distill_skill_execute(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.chat_once.return_value = "distilled"
        mock_get_client.return_value = mock_client

        skill = DistillSkill()
        result = skill.execute("long content")
        assert result == ""  # TODO: implement
