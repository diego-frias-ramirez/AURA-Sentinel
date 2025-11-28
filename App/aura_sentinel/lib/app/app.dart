import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../core/theme/app_theme.dart';
import 'routes.dart';

class AuraSentinelApp extends StatelessWidget {
  const AuraSentinelApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      // ===========================
      //  CONFIGURACIÓN GENERAL
      // ===========================
      title: 'AURA Sentinel',
      debugShowCheckedModeBanner: false,

      // ===========================
      //  TEMA DE LA APP
      // ===========================
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.light,

      // ===========================
      //  INTERNACIONALIZACIÓN
      // ===========================
      locale: const Locale('es', 'MX'),
      fallbackLocale: const Locale('en', 'US'),
      translations: AppTranslations(),

      // ===========================
      //  NAVEGACIÓN
      // ===========================
      initialRoute: AppRoutes.splash,
      getPages: AppRoutes.routes,

      // ===========================
      //  CONFIGURACIÓN ADICIONAL
      // ===========================
      defaultTransition: Transition.cupertino,
      transitionDuration: const Duration(milliseconds: 300),

      // Builder para acceder al contexto global
      builder: (context, child) {
        return MediaQuery(
          data: MediaQuery.of(
            context,
          ).copyWith(textScaler: const TextScaler.linear(1.0)),
          child: child!,
        );
      },
    );
  }
}

// ===========================
//  TRADUCCIONES
// ===========================
class AppTranslations extends Translations {
  @override
  Map<String, Map<String, String>> get keys => {
    'es_MX': {
      'app_name': 'AURA Sentinel',
      'welcome': 'Bienvenido',
      'emergency': 'Emergencia',
      'help': 'Ayuda',
      'cancel': 'Cancelar',
      'accept': 'Aceptar',
      'save': 'Guardar',
      'continue': 'Continuar',
      'back': 'Regresar',
    },
    'en_US': {
      'app_name': 'AURA Sentinel',
      'welcome': 'Welcome',
      'emergency': 'Emergency',
      'help': 'Help',
      'cancel': 'Cancel',
      'accept': 'Accept',
      'save': 'Save',
      'continue': 'Continue',
      'back': 'Back',
    },
  };
}
