/// 归纳模块：覆盖度、统计、概览。
///
/// 回答"当前状态如何"，不回答"有什么变化"。
use crate::model::Coverage;
use crate::repo::Repo;

/// 统计某周每个领域的数据覆盖度。
pub fn coverage(repo: &Repo, world: &str, period: &str) -> Result<Vec<Coverage>, String> {
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
