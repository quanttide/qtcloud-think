/// AI 加工访问仓储（调 provider——清晰度判断/澄清/结构化）。
///
/// 数据访问层：HTTP 调用 provider 的 AI 加工接口。
/// 失败降级：AI 失败 → 抛明确错误（调用方提示用户，不造假结果）。
library;

import 'dart:convert';

import 'package:http/http.dart' as http;

/// 清晰度判断结果
class ClarityResult {
  final String clarity; // clear / unclear
  final String? reason;
  const ClarityResult({required this.clarity, this.reason});
}

/// 澄清回复
class ClarifyReply {
  final String text;
  final bool done; // done=true 澄清完成可结构化
  const ClarifyReply({required this.text, required this.done});
}

/// 结构化结果
class StructureResult {
  final List<String> facts;
  final List<String> feelings;
  final List<String> actions;
  const StructureResult({
    required this.facts,
    required this.feelings,
    required this.actions,
  });
}

/// AI 加工访问（调 provider）
class ClarifyRepository {
  final http.Client _client;
  final String _baseUrl;

  ClarifyRepository({http.Client? client, String? baseUrl})
      : _client = client ?? http.Client(),
        _baseUrl = baseUrl ??
            PlatformEnv.baseUrl;

  Future<ClarityResult> judgeClarity(ThoughtLike thought) async {
    final res = await _client
        .post(
          Uri.parse('$_baseUrl/api/clarity'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'content': thought.content}),
        )
        .timeout(const Duration(seconds: 30));
    if (res.statusCode != 200) {
      throw Exception('清晰度判断失败（HTTP ${res.statusCode}）');
    }
    final j = jsonDecode(res.body) as Map<String, dynamic>;
    return ClarityResult(
      clarity: j['clarity'] as String,
      reason: j['reason'] as String?,
    );
  }

  Future<ClarifyReply> clarify(ThoughtLike thought, String userReply) async {
    final res = await _client
        .post(
          Uri.parse('$_baseUrl/api/clarify'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'content': thought.content,
            'log': [
              for (final e in thought.clarifyLog)
                {'speaker': e.speaker, 'text': e.text}
            ],
            'reply': userReply,
          }),
        )
        .timeout(const Duration(seconds: 30));
    if (res.statusCode != 200) {
      throw Exception('澄清失败（HTTP ${res.statusCode}）');
    }
    final j = jsonDecode(res.body) as Map<String, dynamic>;
    return ClarifyReply(
      text: j['text'] as String,
      done: j['done'] as bool? ?? false,
    );
  }

  Future<StructureResult> structure(ThoughtLike thought) async {
    final res = await _client
        .post(
          Uri.parse('$_baseUrl/api/structure'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'content': thought.content,
            'log': [
              for (final e in thought.clarifyLog)
                {'speaker': e.speaker, 'text': e.text}
            ],
          }),
        )
        .timeout(const Duration(seconds: 30));
    if (res.statusCode != 200) {
      throw Exception('结构化失败（HTTP ${res.statusCode}）');
    }
    final j = jsonDecode(res.body) as Map<String, dynamic>;
    return StructureResult(
      facts: (j['facts'] as List?)?.cast<String>() ?? [],
      feelings: (j['feelings'] as List?)?.cast<String>() ?? [],
      actions: (j['actions'] as List?)?.cast<String>() ?? [],
    );
  }
}

/// 领域对象最小接口（避免仓储依赖具体模型）
abstract class ThoughtLike {
  String get content;
  List<({String speaker, String text})> get clarifyLog;
}

/// 平台环境（隔离 dart:io Platform，便于测试）
abstract class PlatformEnv {
  static String baseUrl =
      String.fromEnvironment('QTCLOUD_THINK_PROVIDER',
          defaultValue: 'http://localhost:8080');
}
