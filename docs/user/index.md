# 用户指南

## 快速开始

```bash
# 使用 scripts（推荐）
./scripts/collect

# 或直接运行
cd src/cli
uv run python app/main.py collect
```

---

## 命令

### collect - 收集思维

```bash
# 使用 scripts
./scripts/collect
./scripts/collect -w meta

# 或直接运行
cd src/cli
uv run python app/main.py collect
uv run python app/main.py collect -w meta
```

### meta - 系统自省

```bash
# 触发 Meta 分析
./scripts/collect meta
./scripts/collect meta -w default

# 或直接运行
cd src/cli
uv run python app/main.py meta
uv run python app/main.py meta -w default
```

---

## 工作空间

工作空间用于隔离不同类型的数据。

| 工作空间 | 用途 |
|---------|------|
| `default` | 个人思维笔记（默认） |
| `meta` | 系统自省数据 |

---

## 数据存储

数据保存在项目根目录的 `data/` 下：

```
data/
├── default/           # 个人思维笔记
│   └── notes/
└── meta/              # 系统自省报告
```
