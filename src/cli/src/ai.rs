use crate::config::Config;
use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};

/// AI client for calling LLM APIs.
pub struct AiClient {
    config: Config,
    client: reqwest::Client,
}

#[derive(Debug, Serialize, Deserialize)]
struct ChatMessage {
    role: String,
    content: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct ChatRequest {
    model: String,
    messages: Vec<ChatMessage>,
    stream: bool,
}

#[derive(Debug, Deserialize)]
struct ChatResponse {
    choices: Vec<Choice>,
}

#[derive(Debug, Deserialize)]
struct Choice {
    message: ChatMessage,
}

/// Context data prepared for the AI call.
pub struct AiContext {
    pub thought_texts: Vec<(i64, String)>,
    pub total_thought_count: usize,
    pub thought_window: usize,
}

impl AiClient {
    pub fn new(config: Config) -> Self {
        Self {
            client: reqwest::Client::new(),
            config,
        }
    }

    /// Build a context string from thoughts.
    fn build_context(context: &AiContext) -> String {
        let mut lines: Vec<String> = Vec::new();

        let total = context.total_thought_count;
        let window = context.thought_window;

        if total > window {
            lines.push(format!("……（之前还有 {} 条念头）", total - window));
        }

        // thought_texts are already newest-first; reverse to chronological order
        for (i, (_, content)) in context.thought_texts.iter().rev().enumerate() {
            lines.push(format!("{}. {}", i + 1, content));
        }

        lines.join("\n")
    }

    /// Call the AI API and return the generated idea text.
    /// No DB access — pure HTTP call.
    pub async fn generate_idea(&self, context: &AiContext) -> Result<String> {
        let context_str = Self::build_context(context);

        let api_key = self
            .config
            .api_key()
            .context("API key not found. Set THINKCLOUD_API_KEY environment variable.")?;

        let system_prompt = "你是一个认知工程助手。用户会输入一系列「念头」（短文本），\
            请分析这些念头后给出一个总结性的「想法」——即洞察、结论或下一步行动建议。\
            保持简洁，不超过 200 字。直接输出想法内容，不要加前缀。";

        let request = ChatRequest {
            model: self.config.ai.model.clone(),
            messages: vec![
                ChatMessage {
                    role: "system".to_string(),
                    content: system_prompt.to_string(),
                },
                ChatMessage {
                    role: "user".to_string(),
                    content: format!("以下是用户当前的念头序列：\n\n{}", context_str),
                },
            ],
            stream: false,
        };

        let base_url = self.config.ai.base_url.trim_end_matches('/');
        let url = format!("{}/chat/completions", base_url);

        let response = self
            .client
            .post(&url)
            .header("Authorization", format!("Bearer {}", api_key))
            .json(&request)
            .send()
            .await
            .with_context(|| "Failed to send AI request")?;

        if !response.status().is_success() {
            let status = response.status();
            let body = response.text().await.unwrap_or_default();
            anyhow::bail!("AI API error ({}): {}", status, body);
        }

        let chat_response: ChatResponse = response
            .json()
            .await
            .context("Failed to parse AI response")?;

        let idea_text = chat_response
            .choices
            .first()
            .map(|c| c.message.content.clone())
            .unwrap_or_default();

        if idea_text.is_empty() {
            anyhow::bail!("AI returned empty response");
        }

        Ok(idea_text)
    }
}

impl AiContext {
    /// Build context from raw thought data (id, content, newest-first).
    pub fn new(
        thought_texts: Vec<(i64, String)>,
        total_thought_count: usize,
        thought_window: usize,
    ) -> Self {
        Self {
            thought_texts,
            total_thought_count,
            thought_window,
        }
    }
}
