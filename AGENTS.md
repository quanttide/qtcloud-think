# AGENTS.md - qtcloud-think 开发指南

## 项目概览

- **名称**: qtcloud-think (量潮思考云)
- **类型**: "思维外脑" - 思维收集与澄清工具
- **状态**: MVP 验证阶段

## 开发者文档入口

**每次开发前查阅**: [docs/dev/index.md](docs/dev/index.md)

---

## 项目结构

多语言 Monorepo 结构，按功能/领域组织代码：

```
src/
├── cli/           # CLI 工具 (Python + Typer)
├── provider/      # FastAPI 后端服务
└── studio/        # Flutter 桌面/移动端

packages/          # 公共库集合（多语言）
                   # 每个子目录是一个独立的库，供 src/ 下的应用消费

scripts/           # 项目级自动化脚本（如部署、数据处理等）
tests/             # 跨项目 E2E 测试（可选）
```

### packages/ 公共库

`packages/` 是共享领域的集中地，包含多个子目录，每个子目录是一个独立的不同语言编写的公共库。例如：
- `packages/shared/` - 共享数据结构和算法
- `packages/api-spec/` - OpenAPI 定义

### src/studio Flutter 规范

- 遵循 Flutter 和 Dart 官方规范
- 使用 `flutter pub` 管理依赖
- 遵循 Dart 风格指南

---

## 环境配置

### 重要原则

**每个子项目独立管理虚拟环境**。虽然技术上可以共用一个虚拟环境，但强烈不建议这么做 —— 尤其当 provider（FastAPI）和 cli 是两个独立的 Python 项目时。

- 依赖版本冲突：不同项目可能需要不同版本的同一库
- 启动方式不同：cli 是命令行入口，provider 是 uvicorn 服务
- 独立演进：各项目可以独立升级依赖而不影响其他项目

**每个子项目独立负责自己的测试**。src/provider 和 src/cli 各自在其目录下管理测试，运行测试时需要进入对应的项目目录。

虽然在顶级目录保留 `tests/` 目录不是必须的，但可以用于跨项目端到端（E2E）测试或系统级集成测试。

`scripts/` 文件夹（项目根目录）用于存放项目级自动化脚本。它的核心作用是：封装复杂、重复或跨项目的操作，让开发者和 CI/CD 只需运行一个命令即可完成任务。

### data/ 动态数据目录

`data/` 用于存放动态生成的数据（如程序运行时产生的文件、临时输出、本地数据库等），而不是静态示例数据。

**重要原则**：
- `data/` 是"易失性"目录——可随时删除重建，绝不提交 Git
- 各子项目通过相对路径安全访问
- 首次运行应用时会自动创建所需子目录

```
data/                     # 动态数据根目录（全部 .gitignore）
├── provider/             # FastAPI 产生的数据
│   ├── app.db            # SQLite 文件
│   └── uploads/          # 用户上传文件（开发用）
├── cli/                  # CLI 产生的输出
│   └── notes/            # 澄清后的笔记
└── shared/               # 跨项目共享的临时数据（谨慎使用）
```

### 通用

```bash
# 安装 uv (如未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**注意**：Windows 系统使用 Unix-like 环境运行脚本（如 Git Bash、WSL 等）。

### CLI 开发

```bash
# 方式一：从项目根目录运行脚本
./scripts/collect

# 方式二：进入 CLI 目录
cd src/cli

# 创建虚拟环境 (在项目目录内)
uv venv

# 安装依赖
uv sync

# 运行
uv run python main.py

# 测试
pytest
pytest tests/test_file.py::TestClass::test_method
pytest tests/test_file.py -k "test_name_pattern"
```

### Provider 开发

```bash
cd src/provider

# 创建虚拟环境
uv venv
source .venv/bin/activate

# 安装依赖
uv sync

# 运行
uv run uvicorn src.provider.main:app --reload
```

---

## 代码规范

### Python
- **格式化**: Black (行长 100)
- **导入排序**: isort
- **类型检查**: mypy
- **Linting**: ruff

```bash
# 在项目目录下运行
black .
isort .
ruff check .
mypy src/
```

### 命名约定
- 文件: `snake_case.py`
- 类: `PascalCase`
- 函数/变量: `snake_case`
- 常量: `UPPER_SNAKE_CASE`
- 布尔值: `is_`, `has_`, `can_`, `should_` 前缀

### 类型提示
- 所有函数签名必须标注类型
- 使用 `| None` 而非 `Optional`

### 错误处理
- 使用具体异常类型
- 包含有意义的错误信息
- 禁止 bare `except:`

### 安全
- 禁止提交 secrets (使用 .env)
- 验证和清理用户输入

### 多语言模型同步

当项目涉及多种编程语言时（如 Python ↔ Dart），需要保持数据模型一致：

- **推荐方案**：使用 OpenAPI/Swagger 定义数据结构，作为单一事实源
- Python Pydantic 模型 ↔ Dart 数据类 通过代码生成保持同步
- 复杂系统建议使用代码生成工具

---

## 配置

- 环境变量: `.env` (项目根目录，不提交)
- 示例配置: `.env.example`
- 配置文件: 各子项目的 `pyproject.toml`

各子项目从项目根目录的 `.env` 加载配置。

---

## 代码审查清单

- [ ] 代码符合命名规范
- [ ] 类型标注正确
- [ ] 错误处理恰当
- [ ] 测试覆盖核心逻辑
- [ ] 无硬编码 secrets
- [ ] 代码可读可维护

---

## 开发复盘

每次开发结束后，复盘经验总结到 AGENTS.md，帮助后续开发者和自动化代理更快上手。

复盘要点：
- 遇到了什么问题？如何解决的？
- 哪些设计决策是对的？哪些需要改进？
- 有没有新增的约定或最佳实践？
- 下一步可以优化什么？
