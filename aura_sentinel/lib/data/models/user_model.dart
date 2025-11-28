// user_model.dart
class UserModel {
  final String id;
  final String name;
  final String email;
  final String? phone;
  final String? photoUrl;
  final DateTime createdAt;
  final DateTime? lastLogin;
  final bool isVerified;
  final bool biometricEnabled;

  UserModel({
    required this.id,
    required this.name,
    required this.email,
    this.phone,
    this.photoUrl,
    required this.createdAt,
    this.lastLogin,
    this.isVerified = false,
    this.biometricEnabled = false,
  });

  // Convertir de JSON (AppWrite)
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] ?? json['\$id'] ?? '',
      name: json['name'] ?? '',
      email: json['email'] ?? '',
      phone: json['phone'],
      photoUrl: json['photoUrl'],
      createdAt: json['createdAt'] != null
          ? DateTime.parse(json['createdAt'])
          : DateTime.now(),
      lastLogin: json['lastLogin'] != null
          ? DateTime.parse(json['lastLogin'])
          : null,
      isVerified: json['isVerified'] ?? false,
      biometricEnabled: json['biometricEnabled'] ?? false,
    );
  }

  // Convertir a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'phone': phone,
      'photoUrl': photoUrl,
      'createdAt': createdAt.toIso8601String(),
      'lastLogin': lastLogin?.toIso8601String(),
      'isVerified': isVerified,
      'biometricEnabled': biometricEnabled,
    };
  }

  // Copiar con modificaciones
  UserModel copyWith({
    String? id,
    String? name,
    String? email,
    String? phone,
    String? photoUrl,
    DateTime? createdAt,
    DateTime? lastLogin,
    bool? isVerified,
    bool? biometricEnabled,
  }) {
    return UserModel(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      phone: phone ?? this.phone,
      photoUrl: photoUrl ?? this.photoUrl,
      createdAt: createdAt ?? this.createdAt,
      lastLogin: lastLogin ?? this.lastLogin,
      isVerified: isVerified ?? this.isVerified,
      biometricEnabled: biometricEnabled ?? this.biometricEnabled,
    );
  }
}
