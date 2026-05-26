use crate::ai::{AiClient, AiContext};
use crate::config::Config;
use crate::db::{Database, Idea, Session, Thought};
use anyhow::Result;
use std::sync::Arc;
use tokio::sync::Mutex;

/// Shared application state between the UI and event handlers.
pub struct AppState {
    /// Current database reference.
    pub db: Arc<Mutex<Database>>,
    /// Application config.
    pub config: Config,
    /// Active session.
    pub session: Option<Session>,
    /// Recent thoughts (newest first).
    pub thoughts: Vec<Thought>,
    /// Currently displayed idea (pending / accepted / rejected).
    pub current_idea: Option<Idea>,
    /// Input buffer.
    pub input: String,
    /// Whether AI is currently processing.
    pub is_processing: bool,
    /// Last error message (if any).
    pub error_message: Option<String>,
    /// Whether the app should quit.
    pub should_quit: bool,
}

impl AppState {
    /// Create a new AppState, initializing the database and default session.
    pub async fn new(config: Config) -> Result<Self> {
        let db_path = config.storage.data_dir.join("thinkcloud.db");
        let db = Database::open(&db_path)?;
        let db = Arc::new(Mutex::new(db));

        let session = {
            let db = db.lock().await;
            db.get_or_create_default_session()?
        };

        let thoughts = {
            let db = db.lock().await;
            db.recent_thoughts(session.id, 10)?
        };

        Ok(Self {
            db,
            config,
            session: Some(session),
            thoughts,
            current_idea: None,
            input: String::new(),
            is_processing: false,
            error_message: None,
            should_quit: false,
        })
    }

    /// The current session's title for the UI header.
    pub fn session_title(&self) -> String {
        self.session
            .as_ref()
            .map(|s| s.title.clone())
            .unwrap_or_else(|| "无会话".to_string())
    }

    /// Submit the current input as a new thought, then trigger AI.
    pub async fn submit_thought(&mut self) -> Result<()> {
        let content = self.input.trim().to_string();
        if content.is_empty() {
            return Ok(());
        }
        self.input.clear();

        let session_id = self.session.as_ref().map(|s| s.id).unwrap_or(0);

        // Insert thought into DB
        let db = self.db.lock().await;
        let thought = db.insert_thought(session_id, &content)?;
        drop(db);
        self.thoughts.insert(0, thought);
        self.thoughts.truncate(20);

        // Trigger AI
        self.trigger_ai().await;

        Ok(())
    }

    /// Trigger AI idea generation.
    /// DB operations and HTTP call are separated so rusqlite (non-Send) never
    /// crosses a `.await` boundary while locked.
    pub async fn trigger_ai(&mut self) {
        if self.is_processing {
            return;
        }

        self.is_processing = true;
        self.error_message = None;

        let session_id = self.session.as_ref().map(|s| s.id).unwrap_or(0);
        let thought_window = self.config.ui.thought_window;

        // --- Phase 1: Load data from DB (hold lock, no await inside) ---
        let (thought_texts, total_count) = {
            let db = self.db.lock().await;
            let thoughts = db
                .recent_thoughts(session_id, thought_window * 2)
                .unwrap_or_default();

            // Mark first (newest) as processing
            if let Some(t) = thoughts.first() {
                let _ = db.update_thought_status(t.id, "processing");
            }

            let texts: Vec<(i64, String)> =
                thoughts.iter().map(|t| (t.id, t.content.clone())).collect();
            let total = texts.len();
            (texts, total)
        };

        // Mark in-memory thoughts as processing
        for t in self.thoughts.iter_mut() {
            if t.status == "pending" {
                t.status = "processing".to_string();
                break;
            }
        }

        if thought_texts.is_empty() {
            self.error_message = Some("没有念头可供处理".to_string());
            self.is_processing = false;
            return;
        }

        // --- Phase 2: Call AI (no DB lock held) ---
        let ai_context = AiContext::new(thought_texts, total_count, thought_window);
        let ai_client = AiClient::new(self.config.clone());
        let ai_result = ai_client.generate_idea(&ai_context).await;

        // --- Phase 3: Store result back to DB ---
        match ai_result {
            Ok(idea_text) => {
                let db = self.db.lock().await;
                // Store idea
                let idea = match db.insert_idea(session_id, &idea_text) {
                    Ok(idea) => idea,
                    Err(e) => {
                        self.error_message = Some(format!("存储想法失败: {}", e));
                        // Mark thoughts as failed
                        for t in self.thoughts.iter_mut() {
                            if t.status == "processing" {
                                t.status = "failed".to_string();
                            }
                        }
                        drop(db);
                        self.is_processing = false;
                        return;
                    }
                };

                // Link to source thoughts
                let source_ids: Vec<i64> = self
                    .thoughts
                    .iter()
                    .filter(|t| t.status == "processing" || t.status == "completed")
                    .map(|t| t.id)
                    .collect();
                let _ = db.link_idea_thoughts(idea.id, &source_ids);

                // Mark thoughts as completed
                for t in self.thoughts.iter_mut() {
                    if t.status == "processing" {
                        let _ = db.update_thought_status(t.id, "completed");
                        t.status = "completed".to_string();
                    }
                }
                drop(db);

                // Set current idea
                self.current_idea = Some(idea);
            }
            Err(e) => {
                self.error_message = Some(e.to_string());
                // Mark thoughts as failed
                let db = self.db.lock().await;
                for t in self.thoughts.iter_mut() {
                    if t.status == "processing" {
                        let _ = db.update_thought_status(t.id, "failed");
                        t.status = "failed".to_string();
                    }
                }
                drop(db);
            }
        }

        self.is_processing = false;
    }

    /// Accept the current idea.
    pub async fn accept_idea(&mut self) -> Result<()> {
        if let Some(idea) = self.current_idea.take() {
            if idea.status == "pending" {
                let db = self.db.lock().await;
                db.update_idea_status(idea.id, "accepted")?;
                drop(db);
                self.current_idea = Some(Idea {
                    status: "accepted".to_string(),
                    ..idea
                });
            }
        }
        Ok(())
    }

    /// Reject the current idea.
    pub async fn reject_idea(&mut self) -> Result<()> {
        if let Some(idea) = self.current_idea.take() {
            if idea.status == "pending" {
                let db = self.db.lock().await;
                db.update_idea_status(idea.id, "rejected")?;
                drop(db);
                self.current_idea = Some(Idea {
                    status: "rejected".to_string(),
                    ..idea
                });
            }
        }
        Ok(())
    }

    /// Retry AI generation after a failure.
    pub async fn retry_ai(&mut self) {
        // Mark failed thoughts back to pending
        let db_lock = self.db.lock().await;
        for t in self.thoughts.iter_mut() {
            if t.status == "failed" {
                let _ = db_lock.update_thought_status(t.id, "pending");
                t.status = "pending".to_string();
            }
        }
        drop(db_lock);
        self.current_idea = None;
        self.error_message = None;
        self.trigger_ai().await;
    }

    /// Handle the "material" command.
    pub async fn set_material(&mut self, path: &str) -> Result<String> {
        Ok(format!("材料已加载: {}", path))
    }

    /// Create a new session.
    pub async fn new_session(&mut self, title: &str) -> Result<()> {
        let db = self.db.lock().await;
        let session_id = db.create_session(title)?;
        let session = db.get_session_by_id(session_id)?;
        drop(db);
        self.session = Some(session);
        self.thoughts.clear();
        self.current_idea = None;
        self.input.clear();
        self.error_message = None;
        Ok(())
    }
}
