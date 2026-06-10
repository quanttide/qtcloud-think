/// 分析模块的数据类型。

/// 一个领域在两段时间点之间的差异。
#[derive(Debug)]
pub struct Diff {
    pub domain: String,
    pub prev: String,
    pub curr: String,
    /// 两段之间的每条意图的变化（新增、修改、删除）。
    pub intentions: Vec<IntentionDiff>,
    /// 图式的实体变化。
    pub schema: SchemaDiff,
}

/// 一条意图在两个时间点的状态。
#[derive(Debug)]
pub struct IntentionDiff {
    pub title: String,
    /// 上一期状态。None 表示该意图在上一期不存在（新增）。
    pub prev: Option<IntentionState>,
    /// 当前期状态。None 表示该意图在当前期不存在（消失）。
    pub curr: Option<IntentionState>,
}

/// 意图在某个时间点的维度状态。
#[derive(Debug)]
pub struct IntentionState {
    pub priority: String,
    pub risk: String,
    pub level: String,
}

/// 图式的实体变化。
#[derive(Debug)]
pub struct SchemaDiff {
    pub prev_entities: Vec<String>,
    pub curr_entities: Vec<String>,
    pub added: Vec<String>,
    pub removed: Vec<String>,
}

/// 一个领域在某周的数据覆盖度。
#[derive(Debug)]
pub struct Coverage {
    pub domain: String,
    pub intentions: usize,
    pub schemas: bool,
    pub relations: usize,
}

/// 一个领域在某周的快照。
#[derive(Debug)]
pub struct Snapshot {
    pub period: String,
    pub intentions: Vec<IntentionEntry>,
    pub entities: Vec<String>,
}

/// 快照中的一条意图记录。
#[derive(Debug)]
pub struct IntentionEntry {
    pub title: String,
    pub priority: String,
    pub level: String,
    pub risk: String,
}
