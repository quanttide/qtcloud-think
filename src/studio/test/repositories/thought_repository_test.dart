import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:qtcloud_think_studio/models/thought.dart';
import 'package:qtcloud_think_studio/repositories/thought_repository.dart';

void main() {
  late Directory tempDir;
  late LocalFileThoughtRepository repo;

  setUp(() {
    tempDir = Directory.systemTemp.createTempSync('thought_repo_test');
    repo = LocalFileThoughtRepository(dataDir: tempDir.path);
  });

  tearDown(() {
    tempDir.deleteSync(recursive: true);
  });

  Thought makeThought(String id, {ThoughtStatus status = ThoughtStatus.raw}) =>
      Thought(
        id: id,
        content: '想法 $id',
        status: status,
        createdAt: DateTime(2026, 8, 22),
      );

  group('写入读回', () {
    test('add → load 一致', () async {
      await repo.add(makeThought('t1'));
      await repo.add(makeThought('t2'));
      final all = await repo.load();
      expect(all.length, 2);
      expect(all.map((t) => t.id), ['t1', 't2']);
    });

    test('update 持久化后读回一致', () async {
      await repo.add(makeThought('t1'));
      final t = (await repo.load()).first;
      t.advanceTo(ThoughtStatus.structured);
      t.facts.add('事实');
      await repo.update(t);

      // 新实例（模拟重启）读回
      final repo2 = LocalFileThoughtRepository(dataDir: tempDir.path);
      final restored = (await repo2.load()).first;
      expect(restored.status, ThoughtStatus.structured);
      expect(restored.facts, ['事实']);
    });
  });

  group('过滤与删除', () {
    test('byStatus 分组正确', () async {
      await repo.add(makeThought('t1', status: ThoughtStatus.raw));
      await repo.add(makeThought('t2', status: ThoughtStatus.structured));
      await repo.add(makeThought('t3', status: ThoughtStatus.structured));
      final structured = await repo.byStatus(ThoughtStatus.structured);
      expect(structured.map((t) => t.id), ['t2', 't3']);
    });

    test('remove 后消失', () async {
      await repo.add(makeThought('t1'));
      await repo.remove('t1');
      expect(await repo.load(), isEmpty);
    });
  });

  group('容错', () {
    test('无文件 → 空列表', () async {
      expect(await repo.load(), isEmpty);
    });

    test('损坏文件 → 空列表不崩溃', () async {
      final f = File('${tempDir.path}/thoughts.json');
      await f.writeAsString('{损坏的 json');
      expect(await repo.load(), isEmpty);
    });
  });
}
