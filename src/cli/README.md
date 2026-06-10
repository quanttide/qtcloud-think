# qtcloud-think-cli

量潮思考云命令行工具库，提供对 journal 数据的访问和分析功能。

## 目录结构

```
src/cli/
├── Cargo.toml              # 项目配置与依赖定义
├── ROADMAP.md              # 开发路线图
├── src/
│   ├── lib.rs              # 库入口，导出四个公共模块
│   ├── analyze.rs          # 分析模块：追踪领域演化轨迹
│   ├── config.rs           # 配置模块：读取环境变量中的路径配置
│   ├── model.rs            # 数据模型定义
│   └── repo.rs             # 仓库/存储层：读取 journal 文件结构
└── tests/
    └── repo.rs             # 集成测试
```

## 架构设计

该 crate 是一个 Rust 库（library crate），而非可执行程序。它导出四个公共模块，供其他组件（如 CLI 二进制或 Web 服务）调用。

### 核心依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| `quanttide-think` | 0.1.0-alpha.10 | 核心数据模型（Domain, Intention, Schema, Situation 等） |
| `quanttide-agent` | 0.1.0-alpha.2 | 智能体基础设施 |
| `serde` | 1 (with `derive`) | 序列化/反序列化框架 |
| `serde_yaml` | 0.9 | YAML 格式解析 |
| `chrono` | 0.4 (with `serde`) | 日期时间处理 |
| `anyhow` | 1 | 错误处理 |

### 数据层次

Journal 数据按以下层次组织：

```
{JOURNAL_PATH}/
├── {world}/                    # 世界（如 quanttide-founder）
│   ├── {period}/               # 周期（如 2026-W23）
│   │   ├── {domain}.yaml       # 领域文件（如 think.yaml）
│   │   └── thoughts.yaml       # 思考文件
│   └── ...
└── ...
```

## 核心模块

### 1. 配置模块 (`config.rs`)

从环境变量读取配置，提供 `Config` 结构体。

```rust
use qtcloud_think_cli::config::Config;

// 生产环境：从 JOURNAL_PATH 环境变量读取，默认 "data/journal"
let config = Config::from_env();

// 测试环境：默认 "../../../../data/journal"（相对路径）
let config = Config::for_tests();
```

### 2. 仓库模块 (`repo.rs`)

对 journal 文件系统的抽象访问层，提供以下功能：

```rust
use qtcloud_think_cli::config::Config;
use qtcloud_think_cli::repo::Repo;

let repo = Repo::from_config(&Config::from_env());

// 列出所有 world
let worlds = repo.worlds()?;

// 列出某 world 下的所有 period
let periods = repo.periods("quanttide-founder")?;

// 列出某 world/period 下的所有 domain
let domains = repo.domains("quanttide-founder", "2026-W23")?;

// 加载并解析单个 domain 文件
let domain_file = repo.load("quanttide-founder", "2026-W23", "think")?;

// 描述某周各领域的数据一致性情况
let coherence = repo.describe("quanttide-founder", "2026-W23")?;
```

### 3. 分析模块 (`analyze.rs`)

追踪领域随时间的变化轨迹：

```rust
use qtcloud_think_cli::analyze::track_evolution;
use qtcloud_think_cli::config::Config;
use qtcloud_think_cli::repo::Repo;

let repo = Repo::from_config(&Config::from_env());
let snapshots = track_evolution(&repo, "quanttide-founder", "think")?;

for snapshot in snapshots {
    println!("Period: {}", snapshot.period);
    println!("Intentions: {:?}", snapshot.intentions);
    println!("Entities: {:?}", snapshot.entities);
}
```

### 4. 数据模型 (`model.rs`)

定义 CLI 层使用的两个核心数据结构：

```rust
/// 某领域在某周的快照
pub struct Snapshot {
    pub period: String,
    pub intentions: Vec<IntentionEntry>,
    pub entities: Vec<String>,
}

/// 单条意图记录
pub struct IntentionEntry {
    pub title: String,
    pub priority: String,
    pub level: String,
    pub risk: String,
}
```

## 使用指南

### 集成到其他 crate

在 `Cargo.toml` 中添加依赖：

```toml
[dependencies]
qtcloud-think-cli = { path = "../cli" }
```

### 读取 journal 数据

```rust
use qtcloud_think_cli::config::Config;
use qtcloud_think_cli::repo::Repo;

fn main() -> Result<(), String> {
    let repo = Repo::from_config(&Config::from_env());
    
    // 列出所有 world
    let worlds = repo.worlds()?;
    println!("Available worlds: {:?}", worlds);
    
    // 列出某 world 的 period
    if let Some(world) = worlds.first() {
        let periods = repo.periods(world)?;
        println!("Periods for {}: {:?}", world, periods);
        
        // 加载某 period 的所有 domain 数据
        if let Some(period) = periods.first() {
            let domains = repo.domains(world, period)?;
            for domain in domains {
                let file = repo.load(world, period, &domain.name)?;
                println!("Domain {}: {:?}", domain.name, file.situations.len());
            }
        }
    }
    
    Ok(())
}
```

## 开发指南

### 环境要求

- Rust 2021 edition 或更高版本
- 需要真实的 journal 数据目录用于测试

### 本地开发

1. 克隆仓库
2. 确保 `data/journal` 目录存在（或设置 `JOURNAL_PATH` 环境变量）
3. 运行测试：`cargo test`

### 运行测试

```bash
# 运行所有测试
cargo test

# 运行特定测试
cargo test test_worlds
```

测试依赖真实的 journal 数据目录。测试默认使用相对路径 `../../../../data/journal`，确保从测试目录能访问到主仓库的 journal 数据。

### 代码规范

- 遵循 Rust 官方代码风格
- 使用 `anyhow` 进行错误处理
- 所有公共 API 需要文档注释

## 数据模型

### DomainFile

解析后的 domain 文件结构：

```rust
pub struct DomainFile {
    pub schemas: Option<Vec<SchemaContent>>,
    pub situations: Vec<JournalSituation>,
    pub intentions: Option<Vec<Intention>>,
    pub thoughts: Option<Vec<String>>,
}
```

### DataCoherence

数据一致性描述：

```rust
pub struct DataCoherence {
    pub domain: String,        // 领域名称
    pub intentions: usize,     // 意图数量
    pub schemas: bool,         // 是否有 schema
    pub relations: usize,      // 关系数量
}
```

## 路线图

详见 [ROADMAP.md](ROADMAP.md)

- [ ] 实现 `storage.rs`，以 journal 结构（world → period → domain）为存储格式
- [ ] 支持按 world、period、domain 查询
- [ ] 以 `quanttide-think` 和 `quanttide-agent` 为数据模型和基础设施

## 相关文档

- [主项目 README](../../README.md)
- [主项目 ROADMAP](../../ROADMAP.md)
- [贡献指南](../../CONTRIBUTING.md)
