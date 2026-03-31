# TUI 实现设计文档

## 1. 概述

### 1.1 设计目标
基于现有CLI架构，设计文本用户界面(TUI)以提供更直观的思维管理体验。TUI将作为CLI的增强层，保留所有现有功能，同时提供可视化交互界面。

### 1.2 核心价值
- **降低认知负荷**：可视化展示思维容器和状态
- **提升操作效率**：快捷键和直观界面减少操作步骤
- **增强关联发现**：可视化展示想法之间的关联关系
- **保持轻量级**：终端环境下的高效渲染

## 2. 技术选型

### 2.1 TUI框架选择
**推荐：Textual**
- 基于Rich的现代TUI框架
- 支持CSS-like样式定义
- 组件化架构，易于扩展
- 良好的事件处理机制
- 活跃的社区和文档

### 2.2 备选方案
- **Rich**：轻量级，适合简单界面
- **Urwid**：成熟稳定，但学习曲线较陡
- **Prompt Toolkit**：适合交互式命令行

### 2.3 依赖管理
```toml
# pyproject.toml
[project.optional-dependencies]
tui = ["textual>=0.40.0", "rich>=13.0.0"]
```

## 3. 架构设计

### 3.1 整体架构
```
src/cli/
├── app/
│   ├── tui/                    # TUI模块
│   │   ├── __init__.py
│   │   ├── app.py             # 主应用类
│   │   ├── screens/           # 界面屏幕
│   │   │   ├── __init__.py
│   │   │   ├── main.py        # 主界面
│   │   │   ├── collect.py     # 想法收集界面
│   │   │   ├── review.py      # 审查界面
│   │   │   └── settings.py    # 设置界面
│   │   ├── widgets/           # 自定义组件
│   │   │   ├── __init__.py
│   │   │   ├── note_card.py   # 想法卡片组件
│   │   │   ├── chat_bubble.py # 对话气泡组件
│   │   │   └── status_badge.py # 状态标签组件
│   │   └── utils/             # 工具函数
│   │       ├── __init__.py
│   │       └── theme.py       # 主题配置
│   └── ...existing files...
```

### 3.2 核心组件
1. **ThinkTUI**：主应用类，管理全局状态和导航
2. **Screen**：界面屏幕基类，处理特定功能流程
3. **Widget**：可复用UI组件，如想法卡片、对话气泡
4. **DataManager**：数据管理器，与现有Storage/Workspace集成

## 4. 界面设计

### 4.1 主界面布局
```
┌─────────────────────────────────────────────────────┐
│ 量潮思考云 v0.0.3                     [设置] [帮助] │
├─────────────────────────────────────────────────────┤
│ [收集] [审查] [关联] [沉淀] [设置]                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  最近想法                                           │
│  ┌─────────────────────────────────────────────┐   │
│  │ 想法1: 如何设计思维容器... [接收] [悬疑]     │   │
│  ├─────────────────────────────────────────────┤   │
│  │ 想法2: AI时代创造者身份... [接收] [悬疑]     │   │
│  ├─────────────────────────────────────────────┤   │
│  │ 想法3: 知识架构迭代... [悬疑] [拒绝]         │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  快捷操作                                           │
│  [C] 新想法 [R] 审查 [S] 搜索 [Q] 退出             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 4.2 收集界面布局
```
┌─────────────────────────────────────────────────────┐
│ 收集新想法                                   [返回] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  输入你的想法：                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │                                             │   │
│  │                                             │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  [提交] [取消]                                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 4.3 澄清对话界面
```
┌─────────────────────────────────────────────────────┐
│ 澄清对话                                    [返回] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  用户：如何设计思维容器的原子定义？                 │
│                                                     │
│  AI：让我复述一下你的想法...                        │
│  你关心的是思维容器的基本组成要素，对吗？           │
│                                                     │
│  [1.补充信息] [2.结束澄清] [3.换一个说法]           │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │ 补充你的想法...                             │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 5. 数据流设计

### 5.1 数据模型扩展
```python
# models.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class NoteStatus(str, Enum):
    RECEIVED = "received"
    REJECTED = "rejected"
    PENDING = "pending"

class RelationType(str, Enum):
    PARENT_CHILD = "parent_child"
    REFERENCE = "reference"
    CONTRADICTION = "contradiction"
    EVOLUTION = "evolution"

@dataclass
class ThoughtAtom:
    """想法原子定义"""
    id: str
    content: str
    summary: str
    original: str
    status: NoteStatus
    created_at: datetime
    updated_at: datetime
    source: str
    identity: str
    rejection_reason: Optional[str] = None

@dataclass
class ThoughtRelation:
    """想法关联关系"""
    source_id: str
    target_id: str
    relation_type: RelationType
    strength: float  # 关联强度 0-1
    created_at: datetime
    description: Optional[str] = None

@dataclass
class ThoughtContainer:
    """思维容器"""
    id: str
    atoms: list[ThoughtAtom]
    relations: list[ThoughtRelation]
    created_at: datetime
    updated_at: datetime
```

### 5.2 数据流
1. **用户输入** → TUI收集界面 → 数据验证 → 创建ThoughtAtom
2. **澄清对话** → 与AI交互 → 更新ThoughtAtom内容
3. **状态决策** → 用户选择 → 更新ThoughtAtom状态
4. **关联发现** → 分析内容 → 创建ThoughtRelation
5. **持久化** → 调用现有Storage → 保存到文件系统

## 6. 交互设计

### 6.1 快捷键映射
| 快捷键 | 功能 | 上下文 |
|--------|------|--------|
| `C` | 新想法 | 主界面 |
| `R` | 审查待定 | 主界面 |
| `S` | 搜索 | 主界面 |
| `Q` | 退出 | 任何界面 |
| `Enter` | 确认/选择 | 表单/列表 |
| `Esc` | 返回/取消 | 任何界面 |
| `Tab` | 切换焦点 | 表单 |
| `↑/↓` | 导航 | 列表 |

### 6.2 用户流程
1. **新想法流程**：主界面 → 收集界面 → 输入想法 → 澄清对话 → 状态决策 → 保存
2. **审查流程**：主界面 → 审查界面 → 选择待定想法 → 重新决策 → 更新状态
3. **关联流程**：主界面 → 关联界面 → 选择想法 → 查看关联 → 创建新关联

## 7. 集成方案

### 7.1 与现有CLI集成
```python
# main.py 扩展
@app.command()
def tui():
    """启动TUI界面"""
    from .tui.app import ThinkTUI
    app = ThinkTUI()
    app.run()

@app.command()
def collect(...):
    """CLI模式收集想法"""
    # 现有实现

@app.command()
def tui_collect():
    """TUI模式收集想法"""
    from .tui.screens.collect import CollectScreen
    app = ThinkTUI(start_screen=CollectScreen)
    app.run()
```

### 7.2 数据层复用
- **Storage类**：复用现有文件存储逻辑
- **Workspace类**：复用工作空间管理
- **SessionRecorder**：复用会话记录功能

### 7.3 配置管理
```python
# config.py
from pydantic import BaseSettings

class TUIConfig(BaseSettings):
    theme: str = "dark"
    auto_save: bool = True
    confirm_exit: bool = True
    show_tips: bool = True
    max_recent_notes: int = 10
    
    class Config:
        env_prefix = "THINK_TUI_"
```

## 8. 实现计划

### 8.1 第一阶段：基础框架（1周）
1. 搭建Textual项目结构
2. 实现主界面框架
3. 集现有数据层
4. 基础导航功能

### 8.2 第二阶段：核心功能（2周）
1. 实现收集界面
2. 实现澄清对话界面
3. 实现状态管理界面
4. 快捷键系统

### 8.3 第三阶段：增强功能（1周）
1. 想法关联可视化
2. 搜索和过滤功能
3. 设置和主题
4. 性能优化

### 8.4 第四阶段：测试和优化（1周）
1. 单元测试
2. 集成测试
3. 用户体验测试
4. 性能调优

## 9. 测试策略

### 9.1 单元测试
```python
# tests/test_tui/test_widgets.py
def test_note_card_rendering():
    """测试想法卡片渲染"""
    from app.tui.widgets.note_card import NoteCard
    card = NoteCard(content="测试想法", status="received")
    assert card.content == "测试想法"
    assert card.status == "received"

def test_status_badge_colors():
    """测试状态标签颜色"""
    from app.tui.widgets.status_badge import StatusBadge
    badge = StatusBadge(status="received")
    assert badge.color == "green"
```

### 9.2 集成测试
```python
# tests/test_tui/test_integration.py
def test_collect_flow():
    """测试收集流程"""
    from app.tui.screens.collect import CollectScreen
    screen = CollectScreen()
    # 模拟用户输入
    screen.on_input_submit("测试想法")
    assert screen.current_note is not None
```

### 9.3 用户接受测试
- 功能完整性测试
- 性能基准测试
- 用户体验评估

## 10. 部署和维护

### 10.1 构建和分发
```bash
# 构建TUI版本
pip install -e ".[tui]"

# 启动TUI
python -m app.tui

# 或通过CLI命令
python -m app tui
```

### 10.2 监控和日志
- 性能监控：界面渲染时间、内存使用
- 错误日志：异常捕获和报告
- 用户行为：匿名使用统计（可选）

### 10.3 更新和维护
- 版本管理：遵循项目版本规范
- 向后兼容：确保配置和数据格式兼容
- 社区支持：文档和示例更新

## 11. 风险评估

### 11.1 技术风险
- **依赖风险**：Textual版本更新可能引入破坏性变更
- **性能风险**：大量数据渲染可能导致界面卡顿
- **兼容性风险**：不同终端环境下的显示差异

### 11.2 缓解措施
- 锁定依赖版本
- 实现虚拟滚动和分页
- 广泛的终端兼容性测试

## 12. 成功指标

### 12.1 技术指标
- 启动时间 < 2秒
- 界面响应时间 < 100ms
- 内存占用 < 100MB
- 测试覆盖率 > 80%

### 12.2 用户指标
- 操作步骤减少 > 30%
- 用户满意度 > 4.0/5.0
- 功能使用率 > 60%
- 错误率 < 5%

---

**文档版本**：v1.0  
**创建日期**：2026-03-31  
**最后更新**：2026-03-31  
**维护者**：量潮团队