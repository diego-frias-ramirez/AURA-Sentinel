// medical_model.dart
class MedicalModel {
  final String userId;
  final String bloodType;
  final List<String> allergies;
  final List<String> medicalConditions;
  final List<Medication> medications;
  final InsuranceInfo? insurance;
  final DateTime lastUpdated;

  MedicalModel({
    required this.userId,
    required this.bloodType,
    this.allergies = const [],
    this.medicalConditions = const [],
    this.medications = const [],
    this.insurance,
    required this.lastUpdated,
  });

  Map<String, dynamic> toMap() {
    return {
      'userId': userId,
      'bloodType': bloodType,
      'allergies': allergies,
      'medicalConditions': medicalConditions,
      'medications': medications.map((med) => med.toMap()).toList(),
      'insurance': insurance?.toMap(),
      'lastUpdated': lastUpdated.toIso8601String(),
    };
  }

  factory MedicalModel.fromMap(Map<String, dynamic> map) {
    return MedicalModel(
      userId: map['userId'] ?? '',
      bloodType: map['bloodType'] ?? '',
      allergies: List<String>.from(map['allergies'] ?? []),
      medicalConditions: List<String>.from(map['medicalConditions'] ?? []),
      medications: List<Medication>.from(
        (map['medications'] ?? []).map((x) => Medication.fromMap(x)),
      ),
      insurance: map['insurance'] != null
          ? InsuranceInfo.fromMap(map['insurance'])
          : null,
      lastUpdated: DateTime.parse(map['lastUpdated']),
    );
  }
}

class Medication {
  final String name;
  final String dosage;
  final String frequency;

  Medication({
    required this.name,
    required this.dosage,
    required this.frequency,
  });

  Map<String, dynamic> toMap() {
    return {'name': name, 'dosage': dosage, 'frequency': frequency};
  }

  factory Medication.fromMap(Map<String, dynamic> map) {
    return Medication(
      name: map['name'] ?? '',
      dosage: map['dosage'] ?? '',
      frequency: map['frequency'] ?? '',
    );
  }
}

class InsuranceInfo {
  final String provider;
  final String policyNumber;
  final DateTime validUntil;

  InsuranceInfo({
    required this.provider,
    required this.policyNumber,
    required this.validUntil,
  });

  Map<String, dynamic> toMap() {
    return {
      'provider': provider,
      'policyNumber': policyNumber,
      'validUntil': validUntil.toIso8601String(),
    };
  }

  factory InsuranceInfo.fromMap(Map<String, dynamic> map) {
    return InsuranceInfo(
      provider: map['provider'] ?? '',
      policyNumber: map['policyNumber'] ?? '',
      validUntil: DateTime.parse(map['validUntil']),
    );
  }
}
