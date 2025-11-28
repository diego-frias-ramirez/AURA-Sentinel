// qr_medical_screen.dart
import 'package:flutter/material.dart';
import 'package:qr_flutter/qr_flutter.dart';

class QRMedicalScreen extends StatelessWidget {
  const QRMedicalScreen({super.key});

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
                    const Center(
                      child: Text(
                        'Código QR Médico',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    const SizedBox(height: 32),
                    // Código QR real (centrado)
                    Center(
                      child: QrImageView(
                        data: 'https://aura-sentinel.com/medical/juan-perez',
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
                            const Text(
                              'Información Médica',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 8),
                            const Text(
                              'Este código QR contiene información médica esencial que puede ser escaneada por profesionales de la salud en caso de emergencia. Asegúrate de mantenerlo actualizado.',
                              style: TextStyle(fontSize: 16),
                            ),
                            const SizedBox(height: 32),
                            // Sección "Advertencia"
                            const Text(
                              'Advertencia',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 8),
                            const Text(
                              'No compartas este código QR con personas no autorizadas. La información médica es confidencial.',
                              style: TextStyle(fontSize: 16),
                            ),
                            const SizedBox(height: 32),
                            // Botones de acción
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                              children: [
                                ElevatedButton(
                                  onPressed: () {
                                    // Guardar QR
                                  },
                                  child: const Text('Guardar'),
                                ),
                                ElevatedButton(
                                  onPressed: () {
                                    // Compartir QR
                                  },
                                  child: const Text('Compartir'),
                                ),
                                ElevatedButton(
                                  onPressed: () {
                                    // Regenerar QR
                                  },
                                  child: const Text('Regenerar'),
                                ),
                              ],
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
