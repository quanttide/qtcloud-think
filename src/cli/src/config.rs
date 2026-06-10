use std::path::PathBuf;

pub struct Config {
    pub journal_path: PathBuf,
}

impl Config {
    pub fn from_env() -> Self {
        let journal_path = std::env::var("JOURNAL_PATH")
            .unwrap_or_else(|_| "data/journal".to_string());
        Self {
            journal_path: PathBuf::from(journal_path),
        }
    }

    pub fn for_tests() -> Self {
        let path = std::env::var("JOURNAL_PATH")
            .unwrap_or_else(|_| "../../../../data/journal".to_string());
        Self { journal_path: PathBuf::from(path) }
    }
}
