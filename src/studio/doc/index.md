# QtCloud Think Studio 模块设计方案

> 更新时间：2026-08-22
> 依据：ROADMAP.md（最小闭环：感知 + 理解）+ data/roadmap/qtcloud-think/studio.md

## 定位

思维外脑的交互端——按 4D 认知过程（感知 → 理解 → 预测 → 决策）组织。当前最小闭环只做前两环：感知（收集想法）+ 理解（AI 加工 + 澄清）。

## 模块结构

```
lib/
├── main.dart                  # 应用壳 + 导航（4D 概念，当前启用感知/理解两环）
├── domain/
│   ├── thought.dart           # 想法模型（原始/加工中/实例三态）
│   └── thought_store.dart     # 仓储接口（ThoughtStore 抽象，DDD Repository）
├── infrastructure/
│   └── local_thought_store.dart # 仓储实现（本地文件，可换 OSS/DB）
├── screens/
│   ├── perceive_screen.dart   # 感知页：想法输入 + 想法流时间线 + 导入素材
│   └── understand_screen.dart # 理解页：清晰度判断 → 澄清对话 → 加工结构化 → 实例
└── services/
    └── clarify_service.dart   # AI 加工服务（清晰度判断/澄清/结构化，调 provider）
```

## 数据模型

```
Thought（想法——情境意识实例的原料）
├── id
├── content        # 原始内容
├── source         # 来源（手输 / journal 导入）
├── status         # raw（原始）| clarifying（澄清中）| structured（已加工）
├── clarity        # 清晰度（clear / unclear，AI 判断）
├── facts/feelings/actions   # 加工产物（结构化后）
└── createdAt
```

加工完成（structured）即形成**情境意识实例**——无独立"升级"动作。

## 页面模块

### 感知页（perceive_screen）

- **输入区**：文本输入（零门槛，想到就记）
- **想法流**：原始想法时间线（时间/来源/内容）
- **导入**：quanttide journal 日志导入（选择日志 → 批量生成想法）

### 理解页（understand_screen）

- **清晰度区**：AI 判断每个想法 清楚/不清楚；用户标记需澄清
- **澄清区**：模糊想法多轮对话（AI 追问、用户回答）
- **结构化区**：AI 拆解 事实/感受/行动 清单；用户确认/修改
- **实例区**：加工完成的想法（情境意识实例）列表

## 数据流

```
感知页（输入/导入）→ Thought(raw)
    ↓
理解页 → AI 判断清晰度（services/clarify_service）
    ├── 清楚 → 直接结构化
    └── 不清楚 → 澄清对话 → 结构化
    ↓ 用户确认/修改
Thought(structured) = 情境意识实例 → 实例区呈现
```

## 依赖

- `http`（现有）——调 provider（AI 加工）
- 数据存储：本地文件（独立数据层，不依赖 CLI）
- 后续（延迟验证）：预测页/决策页按验证标准决定后接入

## 实施顺序

1. models/thought.dart + data/thought_store.dart（数据层）
2. 感知页（输入 + 时间线）
3. 理解页（清晰度 + 澄清 + 结构化 + 实例）
4. 真实使用 1-2 周 → 验证 → 决定预测/决策页

## 实施分解

### 分解 1：领域层 + 基础设施层（domain + infrastructure）

- [ ] `domain/thought.dart`：Thought 模型（id/content/source/status/clarity/facts/feelings/actions/createdAt）
- [ ] `domain/thought_store.dart`：ThoughtStore 仓储接口（抽象）
- [ ] `infrastructure/local_thought_store.dart`：本地文件实现（读写想法列表）
- [ ] 单元测试：Thought 序列化、仓储读写

### 分解 2：感知页（perceive_screen）

- [ ] 输入区：文本输入提交（生成 Thought(raw)）
- [ ] 想法流：原始想法时间线列表（时间/来源/内容）
- [ ] 导入素材：quanttide journal 日志导入（选择 → 批量生成想法）
- [ ] 测试：输入提交、时间线渲染

### 分解 3：理解页（understand_screen）

- [ ] 清晰度区：调 services/clarify_service 判断清楚/不清楚 + 用户标记需澄清
- [ ] 澄清区：多轮对话（AI 追问、用户回答）
- [ ] 结构化区：AI 拆解事实/感受/行动 + 用户确认/修改
- [ ] 实例区：结构化完成的想法（情境意识实例）列表呈现
- [ ] 测试：清晰度展示、澄清对话、结构化确认

### 分解 4：导航壳（main.dart）

- [ ] 4D 导航骨架（感知/理解启用，预测/决策占位灰显）
- [ ] 移除旧方案（annotation_screen 等）
- [ ] widget 测试：导航切换

### 验收

- 最小闭环跑通：输入想法 → AI 判断/澄清 → 结构化 → 实例呈现
- analyze 零问题 + 测试全过 + build web 成功
