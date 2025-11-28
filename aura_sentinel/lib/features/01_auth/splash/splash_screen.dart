// lib/features/01_auth/splash/splash_screen.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart'; // Para la navegación automática
import 'package:aura_sentinel/app/routes.dart'; // Para navegar a la siguiente pantalla

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Navega automáticamente a la siguiente pantalla después de 3 segundos
    Future.delayed(const Duration(seconds: 3), () {
      Get.toNamed(AppRoutes.welcome); // Navega a la pantalla de bienvenida
    });

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
              child: Container(
                // Contenedor interno con el fondo degradado
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      Color.fromRGBO(0, 123, 255, 1), // Azul
                      Color.fromRGBO(0, 200, 180, 1), // Turquesa
                    ],
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                  ),
                ),
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      // Logo "AURA Sentinel" con ícono de escudo
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            Icons.shield_outlined, // Ícono de escudo
                            color: Colors.white,
                            size: 24,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            'AURA Sentinel',
                            style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 20,
                            ),
                          ),
                        ],
                      ),
                      // Ícono de flecha hacia la derecha en la esquina inferior derecha (opcional)
                      Positioned.fill(
                        child: Align(
                          alignment: Alignment.bottomRight,
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Icon(
                              Icons.arrow_forward_ios,
                              color: Colors.white.withOpacity(0.5),
                              size: 16,
                            ),
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
      ),
    );
  }
}
