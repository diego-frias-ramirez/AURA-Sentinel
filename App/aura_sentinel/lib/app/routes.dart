import 'package:get/get.dart';

// Auth
import '../features/01_auth/splash/splash_screen.dart';
import '../features/01_auth/welcome/welcome_screen.dart';
import '../features/01_auth/login/login_screen.dart';
import '../features/01_auth/register/register_screen.dart';
import '../features/01_auth/verification/verification_screen.dart';

// Main
import '../features/02_main/home/home_screen.dart';
import '../features/02_main/main_screen.dart';

// Medical
import '../features/04_medical/medical_form/medical_form_screen.dart';
import '../features/04_medical/medical_profile/medical_profile_screen.dart';
import '../features/04_medical/qr_medical/qr_medical_screen.dart';

// Contacts
import '../features/05_contacts/emergency_contacts/emergency_contacts_screen.dart';
import '../features/05_contacts/contacts_management/contacts_management_screen.dart';

// Emergency
import '../features/03_emergency/alert_active/emergency_alert_screen.dart';

// Chat
import '../features/07_chat/emergency_chat/emergency_chat_screen.dart';

// Maps
import '../features/06_maps/shelters/shelters_screen.dart';

class AppRoutes {
  // ===========================
  //  NOMBRES DE RUTAS
  // ===========================

  // Auth
  static const String splash = '/splash';
  static const String welcome = '/welcome';
  static const String login = '/login';
  static const String register = '/register';
  static const String verification = '/verification';

  // Main
  static const String home = '/home';
  static const String main = '/main';

  // Medical
  static const String medicalForm = '/medical-form';
  static const String medicalProfile = '/medical-profile';
  static const String medicalQR = '/medical-qr';

  // Contacts
  static const String emergencyContacts = '/emergency-contacts';
  static const String contactsManagement = '/contacts-management';

  // Emergency
  static const String emergencyAlert = '/emergency-alert';

  // Chat
  static const String emergencyChat = '/emergency-chat';

  // Maps
  static const String shelters = '/shelters';

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
    GetPage(
      name: register,
      page: () => const RegisterScreen(),
      transition: Transition.rightToLeft,
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
      name: home,
      page: () => const HomeScreen(),
      transition: Transition.fadeIn,
    ),
    GetPage(
      name: main,
      page: () => const MainScreen(),
      transition: Transition.fadeIn,
    ),

    // ===========================
    // 🏥 MEDICAL ROUTES
    // ===========================
    GetPage(
      name: medicalForm,
      page: () => const MedicalFormScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: medicalProfile,
      page: () => const MedicalProfileScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: medicalQR,
      page: () => const QRMedicalScreen(),
      transition: Transition.rightToLeft,
    ),

    // ===========================
    // 📞 CONTACTS ROUTES
    // ===========================
    GetPage(
      name: emergencyContacts,
      page: () => const EmergencyContactsScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: contactsManagement,
      page: () => const ContactsManagementScreen(),
      transition: Transition.rightToLeft,
    ),

    // ===========================
    // 🚨 EMERGENCY ROUTES
    // ===========================
    GetPage(
      name: emergencyAlert,
      page: () => const EmergencyAlertScreen(),
      transition: Transition.downToUp,
    ),

    // ===========================
    // 💬 CHAT ROUTES
    // ===========================
    GetPage(
      name: emergencyChat,
      page: () => const EmergencyChatScreen(),
      transition: Transition.rightToLeft,
    ),

    // ===========================
    // 🗺️ MAPS ROUTES
    // ===========================
    GetPage(
      name: shelters,
      page: () => const SheltersScreen(),
      transition: Transition.rightToLeft,
    ),
  ];
}
