// emergency_repository.dart
import '../models/emergency_model.dart';

class EmergencyRepository {
  final List<EmergencyModel> _emergencies = [];

  Future<String> logEmergency(EmergencyModel emergency) async {
    await Future.delayed(const Duration(milliseconds: 300));
    _emergencies.add(emergency);
    return emergency.id;
  }

  Future<void> updateEmergencyStatus(
    String emergencyId,
    EmergencyStatus status,
  ) async {
    await Future.delayed(const Duration(milliseconds: 200));
    final index = _emergencies.indexWhere((e) => e.id == emergencyId);
    if (index != -1) {
      final emergency = _emergencies[index];
      _emergencies[index] = emergency; // En realidad actualizarías el estado
    }
  }

  Future<List<EmergencyModel>> getUserEmergencies(String userId) async {
    await Future.delayed(const Duration(milliseconds: 500));
    return _emergencies.where((e) => e.userId == userId).toList();
  }

  Future<EmergencyModel?> getActiveEmergency(String userId) async {
    await Future.delayed(const Duration(milliseconds: 300));
    return _emergencies.firstWhere(
      (e) => e.userId == userId && e.status == EmergencyStatus.active,
      orElse: () => throw StateError('No active emergency'),
    );
  }

  // Generar ID único para emergencia
  String _generateEmergencyId() {
    return 'emergency_${DateTime.now().millisecondsSinceEpoch}';
  }

  // Crear nueva emergencia
  EmergencyModel createNewEmergency({
    required String userId,
    required EmergencyType type,
    required double lat,
    required double lng,
    required String address,
    required List<String> contactIds,
  }) {
    return EmergencyModel(
      id: _generateEmergencyId(),
      userId: userId,
      type: type,
      status: EmergencyStatus.active,
      activatedAt: DateTime.now(),
      location: LocationData(latitude: lat, longitude: lng, address: address),
      notifiedContacts: contactIds,
      alertedServices: [EmergencyService.police, EmergencyService.ambulance],
    );
  }
}
