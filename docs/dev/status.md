# 信息状态设计

## 概念

AI 澄清后的输出需经过用户决策才能沉淀，确保只有用户认可的内容进入长期记忆。

---

## 状态定义

| 状态 | 含义 | 存储位置 | 用户操作 |
|------|------|----------|----------|
| 接收 | 认可澄清结果，存入长期记忆 | `notes/received/` | 确认保存 |
| 拒绝 | 不认可，可选择填写原因 | `notes/rejected/` | 选择性填写原因 |
| 悬疑 | 暂时无法判断，暂存待定 | `notes/pending/` | 直接暂存 |

---

## 交互流程

```
Clarifier 澄清结果
       ↓
展示内容给用户
       ↓
请选择：[1]接收 [2]拒绝 [3]悬疑
       ↓
  ┌────┼────┐
  ↓    ↓    ↓
接收  拒绝  悬疑
  ↓    ↓    ↓
存入   存入  存入
received/ rejected/ pending/
```

---

## 文件命名

使用 UUID 命名，确保唯一性：

```
notes/
├── received/
│   └── {uuid}.md
├── rejected/
│   └── {uuid}.md    # 可选在 frontmatter 记录拒绝原因
└── pending/
    └── {uuid}.md
```

---

## Frontmatter 字段

```yaml
---
id: {uuid}
created: {isoformat}
status: received | pending | rejected
summary: "一句话概括"
original: "原始输入"
rejection_reason: "拒绝原因（可选）"
---
```

---

## Pending 召回

悬疑内容通过命令召回：

```bash
# 列出所有 pending 内容
python main.py pending

# 交互式处理每条 pending
python main.py review
```

召回后可重新决策：接收、拒绝、或继续保留在 pending。

---

## 设计理由

1. **用户主导**：AI 输出一律不自动沉淀，必须用户确认
2. **拒绝可选原因**：避免强制询问导致反感
3. **UUID 命名**：避免文件名冲突，简化召回逻辑
