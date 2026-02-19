# Organizer 设计（联想）

## 概念

Organizer 是 CODE 循环中的 O 阶段，负责分析已接收的想法，寻找其中的联系，帮助用户发现潜在的关联和洞察。

---

## 核心职责

1. **读取已接收的想法**：从 `notes/received/` 读取所有笔记
2. **分析关联**：使用 LLM 分析想法之间的联系
3. **展示结果**：以可读方式展示关联（列表或简单可视化）
4. **Meta 反思**：观察联想过程，提出改进建议

---

## 交互流程

```
用户执行 organize 命令
        ↓
读取所有 received 笔记
        ↓
使用 LLM 分析关联
        ↓
展示分析结果
        ↓
询问用户是否执行 meta 反思
```

---

## 命令设计

```bash
# 基础：列出所有已接收想法的关联
python main.py organize

# 指定工作空间
python main.py organize --workspace default

# 仅展示想法列表（不做分析）
python main.py organize --list-only
```

---

## 输出格式

### 关联展示

```
📚 想法关联分析

主题 A
  - 想法 1 (id: xxx)
  - 想法 2 (id: xxx)

主题 B
  - 想法 3 (id: xxx)
  - 想法 4 (id: xxx)

独立想法
  - 想法 5 (id: xxx)
```

### 详细分析

每个关联附带 LLM 生成的简要说明：
- 为什么这些想法相关
- 可能的洞察或行动建议

---

## 实现要点

### 1. Storage 扩展

- 新增 `list_received()` 方法
- 支持按时间/主题排序

### 2. Organizer 模块

```python
class Organizer:
    def __init__(self, storage: Storage, llm: LLMClient):
        ...

    def organize(self, workspace: str) -> list[Association]:
        """执行联想分析"""
        notes = self.storage.list_received(workspace)
        associations = self.llm.analyze_relations(notes)
        return associations

    def meta_review(self, associations: list[Association]) -> str:
        """Meta 反思：观察联想过程"""
        ...
```

### 3. LLM 分析提示词

提示词应引导 AI：
- 识别共同主题
- 发现因果关系
- 找出相似或对立的观点
- 提出有价值的洞察

---

## 设计理由

1. **先 Clarify 再 Organize**：确保想法经过用户认可后再分析
2. **简单优先**：初期用列表展示关联，避免复杂可视化
3. **可选项**：用户可选择只列出想法，不做分析
4. **Meta 内置**：保持观察自身的好习惯

---

## 待定功能（v0.0.x 后）

- 可视图展示（需要前端支持）
- 手动指定关联
- 导出为知识图谱
- 定时自动分析
