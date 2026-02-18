# AGENTS.md - qtcloud-think 工作记忆

## 项目概览

- **名称**: qtcloud-think (量潮思考云)
- **类型**: "思维外脑" - 思维收集与澄清工具
- **状态**: 探索期 (0.0.x)
- **发布规范**: 探索期(0.0.x)有新价值即发布；验证期(0.x.y)验证团队协作；发布期(x.y.z)市场上线

开发时根据 [ROADMAP](ROADMAP.md) 校准长期目标。

---

## 当前开发

**v0.0.2 目标**: 增加 meta 模块（自我反思与改进建议）

### 快速命令

```bash
# CLI 开发
cd src/cli
uv run python main.py

# 测试
pytest tests/test_file.py::TestClass::test_method
pytest tests/ -k "pattern"

# Lint & Typecheck（项目根目录运行）
cd src/cli && uv pip install black ruff mypy
cd src/cli && python -m black . && python -m ruff check . --fix && python -m mypy .
```

---

## 代码审查清单

- [ ] 代码符合命名规范
- [ ] 类型标注正确完整
- [ ] 导入排序正确
- [ ] 错误处理恰当（无 bare except）
- [ ] 测试覆盖核心逻辑
- [ ] 无硬编码 secrets
- [ ] Black/isort/ruff/mypy 检查通过

---

## 开发复盘

每次开发结束后，复盘经验总结到 AGENTS.md，帮助后续开发者和自动化代理更快上手。

复盘要点：
- 遇到了什么问题？如何解决的？
- 哪些设计决策是对的？哪些需要改进？
- 有没有新增的约定或最佳实践？
- 下一步可以优化什么？

---

## 长期记忆

维护这些文件前先阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解相关规范。

| 文件 | 用途 | 何时查阅 |
|------|------|---------|
| [ROADMAP.md](ROADMAP.md) | 版本规划 | 开发前确认目标 |
| [CHANGELOG.md](CHANGELOG.md) | 版本历史 | 发布时更新 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 开发规范 | 贡献代码时 |
| [docs/dev/index.md](docs/dev/index.md) | 设计决策 | 理解架构时 |
