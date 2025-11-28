import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:aura_sentinel/app/app.dart'; // Clase AuraSentinelApp

void main() {
  testWidgets('App inicia correctamente', (WidgetTester tester) async {
    await tester.pumpWidget(const AuraSentinelApp());

    // Verifica que exista al menos un MaterialApp
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
