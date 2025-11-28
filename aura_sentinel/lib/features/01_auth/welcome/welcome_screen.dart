// lib/features/01_auth/welcome/welcome_screen.dart
import 'package:aura_sentinel/app/routes.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

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
                // Añadimos padding general para margen interno
                padding: const EdgeInsets.symmetric(
                  horizontal: 24.0,
                  vertical: 8.0,
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Título "Bienvenido!"
                    Text(
                      'Bienvenido!',
                      style: Theme.of(context).textTheme.headlineMedium
                          ?.copyWith(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 16),
                    // Logo "AURA Sentinel"
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.shield_outlined,
                          color: Color.fromRGBO(0, 123, 255, 1), // Azul
                          size: 24,
                        ),
                        const SizedBox(width: 8),
                        Text(
                          'AURA Sentinel',
                          style: TextStyle(
                            color: Color.fromRGBO(0, 123, 255, 1), // Azul
                            fontWeight: FontWeight.bold,
                            fontSize: 20,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    // Subtítulo "Tu asistente de emergencias IA"
                    Text(
                      'Tu asistente de emergencias IA',
                      style: Theme.of(context).textTheme.headlineSmall
                          ?.copyWith(fontWeight: FontWeight.w500),
                    ),
                    const SizedBox(height: 16),
                    // Cita
                    Text(
                      '"Siempre contigo, cuando más lo necesitas."',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        fontStyle: FontStyle.italic,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 32),
                    // Imagen del teléfono
                    Image.asset(
                      'assets/images/welcome_phone.png', // Asegúrate de tener esta imagen
                      width: 300,
                      height: 400,
                      fit: BoxFit.contain,
                    ),
                    const SizedBox(height: 32),
                    // Botón "Empezar"
                    ElevatedButton(
                      onPressed: () {
                        // Aquí puedes navegar a la siguiente pantalla
                        // Por ejemplo, a la pantalla de login
                        Get.toNamed(AppRoutes.login);
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color.fromRGBO(0, 123, 255, 1), // Azul
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(
                          horizontal: 32,
                          vertical: 16,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            'Empezar',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(width: 8),
                          Icon(Icons.arrow_forward, size: 20),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),
                    // Enlace "iniciar sesión"
                    TextButton(
                      onPressed: () {
                        Get.toNamed(AppRoutes.login);
                      },
                      child: Text(
                        'Ya tienes cuenta? iniciar sesión',
                        style: TextStyle(
                          color: Color.fromRGBO(0, 123, 255, 1), // Azul
                          decoration: TextDecoration.underline,
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
