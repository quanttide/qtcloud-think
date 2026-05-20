import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from llm_client import get_client


class ModuleAnalyzer:
    """使用 LLM 分析模块语义"""

    RESPONSIBILITY_PROMPT = """分析以下 Python 模块的职责。用一句话概括其功能。

模块代码（前1500字符）：
```
{code_content}
```

请返回 JSON 格式：
{{"responsibility": "一句话描述模块职责"}}"""

    RELATIONSHIP_PROMPT = """分析以下模块的依赖关系。

模块列表：{modules}

请分析每个模块依赖哪些其他模块，返回 JSON 格式：
{{
    "dependencies": {{
        "模块名": ["被依赖的模块列表"]
    }}
}}"""

    DUPLICATE_PROMPT = """比较以下模块的职责，判断是否有功能重复。

模块职责：
{responsibilities}

请返回 JSON 格式：
{{
    "duplicates": [
        {{"modules": ["模块A", "模块B"], "reason": "重复原因"}}
    ],
    "warnings": ["警告信息"]
}}"""

    def __init__(self, src_dir: Path):
        self.src_dir = src_dir
        self.client = get_client()
        self.modules: dict[str, str] = {}

    def _discover_modules(self) -> dict[str, str]:
        """发现所有模块及其代码"""
        modules = {}
        for file in self.src_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue
            code = file.read_text(encoding="utf-8")
            modules[file.stem] = code
        self.modules = modules
        return modules

    def analyze_responsibilities(self) -> dict[str, str]:
        """让 LLM 为每个模块生成职责描述"""
        responsibilities = {}

        for name, code in self.modules.items():
            prompt = self.RESPONSIBILITY_PROMPT.format(code_content=code[:1500])
            response = self.client.chat([
                {"role": "system", "content": "你是一个代码架构分析师，擅长概括模块职责。直接返回 JSON，不要有其他内容。"},
                {"role": "user", "content": prompt},
            ]).content

            try:
                result = json.loads(response.strip().strip("```json").strip("```"))
                responsibilities[name] = result.get("responsibility", "未知")
            except json.JSONDecodeError:
                responsibilities[name] = "分析失败"

        return responsibilities

    def analyze_relationships(self) -> dict[str, list[str]]:
        """分析模块间的依赖关系"""
        modules_list = list(self.modules.keys())
        prompt = self.RELATIONSHIP_PROMPT.format(modules=", ".join(modules_list))
        response = self.client.chat([
            {"role": "system", "content": "你是一个代码架构分析师，擅长分析模块依赖关系。直接返回 JSON，不要有其他内容。"},
            {"role": "user", "content": prompt},
        ]).content

        try:
            result = json.loads(response.strip().strip("```json").strip("```"))
            return result.get("dependencies", {})
        except json.JSONDecodeError:
            return {}

    def check_duplicates(self) -> dict:
        """检查是否有功能重复的模块"""
        responsibilities = self.analyze_responsibilities()

        if len(responsibilities) < 2:
            return {"duplicates": [], "warnings": ["模块数量不足，无法比较"]}

        resp_text = "\n".join(
            f"- {name}: {desc}" for name, desc in responsibilities.items()
        )
        prompt = self.DUPLICATE_PROMPT.format(responsibilities=resp_text)

        response = self.client.chat([
            {"role": "system", "content": "你是一个代码架构分析师，擅长发现功能重复的模块。直接返回 JSON，不要有其他内容。"},
            {"role": "user", "content": prompt},
        ]).content

        try:
            result = json.loads(response.strip().strip("```json").strip("```"))
            return result
        except json.JSONDecodeError:
            return {"duplicates": [], "warnings": ["分析失败"]}

    def generate_report(self) -> str:
        """生成模块地图报告"""
        self._discover_modules()
        responsibilities = self.analyze_responsibilities()
        dependencies = self.analyze_relationships()
        duplicates = self.check_duplicates()

        lines = ["📦 模块地图", ""]

        for name, desc in responsibilities.items():
            deps = dependencies.get(name, [])
            deps_str = f" (→ {', '.join(deps)})" if deps else ""
            lines.append(f"├── {name}{deps_str}")
            lines.append(f"│   └── {desc}")
            lines.append("")

        if duplicates.get("duplicates") or duplicates.get("warnings"):
            lines.append("⚠️ 发现问题:")
            for dup in duplicates.get("duplicates", []):
                lines.append(f"  - {', '.join(dup['modules'])}: {dup['reason']}")
            for warn in duplicates.get("warnings", []):
                lines.append(f"  - {warn}")
        else:
            lines.append("✅ 未发现明显问题")

        return "\n".join(lines)


def test_module_analyzer_can_be_instantiated():
    """测试 ModuleAnalyzer 可以被实例化"""
    analyzer = ModuleAnalyzer(Path("app"))
    assert analyzer is not None
    assert analyzer.src_dir == Path("app")


def test_module_analyzer_discovers_modules():
    """测试模块发现功能"""
    analyzer = ModuleAnalyzer(Path("app"))
    modules = analyzer._discover_modules()
    assert len(modules) > 0
    assert "main" in modules
    assert "clarifier" in modules


def test_workspace_default_name():
    """测试默认工作空间名称"""
    from app.workspace import Workspace

    ws = Workspace()
    assert ws.name == "default"


def test_workspace_custom_name():
    """测试自定义工作空间名称"""
    from app.workspace import Workspace

    ws = Workspace("meta")
    assert ws.name == "meta"


if __name__ == "__main__":
    analyzer = ModuleAnalyzer(Path("app"))
    print(analyzer.generate_report())
