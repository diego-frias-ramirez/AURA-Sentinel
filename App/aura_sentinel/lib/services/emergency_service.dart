import 'package:flutter/services.dart';
import '../services/appwrite_service.dart';

class EmergencyService {
  static final EmergencyService _instance = EmergencyService._internal();
  factory EmergencyService() => _instance;
  EmergencyService._internal();

  bool _isEmergencyActive = false;
  DateTime? _emergencyStartTime;

  // Activar emergencia
  Future<bool> activateEmergency({
    required String userId,
    required double lat,
    required double lng,
    required String address,
    required List<String> contactIds,
  }) async {
    try {
      if (_isEmergencyActive) {
        return false;
      }

      _isEmergencyActive = true;
      _emergencyStartTime = DateTime.now();

      // 1. Notificar contactos de emergencia
      await _notifyEmergencyContacts(contactIds, userId, address);

      // 2. Alertar servicios de emergencia
      await _alertEmergencyServices(lat, lng, address);

      // 3. Registrar en base de datos
      await _logEmergencyActivation(userId, lat, lng, address);

      // 4. Iniciar seguimiento de ubicación
      await _startLocationTracking();

      return true;
    } catch (e) {
      _isEmergencyActive = false;
      _emergencyStartTime = null;
      return false;
    }
  }

  // Cancelar emergencia
  Future<bool> cancelEmergency(String userId) async {
    try {
      if (!_isEmergencyActive) {
        print('⚠️ No hay emergencia activa para cancelar');
        return false;
      }

      // 1. Notificar a contactos que la situación está resuelta
      await _notifyEmergencyResolved(userId);

      // 2. Detener seguimiento de ubicación
      await _stopLocationTracking();

      // 3. Actualizar estado en base de datos
      await _logEmergencyResolution(userId);

      _isEmergencyActive = false;
      _emergencyStartTime = null;

      print('✅ Emergencia cancelada correctamente');
      return true;
    } catch (e) {
      print('❌ Error cancelando emergencia: $e');
      return false;
    }
  }

  // Llamar a servicios de emergencia
  Future<void> callEmergencyServices() async {
    try {
      // Llamar al 911
      await _makePhoneCall('911');
    } catch (e) {
      print('❌ Error llamando a servicios de emergencia: $e');
    }
  }

  // Métodos privados
  Future<void> _notifyEmergencyContacts(
    List<String> contactIds,
    String userId,
    String address,
  ) async {
    // TODO: Implementar notificaciones push a contactos
    print('📞 Notificando a ${contactIds.length} contactos de emergencia');
    await Future.delayed(const Duration(milliseconds: 500));
  }

  Future<void> _alertEmergencyServices(
    double lat,
    double lng,
    String address,
  ) async {
    // TODO: Integrar con APIs de servicios de emergencia
    print('🚓 Alertando servicios de emergencia en: $address');
    await Future.delayed(const Duration(milliseconds: 300));
  }

  Future<void> _logEmergencyActivation(
    String userId,
    double lat,
    double lng,
    String address,
  ) async {
    // TODO: Guardar en base de datos
    await AppWriteService.logEmergency(userId, {
      'latitude': lat,
      'longitude': lng,
      'address': address,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }

  Future<void> _logEmergencyResolution(String userId) async {
    // TODO: Actualizar en base de datos
    print('📝 Registrando resolución de emergencia para: $userId');
    await Future.delayed(const Duration(milliseconds: 200));
  }

  Future<void> _notifyEmergencyResolved(String userId) async {
    // TODO: Notificar a contactos
    print('✅ Notificando resolución de emergencia a contactos');
    await Future.delayed(const Duration(milliseconds: 300));
  }

  Future<void> _startLocationTracking() async {
    // TODO: Iniciar seguimiento continuo de ubicación
    print('📍 Iniciando seguimiento de ubicación en tiempo real');
  }

  Future<void> _stopLocationTracking() async {
    // TODO: Detener seguimiento de ubicación
    print('📍 Deteniendo seguimiento de ubicación');
  }

  Future<void> _makePhoneCall(String phoneNumber) async {
    try {
      await Clipboard.setData(ClipboardData(text: phoneNumber));
      // En un entorno real, usaríamos: launch('tel:$phoneNumber');
      print('📞 Llamando a: $phoneNumber');
    } catch (e) {
      print('❌ Error iniciando llamada: $e');
    }
  }

  // Getters
  bool get isEmergencyActive => _isEmergencyActive;
  DateTime? get emergencyStartTime => _emergencyStartTime;
  Duration? get emergencyDuration => _emergencyStartTime != null
      ? DateTime.now().difference(_emergencyStartTime!)
      : null;
}
