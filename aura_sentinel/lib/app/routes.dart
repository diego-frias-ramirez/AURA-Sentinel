// lib/app/routes.dart

import 'package:aura_sentinel/features/04_medical/qr_medical/qr_medical_screen.dart';
import 'package:aura_sentinel/features/06_maps/shelters/shelters_screen.dart';
import 'package:aura_sentinel/features/07_chat/emergency_chat/emergency_chat_screen.dart';
import 'package:get/get.dart';

// Importa las pantallas esenciales
import '../features/01_auth/splash/splash_screen.dart';
import '../features/01_auth/welcome/welcome_screen.dart';
import '../features/01_auth/login/login_screen.dart';

class AppRoutes {
  // ===========================
  //  NOMBRES DE RUTAS
  // ===========================

  // Auth
  static const String splash = '/splash';
  static const String welcome = '/welcome';
  static const String login = '/login';
  static const String shelters = '/shelters';

  // Medical
  static const String medicalQR =
      '/medical-qr'; // ✅ Ruta para la pantalla de QR médico

  // Chat
  static const String emergencyChat =
      '/emergency-chat'; // Const para la ruta de emergencia

  // ===========================
  // 🗺️ DEFINICIÓN DE RUTAS
  // ===========================
  static final List<GetPage> routes = [
    // ===========================
    // 🔐 AUTH ROUTES
    // ===========================
    GetPage(
      name: splash,
      page: () => const SplashScreen(),
      transition: Transition.fadeIn,
    ),
    GetPage(
      name: welcome,
      page: () => const WelcomeScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: login,
      page: () => const LoginScreen(),
      transition: Transition.rightToLeft,
    ),

    // ===========================
    // 🏥 MEDICAL ROUTES
    // ===========================
    GetPage(
      name: medicalQR, // ✅ Usamos la constante definida arriba
      page: () => const MedicalQRScreen(), // ✅ Widget que creamos
      transition:
          Transition.rightToLeft, // Puedes elegir la transición que prefieras
    ),

    // ===========================
    // 💬 CHAT ROUTES
    // ===========================
    GetPage(
      name: emergencyChat, // Usamos la constante definida arriba
      page: () => const EmergencyChatScreen(), // Widget que creamos
      transition:
          Transition.rightToLeft, // Puedes elegir la transición que prefieras
    ),
    GetPage(
      name: shelters,
      page: () => const SheltersScreen(),
      transition: Transition.rightToLeft,
    ),
  ];
}
