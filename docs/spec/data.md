# 数据工程标准

本文件定义数据管理相关概念，属于**数据工程**类别。

---

## Workspace（工作空间）

Workspace（工作空间）是一个数据隔离单元，每个 Workspace 有独立的数据存储，互不干扰。

- **类型**：领域实体（Domain Entity）
- **用途**：隔离不同用途的数据

### 工作空间

| Workspace | 用途 |
|-----------|------|
| `default` | 个人思维笔记（默认） |
| `meta` | 系统自省数据 |

### 数据结构

```
data/
├── default/            # default workspace
│   ├── notes/
│   └── meta/
└── meta/               # meta workspace
    ├── notes/
    └── meta/
```
