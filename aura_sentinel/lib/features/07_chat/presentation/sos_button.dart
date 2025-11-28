// lib/features/07_chat/presentation/widgets/sos_button.dart
import 'package:flutter/material.dart';
// ignore: unused_import
import 'package:aura_sentinel/core/theme/app_theme.dart';

// Opcional: Si solo necesitas AppColors, puedes usar esta línea directamente
// y eliminar la línea de arriba con el ignore.
import '../../../core/theme/colors.dart';

class SOSButton extends StatelessWidget {
  const SOSButton({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 32.0),
      child: GestureDetector(
        onTap: () {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text('Emergencia activada')));
        },
        child: Container(
          width: 200,
          height: 200,
          decoration: BoxDecoration(
            // ✅ Sin `const`
            color: AppColors.error,
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: AppColors.error.withOpacity(0.3),
                blurRadius: 10,
                spreadRadius: 2,
              ),
            ],
          ),
          child: Center(
            child: Text(
              'SOS',
              style: TextStyle(
                // ✅ Sin `const`
                color: Colors.black,
                fontSize: 48,
                fontWeight: FontWeight.bold,
                letterSpacing: 2,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
