"""
AuraGeoGuard - Geographic POI Testing & Inference
Production-grade inference system for emergency facility location,
routing, and nearest facility search for Durango, Mexico.

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
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Paths
CLUSTERS_MODEL_PATH = 'models/geoguard_clusters.joblib'
NEIGHBORS_MODEL_PATH = 'models/geoguard_neighbors.joblib'
SCALER_PATH = 'models/geoguard_scaler.joblib'
FACILITIES_PATH = 'models/facilities_database.json'
ZONES_PATH = 'models/geographic_zones.json'
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


class GeoGuardEngine:
    """Production inference engine for geographic routing and POI search"""
    
    # Durango city center coordinates
    DURANGO_CENTER = {'lat': 24.0277, 'lon': -104.6532}
    
    # Facility type translations
    FACILITY_TYPES = {
        'hospital': 'Hospital',
        'clinica': 'Clínica',
        'cruz_roja': 'Cruz Roja',
        'bomberos': 'Bomberos',
        'policia': 'Estación de Policía',
        'proteccion_civil': 'Protección Civil',
        'refugio': 'Refugio/Albergue',
        'farmacia': 'Farmacia 24h'
    }
    
    def __init__(self):
        self.kmeans_model = None
        self.nn_model = None
        self.scaler = None
        self.facilities_db = None
        self.zones = None
        self.metrics = None
        self.is_loaded = False
        
    def load_artifacts(self):
        """Load all required model artifacts"""
        logger.info("Loading model artifacts...")
        
        try:
            required_files = [
                CLUSTERS_MODEL_PATH,
                NEIGHBORS_MODEL_PATH,
                SCALER_PATH,
                FACILITIES_PATH
            ]
            missing = [f for f in required_files if not os.path.exists(f)]
            
            if missing:
                raise FileNotFoundError(
                    f"Missing required files: {missing}. Run train.py first."
                )
            
            # Load models
            self.kmeans_model = joblib.load(CLUSTERS_MODEL_PATH)
            self.nn_model = joblib.load(NEIGHBORS_MODEL_PATH)
            self.scaler = joblib.load(SCALER_PATH)
            
            # Load facilities database
            with open(FACILITIES_PATH, 'r', encoding='utf-8') as f:
                self.facilities_db = json.load(f)
            
            # Load zones
            if os.path.exists(ZONES_PATH):
                with open(ZONES_PATH, 'r', encoding='utf-8') as f:
                    self.zones = json.load(f)
            
            # Load metrics
            if os.path.exists(METRICS_PATH):
                with open(METRICS_PATH, 'r') as f:
                    self.metrics = json.load(f)
                    logger.info("Model metrics loaded - %d facilities, %d zones",
                              self.metrics.get('n_facilities', 0),
                              self.metrics.get('n_clusters', 0))
            
            self.is_loaded = True
            logger.info("All artifacts loaded successfully")
            logger.info("Total facilities: %d", len(self.facilities_db))
            
        except Exception as e:
            logger.error("Failed to load artifacts: %s", str(e))
            raise
    
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate haversine distance in kilometers"""
        R = 6371  # Earth radius in km
        
        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        delta_lat = np.radians(lat2 - lat1)
        delta_lon = np.radians(lon2 - lon1)
        
        a = np.sin(delta_lat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        
        return R * c
    
    def find_nearest_facilities(self, lat: float, lon: float,
                               facility_type: str = None,
                               k: int = 5) -> List[Dict]:
        """
        Find k nearest facilities to given location
        
        Args:
            lat: Latitude
            lon: Longitude
            facility_type: Filter by type (optional)
            k: Number of nearest facilities
            
        Returns:
            List of nearest facilities with distances
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_artifacts() first.")
        
        # Convert to radians for haversine
        query_point = np.radians([[lat, lon]])
        
        # Find k nearest neighbors
        distances, indices = self.nn_model.kneighbors(query_point, n_neighbors=k)
        
        # Convert distances from radians to kilometers
        distances_km = distances[0] * 6371
        
        results = []
        for i, (idx, dist) in enumerate(zip(indices[0], distances_km)):
            facility = self.facilities_db[idx].copy()
            facility['distance_km'] = float(dist)
            facility['rank'] = i + 1
            
            # Calculate estimated time (assuming 40 km/h average in city)
            facility['estimated_time_minutes'] = float(dist / 40 * 60)
            
            # Filter by type if specified
            if facility_type and facility['tipo'] != facility_type:
                continue
            
            results.append(facility)
        
        # If filtered, get more results
        if facility_type and len(results) < k:
            all_distances = []
            for facility in self.facilities_db:
                if facility['tipo'] == facility_type:
                    dist = self.haversine_distance(
                        lat, lon,
                        facility['latitud'], facility['longitud']
                    )
                    facility_copy = facility.copy()
                    facility_copy['distance_km'] = dist
                    facility_copy['estimated_time_minutes'] = dist / 40 * 60
                    all_distances.append(facility_copy)
            
            all_distances.sort(key=lambda x: x['distance_km'])
            results = all_distances[:k]
            
            for i, facility in enumerate(results):
                facility['rank'] = i + 1
        
        return results[:k]
    
    def find_zone(self, lat: float, lon: float) -> Dict:
        """Find which geographic zone contains the location"""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_artifacts() first.")
        
        # Scale coordinates
        X = np.array([[lat, lon]])
        X_scaled = self.scaler.transform(X)
        
        # Predict cluster
        cluster_id = self.kmeans_model.predict(X_scaled)[0]
        
        # Get zone info
        zone_key = f'zone_{cluster_id}'
        zone_info = self.zones.get(zone_key, {}) if self.zones else {}
        
        result = {
            'zone_id': int(cluster_id),
            'zone_name': f'Zona {cluster_id + 1}',
            'n_facilities': zone_info.get('n_facilities', 0),
            'center_lat': zone_info.get('center_lat'),
            'center_lon': zone_info.get('center_lon')
        }
        
        return result
    
    def get_emergency_route(self, lat: float, lon: float,
                           emergency_type: str) -> Dict:
        """
        Get recommended route based on emergency type
        
        Args:
            lat: Current latitude
            lon: Current longitude
            emergency_type: Type of emergency
            
        Returns:
            Route recommendation with facilities
        """
        # Map emergency types to facility types
        emergency_mapping = {
            'medica': 'hospital',
            'accidente': 'hospital',
            'incendio': 'bomberos',
            'violencia': 'policia',
            'crisis_emocional': 'hospital',
            'otra': None
        }
        
        facility_type = emergency_mapping.get(emergency_type)
        
        # Find nearest facilities
        facilities = self.find_nearest_facilities(lat, lon, facility_type, k=3)
        
        # Find zone
        zone = self.find_zone(lat, lon)
        
        result = {
            'emergency_type': emergency_type,
            'current_location': {'lat': lat, 'lon': lon},
            'zone': zone,
            'recommended_facilities': facilities,
            'primary_destination': facilities[0] if facilities else None,
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def get_facilities_by_type(self, facility_type: str) -> List[Dict]:
        """Get all facilities of specific type"""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_artifacts() first.")
        
        facilities = [f for f in self.facilities_db if f['tipo'] == facility_type]
        
        logger.info("Found %d facilities of type: %s", len(facilities), facility_type)
        
        return facilities
    
    def get_zone_facilities(self, zone_id: int) -> List[Dict]:
        """Get all facilities in a specific zone"""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_artifacts() first.")
        
        facilities = [f for f in self.facilities_db if f.get('cluster_id') == zone_id]
        
        logger.info("Found %d facilities in zone %d", len(facilities), zone_id)
        
        return facilities
    
    def interactive_mode(self):
        """Interactive testing mode"""
        logger.info("Starting interactive mode. Type 'exit' to quit.")
        
        print("\n" + "=" * 80)
        print("AURA SENTINEL - GEOGUARD - INTERACTIVE MODE")
        print("=" * 80)
        print("\nBusca instalaciones de emergencia cercanas en Durango.")
        print(f"\nTipos de instalación disponibles:")
        for key, name in self.FACILITY_TYPES.items():
            print(f"  - {key}: {name}")
        
        print(f"\nUbicación Centro Durango: {self.DURANGO_CENTER['lat']}, {self.DURANGO_CENTER['lon']}")
        print("\nIngresa coordenadas para buscar instalaciones cercanas.")
        print("Formato: latitud longitud [tipo_opcional]")
        print("Ejemplo: 24.027 -104.653 hospital")
        print("\nEscribe 'exit' para salir.\n")
        
        while True:
            try:
                user_input = input("\n> Coordenadas: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\nFinalizando GeoGuard. ¡Hasta pronto!")
                    break
                
                if not user_input:
                    continue
                
                parts = user_input.split()
                if len(parts) < 2:
                    print("Error: Ingresa al menos latitud y longitud")
                    continue
                
                lat = float(parts[0])
                lon = float(parts[1])
                facility_type = parts[2] if len(parts) > 2 else None
                
                # Find nearest
                results = self.find_nearest_facilities(lat, lon, facility_type, k=5)
                
                # Find zone
                zone = self.find_zone(lat, lon)
                
                print("\n" + "-" * 80)
                print(f"Ubicación: {lat}, {lon}")
                print(f"Zona: {zone['zone_name']} (ID: {zone['zone_id']})")
                print(f"\n{len(results)} instalaciones más cercanas:")
                print("-" * 80)
                
                for facility in results:
                    print(f"\n{facility['rank']}. {facility['nombre']}")
                    print(f"   Tipo: {self.FACILITY_TYPES.get(facility['tipo'], facility['tipo'])}")
                    print(f"   Distancia: {facility['distance_km']:.2f} km")
                    print(f"   Tiempo estimado: {facility['estimated_time_minutes']:.0f} minutos")
                    print(f"   Ubicación: {facility['latitud']}, {facility['longitud']}")
                
                print("-" * 80)
                
            except KeyboardInterrupt:
                print("\n\nInterrumpido por usuario. Saliendo.")
                break
            except ValueError:
                print("Error: Coordenadas inválidas. Usa formato: latitud longitud")
            except Exception as e:
                logger.error("Error: %s", str(e))
                print(f"\nError: {str(e)}")


def run_demo_search():
    """Run demo searches for common scenarios"""
    demo_locations = [
        {
            'name': 'Centro Durango',
            'lat': 24.0277,
            'lon': -104.6532,
            'emergency': 'medica'
        },
        {
            'name': 'Zona Norte',
            'lat': 24.0500,
            'lon': -104.6500,
            'emergency': 'incendio'
        },
        {
            'name': 'Zona Sur',
            'lat': 24.0100,
            'lon': -104.6600,
            'emergency': 'accidente'
        }
    ]
    
    engine = GeoGuardEngine()
    engine.load_artifacts()
    
    logger.info("Running demo searches for %d locations", len(demo_locations))
    print("\n" + "=" * 80)
    print("DEMO SEARCHES - COMMON EMERGENCY SCENARIOS")
    print("=" * 80)
    
    for location in demo_locations:
        print(f"\n{'=' * 80}")
        print(f"Ubicación: {location['name']}")
        print(f"Coordenadas: {location['lat']}, {location['lon']}")
        print(f"Tipo de emergencia: {location['emergency']}")
        print("=" * 80)
        
        route = engine.get_emergency_route(
            location['lat'],
            location['lon'],
            location['emergency']
        )
        
        print(f"\nZona: {route['zone']['zone_name']}")
        print(f"\nInstalaciones recomendadas:")
        
        for i, facility in enumerate(route['recommended_facilities'][:3], 1):
            print(f"\n{i}. {facility['nombre']}")
            print(f"   Distancia: {facility['distance_km']:.2f} km")
            print(f"   Tiempo: ~{facility['estimated_time_minutes']:.0f} min")


def main():
    """Main execution with CLI"""
    parser = argparse.ArgumentParser(
        description='AuraGeoGuard POI Search - Testing & Inference'
    )
    parser.add_argument(
        '--mode',
        choices=['demo', 'interactive', 'nearest', 'zone', 'route'],
        default='demo',
        help='Testing mode'
    )
    parser.add_argument('--lat', type=float, help='Latitude')
    parser.add_argument('--lon', type=float, help='Longitude')
    parser.add_argument('--type', type=str, help='Facility type filter')
    parser.add_argument('--emergency', type=str, help='Emergency type for routing')
    parser.add_argument('--k', type=int, default=5, help='Number of nearest facilities')
    
    args = parser.parse_args()
    
    try:
        engine = GeoGuardEngine()
        engine.load_artifacts()
        
        if args.mode == 'demo':
            run_demo_search()
            
        elif args.mode == 'interactive':
            engine.interactive_mode()
            
        elif args.mode == 'nearest':
            if args.lat is None or args.lon is None:
                raise ValueError("--lat and --lon required for nearest mode")
            
            results = engine.find_nearest_facilities(
                args.lat, args.lon, args.type, args.k
            )
            print(json.dumps(results, indent=2, ensure_ascii=False))
            
        elif args.mode == 'zone':
            if args.lat is None or args.lon is None:
                raise ValueError("--lat and --lon required for zone mode")
            
            zone = engine.find_zone(args.lat, args.lon)
            print(json.dumps(zone, indent=2, ensure_ascii=False))
            
        elif args.mode == 'route':
            if args.lat is None or args.lon is None or args.emergency is None:
                raise ValueError("--lat, --lon, and --emergency required for route mode")
            
            route = engine.get_emergency_route(args.lat, args.lon, args.emergency)
            print(json.dumps(route, indent=2, ensure_ascii=False))
        
    except Exception as e:
        logger.error("Execution failed: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
