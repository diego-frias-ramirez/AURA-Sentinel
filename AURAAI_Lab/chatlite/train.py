"""
AuraChatLite - Conversational Intent & Emotion Classifier
Advanced training pipeline for emergency chat support with intent recognition
and emotional state detection for crisis intervention.

Author: AuraAI_Lab
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix
)
import joblib
import os
import json
import logging
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration
CONFIG = {
    'random_state': 42,
    'test_size': 0.2,
    'validation_size': 0.1,
    'n_splits': 5,
    'max_features_tfidf': 400,
    'ngram_range': (1, 2),
    'min_df': 1,
    'max_df': 0.9,
    'use_idf': True,
    'sublinear_tf': True,
    'n_estimators': 150,
    'max_depth': 12,
    'min_samples_split': 3,
    'min_samples_leaf': 1,
    'class_weight': 'balanced',
    'enable_hyperparameter_tuning': False
}

# Paths
DATA_PATH = 'data/chat_intents.csv'
MODEL_PATH = 'models/chatlite_classifier.joblib'
VECTORIZER_PATH = 'models/chatlite_vectorizer.joblib'
ENCODER_PATH = 'models/chatlite_encoder.joblib'
METRICS_PATH = 'models/training_metrics.json'
LOG_PATH = 'models/training.log'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ChatIntentClassifier:
    """Advanced chat intent and emotion classification system"""
    
    def __init__(self, config):
        self.config = config
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.metrics = {}
        
    def load_and_validate_data(self):
        """Load and validate chat intent dataset"""
        logger.info("Loading chat intent dataset from: %s", DATA_PATH)
        
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
        
        df = pd.read_csv(DATA_PATH)
        
        required_cols = ['texto_usuario', 'intent']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Dataset must contain columns: {required_cols}")
        
        # Clean data
        initial_size = len(df)
        df = df.drop_duplicates(subset=['texto_usuario'])
        df = df.dropna(subset=required_cols)
        df['texto_usuario'] = df['texto_usuario'].str.strip()
        
        logger.info("Dataset loaded: %d records (removed %d duplicates/nulls)",
                   len(df), initial_size - len(df))
        logger.info("Intents detected: %s", df['intent'].unique().tolist())
        logger.info("Intent distribution:\n%s", df['intent'].value_counts().to_string())
        
        return df['texto_usuario'], df['intent']
    
    def create_chat_vectorizer(self):
        """Create optimized vectorizer for conversational text"""
        vectorizer = TfidfVectorizer(
            max_features=self.config['max_features_tfidf'],
            ngram_range=self.config['ngram_range'],
            min_df=self.config['min_df'],
            max_df=self.config['max_df'],
            use_idf=self.config['use_idf'],
            sublinear_tf=self.config['sublinear_tf'],
            strip_accents='unicode',
            lowercase=True,
            analyzer='word',
            token_pattern=r'\b[a-záéíóúñü]+\b',
            stop_words=self._get_minimal_stopwords()
        )
        return vectorizer
    
    def _get_minimal_stopwords(self):
        """Minimal stopwords to preserve conversational context"""
        # Keep emotion-relevant words, remove only filler words
        minimal_stops = [
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se',
            'por', 'con', 'su', 'para', 'como', 'estar', 'le', 'lo',
            'pero', 'o', 'este', 'ese', 'si', 'ya', 'ver', 'porque',
            'dar', 'cuando', 'sobre', 'mi', 'yo', 'también', 'hasta'
        ]
        return minimal_stops
    
    def build_model(self):
        """Build optimized Random Forest for intent classification"""
        model = RandomForestClassifier(
            n_estimators=self.config['n_estimators'],
            max_depth=self.config['max_depth'],
            min_samples_split=self.config['min_samples_split'],
            min_samples_leaf=self.config['min_samples_leaf'],
            class_weight=self.config['class_weight'],
            random_state=self.config['random_state'],
            n_jobs=-1,
            bootstrap=True,
            oob_score=True,
            max_features='sqrt'
        )
        
        logger.info("RandomForest classifier configured")
        return model
    
    def train(self, X_text, y):
        """Main training pipeline"""
        logger.info("=" * 80)
        logger.info("CHATLITE TRAINING PIPELINE STARTED")
        logger.info("=" * 80)
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train_text, X_test_text, y_train, y_test = train_test_split(
            X_text, y_encoded,
            test_size=self.config['test_size'],
            random_state=self.config['random_state'],
            stratify=y_encoded
        )
        
        logger.info("Data split - Train: %d, Test: %d", len(X_train_text), len(X_test_text))
        
        # Vectorize
        self.vectorizer = self.create_chat_vectorizer()
        X_train = self.vectorizer.fit_transform(X_train_text)
        X_test = self.vectorizer.transform(X_test_text)
        
        logger.info("Vectorization complete - Features: %d", X_train.shape[1])
        
        # Train model
        if self.config['enable_hyperparameter_tuning']:
            self.model = self.hyperparameter_tuning(X_train, y_train)
        else:
            self.model = self.build_model()
            logger.info("Training model...")
            self.model.fit(X_train, y_train)
            logger.info("Training completed")
        
        # Evaluate
        self.evaluate(X_train, y_train, X_test, y_test)
        
        logger.info("=" * 80)
        logger.info("TRAINING COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
    
    def hyperparameter_tuning(self, X_train, y_train):
        """Optimize hyperparameters with grid search"""
        logger.info("Starting hyperparameter optimization...")
        
        param_grid = {
            'n_estimators': [100, 150, 200],
            'max_depth': [10, 12, 15],
            'min_samples_split': [2, 3, 5],
            'min_samples_leaf': [1, 2]
        }
        
        rf_base = RandomForestClassifier(
            class_weight=self.config['class_weight'],
            random_state=self.config['random_state'],
            n_jobs=-1
        )
        
        cv = StratifiedKFold(n_splits=self.config['n_splits'], shuffle=True,
                            random_state=self.config['random_state'])
        
        grid_search = GridSearchCV(
            rf_base, param_grid, cv=cv,
            scoring='f1_weighted',
            n_jobs=-1, verbose=2
        )
        
        grid_search.fit(X_train, y_train)
        
        logger.info("Best parameters: %s", grid_search.best_params_)
        logger.info("Best CV score: %.4f", grid_search.best_score_)
        
        return grid_search.best_estimator_
    
    def evaluate(self, X_train, y_train, X_test, y_test):
        """Comprehensive evaluation"""
        logger.info("Evaluating model performance...")
        
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_test_pred, average='weighted', zero_division=0
        )
        
        self.metrics = {
            'timestamp': datetime.now().isoformat(),
            'train_accuracy': float(train_acc),
            'test_accuracy': float(test_acc),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'intents': self.label_encoder.classes_.tolist(),
            'n_features': int(X_train.shape[1]),
            'n_train_samples': int(X_train.shape[0]),
            'n_test_samples': int(X_test.shape[0])
        }
        
        logger.info("PERFORMANCE METRICS:")
        logger.info("  Train Accuracy: %.4f", train_acc)
        logger.info("  Test Accuracy:  %.4f", test_acc)
        logger.info("  Precision:      %.4f", precision)
        logger.info("  Recall:         %.4f", recall)
        logger.info("  F1-Score:       %.4f", f1)
        
        report = classification_report(
            y_test, y_test_pred,
            target_names=self.label_encoder.classes_,
            zero_division=0
        )
        logger.info("\nCLASSIFICATION REPORT:\n%s", report)
        
        cm = confusion_matrix(y_test, y_test_pred)
        logger.info("\nCONFUSION MATRIX:\n%s", cm)
        
        if hasattr(self.model, 'feature_importances_'):
            self._log_feature_importance()
    
    def _log_feature_importance(self):
        """Log top important features"""
        feature_names = self.vectorizer.get_feature_names_out()
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1][:20]
        
        logger.info("\nTOP 20 IMPORTANT FEATURES:")
        for i, idx in enumerate(indices, 1):
            logger.info("  %2d. %-20s %.6f", i, feature_names[idx], importances[idx])
    
    def save(self):
        """Save all artifacts"""
        logger.info("Saving model artifacts...")
        
        os.makedirs('models', exist_ok=True)
        
        joblib.dump(self.model, MODEL_PATH, compress=3)
        joblib.dump(self.vectorizer, VECTORIZER_PATH, compress=3)
        joblib.dump(self.label_encoder, ENCODER_PATH, compress=3)
        
        with open(METRICS_PATH, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        logger.info("Model saved to: %s", MODEL_PATH)
        logger.info("Vectorizer saved to: %s", VECTORIZER_PATH)
        logger.info("Label encoder saved to: %s", ENCODER_PATH)
        logger.info("Metrics saved to: %s", METRICS_PATH)


def main():
    """Main execution pipeline"""
    try:
        classifier = ChatIntentClassifier(CONFIG)
        
        X_text, y = classifier.load_and_validate_data()
        classifier.train(X_text, y)
        classifier.save()
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error("Training failed: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
