class PrismData {
  final String entry;
  final String exit;
  final String quote;
  final List<String> tags;
  final String insight;

  const PrismData({
    required this.entry,
    required this.exit,
    required this.quote,
    required this.tags,
    required this.insight,
  });
}

const List<PrismData> prismCards = [
  PrismData(
    entry: '入口转换',
    exit: '元认知框架',
    quote: '尝试换一种角度去更积极地去面对产生的新想法。就不是要求自己要完成的这种执行思维，但是我又发现了新的入口的构建思维。',
    tags: ['自我指涉'],
    insight: '开启了整个认知螺旋的起点。将"完成任务"的压力叙事，重构为"构建新入口"的探索叙事。',
  ),
  PrismData(
    entry: '情感反射',
    exit: '认知安全网',
    quote: '紧张和压力……尝试重新去叙事转换思维。把"这是一个问题"变成"我又发现了一个问题"……我每天都面临大量的困难，它大部分都解决不了，所以发现问题本身就是一个很积极的信号。',
    tags: ['叙事重构'],
    insight: '最频繁也最核心的模式。将"障碍"重构为"养料"，建立了心理上的安全网。',
  ),
  PrismData(
    entry: '角色跃迁',
    exit: '领导力重构',
    quote: '把手上的一些维护工作交给了我助理，然后我感觉我的视野一下子拔高上来，我就敢去处理业务问题……作为 leader 专注于业务整体控制的这个思路已经建立起来了……我专注于澄新意图。',
    tags: ['角色叙事'],
    insight: '通过移交具体维护任务，重新讲述了自己的工作意义：从"系统的核心引擎"变为"系统的意义源头"。',
  ),
  PrismData(
    entry: '知识边界',
    exit: '蒸馏逻辑',
    quote: '简介相对来讲可以更流动得多……案例就可以更固定一点……只要我知道该怎么提炼，我其实就不用过多地去记这个元认知具体是什么。',
    tags: ['认知架构'],
    insight: '在流动的思考与固定的团队资产之间找到了动态平衡。核心不是囤积信息，而是提炼方法。',
  ),
  PrismData(
    entry: '范式突破',
    exit: '重新锚定价值',
    quote: '放弃了一个假设，就是说我并不是一定要去兼容市场现有的标准……我们的体系已经高出市场……最重要的事情是能够给我们掏钱的客户用。',
    tags: ['认知转换'],
    insight: '最彻底的一次认知跳跃。从"适配者"重构为"定义者"。将标准的价值从"市场流行度"重新锚定在"客户真实效用"上。',
  ),
  PrismData(
    entry: '观察者效应',
    exit: '元认知渗透',
    quote: '这种叙事重构的方式已经开始渗透到了我的原思考过程之中……我又发现了我自己一个认知上的升级和迁移。',
    tags: ['闭环'],
    insight: '最精妙的自我指涉：你正在用叙事重构的方法，观察并确认叙事重构正在生效。构成了无限升级的螺旋。',
  ),
];