// emergency_utils.dart
import 'package:url_launcher/url_launcher.dart';

class EmergencyUtils {
  // Llamar a números de emergencia
  static Future<void> callEmergencyNumber(String phoneNumber) async {
    final url = 'tel:$phoneNumber';
    if (await canLaunchUrl(Uri.parse(url))) {
      await launchUrl(Uri.parse(url));
    } else {
      throw 'No se puede realizar la llamada';
    }
  }

  // Enviar SMS de emergencia
  static Future<void> sendEmergencySMS(
    String phoneNumber,
    String message,
  ) async {
    final url = 'sms:$phoneNumber?body=${Uri.encodeComponent(message)}';
    if (await canLaunchUrl(Uri.parse(url))) {
      await launchUrl(Uri.parse(url));
    } else {
      throw 'No se puede enviar el SMS';
    }
  }

  // Formatear duración de emergencia
  static String formatEmergencyDuration(Duration duration) {
    if (duration.inHours > 0) {
      return '${duration.inHours}h ${duration.inMinutes.remainder(60)}m';
    } else if (duration.inMinutes > 0) {
      return '${duration.inMinutes}m ${duration.inSeconds.remainder(60)}s';
    } else {
      return '${duration.inSeconds}s';
    }
  }

  // Validar número de teléfono de emergencia
  static bool isValidEmergencyNumber(String number) {
    final cleaned = number.replaceAll(RegExp(r'[^\d+]'), '');
    return cleaned.length >= 10;
  }

  // Generar mensaje de emergencia para contactos
  static String generateEmergencyMessage({
    required String userName,
    required String location,
    required String? additionalInfo,
  }) {
    String message =
        '''
🚨 ALERTA DE EMERGENCIA 🚨

$userName ha activado una alerta de emergencia.

📍 Ubicación: $location
🕐 Hora: ${DateTime.now().toString()}

La ubicación se está compartiendo en tiempo real.
''';

    if (additionalInfo != null && additionalInfo.isNotEmpty) {
      message += '\nInformación adicional: $additionalInfo';
    }

    message += '\n\nPor favor, contacta a las autoridades si es necesario.';

    return message;
  }

  // Calcular nivel de urgencia basado en síntomas
  static int calculateUrgencyLevel(List<String> symptoms) {
    const highUrgencySymptoms = [
      'dolor pecho',
      'dificultad respirar',
      'sangrado',
      'inconsciente',
    ];
    const mediumUrgencySymptoms = [
      'fiebre alta',
      'vómitos',
      'mareo',
      'dolor intenso',
    ];

    int score = 0;

    for (var symptom in symptoms) {
      final lowerSymptom = symptom.toLowerCase();
      if (highUrgencySymptoms.any((s) => lowerSymptom.contains(s))) {
        score += 3;
      } else if (mediumUrgencySymptoms.any((s) => lowerSymptom.contains(s))) {
        score += 2;
      } else {
        score += 1;
      }
    }

    if (score >= 6) return 3; // Alta urgencia
    if (score >= 3) return 2; // Media urgencia
    return 1; // Baja urgencia
  }
}
