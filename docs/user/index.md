# 用户指南

## 快速开始

```bash
cd src/cli
python app/main.py collect
```

---

## 命令

### collect - 收集思维

```bash
# 使用默认工作空间（default）
python app/main.py collect

# 指定工作空间
python app/main.py collect -w default
python app/main.py collect --workspace meta
```

### meta - 系统自省

```bash
# 触发 Meta 分析
python app/main.py meta

# 分析指定工作空间
python app/main.py meta -w default
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
