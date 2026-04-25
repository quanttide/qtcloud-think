import 'package:flutter/material.dart';
import 'screens/cognitive_prism_screen.dart';

void main() {
  runApp(const QtCloudThinkApp());
}

class QtCloudThinkApp extends StatelessWidget {
  const QtCloudThinkApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '量潮思考云',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF5b6abf),
          brightness: Brightness.light,
        ),
      ),
      home: const CognitivePrismScreen(),
    );
  }
}