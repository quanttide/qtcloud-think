# AI 加工访问设计（repositories/clarify_repository.dart）

## 定位

理解页的 AI 能力封装——清晰度判断、澄清对话、结构化拆解（调 provider）。

## 接口

```
ClarifyRepository
├── judgeClarity(Thought) → ClarityResult
│     # AI 判断想法清楚/不清楚（+ 简要理由）
├── clarify(Thought, String userReply) → ClarifyReply
│     # 澄清对话：AI 基于想法+历史追问/总结
├── structure(Thought) → StructureResult
│     # 拆解 事实/感受/行动 三清单（AI 草稿，用户确认）
└── (待 provider 就绪) — 失败降级
```

## 数据契约

```
ClarityResult: { clarity: clear|unclear, reason: String }
ClarifyReply:  { text: String, done: bool }        # done=澄清完成可结构化
StructureResult: { facts: [String], feelings: [String], actions: [String] }
```

## 实现要点

- 调 provider（http 现有依赖）——AI 加工接口（**数据访问，属仓储层**）
- **失败降级**：AI 不可用时——清晰度默认 unclear？不——降级为"跳过 AI，直接结构化"？——设计决策：AI 失败 → 提示用户，想法保持 raw（不造假结果）
- 超时处理（AI 慢 → 加载态 + 可取消）

## 验收

- 三接口调用正确（judge/clarify/structure 契约对齐）
- AI 失败 → 明确提示，不产生假结果
- 澄清多轮上下文正确传递（clarifyLog 追加）
