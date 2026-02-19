# CLI → Provider 重构计划

## 目标

将 CLI 中的核心业务逻辑迁移到 Provider（FastAPI），CLI 仅保留 UI 交互逻辑。

## 当前架构

```
CLI (Python/Typer)
├── main.py         # 交互逻辑 + 命令入口
├── clarifier.py    # LLM 调用
├── storage.py      # 文件持久化
├── session_recorder.py  # 会话记录
├── meta.py         # 自省分析
├── workspace.py    # 工作空间管理
└── llm_client.py   # LLM 客户端封装
```

## 重构后架构

```
┌─────────────────┐     ┌─────────────────┐
│   CLI (UI)      │────▶│  Provider API   │
│   Typer CLI     │◀────│  FastAPI        │
└─────────────────┘     └─────────────────┘
        │                       │
        ▼                       ▼
   本地存储              共享核心逻辑
   (workspace)          (clarifier/storage)
```

---

## 详细计划

### Phase 1: Provider API 定义与实现

#### 1.1 项目结构

```
src/provider/
├── main.py              # FastAPI 入口
├── api/
│   └── v1/
│       ├── __init__.py
│       ├── clarify.py   # 澄清 API
│       ├── notes.py     # 笔记 API
│       ├── meta.py      # 自省 API
│       └── workspace.py # 工作空间 API
├── core/
│   ├── __init__.py
│   ├── clarifier.py     # 迁移自 CLI
│   ├── storage.py       # 迁移自 CLI
│   ├── llm_client.py    # 迁移自 CLI
│   └── workspace.py     # 迁移自 CLI
└── requirements.txt
```

#### 1.2 API 接口设计

| 接口 | 方法 | 功能 | 请求体 | 响应 |
|------|------|------|--------|------|
| `/api/v1/clarify/reflect` | POST | 首轮反思 | `{"original": str}` | `{"reflection": str}` |
| `/api/v1/clarify/summarize` | POST | 生成总结 | `{"conversation": list}` | `{"summary": str, "content": str}` |
| `/api/v1/clarify/continue` | POST | 继续对话 | `{"conversation": list}` | `{"response": str}` |
| `/api/v1/notes` | GET | 列出笔记 | - | `{"notes": list}` |
| `/api/v1/notes` | POST | 保存笔记 | `{"original", "content", "summary", "status", ...}` | `{"id": str, "filepath": str}` |
| `/api/v1/notes/{id}/status` | PUT | 更新状态 | `{"status": str}` | `{"success": bool}` |
| `/api/v1/notes/pending` | GET | 待定列表 | - | `{"notes": list}` |
| `/api/v1/meta/analyze` | POST | 自省分析 | `{"workspace": str}` | `{"report": str}` |
| `/api/v1/health` | GET | 健康检查 | - | `{"status": "ok"}` |

#### 1.3 核心模块迁移

| CLI 模块 | Provider 路径 | 变更 |
|----------|---------------|------|
| `llm_client.py` | `core/llm_client.py` | 直接迁移 |
| `clarifier.py` | `core/clarifier.py` | 返回 JSON 替代直接打印 |
| `storage.py` | `core/storage.py` | 添加 API 接口层 |
| `workspace.py` | `core/workspace.py` | 直接迁移 |
| `prompts.py` | `core/prompts.py` | 直接迁移 |
| `session_recorder.py` | `core/session_recorder.py` | 直接迁移 |
| `meta.py` | `api/v1/meta.py` | 适配 API 形式 |

---

### Phase 2: CLI 改造

#### 2.1 依赖变更

- 移除 `clarifier.py`, `storage.py`, `llm_client.py` 等核心逻辑
- 保留 `workspace.py`（轻量配置）
- 新增 HTTP 客户端依赖（httpx 或 requests）

#### 2.2 交互模式改造

```python
# 旧：直接调用
clarifier = Clarifier(recorder)
reflection = clarifier.reflect(original)

# 新：通过 API 调用
response = httpx.post(f"{API_BASE}/api/v1/clarify/reflect", json={"original": original})
reflection = response.json()["reflection"]
```

#### 2.3 命令适配

| 命令 | 改造方式 |
|------|----------|
| `collect` | 调用 `/api/v1/clarify/*` 接口 |
| `pending` | 调用 `/api/v1/notes/pending` |
| `review` | 调用 `/api/v1/notes/{id}/status` |
| `meta` | 调用 `/api/v1/meta/analyze` |

---

### Phase 3: 数据与配置共享

#### 3.1 共享目录

```
data/
└── {workspace}/
    ├── notes/
    │   ├── received/
    │   ├── pending/
    │   └── rejected/
    └── sessions/
```

- Provider 和 CLI 共用 `data/` 目录
- 通过文件系统直接读写

#### 3.2 环境配置

```bash
# .env
PROVIDER_URL=http://localhost:8000
DEFAULT_WORKSPACE=default
```

#### 3.3 离线优先

- CLI 检测 Provider 不可用时，回退到本地直接调用
- 通过环境变量 `OFFLINE_MODE=true` 强制本地模式

---

## 执行顺序

1. **Step 1**: 创建 Provider 目录结构和 `requirements.txt`
2. **Step 2**: 迁移 `core/` 模块（llm_client, prompts, workspace）
3. **Step 3**: 实现 `clarifier` API 端点
4. **Step 4**: 实现 `notes` API 端点
5. **Step 5**: 实现 `meta` API 端点
6. **Step 6**: CLI 添加 HTTP 客户端依赖
7. **Step 7**: CLI 改造 `collect` 命令
8. **Step 8**: CLI 改造 `pending`, `review`, `meta` 命令
9. **Step 9**: 添加离线回退逻辑

## 验收标准

- [ ] Provider API 所有端点返回正确格式
- [ ] CLI 各命令功能与重构前一致
- [ ] 离线模式下 CLI 可独立运行
- [ ] 运行 `./scripts/run-provider` 启动服务
- [ ] 运行 `./scripts/run-cli` 正常工作
