# AURA Sentinel

**Lema:** "Siempre contigo, cuando más lo necesitas."

---

## 🔥 Proyecto

AURA Sentinel es un asistente virtual inteligente de emergencias, diseñado para salvar vidas con respuesta inmediata, apoyo conversacional y gestión de crisis, funcionando de manera híbrida pero priorizando la disponibilidad offline.

---

## 📱 Funcionalidades principales

### 🚨 Modo Emergencia
- Activación: Botón de pánico, comando de voz ("AURA, emergencia"), gesto (agitar teléfono)
- Acciones: Clasificación IA automática, llamada 911, alerta a contactos, guía de primeros auxilios, técnicas de calma

### 🩺 Ficha Médica Inteligente
- Perfil médico offline (SQLite)
- QR médico compartible
- Recordatorios de medicamentos/citas
- Modo ICE en lockscreen

### 🗺️ Mapas y Refugios Offline
- Mapas precargados de Durango
- Directorio de hospitales, refugios, rutas de evacuación
- 100% funcional sin internet

### 💬 Chat de Emergencia
- IA conversacional (apoyo emocional, técnicas de calma)
- Conexión con líneas de ayuda reales

### 📚 Centro Educativo
- Guías de primeros auxilios
- Simulacros interactivos
- Preparación para desastres

---

## 🤖 Arquitectura IA

- **IA Offline:** Modelo local para clasificación de emergencias y recomendaciones rápidas.
- **IA Chat:** Integración con OpenAI API para conversación avanzada y apoyo emocional.

---

## 🔧 Tecnologías principales

- **Flutter:** App base multiplataforma
- **AppWrite:** Backend y autenticación
- **GetID:** Acceso biométrico
- **TensorFlow Lite:** IA offline (clasificador)
- **OpenAI API:** Chat y emociones
- **SQLite:** Datos médicos offline/encriptados

---

## 📂 Estructura Principal

AURA Sentinel/
- AURAAI_Lab/ # Laboratorio de los modelos IA
- App/Ai dart/ # Implementaciones y prototipos en Dart/Flutter
- Material Fotos/ # Recursos gráficos y multimedia
- Web/ # Sitio web informativo/promo
- copiloto/ # softwere comiloto como complemneto a la app movil
- README.md # Este archivo
- AURA presentacion.pdf
-Documento de Proyecciones IA.pdf
- ENFOQUE INTEGRAL.pdf
- Investigación de la AI.pdf
- Investigación del tema.pdf
- investigacion Backend.pdf


## ⚡ Flujo Principal

1. Onboarding: splash → welcome → login/register → biometric → verification
2. Home principal: botón pánico + navegación
3. Módulos: ficha médica, contactos, mapas, chat, educación, perfil
4. Emergencia: activación → alerta → confirmación/cancelación

---

## 🚨 Seguridad y Offline

- Todos los datos médicos y de emergencia se guardan y procesan localmente (SQLite + encriptación).
- Mapas y rutas precargados para funcionar sin conexión.
- 60%+ de las funcionalidades funcionan sin internet.

---

## 🎯 Objetivo final

Desarrollar una app móvil profesional que salva vidas,
- Detecta emergencias y guía al usuario (chat, voz, mapa),
- Responde y asiste en crisis incluso sin internet,
- Protege la privacidad y la seguridad de los datos médicos.

---

