import 'dart:io';

void main() {
  final structure = [
    'lib/main.dart',
    'lib/app/app.dart',
    'lib/core/theme/app_theme.dart',
    'lib/core/theme/colors.dart',
    'lib/core/theme/text_styles.dart',
    'lib/app/routes.dart',
    'lib/data/models/user_model.dart',
    'lib/features/01_auth/splash/splash_screen.dart',
    'lib/features/01_auth/welcome/welcome_screen.dart',
    'lib/features/01_auth/login/login_screen.dart',
    'lib/features/01_auth/register/register_screen.dart',
    'lib/features/02_main/main_screen.dart',
    'lib/services/appwrite_service.dart',
    'lib/services/getid_service.dart',
    'lib/features/01_auth/forgot_password/forgot_password_screen.dart',
    'lib/features/01_auth/biometric/biometric_screen.dart',
    'lib/features/01_auth/verification/verification_screen.dart',
    'lib/features/01_auth/verification/verification_complete_screen.dart',
    'lib/widgets/common/bottom_nav_bar.dart',
    'lib/features/02_main/home/home_screen.dart',
    'lib/data/models/medical_model.dart',
    'lib/data/models/contact_model.dart',
    'lib/data/models/emergency_model.dart',
    'lib/features/04_medical/medical_profile/medical_profile_screen.dart',
    'lib/features/04_medical/medical_form/medical_form_screen.dart',
    'lib/features/04_medical/qr_medical/qr_medical_screen.dart',
    'lib/features/05_contacts/emergency_contacts/emergency_contacts_screen.dart',
    'lib/features/05_contacts/contacts_management/contacts_management_screen.dart',
    'lib/features/06_maps/security_map/security_map_screen.dart',
    'lib/features/06_maps/shelters/shelters_screen.dart',
    'lib/features/07_chat/emergency_chat/emergency_chat_screen.dart',
    'lib/features/08_education/education_center/education_center_screen.dart',
    'lib/features/09_profile/user_profile/user_profile_screen.dart',
    'lib/features/09_profile/personal_info/personal_info_screen.dart',
    'lib/features/09_profile/settings/settings_screen.dart',
    'lib/features/09_profile/security_privacy/security_privacy_screen.dart',
    'lib/features/09_profile/notifications/notifications_screen.dart',
    'lib/widgets/common/emergency_button.dart',
    'lib/services/ai_offline_service.dart',
    'lib/services/ai_chat_service.dart',
    'lib/services/location_service.dart',
    'lib/services/emergency_service.dart',
    'lib/services/notification_service.dart',
    'lib/services/permission_service.dart',
    'lib/features/03_emergency/panic_button/panic_button_screen.dart',
    'lib/features/03_emergency/alert_active/emergency_alert_screen.dart',
    'lib/features/03_emergency/cancel_alert/cancel_alert_screen.dart',
    'lib/data/repositories/auth_repository.dart',
    'lib/data/repositories/medical_repository.dart',
    'lib/data/repositories/emergency_repository.dart',
    'lib/core/utils/emergency_utils.dart',
    'lib/widgets/medical/qr_medical_widget.dart',
  ];

  for (final filePath in structure) {
    final file = File(filePath);
    file.createSync(recursive: true);
    file.writeAsStringSync('// ${filePath.split('/').last}');
    print('Creado: $filePath');
  }
}
