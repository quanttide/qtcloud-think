# 开发计划：思维外脑 v0.0.x

## 产品愿景

当人类处于默认神经网络状态时，帮助人类承载需要切换到任务正向网络的任务，使人类可以专注于放松。

核心功能：收集人类思维流，澄清想法念头，记录清晰的知识结构。

---

## 版本目标

### v0.0.1 - 2026-02-18 ✓
- CLI 思维收集与澄清工具原型
- `scripts/collect` 脚本支持从项目根目录运行 CLI
- `data/` 动态数据目录约定
- 开发指南文档 (AGENTS.md)

### v0.0.2 - [开发中]
- **目标**: 增加 meta 模块
- **功能**: 观察自己并提出对自己的修改意见（自我反思与改进建议）

### v0.0.2 开发计划

#### 2.1 SessionRecorder 组件

在澄清流程中收集数据，供 Meta 使用。

```
src/cli/
├── session_recorder.py  # 新增：会话数据收集
```

数据维度：
- 对话轮次、耗时
- 首轮意图是否抓住核心
- 存储是否成功
- 用户是否中断
- API 调用次数
- 错误记录

#### 2.2 Collector 改造

修改 `collector.py`，使 `run()` 方法返回 `(Note, SessionRecord)`。

#### 2.3 Meta 分析器

```
src/cli/
├── meta.py  # 新增：Meta 自省分析
```

功能：
- 接收 SessionRecord
- 分析各维度数据是否异常
- 生成改进建议
- 输出到 `data/cli/meta/{date}.md`

#### 2.4 CLI 集成

在 `main.py` 中，将 Meta 集成到收集流程末尾：

```
collect 命令流程：
1. Collector.run(input) → (Note, SessionRecord)
2. Meta.analyze(SessionRecord)
3. 输出笔记路径 + Meta 建议
```

---

### Phase 3：前端界面（可选）

- Web 界面或桌面端
- 提升交互体验

---

## 运行方式

```bash
cd src/cli
pip install -r requirements.txt
python main.py collect
```

---

## 验证指标

- **转化率**：多少输入最终被成功存储？
- **澄清轮数**：平均几轮对话能澄清一个想法？
- **召回测试**：存储后的笔记能否被语义搜索召回？
- **用户主观**：事后看澄清后的内容，是否比原始输入更清晰？

---

## 下一步

- [ ] 实现 SessionRecorder 组件
- [ ] 改造 Collector 返回 SessionRecord
- [ ] 实现 Meta 分析器
- [ ] CLI 集成 Meta

---

## 运行测试

```bash
cd src/cli
uv run python -m pytest tests/
```

## 已知架构问题

### main 模块耦合风险

**问题 1**：main 与 session_recorder 职责耦合
- main 负责多轮问答引导并记录过程
- session_recorder 专门追踪交互轮次
- **状态**：目前合理，main 作为协调者调用 session_recorder

**问题 2**：main 与 storage 边界模糊
- main 提到"保存元数据"
- storage 负责文件持久化
- **状态**：需明确 main 仅调用 storage 而非自行处理

---

详见 [Meta 模块设计](./meta.md)

详见 [Collector 收集器设计](./collector.md)
