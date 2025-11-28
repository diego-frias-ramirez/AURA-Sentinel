"""
AuraResourceHub - Medical Profile & Reminders System
Advanced training pipeline for personalized health management,
medication reminders, and medical emergency preparedness.

Author: AuraAI_Lab
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
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
    'max_depth': 8,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'criterion': 'gini',
    'class_weight': 'balanced',
    'enable_hyperparameter_tuning': False
}

# Paths
DATA_PATH = 'data/medical_profiles.csv'
MODEL_PATH = 'models/resourcehub_classifier.joblib'
ENCODER_PATH = 'models/resourcehub_encoder.joblib'
FEATURE_NAMES_PATH = 'models/feature_names.json'
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


class ResourceHubTrainer:
    """Medical profile and reminder system trainer"""
    
    def __init__(self, config):
        self.config = config
        self.model = None
        self.label_encoder = None
        self.feature_names = []
        self.metrics = {}
        
    def load_and_validate_data(self):
        """Load and validate medical profiles dataset"""
        logger.info("Loading medical profiles dataset from: %s", DATA_PATH)
        
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
        
        df = pd.read_csv(DATA_PATH)
        
        # Validate required columns
        required_cols = ['edad', 'tiene_alergias', 'condicion_cronica', 
                        'toma_medicamentos', 'tipo_sangre', 'accion_recomendada']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Dataset must contain columns: {required_cols}")
        
        # Clean data
        initial_size = len(df)
        df = df.dropna(subset=required_cols)
        
        logger.info("Dataset loaded: %d profiles (removed %d with nulls)",
                   len(df), initial_size - len(df))
        logger.info("Actions detected: %s", df['accion_recomendada'].unique().tolist())
        logger.info("Action distribution:\n%s", 
                   df['accion_recomendada'].value_counts().to_string())
        
        return df
    
    def prepare_features(self, df):
        """Prepare features from medical profiles"""
        logger.info("Preparing features from medical profiles...")
        
        # Numeric features
        X_numeric = df[['edad']].values
        
        # Binary features
        binary_cols = ['tiene_alergias', 'condicion_cronica', 'toma_medicamentos']
        X_binary = df[binary_cols].astype(int).values
        
        # Categorical: tipo_sangre (one-hot encoding)
        blood_types = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
        X_blood = pd.get_dummies(df['tipo_sangre'], prefix='sangre').reindex(
            columns=[f'sangre_{bt}' for bt in blood_types], fill_value=0
        ).values
        
        # Combine all features
        X = np.concatenate([X_numeric, X_binary, X_blood], axis=1)
        
        # Store feature names
        self.feature_names = ['edad'] + binary_cols + [f'sangre_{bt}' for bt in blood_types]
        
        logger.info("Features prepared: %d samples, %d features", len(X), X.shape[1])
        logger.info("Feature names: %s", self.feature_names)
        
        return X
    
    def build_decision_tree(self):
        """Build decision tree classifier"""
        logger.info("Building Decision Tree classifier...")
        
        model = DecisionTreeClassifier(
            max_depth=self.config['max_depth'],
            min_samples_split=self.config['min_samples_split'],
            min_samples_leaf=self.config['min_samples_leaf'],
            criterion=self.config['criterion'],
            class_weight=self.config['class_weight'],
            random_state=self.config['random_state']
        )
        
        logger.info("Decision Tree configured")
        return model
    
    def train(self, X, y):
        """Main training pipeline"""
        logger.info("=" * 80)
        logger.info("RESOURCEHUB TRAINING PIPELINE STARTED")
        logger.info("=" * 80)
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded,
            test_size=self.config['test_size'],
            random_state=self.config['random_state'],
            stratify=y_encoded
        )
        
        logger.info("Data split - Train: %d, Test: %d", len(X_train), len(X_test))
        
        # Train model
        if self.config['enable_hyperparameter_tuning']:
            self.model = self.hyperparameter_tuning(X_train, y_train)
        else:
            self.model = self.build_decision_tree()
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
            'max_depth': [6, 8, 10],
            'min_samples_split': [3, 5, 7],
            'min_samples_leaf': [1, 2, 3],
            'criterion': ['gini', 'entropy']
        }
        
        dt_base = DecisionTreeClassifier(
            class_weight=self.config['class_weight'],
            random_state=self.config['random_state']
        )
        
        cv = StratifiedKFold(n_splits=5, shuffle=True,
                            random_state=self.config['random_state'])
        
        grid_search = GridSearchCV(
            dt_base, param_grid, cv=cv,
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
            'actions': self.label_encoder.classes_.tolist(),
            'n_features': len(self.feature_names),
            'n_train_samples': int(len(X_train)),
            'n_test_samples': int(len(X_test)),
            'tree_depth': int(self.model.get_depth()),
            'n_leaves': int(self.model.get_n_leaves())
        }
        
        logger.info("PERFORMANCE METRICS:")
        logger.info("  Train Accuracy: %.4f", train_acc)
        logger.info("  Test Accuracy:  %.4f", test_acc)
        logger.info("  Precision:      %.4f", precision)
        logger.info("  Recall:         %.4f", recall)
        logger.info("  F1-Score:       %.4f", f1)
        logger.info("  Tree Depth:     %d", self.model.get_depth())
        logger.info("  Tree Leaves:    %d", self.model.get_n_leaves())
        
        report = classification_report(
            y_test, y_test_pred,
            target_names=self.label_encoder.classes_,
            zero_division=0
        )
        logger.info("\nCLASSIFICATION REPORT:\n%s", report)
        
        cm = confusion_matrix(y_test, y_test_pred)
        logger.info("\nCONFUSION MATRIX:\n%s", cm)
        
        self._log_feature_importance()
    
    def _log_feature_importance(self):
        """Log feature importance from decision tree"""
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        logger.info("\nFEATURE IMPORTANCE:")
        for i, idx in enumerate(indices, 1):
            if importances[idx] > 0:
                logger.info("  %2d. %-20s %.6f", 
                          i, self.feature_names[idx], importances[idx])
    
    def save(self):
        """Save all artifacts"""
        logger.info("Saving model artifacts...")
        
        os.makedirs('models', exist_ok=True)
        
        joblib.dump(self.model, MODEL_PATH, compress=3)
        joblib.dump(self.label_encoder, ENCODER_PATH, compress=3)
        
        with open(FEATURE_NAMES_PATH, 'w') as f:
            json.dump(self.feature_names, f, indent=2)
        
        with open(METRICS_PATH, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        logger.info("Model saved to: %s", MODEL_PATH)
        logger.info("Label encoder saved to: %s", ENCODER_PATH)
        logger.info("Feature names saved to: %s", FEATURE_NAMES_PATH)
        logger.info("Metrics saved to: %s", METRICS_PATH)


def main():
    """Main execution pipeline"""
    try:
        trainer = ResourceHubTrainer(CONFIG)
        
        # Load data
        df = trainer.load_and_validate_data()
        
        # Prepare features
        X = trainer.prepare_features(df)
        y = df['accion_recomendada']
        
        # Train
        trainer.train(X, y)
        
        # Save
        trainer.save()
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error("Training failed: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
