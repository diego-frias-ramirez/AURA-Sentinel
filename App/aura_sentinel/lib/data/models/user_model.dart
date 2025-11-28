class UserModel {
  final String id;
  final String name;
  final String email;
  final String phone;
  final DateTime? birthDate;
  final String? gender;
  final double? weight;
  final bool isVerified;
  final DateTime createdAt;

  UserModel({
    required this.id,
    required this.name,
    required this.email,
    required this.phone,
    this.birthDate,
    this.gender,
    this.weight,
    this.isVerified = false,
    required this.createdAt,
  });

  // Convertir a Map para Firestore/AppWrite
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'phone': phone,
      'birthDate': birthDate?.toIso8601String(),
      'gender': gender,
      'weight': weight,
      'isVerified': isVerified,
      'createdAt': createdAt.toIso8601String(),
    };
  }

  // Crear desde Map
  factory UserModel.fromMap(Map<String, dynamic> map) {
    return UserModel(
      id: map['id'] ?? '',
      name: map['name'] ?? '',
      email: map['email'] ?? '',
      phone: map['phone'] ?? '',
      birthDate: map['birthDate'] != null
          ? DateTime.parse(map['birthDate'])
          : null,
      gender: map['gender'],
      weight: map['weight']?.toDouble(),
      isVerified: map['isVerified'] ?? false,
      createdAt: DateTime.parse(map['createdAt']),
    );
  }

  // Copiar con cambios
  UserModel copyWith({
    String? id,
    String? name,
    String? email,
    String? phone,
    DateTime? birthDate,
    String? gender,
    double? weight,
    bool? isVerified,
    DateTime? createdAt,
  }) {
    return UserModel(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      phone: phone ?? this.phone,
      birthDate: birthDate ?? this.birthDate,
      gender: gender ?? this.gender,
      weight: weight ?? this.weight,
      isVerified: isVerified ?? this.isVerified,
      createdAt: createdAt ?? this.createdAt,
    );
  }
}
