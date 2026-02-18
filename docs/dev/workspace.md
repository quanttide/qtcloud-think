# Workspace 设计

## 概念

Workspace（工作空间）是一个数据隔离单元，每个 Workspace 有独立的数据存储，互不干扰。

## 使用场景

| Workspace | 用途 |
|-----------|------|
| `personal` | 个人思维笔记 |
| `meta` | 系统自省数据 |
| `department:engineering` | 工程部数据 |
| `department:marketing` | 市场部数据 |

## 核心流程

```
用户输入 → 选择 Workspace → 路由到对应存储 → 处理 → 保存
```

## 数据结构

```
data/
├── personal/           # personal workspace
│   └── notes/
├── meta/               # meta workspace
│   └── 2026-02-18.md
├── engineering/        # department workspace
│   └── notes/
└── marketing/
    └── notes/
```

## 接口设计

```python
class Workspace:
    def __init__(self, name: str):
        self.name = name
        self.root = Path(f"data/{name}")

    def get_notes_dir(self) -> Path:
        return self.root / "notes"

    def save_note(self, content: str) -> Path:
        # 保存到对应 workspace 目录

    def list_notes(self) -> list[Path]:
        # 列出当前 workspace 下的笔记
```

## CLI 使用

```bash
# 指定 workspace
qtcloud collect --workspace personal
qtcloud collect --workspace meta
qtcloud collect --workspace engineering

# 默认使用 personal
qtcloud collect
```

## 配置

在 `.env` 中指定默认 Workspace：

```bash
DEFAULT_WORKSPACE=personal
```
