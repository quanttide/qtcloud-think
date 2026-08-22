import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:qtcloud_think_studio/models/thought.dart';
import 'package:qtcloud_think_studio/repositories/clarify_repository.dart';

Thought _thought() => Thought(
      id: 't1',
      content: '模糊的想法',
      createdAt: DateTime(2026, 8, 22),
    );

void main() {
  group('judgeClarity', () {
    test('200 → ClarityResult 解析', () async {
      final client = MockClient((req) async {
        expect(req.url.path, '/api/clarity');
        expect(req.body, contains('模糊的想法'));
        return http.Response(
          jsonEncode({'clarity': 'unclear', 'reason': '缺少具体对象'}),
          200,
          headers: {'content-type': 'application/json'},
        );
      });
      final repo = ClarifyRepository(client: client);
      final r = await repo.judgeClarity(_thought());
      expect(r.clarity, 'unclear');
      expect(r.reason, '缺少具体对象');
    });

    test('500 → 抛明确错误（不造假结果）', () async {
      final client = MockClient((_) async => http.Response('err', 500));
      final repo = ClarifyRepository(client: client);
      expect(
        () => repo.judgeClarity(_thought()),
        throwsA(isA<Exception>().having(
            (e) => e.toString(), 'message', contains('HTTP 500'))),
      );
    });
  });

  group('clarify', () {
    test('上下文传递 + done 解析', () async {
      final client = MockClient((req) async {
        final body = jsonDecode(req.body) as Map<String, dynamic>;
        expect(body['log'], isNotEmpty); // 历史上下文传递
        expect(body['reply'], '回答');
        return http.Response(
          jsonEncode({'text': '追问', 'done': false}),
          200,
          headers: {'content-type': 'application/json'},
        );
      });
      final repo = ClarifyRepository(client: client);
      final t = _thought()
        ..clarifyLog.add((speaker: 'ai', text: '之前的追问'));
      final r = await repo.clarify(t, '回答');
      expect(r.text, '追问');
      expect(r.done, false);
    });
  });

  group('structure', () {
    test('三清单解析', () async {
      final client = MockClient((_) async => http.Response(
            jsonEncode({
              'facts': ['事实'],
              'feelings': ['感受'],
              'actions': ['行动'],
            }),
            200,
            headers: {'content-type': 'application/json'},
          ));
      final repo = ClarifyRepository(client: client);
      final r = await repo.structure(_thought());
      expect(r.facts, ['事实']);
      expect(r.feelings, ['感受']);
      expect(r.actions, ['行动']);
    });

    test('缺字段 → 空清单不崩溃', () async {
      final client = MockClient((_) async => http.Response(
            jsonEncode({'facts': ['事实']}),
            200,
            headers: {'content-type': 'application/json'},
          ));
      final repo = ClarifyRepository(client: client);
      final r = await repo.structure(_thought());
      expect(r.feelings, isEmpty);
      expect(r.actions, isEmpty);
    });
  });
}
