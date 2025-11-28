// lib/features/07_chat/presentation/widgets/emergency_header.dart
import 'package:flutter/material.dart';

// Quitamos la importación de app_theme.dart
// import 'package:aura_sentinel/core/theme/app_theme.dart';
// Quitamos la importación de colors.dart ya que no la usamos más aquí
// import '../../../core/theme/colors.dart';
class EmergencyHeader extends StatelessWidget {
  const EmergencyHeader({super.key});
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(24), // Bordes redondeados
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.2), // Sombra suave
              blurRadius: 4,
              spreadRadius: 2,
            ),
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0),
          child: Row(
            children: [
              // 1. Botón de retroceso
              IconButton(
                onPressed: () => Navigator.pop(context),
                icon: const Icon(Icons.arrow_back, color: Colors.black),
              ),
              const SizedBox(width: 16),
              // 2. Badge "AURA Sentinel"
              Expanded(
                child: Center(
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: Color.fromRGBO(0, 123, 255, 1),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Container(
                          width: 8,
                          height: 8,
                          decoration: BoxDecoration(
                            color: Colors.white,
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 8),
                        Text(
                          'AURA Sentinel',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              // 3. Avatar (con silueta de persona)
              CircleAvatar(
                backgroundColor: Colors.white, // Fondo blanco para el avatar
                radius: 20,
                child: Icon(
                  Icons.person, // ✅ Ícono genérico de persona
                  color: Color.fromRGBO(0, 123, 255, 1),
                  size: 30,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
