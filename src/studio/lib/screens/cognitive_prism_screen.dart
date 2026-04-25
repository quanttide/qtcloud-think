import 'package:flutter/material.dart';
import '../models/log_data.dart';

class CognitivePrismScreen extends StatefulWidget {
  const CognitivePrismScreen({super.key});

  @override
  State<CognitivePrismScreen> createState() => _CognitivePrismScreenState();
}

class _CognitivePrismScreenState extends State<CognitivePrismScreen> {
  String? _activeAnnotationId;

  void _activateAnnotation(String annotationId) {
    setState(() {
      if (_activeAnnotationId == annotationId) {
        _activeAnnotationId = null;
      } else {
        _activeAnnotationId = annotationId;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFf5f5f0),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final isWide = constraints.maxWidth > 800;
            if (isWide) {
              return _buildDualPane();
            } else {
              return _buildNarrowLayout();
            }
          },
        ),
      ),
    );
  }

  Widget _buildDualPane() {
    return Row(
      children: [
        Expanded(
          flex: 55,
          child: _buildLogPane(),
        ),
        Container(
          width: 1,
          color: const Color(0xFFe8e0d5),
        ),
        Expanded(
          flex: 45,
          child: _buildAnnotationPane(),
        ),
      ],
    );
  }

  Widget _buildNarrowLayout() {
    return CustomScrollView(
      slivers: [
        SliverToBoxAdapter(child: _buildLogPane()),
        SliverToBoxAdapter(child: _buildAnnotationPane()),
      ],
    );
  }

  Widget _buildLogPane() {
    return Container(
      color: const Color(0xFFfdfaf5),
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 20),
            const Text(
              '2026年4月23日',
              style: TextStyle(
                fontSize: 13,
                color: Color(0xFF9b8e7a),
                letterSpacing: 0.5,
              ),
            ),
            const SizedBox(height: 4),
            const Text(
              '创始人日志',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.w700,
                color: Color(0xFF1a1208),
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              '一次密集的思维重构——从焦虑到构建，从执行到澄明',
              style: TextStyle(
                fontSize: 13,
                fontStyle: FontStyle.italic,
                color: Color(0xFF6b5e4a),
              ),
            ),
            const SizedBox(height: 24),
            ...logParagraphs.map((para) => _buildLogParagraph(para)),
            const SizedBox(height: 20),
            const Center(
              child: Text(
                '—— 日志摘录完毕。点击高亮词查看对应的认知批注。',
                style: TextStyle(
                  fontSize: 12,
                  fontStyle: FontStyle.italic,
                  color: Color(0xFF9b8e7a),
                ),
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  Widget _buildLogParagraph(LogParagraph para) {
    if (para.hotspots.isEmpty) {
      return Padding(
        padding: const EdgeInsets.only(bottom: 16),
        child: Text(
          para.content,
          style: const TextStyle(
            fontSize: 15,
            color: Color(0xFF3d3226),
            height: 1.8,
          ),
        ),
      );
    }

    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: RichText(
        text: TextSpan(
          style: const TextStyle(
            fontSize: 15,
            color: Color(0xFF3d3226),
            height: 1.8,
          ),
          children: _buildParagraphSpans(para),
        ),
      ),
    );
  }

  List<InlineSpan> _buildParagraphSpans(LogParagraph para) {
    final spans = <InlineSpan>[];
    String remaining = para.content;

    for (final hotspot in para.hotspots) {
      final index = remaining.indexOf(hotspot.text);
      if (index == -1) continue;

      if (index > 0) {
        spans.add(TextSpan(text: remaining.substring(0, index)));
      }

      final isActive = _activeAnnotationId == hotspot.annotationId;
      spans.add(
        WidgetSpan(
          child: GestureDetector(
            onTap: () => _activateAnnotation(hotspot.annotationId),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
              decoration: BoxDecoration(
                color: isActive
                    ? const Color(0xFFffe9a0)
                    : const Color(0xFFfef3c7),
                borderRadius: BorderRadius.circular(4),
                border: Border(
                  bottom: BorderSide(
                    color: isActive
                        ? const Color(0xFFc97d60)
                        : const Color(0xFFd4b896),
                    width: 1.5,
                    style: BorderStyle.solid,
                  ),
                ),
              ),
              child: Text(
                hotspot.text,
                style: TextStyle(
                  fontWeight: FontWeight.w500,
                  color: const Color(0xFF5c3d2e),
                ),
              ),
            ),
          ),
        ),
      );

      remaining = remaining.substring(index + hotspot.text.length);
    }

    if (remaining.isNotEmpty) {
      spans.add(TextSpan(text: remaining));
    }

    return spans;
  }

  Widget _buildAnnotationPane() {
    return Container(
      color: const Color(0xFFfaf7f2),
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 8),
            const Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('🔍', style: TextStyle(fontSize: 14)),
                SizedBox(width: 6),
                Text(
                  '认知批注 · 思维工具箱',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    letterSpacing: 1,
                    color: Color(0xFF9b8e7a),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (_activeAnnotationId == null)
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: const Color(0xFFfffbf5),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Color(0xFFe8d5c0)),
                ),
                child: const Center(
                  child: Text(
                    '点击左侧高亮文字，\n这里将展开对应的深度解读。',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 13,
                      color: Color(0xFFbfb5a3),
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                ),
              ),
            ...annotations.map((anno) => _buildAnnotationCard(anno)),
          ],
        ),
      ),
    );
  }

  Widget _buildAnnotationCard(Annotation anno) {
    final isActive = _activeAnnotationId == anno.id;

    return GestureDetector(
      onTap: () => _activateAnnotation(anno.id),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOutCubic,
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: isActive ? const Color(0xFFfffef9) : const Color(0xFFfffbf5),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isActive ? const Color(0xFFc97d60) : const Color(0xFFe8d5c0),
            width: isActive ? 1.5 : 1,
          ),
          boxShadow: [
            BoxShadow(
              color: isActive
                  ? const Color(0xFFc97d60).withValues(alpha: 0.15)
                  : const Color(0xFF000000).withValues(alpha: 0.04),
              blurRadius: isActive ? 12 : 6,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Opacity(
          opacity: isActive ? 1.0 : 0.7,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: anno.tags
                    .map((tag) => Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 2,
                          ),
                          decoration: BoxDecoration(
                            color: const Color(0xFFfef0ea),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Text(
                            tag,
                            style: const TextStyle(
                              fontSize: 10,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFFb15330),
                            ),
                          ),
                        ))
                    .toList(),
              ),
              const SizedBox(height: 8),
              Text(
                '${anno.entry} → ${anno.exit}',
                style: const TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF8b7355),
                  letterSpacing: 0.5,
                ),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(6),
                  border: const Border(
                    left: BorderSide(
                      color: Color(0xFFd4c4a8),
                      width: 2,
                    ),
                  ),
                ),
                child: Text(
                  '"${anno.quote}"',
                  style: const TextStyle(
                    fontSize: 12,
                    fontStyle: FontStyle.italic,
                    color: Color(0xFF7a6a55),
                    height: 1.5,
                  ),
                ),
              ),
              const SizedBox(height: 10),
              ...anno.insights.map((insight) => Padding(
                    padding: const EdgeInsets.only(bottom: 4),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          '▸',
                          style: TextStyle(
                            fontSize: 10,
                            color: Color(0xFFc97d60),
                          ),
                        ),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            insight,
                            style: const TextStyle(
                              fontSize: 12,
                              color: Color(0xFF4a3f35),
                              height: 1.4,
                            ),
                          ),
                        ),
                      ],
                    ),
                  )),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
              decoration: BoxDecoration(
                color: const Color(0xFFf4f9f4),
                borderRadius: BorderRadius.circular(6),
                border: const Border(
                  left: BorderSide(
                    color: Color(0xFFb8d4b8),
                    width: 3,
                  ),
                ),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    '💡',
                    style: TextStyle(fontSize: 12),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      anno.action,
                      style: const TextStyle(
                        fontSize: 11,
                        color: Color(0xFF3b5e3b),
                        height: 1.5,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            ],
          ),
        ),
      ),
    );
  }
}