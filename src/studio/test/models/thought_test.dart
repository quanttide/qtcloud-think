import 'package:flutter_test/flutter_test.dart';
import 'package:qtcloud_think_studio/models/thought.dart';

Thought _thought({ThoughtStatus status = ThoughtStatus.raw}) => Thought(
      id: 't1',
      content: '验证比规划重要',
      status: status,
      createdAt: DateTime(2026, 8, 22),
    );

void main() {
  group('Thought JSON 往返', () {
    test('全字段往返无损', () {
      final t = Thought(
        id: 't1',
        content: '想法内容',
        source: ThoughtSource.journal,
        status: ThoughtStatus.structured,
        clarity: 'clear',
        facts: ['事实1'],
        feelings: ['感受1'],
        actions: ['行动1'],
        clarifyLog: [
          (speaker: 'ai', text: '追问？'),
          (speaker: 'user', text: '回答'),
        ],
        createdAt: DateTime(2026, 8, 22, 10, 30),
      );
      final restored = Thought.fromJson(t.toJson());
      expect(restored.id, t.id);
      expect(restored.content, t.content);
      expect(restored.source, ThoughtSource.journal);
      expect(restored.status, ThoughtStatus.structured);
      expect(restored.clarity, 'clear');
      expect(restored.facts, ['事实1']);
      expect(restored.feelings, ['感受1']);
      expect(restored.actions, ['行动1']);
      expect(restored.clarifyLog.length, 2);
      expect(restored.clarifyLog[0].speaker, 'ai');
      expect(restored.createdAt, t.createdAt);
    });

    test('默认值（clarity=null、清单为空）', () {
      final t = _thought();
      final restored = Thought.fromJson(t.toJson());
      expect(restored.clarity, isNull);
      expect(restored.facts, isEmpty);
      expect(restored.clarifyLog, isEmpty);
    });
  });

  group('状态流转', () {
    test('合法流转 raw → clarifying → structured', () {
      final t = _thought();
      t.advanceTo(ThoughtStatus.clarifying);
      expect(t.status, ThoughtStatus.clarifying);
      t.advanceTo(ThoughtStatus.structured);
      expect(t.status, ThoughtStatus.structured);
    });

    test('raw 直接到 structured 合法', () {
      final t = _thought();
      t.advanceTo(ThoughtStatus.structured);
      expect(t.status, ThoughtStatus.structured);
    });

    test('非法回退抛错', () {
      final t = _thought(status: ThoughtStatus.structured);
      expect(
        () => t.advanceTo(ThoughtStatus.raw),
        throwsStateError,
      );
    });
  });
}
