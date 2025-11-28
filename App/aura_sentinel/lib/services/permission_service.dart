// permission_service.dart
import 'package:permission_handler/permission_handler.dart';

class PermissionService {
  static final PermissionService _instance = PermissionService._internal();
  factory PermissionService() => _instance;
  PermissionService._internal();

  /// Solicitar permisos esenciales
  Future<Map<Permission, PermissionStatus>>
  requestEssentialPermissions() async {
    final permissions = [
      Permission.location,
      Permission.camera,
      Permission.contacts,
      Permission.notification,
      Permission.phone,
    ];

    final results = <Permission, PermissionStatus>{};

    for (var permission in permissions) {
      final status = await permission.request();
      results[permission] = status;
    }

    return results;
  }

  /// Verificar permisos individuales
  Future<bool> checkLocationPermission() async =>
      (await Permission.location.status).isGranted;

  Future<bool> checkCameraPermission() async =>
      (await Permission.camera.status).isGranted;

  Future<bool> checkContactsPermission() async =>
      (await Permission.contacts.status).isGranted;

  Future<bool> checkNotificationPermission() async =>
      (await Permission.notification.status).isGranted;

  /// Verificar si TODOS los permisos esenciales están concedidos
  Future<bool> areAllEssentialPermissionsGranted() async {
    final permissions = [
      await checkLocationPermission(),
      await checkCameraPermission(),
      await checkContactsPermission(),
      await checkNotificationPermission(),
    ];

    return permissions.every((p) => p == true);
  }

  /// Abrir configuración de la app correctamente (SIN bucle infinito)
  Future<void> openSettings() async {
    await openAppSettings();
  }
}
