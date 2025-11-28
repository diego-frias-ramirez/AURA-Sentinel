// emergency_model.dart
class EmergencyModel {
  final String id;
  final String userId;
  final EmergencyType type;
  final EmergencyStatus status;
  final DateTime activatedAt;
  final DateTime? resolvedAt;
  final LocationData location;
  final List<String> notifiedContacts;
  final List<EmergencyService> alertedServices;

  EmergencyModel({
    required this.id,
    required this.userId,
    required this.type,
    required this.status,
    required this.activatedAt,
    this.resolvedAt,
    required this.location,
    this.notifiedContacts = const [],
    this.alertedServices = const [],
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'userId': userId,
      'type': type.toString(),
      'status': status.toString(),
      'activatedAt': activatedAt.toIso8601String(),
      'resolvedAt': resolvedAt?.toIso8601String(),
      'location': location.toMap(),
      'notifiedContacts': notifiedContacts,
      'alertedServices': alertedServices
          .map((service) => service.toString())
          .toList(),
    };
  }

  factory EmergencyModel.fromMap(Map<String, dynamic> map) {
    return EmergencyModel(
      id: map['id'] ?? '',
      userId: map['userId'] ?? '',
      type: EmergencyType.values.firstWhere(
        (e) => e.toString() == map['type'],
        orElse: () => EmergencyType.medical,
      ),
      status: EmergencyStatus.values.firstWhere(
        (e) => e.toString() == map['status'],
        orElse: () => EmergencyStatus.active,
      ),
      activatedAt: DateTime.parse(map['activatedAt']),
      resolvedAt: map['resolvedAt'] != null
          ? DateTime.parse(map['resolvedAt'])
          : null,
      location: LocationData.fromMap(map['location']),
      notifiedContacts: List<String>.from(map['notifiedContacts'] ?? []),
      alertedServices: List<EmergencyService>.from(
        (map['alertedServices'] ?? []).map(
          (x) => EmergencyService.values.firstWhere(
            (e) => e.toString() == x,
            orElse: () => EmergencyService.police,
          ),
        ),
      ),
    );
  }
}

class LocationData {
  final double latitude;
  final double longitude;
  final String address;

  LocationData({
    required this.latitude,
    required this.longitude,
    required this.address,
  });

  Map<String, dynamic> toMap() {
    return {'latitude': latitude, 'longitude': longitude, 'address': address};
  }

  factory LocationData.fromMap(Map<String, dynamic> map) {
    return LocationData(
      latitude: map['latitude']?.toDouble() ?? 0.0,
      longitude: map['longitude']?.toDouble() ?? 0.0,
      address: map['address'] ?? '',
    );
  }
}

enum EmergencyType { medical, security, psychological, other }

enum EmergencyStatus { active, resolved, cancelled }

enum EmergencyService { police, ambulance, fireDepartment, civilProtection }
