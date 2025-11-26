import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'app/app.dart';
import 'services/appwrite_service.dart';

// Inicialización de notificaciones locales
final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
    FlutterLocalNotificationsPlugin();

void main() async {
  // Asegurar inicialización de Flutter
  WidgetsFlutterBinding.ensureInitialized();

  // ===========================
  // 🔒 ORIENTACIÓN DE PANTALLA
  // ===========================
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  // ===========================
  // 🎨 ESTILO DE BARRA DE ESTADO
  // ===========================
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.dark,
      systemNavigationBarColor: Colors.white,
      systemNavigationBarIconBrightness: Brightness.dark,
    ),
  );

  // ===========================
  // 🗄️ INICIALIZAR HIVE (Base de datos local)
  // ===========================
  await Hive.initFlutter();

  // Abrir cajas de Hive para datos offline
  await Hive.openBox('user_data');
  await Hive.openBox('medical_data');
  await Hive.openBox('emergency_data');
  await Hive.openBox('contacts_data');
  await Hive.openBox('settings');

  // ===========================
  // 🔷 INICIALIZAR APPWRITE (Backend)
  // ===========================
  try {
    await AppWriteService.initialize();
    print('✅ AppWrite inicializado correctamente');
  } catch (e) {
    print('⚠️ AppWrite no configurado: $e');
    // Continuar sin AppWrite (la app funciona offline)
  }

  // ===========================
  // 🔔 INICIALIZAR NOTIFICACIONES LOCALES
  // ===========================
  const AndroidInitializationSettings initializationSettingsAndroid =
      AndroidInitializationSettings('@mipmap/ic_launcher');

  const DarwinInitializationSettings initializationSettingsIOS =
      DarwinInitializationSettings(
        requestAlertPermission: true,
        requestBadgePermission: true,
        requestSoundPermission: true,
      );

  const InitializationSettings initializationSettings = InitializationSettings(
    android: initializationSettingsAndroid,
    iOS: initializationSettingsIOS,
  );

  await flutterLocalNotificationsPlugin.initialize(
    initializationSettings,
    onDidReceiveNotificationResponse: (NotificationResponse response) {
      // Manejar tap en notificación
      print('Notificación presionada: ${response.payload}');
    },
  );

  // ===========================
  // 🚀 EJECUTAR APP
  // ===========================
  runApp(const AuraSentinelApp());
}
