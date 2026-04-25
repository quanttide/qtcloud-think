#!/usr/bin/env python3
"""
记忆卡片画像报告

读取 data/cards/ 下的所有记忆卡片，按四种记忆类型分别总结，
刻画作者的认知特征、知识体系、自我认知和行为模式。

输出到 data/report/profile.md

用法:
    python scripts/generate_profile_report.py
    python scripts/generate_profile_report.py --output data/report/custom.md
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import urllib.request
import urllib.error

CARDS_DIR = Path("data/cards")
DEFAULT_OUTPUT = Path("data/report/profile.md")
OLLAMA_MODEL = "qwen2.5-coder:3b"
OLLAMA_BASE_URL = "http://127.0.0.1:11434"

CATEGORY_PROFILES = {
    "episodic": {
        "title": "事件记忆画像",
        "desc": "作者经历过的重要事件、决策时刻、关键转折点",
        "prompt": """你是一位心理分析师。请根据以下事件记忆卡片，分析作者的经历特征。

分析维度：
1. 关注焦点：作者最关心什么类型的事情？
2. 决策风格：作者如何做决策？有什么特点？
3. 行为模式：从事件中可以观察到什么重复出现的行为？
4. 关键转折：哪些事件标志着重要的认知或行为转变？

重要约束：
- 只基于卡片中明确出现的内容作答，不要从"卡片缺少某类内容"推断"作者忽视某方面"
- 日志的功能定位可能导致某些内容缺失，这不等于作者不关心
- 每条推断必须直接引用卡片 description 字段的原文作为证据，格式：> "原文"（卡片标题, 日期）
- 标注每条推断的置信度：[高] 有多处卡片支撑 / [中] 有1-2处支撑 / [低] 仅为合理推测

输出 Markdown 格式的分析报告，200-400 字。""",
    },
    "semantic": {
        "title": "语义记忆画像",
        "desc": "作者掌握的知识、概念、规则和客观认知",
        "prompt": """你是一位知识分析师。请根据以下语义记忆卡片，分析作者的知识体系。

分析维度：
1. 知识结构：作者的知识分布在哪些领域？
2. 认知深度：作者对哪些概念有深入理解？
3. 知识偏好：作者倾向于什么类型的知识？（注意：不要简单归类为"技术+管理"，卡片中涉及的可能是"元工具设计"、"认知架构"、"知识工程"等更交叉的领域，请根据卡片内容给出更精确的交叉学科描述）
4. 知识前沿：作者正在主动探索或推进的边界是什么？（注意：卡片中提到的挑战可能是正在攻克的前沿，而非盲区）

重要约束：
- 区分"知识盲区"和"正在探索的前沿"：如果卡片提到某个领域的挑战，可能是作者正在主动处理，不等于不懂
- 不要从"卡片未提及某领域"推断"作者不了解该领域"
- 每条推断必须直接引用卡片 description 字段的原文作为证据，格式：> "原文"（卡片标题, 日期）
- 标注每条推断的置信度：[高] 有多处卡片支撑 / [中] 有1-2处支撑 / [低] 仅为合理推测

输出 Markdown 格式的分析报告，200-400 字。""",
    },
    "self": {
        "title": "自我记忆画像",
        "desc": "作者的自我认知、价值观、情感反思和身份认同",
        "prompt": """你是一位人格分析师。请根据以下自我记忆卡片，分析作者的自我认知和人格特征。

分析维度：
1. 核心信念：作者最深层的价值观和信念是什么？
2. 自我期待：作者想成为什么样的人？
3. 内在冲突：作者面临哪些内在张力或矛盾？
4. 成长轨迹：从自我反思中可以看出怎样的成长路径？

重要约束：
- 不要从"卡片缺少情感内容"推断"作者忽视情感"，日志的功能定位可能导致内容偏向工作思考
- 严格区分以下两类情况：
  - "困惑/探索中的不确定"：对某个技术问题的困惑、对方案的选择困难 → 应描述为"技术攻关中的探索"或"方案权衡"
  - "迷茫/方向不清"：完全不知道要做什么、失去目标感 → 只有卡片明确表达"失去方向感"时才可使用
  - 如果卡片描述的是对某个具体问题（如 openCLAW 改造）的困惑，绝不能等同于"工作方向迷茫"
- 内在冲突应描述为"张力"或"待解决的挑战"，避免使用"迷茫"、"迷失"、"方向不清"等负面定性词汇，除非卡片原文如此表述
- 每条推断必须直接引用卡片 description 字段的原文作为证据，格式：> "原文"（卡片标题, 日期）
- 标注每条推断的置信度：[高] 有多处卡片支撑 / [中] 有1-2处支撑 / [低] 仅为合理推测

输出 Markdown 格式的分析报告，200-400 字。""",
    },
    "procedural": {
        "title": "程序性记忆画像",
        "desc": "作者的方法论、工作流程、技能和问题解决模式",
        "prompt": """你是一位方法论分析师。请根据以下程序性记忆卡片，分析作者的工作方法和技能特征。

分析维度：
1. 工作风格：作者偏好什么样的工作方式？
2. 问题解决：作者面对问题时的典型应对策略是什么？
3. 技能分布：作者在哪些方面有方法论积累？
4. 效率模式：作者如何提升自己的效率？

重要约束：
- 每条推断必须直接引用卡片 description 字段的原文作为证据，格式：> "原文"（卡片标题, 日期）
- 标注每条推断的置信度：[高] 有多处卡片支撑 / [中] 有1-2处支撑 / [低] 仅为合理推测

输出 Markdown 格式的分析报告，200-400 字。""",
    },
}


def load_cards() -> dict[str, list[dict]]:
    """加载所有卡片，按类别分组"""
    cards_by_cat = {}
    for cat in CATEGORY_PROFILES:
        cat_dir = CARDS_DIR / cat
        if not cat_dir.exists():
            cards_by_cat[cat] = []
            continue
        cards = []
        for f in sorted(cat_dir.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            cards.append(data)
        cards_by_cat[cat] = cards
    return cards_by_cat


def call_ollama(prompt: str, system: str, model: str = OLLAMA_MODEL) -> str:
    """调用本地 ollama"""
    data = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "system": system,
            "stream": False,
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
        return f"[调用失败: {e}]"


def build_cards_text(cards: list[dict]) -> str:
    """将卡片列表转为文本"""
    lines = []
    for i, card in enumerate(cards, 1):
        lines.append(f"卡片{i}: [{card.get('tense', '?')}] {card['title']}")
        lines.append(f"  日期: {card.get('source_date', '未知')}")
        lines.append(f"  {card.get('description', '')}")
        lines.append("")
    return "\n".join(lines)


def generate_profile(cards_by_cat: dict[str, list[dict]]) -> str:
    """生成画像报告"""
    sections = []

    for cat, info in CATEGORY_PROFILES.items():
        cards = cards_by_cat.get(cat, [])
        if not cards:
            sections.append(f"## {info['title']}\n\n（无数据）\n")
            continue

        cards_text = build_cards_text(cards)
        prompt = f"请分析以下{info['title']}卡片，刻画作者的特征：\n\n{cards_text}"

        print(f"  分析: {info['title']} ({len(cards)} 张卡片)")
        analysis = call_ollama(prompt, info["prompt"])

        sections.append(f"## {info['title']}\n\n{info['desc']}\n\n{analysis}\n")

    return "\n".join(sections)


def generate_cross_analysis(cards_by_cat: dict[str, list[dict]]) -> str:
    """生成跨类别综合分析"""
    # 收集所有卡片的完整内容
    all_cards_text = []
    for cat, cards in cards_by_cat.items():
        for card in cards:
            all_cards_text.append(
                f"[{cat}] [{card.get('tense', '?')}] {card['title']}\n"
                f"  日期: {card.get('source_date', '未知')}\n"
                f"  {card.get('description', '')}\n"
            )

    if not all_cards_text:
        return ""

    cross_prompt = """你是一位跨领域分析师。请根据以下来自四种记忆类型的卡片，识别跨类别的模式和关联。

每个分析维度必须按以下格式输出：

### 维度名称
**结论**：...
**证据**：
> "原文"（卡片标题, 日期）
> "原文"（卡片标题, 日期）

**置信度**：[高/中/低] 理由

重点分析以下维度：
1. 元认知偏好：作者是否经常"对思考方式进行思考"？有哪些证据？
2. 工具迭代频率：从日志分类到版本管理到外脑构建，工具迭代的速度和模式反映了什么？
3. 跨界特征：作者在写作与技术之间的张力或融合（如用结构化方法构建故事、写作需求与技术实现的交叉）
4. 回环效应：记录→分析→调整记录方式，是否形成了一个自我强化的循环？

重要约束：
- 必须直接引用卡片 description 字段的原文作为证据，不能只给卡片编号或转述
- 区分"数据缺失"与"真实特征"，不要从缺少某类内容推断作者忽视某方面
- 标注每条推断的置信度：[高] 有多处卡片支撑 / [中] 有1-2处支撑 / [低] 仅为合理推测

输出 Markdown 格式的分析报告，300-500 字。"""

    prompt = "请分析以下跨类别的记忆卡片数据，识别隐藏的模式和关联：\n\n" + "\n".join(
        all_cards_text
    )

    print("  生成跨类别综合分析...")
    return call_ollama(prompt, cross_prompt)


def generate_time_analysis(cards_by_cat: dict[str, list[dict]]) -> str:
    """生成时间维度分析"""
    # 按日期排序所有卡片
    all_cards = []
    for cat, cards in cards_by_cat.items():
        for card in cards:
            all_cards.append(card)

    # 按日期排序
    all_cards.sort(key=lambda c: c.get("source_date", ""))

    if not all_cards:
        return ""

    dates = [c.get("source_date", "") for c in all_cards if c.get("source_date")]
    if not dates:
        return ""

    date_range = f"{min(dates)} 至 {max(dates)}"

    cards_text = []
    for card in all_cards:
        cards_text.append(
            f"[{card.get('category', '?')}] [{card.get('source_date', '未知')}] "
            f"{card['title']}\n  {card.get('description', '')}\n"
        )

    time_prompt = f"""你是一位认知演化分析师。请根据以下按时间排序的记忆卡片，分析作者在时间轴上的认知演化。

数据时间跨度：{date_range}
卡片总数：{len(all_cards)}

分析维度：
1. 时间分布：卡片在不同时间段的分布特征（密集期、空白期）
2. 主题演化：不同时期关注焦点的变化轨迹
3. 认知深化：哪些概念从早期的模糊探索逐渐变得清晰？
4. 行为模式变化：工作方法、工具使用、思考方式是否有明显转变？
5. 关键转折点：哪些日期标志着认知或行为的重大转变？

重要约束：
- 必须直接引用卡片 description 字段的原文作为证据，格式：> "原文"（卡片标题, 日期）
- 标注每条推断的置信度：[高] 有多处卡片支撑 / [中] 有1-2处支撑 / [低] 仅为合理推测
- 不要过度解读，如果时间跨度太短或数据不足以支撑演化分析，请明确说明

输出 Markdown 格式的分析报告，300-500 字。"""

    prompt = "请根据以下按时间排序的记忆卡片，分析认知演化轨迹：\n\n" + "\n".join(
        cards_text
    )

    print("  生成时间维度分析...")
    return call_ollama(prompt, time_prompt)


def generate_counter_evidence(cards_by_cat: dict[str, list[dict]]) -> str:
    """生成否定证据分析"""
    # 收集所有卡片的完整内容
    all_cards_text = []
    for cat, cards in cards_by_cat.items():
        for card in cards:
            all_cards_text.append(
                f"[{cat}] [{card.get('tense', '?')}] {card['title']}\n"
                f"  日期: {card.get('source_date', '未知')}\n"
                f"  {card.get('description', '')}\n"
            )

    if not all_cards_text:
        return ""

    counter_prompt = """你是一位批判性分析师。你的任务是主动寻找与主流画像相矛盾的证据，而不是验证已有结论。

以下是常见的画像结论，请逐一挑战：
- "系统论武装的浪漫主义者" → 有没有卡片显示作者缺乏系统性思维？有没有卡片显示作者并不浪漫、过于理性或功利？
- "跨领域知识融合" → 有没有卡片显示作者的知识其实很单一或碎片化？
- "元认知偏好强" → 有没有卡片显示作者缺乏自我反思、只是机械执行？
- "工具迭代频率高" → 有没有卡片显示作者长期固守某个工具、抗拒改变？
- "善于分层处理问题" → 有没有卡片显示作者处理问题时混乱无序？

分析维度：
1. 反例寻找：逐条挑战上述结论，寻找不支持或相反的证据
2. 不一致性：作者在不同卡片中的表述是否有自相矛盾之处？（如早期说A，后期说非A）
3. 证据不足：哪些流行判断实际上只有很少的卡片支撑？列出具体数量
4. 替代解释：对于同一个行为，是否有不同于主流画像的解释？（例如"工具迭代频繁"也可能是"缺乏定力"）
5. 自我描述 vs 实际行为：作者的自我描述（如"系统论武装的浪漫主义者"）是否与实际行为一致？有没有行为证据不支持这个自我标签？

重要约束：
- 必须引用卡片原文作为证据，格式：> "原文引用"（卡片标题, 日期）
- 不要说"没有矛盾"——即使找不到完全相反的证据，也要找出边缘情况、例外或弱支撑点
- 如果某条结论的支撑卡片少于3张，必须标注为"证据不足"
- 标注每条推断的置信度：[高] 有多处卡片支撑 / [中] 有1-2处支撑 / [低] 仅为合理推测

输出 Markdown 格式的分析报告，300-500 字。"""

    prompt = "请寻找以下卡片数据中与主流画像相矛盾的证据：\n\n" + "\n".join(
        all_cards_text
    )

    print("  生成否定证据分析...")
    return call_ollama(prompt, counter_prompt)


def generate_summary(cards_by_cat: dict[str, list[dict]]) -> str:
    """生成综合总结"""
    all_cards = []
    for cards in cards_by_cat.values():
        all_cards.extend(cards)

    if not all_cards:
        return ""

    summary_prompt = f"""你是一位综合分析师。请根据以下四种记忆类型的分析结果，给出对作者的整体画像。

分析维度：
1. 核心特质：用 3-5 个关键词概括作者的核心特征
2. 认知模式：作者的思维方式和认知习惯
3. 成长方向：作者正在向什么方向进化？
4. 潜在风险：可能存在什么盲点或风险？
5. 一句话画像：用一句话概括这个人

重要约束：
- 每条推断必须标注置信度：[高] 有多处卡片支撑 / [中] 有1-2处支撑 / [低] 仅为合理推测
- 每条推断必须直接引用卡片 description 字段的原文，格式：> "原文"（卡片标题, 日期）
- 不要从"卡片缺少某类内容"推断"作者忽视某方面"
- 区分"主动探索边界"与"理解有误/走偏"：卡片中提到的探索行为应视为积极尝试，除非有明确证据表明方向错误
- 情感类判断（如"情感深沉"）需要明确标注数据是否稀薄，若日志定位是工作思考则承认推测性质
- 风险项必须说明推断逻辑，不能仅给出结论
- 注意锚定效应：如果某个标签（如"系统论武装的浪漫主义者"）只出现在一张卡片的自我描述中，而不是通过行为证据独立推导出的，请在报告中明确标注这是"自我描述"而非"独立推断"
- 区分"系统推断的新发现"和"用户反馈后植入的内容"：只报告从卡片数据中独立推导出的结论，不要为了迎合预期而调整判断

输出 Markdown 格式，300-500 字。"""

    # 传入完整卡片内容而非仅标题
    all_cards_text = []
    for cat, cards in cards_by_cat.items():
        for card in cards:
            all_cards_text.append(
                f"[{cat}] [{card.get('tense', '?')}] {card['title']}\n"
                f"  日期: {card.get('source_date', '未知')}\n"
                f"  {card.get('description', '')}\n"
            )

    prompt = f"请根据以下记忆卡片数据，给出对作者的整体画像：\n\n" + "\n".join(
        all_cards_text
    )

    print("  生成综合画像...")
    return call_ollama(prompt, summary_prompt)


def main():
    output = DEFAULT_OUTPUT
    for arg in sys.argv[1:]:
        if arg.startswith("--output="):
            output = Path(arg.split("=", 1)[1])
        elif arg.startswith("--output"):
            idx = sys.argv.index(arg)
            if idx + 1 < len(sys.argv):
                output = Path(sys.argv[idx + 1])

    if not CARDS_DIR.exists():
        print(f"错误: 找不到 {CARDS_DIR}")
        print("请先运行 parse_think_cards.py")
        sys.exit(1)

    cards_by_cat = load_cards()
    total = sum(len(v) for v in cards_by_cat.values())
    print(f"加载 {total} 张卡片")

    output.parent.mkdir(parents=True, exist_ok=True)

    profile = generate_profile(cards_by_cat)
    cross_analysis = generate_cross_analysis(cards_by_cat)
    time_analysis = generate_time_analysis(cards_by_cat)
    counter_evidence = generate_counter_evidence(cards_by_cat)
    summary = generate_summary(cards_by_cat)

    report = f"""# 作者画像报告

> 基于 {total} 张记忆卡片，来源于 {len(list(CARDS_DIR.glob("*/*.json")))} 个 think 日志文件
> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 卡片统计

| 记忆类型 | 数量 |
|---------|------|
"""
    for cat, cards in cards_by_cat.items():
        report += f"| {cat} | {len(cards)} |\n"

    report += f"""
---

{profile}

---

## 跨类别综合分析

{cross_analysis}

---

## 时间维度分析

{time_analysis}

---

## 否定证据分析

{counter_evidence}

---

## 综合画像

{summary}
"""

    output.write_text(report, encoding="utf-8")
    print(f"\n报告已输出: {output}")


if __name__ == "__main__":
    main()
