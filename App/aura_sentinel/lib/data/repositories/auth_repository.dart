// auth_repository.dart
import '../models/user_model.dart';

class AuthRepository {
  // Simular autenticación - en producción usarías AppWrite/Firebase
  Future<UserModel?> login(String email, String password) async {
    await Future.delayed(const Duration(seconds: 2)); // Simulación

    if (email.isNotEmpty && password.isNotEmpty) {
      return UserModel(
        id: 'user_${DateTime.now().millisecondsSinceEpoch}',
        name: 'Usuario Demo',
        email: email,
        phone: '+52 55 1234 5678',
        isVerified: true,
        createdAt: DateTime.now(),
      );
    }

    return null;
  }

  Future<UserModel?> register(Map<String, dynamic> userData) async {
    await Future.delayed(const Duration(seconds: 2)); // Simulación

    return UserModel(
      id: 'user_${DateTime.now().millisecondsSinceEpoch}',
      name: userData['name'] ?? '',
      email: userData['email'] ?? '',
      phone: userData['phone'] ?? '',
      birthDate: userData['birthDate'],
      gender: userData['gender'],
      weight: userData['weight'],
      isVerified: false,
      createdAt: DateTime.now(),
    );
  }

  Future<bool> verifyIdentity(String userId) async {
    await Future.delayed(const Duration(seconds: 3)); // Simulación
    return true;
  }

  Future<void> logout() async {
    await Future.delayed(const Duration(milliseconds: 500));
  }

  Future<bool> resetPassword(String email) async {
    await Future.delayed(const Duration(seconds: 1));
    return email.contains('@');
  }
}
