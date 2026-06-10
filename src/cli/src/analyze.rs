/// 分析模块：跨周对比、覆盖率、演化轨迹。
///
/// 所有函数都是纯数据变换——输入 Repo，输出结构化数据，不关心输出格式。
use crate::model::{
    Coverage, Diff, IntentionDiff, IntentionEntry, IntentionState, SchemaDiff, Snapshot,
};
use crate::repo::Repo;

/// 对比一个领域在两个周的数据差异。
pub fn compare_domain(repo: &Repo, world: &str, prev: &str, curr: &str, domain: &str) -> Result<Diff, String> {
    let a = repo.load(world, prev, domain)?;
    let b = repo.load(world, curr, domain)?;

    let intentions = {
        let ai = a.intentions.unwrap_or_default();
        let bi = b.intentions.unwrap_or_default();
        let mut result = Vec::new();
        for i in &ai {
            result.push(IntentionDiff {
                title: i.title.clone(),
                prev: Some(IntentionState { priority: i.priority.name.clone(), risk: i.risk.name.clone(), level: i.level.name.clone() }),
                curr: bi.iter().find(|x| x.title == i.title).map(|x| IntentionState { priority: x.priority.name.clone(), risk: x.risk.name.clone(), level: x.level.name.clone() }),
            });
        }
        for i in &bi {
            if !ai.iter().any(|x| x.title == i.title) {
                result.push(IntentionDiff {
                    title: i.title.clone(),
                    prev: None,
                    curr: Some(IntentionState { priority: i.priority.name.clone(), risk: i.risk.name.clone(), level: i.level.name.clone() }),
                });
            }
        }
        result
    };

    let schema = {
        let prev_ents = a.schemas.as_ref()
            .and_then(|s| s.first())
            .map(|s| s.entities.iter().map(|e| e.name.clone()).collect::<Vec<_>>())
            .unwrap_or_default();
        let curr_ents = b.schemas.as_ref()
            .and_then(|s| s.first())
            .map(|s| s.entities.iter().map(|e| e.name.clone()).collect::<Vec<_>>())
            .unwrap_or_default();
        SchemaDiff {
            added: curr_ents.iter().filter(|e| !prev_ents.contains(e)).cloned().collect(),
            removed: prev_ents.iter().filter(|e| !curr_ents.contains(e)).cloned().collect(),
            prev_entities: prev_ents,
            curr_entities: curr_ents,
        }
    };

    Ok(Diff { domain: domain.to_string(), prev: prev.to_string(), curr: curr.to_string(), intentions, schema })
}

/// 对比整个周的所有领域的数据差异。
pub fn compare_period(repo: &Repo, world: &str, prev: &str, curr: &str) -> Result<Vec<Diff>, String> {
    let domains = repo.domains(world, curr)?;
    let mut results = Vec::new();
    for d in &domains {
        if let Ok(diff) = compare_domain(repo, world, prev, curr, &d.name) {
            if !diff.intentions.is_empty() || !diff.schema.added.is_empty() || !diff.schema.removed.is_empty() {
                results.push(diff);
            }
        }
    }
    Ok(results)
}

/// 统计某周每个领域的数据覆盖度。
pub fn summarize_coverage(repo: &Repo, world: &str, period: &str) -> Result<Vec<Coverage>, String> {
    let domains = repo.domains(world, period)?;
    let mut results = Vec::new();
    for d in &domains {
        let file = repo.load(world, period, &d.name)?;
        results.push(Coverage {
            domain: d.name.clone(),
            intentions: file.intentions.as_ref().map(|v| v.len()).unwrap_or(0),
            schemas: file.schemas.is_some(),
            relations: file.relations().len(),
        });
    }
    Ok(results)
}

/// 追踪一个领域在所有周中的演化轨迹。
pub fn track_evolution(repo: &Repo, world: &str, domain: &str) -> Result<Vec<Snapshot>, String> {
    let periods = repo.periods(world)?;
    let mut snapshots = Vec::new();
    for p in &periods {
        if let Ok(file) = repo.load(world, p, domain) {
            let intentions = file.intentions.unwrap_or_default().into_iter().map(|i| IntentionEntry {
                title: i.title,
                priority: i.priority.name,
                level: i.level.name,
                risk: i.risk.name,
            }).collect();
            let entities = file.schemas.as_ref()
                .and_then(|s| s.first())
                .map(|s| s.entities.iter().map(|e| e.name.clone()).collect())
                .unwrap_or_default();
            snapshots.push(Snapshot { period: p.clone(), intentions, entities });
        }
    }
    Ok(snapshots)
}
