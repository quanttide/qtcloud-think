# Workspace 设计

## 概念

Workspace（工作空间）是一个数据隔离单元，每个 Workspace 有独立的数据存储，互不干扰。

## 使用场景

| Workspace | 用途 |
|-----------|------|
| `default` | 个人思维笔记（默认） |
| `meta` | 系统自省数据 |

## 数据结构

```
data/
├── default/            # default workspace
│   ├── notes/
│   │   ├── received/   # 接收的笔记
│   │   ├── pending/    # 悬疑待定
│   │   └── rejected/  # 拒绝的笔记
│   └── sessions/      # 会话记录
└── meta/              # meta workspace（系统自省）
```

详见 [信息状态设计](./status.md)。

## 实现

```python
# src/cli/workspace.py
class Workspace:
    DEFAULT = "default"

    def __init__(self, name: str | None = None):
        self.name = name or os.getenv("DEFAULT_WORKSPACE", self.DEFAULT)
        self.root = Path("data") / self.name

    def get_notes_dir(self) -> Path:
        return self.root / "notes"

    def get_meta_dir(self) -> Path:
        return self.root / "meta"
```

## CLI 使用

```bash
# 指定 workspace（默认 default）
python main.py collect                    # default
python main.py collect --workspace meta   # meta

# 简写
python main.py collect -w default
python main.py collect -w meta
```

## 配置

在 `.env` 中指定默认 Workspace：

```bash
DEFAULT_WORKSPACE=default
```
