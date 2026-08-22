# Thought 模型设计（models/thought.dart）

## 定位

想法的领域模型——从原始输入到情境意识实例的唯一载体（三态流转）。

## 模型定义

```
Thought
├── id            # 唯一标识
├── content       # 原始内容（用户输入/日志片段）
├── source        # 来源：manual（手输）/ journal（日志导入）
├── status        # raw（原始）| clarifying（澄清中）| structured（已加工）
├── clarity       # 清晰度：clear / unclear（AI 判断，可空）
├── facts         # 事实清单（结构化产物）
├── feelings      # 感受清单（结构化产物）
├── actions       # 行动清单（结构化产物）
├── clarifyLog    # 澄清对话记录（AI/用户 交替，List<(speaker, text)>）
└── createdAt     # 创建时间
```

## 状态流转

```
raw（感知页输入）
  ↓ AI 判断清晰度
clarifying（不清楚 → 澄清对话）
  ↓ 澄清完成
structured（加工完成 = 情境意识实例）★
```

- 状态只前进不后退（raw → clarifying → structured）
- **structured 即情境意识实例**——无独立"升级"动作

## 序列化

- JSON 序列化/反序列化（toJson/fromJson，全字段）
- 存本地文件（thought_store 使用）

## 验收

- 三态流转正确（raw → clarifying → structured）
- JSON 往返无损（含澄清记录）
- 字段类型明确（clarity 可空、清单默认空）
