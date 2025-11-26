# Sistema Copiloto 911 con IA

Sistema inteligente para operadores 911 que recibe alertas de AURA con información completa del usuario antes de contestar la llamada.

## Características

- Recepción automática de alertas desde AURA
- Ficha médica completa (alergias, tipo de sangre, medicamentos)
- Ubicación GPS en tiempo real
- Clasificación automática de emergencias por IA
- Sugerencias de protocolos y recursos
- Interfaz premium con CustomTkinter

## Instalación
```bash
pip install -r requirements.txt
```

## Uso
```bash
python main.py
```

## Estructura del Proyecto

- `core/` - Modelos y lógica de negocio
- `ui/` - Interfaz gráfica
- `services/` - Servicios externos (AURA, GPS, etc.)
- `utils/` - Utilidades y helpers
- `data/` - Base de datos y logs
- `tests/` - Pruebas unitarias

## Configuración

Edita `config.py` para configurar:
- URL de la API de AURA
- Configuración de la base de datos
- Parámetros de la IA

## Licencia

Propietario - Todos los derechos reservados
