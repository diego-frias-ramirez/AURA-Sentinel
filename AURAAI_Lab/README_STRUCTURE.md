# Estructura - AURAAI_Lab

Generado: 2025-11-25 07:53:43

AURAAI_Lab/
├── agentcore/
│   ├── data/
│   │   └── emergencias.csv
│   ├── models/
│   │   ├── mobile/
│   │   │   ├── metadata.json
│   │   │   ├── random_forest.json
│   │   │   └── vocabulary.json
│   │   ├── agentcore_encoder.joblib
│   │   ├── agentcore_production.joblib
│   │   ├── agentcore_vectorizer.joblib
│   │   ├── inference.log
│   │   ├── training.log
│   │   └── training_metrics.json
│   ├── export.py
│   ├── test.py
│   └── train.py
├── chatlite/
│   ├── data/
│   │   └── chat_intents.csv
│   ├── models/
│   │   ├── mobile/
│   │   │   ├── metadata.json
│   │   │   ├── random_forest.json
│   │   │   └── vocabulary.json
│   │   ├── chatlite_classifier.joblib
│   │   ├── chatlite_encoder.joblib
│   │   ├── chatlite_vectorizer.joblib
│   │   ├── inference.log
│   │   ├── training.log
│   │   └── training_metrics.json
│   ├── export.py
│   ├── test.py
│   └── train.py
├── geoguard/
│   ├── data/
│   │   └── facilities.csv
│   ├── models/
│   │   ├── facilities_database.json
│   │   ├── geographic_zones.json
│   │   ├── geoguard_clusters.joblib
│   │   ├── geoguard_neighbors.joblib
│   │   ├── geoguard_scaler.joblib
│   │   ├── inference.log
│   │   ├── training.log
│   │   └── training_metrics.json
│   ├── export_tflite.py
│   ├── test.py
│   └── train.py
├── orchestrator/
│   ├── config.json
│   └── main.py
├── resourcehub/
│   ├── data/
│   │   └── medical_profiles.csv
│   ├── models/
│   │   ├── mobile/
│   │   │   ├── decision_tree.json
│   │   │   └── metadata.json
│   │   ├── feature_names.json
│   │   ├── inference.log
│   │   ├── resourcehub_classifier.joblib
│   │   ├── resourcehub_encoder.joblib
│   │   ├── training.log
│   │   └── training_metrics.json
│   ├── export.py
│   ├── test.py
│   └── train.py
├── voicelite/
│   ├── data/
│   ├── models/
│   ├── infer_stt.py
│   └── infer_tts.py
├── gen.py
├── README.md
└── requirements.txt
```

## Modulos

- agentcore - Clasificador emergencias
- chatlite - Clasificador intents
- geoguard - Geolocalizacion
- resourcehub - Perfiles medicos
- voicelite - Voz
- orchestrator - Cerebro IA
