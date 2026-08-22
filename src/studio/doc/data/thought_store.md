# 想法存储设计（data/thought_store.dart）

## 定位

想法的本地数据层——独立管理数据（不依赖 CLI），文件即数据。

## 存储方案

```
数据根：~/.qtcloud-think/（可被 QTCLOUD_THINK_DATA 环境变量覆盖）
└── thoughts.json      # 全部想法（Thought 列表，JSON）
```

- 单文件 JSON（想法量级小，简单优先）
- 每次变更全量写（原子写：临时文件 + rename）

## 接口

```
ThoughtStore
├── load() → List<Thought>          # 启动加载
├── add(Thought)                    # 新增想法
├── update(Thought)                 # 更新（状态/清晰度/结构化）
├── remove(String id)               # 删除
├── byStatus(ThoughtStatus) → List  # 按状态过滤（raw/structured…）
└── save()                          # 持久化
```

## 并发/一致性

- 单进程单写者（studio 本地使用）
- 原子写防损坏（临时文件 + rename）
- 加载失败 → 返回空列表（不崩溃，下次写入重建）

## 验收

- 写入 → 重启后读回一致
- 状态过滤正确（raw/structured 分组）
- 原子写：写入中断不损坏已有数据
