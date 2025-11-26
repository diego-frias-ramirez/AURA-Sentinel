"""
AuraAgentCore - Emergency Classification Testing & Inference
Production-grade inference system with batch processing, confidence scoring,
and comprehensive error handling.

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
from typing import Dict, List, Tuple, Union
import warnings
warnings.filterwarnings('ignore')

# Paths
MODEL_PATH = 'models/agentcore_production.joblib'
VECTORIZER_PATH = 'models/agentcore_vectorizer.joblib'
ENCODER_PATH = 'models/agentcore_encoder.joblib'
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


class EmergencyInferenceEngine:
    """Production inference engine for emergency classification"""
    
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
            # Validate files exist
            required_files = [MODEL_PATH, VECTORIZER_PATH, ENCODER_PATH]
            missing = [f for f in required_files if not os.path.exists(f)]
            
            if missing:
                raise FileNotFoundError(
                    f"Missing required files: {missing}. Run train.py first."
                )
            
            # Load artifacts
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            self.label_encoder = joblib.load(ENCODER_PATH)
            
            # Load metrics if available
            if os.path.exists(METRICS_PATH):
                with open(METRICS_PATH, 'r') as f:
                    self.metrics = json.load(f)
                    logger.info("Model metrics loaded - Test Accuracy: %.4f", 
                              self.metrics.get('test_accuracy', 0))
            
            self.is_loaded = True
            logger.info("All artifacts loaded successfully")
            logger.info("Available classes: %s", self.label_encoder.classes_.tolist())
            
        except Exception as e:
            logger.error("Failed to load artifacts: %s", str(e))
            raise
    
    def predict_single(self, text: str, return_probabilities: bool = True) -> Dict:
        """
        Predict emergency class for single text input
        
        Args:
            text: Input emergency message
            return_probabilities: Whether to return confidence scores
            
        Returns:
            Dictionary with prediction results
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_artifacts() first.")
        
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")
        
        # Vectorize input
        X = self.vectorizer.transform([text])
        
        # Predict
        prediction_encoded = self.model.predict(X)[0]
        prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
        
        result = {
            'text': text,
            'predicted_class': prediction,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add probabilities if requested
        if return_probabilities and hasattr(self.model, 'predict_proba'):
            probas = self.model.predict_proba(X)[0]
            
            # Create probability distribution
            prob_dist = {
                cls: float(prob) 
                for cls, prob in zip(self.label_encoder.classes_, probas)
            }
            
            result['confidence'] = float(probas[prediction_encoded])
            result['all_probabilities'] = prob_dist
            
            # Sort by probability
            sorted_probs = sorted(
                prob_dist.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            result['top_3_predictions'] = [
                {'class': cls, 'probability': prob}
                for cls, prob in sorted_probs[:3]
            ]
        
        return result
    
    def predict_batch(self, texts: List[str], 
                     return_probabilities: bool = True) -> List[Dict]:
        """
        Predict emergency classes for multiple texts
        
        Args:
            texts: List of emergency messages
            return_probabilities: Whether to return confidence scores
            
        Returns:
            List of prediction dictionaries
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_artifacts() first.")
        
        logger.info("Processing batch of %d samples", len(texts))
        
        # Vectorize all inputs
        X = self.vectorizer.transform(texts)
        
        # Predict
        predictions_encoded = self.model.predict(X)
        predictions = self.label_encoder.inverse_transform(predictions_encoded)
        
        results = []
        
        for i, (text, pred) in enumerate(zip(texts, predictions)):
            result = {
                'id': i,
                'text': text,
                'predicted_class': pred,
                'timestamp': datetime.now().isoformat()
            }
            
            if return_probabilities and hasattr(self.model, 'predict_proba'):
                probas = self.model.predict_proba(X[i:i+1])[0]
                pred_idx = predictions_encoded[i]
                
                result['confidence'] = float(probas[pred_idx])
                result['all_probabilities'] = {
                    cls: float(prob) 
                    for cls, prob in zip(self.label_encoder.classes_, probas)
                }
            
            results.append(result)
        
        logger.info("Batch processing completed")
        return results
    
    def evaluate_dataset(self, csv_path: str) -> Dict:
        """
        Evaluate model on a labeled dataset
        
        Args:
            csv_path: Path to CSV with 'texto_mensaje' and 'clase_emergencia'
            
        Returns:
            Evaluation metrics dictionary
        """
        logger.info("Evaluating on dataset: %s", csv_path)
        
        df = pd.read_csv(csv_path)
        
        if 'texto_mensaje' not in df.columns or 'clase_emergencia' not in df.columns:
            raise ValueError("CSV must contain 'texto_mensaje' and 'clase_emergencia' columns")
        
        X = self.vectorizer.transform(df['texto_mensaje'])
        y_true_encoded = self.label_encoder.transform(df['clase_emergencia'])
        y_pred_encoded = self.model.predict(X)
        
        from sklearn.metrics import (
            accuracy_score, precision_recall_fscore_support,
            classification_report, confusion_matrix
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
        
        # Detailed report
        report = classification_report(
            y_true_encoded, y_pred_encoded,
            target_names=self.label_encoder.classes_,
            zero_division=0
        )
        logger.info("\nDetailed Classification Report:\n%s", report)
        
        return results
    
    def get_feature_importance(self, top_n: int = 20) -> List[Tuple[str, float]]:
        """
        Get most important features from the model
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            List of (feature_name, importance_score) tuples
        """
        if not hasattr(self.model, 'feature_importances_'):
            logger.warning("Model does not have feature_importances_ attribute")
            return []
        
        feature_names = self.vectorizer.get_feature_names_out()
        importances = self.model.feature_importances_
        
        # Sort by importance
        indices = np.argsort(importances)[::-1][:top_n]
        
        top_features = [
            (feature_names[idx], float(importances[idx]))
            for idx in indices
        ]
        
        return top_features
    
    def interactive_mode(self):
        """Interactive testing mode for manual input"""
        logger.info("Starting interactive mode. Type 'exit' to quit.")
        print("\n" + "=" * 80)
        print("AURA SENTINEL - EMERGENCY CLASSIFIER - INTERACTIVE MODE")
        print("=" * 80)
        print("\nAvailable classes:", ", ".join(self.label_encoder.classes_))
        print("\nEnter emergency messages to classify (type 'exit' to quit):\n")
        
        while True:
            try:
                text = input("\n> Emergency message: ").strip()
                
                if text.lower() == 'exit':
                    print("\nExiting interactive mode.")
                    break
                
                if not text:
                    print("Please enter a valid message.")
                    continue
                
                result = self.predict_single(text, return_probabilities=True)
                
                print("\n" + "-" * 80)
                print(f"Predicted Class: {result['predicted_class']}")
                print(f"Confidence: {result['confidence']:.4f}")
                print("\nTop 3 Predictions:")
                for i, pred in enumerate(result['top_3_predictions'], 1):
                    print(f"  {i}. {pred['class']}: {pred['probability']:.4f}")
                print("-" * 80)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting.")
                break
            except Exception as e:
                logger.error("Error during prediction: %s", str(e))
                print(f"\nError: {str(e)}")


def run_demo_predictions():
    """Run demo predictions with sample emergency messages"""
    demo_cases = [
        "Me caí de la escalera y me duele mucho la pierna, no puedo caminar",
        "Incendio en la cocina, hay mucho humo y fuego",
        "Asalto en la calle, me robaron mi celular con violencia",
        "Terremoto muy fuerte, los muebles se cayeron",
        "Accidente automovilístico grave, hay varios heridos",
        "Tengo mucha ansiedad y no puedo respirar bien",
        "Creo que me intoxiqué con comida en mal estado",
        "Inundación en mi casa por las lluvias fuertes"
    ]
    
    engine = EmergencyInferenceEngine()
    engine.load_artifacts()
    
    logger.info("Running demo predictions on %d sample cases", len(demo_cases))
    print("\n" + "=" * 80)
    print("DEMO PREDICTIONS")
    print("=" * 80)
    
    results = engine.predict_batch(demo_cases, return_probabilities=True)
    
    for result in results:
        print(f"\n[Case {result['id'] + 1}]")
        print(f"Text: {result['text']}")
        print(f"Predicted: {result['predicted_class']} (confidence: {result['confidence']:.4f})")


def main():
    """Main execution with CLI argument parsing"""
    parser = argparse.ArgumentParser(
        description='AuraAgentCore Emergency Classifier - Testing & Inference'
    )
    parser.add_argument(
        '--mode',
        choices=['demo', 'interactive', 'evaluate', 'single'],
        default='demo',
        help='Testing mode to run'
    )
    parser.add_argument(
        '--text',
        type=str,
        help='Single text to classify (for single mode)'
    )
    parser.add_argument(
        '--csv',
        type=str,
        help='Path to CSV for evaluation (for evaluate mode)'
    )
    
    args = parser.parse_args()
    
    try:
        engine = EmergencyInferenceEngine()
        engine.load_artifacts()
        
        if args.mode == 'demo':
            run_demo_predictions()
            
        elif args.mode == 'interactive':
            engine.interactive_mode()
            
        elif args.mode == 'single':
            if not args.text:
                raise ValueError("--text argument required for single mode")
            
            result = engine.predict_single(args.text, return_probabilities=True)
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
    main()
