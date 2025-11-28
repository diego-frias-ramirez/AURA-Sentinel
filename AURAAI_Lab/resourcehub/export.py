"""
Export ResourceHub for Flutter (sin TensorFlow)
Exporta DecisionTreeClassifier a formato JSON para Flutter
"""

import joblib
import json
import numpy as np
import os

# Paths
MODEL_PATH = 'models/resourcehub_classifier.joblib'
ENCODER_PATH = 'models/resourcehub_encoder.joblib'
FEATURE_NAMES_PATH = 'models/feature_names.json'
OUTPUT_DIR = 'models/mobile'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("RESOURCEHUB MOBILE EXPORT")
print("=" * 80)

# Cargar modelos
print("\nCargando modelos...")
model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

# Cargar nombres de características
with open(FEATURE_NAMES_PATH, 'r', encoding='utf-8') as f:
    feature_names = json.load(f)

print(f"✓ Modelo: {type(model).__name__}")
print(f"✓ Acciones: {encoder.classes_.tolist()}")
print(f"✓ Número de características: {len(feature_names)}")

def convert_numpy(obj):
    """Convierte tipos numpy a tipos nativos Python"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

def export_tree(tree, feature_names, class_names):
    """Exporta un árbol de decisión a JSON"""
    tree_ = tree.tree_
    
    def recurse(node):
        if tree_.feature[node] != -2:  # No es hoja
            feature_idx = int(tree_.feature[node])
            feature_name = feature_names[feature_idx] if feature_idx < len(feature_names) else f"feature_{feature_idx}"
            threshold = float(tree_.threshold[node])
            
            return {
                'type': 'decision',
                'feature_idx': feature_idx,
                'feature': feature_name,
                'threshold': threshold,
                'left': recurse(int(tree_.children_left[node])),
                'right': recurse(int(tree_.children_right[node]))
            }
        else:  # Es hoja
            values = tree_.value[node][0]
            class_idx = int(np.argmax(values))
            confidence = float(values[class_idx] / np.sum(values)) if np.sum(values) > 0 else 0.0
            
            return {
                'type': 'leaf',
                'class_idx': class_idx,
                'class': class_names[class_idx],
                'confidence': confidence,
                'votes': [float(v) for v in values]
            }
    
    return recurse(0)

# Exportar árbol de decisión
print("\nExportando árbol de decisión...")
class_names = encoder.classes_.tolist()
tree_data = export_tree(model, feature_names, class_names)

tree_path = os.path.join(OUTPUT_DIR, 'decision_tree.json')
with open(tree_path, 'w', encoding='utf-8') as f:
    json.dump(tree_data, f, ensure_ascii=False, indent=2)
print(f"✓ Árbol de decisión: {tree_path}")

# Exportar metadata
print("\nExportando metadata...")
metadata = {
    'model_type': 'DecisionTreeClassifier',
    'actions': class_names,
    'n_actions': int(len(class_names)),
    'n_features': int(len(feature_names)),
    'feature_names': feature_names,
    'max_depth': int(model.max_depth),
    'min_samples_split': int(model.min_samples_split),
    'min_samples_leaf': int(model.min_samples_leaf),
    'criterion': model.criterion,
    'tree_depth': int(model.get_depth()),
    'n_leaves': int(model.get_n_leaves())
}

metadata_path = os.path.join(OUTPUT_DIR, 'metadata.json')
with open(metadata_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)
print(f"✓ Metadata: {metadata_path}")

# Calcular tamaño total
total_size = sum(
    os.path.getsize(os.path.join(OUTPUT_DIR, f)) 
    for f in os.listdir(OUTPUT_DIR)
)

print("\n" + "=" * 80)
print("✓ EXPORTACIÓN COMPLETADA")
print("=" * 80)
print(f"\nArchivos generados en: {OUTPUT_DIR}/")
print(f"  - decision_tree.json")
print(f"  - metadata.json")
print(f"\nTamaño total: {total_size / 1024:.1f} KB")
print("\nEstos archivos se pueden usar directamente en Flutter/Dart")