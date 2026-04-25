class LogParagraph {
  final String id;
  final String content;
  final List<Hotspot> hotspots;

  const LogParagraph({
    required this.id,
    required this.content,
    required this.hotspots,
  });
}

class Hotspot {
  final String id;
  final String text;
  final String annotationId;

  const Hotspot({
    required this.id,
    required this.text,
    required this.annotationId,
  });
}

class Annotation {
  final String id;
  final String title;
  final String quote;
  final String action;

  const Annotation({
    required this.id,
    required this.title,
    required this.quote,
    required this.action,
  });
}

const List<LogParagraph> logParagraphs = [
  LogParagraph(
    id: 'para-1',
    content: '尝试换一种角度去更积极地去面对产生的新想法。就不是要求自己要完成的这种执行思维，但是我又发现了新的入口的构建思维。',
    hotspots: [
      Hotspot(id: 'hs-1', text: '执行思维', annotationId: 'a1'),
      Hotspot(id: 'hs-1b', text: '构建思维', annotationId: 'a1'),
    ],
  ),
  LogParagraph(
    id: 'para-2',
    content: '原始的日志整理加工后，具备去看真实的思考过程和情感过程。这些是非常丰富的元素材。同时，这也是AI原生时代的一个原方法。',
    hotspots: [],
  ),
  LogParagraph(
    id: 'para-3',
    content: '我尝试重新去叙事转换思维。把"这是一个问题"变成"我又发现了一个问题"。我每天都面临大量的困难，它大部分都解决不了，所以发现问题本身就是一个很积极的信号。',
    hotspots: [
      Hotspot(id: 'hs-2', text: '这是一个问题变成我又发现了一个问题', annotationId: 'a2'),
      Hotspot(id: 'hs-2b', text: '发现问题本身就是一个很积极的信号', annotationId: 'a2'),
    ],
  ),
  LogParagraph(
    id: 'para-4',
    content: '我又发现我的紧张和压力，就是说这种积极思考法最大的信号就是我感觉到紧张压力的时候，那我就尝试重新去叙事转换思维。这种叙事重构的方式已经开始渗透到了我的原思考过程之中。',
    hotspots: [
      Hotspot(id: 'hs-2c', text: '叙事重构的方式已经开始渗透到了我的原思考过程之中', annotationId: 'a2'),
    ],
  ),
  LogParagraph(
    id: 'para-5',
    content: '把手上的一些维护工作交给了我助理，然后我感觉我的视野一下子拔高上来，我就敢去处理业务问题。作为 leader 专注于业务整体控制的思路已经建立起来了，我专注于澄新意图。',
    hotspots: [
      Hotspot(id: 'hs-3', text: '拔高上来', annotationId: 'a3'),
      Hotspot(id: 'hs-3b', text: '澄新意图', annotationId: 'a3'),
    ],
  ),
  LogParagraph(
    id: 'para-6',
    content: '简介相对来讲可以更流动得多……案例就可以更固定一点。只要我知道该怎么提炼，我其实就不用过多地去记这个元认知具体是什么。',
    hotspots: [
      Hotspot(id: 'hs-4', text: '流动', annotationId: 'a4'),
      Hotspot(id: 'hs-4b', text: '固定', annotationId: 'a4'),
      Hotspot(id: 'hs-4c', text: '提炼', annotationId: 'a4'),
    ],
  ),
  LogParagraph(
    id: 'para-7',
    content: '我放弃了一个假设，就是说我并不是一定要去兼容市场现有的标准。我们的体系已经高出市场……最重要的事情是能够给我们掏钱的客户用。',
    hotspots: [
      Hotspot(id: 'hs-5', text: '并不是一定要去兼容市场现有的标准', annotationId: 'a5'),
      Hotspot(id: 'hs-5b', text: '掏钱的客户', annotationId: 'a5'),
    ],
  ),
  LogParagraph(
    id: 'para-8',
    content: '我从知识工程角度来看的话，其实我��对资产做的这一系列活动，很大程度上就是知识工程的流程。范畴论就很有 summarize 的这种感觉在。',
    hotspots: [
      Hotspot(id: 'hs-6', text: '范畴论', annotationId: 'a6'),
    ],
  ),
];

const List<Annotation> annotations = [
  Annotation(
    id: 'a1',
    title: '执行思维 → 构建思维',
    quote: '不是要求自己要完成，而是发现了新入口',
    action: '下次感到被任务追赶时，问自己：这是在执行旧脚本，还是在构建新入口？',
  ),
  Annotation(
    id: 'a2',
    title: '问题 → 发现',
    quote: "把'这是一个问题'变成'我又发现了一个问题'",
    action: '遇到阻塞时对自己说"我又发现了一个问题"，然后用1分钟把它写进日志。',
  ),
  Annotation(
    id: 'a3',
    title: '执行 → 澄明意图',
    quote: '视野一下子拔高上来……我专注于澄新意图',
    action: '想插手执行时，把手从键盘上拿开。只写一个方向性意图，交给团队去组装。',
  ),
  Annotation(
    id: 'a4',
    title: '囤积 → 蒸馏',
    quote: '知道怎么提炼，就不用去记元认知具体是什么',
    action: '写完日志后做单句蒸馏：只能留一段给团队，留哪段？放进案例，剩下的流动。',
  ),
  Annotation(
    id: 'a5',
    title: '标准 → 客户价值',
    quote: '并不是一定要去兼容市场现有的标准……最重要是给掏钱的客户用',
    action: '评估外部标准时，先问"它对我们的客户有用吗？"而不是"它流行吗？"。',
  ),
  Annotation(
    id: 'a6',
    title: '观察者闭环',
    quote: '范畴论……按照上级的范畴去做事，是对结构的总结',
    action: '意识到自己正在用某种思维模式时，把这个"意识到"也写下来，持续递归升级元认知。',
  ),
];