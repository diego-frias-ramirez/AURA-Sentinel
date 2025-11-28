// emergency_button.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../app/routes.dart';
import '../../core/theme/colors.dart';
import '../../core/theme/text_styles.dart';

class EmergencyButton extends StatelessWidget {
  final double size;
  final bool withLabel;

  const EmergencyButton({super.key, this.size = 200, this.withLabel = true});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _activateEmergency,
      child: Column(
        children: [
          Container(
            width: size,
            height: size,
            decoration: BoxDecoration(
              color: AppColors.emergency,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: AppColors.emergency.withOpacity(0.4),
                  blurRadius: 20,
                  spreadRadius: 5,
                ),
                BoxShadow(
                  color: AppColors.emergency.withOpacity(0.3),
                  blurRadius: 40,
                  spreadRadius: 10,
                ),
              ],
            ),
            child: Stack(
              children: [
                // Efecto de pulso
                Positioned.fill(
                  child: Container(
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: Colors.white.withOpacity(0.3),
                        width: 4,
                      ),
                    ),
                  ),
                ),
                // Texto SOS
                Center(
                  child: Text(
                    'SOS',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: size * 0.2,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2,
                    ),
                  ),
                ),
                // Icono de emergencia
                Positioned(
                  bottom: 20,
                  right: 20,
                  child: Icon(
                    Icons.warning,
                    color: Colors.white,
                    size: size * 0.15,
                  ),
                ),
              ],
            ),
          ),
          if (withLabel) ...[
            const SizedBox(height: 16),
            Text(
              'BOTÓN DE PÁNICO',
              style: AppTextStyles.emergencyText.copyWith(
                color: AppColors.emergency,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              'Presiona para activar ayuda inmediata',
              style: AppTextStyles.bodySmall.copyWith(
                color: AppColors.textSecondary,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ],
      ),
    );
  }

  void _activateEmergency() {
    // Mostrar confirmación antes de activar
    showDialog(
      context: Get.context!,
      builder: (context) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.warning, color: AppColors.emergency),
            SizedBox(width: 8),
            Text('Activar Emergencia'),
          ],
        ),
        content: const Text(
          '¿Estás seguro de que quieres activar la alerta de emergencia? '
          'Se notificará a tus contactos y servicios de emergencia.',
        ),
        actions: [
          TextButton(
            onPressed: () => Get.back(),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () {
              Get.back();
              Get.toNamed(AppRoutes.emergencyAlert);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.emergency,
            ),
            child: const Text('Activar Emergencia'),
          ),
        ],
      ),
    );
  }
}
