"""
AuraResourceHub - Medical Profile Testing & Inference
Production-grade inference system for personalized health management,
medication reminders, and medical profile recommendations.

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
MODEL_PATH = 'models/resourcehub_classifier.joblib'
ENCODER_PATH = 'models/resourcehub_encoder.joblib'
FEATURE_NAMES_PATH = 'models/feature_names.json'
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


class ResourceHubEngine:
    """Production inference engine for medical profile management"""
    
    # Blood type mapping
    BLOOD_TYPES = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
    
    # Action descriptions
    ACTION_DESCRIPTIONS = {
        'recordatorio_medicamento': 'Recordar tomar medicamento',
        'revisar_alergias': 'Revisar información de alergias',
        'actualizar_ficha': 'Actualizar ficha médica',
        'contactar_medico': 'Contactar a médico de cabecera',
        'verificar_condicion': 'Verificar condición crónica',
        'sin_accion': 'No se requiere acción'
    }
    
    # Detailed recommendations
    ACTION_RECOMMENDATIONS = {
        'recordatorio_medicamento': [
            "Revisa tu lista de medicamentos y horarios",
            "Configura alarmas para tus medicamentos",
            "Verifica que tengas suficiente stock"
        ],
        'revisar_alergias': [
            "Actualiza tu lista de alergias conocidas",
            "Lleva siempre tu información de alergias contigo",
            "Informa a personal médico sobre tus alergias"
        ],
        'actualizar_ficha': [
            "Actualiza tu información de contacto de emergencia",
            "Agrega cualquier nuevo diagnóstico o condición",
            "Revisa y actualiza medicamentos actuales"
        ],
        'contactar_medico': [
            "Agenda cita de seguimiento con tu médico",
            "Prepara lista de síntomas o preocupaciones",
            "Lleva tu ficha médica actualizada"
        ],
        'verificar_condicion': [
            "Monitorea tus síntomas regularmente",
            "Mantén registro de cambios en tu condición",
            "Sigue tu plan de tratamiento prescrito"
        ],
        'sin_accion': [
            "Tu perfil está actualizado",
            "Continúa con tu rutina normal",
            "Revisa periódicamente tu información"
        ]
    }
    
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.feature_names = None
        self.metrics = None
        self.is_loaded = False
        
    def load_artifacts(self):
        """Load all required model artifacts"""
        logger.info("Loading model artifacts...")
        
        try:
            required_files = [MODEL_PATH, ENCODER_PATH, FEATURE_NAMES_PATH]
            missing = [f for f in required_files if not os.path.exists(f)]
            
            if missing:
                raise FileNotFoundError(
                    f"Missing required files: {missing}. Run train.py first."
                )
            
            self.model = joblib.load(MODEL_PATH)
            self.label_encoder = joblib.load(ENCODER_PATH)
            
            with open(FEATURE_NAMES_PATH, 'r') as f:
                self.feature_names = json.load(f)
            
            if os.path.exists(METRICS_PATH):
                with open(METRICS_PATH, 'r') as f:
                    self.metrics = json.load(f)
                    logger.info("Model metrics loaded - Test Accuracy: %.4f",
                              self.metrics.get('test_accuracy', 0))
            
            self.is_loaded = True
            logger.info("All artifacts loaded successfully")
            logger.info("Available actions: %s", self.label_encoder.classes_.tolist())
            
        except Exception as e:
            logger.error("Failed to load artifacts: %s", str(e))
            raise
    
    def prepare_profile_features(self, edad: int, tiene_alergias: bool,
                                 condicion_cronica: bool, toma_medicamentos: bool,
                                 tipo_sangre: str) -> np.ndarray:
        """Prepare features from medical profile"""
        
        # Validate inputs
        if not 0 <= edad <= 120:
            raise ValueError("Edad debe estar entre 0 y 120")
        if tipo_sangre not in self.BLOOD_TYPES:
            raise ValueError(f"Tipo de sangre debe ser uno de: {self.BLOOD_TYPES}")
        
        # Numeric feature
        features = [edad]
        
        # Binary features
        features.extend([
            int(tiene_alergias),
            int(condicion_cronica),
            int(toma_medicamentos)
        ])
        
        # Blood type one-hot encoding
        blood_encoding = [1 if tipo_sangre == bt else 0 for bt in self.BLOOD_TYPES]
        features.extend(blood_encoding)
        
        return np.array([features])
    
    def predict_action(self, edad: int, tiene_alergias: bool,
                      condicion_cronica: bool, toma_medicamentos: bool,
                      tipo_sangre: str) -> Dict:
        """
        Predict recommended action for medical profile
        
        Args:
            edad: Age in years
            tiene_alergias: Has known allergies
            condicion_cronica: Has chronic condition
            toma_medicamentos: Takes regular medications
            tipo_sangre: Blood type
            
        Returns:
            Dictionary with prediction and recommendations
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_artifacts() first.")
        
        # Prepare features
        X = self.prepare_profile_features(
            edad, tiene_alergias, condicion_cronica, 
            toma_medicamentos, tipo_sangre
        )
        
        # Predict
        prediction_encoded = self.model.predict(X)[0]
        prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
        
        result = {
            'profile': {
                'edad': edad,
                'tiene_alergias': tiene_alergias,
                'condicion_cronica': condicion_cronica,
                'toma_medicamentos': toma_medicamentos,
                'tipo_sangre': tipo_sangre
            },
            'accion_recomendada': prediction,
            'descripcion': self.ACTION_DESCRIPTIONS.get(prediction, ''),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add probabilities if available
        if hasattr(self.model, 'predict_proba'):
            probas = self.model.predict_proba(X)[0]
            
            prob_dist = {
                action: float(prob)
                for action, prob in zip(self.label_encoder.classes_, probas)
            }
            
            result['confidence'] = float(probas[prediction_encoded])
            result['all_probabilities'] = prob_dist
        
        # Add recommendations
        recommendations = self.ACTION_RECOMMENDATIONS.get(prediction, [])
        result['recomendaciones'] = recommendations
        
        return result
    
    def analyze_risk_factors(self, profile: Dict) -> Dict:
        """Analyze risk factors from profile"""
        risk_factors = []
        risk_level = 'bajo'
        
        edad = profile['edad']
        
        # Age risk
        if edad > 65:
            risk_factors.append('Edad avanzada (>65 años)')
            risk_level = 'medio'
        elif edad < 5:
            risk_factors.append('Edad pediátrica (<5 años)')
            risk_level = 'medio'
        
        # Medical conditions
        if profile['tiene_alergias']:
            risk_factors.append('Tiene alergias conocidas')
        
        if profile['condicion_cronica']:
            risk_factors.append('Condición crónica activa')
            if risk_level == 'bajo':
                risk_level = 'medio'
            else:
                risk_level = 'alto'
        
        if profile['toma_medicamentos']:
            risk_factors.append('Toma medicamentos regularmente')
        
        # Combined risk
        if len(risk_factors) >= 3:
            risk_level = 'alto'
        
        return {
            'nivel_riesgo': risk_level,
            'factores_riesgo': risk_factors,
            'total_factores': len(risk_factors)
        }
    
    def evaluate_dataset(self, csv_path: str) -> Dict:
        """Evaluate model on labeled dataset"""
        logger.info("Evaluating on dataset: %s", csv_path)
        
        df = pd.read_csv(csv_path)
        
        required_cols = ['edad', 'tiene_alergias', 'condicion_cronica',
                        'toma_medicamentos', 'tipo_sangre', 'accion_recomendada']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"CSV must contain columns: {required_cols}")
        
        # Prepare features
        X_list = []
        for _, row in df.iterrows():
            X = self.prepare_profile_features(
                row['edad'], row['tiene_alergias'], row['condicion_cronica'],
                row['toma_medicamentos'], row['tipo_sangre']
            )
            X_list.append(X[0])
        
        X = np.array(X_list)
        y_true_encoded = self.label_encoder.transform(df['accion_recomendada'])
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
        logger.info("\nDetailed Report:\n%s", report)
        
        return results
    
    def interactive_mode(self):
        """Interactive testing mode"""
        logger.info("Starting interactive mode. Type 'exit' to quit.")
        
        print("\n" + "=" * 80)
        print("AURA SENTINEL - RESOURCEHUB - INTERACTIVE MODE")
        print("=" * 80)
        print("\nAnaliza perfiles médicos y recomienda acciones.")
        print(f"\nTipos de sangre válidos: {', '.join(self.BLOOD_TYPES)}")
        print("\nIngresa información del perfil médico:\n")
        
        while True:
            try:
                print("\n" + "-" * 80)
                
                edad_input = input("Edad (0-120): ").strip()
                if edad_input.lower() == 'exit':
                    break
                edad = int(edad_input)
                
                alergias = input("¿Tiene alergias? (s/n): ").strip().lower() == 's'
                cronica = input("¿Condición crónica? (s/n): ").strip().lower() == 's'
                medicamentos = input("¿Toma medicamentos? (s/n): ").strip().lower() == 's'
                tipo_sangre = input(f"Tipo de sangre ({', '.join(self.BLOOD_TYPES)}): ").strip().upper()
                
                result = self.predict_action(edad, alergias, cronica, medicamentos, tipo_sangre)
                risk = self.analyze_risk_factors(result['profile'])
                
                print("\n" + "=" * 80)
                print("ANÁLISIS DE PERFIL")
                print("=" * 80)
                print(f"\nAcción recomendada: {result['accion_recomendada']}")
                print(f"Descripción: {result['descripcion']}")
                print(f"Confianza: {result.get('confidence', 0):.2%}")
                
                print(f"\nNivel de riesgo: {risk['nivel_riesgo'].upper()}")
                if risk['factores_riesgo']:
                    print("\nFactores de riesgo identificados:")
                    for factor in risk['factores_riesgo']:
                        print(f"  - {factor}")
                
                print("\nRecomendaciones:")
                for i, rec in enumerate(result['recomendaciones'], 1):
                    print(f"  {i}. {rec}")
                
                print("=" * 80)
                
            except KeyboardInterrupt:
                print("\n\nInterrumpido por usuario. Saliendo.")
                break
            except ValueError as e:
                print(f"\nError: {str(e)}")
            except Exception as e:
                logger.error("Error: %s", str(e))
                print(f"\nError: {str(e)}")


def run_demo_profiles():
    """Run demo with sample profiles"""
    demo_profiles = [
        {
            'nombre': 'Adulto Mayor con Medicamentos',
            'edad': 72,
            'tiene_alergias': True,
            'condicion_cronica': True,
            'toma_medicamentos': True,
            'tipo_sangre': 'O+'
        },
        {
            'nombre': 'Joven Saludable',
            'edad': 25,
            'tiene_alergias': False,
            'condicion_cronica': False,
            'toma_medicamentos': False,
            'tipo_sangre': 'A+'
        },
        {
            'nombre': 'Adulto con Alergias',
            'edad': 45,
            'tiene_alergias': True,
            'condicion_cronica': False,
            'toma_medicamentos': False,
            'tipo_sangre': 'B+'
        }
    ]
    
    engine = ResourceHubEngine()
    engine.load_artifacts()
    
    logger.info("Running demo with %d sample profiles", len(demo_profiles))
    print("\n" + "=" * 80)
    print("DEMO PROFILES - MEDICAL RECOMMENDATIONS")
    print("=" * 80)
    
    for profile in demo_profiles:
        print(f"\n{'=' * 80}")
        print(f"Perfil: {profile['nombre']}")
        print("=" * 80)
        
        result = engine.predict_action(
            profile['edad'],
            profile['tiene_alergias'],
            profile['condicion_cronica'],
            profile['toma_medicamentos'],
            profile['tipo_sangre']
        )
        
        risk = engine.analyze_risk_factors(result['profile'])
        
        print(f"\nEdad: {profile['edad']} años")
        print(f"Tipo de sangre: {profile['tipo_sangre']}")
        print(f"\nAcción: {result['accion_recomendada']}")
        print(f"Nivel de riesgo: {risk['nivel_riesgo'].upper()}")
        print(f"\nRecomendaciones:")
        for i, rec in enumerate(result['recomendaciones'], 1):
            print(f"  {i}. {rec}")


def main():
    """Main execution with CLI"""
    parser = argparse.ArgumentParser(
        description='AuraResourceHub Medical Profile - Testing & Inference'
    )
    parser.add_argument(
        '--mode',
        choices=['demo', 'interactive', 'single', 'evaluate'],
        default='demo',
        help='Testing mode'
    )
    parser.add_argument('--edad', type=int, help='Age')
    parser.add_argument('--alergias', action='store_true', help='Has allergies')
    parser.add_argument('--cronica', action='store_true', help='Has chronic condition')
    parser.add_argument('--medicamentos', action='store_true', help='Takes medications')
    parser.add_argument('--sangre', type=str, help='Blood type')
    parser.add_argument('--csv', type=str, help='CSV for evaluation')
    
    args = parser.parse_args()
    
    try:
        engine = ResourceHubEngine()
        engine.load_artifacts()
        
        if args.mode == 'demo':
            run_demo_profiles()
            
        elif args.mode == 'interactive':
            engine.interactive_mode()
            
        elif args.mode == 'single':
            if args.edad is None or args.sangre is None:
                raise ValueError("--edad and --sangre required for single mode")
            
            result = engine.predict_action(
                args.edad, args.alergias, args.cronica,
                args.medicamentos, args.sangre
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.mode == 'evaluate':
            if not args.csv:
                raise ValueError("--csv required for evaluate mode")
            
            results = engine.evaluate_dataset(args.csv)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        
    except Exception as e:
        logger.error("Execution failed: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
