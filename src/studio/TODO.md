# QtCloud Think Studio TODO

> 依据：doc/index.md（实施分解）+ ROADMAP.md（最小闭环：感知 + 理解）
> 更新：2026-08-22

## 分解 1：模型 + 仓储（models + repositories）

- [ ] `models/thought.dart`：Thought 模型（id/content/source/status/clarity/facts/feelings/actions/createdAt）
- [ ] `repositories/thought_repository.dart`：想法仓储（本地文件读写）
- [ ] `repositories/clarify_repository.dart`：AI 加工访问（调 provider——判断/澄清/结构化）
- [ ] 测试：thought_test / thought_repository_test / clarify_repository_test（MockClient）

## 分解 2：感知页（perceive_screen）

- [ ] 输入区：文本输入提交（生成 Thought(raw)）
- [ ] 想法流：原始想法时间线列表（时间/来源/内容）
- [ ] 导入素材：quanttide journal 日志导入（选择 → 批量生成想法）
- [ ] 测试：输入提交、时间线渲染、空状态、点击跳转

## 分解 3：理解页（understand_screen）

- [ ] 清晰度区：调 clarify_repository 判断清楚/不清楚 + 用户标记需澄清
- [ ] 澄清区：多轮对话（AI 追问、用户回答）
- [ ] 结构化区：AI 拆解事实/感受/行动 + 用户确认/修改
- [ ] 实例区：结构化完成的想法（情境意识实例）列表呈现
- [ ] 测试：清晰度分支、澄清对话、结构化确认、失败提示

## 分解 4：导航壳（main.dart）

- [ ] 4D 导航骨架（感知/理解启用，预测/决策占位灰显）
- [ ] 移除旧方案（annotation_screen 等）
- [ ] widget 测试：导航切换

## 验收

- [ ] 最小闭环跑通：输入想法 → AI 判断/澄清 → 结构化 → 实例呈现
- [ ] analyze 零问题 + 测试全过 + build web 成功
