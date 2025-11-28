class AIChatService {
  static final AIChatService _instance = AIChatService._internal();
  factory AIChatService() => _instance;
  AIChatService._internal();

  // Simular respuesta de IA para emergencias
  Future<String> getAIResponse(String userMessage) async {
    // Simular procesamiento de IA
    await Future.delayed(const Duration(seconds: 1));

    final message = userMessage.toLowerCase();

    if (message.contains('respiración') || message.contains('ansiedad')) {
      return '''**Técnica de Respiración 4-7-8:**
1. Inhala por la nariz contando hasta 4
2. Mantén la respiración contando hasta 7  
3. Exhala por la boca contando hasta 8
4. Repite 3-4 veces

Esto ayuda a calmar el sistema nervioso.''';
    } else if (message.contains('hablar') || message.contains('solo')) {
      return '''Entiendo que necesitas apoyo. No estás solo/a.

**Recursos inmediatos:**
• Línea de crisis: 911
• Chat de apoyo 24/7: [Enlace disponible]
• Respira profundamente, estoy aquí para ayudarte.

¿Puedes contarme más sobre cómo te sientes?''';
    } else if (message.contains('emergencia') || message.contains('pánico')) {
      return '''🚨 **PROTOCOLO DE EMERGENCIA ACTIVADO**

1. **Mantén la calma** - Respira profundamente
2. **Busca un lugar seguro** - Aléjate del peligro
3. **Activa el botón de pánico** si no lo has hecho
4. **Tu ubicación se está compartiendo** con contactos de emergencia
5. **La ayuda está en camino**

¿Necesitas que active la alerta de emergencia?''';
    } else {
      return '''Entiendo que estás pasando por un momento difícil. 

Como asistente de IA, puedo ofrecerte:
• Técnicas de relajación
• Protocolos de seguridad  
• Información de primeros auxilios psicológicos
• Guía para contactar ayuda profesional

**Recuerda:** Para emergencias médicas reales, contacta al 911 inmediatamente.

¿En qué más puedo ayudarte?''';
    }
  }

  // Obtener respuestas rápidas predefinidas
  List<String> getQuickReplies() {
    return [
      'Necesito hablar ahora',
      'Técnicas de respiración',
      'Cómo activar emergencia',
      'Recursos de apoyo',
      'Primeros auxilios psicológicos',
    ];
  }

  // Verificar si el mensaje indica emergencia
  bool isEmergencyMessage(String message) {
    final emergencyKeywords = [
      'ayuda',
      'emergencia',
      'peligro',
      'socorro',
      'auxilio',
      'herido',
      'accidente',
      'ataque',
      'riesgo',
      'urgencia',
    ];

    final lowerMessage = message.toLowerCase();
    return emergencyKeywords.any((keyword) => lowerMessage.contains(keyword));
  }

  // Obtener nivel de urgencia del mensaje
  int getUrgencyLevel(String message) {
    if (isEmergencyMessage(message)) return 3; // Alta urgencia

    final mediumUrgencyKeywords = ['miedo', 'ansiedad', 'solo', 'triste'];
    final lowerMessage = message.toLowerCase();

    if (mediumUrgencyKeywords.any(
      (keyword) => lowerMessage.contains(keyword),
    )) {
      return 2; // Media urgencia
    }

    return 1; // Baja urgencia
  }
}
