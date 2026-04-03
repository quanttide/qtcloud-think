#!/usr/bin/env python3
"""
解析 think 日志为记忆卡片

从 docs/archive/journal/think/ 读取原始想法文件，
使用本地 ollama (qwen2.5-coder:3b) 将内容分类为四种记忆类型的卡片，
输出到 data/cards/{episodic,semantic,self,procedural}/ 目录。

用法:
    python scripts/parse_think_cards.py              # 解析所有文件
    python scripts/parse_think_cards.py 2026-03-11   # 只解析指定日期
    python scripts/parse_think_cards.py --dry-run    # 预览模式
"""

import json
import re
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path

# 配置
THINK_DIR = Path("docs/archive/journal/think")
OUTPUT_DIR = Path("data/cards")
OLLAMA_MODEL = "qwen2.5-coder:3b"
OLLAMA_BASE_URL = "http://127.0.0.1:11434"

CARD_TYPES = {
    "episodic": "事件记忆 - 个人经历的、发生在特定时空的具体事件",
    "semantic": "语义记忆 - 客观的、去情境化的知识、事实、概念、规则",
    "self": "自我记忆 - 与自我认知、身份、价值观、情感反思相关的记忆",
    "procedural": "程序性记忆 - 关于怎么做的记忆，技能、流程、操作方法",
}

TENSE_VALUES = ["past", "present", "future"]
TYPE_VALUES = ["decision", "plan", "report", "evaluation", "retrospective"]

SYSTEM_PROMPT = """你是一个记忆卡片分类助手。请将输入的思考日志内容拆解为结构化的记忆卡片。

输出格式：输出一个 JSON 数组，每个元素是一张卡片。

每张卡片字段：
- title: 简短标题（10字以内）
- content: 卡片内容摘要（50字以内）
- category: 四选一: episodic(事件记忆), semantic(语义知识), self(自我认知), procedural(方法流程)
- tense: 三选一: past(过去), present(现在), future(未来)
- card_type: 五选一: decision(决策), plan(计划), report(汇报), evaluation(评估), retrospective(回顾)

规则：
1. 只输出 JSON 数组，不要任何其他文字
2. 提取 5-10 张卡片
3. 忽略 AI 回复的客套话，只提取核心观点
4. 同一主题合并为一张卡片
5. 确保四种类型都有覆盖"""


def call_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    """调用本地 ollama API"""
    import urllib.request
    import urllib.error

    data = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
            "format": "json",
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        f"{OLLAMA_BASE_URL}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "")
    except Exception as e:
        print(f"  [WARN] ollama 调用失败: {e}")
        return ""


def parse_json_from_llm(text: str) -> list[dict]:
    """从 LLM 输出中提取卡片数据"""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    try:
        data = json.loads(text)
        return _normalize_cards(data)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                data = json.loads(match.group())
                return _normalize_cards(data)
            except json.JSONDecodeError:
                pass
        match = re.search(r"\[[\s\S]*\]", text)
        if match:
            try:
                return _normalize_cards(json.loads(match.group()))
            except json.JSONDecodeError:
                pass
    return []


def _normalize_cards(data) -> list[dict]:
    """规范化卡片数据，处理各种嵌套格式"""
    if isinstance(data, dict):
        # 处理 {"cards": [...]} 或 {"data": [...]} 等包装
        for key in ("cards", "data", "items", "results"):
            if key in data and isinstance(data[key], list):
                return [item for item in data[key] if isinstance(item, dict)]
        # 单个卡片对象
        return [data]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def read_think_file(filepath: Path) -> tuple[str, str]:
    """读取 think 日志文件，返回 (date, content)"""
    date_match = filepath.stem
    content = filepath.read_text(encoding="utf-8")
    # 去除 AI 对话的冗余格式，保留核心内容
    return date_match, content


def extract_human_content(content: str) -> str:
    """提取人类原始想法，去除 AI 回复的冗余"""
    lines = content.split("\n")
    filtered = []
    skip_ai = False

    for line in lines:
        # 跳过明显的 AI 回复标记
        if re.match(r"^#{1,3}\s*(第一轮|第二轮|第三轮|第四轮|第五轮)", line):
            skip_ai = True
            continue
        if re.match(r"^#{1,3}\s*(DeepSeek|Kimi|GPT|Claude)", line):
            skip_ai = True
            continue

        # 检测 AI 风格开头
        if re.match(
            r"^(你今天|你今天这段|你今天这段思考|你提到|你的思考|你正在构建|你这个观察)",
            line,
        ):
            skip_ai = True
            continue

        if not skip_ai:
            filtered.append(line)

    result = "\n".join(filtered)
    # 如果过滤后内容太少，返回原始内容
    if len(result) < len(content) * 0.2:
        return content
    return result


def save_card(card: dict, category: str, source_date: str, source_file: str) -> Path:
    """保存卡片到文件"""
    output_dir = OUTPUT_DIR / category
    output_dir.mkdir(parents=True, exist_ok=True)

    card_data = {
        "id": str(uuid.uuid4()),
        "title": card["title"],
        "description": card["content"],
        "category": category,
        "tense": card.get("tense", "present"),
        "type": card.get("card_type", "evaluation"),
        "source_date": source_date,
        "source_file": source_file,
        "created_at": datetime.now().isoformat(),
    }

    # 文件名使用标题的 slug
    slug = re.sub(r"[^\w\u4e00-\u9fff-]", "_", card["title"])[:50]
    filename = f"{source_date}_{slug}.json"
    filepath = output_dir / filename

    filepath.write_text(
        json.dumps(card_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return filepath


def process_file(filepath: Path, dry_run: bool = False) -> list[dict]:
    """处理单个 think 日志文件"""
    date_str, content = read_think_file(filepath)
    human_content = extract_human_content(content)

    print(f"处理: {filepath.name} ({len(human_content)} chars)")

    prompt = (
        f"请将以下思考日志拆解为记忆卡片（JSON 数组格式）：\n\n{human_content[:4000]}"
    )

    if dry_run:
        print(f"  [DRY-RUN] 将调用 ollama 解析")
        return []

    response = call_ollama(prompt)
    if not response:
        print(f"  [WARN] 无响应，跳过")
        return []

    cards = parse_json_from_llm(response)
    if not cards:
        print(f"  [WARN] 解析 JSON 失败")
        print(f"  Raw: {response[:200]}...")
        return []

    saved = []
    for card in cards:
        category = card.get("category", "semantic")
        if category not in CARD_TYPES:
            category = "semantic"

        path = save_card(card, category, date_str, filepath.name)
        saved.append(card)
        print(f"  ✓ [{category}] {card['title']}")

    return saved


def main():
    dry_run = "--dry-run" in sys.argv
    target = None
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            target = arg
            break

    if not THINK_DIR.exists():
        print(f"错误: 找不到 {THINK_DIR}")
        sys.exit(1)

    # 获取要处理的文件
    if target:
        files = sorted(THINK_DIR.glob(f"{target}*.md"))
    else:
        files = sorted(THINK_DIR.glob("*.md"))

    if not files:
        print(f"未找到匹配的 think 日志文件")
        sys.exit(1)

    print(f"将处理 {len(files)} 个文件")
    if dry_run:
        print("[DRY-RUN] 模式，不会实际调用 ollama")

    total_cards = 0
    for filepath in files:
        cards = process_file(filepath, dry_run=dry_run)
        total_cards += len(cards)

    if not dry_run:
        print(f"\n完成! 共生成 {total_cards} 张卡片到 {OUTPUT_DIR}/")
        for cat in CARD_TYPES:
            count = len(list((OUTPUT_DIR / cat).glob("*.json")))
            if count:
                print(f"  {cat}: {count} 张")
    else:
        print(f"\n[DRY-RUN] 预计处理 {len(files)} 个文件")


if __name__ == "__main__":
    main()
