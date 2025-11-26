"""
Export ChatLite for Flutter (sin TensorFlow)
Exporta RandomForestClassifier a formato JSON para Flutter
"""

import joblib
import json
import numpy as np
import os

# Paths
MODEL_PATH = 'models/chatlite_classifier.joblib'
VECTORIZER_PATH = 'models/chatlite_vectorizer.joblib'
ENCODER_PATH = 'models/chatlite_encoder.joblib'
OUTPUT_DIR = 'models/mobile'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("CHATLITE MOBILE EXPORT")
print("=" * 80)

# Cargar modelos
print("\nCargando modelos...")
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
encoder = joblib.load(ENCODER_PATH)

print(f"✓ Modelo: {type(model).__name__}")
print(f"✓ Intenciones: {encoder.classes_.tolist()}")
print(f"✓ Número de árboles: {len(model.estimators_)}")

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
            # Asegurarse de que feature_idx esté dentro de los límites
            if feature_idx < len(feature_names):
                feature_name = feature_names[feature_idx]
            else:
                feature_name = f"feature_{feature_idx}"
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

# Exportar vocabulario
print("\nExportando vocabulario...")
vocab = vectorizer.vocabulary_
# Convertir int64 a int nativo
vocabulary = {word: int(idx) for word, idx in vocab.items()}

vocab_path = os.path.join(OUTPUT_DIR, 'vocabulary.json')
with open(vocab_path, 'w', encoding='utf-8') as f:
    json.dump(vocabulary, f, ensure_ascii=False, indent=2)
print(f"✓ Vocabulario: {vocab_path} ({len(vocabulary)} palabras)")

# Exportar todos los árboles del RandomForest
print("\nExportando árboles del RandomForest...")
feature_names = sorted(vocabulary.keys(), key=lambda x: vocabulary[x])
class_names = encoder.classes_.tolist()

trees = []
for i, estimator in enumerate(model.estimators_):
    print(f"  Exportando árbol {i+1}/{len(model.estimators_)}...", end='\r')
    tree_data = export_tree(estimator, feature_names, class_names)
    trees.append(tree_data)

print(f"\n✓ Exportados {len(trees)} árboles")

forest_path = os.path.join(OUTPUT_DIR, 'random_forest.json')
with open(forest_path, 'w', encoding='utf-8') as f:
    json.dump({'trees': trees}, f, ensure_ascii=False, indent=2)
print(f"✓ RandomForest: {forest_path}")

# Exportar metadata
print("\nExportando metadata...")
metadata = {
    'model_type': 'RandomForestClassifier',
    'n_estimators': int(len(model.estimators_)),
    'intents': class_names,
    'n_intents': int(len(class_names)),
    'n_features': int(len(vocabulary)),
    'vocab_size': int(len(vocabulary)),
    'max_depth': int(model.max_depth) if model.max_depth else None,
    'feature_names': feature_names[:10]  # Primeras 10 para referencia
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
print(f"  - vocabulary.json ({len(vocabulary)} palabras)")
print(f"  - random_forest.json ({len(trees)} árboles)")
print(f"  - metadata.json")
print(f"\nTamaño total: {total_size / 1024:.1f} KB")
print("\nEstos archivos se pueden usar directamente en Flutter/Dart")