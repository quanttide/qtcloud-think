import uuid

import typer
from clarifier import Clarifier
from meta import Meta
from session_recorder import SessionRecorder
from storage import Storage
from workspace import Workspace

app = typer.Typer(help="思维收集与澄清工具")


@app.command()
def collect(
    workspace: str = typer.Option(
        "default",
        "--workspace",
        "-w",
        help="指定工作空间",
    ),
):
    """收集并澄清你的想法"""
    ws = Workspace(workspace)
    typer.echo(f"📁 当前工作空间: {ws.name}\n")

    session_id = str(uuid.uuid4())
    recorder = SessionRecorder(session_id)
    clarifier = Clarifier(recorder)
    storage = Storage(ws)

    typer.echo("欢迎使用思维澄清工具！请输入你的想法（输入 '退出' 结束）\n")

    original_input = typer.prompt("你的想法是什么？")
    if original_input.strip() in ("退出", "exit", "q"):
        recorder.record_user_abandoned()
        recorder.end_session()
        return

    typer.echo("\n正在分析想法清晰度...\n")
    result = clarifier.check_clarity(original_input)
    recorder.record_round()
    recorder.record_intent_captured(result.get("is_clear", False))

    conversation = [{"role": "user", "content": original_input}]

    while not result.get("is_clear", False):
        issues = result.get("issues", ["内容不够清晰"])
        typer.echo(f"💭 发现问题: {', '.join(issues)}\n")

        response = clarifier.ask_clarification(original_input, issues)
        typer.echo(f"🤖 {response}\n")

        conversation.append({"role": "assistant", "content": response})

        user_reply = typer.prompt("请补充信息（输入 '完成' 结束澄清）")
        if user_reply.strip() in ("完成", "done", "finish"):
            conversation.append({"role": "user", "content": user_reply})
            recorder.record_user_abandoned()
            break

        conversation.append({"role": "user", "content": user_reply})

        typer.echo("\n正在重新分析...\n")
        result = clarifier.check_clarity(user_reply)
        recorder.record_round()
        recorder.record_intent_captured(result.get("is_clear", False))

    typer.echo("✅ 想法已澄清！正在生成总结...\n")
    clarified = clarifier.summarize(conversation)

    lines = clarified.split("\n")
    summary = ""
    content = ""
    in_content = False
    for line in lines:
        if line.startswith("summary:"):
            summary = line.replace("summary:", "").strip().strip('"')
        elif line.startswith("content:"):
            in_content = True
            content = line.replace("content:", "").strip()
        elif in_content:
            content += "\n" + line

    filepath = storage.save(original_input, content.strip(), summary)
    recorder.record_storage(True, str(filepath))

    typer.echo(f"✅ 已保存到: {filepath}")
    typer.echo(f"\n摘要: {summary}")


@app.command()
def meta(
    workspace: str = typer.Option(
        "default",
        "--workspace",
        "-w",
        help="指定要分析的工作空间",
    ),
):
    """触发 Meta 自省分析"""
    from session_recorder import SessionRecord

    ws = Workspace(workspace)
    meta = Meta(ws)

    typer.echo(f"📊 正在分析工作空间: {ws.name}\n")

    notes_dir = ws.get_notes_dir()
    if not notes_dir.exists() or not list(notes_dir.glob("*.md")):
        typer.echo("⚠️ 该工作空间没有笔记数据")
        return

    sample_record = SessionRecord(session_id="manual-trigger")
    sample_record.rounds = 1
    sample_record.api_calls = 1

    filepath = meta.save(sample_record)

    typer.echo(f"✅ Meta 自省报告已生成: {filepath}")


if __name__ == "__main__":
    app()
