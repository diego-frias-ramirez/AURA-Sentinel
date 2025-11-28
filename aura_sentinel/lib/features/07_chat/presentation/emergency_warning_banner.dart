// lib/features/07_chat/presentation/widgets/emergency_warning_banner.dart
import 'package:flutter/material.dart';
// Quitamos la importación de app_theme.dart
// import 'package:aura_sentinel/core/theme/app_theme.dart';

// Importamos colors.dart directamente
import '../../../core/theme/colors.dart';

class EmergencyWarningBanner extends StatelessWidget {
  const EmergencyWarningBanner({super.key});
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: AppColors.error.withOpacity(0.2),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          children: [
            Icon(Icons.warning_amber_rounded, color: AppColors.error, size: 20),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                'No soy un profesional médico/experto. Verifica esta información con un especialista.',
                style: TextStyle(
                  color: AppColors.error,
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
                softWrap: true,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
