# 想法仓储设计（data/thought_store.dart）

## 定位

领域驱动设计的**仓储层（Repository）**——封装想法数据访问，隔离领域层与基础设施层。领域层依赖 `ThoughtStore` 接口，不依赖存储实现。

## 仓储接口（领域层依赖）

```
ThoughtStore（抽象）
├── load() → List<Thought>          # 启动加载
├── add(Thought)                    # 新增想法
├── update(Thought)                 # 更新（状态/清晰度/结构化）
├── remove(String id)               # 删除
├── byStatus(ThoughtStatus) → List  # 按状态过滤（raw/structured…）
└── save()                          # 持久化
```

## 实现（基础设施层）

```
LocalFileThoughtStore implements ThoughtStore
└── 本地文件：~/.qtcloud-think/thoughts.json
    （QTCLOUD_THINK_DATA 环境变量可覆盖；未来可换 OSS/DB 实现）
```

- 单文件 JSON（想法量级小，简单优先）
- 每次变更全量写（原子写：临时文件 + rename）

## 种子数据（示例，非仓储概念）

种子（演示想法/示例日志）在 `src/studio/assets/data/`（git 跟踪）——加载时作为初始数据源（可区分来源），与仓储接口无关。

## 并发/一致性

- 单进程单写者（studio 本地使用）
- 原子写防损坏（临时文件 + rename）
- 加载失败 → 返回空列表（不崩溃，下次写入重建）

## 验收

- 写入 → 重启后读回一致
- 状态过滤正确（raw/structured 分组）
- 原子写：写入中断不损坏已有数据
