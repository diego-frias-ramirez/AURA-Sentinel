// routes.dart
import 'package:get/get.dart';
import '../features/01_auth/splash/splash_screen.dart';
import '../features/01_auth/welcome/welcome_screen.dart';
import '../features/01_auth/login/login_screen.dart';
import '../features/01_auth/register/register_screen.dart';
import '../features/01_auth/forgot_password/forgot_password_screen.dart';
import '../features/01_auth/biometric/biometric_screen.dart';
import '../features/01_auth/verification/verification_screen.dart';
import '../features/02_main/main_screen.dart';

class AppRoutes {
  // ===========================
  //  NOMBRES DE RUTAS
  // ===========================

  // Auth
  static const String splash = '/splash';
  static const String welcome = '/welcome';
  static const String login = '/login';
  static const String register = '/register';
  static const String forgotPassword = '/forgot-password';
  static const String biometric = '/biometric';
  static const String verification = '/verification';

  // Main
  static const String main = '/main';
  static const String home = '/home';

  // Emergency
  static const String panicButton = '/panic-button';
  static const String emergencyAlert = '/emergency-alert';
  static const String cancelAlert = '/cancel-alert';

  // Medical
  static const String medicalProfile = '/medical-profile';
  static const String medicalForm = '/medical-form';
  static const String qrMedical = '/qr-medical';

  // Contacts
  static const String emergencyContacts = '/emergency-contacts';
  static const String contactsManagement = '/contacts-management';

  // Maps
  static const String securityMap = '/security-map';
  static const String shelters = '/shelters';

  // Chat
  static const String emergencyChat = '/emergency-chat';

  // Education
  static const String educationCenter = '/education-center';

  // Profile
  static const String userProfile = '/user-profile';
  static const String personalInfo = '/personal-info';
  static const String settings = '/settings';
  static const String securityPrivacy = '/security-privacy';
  static const String notifications = '/notifications';

  // ===========================
  // 🗺️ DEFINICIÓN DE RUTAS
  // ===========================
  static final routes = [
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
    GetPage(
      name: register,
      page: () => const RegisterScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: forgotPassword,
      page: () => const ForgotPasswordScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: biometric,
      page: () => const BiometricScreen(),
      transition: Transition.fadeIn,
    ),
    GetPage(
      name: verification,
      page: () => const VerificationScreen(),
      transition: Transition.rightToLeft,
    ),

    // ===========================
    // 🏠 MAIN ROUTES
    // ===========================
    GetPage(
      name: main,
      page: () => const MainScreen(),
      transition: Transition.fadeIn,
    ),

    // Agregar más rutas cuando creemos las pantallas...
  ];
}
