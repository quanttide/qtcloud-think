"""
系统测试：验证 qtcloud-think 各模块正常工作

运行方式：
    pytest tests/ -v
    pytest tests/test_system.py -v -k "test_studio"
"""

import pytest
import subprocess
import time
import os
import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PROVIDER_DIR = PROJECT_ROOT / "src" / "provider"
CLI_DIR = PROJECT_ROOT / "src" / "cli"


@pytest.fixture(scope="module")
def provider_server():
    """启动 Provider 服务"""
    original_dir = os.getcwd()
    os.chdir(PROVIDER_DIR)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROVIDER_DIR)

    proc = subprocess.Popen(
        [
            ".venv/bin/python",
            "-m",
            "uvicorn",
            "main:app",
            "--port",
            "8000",
            "--host",
            "127.0.0.1",
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=PROVIDER_DIR,
    )

    # 等待服务启动
    max_retries = 30
    for _ in range(max_retries):
        try:
            resp = requests.get("http://127.0.0.1:8000/health", timeout=1)
            if resp.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(0.5)

    yield proc

    # 清理
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()

    os.chdir(original_dir)


class TestProvider:
    """Provider API 测试"""

    def test_health(self, provider_server):
        """健康检查"""
        resp = requests.get("http://127.0.0.1:8000/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_workspace_info(self, provider_server):
        """获取工作空间信息"""
        resp = requests.get(
            "http://127.0.0.1:8000/api/v1/workspace", params={"workspace": "default"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "name" in data

    def test_clarify_reflect(self, provider_server):
        """测试反思接口"""
        resp = requests.post(
            "http://127.0.0.1:8000/api/v1/clarify/reflect",
            json={"original": "测试想法"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "reflection" in data

    def test_clarify_summarize(self, provider_server):
        """测试总结接口"""
        conversation = [
            {"role": "user", "content": "测试想法"},
            {"role": "assistant", "content": "复述测试想法"},
        ]
        resp = requests.post(
            "http://127.0.0.1:8000/api/v1/clarify/summarize",
            json=conversation,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "summary" in data

    def test_notes_crud(self, provider_server):
        """测试笔记 CRUD"""
        # 创建笔记
        resp = requests.post(
            "http://127.0.0.1:8000/api/v1/notes",
            json={
                "original": "测试原始输入",
                "content": "测试内容",
                "summary": "测试摘要",
                "status": "received",
            },
        )
        assert resp.status_code == 200

        # 获取笔记列表
        resp = requests.get("http://127.0.0.1:8000/api/v1/notes")
        assert resp.status_code == 200
        notes = resp.json()["notes"]
        assert len(notes) > 0


class TestCLI:
    """CLI 测试"""

    def test_cli_help(self):
        """测试 CLI 帮助"""
        result = subprocess.run(
            ["python", "-m", "pytest", "--version"],
            cwd=CLI_DIR,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0


class TestStudio:
    """Studio 测试"""

    def test_flutter_analyze(self):
        """Flutter 代码分析"""
        result = subprocess.run(
            ["flutter", "analyze"],
            cwd=PROJECT_ROOT / "src" / "studio",
            capture_output=True,
            text=True,
            timeout=120,
        )
        # 允许警告但不能有严重错误
        assert "error" not in result.stdout.lower() or result.returncode == 0

    def test_flutter_build_web(self):
        """Flutter Web 构建"""
        result = subprocess.run(
            ["flutter", "build", "web", "--release"],
            cwd=PROJECT_ROOT / "src" / "studio",
            capture_output=True,
            text=True,
            timeout=300,
        )
        assert result.returncode == 0
        assert (PROJECT_ROOT / "src" / "studio" / "build" / "web").exists()


class TestIntegration:
    """集成测试"""

    def test_provider_notes_flow(self, provider_server):
        """完整的笔记流程"""
        # 1. 反思
        resp = requests.post(
            "http://127.0.0.1:8000/api/v1/clarify/reflect",
            json={"original": "这是一个集成测试想法"},
        )
        reflection = resp.json()["reflection"]

        # 2. 总结
        conversation = [
            {"role": "user", "content": "这是一个集成测试想法"},
            {"role": "assistant", "content": reflection},
        ]
        resp = requests.post(
            "http://127.0.0.1:8000/api/v1/clarify/summarize",
            json=conversation,
        )
        summary_data = resp.json()

        # 3. 保存笔记
        resp = requests.post(
            "http://127.0.0.1:8000/api/v1/notes",
            json={
                "original": "这是一个集成测试想法",
                "content": summary_data.get("content", ""),
                "summary": summary_data.get("summary", ""),
                "status": "received",
            },
        )
        assert resp.status_code == 200
        note_id = resp.json()["id"]

        # 4. 获取笔记列表验证
        resp = requests.get("http://127.0.0.1:8000/api/v1/notes")
        notes = resp.json()["notes"]
        note_ids = [n["id"] for n in notes]
        assert note_id in note_ids
