# 参考借鉴：知识管理实践

本文档记录从 quanttide 组织其他项目（主要是 quanttide-profile-of-founder）学习到的知识管理经验，供 qtcloud-think 参考。

---

## 目录结构设计

参考 quanttide-profile-of-founder 的板块划分：

| 目录 | 含义 | 说明 |
|------|------|------|
| `think/` | 思维 | 核心思考内容 |
| `knowl/` | 知识 | 已沉淀的结构化知识 |
| `learn/` | 学习 | 学习记录与心得 |
| `write/` | 写作 | 写作产出 |
| `code/` | 编程 | 代码相关 |
| `product/` | 产品 | 产品设计 |
| `agent/` | 智能体 | AI Agent 工程 |

qtcloud-think 当前使用 `notes/` 目录，按状态分类（received/rejected/pending），可考虑结合状态 + 主题的双层结构。

---

## 文件命名规范

- 小写字母
- 单词之间用连字符 `-` 分隔
- 示例：`ai-clarify-method.md`、`knowledge-taxonomy.md`

与 qtcloud-think 当前规范一致。

---

## 知识管理方法论

### PARA 方法

Tiago Forte 的 PARA 方法：

- **Projects**: 有明确目标和截止日期的项目
- **Areas**: 持续关注的领域（无截止日期）
- **Resources**: 感兴趣的主题和参考资料
- **Archives**: 归档内容

### 原子事实（Atomic Facts）

将知识拆解为不可再分的事实单元：

```json
{
  "id": "entity-001",
  "fact": " Joined the company as CTO in March 2025",
  "category": "milestone",
  "timestamp": "2025-03-15"
}
```

类别包括：relationship、milestone、status、preference、context

**适用于 qtcloud-think**：用户决策（接收/拒绝/悬疑）本身就是一种原子事实，可结构化存储便于后续分析。

---

## 本地搜索方案

### QMD (Quick Markdown Search)

开源的本地 Markdown 搜索工具，特点：

- **混合搜索**：BM25 + 向量嵌入 + LLM 重排序
- **本地运行**：无需联网，保护隐私
- **MCP 集成**：可作为 AI Agent 的工具

### 适用场景

qtcloud-think 后续可考虑：
1. 基于 QMD 实现思维笔记的语义搜索
2. 利用 MCP 协议让 AI Agent 读取历史思维

---

## 质量检查清单

### Linting

```bash
markdownlint "**/*.md"
```

### 验证清单

- [ ] 所有内部链接指向已存在的文件
- [ ] YAML 文件语法正确
- [ ] 新增文件已添加到文档索引
- [ ] 构建无错误

---

## 许可证参考

quanttide-profile-of-founder 采用 CC BY 4.0 许可证，适合文档类项目。

qtcloud-think 的用户文档和示例内容可参考此许可证。

---

## 相关阅读

- [PARA Method](https://fortelabs.com/blog/para) - Tiago Forte
- [QMD GitHub](https://github.com/tobi/qmd) - 本地 Markdown 搜索
- [Agentic PKM](https://www.techtwitter.com/articles/agentic-personal-knowledge-management-with-openclaw-para-and-qmd) - AI 辅助知识管理实践
