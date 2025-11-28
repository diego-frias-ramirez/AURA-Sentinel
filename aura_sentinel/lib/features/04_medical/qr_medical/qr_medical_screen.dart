// lib/features/04_medical/medical_qr_screen.dart
import 'package:flutter/material.dart';
// Para la navegación
import 'package:qr_flutter/qr_flutter.dart'; // Para generar el código QR

class MedicalQRScreen extends StatelessWidget {
  const MedicalQRScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Center(
          child: SizedBox(
            width: 395, // Ancho fijo de 395px
            height: 852, // Alto fijo de 852px
            child: Container(
              decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.blue,
                  width: 2,
                ), // 🟦 Borde azul para referencia
              ),
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Título "Código QR Médico" (centrado)
                    Center(
                      child: Text(
                        'Código QR Médico',
                        style: Theme.of(context).textTheme.headlineSmall
                            ?.copyWith(fontWeight: FontWeight.bold),
                      ),
                    ),
                    const SizedBox(height: 32),
                    // Código QR real (centrado)
                    Center(
                      child: QrImageView(
                        data:
                            'https://imgv2-1-f.scribdassets.com/img/document/466176309/original/a74e7d46c9/1?v=1', // URL que quieres almacenar
                        version: QrVersions.auto,
                        size: 200,
                        backgroundColor: Colors.white,
                        foregroundColor: Colors.black,
                      ),
                    ),
                    const SizedBox(height: 32),
                    // Sección "Información Médica"
                    Expanded(
                      child: SingleChildScrollView(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Información Médica',
                              style: Theme.of(context).textTheme.headlineSmall
                                  ?.copyWith(fontWeight: FontWeight.bold),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Este código QR contiene información médica esencial que puede ser escaneada por profesionales de la salud en caso de emergencia. Asegúrate de mantenerlo actualizado.',
                              style: Theme.of(context).textTheme.bodyLarge,
                            ),
                            const SizedBox(height: 32),
                            // Sección "Advertencia"
                            Text(
                              'Advertencia',
                              style: Theme.of(context).textTheme.headlineSmall
                                  ?.copyWith(fontWeight: FontWeight.bold),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'No compartas este código QR con personas no autorizadas. La información médica es confidencial.',
                              style: Theme.of(context).textTheme.bodyLarge,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
