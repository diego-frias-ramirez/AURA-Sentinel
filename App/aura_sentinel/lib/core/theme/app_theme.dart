import 'package:flutter/material.dart';
import 'colors.dart';
import 'text_styles.dart';

class AppTheme {
  // Tema claro
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.light(
        primary: AppColors.primary,
        secondary: AppColors.secondary,
        error: AppColors.error,
        surface: AppColors.backgroundLight,
      ),
      scaffoldBackgroundColor: AppColors.backgroundLight,

      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: AppTextStyles.headlineSmall.copyWith(
          color: Colors.white,
        ),
      ),

      // ⬅️ USO CORRECTO EN MATERIAL 3
      cardTheme: CardThemeData(
        elevation: 2,
        color: AppColors.surfaceLight,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),

      // Material 3 → buttonTheme está obsoleto
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
        ),
      ),

      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.outline),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.outline),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.primary),
        ),
        filled: true,
        fillColor: Colors.white,
      ),
    );
  }

  // Tema oscuro
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.dark(
        primary: AppColors.primary,
        secondary: AppColors.secondary,
        error: AppColors.error,
        surface: AppColors.backgroundDark, // ⬅️ reemplaza background
      ),
      scaffoldBackgroundColor: AppColors.backgroundDark,

      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.surfaceDark,
        elevation: 0,
        centerTitle: true,
      ),

      // ⬅️ USO CORRECTO EN MATERIAL 3
      cardTheme: CardThemeData(
        elevation: 4,
        color: AppColors.surfaceDark,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
    );
  }
}
