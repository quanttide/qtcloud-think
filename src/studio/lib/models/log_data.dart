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
  final List<String> tags;
  final List<String> insights;
  final String entry;
  final String exit;
  final String action;

  const Annotation({
    required this.id,
    required this.title,
    required this.quote,
    required this.tags,
    required this.insights,
    required this.entry,
    required this.exit,
    required this.action,
  });
}

const List<LogParagraph> logParagraphs = [
  LogParagraph(
    id: 'para-1',
    content: '尝试换一种角度去更积极地去面对产生的新想法。就不是要求自己要完成的这种执行思维，但是我又发现了新的入口的构建思维。',
    hotspots: [
      Hotspot(id: 'hs-1', text: '执行思维', annotationId: 'anno-1'),
      Hotspot(id: 'hs-1b', text: '构建思维', annotationId: 'anno-1'),
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
      Hotspot(id: 'hs-2', text: '这是一个问题变成我又发现了一个问题', annotationId: 'anno-2'),
      Hotspot(id: 'hs-2b', text: '发现问题本身就是一个很积极的信号', annotationId: 'anno-2'),
    ],
  ),
  LogParagraph(
    id: 'para-4',
    content: '我又发现我的紧张和压力，就是说这种积极思考法最大的信号就是我感觉到紧张压力的时候，那我就尝试重新去叙事转换思维。这种叙事重构的方式已经开始渗透到了我的原思考过程之中。',
    hotspots: [
      Hotspot(id: 'hs-2c', text: '叙事重构的方式已经开始渗透到了我的原思考过程之中', annotationId: 'anno-2'),
    ],
  ),
  LogParagraph(
    id: 'para-5',
    content: '把手上的一些维护工作交给了我助理，然后我感觉我的视野一下子拔高上来，我就敢去处理业务问题。作为 leader 专注于业务整体控制的思路已经建立起来了，我专注于澄新意图。',
    hotspots: [
      Hotspot(id: 'hs-3', text: '拔高上来', annotationId: 'anno-3'),
      Hotspot(id: 'hs-3b', text: '澄新意图', annotationId: 'anno-3'),
    ],
  ),
  LogParagraph(
    id: 'para-6',
    content: '简介相对来讲可以更流动得多……案例就可以更固定一点。只要我知道该怎么提炼，我其实就不用过多地去记这个元认知具体是什么。',
    hotspots: [
      Hotspot(id: 'hs-4', text: '流动', annotationId: 'anno-4'),
      Hotspot(id: 'hs-4b', text: '固定', annotationId: 'anno-4'),
      Hotspot(id: 'hs-4c', text: '提炼', annotationId: 'anno-4'),
    ],
  ),
  LogParagraph(
    id: 'para-7',
    content: '我放弃了一个假设，就是说我并不是一定要去兼容市场现有的标准。我们的体系已经高出市场……最重要的事情是能够给我们掏钱的客户用。',
    hotspots: [
      Hotspot(id: 'hs-5', text: '并不是一定要去兼容市场现有的标��', annotationId: 'anno-5'),
      Hotspot(id: 'hs-5b', text: '掏钱的客户', annotationId: 'anno-5'),
    ],
  ),
  LogParagraph(
    id: 'para-8',
    content: '我又发现了一个点，就是从知识工程角度来看的话，其实我们对资产做的这一系列活动，很大程度上就是知识工程的流程。范畴论就很有 summarize 的这种感觉在。',
    hotspots: [
      Hotspot(id: 'hs-6', text: '范畴论', annotationId: 'anno-6'),
    ],
  ),
];

const List<Annotation> annotations = [
  Annotation(
    id: 'anno-1',
    entry: '入口转换',
    exit: '元认知框架',
    title: '自我指涉',
    quote: '不是要求自己要完成的执行思维，而是发现了新入口的构建思维',
    tags: ['自我指涉'],
    insights: [
      '从被动响应到主动创造框架',
      '在元层面重新定义思维活动的意义',
      '开启了整个认知螺旋的起点',
    ],
    action: '下次当你感到被任务追着跑时，停一秒问自己："这个任务是在执行旧脚本，还是在构建新入口？" 把"我要完成"改成"我正在发现一个可复用的新入口"。',
  ),
  Annotation(
    id: 'anno-2',
    entry: '情感反射',
    exit: '认知安全网',
    title: '叙事重构',
    quote: "把'这是一个问题'变成'我又发现了一个问题'",
    tags: ['叙事重构'],
    insights: [
      '障碍 → 养料的叙事重构',
      '建立心理上的安全网',
      '困难成为信息生产的持续来源',
      '压力被左移为预警信号，而非终点',
    ],
    action: '遇到阻塞时立刻对自己说："我又发现了一个问题"（注意用"发现"而不是"遇到"），然后花1分钟把这个问题写进日志。它从压在你身上的石头，变成了你产出给团队的养料。',
  ),
  Annotation(
    id: 'anno-3',
    entry: '角色跃迁',
    exit: '领导力重构',
    title: '角色叙事',
    quote: '视野一下子拔高上来……我专注于澄新意图',
    tags: ['角色叙事'],
    insights: [
      '从系统的核心引擎变为意义源头',
      '清晰意图比亲自执行更重要',
      '认知上的升维而非简单分工',
    ],
    action: '当你想插手具体执行时，把手从键盘上拿开。只写下一个方向性意图（例如"把这个建模思路跑通"），交给助理，让她自己去组装路径。你只负责澄明意图，不负责铺设轨道。',
  ),
  Annotation(
    id: 'anno-4',
    entry: '知识边界',
    exit: '蒸馏逻辑',
    title: '认知架构',
    quote: '简介流动……案例固定……知道怎么提炼就不用记元认知',
    tags: ['认知架构'],
    insights: [
      '流动思考与固定资产的动态平衡',
      '核心是提炼方法而非囤积信息',
      '定义"蒸馏"而非"存储"的知识哲学',
    ],
    action: '写完一篇日志后，做一次单句蒸馏：如果这篇只能留一段给团队，留哪段？把它放进案例或简介，剩下的让它流动。你的目标是"提炼一次，团队反复使用"。',
  ),
  Annotation(
    id: 'anno-5',
    entry: '范式突破',
    exit: '重新锚定价值',
    title: '认知转换',
    quote: '并不是一定要去兼容市场现有的标准……最重要是给掏钱的客户用',
    tags: ['认知转换'],
    insights: [
      '从适配者到定义者的框架转换',
      '价值从市场流行度转到客户真实效用',
      '为体系自主性打开空间',
    ],
    action: '下次评估一个外部标准或竞品时，先问"它对我们的客户有用吗？"而不是"它在市场上流行吗？"。把判断价值的锚点从外部认可拉回到客户实际受益上。',
  ),
  Annotation(
    id: 'anno-6',
    entry: '闭环',
    exit: '元认知递归',
    title: '闭环',
    quote: '范畴论……按照上级的范畴去做事，是对结构的总结',
    tags: ['闭环', '自我指涉'],
    insights: [
      '用叙事重构观察叙事重构本身',
      '元认知的递归升级',
      '构成无限升级的螺旋',
    ],
    action: '当你意识到自己正在使用某种思维模式（比如叙事重构）时，把这个"意识到"本身也写下来。这等于在思维上又加了一层透镜，持续递归升级你的元认知。',
  ),
];