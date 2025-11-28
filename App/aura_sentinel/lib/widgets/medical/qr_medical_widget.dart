// qr_medical_widget.dart
import 'package:flutter/material.dart';
import 'package:qr_flutter/qr_flutter.dart';
import '../../core/theme/colors.dart';
import '../../core/theme/text_styles.dart';

class QRMedicalWidget extends StatelessWidget {
  final String medicalData;
  final double size;

  const QRMedicalWidget({
    super.key,
    required this.medicalData,
    this.size = 200,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
        border: Border.all(color: AppColors.primary.withOpacity(0.3), width: 2),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Código QR
          QrImageView(
            data: medicalData,
            version: QrVersions.auto,
            size: size,
            backgroundColor: Colors.white,
            foregroundColor: Colors.black,
          ),
          const SizedBox(height: 16),

          // Información del QR
          Text(
            'Código QR Médico',
            style: AppTextStyles.headlineSmall.copyWith(
              color: AppColors.primary,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Escanea para ver información médica de emergencia',
            style: AppTextStyles.bodySmall,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 12),

          // Advertencia
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: AppColors.warning.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              children: [
                Icon(Icons.security, color: AppColors.warning, size: 16),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'Información confidencial - Solo para profesionales de salud',
                    style: AppTextStyles.labelSmall.copyWith(
                      color: AppColors.warning,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
