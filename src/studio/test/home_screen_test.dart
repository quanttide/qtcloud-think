import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:studio/screens/home_screen.dart';
import 'dart:convert';

void main() {
  group('HomeScreen 聊天功能测试', () {
    testWidgets('用户可以输入想法并发送', (WidgetTester tester) async {
      final mockClient = MockClient((request) async {
        return http.Response(json.encode({'result': '复述：你有一个想法。'}), 200);
      });

      await tester.pumpWidget(
        MaterialApp(home: HomeScreen(client: mockClient)),
      );

      expect(find.text('思维外脑'), findsOneWidget);
      expect(find.text('请输入你的想法...'), findsOneWidget);
      expect(find.text('开始思考'), findsOneWidget);

      await tester.enterText(find.byType(TextField), '测试');
      await tester.pump();

      await tester.tap(find.text('开始思考'));
      await tester.pumpAndSettle();

      expect(find.text('开始思考'), findsOneWidget);
    });

    testWidgets('输入为空时按钮禁用', (WidgetTester tester) async {
      final mockClient = MockClient((request) async {
        return http.Response('Not Found', 404);
      });

      await tester.pumpWidget(
        MaterialApp(home: HomeScreen(client: mockClient)),
      );

      await tester.pump();

      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.onPressed, isNull);
    });

    testWidgets('有输入时按钮可用', (WidgetTester tester) async {
      final mockClient = MockClient((request) async {
        return http.Response(json.encode({'result': '结果'}), 200);
      });

      await tester.pumpWidget(
        MaterialApp(home: HomeScreen(client: mockClient)),
      );

      await tester.enterText(find.byType(TextField), '测试输入');
      await tester.pump();

      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.onPressed, isNotNull);
    });

    testWidgets('可以查看历史对话', (WidgetTester tester) async {
      final mockClient = MockClient((request) async {
        return http.Response('Not Found', 404);
      });

      await tester.pumpWidget(
        MaterialApp(home: HomeScreen(client: mockClient)),
      );

      expect(find.byIcon(Icons.list), findsOneWidget);
    });

    testWidgets('加载时显示加载指示器', (WidgetTester tester) async {
      bool requestCompleted = false;
      final mockClient = MockClient((request) async {
        await Future.delayed(const Duration(seconds: 2));
        requestCompleted = true;
        return http.Response(json.encode({'result': '结果'}), 200);
      });

      await tester.pumpWidget(
        MaterialApp(home: HomeScreen(client: mockClient)),
      );

      await tester.enterText(find.byType(TextField), '测试');
      await tester.pump();
      await tester.tap(find.text('开始思考'));
      await tester.pump();

      expect(find.byType(CircularProgressIndicator), findsOneWidget);

      await tester.pump(const Duration(seconds: 3));
      expect(requestCompleted, isTrue);
    });
  });

  group('HomeScreen 导航测试', () {
    testWidgets('可以导航到笔记列表', (WidgetTester tester) async {
      final mockClient = MockClient((request) async {
        return http.Response('Not Found', 404);
      });

      await tester.pumpWidget(
        MaterialApp(
          home: HomeScreen(client: mockClient),
          routes: {'/notes': (context) => const Scaffold(body: Text('笔记列表'))},
        ),
      );

      await tester.tap(find.byIcon(Icons.list));
      await tester.pumpAndSettle();

      expect(find.text('笔记列表'), findsOneWidget);
    });
  });

  group('HomeScreen 错误处理', () {
    testWidgets('API 错误时保持界面可用', (WidgetTester tester) async {
      final mockClient = MockClient((request) async {
        return http.Response('Server Error', 500);
      });

      await tester.pumpWidget(
        MaterialApp(home: HomeScreen(client: mockClient)),
      );

      await tester.enterText(find.byType(TextField), '测试');
      await tester.pump();
      await tester.tap(find.text('开始思考'));
      await tester.pumpAndSettle();

      expect(find.text('开始思考'), findsOneWidget);
    });

    testWidgets('网络错误时保持界面可用', (WidgetTester tester) async {
      final mockClient = MockClient((request) async {
        throw Exception('Network error');
      });

      await tester.pumpWidget(
        MaterialApp(home: HomeScreen(client: mockClient)),
      );

      await tester.enterText(find.byType(TextField), '测试');
      await tester.pump();
      await tester.tap(find.text('开始思考'));
      await tester.pumpAndSettle();

      expect(find.text('开始思考'), findsOneWidget);
    });
  });
}
