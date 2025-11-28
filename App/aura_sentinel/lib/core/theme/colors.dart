import 'package:flutter/material.dart';

class AppColors {
  // Colores primarios
  static const Color primary = Color(0xFF007BFF);
  static const Color primaryDark = Color(0xFF0056CC);
  static const Color primaryLight = Color(0xFF66AFFF);

  // Colores secundarios
  static const Color secondary = Color(0xFF00C6FF);
  static const Color secondaryDark = Color(0xFF0099CC);
  static const Color secondaryLight = Color(0xFF66E0FF);

  // Colores de estado
  static const Color success = Color(0xFF28A745);
  static const Color warning = Color(0xFFFFC107);
  static const Color error = Color(0xFFDC3545);
  static const Color info = Color(0xFF17A2B8);

  // Colores de emergencia
  static const Color emergency = Color(0xFFDC3545);
  static const Color emergencyDark = Color(0xFFC82333);
  static const Color emergencyLight = Color(0xFFFF6B6B);

  // Colores neutros
  static const Color backgroundLight = Color(0xFFF8F9FA);
  static const Color backgroundDark = Color(0xFF121212);
  static const Color surfaceLight = Color(0xFFFFFFFF);
  static const Color surfaceDark = Color(0xFF1E1E1E);
  static const Color outline = Color(0xFFDEE2E6);
  static const Color textPrimary = Color(0xFF212529);
  static const Color textSecondary = Color(0xFF6C757D);
  static const Color textDisabled = Color(0xFFADB5BD);

  // Colores de categorías
  static const Color medical = Color(0xFFE74C3C);
  static const Color security = Color(0xFF3498DB);
  static const Color psychological = Color(0xFF9B59B6);
  static const Color community = Color(0xFF2ECC71);

  // Gradientes
  static const Gradient primaryGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [primary, secondary],
  );

  static const Gradient emergencyGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [emergency, Color(0xFFFF6B6B)],
  );

  static const Gradient successGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [success, Color(0xFF7CFC00)],
  );
}
