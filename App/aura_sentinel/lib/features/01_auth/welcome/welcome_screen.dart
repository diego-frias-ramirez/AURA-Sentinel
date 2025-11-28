import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../../app/routes.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          // <-- ARREGLA EL OVERFLOW
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const SizedBox(height: 20),

                Text(
                  'Bienvenido !',
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 16),

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.shield, color: Colors.blue, size: 28),
                    const SizedBox(width: 8),
                    Text(
                      'AURA Sentinel',
                      style: TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.w600,
                        color: Colors.blue,
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 24),

                Text(
                  'Tu asistente de emergencias IA',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w500,
                    color: Colors.grey[800],
                  ),
                ),

                const SizedBox(height: 16),

                Text(
                  '"Siempre contigo, cuando más lo necesitas."',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 16,
                    fontStyle: FontStyle.italic,
                    color: Colors.grey[600],
                  ),
                ),

                const SizedBox(height: 32),

                ClipRRect(
                  borderRadius: BorderRadius.circular(20),
                  child: Image.asset(
                    'assets/img/card_bienvendia.png',
                    width: 300,
                    height: 400,
                    fit: BoxFit
                        .cover, // Ajusta la imagen para llenar el contenedor
                  ),
                ),

                const SizedBox(height: 32),

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _dot(active: true),
                    const SizedBox(width: 8),
                    _dot(),
                    const SizedBox(width: 8),
                    _dot(),
                  ],
                ),

                const SizedBox(height: 40),

                ElevatedButton(
                  onPressed: () {
                    Get.offNamed(AppRoutes.login);
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 40,
                      vertical: 16,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
                    ),
                  ),
                  child: const Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text('Empezar'),
                      SizedBox(width: 8),
                      Icon(Icons.arrow_forward),
                    ],
                  ),
                ),

                const SizedBox(height: 24),

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Ya tienes cuenta? ',
                      style: TextStyle(color: Colors.grey[700]),
                    ),
                    GestureDetector(
                      onTap: () {
                        Get.offNamed(AppRoutes.login);
                      },
                      child: Text(
                        'Iniciar sesión',
                        style: TextStyle(
                          color: Colors.blue,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 20),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _dot({bool active = false}) {
    return Container(
      width: 12,
      height: 12,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: active ? Colors.green : Colors.grey[300],
      ),
    );
  }
}
