import 'package:flutter/material.dart';
import '../models/journal_data.dart';

class AnnotationScreen extends StatefulWidget {
  const AnnotationScreen({super.key});

  @override
  State<AnnotationScreen> createState() => _AnnotationScreenState();
}

class _AnnotationScreenState extends State<AnnotationScreen> {
  String? _activeCardId;

  void _activateCard(String cardId) {
    setState(() {
      if (_activeCardId == cardId) {
        _activeCardId = null;
      } else {
        _activeCardId = cardId;
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
            final isWide = constraints.maxWidth > 750;
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
          flex: 58,
          child: _buildLogPane(),
        ),
        Container(
          width: 1,
          color: const Color(0xFFe8e0d5),
        ),
        Expanded(
          flex: 42,
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
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 16),
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
                fontSize: 22,
                fontWeight: FontWeight.w700,
                color: Color(0xFF1a1208),
              ),
            ),
            const SizedBox(height: 6),
            const Text(
              '一次密集的思维重构——从焦虑到构建，从执行到澄明',
              style: TextStyle(
                fontSize: 13,
                fontStyle: FontStyle.italic,
                color: Color(0xFF6b5e4a),
              ),
            ),
            const SizedBox(height: 16),
            ...journalEntries.map((para) => _buildJournalEntry(para)),
            const SizedBox(height: 16),
            const Center(
              child: Text(
                '—— 点击高亮词查看对应批注。按 Esc 取消选中。',
                style: TextStyle(
                  fontSize: 12,
                  fontStyle: FontStyle.italic,
                  color: Color(0xFF9b8e7a),
                ),
              ),
            ),
            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }

  Widget _buildJournalEntry(JournalEntry para) {
    if (para.highlights.isEmpty) {
      return Padding(
        padding: const EdgeInsets.only(bottom: 14),
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
      padding: const EdgeInsets.only(bottom: 14),
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

  List<InlineSpan> _buildParagraphSpans(JournalEntry para) {
    final spans = <InlineSpan>[];
    String remaining = para.content;

    for (final highlight in para.highlights) {
      final index = remaining.indexOf(highlight.text);
      if (index == -1) continue;

      if (index > 0) {
        spans.add(TextSpan(text: remaining.substring(0, index)));
      }

      final isActive = _activeCardId == highlight.cardId;
      spans.add(
        WidgetSpan(
          child: GestureDetector(
            onTap: () => _activateCard(highlight.cardId),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 3, vertical: 1),
              decoration: BoxDecoration(
                color: isActive
                    ? const Color(0xFFffe087)
                    : const Color(0xFFfef3c7),
                borderRadius: BorderRadius.circular(3),
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
                highlight.text,
                style: TextStyle(
                  fontWeight: FontWeight.w500,
                  color: const Color(0xFF5c3d2e),
                ),
              ),
            ),
          ),
        ),
      );

      remaining = remaining.substring(index + highlight.text.length);
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
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 8),
            const Center(
              child: Text(
                '🔍 思维标注',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  letterSpacing: 1,
                  color: Color(0xFF9b8e7a),
                ),
              ),
            ),
            const SizedBox(height: 12),
            if (_activeCardId == null)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFFfffdf8),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: Color(0xFFe5dbca)),
                ),
                child: const Center(
                  child: Text(
                    '点击左侧高亮文字，\n这里将显示对应的思维工具。',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 13,
                      color: Color(0xFFbfb5a3),
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                ),
              ),
            ...cognitiveCards.map((anno) => _buildAnnotationCard(anno)),
          ],
        ),
      ),
    );
  }

  Widget _buildAnnotationCard(CognitiveCard card) {
    final isActive = _activeCardId == card.id;

    return GestureDetector(
      onTap: () => _activateCard(card.id),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 250),
        curve: Curves.ease,
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        decoration: BoxDecoration(
          color: isActive ? const Color(0xFFfffef9) : const Color(0xFFfffdf8),
          borderRadius: BorderRadius.circular(10),
          border: Border.all(
            color: isActive ? const Color(0xFFc97d60) : const Color(0xFFe5dbca),
            width: isActive ? 1.5 : 1,
          ),
          boxShadow: isActive
              ? [
                  BoxShadow(
                    color: const Color(0xFFc97d60).withValues(alpha: 0.08),
                    blurRadius: 10,
                    offset: const Offset(0, 2),
                  ),
                ]
              : null,
        ),
        child: Opacity(
          opacity: isActive ? 1.0 : 0.75,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                card.title,
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w700,
                  color: Color(0xFF4a3a2a),
                ),
              ),
              const SizedBox(height: 6),
              Text(
                '"${card.quote}"',
                style: const TextStyle(
                  fontSize: 12,
                  fontStyle: FontStyle.italic,
                  color: Color(0xFF9b8e7a),
                ),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                decoration: BoxDecoration(
                  color: const Color(0xFFf7faf7),
                  borderRadius: BorderRadius.circular(5),
                ),
                child: Row(
                  children: [
                    const Text(
                      '▸',
                      style: TextStyle(
                        fontSize: 11,
                        color: Color(0xFF3b5e3b),
                      ),
                    ),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(
                        card.action,
                        style: const TextStyle(
                          fontSize: 12,
                          color: Color(0xFF3b5e3b),
                          height: 1.4,
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