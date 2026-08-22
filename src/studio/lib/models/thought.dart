/// 想法模型——从原始输入到情境意识实例的唯一载体。
library;

import '../repositories/clarify_repository.dart' show ThoughtLike;

/// 想法状态（只前进不后退：raw → clarifying → structured）
enum ThoughtStatus { raw, clarifying, structured }

/// 来源
enum ThoughtSource { manual, journal }

/// 想法（原始/加工中/实例三态）
class Thought implements ThoughtLike {
  final String id;
  @override
  final String content;
  final ThoughtSource source;
  ThoughtStatus status;
  String? clarity; // clear / unclear（AI 判断，可空）
  List<String> facts;
  List<String> feelings;
  List<String> actions;
  @override
  final List<({String speaker, String text})> clarifyLog; // 澄清对话记录
  final DateTime createdAt;

  Thought({
    required this.id,
    required this.content,
    this.source = ThoughtSource.manual,
    this.status = ThoughtStatus.raw,
    this.clarity,
    List<String>? facts,
    List<String>? feelings,
    List<String>? actions,
    List<({String speaker, String text})>? clarifyLog,
    required this.createdAt,
  })  : facts = facts ?? [],
        feelings = feelings ?? [],
        actions = actions ?? [],
        clarifyLog = clarifyLog ?? [];

  /// 状态流转（非法回退抛错）
  void advanceTo(ThoughtStatus next) {
    const valid = {
      ThoughtStatus.raw: {ThoughtStatus.clarifying, ThoughtStatus.structured},
      ThoughtStatus.clarifying: {ThoughtStatus.structured},
      ThoughtStatus.structured: <ThoughtStatus>{},
    };
    if (!valid[status]!.contains(next)) {
      throw StateError('非法状态流转：$status → $next');
    }
    status = next;
  }

  // ─── 序列化 ───

  Map<String, dynamic> toJson() => {
        'id': id,
        'content': content,
        'source': source.name,
        'status': status.name,
        'clarity': clarity,
        'facts': facts,
        'feelings': feelings,
        'actions': actions,
        'clarifyLog': [
          for (final e in clarifyLog) {'speaker': e.speaker, 'text': e.text}
        ],
        'createdAt': createdAt.toIso8601String(),
      };

  factory Thought.fromJson(Map<String, dynamic> json) => Thought(
        id: json['id'] as String,
        content: json['content'] as String,
        source: ThoughtSource.values.byName(json['source'] as String),
        status: ThoughtStatus.values.byName(json['status'] as String),
        clarity: json['clarity'] as String?,
        facts: (json['facts'] as List?)?.cast<String>() ?? [],
        feelings: (json['feelings'] as List?)?.cast<String>() ?? [],
        actions: (json['actions'] as List?)?.cast<String>() ?? [],
        clarifyLog: [
          for (final e in (json['clarifyLog'] as List?) ?? [])
            (speaker: e['speaker'] as String, text: e['text'] as String)
        ],
        createdAt: DateTime.parse(json['createdAt'] as String),
      );
}
