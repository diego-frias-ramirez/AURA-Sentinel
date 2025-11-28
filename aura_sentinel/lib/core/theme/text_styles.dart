// lib/core/theme/text_styles.dart
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'colors.dart';

class AppTextStyles {
  // ===========================
  //  HEADINGS
  // ===========================

  // H1 - Título principal
  static TextStyle h1 = GoogleFonts.inter(
    fontSize: 32,
    fontWeight: FontWeight.bold,
    color: AppColors.textPrimary,
    height: 1.2,
    letterSpacing: -0.5,
  );

  // H2 - Título secundario
  static TextStyle h2 = GoogleFonts.inter(
    fontSize: 28,
    fontWeight: FontWeight.bold,
    color: AppColors.textPrimary,
    height: 1.3,
    letterSpacing: -0.3,
  );

  // H3 - Título terciario
  static TextStyle h3 = GoogleFonts.inter(
    fontSize: 24,
    fontWeight: FontWeight.w600,
    color: AppColors.textPrimary,
    height: 1.3,
  );

  // H4 - Subtítulo grande
  static TextStyle h4 = GoogleFonts.inter(
    fontSize: 20,
    fontWeight: FontWeight.w600,
    color: AppColors.textPrimary,
    height: 1.4,
  );

  // ===========================
  //  SUBTÍTULOS
  // ===========================

  static TextStyle subtitle1 = GoogleFonts.inter(
    fontSize: 18,
    fontWeight: FontWeight.w500,
    color: AppColors.textPrimary,
    height: 1.5,
  );

  static TextStyle subtitle2 = GoogleFonts.inter(
    fontSize: 16,
    fontWeight: FontWeight.w500,
    color: AppColors.textSecondary,
    height: 1.5,
  );

  // ===========================
  //  BODY TEXT
  // ===========================

  static TextStyle body1 = GoogleFonts.inter(
    fontSize: 16,
    fontWeight: FontWeight.normal,
    color: AppColors.textPrimary,
    height: 1.5,
  );

  static TextStyle body2 = GoogleFonts.inter(
    fontSize: 14,
    fontWeight: FontWeight.normal,
    color: AppColors.textSecondary,
    height: 1.5,
  );

  // ===========================
  //  BOTONES
  // ===========================

  static TextStyle button = GoogleFonts.inter(
    fontSize: 16,
    fontWeight: FontWeight.w600,
    letterSpacing: 0.5,
    height: 1.2,
  );

  static TextStyle buttonSmall = GoogleFonts.inter(
    fontSize: 14,
    fontWeight: FontWeight.w600,
    letterSpacing: 0.5,
    height: 1.2,
  );

  // ===========================
  //  CAPTION & OVERLINE
  // ===========================

  static TextStyle caption = GoogleFonts.inter(
    fontSize: 12,
    fontWeight: FontWeight.normal,
    color: AppColors.textSecondary,
    height: 1.4,
  );

  static TextStyle overline = GoogleFonts.inter(
    fontSize: 10,
    fontWeight: FontWeight.w600,
    color: AppColors.textTertiary,
    letterSpacing: 1.5,
    height: 1.6,
  );

  // ===========================
  //  ESTILOS ESPECIALES
  // ===========================

  // Botón de emergencia
  static TextStyle emergency = GoogleFonts.inter(
    fontSize: 20,
    fontWeight: FontWeight.bold,
    color: Colors.white,
    letterSpacing: 1,
    height: 1.2,
  );

  // Números grandes (ej: contador, timer)
  static TextStyle numeric = GoogleFonts.robotoMono(
    fontSize: 48,
    fontWeight: FontWeight.bold,
    color: AppColors.textPrimary,
    height: 1,
  );

  // Código (ej: código QR, ID)
  static TextStyle code = GoogleFonts.robotoMono(
    fontSize: 14,
    fontWeight: FontWeight.normal,
    color: AppColors.textSecondary,
    height: 1.5,
    letterSpacing: 1,
  );

  // ===========================
  //  ESTILOS M3 (Material 3)
  // ===========================
  // Agregamos los estilos de Material 3 que faltan, como headlineMedium
  static TextStyle headlineLarge = GoogleFonts.inter(
    fontSize: 32,
    fontWeight: FontWeight.w400,
    color: AppColors.textPrimary,
    height: 1.2,
  );

  static TextStyle headlineMedium = GoogleFonts.inter(
    // ✅ ESTE ES EL ESTILO FALTANTE
    fontSize: 28,
    fontWeight: FontWeight.w400,
    color: AppColors.textPrimary,
    height: 1.3,
  );

  static TextStyle headlineSmall = GoogleFonts.inter(
    fontSize: 24,
    fontWeight: FontWeight.w400,
    color: AppColors.textPrimary,
    height: 1.3,
  );

  static TextStyle titleLarge = GoogleFonts.inter(
    fontSize: 22,
    fontWeight: FontWeight.w500,
    color: AppColors.textPrimary,
    height: 1.4,
  );

  static TextStyle titleMedium = GoogleFonts.inter(
    fontSize: 16,
    fontWeight: FontWeight.w500,
    color: AppColors.textPrimary,
    height: 1.5,
  );

  static TextStyle titleSmall = GoogleFonts.inter(
    fontSize: 14,
    fontWeight: FontWeight.w500,
    color: AppColors.textPrimary,
    height: 1.6,
  );

  // ===========================
  //  HELPERS
  // ===========================

  // Aplicar color personalizado
  static TextStyle withColor(TextStyle style, Color color) {
    return style.copyWith(color: color);
  }

  // Texto en negrita
  static TextStyle bold(TextStyle style) {
    return style.copyWith(fontWeight: FontWeight.bold);
  }

  // Texto en semi-negrita
  static TextStyle semiBold(TextStyle style) {
    return style.copyWith(fontWeight: FontWeight.w600);
  }

  // Texto en regular
  static TextStyle regular(TextStyle style) {
    return style.copyWith(fontWeight: FontWeight.normal);
  }

  // Texto en light
  static TextStyle light(TextStyle style) {
    return style.copyWith(fontWeight: FontWeight.w300);
  }

  // Cambiar tamaño
  static TextStyle withSize(TextStyle style, double size) {
    return style.copyWith(fontSize: size);
  }

  // Cambiar altura de línea
  static TextStyle withHeight(TextStyle style, double height) {
    return style.copyWith(height: height);
  }

  // Texto centrado
  static TextStyle centered(TextStyle style) {
    return style;
  }
}
