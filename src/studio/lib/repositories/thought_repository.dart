/// 想法仓储（DDD Repository）——领域层依赖接口，不依赖存储实现。
library;

import 'dart:convert';
import 'dart:io';

import '../models/thought.dart';

/// 想法仓储抽象（测试可注入内存实现）
abstract class ThoughtRepository {
  Future<List<Thought>> load();
  Future<void> add(Thought thought);
  Future<void> update(Thought thought);
  Future<void> remove(String id);
  Future<List<Thought>> byStatus(ThoughtStatus status);
  Future<void> save();
}

/// 本地文件实现（仓储：~/.qtcloud-think/thoughts.json，QTCLOUD_THINK_DATA 可覆盖）
class LocalFileThoughtRepository implements ThoughtRepository {
  final File _file;
  List<Thought> _cache = [];
  bool _loaded = false;

  LocalFileThoughtRepository({String? dataDir})
      : _file = File(
          '${dataDir ?? _defaultDataDir()}/thoughts.json',
        );

  static String _defaultDataDir() =>
      Platform.environment['QTCLOUD_THINK_DATA'] ??
      '${Platform.environment['HOME'] ?? '.'}/.qtcloud-think';

  Future<void> _ensureLoaded() async {
    if (_loaded) return;
    if (_file.existsSync()) {
      try {
        final list = jsonDecode(_file.readAsStringSync()) as List;
        _cache = [
          for (final e in list) Thought.fromJson(e as Map<String, dynamic>)
        ];
      } catch (_) {
        _cache = []; // 损坏文件 → 空列表，下次写入重建
      }
    }
    _loaded = true;
  }

  @override
  Future<List<Thought>> load() async {
    await _ensureLoaded();
    return List.of(_cache);
  }

  @override
  Future<void> add(Thought thought) async {
    await _ensureLoaded();
    _cache.add(thought);
    await save();
  }

  @override
  Future<void> update(Thought thought) async {
    await _ensureLoaded();
    final i = _cache.indexWhere((t) => t.id == thought.id);
    if (i >= 0) _cache[i] = thought;
    await save();
  }

  @override
  Future<void> remove(String id) async {
    await _ensureLoaded();
    _cache.removeWhere((t) => t.id == id);
    await save();
  }

  @override
  Future<List<Thought>> byStatus(ThoughtStatus status) async {
    await _ensureLoaded();
    return _cache.where((t) => t.status == status).toList();
  }

  @override
  Future<void> save() async {
    await _ensureLoaded();
    await _file.parent.create(recursive: true);
    // 原子写：临时文件 + rename
    final tmp = File('${_file.path}.tmp');
    await tmp.writeAsString(
      jsonEncode([for (final t in _cache) t.toJson()]),
    );
    await tmp.rename(_file.path);
  }
}
