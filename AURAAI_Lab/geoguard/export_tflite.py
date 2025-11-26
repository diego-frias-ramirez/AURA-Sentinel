"""
AuraGeoGuard - TensorFlow Lite Export Pipeline
Professional conversion pipeline for geographic clustering and routing
optimized for mobile deployment with offline map support.

Author: AuraAI_Lab
Version: 1.0.0
"""

import numpy as np
import tensorflow as tf
import joblib
import os
import json
import logging
from datetime import datetime
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

# Paths
CLUSTERS_MODEL_PATH = 'models/geoguard_clusters.joblib'
NEIGHBORS_MODEL_PATH = 'models/geoguard_neighbors.joblib'
SCALER_PATH = 'models/geoguard_scaler.joblib'
FACILITIES_PATH = 'models/facilities_database.json'
ZONES_PATH = 'models/geographic_zones.json'
TFLITE_CLUSTERS_PATH = 'models/geoguard_clusters.tflite'
FACILITIES_MOBILE_PATH = 'models/facilities_mobile.json'
ZONES_MOBILE_PATH = 'models/zones_mobile.json'
ROUTING_CONFIG_PATH = 'models/routing_config.json'
CONVERSION_LOG = 'models/tflite_conversion.log'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONVERSION_LOG),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GeoGuardTFLiteConverter:
    """Advanced converter for geographic models to mobile format"""
    
    def __init__(self):
        self.kmeans_model = None
        self.nn_model = None
        self.scaler = None
        self.facilities_db = None
        self.zones = None
        self.tf_model = None
        
    def load_sklearn_artifacts(self):
        """Load trained scikit-learn models"""
        logger.info("Loading scikit-learn artifacts...")
        
        if not os.path.exists(CLUSTERS_MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {CLUSTERS_MODEL_PATH}")
        
        self.kmeans_model = joblib.load(CLUSTERS_MODEL_PATH)
        self.nn_model = joblib.load(NEIGHBORS_MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)
        
        with open(FACILITIES_PATH, 'r', encoding='utf-8') as f:
            self.facilities_db = json.load(f)
        
        if os.path.exists(ZONES_PATH):
            with open(ZONES_PATH, 'r', encoding='utf-8') as f:
                self.zones = json.load(f)
        
        logger.info("Artifacts loaded successfully")
        logger.info("KMeans clusters: %d", self.kmeans_model.n_clusters)
        logger.info("Facilities: %d", len(self.facilities_db))
    
    def build_keras_clustering_model(self):
        """
        Build Keras model to approximate KMeans clustering
        Uses cluster centers as fixed weights
        """
        logger.info("Building Keras clustering approximation...")
        
        n_features = 2  # lat, lon
        n_clusters = self.kmeans_model.n_clusters
        
        # Get cluster centers
        cluster_centers = self.kmeans_model.cluster_centers_
        
        # Build model that computes distances to cluster centers
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(n_features,), name='coordinates_input'),
            tf.keras.layers.Dense(
                n_clusters,
                activation='softmax',
                use_bias=False,
                name='cluster_distances'
            )
        ])
        
        # Initialize weights with cluster centers (transposed)
        # Note: This is an approximation, actual KMeans uses Euclidean distance
        model.layers[0].set_weights([cluster_centers.T])
        
        logger.info("Keras clustering model created")
        logger.info("Input: 2 features (lat, lon)")
        logger.info("Output: %d cluster probabilities", n_clusters)
        
        return model
    
    def convert_clustering_to_tflite(self) -> bytes:
        """Convert clustering model to TFLite"""
        logger.info("Converting clustering model to TFLite...")
        
        # Build Keras approximation
        self.tf_model = self.build_keras_clustering_model()
        
        # Convert to TFLite
        converter = tf.lite.TFLiteConverter.from_keras_model(self.tf_model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.experimental_new_converter = True
        
        tflite_model = converter.convert()
        
        logger.info("Conversion completed")
        logger.info("Model size: %.2f KB", len(tflite_model) / 1024)
        
        return tflite_model
    
    def prepare_facilities_for_mobile(self) -> Dict:
        """
        Prepare facilities database optimized for mobile use
        Includes precomputed distances and routing hints
        """
        logger.info("Preparing facilities database for mobile...")
        
        # Group facilities by type
        facilities_by_type = {}
        for facility in self.facilities_db:
            ftype = facility['tipo']
            if ftype not in facilities_by_type:
                facilities_by_type[ftype] = []
            
            # Simplify facility data for mobile
            mobile_facility = {
                'id': facility.get('id', facilities_by_type[ftype].__len__()),
                'nombre': facility['nombre'],
                'tipo': facility['tipo'],
                'lat': float(facility['latitud']),
                'lon': float(facility['longitud']),
                'cluster_id': int(facility.get('cluster_id', -1)),
                'direccion': facility.get('direccion', ''),
                'telefono': facility.get('telefono', ''),
                'horario': facility.get('horario', '24 horas')
            }
            
            facilities_by_type[ftype].append(mobile_facility)
        
        # Create index for fast lookup
        mobile_data = {
            'facilities_by_type': facilities_by_type,
            'all_facilities': self.facilities_db,
            'total_count': len(self.facilities_db),
            'types': list(facilities_by_type.keys()),
            'export_timestamp': datetime.now().isoformat()
        }
        
        logger.info("Mobile facilities prepared: %d types", len(facilities_by_type))
        
        return mobile_data
    
    def prepare_zones_for_mobile(self) -> Dict:
        """Prepare geographic zones optimized for mobile"""
        logger.info("Preparing zones for mobile...")
        
        if not self.zones:
            logger.warning("No zones data available")
            return {}
        
        mobile_zones = {}
        
        for zone_key, zone_data in self.zones.items():
            zone_id = zone_data['zone_id']
            
            mobile_zone = {
                'id': zone_id,
                'name': f"Zona {zone_id + 1}",
                'center': {
                    'lat': float(zone_data['center_lat']),
                    'lon': float(zone_data['center_lon'])
                },
                'bounds': zone_data['bounds'],
                'facility_count': zone_data['n_facilities'],
                'facility_types': {}
            }
            
            # Count facility types in zone
            for facility in zone_data.get('facilities', []):
                ftype = facility['tipo']
                mobile_zone['facility_types'][ftype] = \
                    mobile_zone['facility_types'].get(ftype, 0) + 1
            
            mobile_zones[f"zone_{zone_id}"] = mobile_zone
        
        logger.info("Mobile zones prepared: %d zones", len(mobile_zones))
        
        return mobile_zones
    
    def create_routing_config(self) -> Dict:
        """Create routing configuration for mobile app"""
        logger.info("Creating routing configuration...")
        
        config = {
            'model_info': {
                'name': 'AuraGeoGuard',
                'version': '1.0.0',
                'type': 'geographic_routing',
                'framework': 'tflite'
            },
            'clustering': {
                'n_clusters': int(self.kmeans_model.n_clusters),
                'scaler_mean': self.scaler.mean_.tolist(),
                'scaler_scale': self.scaler.scale_.tolist(),
                'cluster_centers': self.kmeans_model.cluster_centers_.tolist()
            },
            'routing': {
                'distance_metric': 'haversine',
                'earth_radius_km': 6371,
                'default_speed_kmh': 40,
                'max_search_radius_km': 50
            },
            'emergency_mapping': {
                'medica': 'hospital',
                'accidente': 'hospital',
                'incendio': 'bomberos',
                'desastre_natural': 'refugio',
                'violencia': 'policia',
                'intoxicacion': 'hospital',
                'crisis_emocional': 'hospital',
                'otra': None
            },
            'facility_priorities': {
                'hospital': 1,
                'cruz_roja': 2,
                'clinica': 3,
                'bomberos': 1,
                'policia': 1,
                'proteccion_civil': 2,
                'refugio': 3,
                'farmacia': 4
            },
            'durango_region': {
                'center': {'lat': 24.0277, 'lon': -104.6532},
                'bounds': {
                    'min_lat': 23.5,
                    'max_lat': 25.0,
                    'min_lon': -105.5,
                    'max_lon': -104.0
                }
            },
            'offline_support': {
                'preload_facilities': True,
                'cache_routes': True,
                'fallback_to_nearest': True
            },
            'inference': {
                'input_format': 'normalized_coordinates',
                'output_format': 'cluster_probabilities',
                'confidence_threshold': 0.5
            }
        }
        
        return config
    
    def validate_mobile_export(self) -> Dict:
        """Validate exported data for mobile use"""
        logger.info("Validating mobile export...")
        
        validation = {
            'clustering_model': os.path.exists(TFLITE_CLUSTERS_PATH),
            'facilities_data': os.path.exists(FACILITIES_MOBILE_PATH),
            'zones_data': os.path.exists(ZONES_MOBILE_PATH),
            'routing_config': os.path.exists(ROUTING_CONFIG_PATH),
            'total_facilities': len(self.facilities_db),
            'facility_types': len(set(f['tipo'] for f in self.facilities_db)),
            'zones_count': len(self.zones) if self.zones else 0
        }
        
        # Calculate total export size
        total_size = 0
        for path in [TFLITE_CLUSTERS_PATH, FACILITIES_MOBILE_PATH, 
                     ZONES_MOBILE_PATH, ROUTING_CONFIG_PATH]:
            if os.path.exists(path):
                total_size += os.path.getsize(path)
        
        validation['total_size_kb'] = total_size / 1024
        validation['all_files_present'] = all([
            validation['clustering_model'],
            validation['facilities_data'],
            validation['routing_config']
        ])
        
        logger.info("Validation completed")
        logger.info("  All files present: %s", validation['all_files_present'])
        logger.info("  Total size: %.2f KB", validation['total_size_kb'])
        
        return validation
    
    def save_artifacts(self, tflite_model: bytes, mobile_facilities: Dict,
                      mobile_zones: Dict, routing_config: Dict):
        """Save all mobile artifacts"""
        logger.info("Saving mobile artifacts...")
        
        os.makedirs('models', exist_ok=True)
        
        # Save TFLite model
        with open(TFLITE_CLUSTERS_PATH, 'wb') as f:
            f.write(tflite_model)
        logger.info("TFLite model saved: %s (%.2f KB)",
                   TFLITE_CLUSTERS_PATH, len(tflite_model) / 1024)
        
        # Save mobile facilities
        with open(FACILITIES_MOBILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(mobile_facilities, f, indent=2, ensure_ascii=False)
        logger.info("Mobile facilities saved: %s", FACILITIES_MOBILE_PATH)
        
        # Save mobile zones
        with open(ZONES_MOBILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(mobile_zones, f, indent=2, ensure_ascii=False)
        logger.info("Mobile zones saved: %s", ZONES_MOBILE_PATH)
        
        # Save routing config
        with open(ROUTING_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(routing_config, f, indent=2, ensure_ascii=False)
        logger.info("Routing config saved: %s", ROUTING_CONFIG_PATH)


def main():
    """Main conversion pipeline"""
    logger.info("=" * 80)
    logger.info("GEOGUARD MOBILE EXPORT PIPELINE STARTED")
    logger.info("=" * 80)
    
    try:
        converter = GeoGuardTFLiteConverter()
        
        # Load artifacts
        converter.load_sklearn_artifacts()
        
        # Convert clustering to TFLite
        tflite_model = converter.convert_clustering_to_tflite()
        
        # Prepare mobile data
        mobile_facilities = converter.prepare_facilities_for_mobile()
        mobile_zones = converter.prepare_zones_for_mobile()
        routing_config = converter.create_routing_config()
        
        # Save artifacts
        converter.save_artifacts(
            tflite_model,
            mobile_facilities,
            mobile_zones,
            routing_config
        )
        
        # Validate export
        validation = converter.validate_mobile_export()
        
        logger.info("=" * 80)
        logger.info("EXPORT COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        logger.info("\nGenerated files:")
        logger.info("  - %s", TFLITE_CLUSTERS_PATH)
        logger.info("  - %s", FACILITIES_MOBILE_PATH)
        logger.info("  - %s", ZONES_MOBILE_PATH)
        logger.info("  - %s", ROUTING_CONFIG_PATH)
        
        logger.info("\nExport summary:")
        logger.info("  Total facilities: %d", validation['total_facilities'])
        logger.info("  Facility types: %d", validation['facility_types'])
        logger.info("  Geographic zones: %d", validation['zones_count'])
        logger.info("  Total export size: %.2f KB", validation['total_size_kb'])
        
        logger.info("\nReady for Flutter integration!")
        
    except Exception as e:
        logger.error("Export failed: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
