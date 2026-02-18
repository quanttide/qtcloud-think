# 用户指南

## 快速开始

```bash
# 收集思维（推荐）
./scripts/collect

# 查看待定内容
./scripts/collect pending
./scripts/collect pending -w meta

# 审查待定内容
./scripts/collect review
./scripts/collect review -w meta

# 触发 Meta 自省
./scripts/collect meta
./scripts/collect meta -w meta
```

---

## 思维收集流程

当你运行 `collect` 命令时，会经历以下步骤：

1. **输入想法** - 输入你的原始想法
2. **AI 澄清** - AI 会分析并帮助你澄清想法
3. **决策分类** - 澄清完成后，选择处理方式

### 决策分类

| 状态 | 含义 | 后续操作 |
|------|------|----------|
| 接收 | 认可澄清结果，存入长期记忆 | 自动保存到 `notes/received/` |
| 拒绝 | 不认可，可选择填写原因 | 保存到 `notes/rejected/` |
| 悬疑 | 暂时无法判断，暂存待定 | 保存到 `notes/pending/` |

---

## 命令

### collect - 收集思维

```bash
# 使用 scripts（推荐）
./scripts/collect
./scripts/collect -w meta
```

### pending - 查看待定内容

```bash
# 列出所有悬疑待定的内容
./scripts/collect pending
./scripts/collect pending -w meta
```

### review - 审查待定内容

```bash
# 交互式审查待定内容，重新决策
./scripts/collect review
./scripts/collect review -w meta
```

审查时可选择：
- **接收** - 移至长期记忆
- **拒绝** - 丢弃（可填写原因）
- **跳过** - 保留在待定

### meta - 系统自省

```bash
# 触发 Meta 分析
./scripts/collect meta
./scripts/collect meta -w default
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
│   ├── notes/
│   │   ├── received/   # 已接收
│   │   ├── rejected/   # 已拒绝
│   │   └── pending/    # 待定
│   └── sessions/
└── meta/              # 系统自省报告
```
