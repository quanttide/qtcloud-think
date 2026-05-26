use anyhow::{Context, Result};
use chrono::Utc;
use rusqlite::{params, Connection};
use std::path::Path;

/// A session groups thoughts and ideas under a common topic.
#[derive(Debug, Clone)]
pub struct Session {
    pub id: i64,
    pub title: String,
    pub material_id: Option<i64>,
    pub created_at: String,
    pub updated_at: String,
}

/// A thought is a short text input from the user.
#[derive(Debug, Clone)]
pub struct Thought {
    pub id: i64,
    pub session_id: i64,
    pub material_id: Option<i64>,
    pub content: String,
    pub status: String, // pending | processing | completed | failed
    pub created_at: String,
}

/// An idea is an AI-generated conclusion.
#[derive(Debug, Clone)]
pub struct Idea {
    pub id: i64,
    pub session_id: i64,
    pub content: String,
    pub status: String, // pending | accepted | rejected
    pub created_at: String,
}

/// Database handle wrapping a SQLite connection.
pub struct Database {
    conn: Connection,
}

impl Database {
    /// Open (or create) the database at the given path.
    pub fn open(db_path: &Path) -> Result<Self> {
        if let Some(parent) = db_path.parent() {
            std::fs::create_dir_all(parent).with_context(|| {
                format!("Failed to create data directory: {}", parent.display())
            })?;
        }

        let conn = Connection::open(db_path)
            .with_context(|| format!("Failed to open database: {}", db_path.display()))?;

        let db = Self { conn };
        db.migrate()?;
        Ok(db)
    }

    /// Run schema migrations.
    fn migrate(&self) -> Result<()> {
        self.conn
            .execute_batch(
                "
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                material_id INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (material_id) REFERENCES materials(id)
            );

            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY,
                path TEXT,
                content_snippet TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS thoughts (
                id INTEGER PRIMARY KEY,
                session_id INTEGER NOT NULL,
                material_id INTEGER,
                content TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id),
                FOREIGN KEY (material_id) REFERENCES materials(id)
            );

            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY,
                session_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            );

            CREATE TABLE IF NOT EXISTS idea_thoughts (
                idea_id INTEGER NOT NULL,
                thought_id INTEGER NOT NULL,
                PRIMARY KEY (idea_id, thought_id),
                FOREIGN KEY (idea_id) REFERENCES ideas(id),
                FOREIGN KEY (thought_id) REFERENCES thoughts(id)
            );
            ",
            )
            .context("Failed to run database migrations")?;
        Ok(())
    }

    // --- Session ---

    /// Create a new session and return its id.
    pub fn create_session(&self, title: &str) -> Result<i64> {
        let now = Utc::now().to_rfc3339();
        self.conn
            .execute(
                "INSERT INTO sessions (title, created_at, updated_at) VALUES (?1, ?2, ?3)",
                params![title, now, now],
            )
            .context("Failed to create session")?;
        Ok(self.conn.last_insert_rowid())
    }

    /// Get all sessions, ordered by most recently updated.
    pub fn list_sessions(&self) -> Result<Vec<Session>> {
        let mut stmt = self
            .conn
            .prepare("SELECT id, title, material_id, created_at, updated_at FROM sessions ORDER BY updated_at DESC")
            .context("Failed to prepare session query")?;

        let sessions = stmt
            .query_map([], |row| {
                Ok(Session {
                    id: row.get(0)?,
                    title: row.get(1)?,
                    material_id: row.get(2)?,
                    created_at: row.get(3)?,
                    updated_at: row.get(4)?,
                })
            })
            .context("Failed to query sessions")?
            .collect::<std::result::Result<Vec<_>, _>>()
            .context("Failed to collect sessions")?;

        Ok(sessions)
    }

    /// Get the most recent session, or create a default one.
    pub fn get_or_create_default_session(&self) -> Result<Session> {
        let sessions = self.list_sessions()?;
        if let Some(session) = sessions.into_iter().next() {
            Ok(session)
        } else {
            let id = self.create_session("默认会话")?;
            self.get_session_by_id(id)
        }
    }

    pub fn get_session_by_id(&self, id: i64) -> Result<Session> {
        self.conn
            .query_row(
                "SELECT id, title, material_id, created_at, updated_at FROM sessions WHERE id = ?1",
                params![id],
                |row| {
                    Ok(Session {
                        id: row.get(0)?,
                        title: row.get(1)?,
                        material_id: row.get(2)?,
                        created_at: row.get(3)?,
                        updated_at: row.get(4)?,
                    })
                },
            )
            .context("Failed to get session")
    }

    // --- Thought ---

    /// Insert a new thought.
    pub fn insert_thought(&self, session_id: i64, content: &str) -> Result<Thought> {
        let now = Utc::now().to_rfc3339();
        self.conn
            .execute(
                "INSERT INTO thoughts (session_id, content, status, created_at) VALUES (?1, ?2, 'pending', ?3)",
                params![session_id, content, now],
            )
            .context("Failed to insert thought")?;

        let id = self.conn.last_insert_rowid();
        self.get_thought(id)
    }

    /// Get a single thought by id.
    pub fn get_thought(&self, id: i64) -> Result<Thought> {
        self.conn
            .query_row(
                "SELECT id, session_id, material_id, content, status, created_at FROM thoughts WHERE id = ?1",
                params![id],
                |row| {
                    Ok(Thought {
                        id: row.get(0)?,
                        session_id: row.get(1)?,
                        material_id: row.get(2)?,
                        content: row.get(3)?,
                        status: row.get(4)?,
                        created_at: row.get(5)?,
                    })
                },
            )
            .context("Failed to get thought")
    }

    /// Update thought status.
    pub fn update_thought_status(&self, id: i64, status: &str) -> Result<()> {
        self.conn
            .execute(
                "UPDATE thoughts SET status = ?1 WHERE id = ?2",
                params![status, id],
            )
            .context("Failed to update thought status")?;
        Ok(())
    }

    /// Get recent thoughts for a session, newest first.
    pub fn recent_thoughts(&self, session_id: i64, limit: usize) -> Result<Vec<Thought>> {
        let mut stmt = self
            .conn
            .prepare(
                "SELECT id, session_id, material_id, content, status, created_at \
                 FROM thoughts WHERE session_id = ?1 \
                 ORDER BY created_at DESC LIMIT ?2",
            )
            .context("Failed to prepare recent thoughts query")?;

        let thoughts = stmt
            .query_map(params![session_id, limit as i64], |row| {
                Ok(Thought {
                    id: row.get(0)?,
                    session_id: row.get(1)?,
                    material_id: row.get(2)?,
                    content: row.get(3)?,
                    status: row.get(4)?,
                    created_at: row.get(5)?,
                })
            })
            .context("Failed to query recent thoughts")?
            .collect::<std::result::Result<Vec<_>, _>>()
            .context("Failed to collect thoughts")?;

        Ok(thoughts)
    }

    // --- Idea ---

    /// Insert a new idea (pending status).
    pub fn insert_idea(&self, session_id: i64, content: &str) -> Result<Idea> {
        let now = Utc::now().to_rfc3339();
        self.conn
            .execute(
                "INSERT INTO ideas (session_id, content, status, created_at) VALUES (?1, ?2, 'pending', ?3)",
                params![session_id, content, now],
            )
            .context("Failed to insert idea")?;

        let id = self.conn.last_insert_rowid();
        self.get_idea(id)
    }

    /// Get a single idea by id.
    pub fn get_idea(&self, id: i64) -> Result<Idea> {
        self.conn
            .query_row(
                "SELECT id, session_id, content, status, created_at FROM ideas WHERE id = ?1",
                params![id],
                |row| {
                    Ok(Idea {
                        id: row.get(0)?,
                        session_id: row.get(1)?,
                        content: row.get(2)?,
                        status: row.get(3)?,
                        created_at: row.get(4)?,
                    })
                },
            )
            .context("Failed to get idea")
    }

    /// Update idea status (accept/reject).
    pub fn update_idea_status(&self, id: i64, status: &str) -> Result<()> {
        self.conn
            .execute(
                "UPDATE ideas SET status = ?1 WHERE id = ?2",
                params![status, id],
            )
            .context("Failed to update idea status")?;
        Ok(())
    }

    /// Link an idea to its source thoughts.
    pub fn link_idea_thoughts(&self, idea_id: i64, thought_ids: &[i64]) -> Result<()> {
        let mut stmt = self
            .conn
            .prepare("INSERT INTO idea_thoughts (idea_id, thought_id) VALUES (?1, ?2)")
            .context("Failed to prepare idea_thoughts insert")?;

        for &tid in thought_ids {
            stmt.execute(params![idea_id, tid])
                .context("Failed to insert idea_thoughts link")?;
        }
        Ok(())
    }

    /// Get the latest pending idea for a session.
    pub fn latest_pending_idea(&self, session_id: i64) -> Result<Option<Idea>> {
        let result = self.conn.query_row(
            "SELECT id, session_id, content, status, created_at \
             FROM ideas WHERE session_id = ?1 AND status = 'pending' \
             ORDER BY created_at DESC LIMIT 1",
            params![session_id],
            |row| {
                Ok(Idea {
                    id: row.get(0)?,
                    session_id: row.get(1)?,
                    content: row.get(2)?,
                    status: row.get(3)?,
                    created_at: row.get(4)?,
                })
            },
        );

        match result {
            Ok(idea) => Ok(Some(idea)),
            Err(rusqlite::Error::QueryReturnedNoRows) => Ok(None),
            Err(e) => Err(e).context("Failed to query latest pending idea"),
        }
    }
}
