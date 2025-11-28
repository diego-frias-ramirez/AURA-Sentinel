// lib/features/07_chat/emergency_chat_screen.dart
import 'package:flutter/material.dart';
import 'package:aura_sentinel/features/07_chat/presentation/emergency_footer.dart';
import 'package:aura_sentinel/features/07_chat/presentation/emergency_header.dart';
import 'package:aura_sentinel/features/07_chat/presentation/emergency_warning_banner.dart';
import 'package:aura_sentinel/features/07_chat/presentation/message_input.dart';
import 'package:aura_sentinel/features/07_chat/presentation/quick_replies.dart';
import 'package:aura_sentinel/features/07_chat/presentation/sos_button.dart';
import 'package:aura_sentinel/core/theme/text_styles.dart';

class EmergencyChatScreen extends StatelessWidget {
  const EmergencyChatScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Center(
          child: Container(
            width: double.infinity,
            constraints: BoxConstraints(
              maxWidth: 400,
            ), // Ancho máximo de 400px (tamaño típico de móvil)
            decoration: BoxDecoration(
              border: Border.all(
                color: Colors.blue,
                width: 2,
              ), // 🟦 Borde azul para referencia
            ),
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(
                horizontal: 16.0,
                vertical: 8.0,
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment
                    .center, // Centra verticalmente todo el contenido
                crossAxisAlignment: CrossAxisAlignment
                    .center, // Centra horizontalmente todos los elementos
                children: [
                  // 1. Header
                  const EmergencyHeader(),
                  // 2. Warning Banner
                  const SizedBox(
                    height: 16,
                  ), // Espacio entre Header y Warning Banner
                  const EmergencyWarningBanner(),
                  // 3. Title
                  const SizedBox(
                    height: 24,
                  ), // Espacio entre Warning Banner y Título
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 24.0),
                    child: Text(
                      '¿Que emergencia tienes?',
                      style: AppTextStyles.headlineMedium.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center, // Centra el título
                    ),
                  ),
                  // 4. SOS Button
                  const SizedBox(
                    height: 32,
                  ), // Espacio entre Título y Botón SOS
                  Center(
                    // Centra el botón SOS horizontalmente
                    child: const SOSButton(),
                  ),
                  // 5. Quick Replies
                  const SizedBox(
                    height: 24,
                  ), // Espacio entre Botón SOS y Respuestas Rápidas
                  const QuickReplies(), // Ya está diseñado para mostrarlos en fila
                  // 6. Message Input
                  const SizedBox(
                    height: 24,
                  ), // Espacio entre Respuestas Rápidas y Campo de Mensaje
                  const MessageInput(),
                  // 7. Footer
                  const SizedBox(
                    height: 24,
                  ), // Espacio entre Campo de Mensaje y Pie de Página
                  const EmergencyFooter(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
