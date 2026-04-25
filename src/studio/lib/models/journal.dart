class JournalEntry {
  final String id;
  final String content;
  final List<Highlight> highlights;

  const JournalEntry({
    required this.id,
    required this.content,
    required this.highlights,
  });
}

class Highlight {
  final String id;
  final String text;
  final String cardId;

  const Highlight({
    required this.id,
    required this.text,
    required this.cardId,
  });
}

class CognitiveCard {
  final String id;
  final String title;
  final String quote;
  final String action;

  const CognitiveCard({
    required this.id,
    required this.title,
    required this.quote,
    required this.action,
  });
}