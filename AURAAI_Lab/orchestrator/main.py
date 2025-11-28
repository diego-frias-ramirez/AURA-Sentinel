"""
AuraOrchestrator - Motor IA avanzado para Aura Sentinel
Usa modelos joblib (scikit-learn) para prototipado en PC.
Totalmente offline. Prototipo Python (para portar a Flutter/Dart).
"""

import os
import json
import numpy as np
import joblib
from typing import Optional, Dict, Any

# Paths relativos desde orchestrator/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

# Usar modelos .joblib - NOMBRES CORREGIDOS
MODELS = {
    "agentcore": os.path.join(PARENT_DIR, "agentcore/models/agentcore_production.joblib"),
    "agentcore_vectorizer": os.path.join(PARENT_DIR, "agentcore/models/agentcore_vectorizer.joblib"),
    "agentcore_encoder": os.path.join(PARENT_DIR, "agentcore/models/agentcore_encoder.joblib"),
    
    "chatlite": os.path.join(PARENT_DIR, "chatlite/models/chatlite_classifier.joblib"),
    "chatlite_vectorizer": os.path.join(PARENT_DIR, "chatlite/models/chatlite_vectorizer.joblib"),
    "chatlite_encoder": os.path.join(PARENT_DIR, "chatlite/models/chatlite_encoder.joblib"),
    
    "resourcehub": os.path.join(PARENT_DIR, "resourcehub/models/resourcehub_classifier.joblib"),
    "resourcehub_encoder": os.path.join(PARENT_DIR, "resourcehub/models/resourcehub_encoder.joblib"),
}

ASSETS = {
    "chatlite_intents": os.path.join(PARENT_DIR, "chatlite/models/intent_responses.json"),
    "geoguard_db": os.path.join(PARENT_DIR, "geoguard/models/facilities_mobile.json"),
    "geoguard_config": os.path.join(PARENT_DIR, "geoguard/models/routing_config.json"),
    "resourcehub_config": os.path.join(PARENT_DIR, "resourcehub/models/medical_config.json"),
    "resourcehub_templates": os.path.join(PARENT_DIR, "resourcehub/models/action_templates.json")
}

class AuraOrchestrator:
    def __init__(self, config_path: Optional[str] = None):
        """Inicializa el orquestador con modelos sklearn y configuración"""
        if config_path is None:
            config_path = os.path.join(BASE_DIR, "config.json")
        
        self.config = self.load_config(config_path)
        
        print("[AuraOrchestrator] Cargando modelos sklearn...")
        
        # Cargar modelos con manejo de errores
        try:
            self.agentcore_model = joblib.load(MODELS["agentcore"])
            self.agentcore_vectorizer = joblib.load(MODELS["agentcore_vectorizer"])
            self.agentcore_encoder = joblib.load(MODELS["agentcore_encoder"])
            print("  ✓ AgentCore cargado")
        except Exception as e:
            print(f"  ✗ Error cargando AgentCore: {e}")
            raise
        
        try:
            self.chatlite_model = joblib.load(MODELS["chatlite"])
            self.chatlite_vectorizer = joblib.load(MODELS["chatlite_vectorizer"])
            self.chatlite_encoder = joblib.load(MODELS["chatlite_encoder"])
            print("  ✓ ChatLite cargado")
        except Exception as e:
            print(f"  ✗ Error cargando ChatLite: {e}")
            raise
        
        try:
            self.resourcehub_model = joblib.load(MODELS["resourcehub"])
            self.resourcehub_encoder = joblib.load(MODELS["resourcehub_encoder"])
            print("  ✓ ResourceHub cargado")
        except Exception as e:
            print(f"  ✗ Error cargando ResourceHub: {e}")
            raise
        
        print("[AuraOrchestrator] Cargando configuraciones...")
        self.chatlite_intents = self._load_json(ASSETS["chatlite_intents"])
        self.geoguard_db = self._load_json(ASSETS["geoguard_db"])
        self.geoguard_config = self._load_json(ASSETS["geoguard_config"])
        self.resourcehub_config = self._load_json(ASSETS["resourcehub_config"])
        self.resourcehub_templates = self._load_json(ASSETS["resourcehub_templates"])
        
        print("[AuraOrchestrator] ✓ Iniciado correctamente. Modelos y assets cargados.")

    def load_config(self, config_path: str) -> dict:
        """Carga configuración desde JSON"""
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        print(f"[WARN] Config no encontrado: {config_path}. Usando config por defecto.")
        return {}

    def _load_json(self, path: str):
        """Carga archivo JSON"""
        if not os.path.exists(path):
            print(f"[WARN] Asset no encontrado: {path}")
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def run_agentcore(self, text: str) -> Dict[str, Any]:
        """Ejecuta modelo AgentCore (clasificación de emergencias)"""
        X = self.agentcore_vectorizer.transform([text])
        pred = self.agentcore_model.predict(X)
        pred_proba = self.agentcore_model.predict_proba(X)
        
        tipo_emergencia = self.agentcore_encoder.inverse_transform(pred)[0]
        confianza = float(np.max(pred_proba))
        
        return {
            "tipo_emergencia": tipo_emergencia,
            "confianza": confianza
        }

    def run_chatlite(self, text: str) -> Dict[str, Any]:
        """Ejecuta modelo ChatLite (clasificación de intents)"""
        X = self.chatlite_vectorizer.transform([text])
        pred = self.chatlite_model.predict(X)
        pred_proba = self.chatlite_model.predict_proba(X)
        
        intent = self.chatlite_encoder.inverse_transform(pred)[0]
        confianza = float(np.max(pred_proba))
        
        response_candidates = self.chatlite_intents.get(intent, {}).get("responses", [])
        suggested_response = response_candidates[0] if response_candidates else None
        
        return {
            "intent": intent,
            "confianza": confianza,
            "suggested_response": suggested_response
        }

    def run_resourcehub(self, profile: Dict) -> Dict:
        """Ejecuta modelo ResourceHub (perfil médico)"""
        blood_types = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
        
        # Construir vector de entrada (debe coincidir con el orden de train.py)
        X = np.array([[
            profile['edad'],
            int(profile['tiene_alergias']),
            int(profile['condicion_cronica']),
            int(profile['toma_medicamentos']),
            *[1 if profile['tipo_sangre'] == bt else 0 for bt in blood_types]
        ]])
        
        pred = self.resourcehub_model.predict(X)
        pred_proba = self.resourcehub_model.predict_proba(X)
        
        action = self.resourcehub_encoder.inverse_transform(pred)[0]
        confianza = float(np.max(pred_proba))
        
        templates = self.resourcehub_templates.get(action, {})
        recommendations = templates.get("recommendations", [])
        
        return {
            "action": action,
            "confianza": confianza,
            "recommendations": recommendations
        }

    def find_nearest_facility(self, lat: float, lon: float, tipo: Optional[str] = None):
        """Encuentra instalación más cercana usando GeoGuard"""
        facilities = self.geoguard_db.get("all_facilities", [])
        
        if not facilities:
            facilities = self.geoguard_db  # Por si el JSON es lista directa
        
        dists = []
        for f in facilities:
            if tipo and f.get('tipo') != tipo:
                continue
            
            f_lat = f.get('lat') or f.get('latitud', 0)
            f_lon = f.get('lon') or f.get('longitud', 0)
            
            # Distancia euclidiana simple (para prototipo)
            d = np.sqrt((f_lat - lat) ** 2 + (f_lon - lon) ** 2)
            dists.append((d, f))
        
        dists.sort(key=lambda x: x[0])
        return dists[0][1] if dists else None

    def handle_input(
        self,
        texto: Optional[str] = None,
        ubicacion: Optional[Dict] = None,
        perfil: Optional[Dict] = None,
        panic: bool = False
    ) -> Dict:
        """
        Motor central de IA. Procesa entrada y decide acción.
        
        Args:
            texto: Mensaje del usuario
            ubicacion: {'lat': float, 'lon': float}
            perfil: Perfil médico del usuario
            panic: Botón de pánico presionado
            
        Returns:
            Dict con respuesta y acción a ejecutar
        """
        
        # MODO PÁNICO
        if panic:
            return {
                "respuesta_texto": "¡Modo pánico activado! Llamando a emergencia 911.",
                "accion_app": "marcar_911",
                "usar_tts": True,
                "respuesta_voz_texto": "¡Tranquilo, ya estoy llamando a los servicios de emergencia!",
                "metadata": {
                    "panic_mode": True,
                    "intent": "panic_button",
                    "tipo_emergencia": "panic",
                    "priority": "critical"
                }
            }
        
        if not texto:
            return {
                "respuesta_texto": "No recibí ningún mensaje. ¿Puedes escribir de nuevo?",
                "accion_app": "none",
                "usar_tts": False,
                "metadata": {}
            }
        
        # Ejecutar modelos
        results = {}
        chat = self.run_chatlite(texto)
        results.update(chat)
        
        intent = chat.get("intent", "")
        confianza = chat.get("confianza", 0.0)
        
        # Lógica de decisión
        accion_app = "none"
        respuesta = chat.get("suggested_response", "¿Puedes darme más detalles?")
        tipo_emergencia = None
        poi = None
        
        # Detectar si es emergencia
        intent_mapping = self.config.get("intent_mapping", {})
        intent_config = intent_mapping.get(intent, {})
        
        trigger_agentcore = intent_config.get("trigger_agentcore", False)
        
        if trigger_agentcore or confianza > 0.7:
            agentcore = self.run_agentcore(texto)
            tipo_emergencia = agentcore["tipo_emergencia"]
            results.update(agentcore)
            
            # Mapear tipo de emergencia a acción
            emergency_mapping = self.config.get("emergency_mapping", {})
            emergency_config = emergency_mapping.get(tipo_emergencia, {})
            
            accion_app = emergency_config.get("action", "abrir_mapa_hospital")
            respuesta = emergency_config.get("response_template", respuesta)
            
            # Buscar instalación cercana si hay ubicación
            if ubicacion and emergency_config.get("facility_type"):
                facility_type = emergency_config["facility_type"]
                poi = self.find_nearest_facility(
                    ubicacion['lat'], 
                    ubicacion['lon'], 
                    tipo=facility_type
                )
        else:
            # No es emergencia, usar respuesta del intent
            accion_app = intent_config.get("action", "none")
        
        # Integrar perfil médico si existe
        if perfil:
            rhub = self.run_resourcehub(perfil)
            results.update(rhub)
        
        # Construir respuesta final
        output = {
            "respuesta_texto": respuesta,
            "accion_app": accion_app,
            "usar_tts": True,
            "respuesta_voz_texto": respuesta,
            "metadata": {
                "intent": intent,
                "tipo_emergencia": tipo_emergencia,
                "poi": poi,
                "confianza_intent": confianza,
                "recomendaciones": results.get("recommendations", []),
            }
        }
        
        return output


# ============================================================================
# EJEMPLO DE USO (para testing local)
# ============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("AURA SENTINEL - ORCHESTRATOR TEST")
    print("=" * 80)
    
    try:
        orquestor = AuraOrchestrator()
        
        print("\n" + "=" * 80)
        print("[TEST 1] Emergencia médica")
        print("=" * 80)
        resultado = orquestor.handle_input(
            texto="Ayuda, me caí y me duele mucho la pierna, no puedo moverme",
            ubicacion={'lat': 24.027, 'lon': -104.653},
            perfil={
                "edad": 72,
                "tiene_alergias": True,
                "condicion_cronica": True,
                "toma_medicamentos": True,
                "tipo_sangre": "O+"
            },
            panic=False
        )
        
        print("\nRESULTADO:")
        from pprint import pprint
        pprint(resultado)
        
        print("\n" + "=" * 80)
        print("[TEST 2] Botón de pánico")
        print("=" * 80)
        resultado_panic = orquestor.handle_input(panic=True)
        pprint(resultado_panic)
        
        print("\n" + "=" * 80)
        print("[TEST 3] Solicitud de calma")
        print("=" * 80)
        resultado_calma = orquestor.handle_input(
            texto="Estoy muy nervioso y asustado, ayúdame a calmarme"
        )
        pprint(resultado_calma)
        
        print("\n" + "=" * 80)
        print("[TEST 4] Mensaje simple")
        print("=" * 80)
        resultado_simple = orquestor.handle_input(
            texto="Hola, ¿cómo estás?"
        )
        pprint(resultado_simple)
        
        print("\n" + "=" * 80)
        print("✓ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
