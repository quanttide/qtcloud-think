use crate::app::AppState;
use ratatui::{
    layout::{Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span, Text},
    widgets::{Block, BorderType, Borders, List, ListItem, Paragraph, Wrap},
    Frame,
};

/// Render the entire TUI layout.
pub fn render(frame: &mut Frame, state: &AppState) {
    let area = frame.area();

    // Outer block: title bar
    let title = format!(" 思考云 - {} (按 :help 查看命令) ", state.session_title());
    let outer_block = Block::default()
        .title(title)
        .borders(Borders::ALL)
        .border_type(BorderType::Rounded)
        .border_style(Style::default().fg(Color::Cyan));

    let inner = outer_block.inner(area);
    frame.render_widget(outer_block, area);

    // Split into main area (top) and input bar (bottom)
    let main_chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([Constraint::Min(3), Constraint::Length(3)])
        .split(inner);

    render_main_area(frame, main_chunks[0], state);
    render_input_bar(frame, main_chunks[1], state);
}

/// Render the main content area (left: thoughts, right: idea).
fn render_main_area(frame: &mut Frame, area: Rect, state: &AppState) {
    let chunks = Layout::default()
        .direction(Direction::Horizontal)
        .constraints([Constraint::Ratio(1, 2), Constraint::Ratio(1, 2)])
        .split(area);

    render_thoughts_panel(frame, chunks[0], state);
    render_idea_panel(frame, chunks[1], state);
}

/// Left panel: list of recent thoughts.
fn render_thoughts_panel(frame: &mut Frame, area: Rect, state: &AppState) {
    let block = Block::default()
        .title("念头流")
        .borders(Borders::ALL)
        .border_style(Style::default().fg(Color::Blue));

    let thoughts: Vec<ListItem> = state
        .thoughts
        .iter()
        .enumerate()
        .map(|(_, t)| {
            let prefix = match t.status.as_str() {
                "failed" => "✗",
                "processing" => "⟳",
                "completed" => "✓",
                _ => ">",
            };
            let style = match t.status.as_str() {
                "failed" => Style::default().fg(Color::Red),
                "processing" => Style::default().fg(Color::Yellow),
                _ => Style::default(),
            };
            ListItem::new(Line::from(vec![
                Span::styled(format!("{} ", prefix), style),
                Span::raw(&t.content),
            ]))
        })
        .collect();

    let list = List::new(thoughts)
        .block(block)
        .highlight_style(Style::default().add_modifier(Modifier::BOLD));

    frame.render_widget(list, area);
}

/// Right panel: current idea display.
fn render_idea_panel(frame: &mut Frame, area: Rect, state: &AppState) {
    let block = Block::default()
        .title("最新想法")
        .borders(Borders::ALL)
        .border_style(Style::default().fg(Color::Green));

    let (content, _actions_style) = match &state.current_idea {
        Some(idea) => match idea.status.as_str() {
            "pending" => (
                vec![
                    Line::from(Span::raw(&idea.content)),
                    Line::from(""),
                    Line::from(Span::styled(
                        "[y] 接受  [n] 拒绝  [r] 重试",
                        Style::default()
                            .fg(Color::Yellow)
                            .add_modifier(Modifier::BOLD),
                    )),
                ],
                Style::default().fg(Color::Yellow),
            ),
            "accepted" => (
                vec![
                    Line::from(Span::raw(&idea.content)),
                    Line::from(""),
                    Line::from(Span::styled(
                        "✓ 已接受",
                        Style::default()
                            .fg(Color::Green)
                            .add_modifier(Modifier::BOLD),
                    )),
                ],
                Style::default().fg(Color::Green),
            ),
            "rejected" => (
                vec![Line::from(Span::raw("想法已拒绝，继续输入新念头..."))],
                Style::default().fg(Color::DarkGray),
            ),
            _ => (vec![Line::from(Span::raw(&idea.content))], Style::default()),
        },
        None => {
            if state.is_processing {
                (
                    vec![Line::from(Span::styled(
                        "⟳ AI 正在思考中...",
                        Style::default().fg(Color::Yellow),
                    ))],
                    Style::default(),
                )
            } else {
                (
                    vec![Line::from(Span::styled(
                        "输入念头后按回车，AI 将自动生成想法",
                        Style::default().fg(Color::DarkGray),
                    ))],
                    Style::default(),
                )
            }
        }
    };

    // Error display
    let mut lines = content;
    if let Some(ref err) = state.error_message {
        lines.push(Line::from(""));
        lines.push(Line::from(Span::styled(
            format!("错误: {}", err),
            Style::default().fg(Color::Red),
        )));
        lines.push(Line::from(Span::styled(
            "[r] 重试",
            Style::default().fg(Color::Red).add_modifier(Modifier::BOLD),
        )));
    }

    let paragraph = Paragraph::new(Text::from(lines))
        .block(block)
        .wrap(Wrap { trim: false });

    frame.render_widget(paragraph, area);
}

/// Bottom input bar.
fn render_input_bar(frame: &mut Frame, area: Rect, state: &AppState) {
    let input_block = Block::default()
        .title("输入新念头")
        .borders(Borders::ALL)
        .border_style(Style::default().fg(Color::Magenta));

    let input_text = if state.input.is_empty() {
        Text::from(Line::from(Span::styled(
            "输入念头后按回车...",
            Style::default().fg(Color::DarkGray),
        )))
    } else {
        Text::from(Line::from(Span::raw(&state.input)))
    };

    let paragraph = Paragraph::new(input_text).block(input_block);
    frame.render_widget(paragraph, area);
}
