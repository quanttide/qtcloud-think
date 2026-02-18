import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from workspace import Workspace
from storage import Storage


class TestWorkspaceDirectories:
    """测试 Workspace 目录方法"""

    def test_get_received_dir(self, tmp_path, monkeypatch):
        """测试获取 received 目录"""
        monkeypatch.chdir(tmp_path)

        class TestWorkspace(Workspace):
            def __init__(self, name: str = "test"):
                self.name = name
                self.root = tmp_path / "data" / name

        ws = TestWorkspace()
        received_dir = ws.get_received_dir()

        assert received_dir.exists()
        assert "received" in str(received_dir)

    def test_get_pending_dir(self, tmp_path, monkeypatch):
        """测试获取 pending 目录"""
        monkeypatch.chdir(tmp_path)

        class TestWorkspace(Workspace):
            def __init__(self, name: str = "test"):
                self.name = name
                self.root = tmp_path / "data" / name

        ws = TestWorkspace()
        pending_dir = ws.get_pending_dir()

        assert pending_dir.exists()
        assert "pending" in str(pending_dir)

    def test_get_rejected_dir(self, tmp_path, monkeypatch):
        """测试获取 rejected 目录"""
        monkeypatch.chdir(tmp_path)

        class TestWorkspace(Workspace):
            def __init__(self, name: str = "test"):
                self.name = name
                self.root = tmp_path / "data" / name

        ws = TestWorkspace()
        rejected_dir = ws.get_rejected_dir()

        assert rejected_dir.exists()
        assert "rejected" in str(rejected_dir)


class TestStorageStatus:
    """测试 Storage 状态分类存储"""

    def test_save_received(self, tmp_path, monkeypatch):
        """测试保存 received 状态"""
        monkeypatch.chdir(tmp_path)

        class TestWorkspace(Workspace):
            def __init__(self, name: str = "test"):
                self.name = name
                self.root = tmp_path / "data" / name

        ws = TestWorkspace()
        storage = Storage(ws)

        filepath = storage.save(
            original="test original",
            clarified="test clarified",
            summary="test summary",
            status="received",
        )

        assert filepath.exists()
        assert "received" in str(filepath)
        content = filepath.read_text()
        assert "status: received" in content
        assert "test summary" in content

    def test_save_pending(self, tmp_path, monkeypatch):
        """测试保存 pending 状态"""
        monkeypatch.chdir(tmp_path)

        class TestWorkspace(Workspace):
            def __init__(self, name: str = "test"):
                self.name = name
                self.root = tmp_path / "data" / name

        ws = TestWorkspace()
        storage = Storage(ws)

        filepath = storage.save(
            original="test original",
            clarified="test clarified",
            summary="test summary",
            status="pending",
        )

        assert filepath.exists()
        assert "pending" in str(filepath)
        content = filepath.read_text()
        assert "status: pending" in content

    def test_save_rejected_with_reason(self, tmp_path, monkeypatch):
        """测试保存 rejected 状态及原因"""
        monkeypatch.chdir(tmp_path)

        class TestWorkspace(Workspace):
            def __init__(self, name: str = "test"):
                self.name = name
                self.root = tmp_path / "data" / name

        ws = TestWorkspace()
        storage = Storage(ws)

        filepath = storage.save(
            original="test original",
            clarified="test clarified",
            summary="test summary",
            status="rejected",
            rejection_reason="not relevant",
        )

        assert filepath.exists()
        content = filepath.read_text()
        assert "status: rejected" in content
        assert "not relevant" in content

    def test_list_pending(self, tmp_path, monkeypatch):
        """测试列出 pending 内容"""
        monkeypatch.chdir(tmp_path)

        class TestWorkspace(Workspace):
            def __init__(self, name: str = "test"):
                self.name = name
                self.root = tmp_path / "data" / name

        ws = TestWorkspace()
        storage = Storage(ws)

        storage.save(
            original="original 1",
            clarified="clarified 1",
            summary="summary 1",
            status="pending",
        )

        pending = storage.list_pending()

        assert len(pending) == 1
        assert pending[0]["summary"] == "summary 1"

    def test_move_file(self, tmp_path, monkeypatch):
        """测试移动文件到不同状态"""
        monkeypatch.chdir(tmp_path)

        class TestWorkspace(Workspace):
            def __init__(self, name: str = "test"):
                self.name = name
                self.root = tmp_path / "data" / name

        ws = TestWorkspace()
        storage = Storage(ws)

        filepath = storage.save(
            original="original",
            clarified="clarified",
            summary="summary",
            status="pending",
        )

        note_id = filepath.stem

        storage.move_file(note_id, ws.get_pending_dir(), "received")

        assert not filepath.exists()
        new_filepath = ws.get_received_dir() / f"{note_id}.md"
        assert new_filepath.exists()

        content = new_filepath.read_text()
        assert "status: received" in content

    def test_parse_frontmatter(self, tmp_path, monkeypatch):
        """测试解析 frontmatter"""
        monkeypatch.chdir(tmp_path)

        class TestWorkspace(Workspace):
            def __init__(self, name: str = "test"):
                self.name = name
                self.root = tmp_path / "data" / name

        ws = TestWorkspace()
        storage = Storage(ws)

        content = """---
id: test-id
status: pending
summary: "test summary"
---

# Body content
"""

        frontmatter, body = storage._parse_frontmatter(content)

        assert frontmatter["id"] == "test-id"
        assert frontmatter["status"] == "pending"
        assert "Body content" in body
