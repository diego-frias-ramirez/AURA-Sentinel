// notification_service.dart
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();
  factory NotificationService() => _instance;
  NotificationService._internal();

  static final FlutterLocalNotificationsPlugin _notifications =
      FlutterLocalNotificationsPlugin();

  // Inicializar notificaciones
  Future<void> initialize() async {
    const AndroidInitializationSettings androidSettings =
        AndroidInitializationSettings('@mipmap/ic_launcher');

    const DarwinInitializationSettings iosSettings =
        DarwinInitializationSettings(
          requestAlertPermission: true,
          requestBadgePermission: true,
          requestSoundPermission: true,
        );

    const InitializationSettings settings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );

    await _notifications.initialize(settings);
  }

  // Mostrar notificación simple
  Future<void> showNotification({
    required String title,
    required String body,
    int id = 0,
    String? payload,
  }) async {
    const AndroidNotificationDetails androidDetails =
        AndroidNotificationDetails(
          'aura_sentinel_channel',
          'AURA Sentinel Notifications',
          channelDescription: 'Canal para notificaciones de emergencia',
          importance: Importance.high,
          priority: Priority.high,
          ticker: 'ticker',
        );

    const DarwinNotificationDetails iosDetails = DarwinNotificationDetails();

    const NotificationDetails details = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _notifications.show(id, title, body, details, payload: payload);
  }

  // Mostrar notificación de emergencia
  Future<void> showEmergencyNotification({
    required String contactName,
    required String location,
  }) async {
    await showNotification(
      title: '🚨 EMERGENCIA ACTIVADA',
      body: '$contactName ha activado una emergencia en $location',
      id: 1,
    );
  }

  // Mostrar notificación de resolución
  Future<void> showEmergencyResolvedNotification(String contactName) async {
    await showNotification(
      title: '✅ Situación Resuelta',
      body:
          '$contactName ha indicado que la situación de emergencia ha sido resuelta',
      id: 2,
    );
  }

  // Mostrar notificación de recordatorio de seguridad
  Future<void> showSafetyReminder() async {
    await showNotification(
      title: '💡 Recordatorio de Seguridad',
      body: 'Recuerda mantener tu información médica actualizada',
      id: 3,
    );
  }

  // Cancelar todas las notificaciones
  Future<void> cancelAllNotifications() async {
    await _notifications.cancelAll();
  }
}
