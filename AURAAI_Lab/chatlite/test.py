"""
AuraChatLite - Intent Classification Testing & Inference
Production-grade inference system for conversational intent recognition
with confidence scoring and emotional context analysis.

Author: AuraAI_Lab
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import joblib
import os
import json
import logging
import argparse
from datetime import datetime
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

# Paths
MODEL_PATH = 'models/chatlite_classifier.joblib'
VECTORIZER_PATH = 'models/chatlite_vectorizer.joblib'
ENCODER_PATH = 'models/chatlite_encoder.joblib'
METRICS_PATH = 'models/training_metrics.json'
INFERENCE_LOG = 'models/inference.log'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(INFERENCE_LOG),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ChatIntentEngine:
    """Production inference engine for chat intent classification"""
    
    # Intent descriptions for better UX
    INTENT_DESCRIPTIONS = {
        'solicitud_ayuda': 'Usuario pide ayuda urgente',
        'expresion_miedo': 'Usuario expresa miedo o pánico',
        'solicitud_calma': 'Usuario pide técnicas de calma',
        'informacion_emergencia': 'Usuario describe la emergencia',
        'estado_emocional': 'Usuario describe síntomas emocionales',
        'confirmacion': 'Respuesta afirmativa',
        'negacion': 'Respuesta negativa',
        'agradecimiento': 'Usuario agradece la ayuda',
        'ubicacion': 'Usuario da/pide ubicación',
        'instrucciones': 'Usuario pide instrucciones'
    }
    
    # Suggested responses by intent
    SUGGESTED_RESPONSES = {
        'solicitud_ayuda': [
            "Entiendo, estoy aquí para ayudarte. ¿Qué tipo de emergencia es?",
            "Ya estoy contigo. Cuéntame qué está pasando.",
            "No te preocupes, vamos a resolver esto juntos. ¿Qué necesitas?"
        ],
        'expresion_miedo': [
            "Entiendo que tengas miedo. Vamos a respirar juntos. ¿Puedes inhalar por 4 segundos?",
            "Es normal sentir miedo. Estoy aquí contigo. Vamos a calmarnos poco a poco.",
            "Comprendo tu miedo. Respira conmigo: inhala... sostén... exhala."
        ],
        'solicitud_calma': [
            "Claro, te voy a guiar. Inhala por la nariz contando 4... aguanta 7... exhala por la boca contando 8.",
            "Hagamos respiración 4-7-8. ¿Listo? Inhala profundo...",
            "Perfecto. Vamos a usar la técnica de respiración profunda. Sígueme."
        ],
        'informacion_emergencia': [
            "Entendido. ¿Hay heridos? ¿Están conscientes?",
            "Recibido. ¿Es seguro donde estás ahora?",
            "Gracias por la información. ¿Cuántas personas están involucradas?"
        ],
        'estado_emocional': [
            "Te escucho. ¿Quieres que hagamos ejercicios de respiración?",
            "Comprendo cómo te sientes. Vamos a trabajar en esto juntos.",
            "Es válido lo que sientes. ¿Necesitas que te guíe para calmarte?"
        ],
        'confirmacion': [
            "Perfecto, continuemos.",
            "Muy bien. Siguiente paso:",
            "Excelente. Ahora:"
        ],
        'negacion': [
            "Entiendo. ¿Puedes intentarlo de otra forma?",
            "No hay problema. Vamos con otra opción.",
            "Está bien. Te explico de otra manera."
        ],
        'agradecimiento': [
            "Con gusto, para eso estoy aquí.",
            "No tienes que agradecer. ¿Necesitas algo más?",
            "Me da gusto ayudarte. ¿Cómo te sientes ahora?"
        ],
        'ubicacion': [
            "Gracias por tu ubicación. El hospital más cercano es:",
            "Recibido. Te voy a indicar hacia dónde ir.",
            "Perfecto. Basado en tu ubicación, te recomiendo:"
        ],
        'instrucciones': [
            "Con gusto te guío. Paso 1:",
            "Te explico paso a paso. Primero:",
            "Claro, hagámoslo juntos. Comencemos con:"
        ]
    }
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.metrics = None
        self.is_loaded = False
        
    def load_artifacts(self):
        """Load all required model artifacts"""
        logger.info("Loading model artifacts...")
        
        try:
            required_files = [MODEL_PATH, VECTORIZER_PATH, ENCODER_PATH]
            missing = [f for f in required_files if not os.path.exists(f)]
            
            if missing:
                raise FileNotFoundError(
                    f"Missing required files: {missing}. Run train.py first."
                )
            
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            self.label_encoder = joblib.load(ENCODER_PATH)
            
            if os.path.exists(METRICS_PATH):
                with open(METRICS_PATH, 'r') as f:
                    self.metrics = json.load(f)
                    logger.info("Model metrics loaded - Test Accuracy: %.4f",
                              self.metrics.get('test_accuracy', 0))
            
            self.is_loaded = True
            logger.info("All artifacts loaded successfully")
            logger.info("Available intents: %s", self.label_encoder.classes_.tolist())
            
        except Exception as e:
            logger.error("Failed to load artifacts: %s", str(e))
            raise
    
    def predict_intent(self, text: str, return_suggestions: bool = True) -> Dict:
        """
        Predict intent for user message
        
        Args:
            text: User message
            return_suggestions: Whether to return suggested responses
            
        Returns:
            Dictionary with prediction results
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_artifacts() first.")
        
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")
        
        # Vectorize
        X = self.vectorizer.transform([text])
        
        # Predict
        prediction_encoded = self.model.predict(X)[0]
        prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
        
        result = {
            'user_message': text,
            'predicted_intent': prediction,
            'intent_description': self.INTENT_DESCRIPTIONS.get(prediction, ''),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add probabilities
        if hasattr(self.model, 'predict_proba'):
            probas = self.model.predict_proba(X)[0]
            
            prob_dist = {
                intent: float(prob)
                for intent, prob in zip(self.label_encoder.classes_, probas)
            }
            
            result['confidence'] = float(probas[prediction_encoded])
            result['all_probabilities'] = prob_dist
            
            # Top 3
            sorted_probs = sorted(prob_dist.items(), key=lambda x: x[1], reverse=True)
            result['top_3_intents'] = [
                {
                    'intent': intent,
                    'probability': prob,
                    'description': self.INTENT_DESCRIPTIONS.get(intent, '')
                }
                for intent, prob in sorted_probs[:3]
            ]
        
        # Add suggested responses
        if return_suggestions:
            suggestions = self.SUGGESTED_RESPONSES.get(prediction, [])
            if suggestions:
                result['suggested_response'] = random.choice(suggestions)
                result['all_suggestions'] = suggestions
        
        return result
    
    def predict_conversation(self, messages: List[str]) -> List[Dict]:
        """
        Predict intents for a conversation sequence
        
        Args:
            messages: List of user messages in order
            
        Returns:
            List of prediction dictionaries with conversation context
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_artifacts() first.")
        
        logger.info("Analyzing conversation with %d messages", len(messages))
        
        results = []
        intent_history = []
        
        for i, message in enumerate(messages):
            result = self.predict_intent(message, return_suggestions=True)
            result['message_index'] = i
            result['intent_history'] = intent_history.copy()
            
            # Detect emotional progression
            if i > 0:
                prev_intent = results[-1]['predicted_intent']
                curr_intent = result['predicted_intent']
                
                # Check if user is calming down
                if prev_intent == 'expresion_miedo' and curr_intent in ['confirmacion', 'agradecimiento']:
                    result['emotional_state'] = 'mejorando'
                elif prev_intent == 'solicitud_calma' and curr_intent == 'confirmacion':
                    result['emotional_state'] = 'respondiendo_bien'
                elif curr_intent == 'expresion_miedo':
                    result['emotional_state'] = 'necesita_apoyo'
                else:
                    result['emotional_state'] = 'estable'
            
            intent_history.append(result['predicted_intent'])
            results.append(result)
        
        return results
    
    def evaluate_dataset(self, csv_path: str) -> Dict:
        """Evaluate model on labeled dataset"""
        logger.info("Evaluating on dataset: %s", csv_path)
        
        df = pd.read_csv(csv_path)
        
        if 'texto_usuario' not in df.columns or 'intent' not in df.columns:
            raise ValueError("CSV must contain 'texto_usuario' and 'intent' columns")
        
        X = self.vectorizer.transform(df['texto_usuario'])
        y_true_encoded = self.label_encoder.transform(df['intent'])
        y_pred_encoded = self.model.predict(X)
        
        from sklearn.metrics import (
            accuracy_score, precision_recall_fscore_support,
            classification_report
        )
        
        accuracy = accuracy_score(y_true_encoded, y_pred_encoded)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true_encoded, y_pred_encoded, average='weighted', zero_division=0
        )
        
        results = {
            'dataset': csv_path,
            'n_samples': len(df),
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info("Evaluation Results:")
        logger.info("  Accuracy:  %.4f", accuracy)
        logger.info("  Precision: %.4f", precision)
        logger.info("  Recall:    %.4f", recall)
        logger.info("  F1-Score:  %.4f", f1)
        
        report = classification_report(
            y_true_encoded, y_pred_encoded,
            target_names=self.label_encoder.classes_,
            zero_division=0
        )
        logger.info("\nDetailed Classification Report:\n%s", report)
        
        return results
    
    def interactive_chat(self):
        """Interactive chat mode for testing"""
        logger.info("Starting interactive chat mode. Type 'exit' to quit.")
        
        print("\n" + "=" * 80)
        print("AURA SENTINEL - CHATLITE - INTERACTIVE CHAT MODE")
        print("=" * 80)
        print("\nSimula una conversación de emergencia.")
        print("El sistema detectará tu intención y sugerirá respuestas.\n")
        print("Intents disponibles:")
        for intent, desc in self.INTENT_DESCRIPTIONS.items():
            print(f"  - {intent}: {desc}")
        print("\nEscribe tus mensajes (escribe 'exit' para salir):\n")
        
        conversation_history = []
        
        while True:
            try:
                text = input("\n[Usuario]: ").strip()
                
                if text.lower() == 'exit':
                    print("\nFinalizando chat. ¡Hasta pronto!")
                    break
                
                if not text:
                    continue
                
                result = self.predict_intent(text, return_suggestions=True)
                conversation_history.append(result)
                
                print("\n" + "-" * 80)
                print(f"Intent Detectado: {result['predicted_intent']}")
                print(f"Descripción: {result['intent_description']}")
                print(f"Confianza: {result['confidence']:.2%}")
                print(f"\n[AURA Sugerencia]: {result.get('suggested_response', 'Sin sugerencia')}")
                print("-" * 80)
                
            except KeyboardInterrupt:
                print("\n\nInterrumpido por usuario. Saliendo.")
                break
            except Exception as e:
                logger.error("Error: %s", str(e))
                print(f"\nError: {str(e)}")
        
        # Show conversation summary
        if conversation_history:
            print("\n" + "=" * 80)
            print("RESUMEN DE CONVERSACIÓN")
            print("=" * 80)
            intent_counts = {}
            for msg in conversation_history:
                intent = msg['predicted_intent']
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            print(f"Total mensajes: {len(conversation_history)}")
            print("\nIntents detectados:")
            for intent, count in sorted(intent_counts.items()):
                print(f"  - {intent}: {count} veces")


def run_demo_chat():
    """Run demo conversation"""
    demo_conversation = [
        "Ayuda por favor",
        "Hubo un accidente en mi casa",
        "Tengo mucho miedo",
        "Ayúdame a calmarme",
        "Sí por favor",
        "Estoy en la colonia Centro",
        "Gracias",
        "Qué hago ahora"
    ]
    
    engine = ChatIntentEngine()
    engine.load_artifacts()
    
    logger.info("Running demo conversation with %d messages", len(demo_conversation))
    print("\n" + "=" * 80)
    print("DEMO CONVERSATION")
    print("=" * 80)
    
    results = engine.predict_conversation(demo_conversation)
    
    for result in results:
        print(f"\n[Mensaje {result['message_index'] + 1}]")
        print(f"Usuario: {result['user_message']}")
        print(f"Intent: {result['predicted_intent']} ({result['confidence']:.2%})")
        print(f"Sugerencia: {result.get('suggested_response', 'N/A')}")
        if 'emotional_state' in result:
            print(f"Estado emocional: {result['emotional_state']}")


def main():
    """Main execution with CLI"""
    parser = argparse.ArgumentParser(
        description='AuraChatLite Intent Classifier - Testing & Inference'
    )
    parser.add_argument(
        '--mode',
        choices=['demo', 'interactive', 'evaluate', 'single'],
        default='demo',
        help='Testing mode'
    )
    parser.add_argument('--text', type=str, help='Single text to classify')
    parser.add_argument('--csv', type=str, help='CSV for evaluation')
    
    args = parser.parse_args()
    
    try:
        engine = ChatIntentEngine()
        engine.load_artifacts()
        
        if args.mode == 'demo':
            run_demo_chat()
            
        elif args.mode == 'interactive':
            engine.interactive_chat()
            
        elif args.mode == 'single':
            if not args.text:
                raise ValueError("--text argument required for single mode")
            
            result = engine.predict_intent(args.text, return_suggestions=True)
            print("\nPrediction Result:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.mode == 'evaluate':
            if not args.csv:
                raise ValueError("--csv argument required for evaluate mode")
            
            results = engine.evaluate_dataset(args.csv)
            print("\nEvaluation Results:")
            print(json.dumps(results, indent=2, ensure_ascii=False))
        
    except Exception as e:
        logger.error("Execution failed: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    import random
    main()
