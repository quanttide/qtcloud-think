mod ai;
mod app;
mod config;
mod db;
mod ui;

use anyhow::Result;
use app::AppState;
use crossterm::{
    event::{self, Event, KeyCode, KeyEventKind, KeyModifiers},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::backend::CrosstermBackend;
use ratatui::Terminal;
use std::io;

#[tokio::main]
async fn main() -> Result<()> {
    // Load config
    let config = config::Config::load()?;

    // Initialize state
    let state = AppState::new(config).await?;
    let state = std::sync::Mutex::new(state);

    // Setup terminal
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen)?;
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    // Run the TUI event loop
    let result = run_app(&mut terminal, &state).await;

    // Restore terminal
    disable_raw_mode()?;
    execute!(terminal.backend_mut(), LeaveAlternateScreen)?;
    terminal.show_cursor()?;

    result
}

/// The main TUI event loop.
async fn run_app(
    terminal: &mut Terminal<CrosstermBackend<io::Stdout>>,
    state_mutex: &std::sync::Mutex<AppState>,
) -> Result<()> {
    loop {
        // Render
        {
            let state = state_mutex.lock().unwrap();
            terminal.draw(|frame| ui::render(frame, &state))?;
        }

        // Handle event with timeout for responsive rendering
        if event::poll(std::time::Duration::from_millis(100))? {
            match event::read()? {
                Event::Key(key) => {
                    if key.kind == KeyEventKind::Press {
                        let mut state = state_mutex.lock().unwrap();

                        match key.code {
                            // Quit
                            KeyCode::Char('q') if key.modifiers == KeyModifiers::CONTROL => {
                                state.should_quit = true;
                            }
                            KeyCode::Esc => {
                                state.should_quit = true;
                            }

                            // Enter: submit thought
                            KeyCode::Enter => {
                                // Check for command mode
                                if state.input.starts_with(':') {
                                    handle_command(&mut state).await;
                                } else {
                                    let _ = state.submit_thought().await;
                                }
                            }

                            // Accept idea
                            KeyCode::Char('y') => {
                                let _ = state.accept_idea().await;
                            }

                            // Reject idea
                            KeyCode::Char('n') => {
                                let _ = state.reject_idea().await;
                            }

                            // Retry
                            KeyCode::Char('r') => {
                                state.retry_ai().await;
                            }

                            // Backspace
                            KeyCode::Backspace => {
                                state.input.pop();
                            }

                            // Typing
                            KeyCode::Char(c) => {
                                state.input.push(c);
                            }

                            _ => {}
                        }

                        if state.should_quit {
                            break;
                        }
                    }
                }
                Event::Resize(_, _) => {
                    // Render will handle the new size on next draw
                }
                _ => {}
            }
        }

        // Check if we should quit
        if state_mutex.lock().unwrap().should_quit {
            break;
        }
    }

    Ok(())
}

/// Handle command-mode input (lines starting with `:`).
async fn handle_command(state: &mut AppState) {
    let cmd = state.input.trim_start_matches(':').trim().to_string();
    state.input.clear();

    let parts: Vec<&str> = cmd.splitn(2, ' ').collect();
    match parts[0] {
        "quit" | "q" => {
            state.should_quit = true;
        }
        "help" | "h" => {
            show_help(state);
        }
        "material" | "m" => {
            if let Some(path) = parts.get(1) {
                match state.set_material(path).await {
                    Ok(_msg) => {
                        state.error_message = None;
                        // Store feedback as a temporary thought-like display
                    }
                    Err(e) => {
                        state.error_message = Some(e.to_string());
                    }
                }
            } else {
                state.error_message = Some("用法: :material <路径>".to_string());
            }
        }
        "session" | "s" => {
            if let Some(title) = parts.get(1) {
                let _ = state.new_session(title).await;
            } else {
                state.error_message = Some("用法: :session <标题>".to_string());
            }
        }
        _ => {
            state.error_message = Some(format!("未知命令: :{}", parts[0]));
        }
    }
}

/// Show help information in the idea panel.
fn show_help(state: &mut AppState) {
    let help_text = "\
可用命令:
  :quit / :q     退出
  :help / :h     显示帮助
  :material <路径>  加载材料文件
  :session <标题>   新建会话

快捷键:
  Enter      提交念头
  y / n      接受/拒绝想法
  r          重试 AI
  Ctrl+q     退出
  Esc        退出";

    // Store help as a transient message via error_message (reused as info area)
    state.error_message = None;
    // We'll use current_idea as a temporary display
    // For simplicity, we just set a message that gets displayed
    // A better approach would be a dedicated status field
    println!("{}", help_text);
}
