/// 数据类型。

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
