import uuid

import typer
from clarifier import Clarifier
from meta import Meta
from prompts import META_ANALYSIS_PROMPT
from session_recorder import SessionRecorder
from storage import Storage
from workspace import Workspace

app = typer.Typer(help="思维收集与澄清工具")


def read_multiline(prompt_text: str) -> str:
    """读取多行输入，连续两个空行结束"""
    typer.echo(f"{prompt_text}（连续两个空行结束）\n")
    lines = []
    empty_count = 0
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            empty_count += 1
            if empty_count >= 2:
                break
            continue
        empty_count = 0
        lines.append(line)
    return "\n".join(lines).strip()


def run_collect(workspace: str = "default") -> None:
    """执行 collect 逻辑"""
    ws = Workspace(workspace)
    typer.echo(f"📁 当前工作空间: {ws.name}\n")

    session_id = str(uuid.uuid4())
    recorder = SessionRecorder(session_id)
    clarifier = Clarifier(recorder)
    storage = Storage(ws)

    typer.echo("欢迎使用思维外脑！\n")

    original_input = read_multiline("请输入你的想法")
    if not original_input:
        typer.echo("⚠️ 请输入想法")
        return

    conversation = [{"role": "user", "content": original_input}]

    typer.echo("\n🪞 让我复述一下你的想法...\n")
    reflection = clarifier.reflect(original_input)
    typer.echo(f"{reflection}\n")

    while True:
        choice = typer.prompt(
            "\n请选择：\n1. 补充更多信息\n2. 已有足够信息，结束澄清\n请输入 1/2",
            default="2",
        ).strip()

        if choice == "2" or not choice:
            break

        user_reply = read_multiline("请补充")
        if not user_reply:
            continue

        conversation.append({"role": "user", "content": user_reply})
        recorder.record_round()

        typer.echo("\n🪞 让我再帮你理清一下...\n")
        reflection = clarifier.reflect(user_reply)
        typer.echo(f"{reflection}\n")

    typer.echo("✅ 正在生成总结...\n")
    clarified = clarifier.summarize(conversation)

    summary = clarified.get("summary", "")
    content = clarified.get("content", "")

    while True:
        typer.echo("\n" + "=" * 40)
        typer.echo("📝 澄清结果：")
        typer.echo("=" * 40)
        typer.echo(f"\n摘要：{summary}\n")
        typer.echo("-" * 40)
        typer.echo(f"内容：\n{content}\n")
        typer.echo("=" * 40)

        choice = typer.prompt(
            "\n请选择：\n"
            "1. 接收 - 存入长期记忆\n"
            "2. 修改 - 调整摘要或内容\n"
            "3. 拒绝 - 丢弃（可填写原因）\n"
            "4. 悬疑 - 暂存待定\n"
            "请输入 1/2/3/4",
            default="1",
        ).strip()

        if choice in ("2", "修改"):
            edit_choice = typer.prompt(
                "修改什么？\n1. 摘要\n2. 内容\n请输入 1/2",
            ).strip()
            if edit_choice == "1":
                summary = typer.prompt("请输入新摘要", default=summary)
            elif edit_choice == "2":
                typer.echo("请输入新内容（连续两个空行结束）：")
                content = read_multiline("") or content
            continue

        if choice in ("1", "接收"):
            status = "received"
            rejection_reason = None
            break
        elif choice in ("4", "悬疑"):
            status = "pending"
            rejection_reason = None
            break
        elif choice in ("3", "拒绝"):
            status = "rejected"
            reason_choice = (
                typer.prompt("是否填写拒绝原因？(y/n)", default="n").strip().lower()
            )
            if reason_choice in ("y", "是"):
                rejection_reason = typer.prompt("请输入拒绝原因（可选）")
            else:
                rejection_reason = None
            break
        else:
            typer.echo("⚠️ 请输入 1、2、3 或 4")

    filepath = storage.save(
        original_input,
        content,
        summary,
        session_record=recorder.record.to_dict(),
        status=status,
        rejection_reason=rejection_reason,
    )

    storage.save_conversation(conversation, summary, session_id)

    recorder.record_storage(True, str(filepath))
    recorder.end_session()

    if status == "received":
        typer.echo(f"✅ 已保存到长期记忆: {filepath}")
    elif status == "pending":
        typer.echo(f"⏳ 已暂存到待定: {filepath}")
    elif status == "rejected":
        typer.echo(f"❌ 已拒绝: {filepath}")

    typer.echo(f"\n摘要: {summary}")


@app.command()
def pending(
    workspace: str = typer.Option(
        "default",
        "--workspace",
        "-w",
        help="指定工作空间",
    ),
):
    """列出所有悬疑待定的内容"""
    ws = Workspace(workspace)
    storage = Storage(ws)

    pending_notes = storage.list_pending()

    if not pending_notes:
        typer.echo("📭 当前没有悬疑待定的内容")
        return

    typer.echo(f"📋 悬疑待定内容 ({len(pending_notes)} 条)：\n")

    for i, note in enumerate(pending_notes, 1):
        typer.echo(f"{i}. {note['summary']}")
        typer.echo(f"   ID: {note['id']}")
        typer.echo(f"   创建时间: {note['created']}")
        typer.echo(f"   原始输入: {note['original'][:50]}...")
        typer.echo()


@app.command()
def review(
    workspace: str = typer.Option(
        "default",
        "--workspace",
        "-w",
        help="指定工作空间",
    ),
):
    """对悬疑待定内容进行重新决策"""
    ws = Workspace(workspace)
    storage = Storage(ws)

    pending_notes = storage.list_pending()

    if not pending_notes:
        typer.echo("📭 当前没有悬疑待定的内容")
        return

    typer.echo(f"📋 悬疑待定内容 ({len(pending_notes)} 条)：\n")

    for i, note in enumerate(pending_notes, 1):
        typer.echo(f"\n{'=' * 40}")
        typer.echo(f"{i}. {note['summary']}")
        typer.echo(f"   原始输入: {note['original']}")
        typer.echo("=" * 40)

        filepath = note["filepath"]
        content = filepath.read_text(encoding="utf-8")
        frontmatter, body = storage._parse_frontmatter(content)
        typer.echo(f"\n内容:\n{body}\n")

        while True:
            choice = typer.prompt(
                "\n请选择：\n"
                "1. 接收 - 存入长期记忆\n"
                "2. 拒绝 - 丢弃（可填写原因）\n"
                "3. 跳过 - 保留在待定\n"
                "请输入 1/2/3",
                default="3",
            ).strip()

            if choice in ("1", "接收"):
                storage.move_file(
                    note["id"],
                    ws.get_pending_dir(),
                    "received",
                )
                typer.echo("✅ 已接收，移至长期记忆")
                break
            elif choice in ("2", "拒绝"):
                reason_choice = (
                    typer.prompt("是否填写拒绝原因？(y/n)", default="n").strip().lower()
                )
                if reason_choice in ("y", "是"):
                    rejection_reason = typer.prompt("请输入拒绝原因")
                else:
                    rejection_reason = None
                storage.move_file(
                    note["id"],
                    ws.get_pending_dir(),
                    "rejected",
                    rejection_reason,
                )
                typer.echo("❌ 已拒绝")
                break
            elif choice in ("3", "跳过"):
                typer.echo("⏭️ 跳过")
                break
            else:
                typer.echo("⚠️ 请输入 1、2 或 3")

    typer.echo("\n✅ 审查完成")


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
    run_collect(workspace)


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
    import json

    from clarifier import Clarifier
    from session_recorder import SessionRecord

    target_ws = Workspace(workspace)
    meta_obj = Meta()

    typer.echo(f"📊 正在分析工作空间: {target_ws.name}\n")

    sessions_dir = target_ws.get_notes_dir().parent / "sessions"
    if not sessions_dir.exists():
        typer.echo(f"⚠️ 工作空间 '{target_ws.name}' 没有会话数据")
        return

    # 读取会话记录和对话历史
    sessions = []
    conversations = []

    for f in sessions_dir.glob("session_*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        sessions.append(SessionRecord.from_dict(data))

    for f in sessions_dir.glob("conversation_*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        conversations.append(data)

    if not sessions or not conversations:
        typer.echo(f"⚠️ 工作空间 '{target_ws.name}' 没有会话数据")
        return

    # 汇总分析
    total_rounds = sum(s.rounds for s in sessions)
    total_api_calls = sum(s.api_calls for s in sessions)
    total_duration = sum(s.duration for s in sessions)
    abandoned_count = sum(1 for s in sessions if s.user_abandoned)
    storage_failed_count = sum(1 for s in sessions if not s.storage_success)

    avg_rounds = total_rounds / len(sessions)
    avg_api_calls = total_api_calls / len(sessions)
    avg_duration = total_duration / len(sessions)

    # 异常检测
    issues = []
    suggestions = []

    if avg_rounds > 5:
        issues.append(f"平均澄清轮次过多: {avg_rounds:.1f}")
        suggestions.append("建议优化首轮意图识别，减少澄清轮次")

    if avg_duration > 120:
        issues.append(f"平均耗时过长: {avg_duration:.1f}s")
        suggestions.append("建议检查 LLM 响应速度")

    if avg_api_calls > 10:
        issues.append(f"平均 API 调用过多: {avg_api_calls:.1f}")
        suggestions.append("建议合并 API 调用或优化逻辑")

    if abandoned_count > 0:
        issues.append(f"用户中断次数: {abandoned_count}/{len(sessions)}")
        suggestions.append("追问方式可能不够友好，需要优化")

    if storage_failed_count > 0:
        issues.append(f"存储失败次数: {storage_failed_count}/{len(sessions)}")
        suggestions.append("检查存储路径和权限")

    # 语义分析（使用 LLM）
    typer.echo("🔍 正在进行语义分析...\n")

    conversation_texts = []
    for conv in conversations[:5]:  # 分析最近5次对话
        summary = conv.get("summary", "")
        msgs = conv.get("conversation", [])
        conversation_texts.append(f"总结: {summary}\n对话: {msgs}")

    if conversation_texts:
        analysis_prompt = META_ANALYSIS_PROMPT.format(
            conversations="\n".join(conversation_texts)
        )

        try:
            clarifier = Clarifier()
            result = clarifier.client.chat_once(
                "你是一个系统自省分析师，擅长分析对话并给出改进建议。直接返回 JSON，不要有其他内容。",
                analysis_prompt,
            )
            llm_result = json.loads(result.strip().strip("```json").strip("```"))
            suggestions.extend(llm_result.get("suggestions", []))
        except Exception:
            pass

    # 生成报告（duration 是计算属性，通过 start_time/end_time 自动计算）
    from datetime import datetime, timedelta

    record = SessionRecord(
        session_id="meta-analysis",
        start_time=datetime.now() - timedelta(seconds=int(total_duration)),
        end_time=datetime.now(),
    )
    record.rounds = total_rounds
    record.api_calls = total_api_calls

    filepath = meta_obj.save(
        record,
        analysis={
            "session_count": len(sessions),
            "avg_rounds": avg_rounds,
            "avg_api_calls": avg_api_calls,
            "avg_duration": avg_duration,
            "abandoned_count": abandoned_count,
            "storage_failed_count": storage_failed_count,
            "issues": issues,
            "suggestions": suggestions,
        },
    )

    # 输出摘要
    typer.echo(f"📈 分析了 {len(sessions)} 次会话\n")
    typer.echo(f"平均轮次: {avg_rounds:.1f}")
    typer.echo(f"平均 API 调用: {avg_api_calls:.1f}")
    typer.echo(f"平均耗时: {avg_duration:.1f}s")

    if issues:
        typer.echo("\n⚠️ 发现问题:")
        for issue in issues:
            typer.echo(f"  - {issue}")

    if suggestions:
        typer.echo("\n💡 改进建议:")
        for suggestion in suggestions:
            typer.echo(f"  - {suggestion}")

    typer.echo(f"\n✅ Meta 自省报告已生成: {filepath}")


if __name__ == "__main__":
    app()
