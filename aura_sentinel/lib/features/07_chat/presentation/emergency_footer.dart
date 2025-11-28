// lib/features/07_chat/presentation/widgets/emergency_footer.dart
import 'package:flutter/material.dart';

// Quitamos la importación de app_theme.dart
// import 'package:aura_sentinel/core/theme/app_theme.dart';
// Quitamos la importación de colors.dart ya que no la usamos más aquí
// import '../../../core/theme/colors.dart';
class EmergencyFooter extends StatelessWidget {
  const EmergencyFooter({super.key});
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.info_outline, size: 16, color: Colors.grey.shade600),
          const SizedBox(width: 4),
          Text(
            'Emergencia: ',
            style: TextStyle(color: Colors.grey.shade600, fontSize: 14),
          ),
          GestureDetector(
            onTap: () {
              ScaffoldMessenger.of(
                context,
              ).showSnackBar(SnackBar(content: Text('Llamando al 911...')));
            },
            child: Text(
              'Llamar al 911',
              style: TextStyle(
                color: Color.fromRGBO(0, 123, 255, 1),
                fontSize: 14,
                fontWeight: FontWeight.bold,
                decoration: TextDecoration.underline,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
