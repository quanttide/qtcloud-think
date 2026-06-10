use std::path::{Path, PathBuf};

use quanttide_think::{
    domain::Domain,
    intention::Intention,
    schema::SchemaContent,
    situation::Situation,
    situation_relation::SituationRelation,
};

#[derive(Debug)]
pub struct Repo {
    path: PathBuf,
}

impl Repo {
    pub fn from_config(cfg: &crate::config::Config) -> Self {
        Self::open(&cfg.journal_path)
    }
    /// Open a journal at the given path.
    pub fn open<P: AsRef<Path>>(path: P) -> Self {
        Self { path: path.as_ref().to_path_buf() }
    }

    /// List all worlds (directories under root).
    pub fn worlds(&self) -> Result<Vec<String>, String> {
        let mut worlds = Vec::new();
        let entries = std::fs::read_dir(&self.path)
            .map_err(|e| format!("cannot read journal: {}", e))?;
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_dir() && !path.file_name().unwrap().to_str().unwrap().starts_with('.') {
                if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
                    worlds.push(name.to_string());
                }
            }
        }
        worlds.sort();
        Ok(worlds)
    }

    /// List all periods (weeks) for a world.
    pub fn periods(&self, world: &str) -> Result<Vec<String>, String> {
        let dir = self.path.join(world);
        let mut periods = Vec::new();
        let entries = std::fs::read_dir(&dir)
            .map_err(|e| format!("cannot read world {}: {}", world, e))?;
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_dir() {
                if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
                    periods.push(name.to_string());
                }
            }
        }
        periods.sort();
        Ok(periods)
    }

    /// List all domains for a world + period.
    pub fn domains(&self, world: &str, period: &str) -> Result<Vec<Domain>, String> {
        let dir = self.path.join(world).join(period);
        let mut domains = Vec::new();
        let entries = std::fs::read_dir(&dir)
            .map_err(|e| format!("cannot read {}/{}: {}", world, period, e))?;
        for entry in entries.flatten() {
            let path = entry.path();
            if path.extension().map_or(false, |e| e == "yaml") {
                if let Some(stem) = path.file_stem().and_then(|n| n.to_str()) {
                    if stem != "thoughts" {
                        let label = stem.to_string();
                        domains.push(Domain { name: stem.to_string(), label });
                    }
                }
            }
        }
        domains.sort_by(|a, b| a.name.cmp(&b.name));
        Ok(domains)
    }

    /// Load a domain file.
    pub fn load(&self, world: &str, period: &str, domain: &str) -> Result<DomainFile, String> {
        let path = self.path.join(world).join(period).join(format!("{}.yaml", domain));
        let content = std::fs::read_to_string(&path)
            .map_err(|e| format!("cannot read {}: {}", path.display(), e))?;
        let raw: serde_yaml::Value = serde_yaml::from_str(&content)
            .map_err(|e| format!("cannot parse {}: {}", path.display(), e))?;

        let schemas = raw.get("schemas")
            .and_then(|v| serde_yaml::from_value::<Vec<SchemaContent>>(v.clone()).ok());

        let situations = raw.get("situations")
            .and_then(|arr| arr.as_sequence())
            .map(|seq| seq.iter().filter_map(JournalSituation::from_value).collect())
            .unwrap_or_default();

        let intentions = raw.get("intentions")
            .and_then(|v| serde_yaml::from_value::<Vec<Intention>>(v.clone()).ok());

        let thoughts = raw.get("thoughts")
            .and_then(|v| serde_yaml::from_value::<Vec<String>>(v.clone()).ok());

        Ok(DomainFile {
            schemas,
            situations,
            intentions,
            thoughts,
        })
    }
}

#[derive(Debug, Clone)]
pub struct JournalSituation {
    pub situation: Situation,
    pub relations: Vec<SituationRelation>,
}

impl JournalSituation {
    pub fn from_value(v: &serde_yaml::Value) -> Option<Self> {
        let situation: Situation = serde_yaml::from_value(v.clone()).ok()?;
        let relations = v.get("relations")
            .and_then(|r| serde_yaml::from_value(r.clone()).ok())
            .unwrap_or_default();
        Some(Self { situation, relations })
    }
}

#[derive(Debug)]
pub struct DomainFile {
    pub schemas: Option<Vec<SchemaContent>>,
    pub situations: Vec<JournalSituation>,
    pub intentions: Option<Vec<Intention>>,
    pub thoughts: Option<Vec<String>>,
}

impl DomainFile {
    /// The situation name is the primary identifier.
    pub fn situation(&self) -> Option<&Situation> {
        self.situations.first().map(|js| &js.situation)
    }

    /// All relations from the embedded situation entries.
    pub fn relations(&self) -> Vec<&SituationRelation> {
        self.situations.iter().flat_map(|js| js.relations.iter()).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_worlds() {
        let repo = Repo::open("../../../../data/journal");
        let worlds = repo.worlds().unwrap();
        assert!(worlds.contains(&"quanttide-founder".to_string()));
    }

    #[test]
    fn test_periods() {
        let repo = Repo::open("../../../../data/journal");
        let periods = repo.periods("quanttide-founder").unwrap();
        assert!(periods.contains(&"2026-W23".to_string()));
    }

    #[test]
    fn test_domains() {
        let journal = Repo::open("../../../../data/journal");
        let domains = journal.domains("quanttide-founder", "2026-W23").unwrap();
        let names: Vec<&str> = domains.iter().map(|d| d.name.as_str()).collect();
        assert!(names.contains(&"think"));
    }

    #[test]
    fn test_load() {
        let journal = Repo::open("../../../../data/journal");
        let df = journal.load("quanttide-founder", "2026-W23", "think").unwrap();
        assert!(df.situations.iter().any(|js| js.situation.name == "think"));
    }
}
