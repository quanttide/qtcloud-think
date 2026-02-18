# 测试指南

本目录收录测试相关文档。

## 目录结构

| 文件 | 内容 |
|------|------|
| [index.md](./index.md) | 测试概览与规范 |
| [module-checker.md](./module-checker.md) | 模块检查器设计文档 |

---

## 测试类型

| 类型 | 说明 |
|------|------|
| 单元测试 | 测试单个函数/类 |
| 集成测试 | 测试模块间协作 |
| 质量检查 | 代码规范检查（lint、命名等） |

---

## 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_module_checker.py

# 运行质量检查
cd src/cli && python -m black . && python -m ruff check . --fix
```
