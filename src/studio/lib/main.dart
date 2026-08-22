import 'package:flutter/material.dart';

void main() {
  runApp(const QtCloudThinkStudioApp());
}

/// 应用壳（4D 导航——分解 4 实施，当前最小壳）
class QtCloudThinkStudioApp extends StatelessWidget {
  const QtCloudThinkStudioApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '量潮思考云',
      theme: ThemeData(useMaterial3: true),
      home: const Scaffold(
        body: Center(child: Text('量潮思考云 · 建设中')),
      ),
    );
  }
}
