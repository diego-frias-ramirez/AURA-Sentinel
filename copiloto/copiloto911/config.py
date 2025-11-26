# config.py
# Configuración global del sistema Copiloto 911

import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
ASSETS_DIR = BASE_DIR / 'assets'
LOGS_DIR = DATA_DIR / 'logs'

# Configuración de la base de datos
DATABASE_URL = f"sqlite:///{DATA_DIR / 'emergencias.db'}"

# Configuración de la interfaz
WINDOW_TITLE = "Sistema Copiloto 911 con IA"
WINDOW_SIZE = "1600x900"
THEME = "dark"
COLOR_THEME = "blue"

# Configuración de AURA
AURA_API_URL = os.getenv('AURA_API_URL', 'http://localhost:5000/api')
AURA_API_KEY = os.getenv('AURA_API_KEY', '')

# Configuración de servicios
GPS_UPDATE_INTERVAL = 5  # segundos
NOTIFICATION_SOUND = True

# Configuración de logs
LOG_LEVEL = "INFO"
LOG_FILE = LOGS_DIR / 'app.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Configuración de IA
IA_MODEL = "local"  # local o api
IA_CONFIDENCE_THRESHOLD = 0.85
