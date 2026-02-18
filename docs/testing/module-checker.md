# 模块检查器设计

## 定位

使用 LLM 分析模块语义，帮助理解模块职责和依赖关系。

## 检查功能

| 功能 | 说明 |
|------|------|
| 职责分析 | LLM 为每个模块生成一句话职责描述 |
| 依赖关系 | 分析模块间的 import 依赖 |
| 重复检测 | 检查是否有功能重复的模块 |
| 问题预警 | 标记职责边界模糊、耦合过高等问题 |

## 使用方式

```bash
python tests/test_module_checker.py
```

## 输出示例

```
📦 模块地图

├── clarifier (→ llm_client, storage)
│   └── 该模块通过 LLM 评估用户输入的清晰度...

├── main (→ clarifier, session_recorder, meta, storage)
│   └── 该模块实现了一个命令行思维收集与澄清工具...

⚠️ 发现问题:
  - main 模块与 clarifier 模块在'多轮对话澄清逻辑'上存在职责耦合风险
```
