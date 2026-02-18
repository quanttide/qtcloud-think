import uuid

import typer
from clarifier import Clarifier
from meta import Meta
from session_recorder import SessionRecorder
from storage import Storage

app = typer.Typer(help="思维收集与澄清工具")


@app.command()
def collect():
    """收集并澄清你的想法"""
    session_id = str(uuid.uuid4())
    recorder = SessionRecorder(session_id)
    clarifier = Clarifier(recorder)
    storage = Storage()
    meta = Meta()

    typer.echo("欢迎使用思维澄清工具！请输入你的想法（输入 '退出' 结束）\n")

    original_input = typer.prompt("你的想法是什么？")
    if original_input.strip() in ("退出", "exit", "q"):
        recorder.record_user_abandoned()
        record = recorder.end_session()
        meta.save(record)
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

    record = recorder.end_session()
    meta_filepath = meta.save(record)

    typer.echo(f"✅ 已保存到: {filepath}")
    typer.echo(f"\n摘要: {summary}")
    typer.echo(f"\n📊 Meta 自省报告已保存到: {meta_filepath}")

    analysis = meta.analyze(record)
    if analysis["issues"]:
        typer.echo("\n⚠️ 发现问题:")
        for issue in analysis["issues"]:
            typer.echo(f"  - {issue}")
    if analysis["suggestions"]:
        typer.echo("\n💡 改进建议:")
        for suggestion in analysis["suggestions"]:
            typer.echo(f"  - {suggestion}")


if __name__ == "__main__":
    app()
