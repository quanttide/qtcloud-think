# AGENTS.md - qtcloud-think 工作记忆

## 项目概览

- **名称**: qtcloud-think (量潮思考云)
- **类型**: "思维外脑" - 思维收集与澄清工具
- **状态**: 探索期 (0.0.x)
- **发布规范**: 探索期(0.0.x)有新价值即发布；验证期(0.x.y)验证团队协作；发布期(x.y.z)市场上线

开发时根据 [ROADMAP](ROADMAP.md) 校准长期目标。

---

## 当前开发

**v0.0.3 目标**: 信息状态分类（接收/拒绝/悬疑）

### 用户决策功能

AI 澄清后用户可选择接收/拒绝/悬疑，分类存储。具体设计见 docs/dev/status.md。

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

### v0.0.4 开发经验

**架构重构：启发者与观察者架构**

1. **智能体分类**
   - 启发者(Sower)：主动思考，围绕上下文选择 CODE 技能
   - 观察者(Observer)：通过客观指标(clarity/completeness/depth/coherence/relevance)与启发者沟通
   - Meta：元认知反思
   - **CODE 是技能(Skill)，不是智能体**

2. **目录结构**
   ```
   src/provider/
   ├── app/
   │   ├── agents/      # 智能体
   │   ├── skills/     # 技能
   │   ├── infrastructure/  # 基础设施(LLM/Storage/Workspace)
   │   └── api/        # API
   └── tests/
   ```

3. **测试经验**
   - 使用 `@patch("skills.xxx.get_client")` mock LLM 调用
   - 未实现的技能返回空字符串 `""`，测试需匹配
   - ExpressSkill 依赖 Storage，需要正确初始化
   - Observer 可选注入，不影响 Sower 独立工作

4. **下一步优化**
   - Observer 评估逻辑需要真实实现
   - Organize/Distill 技能需要实现
   - Exporter 从 Storage 解绑后需要重新设计

---

## 长期记忆

维护这些文件前先阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解相关规范。

| 文件 | 用途 | 何时查阅 |
|------|------|---------|
| [ROADMAP.md](ROADMAP.md) | 版本规划 | 开发前确认目标 |
| [CHANGELOG.md](CHANGELOG.md) | 版本历史 | 发布时更新 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 开发规范 | 贡献代码时 |
| [docs/dev/index.md](docs/dev/index.md) | 设计决策 | 理解架构时 |
