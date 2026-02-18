# Contributing to qtcloud-think

感谢你的关注！以下是开发指南。

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

## 开发环境

### 安装 uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**注意**: Windows 系统使用 Git Bash、WSL 等 Unix-like 环境运行脚本。

### CLI 开发

```bash
cd src/cli
uv venv && uv sync
uv run python main.py
./scripts/collect  # 从项目根目录运行

# 测试
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

**代码与文档命名一致**：代码模块名与文档文件名尽量保持一致，便于查找关联。如 `collector.py` 对应 `docs/dev/collector.md`。

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

## 配置

- 环境变量: `.env` (项目根目录，不提交)
- 示例配置: `.env.example`
- 配置文件: 各子项目的 `pyproject.toml`
- 各子项目从项目根目录的 `.env` 加载配置

## 数据目录

所有动态生成的数据存放在项目根目录的 `data/` 下：

```
data/
├── provider/             # FastAPI 产生的数据
│   ├── app.db
│   └── uploads/
├── cli/                  # CLI 产生的输出
│   └── notes/
└── shared/               # 跨项目共享的临时数据
```

- 该目录**不会被提交到 Git**，可安全删除
- 首次运行应用时会自动创建所需子目录

## 开发者文档

文档位于 `docs/dev/` 目录：

| 文件 | 内容 |
|------|------|
| [index.md](../docs/dev/index.md) | 主开发文档：产品愿景、版本目标、核心流程、技术选型 |
| [meta.md](../docs/dev/meta.md) | Meta 模块设计 |
| [collector.md](../docs/dev/collector.md) | Collector 收集器设计 |

### 新增模块文档

1. 在 `docs/dev/` 下创建 `{module}.md`
2. 在 `docs/dev/README.md` 的文件划分表添加链接
3. 在 `docs/dev/index.md` 末尾添加引用链接

## 用户文档

文档位于 `docs/user/` 目录。编写用户文档时要注意介绍最佳实践，帮助用户正确使用功能。

| 文件 | 内容 |
|------|------|
| [index.md](../docs/user/index.md) | 用户指南：快速开始、命令使用 |
| [workspace.md](../docs/user/workspace.md) | Workspace 最佳实践 |

## 规范文档

`docs/spec/` 存放工程标准文件——在开发过程中发现的稳定的、可以长期维护的、具备跨项目价值的核心概念。

例如：认知工程领域的 Collector（收集器）是跨项目可复用的核心概念。

| 文件 | 内容 |
|------|------|
| 待补充 | - |

## 版本发布

项目处于探索期 (0.0.x)，有新价值即发布。

### 版本号规范

- 探索期：0.0.x（如 0.0.1, 0.0.2）
- 验证期：0.x.y
- 发布期：x.y.z

### 发布流程

```bash
# 1. 更新 CHANGELOG.md
# 2. 提交 CHANGELOG
git add CHANGELOG.md && git commit -m "chore: 更新 CHANGELOG 0.0.1"

# 3. 创建 annotated tag（格式：0.0.1，不带 v 前缀）
git tag -a 0.0.1 -m "版本说明"

# 4. 推送代码和 tag
git push && git push origin 0.0.1

# 5. 创建 GitHub Release（标题格式：v0.0.1，带 v 前缀）
gh release create 0.0.1 --title "v0.0.1" --notes-file CHANGELOG.md
```

### CHANGELOG 规范

遵循 [Keep a Changelog](https://keepachangelog.com/) 格式：
- 标题：版本号 + 日期
- 分类：Added, Changed, Deprecated, Removed, Fixed, Security
- 仅记录用户可见的变化
