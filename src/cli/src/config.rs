use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

/// Application configuration loaded from `config.toml`.
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct Config {
    #[serde(default)]
    pub ai: AiConfig,
    #[serde(default)]
    pub storage: StorageConfig,
    #[serde(default)]
    pub ui: UiConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AiConfig {
    /// API provider: "openai" or "ollama"
    #[serde(default = "default_provider")]
    pub provider: String,
    /// API base URL
    #[serde(default = "default_base_url")]
    pub base_url: String,
    /// Model name
    #[serde(default = "default_model")]
    pub model: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageConfig {
    /// Data directory for SQLite database
    #[serde(default = "default_data_dir")]
    pub data_dir: PathBuf,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UiConfig {
    /// Number of recent thoughts to include in AI context
    #[serde(default = "default_thought_window")]
    pub thought_window: usize,
}

// --- Defaults ---

impl Default for AiConfig {
    fn default() -> Self {
        Self {
            provider: default_provider(),
            base_url: default_base_url(),
            model: default_model(),
        }
    }
}

impl Default for StorageConfig {
    fn default() -> Self {
        Self {
            data_dir: default_data_dir(),
        }
    }
}

impl Default for UiConfig {
    fn default() -> Self {
        Self {
            thought_window: default_thought_window(),
        }
    }
}

fn default_provider() -> String {
    "openai".to_string()
}

fn default_base_url() -> String {
    "https://api.openai.com/v1".to_string()
}

fn default_model() -> String {
    "gpt-4o".to_string()
}

fn default_data_dir() -> PathBuf {
    dirs::data_dir()
        .unwrap_or_else(|| PathBuf::from("."))
        .join("thinkcloud")
}

fn default_thought_window() -> usize {
    10
}

impl Config {
    /// Load config from the default path `~/.config/thinkcloud/config.toml`.
    /// Returns default config if the file does not exist.
    pub fn load() -> Result<Self> {
        let config_path = Self::config_path()?;
        if config_path.exists() {
            let content = std::fs::read_to_string(&config_path).with_context(|| {
                format!("Failed to read config file: {}", config_path.display())
            })?;
            let config: Config = toml::from_str(&content).with_context(|| {
                format!("Failed to parse config file: {}", config_path.display())
            })?;
            Ok(config)
        } else {
            Ok(Config::default())
        }
    }

    /// Get the API key from environment variable `THINKCLOUD_API_KEY`.
    pub fn api_key(&self) -> Option<String> {
        std::env::var("THINKCLOUD_API_KEY").ok()
    }

    /// Path to the config file.
    fn config_path() -> Result<PathBuf> {
        let config_dir = dirs::config_dir()
            .context("Cannot determine config directory")?
            .join("thinkcloud");
        Ok(config_dir.join("config.toml"))
    }
}
