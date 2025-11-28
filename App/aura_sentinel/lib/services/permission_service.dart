// permission_service.dart
import 'package:permission_handler/permission_handler.dart';

class PermissionService {
  static final PermissionService _instance = PermissionService._internal();
  factory PermissionService() => _instance;
  PermissionService._internal();

  // Solicitar permisos esenciales
  Future<Map<Permission, PermissionStatus>>
  requestEssentialPermissions() async {
    final permissions = [
      Permission.location,
      Permission.camera,
      Permission.contacts,
      Permission.notifications,
      Permission.sms,
      Permission.phone,
    ];

    final results = <Permission, PermissionStatus>{};

    for (var permission in permissions) {
      final status = await permission.request();
      results[permission] = status;
    }

    return results;
  }

  // Verificar permisos de ubicación
  Future<bool> checkLocationPermission() async {
    final status = await Permission.location.status;
    return status.isGranted;
  }

  // Verificar permisos de cámara
  Future<bool> checkCameraPermission() async {
    final status = await Permission.camera.status;
    return status.isGranted;
  }

  // Verificar permisos de contactos
  Future<bool> checkContactsPermission() async {
    final status = await Permission.contacts.status;
    return status.isGranted;
  }

  // Verificar permisos de notificaciones
  Future<bool> checkNotificationPermission() async {
    final status = await Permission.notification.status;
    return status.isGranted;
  }

  // Verificar si todos los permisos esenciales están concedidos
  Future<bool> areAllEssentialPermissionsGranted() async {
    final permissions = [
      await checkLocationPermission(),
      await checkCameraPermission(),
      await checkContactsPermission(),
      await checkNotificationPermission(),
    ];

    return permissions.every((isGranted) => isGranted == true);
  }

  // Abrir configuración de la app
  Future<void> openAppSettings() async {
    await openAppSettings();
  }
}
