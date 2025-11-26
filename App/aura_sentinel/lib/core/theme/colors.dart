import 'package:flutter/material.dart';

class AppColors {
  // ===========================
  //  COLORES PRINCIPALES
  // ===========================

  // Gradiente turquesa-azul (como en tus diseños)
  static const Color primary = Color(0xFF00BFA5); // Turquesa
  static const Color primaryLight = Color(0xFF64FFDA);
  static const Color primaryDark = Color(0xFF00897B);

  static const Color secondary = Color(0xFF0288D1); // Azul
  static const Color secondaryLight = Color(0xFF4FC3F7);
  static const Color secondaryDark = Color(0xFF01579B);

  // ===========================
  //  COLORES DE ESTADO
  // ===========================
  static const Color emergency = Color(0xFFEF5350); // Rojo para botón de pánico
  static const Color success = Color(0xFF66BB6A); // Verde para éxito
  static const Color warning = Color(0xFFFFCA28); // Amarillo para advertencias
  static const Color error = Color(0xFFEF5350); // Rojo para errores
  static const Color info = Color(0xFF29B6F6); // Azul para información

  // ===========================
  //  BACKGROUNDS
  // ===========================
  static const Color background = Color(0xFFF5F7FA); // Gris muy claro
  static const Color surface = Colors.white;
  static const Color inputBackground = Color(
    0xFFF0F4F8,
  ); // Gris claro para inputs

  // ===========================
  //  TEXTOS
  // ===========================
  static const Color textPrimary = Color(0xFF1A1A1A); // Negro suave
  static const Color textSecondary = Color(0xFF6B7280); // Gris medio
  static const Color textTertiary = Color(0xFF9CA3AF); // Gris claro
  static const Color textDisabled = Color(0xFFD1D5DB); // Gris muy claro

  // ===========================
  //  BORDERS & DIVIDERS
  // ===========================
  static const Color border = Color(0xFFE5E7EB);
  static const Color divider = Color(0xFFE5E7EB);

  // ===========================
  //  OVERLAYS
  // ===========================
  static const Color overlay = Color(0x80000000); // Negro 50% transparencia
  static const Color shimmer = Color(0xFFE0E0E0);

  // ===========================
  //  GRADIENTES
  // ===========================
  static const LinearGradient primaryGradient = LinearGradient(
    colors: [primary, secondary],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient emergencyGradient = LinearGradient(
    colors: [Color(0xFFEF5350), Color(0xFFE53935)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );

  static const LinearGradient successGradient = LinearGradient(
    colors: [Color(0xFF66BB6A), Color(0xFF43A047)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // ===========================
  //  COLORES MÉDICOS
  // ===========================
  static const Color bloodTypeA = Color(0xFFE57373);
  static const Color bloodTypeB = Color(0xFF64B5F6);
  static const Color bloodTypeAB = Color(0xFFBA68C8);
  static const Color bloodTypeO = Color(0xFF81C784);

  // ===========================
  //  COLORES DE MAPAS
  // ===========================
  static const Color hospitalMarker = Color(0xFFEF5350);
  static const Color shelterMarker = Color(0xFF29B6F6);
  static const Color policeMarker = Color(0xFF5C6BC0);
  static const Color userLocation = Color(0xFF00BFA5);

  // ===========================
  //  COLORES DE GRÁFICOS
  // ===========================
  static const List<Color> chartColors = [
    Color(0xFF00BFA5),
    Color(0xFF0288D1),
    Color(0xFFFFCA28),
    Color(0xFFEF5350),
    Color(0xFF66BB6A),
    Color(0xFFBA68C8),
  ];

  // ===========================
  //  HELPERS
  // ===========================

  // Obtener color con opacidad
  static Color withOpacity(Color color, double opacity) {
    return color.withValues(alpha: opacity);
  }

  // Obtener color de tipo de sangre
  static Color getBloodTypeColor(String bloodType) {
    switch (bloodType.toUpperCase()) {
      case 'A+':
      case 'A-':
        return bloodTypeA;
      case 'B+':
      case 'B-':
        return bloodTypeB;
      case 'AB+':
      case 'AB-':
        return bloodTypeAB;
      case 'O+':
      case 'O-':
        return bloodTypeO;
      default:
        return textSecondary;
    }
  }

  // Obtener color de prioridad de emergencia
  static Color getEmergencyPriorityColor(String priority) {
    switch (priority.toLowerCase()) {
      case 'crítica':
      case 'critical':
        return emergency;
      case 'alta':
      case 'high':
        return warning;
      case 'media':
      case 'medium':
        return info;
      case 'baja':
      case 'low':
        return success;
      default:
        return textSecondary;
    }
  }
}
