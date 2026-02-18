# AGENTS.md - qtcloud-think 开发指南

## 项目概览

- **名称**: qtcloud-think (量潮思考云)
- **类型**: "思维外脑" - 思维收集与澄清工具
- **状态**: 探索期 (0.0.x)
- **发布规范**: 探索期(0.0.x)有新价值即发布；验证期(0.x.y)验证团队协作；发布期(x.y.z)市场上线

## 项目结构

```
src/
├── cli/           # Python + Typer CLI 工具
├── provider/      # FastAPI 后端服务
└── studio/        # Flutter 桌面/移动端
packages/          # 公共库集合（多语言）
scripts/           # 项目级自动化脚本
data/              # 动态数据目录（运行时生成，不提交Git）
```

---

## 环境配置

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### CLI 开发

```bash
cd src/cli
uv venv && uv sync
uv run python main.py

# 单个测试
pytest tests/test_file.py::TestClass::test_method
pytest tests/ -k "pattern"

# Lint & Format
ruff check . && black . && isort . && mypy src/
```

### Provider 开发

```bash
cd src/provider
uv venv && uv sync
uv run uvicorn src.provider.main:app --reload
```

---

## 代码规范

### Python 工具链

| 工具 | 作用 | 配置 |
|------|------|------|
| Black | 格式化 | 行长 100 |
| isort | 导入排序 | 标准库→外部库→内部模块 |
| ruff | Linting | 替代 flake8, isort |
| mypy | 类型检查 | strict mode |

```bash
isort . && black . && ruff check . --fix && mypy src/
```

### 命名约定

| 类型 | 规则 | 示例 |
|------|------|------|
| 文件 | snake_case.py | `user_service.py` |
| 类 | PascalCase | `ThoughtCollector` |
| 函数/变量 | snake_case | `collect_thoughts()` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRIES = 3` |
| 布尔值 | is_/has_/can_/should_ 前缀 | `is_valid` |

### 导入排序

```python
# 1. 标准库
import os
# 2. 外部库
import typer
# 3. 内部模块
from . import module
```

### 类型提示

- 所有函数签名标注类型
- 使用 `| None` 而非 `Optional`
- 泛型优先于 Union

```python
def process(items: list[str]) -> dict[str, int] | None:
    ...
```

### 错误处理

- 使用具体异常类型（禁止 bare `except:`）
- 包含有意义的错误信息
- 异常需要传播时使用 `raise`

```python
# Good
raise ValueError(f"Invalid input: {value}")

# Bad
try:
    ...
except:  # 禁止
    pass
```

### 安全

- 禁止提交 secrets（使用 .env）
- 验证和清理用户输入

---

## 配置

- 环境变量: `.env` (项目根目录，不提交)
- 示例配置: `.env.example`
- 各子项目从项目根目录的 `.env` 加载配置

---

## 代码审查清单

- [ ] 代码符合命名规范
- [ ] 类型标注正确完整
- [ ] 导入排序正确
- [ ] 错误处理恰当（无 bare except）
- [ ] 测试覆盖核心逻辑
- [ ] 无硬编码 secrets
- [ ] Black/isort/ruff/mypy 检查通过
