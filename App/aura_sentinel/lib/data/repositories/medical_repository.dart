// medical_repository.dart
import '../models/medical_model.dart';

class MedicalRepository {
  final Map<String, MedicalModel> _medicalData = {};

  Future<MedicalModel?> getMedicalData(String userId) async {
    await Future.delayed(const Duration(milliseconds: 500));
    return _medicalData[userId];
  }

  Future<void> saveMedicalData(String userId, MedicalModel medicalData) async {
    await Future.delayed(const Duration(milliseconds: 800));
    _medicalData[userId] = medicalData;
  }

  Future<void> updateMedicalData(
    String userId,
    Map<String, dynamic> updates,
  ) async {
    await Future.delayed(const Duration(milliseconds: 600));
    final currentData = _medicalData[userId];
    if (currentData != null) {
      // En una implementación real, actualizarías campos específicos
      _medicalData[userId] = currentData;
    }
  }

  Future<bool> hasMedicalData(String userId) async {
    await Future.delayed(const Duration(milliseconds: 200));
    return _medicalData.containsKey(userId);
  }

  // Generar datos médicos de ejemplo
  MedicalModel generateSampleMedicalData(String userId) {
    return MedicalModel(
      userId: userId,
      bloodType: 'O+',
      allergies: ['Penicilina', 'Maní'],
      medicalConditions: ['Asma', 'Hipertensión'],
      medications: [
        Medication(
          name: 'Salbutamol',
          dosage: '100 mcg',
          frequency: 'Según necesidad',
        ),
        Medication(
          name: 'Losartán',
          dosage: '50 mg',
          frequency: '1 vez al día',
        ),
      ],
      insurance: InsuranceInfo(
        provider: 'Seguro Nacional de Salud',
        policyNumber: 'SNS-2024-789456',
        validUntil: DateTime(2025, 12, 31),
      ),
      lastUpdated: DateTime.now(),
    );
  }
}
