"""
AuraGeoGuard - Geographic POI Clustering & Routing with Social Impact & AI Agent Architecture
Advanced training pipeline for emergency facility location and routing
using K-Means clustering and nearest neighbor search for Durango, Mexico.

Author: AuraAI_Lab
Version: 2.0.0
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
import joblib
import os
import json
import logging
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Importar módulos adicionales
from scipy.spatial import ConvexHull
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, request, jsonify

# Configuration
CONFIG = {
    'random_state': 42,
    'n_clusters': 8,  # Number of geographic zones
    'n_neighbors': 5,  # K nearest facilities
    'distance_metric': 'haversine',  # For lat/lon
    'cluster_algorithm': 'lloyd'  # CORREGIDO: 'auto' ya no es válido
}

# Paths
DATA_PATH = 'data/facilities.csv'
CLUSTERS_MODEL_PATH = 'models/geoguard_clusters.joblib'
NEIGHBORS_MODEL_PATH = 'models/geoguard_neighbors.joblib'
SCALER_PATH = 'models/geoguard_scaler.joblib'
FACILITIES_PATH = 'models/facilities_database.json'
ZONES_PATH = 'models/geographic_zones.json'
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


class GeoGuardTrainer:
    """Geographic clustering and routing system trainer"""
    
    def __init__(self, config):
        self.config = config
        self.kmeans_model = None
        self.nn_model = None
        self.scaler = None
        self.facilities_data = None
        self.metrics = {}
        
    def load_and_validate_data(self):
        """Load and validate facilities dataset"""
        logger.info("Loading facilities dataset from: %s", DATA_PATH)
        
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
        
        df = pd.read_csv(DATA_PATH)
        
        required_cols = ['nombre', 'tipo', 'latitud', 'longitud']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Dataset must contain columns: {required_cols}")
        
        # Validate coordinates
        if not df['latitud'].between(23.5, 25.0).all():
            logger.warning("Some latitudes outside Durango region (23.5-25.0)")
        if not df['longitud'].between(-105.5, -104.0).all():
            logger.warning("Some longitudes outside Durango region (-105.5 to -104.0)")
        
        # Clean data
        initial_size = len(df)
        df = df.drop_duplicates(subset=['nombre', 'latitud', 'longitud'])
        df = df.dropna(subset=required_cols)
        
        logger.info("Dataset loaded: %d facilities (removed %d duplicates/nulls)",
                   len(df), initial_size - len(df))
        logger.info("Facility types: %s", df['tipo'].unique().tolist())
        logger.info("Type distribution:\n%s", df['tipo'].value_counts().to_string())
        
        self.facilities_data = df
        return df
    
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate haversine distance between two points in kilometers
        For accurate geographic distance on Earth's surface
        """
        R = 6371  # Earth radius in kilometers
        
        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        delta_lat = np.radians(lat2 - lat1)
        delta_lon = np.radians(lon2 - lon1)
        
        a = np.sin(delta_lat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        
        return R * c
    
    def prepare_features(self, df):
        """Prepare features for clustering"""
        logger.info("Preparing geographic features...")
        
        # Use lat/lon as features
        X = df[['latitud', 'longitud']].values
        
        # Scale features for better clustering
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        logger.info("Features prepared: %d facilities, 2 dimensions", len(X))
        
        return X_scaled, X
    
    def train_clustering(self, X_scaled):
        """Train K-Means clustering model"""
        logger.info("Training K-Means clustering with %d clusters...", 
                   self.config['n_clusters'])
        
        self.kmeans_model = KMeans(
            n_clusters=self.config['n_clusters'],
            random_state=self.config['random_state'],
            n_init=10,
            max_iter=300,
            algorithm=self.config['cluster_algorithm']
        )
        
        clusters = self.kmeans_model.fit_predict(X_scaled)
        
        logger.info("Clustering completed")
        
        return clusters
    
    def train_nearest_neighbors(self, X):
        """Train Nearest Neighbors model for routing"""
        logger.info("Training Nearest Neighbors model with k=%d...",
                   self.config['n_neighbors'])
        
        # Use haversine metric for geographic coordinates
        # Note: NearestNeighbors expects radians for haversine
        X_radians = np.radians(X)
        
        self.nn_model = NearestNeighbors(
            n_neighbors=self.config['n_neighbors'],
            metric='haversine',
            algorithm='ball_tree'  # Efficient for haversine
        )
        
        self.nn_model.fit(X_radians)
        
        logger.info("Nearest Neighbors model trained")
    
    def evaluate_clustering(self, X_scaled, clusters):
        """Evaluate clustering quality"""
        logger.info("Evaluating clustering quality...")
        
        # Silhouette score (higher is better, range -1 to 1)
        silhouette = silhouette_score(X_scaled, clusters)
        
        # Davies-Bouldin index (lower is better)
        davies_bouldin = davies_bouldin_score(X_scaled, clusters)
        
        # Cluster size distribution
        unique, counts = np.unique(clusters, return_counts=True)
        cluster_sizes = dict(zip(unique.tolist(), counts.tolist()))
        
        self.metrics = {
            'timestamp': datetime.now().isoformat(),
            'n_facilities': int(len(X_scaled)),
            'n_clusters': int(self.config['n_clusters']),
            'silhouette_score': float(silhouette),
            'davies_bouldin_index': float(davies_bouldin),
            'cluster_sizes': cluster_sizes,
            'avg_cluster_size': float(np.mean(counts)),
            'min_cluster_size': int(np.min(counts)),
            'max_cluster_size': int(np.max(counts))
        }
        
        logger.info("CLUSTERING METRICS:")
        logger.info("  Silhouette Score: %.4f (higher is better)", silhouette)
        logger.info("  Davies-Bouldin Index: %.4f (lower is better)", davies_bouldin)
        logger.info("  Average cluster size: %.1f facilities", np.mean(counts))
        logger.info("  Cluster size range: %d - %d", np.min(counts), np.max(counts))
    
    def create_geographic_zones(self, clusters):
        """Create geographic zone descriptions"""
        logger.info("Creating geographic zone descriptions...")
        
        zones = {}
        
        for cluster_id in range(self.config['n_clusters']):
            cluster_facilities = self.facilities_data[clusters == cluster_id]
            
            zone_info = {
                'zone_id': int(cluster_id),
                'n_facilities': int(len(cluster_facilities)),
                'center_lat': float(cluster_facilities['latitud'].mean()),
                'center_lon': float(cluster_facilities['longitud'].mean()),
                'facilities': cluster_facilities[['nombre', 'tipo', 'latitud', 'longitud']].to_dict('records'),
                'bounds': {
                    'min_lat': float(cluster_facilities['latitud'].min()),
                    'max_lat': float(cluster_facilities['latitud'].max()),
                    'min_lon': float(cluster_facilities['longitud'].min()),
                    'max_lon': float(cluster_facilities['longitud'].max())
                }
            }
            
            zones[f'zone_{cluster_id}'] = zone_info
        
        logger.info("Geographic zones created: %d zones", len(zones))
        
        return zones
    
    def calculate_social_impact(self, zones):
        """Calcular indicadores de impacto social por zona"""
        logger.info("Calculando impacto social por zona...")
        
        for zone_id, zone in zones.items():
            # Simulación: suponemos densidad poblacional por zona (ajustable)
            population_density = np.random.randint(500, 5000)  # ej: hab/km²
            area_km2 = self.calculate_zone_area(zone['bounds'])
            total_population = int(population_density * area_km2)
            
            avg_distance_to_facility = self.calculate_avg_distance_to_nearest(zone['facilities'])
            
            zone['social_metrics'] = {
                'estimated_population': total_population,
                'population_density_per_km2': population_density,
                'avg_distance_to_nearest_facility_km': avg_distance_to_facility,
                'accessibility_index': 100 - (avg_distance_to_facility * 5),  # Escala 0-100
                'vulnerable_groups_served': ['Mujeres', 'Niños', 'Adultos Mayores'],  # Ejemplo
                'recommendation': "Zona con alta cobertura" if avg_distance_to_facility < 5 else "Requiere más centros"
            }
        
        return zones

    def calculate_zone_area(self, bounds):
        """Estimar área aproximada en km² usando haversine entre esquinas"""
        # Simplificado: usar rectángulo medio
        lat_diff = bounds['max_lat'] - bounds['min_lat']
        lon_diff = bounds['max_lon'] - bounds['min_lon']
        # Convertir diferencias a km
        km_per_deg_lat = 111.0
        km_per_deg_lon = 111.0 * np.cos(np.radians((bounds['min_lat'] + bounds['max_lat']) / 2))
        area = abs(lat_diff * km_per_deg_lat) * abs(lon_diff * km_per_deg_lon)
        return max(1.0, area)  # Evitar 0

    def calculate_avg_distance_to_nearest(self, facilities):
        """Calcular distancia promedio desde el centro de la zona a cada facility"""
        if len(facilities) == 0:
            return 0.0
        
        center_lat = np.mean([f['latitud'] for f in facilities])
        center_lon = np.mean([f['longitud'] for f in facilities])
        
        distances = []
        for f in facilities:
            d = self.haversine_distance(center_lat, center_lon, f['latitud'], f['longitud'])
            distances.append(d)
        
        return np.mean(distances)

    def generate_zone_polygons(self, zones):
        """Generar polígonos convexos para cada zona"""
        logger.info("Generando polígonos convexos por zona...")
        
        for zone_id, zone in zones.items():
            coords = [(f['latitud'], f['longitud']) for f in zone['facilities']]
            if len(coords) < 3:
                continue  # No se puede formar polígono
            
            try:
                hull = ConvexHull(coords)
                polygon = [coords[i] for i in hull.vertices]
                zone['polygon'] = polygon
                zone['area_km2'] = self.calculate_polygon_area(polygon)
            except:
                zone['polygon'] = None
                zone['area_km2'] = 0.0
        
        return zones

    def calculate_polygon_area(self, polygon):
        """Calcular área de polígono usando fórmula de Gauss"""
        if len(polygon) < 3:
            return 0.0
        
        x = [p[0] for p in polygon]
        y = [p[1] for p in polygon]
        
        # Convertir a km
        km_per_deg_lat = 111.0
        km_per_deg_lon = 111.0 * np.cos(np.radians(np.mean(x)))
        
        x_km = [xi * km_per_deg_lat for xi in x]
        y_km = [yi * km_per_deg_lon for yi in y]
        
        # Fórmula de Gauss
        n = len(x_km)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += x_km[i] * y_km[j] - x_km[j] * y_km[i]
        
        return abs(area) / 2.0

    def calculate_prevention_index(self, zones):
        """Calcular índice de prevención por zona"""
        logger.info("Calculando índice de prevención...")
        
        for zone_id, zone in zones.items():
            metrics = zone.get('social_metrics', {})
            coverage = metrics.get('accessibility_index', 0)
            density = metrics.get('population_density_per_km2', 0)
            facilities_count = len(zone['facilities'])
            
            # Índice de prevención: combinación de cobertura, densidad y cantidad de centros
            prevention_index = (coverage * 0.4) + (density * 0.3 / 1000) + (facilities_count * 0.3)
            prevention_index = min(100, max(0, prevention_index))  # Escalar 0-100
            
            zone['prevention_index'] = float(prevention_index)
            zone['risk_level'] = "Bajo" if prevention_index > 70 else ("Medio" if prevention_index > 40 else "Alto")
            
            logger.info(f"{zone_id}: Prevención Index = {prevention_index:.1f} | Riesgo: {zone['risk_level']}")
        
        return zones

    def generate_project_summary(self, zones):
        """Generar resumen ejecutivo del proyecto"""
        total_facilities = sum(len(zone['facilities']) for zone in zones.values())
        total_zones = len(zones)
        avg_facilities_per_zone = total_facilities / total_zones
        avg_accessibility = np.mean([z.get('social_metrics', {}).get('accessibility_index', 0) for z in zones.values()])
        high_risk_zones = sum(1 for z in zones.values() if z.get('risk_level') == "Alto")
        
        summary = {
            "project_name": "AuraGeoGuard",
            "region": "Durango, México",
            "total_facilities": int(total_facilities),
            "total_zones": int(total_zones),
            "avg_facilities_per_zone": float(avg_facilities_per_zone),
            "avg_accessibility_index": float(avg_accessibility),
            "high_risk_zones": int(high_risk_zones),
            "women_services_count": int(len(self.load_women_services())),
            "impact_statement": (
                "AuraGeoGuard optimiza la distribución de servicios de emergencia en Durango, "
                "priorizando la seguridad de grupos vulnerables, especialmente mujeres, "
                "y mejorando la prevención mediante análisis geoespacial y alertas inteligentes."
            ),
            "next_steps": [
                "Integrar con API de emergencias reales",
                "Desarrollar dashboard interactivo",
                "Incorporar datos en tiempo real",
                "Expandir a otras regiones"
            ]
        }
        
        logger.info("=" * 80)
        logger.info("RESUMEN EJECUTIVO DEL PROYECTO")
        logger.info("=" * 80)
        for k, v in summary.items():
            if isinstance(v, (int, float)):
                logger.info(f"{k}: {v}")
            elif isinstance(v, str):
                logger.info(f"{k}: {v[:100]}...")
            elif isinstance(v, list):
                logger.info(f"{k}: {len(v)} elementos")
        
        return summary

    def load_women_services(self):
        """Cargar servicios específicos para mujeres"""
        women_types = [
            'Refugio para Mujeres', 
            'Centro de Atención a la Violencia', 
            'Clínica de Salud Integral para Mujeres',
            'Centro de Apoyo Psicológico Femenino'
        ]
        
        women_facilities = self.facilities_data[
            self.facilities_data['tipo'].isin(women_types)
        ]
        
        logger.info("Servicios para mujeres encontrados: %d", len(women_facilities))
        return women_facilities

    def save_artifacts(self, clusters, zones):
        """Save all trained models and data"""
        logger.info("Saving model artifacts...")
        
        os.makedirs('models', exist_ok=True)
        
        # Save models
        joblib.dump(self.kmeans_model, CLUSTERS_MODEL_PATH, compress=3)
        joblib.dump(self.nn_model, NEIGHBORS_MODEL_PATH, compress=3)
        joblib.dump(self.scaler, SCALER_PATH, compress=3)
        
        logger.info("Models saved:")
        logger.info("  - %s", CLUSTERS_MODEL_PATH)
        logger.info("  - %s", NEIGHBORS_MODEL_PATH)
        logger.info("  - %s", SCALER_PATH)
        
        # Save facilities database with cluster assignments
        facilities_db = self.facilities_data.copy()
        facilities_db['cluster_id'] = clusters
        facilities_json = facilities_db.to_dict('records')
        
        with open(FACILITIES_PATH, 'w', encoding='utf-8') as f:
            json.dump(facilities_json, f, indent=2, ensure_ascii=False)
        logger.info("Facilities database saved: %s", FACILITIES_PATH)
        
        # Save geographic zones
        with open(ZONES_PATH, 'w', encoding='utf-8') as f:
            json.dump(zones, f, indent=2, ensure_ascii=False)
        logger.info("Geographic zones saved: %s", ZONES_PATH)
        
        # Save metrics
        with open(METRICS_PATH, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        logger.info("Metrics saved: %s", METRICS_PATH)
    
    def train(self):
        """Main training pipeline"""
        logger.info("=" * 80)
        logger.info("GEOGUARD TRAINING PIPELINE STARTED")
        logger.info("=" * 80)
        
        # Load data
        df = self.load_and_validate_data()
        
        # Prepare features
        X_scaled, X = self.prepare_features(df)
        
        # Train clustering
        clusters = self.train_clustering(X_scaled)
        
        # Train nearest neighbors
        self.train_nearest_neighbors(X)
        
        # Evaluate
        self.evaluate_clustering(X_scaled, clusters)
        
        # Create zones
        zones = self.create_geographic_zones(clusters)
        
        # Add social impact
        zones = self.calculate_social_impact(zones)
        
        # Add polygons
        zones = self.generate_zone_polygons(zones)
        
        # Add prevention index
        zones = self.calculate_prevention_index(zones)
        
        # Generate project summary
        summary = self.generate_project_summary(zones)
        
        # Save
        self.save_artifacts(clusters, zones)
        
        logger.info("=" * 80)
        logger.info("TRAINING COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)

        return zones, summary


class CallMetadataManager:
    def __init__(self, trainer):
        self.trainer = trainer
        self.calls_log = []
        self.call_id_counter = 0
    
    def log_emergency_call(self, lat, lon, emergency_type="General", priority=1):
        """Registrar una llamada de emergencia simulada"""
        self.call_id_counter += 1
        call_id = f"CALL_{self.call_id_counter:06d}"
        
        # Buscar centro más cercano
        nearest_facility = self.find_nearest_facility(lat, lon)
        distance_km = self.trainer.haversine_distance(lat, lon, nearest_facility['latitud'], nearest_facility['longitud'])
        
        # Estimar tiempo de respuesta (ej: 1 minuto por km)
        estimated_response_time_min = max(5, distance_km * 2)  # Mínimo 5 minutos
        
        call_data = {
            "call_id": call_id,
            "timestamp": datetime.now().isoformat(),
            "latitude": lat,
            "longitude": lon,
            "emergency_type": emergency_type,
            "priority": priority,
            "nearest_facility": nearest_facility,
            "distance_to_facility_km": round(distance_km, 2),
            "estimated_response_time_minutes": round(estimated_response_time_min, 1),
            "assigned_cluster": nearest_facility.get('cluster_id', -1),
            "status": "Pending"
        }
        
        self.calls_log.append(call_data)
        logger.info(f"[CALL] {call_id} registered at ({lat}, {lon}) → Nearest: {nearest_facility['nombre']} ({distance_km:.2f} km)")
        
        return call_data
    
    def find_nearest_facility(self, lat, lon):
        """Buscar el centro más cercano usando el modelo entrenado"""
        X_radians = np.radians([[lat, lon]])
        distances, indices = self.trainer.nn_model.kneighbors(X_radians)
        
        # Índice del más cercano
        idx = indices[0][0]
        facility = self.trainer.facilities_data.iloc[idx].to_dict()
        facility['cluster_id'] = self.trainer.facilities_data.iloc[idx]['cluster_id']
        return facility

    def log_women_emergency_call(self, lat, lon, priority=1):
        """Llamada de emergencia prioritaria para mujeres"""
        women_facilities = self.trainer.load_women_services()
        
        if len(women_facilities) == 0:
            logger.warning("No se encontraron servicios específicos para mujeres")
            return self.log_emergency_call(lat, lon, "Mujer (Sin Servicio Específico)", priority)
        
        # Calcular el más cercano entre servicios para mujeres
        X_radians = np.radians([[lat, lon]])
        women_coords = women_facilities[['latitud', 'longitud']].values
        women_radians = np.radians(women_coords)
        
        nn = NearestNeighbors(metric='haversine', algorithm='ball_tree')
        nn.fit(women_radians)
        distances, indices = nn.kneighbors(X_radians)
        
        idx = indices[0][0]
        nearest_women_facility = women_facilities.iloc[idx].to_dict()
        
        distance_km = self.trainer.haversine_distance(
            lat, lon, nearest_women_facility['latitud'], nearest_women_facility['longitud']
        )
        
        call_data = {
            "call_id": f"WOMEN_CALL_{self.call_id_counter:06d}",
            "timestamp": datetime.now().isoformat(),
            "latitude": lat,
            "longitude": lon,
            "emergency_type": "Violencia de Género",
            "priority": 3,  # Máxima prioridad
            "nearest_women_facility": nearest_women_facility,
            "distance_to_women_facility_km": round(distance_km, 2),
            "estimated_response_time_minutes": round(max(5, distance_km * 2), 1),
            "status": "Priority - Women's Safety"
        }
        
        self.calls_log.append(call_data)
        logger.info(f"[WOMEN CALL] Prioritario → {nearest_women_facility['nombre']} ({distance_km:.2f} km)")
        
        return call_data


class ParallelAgent:
    def __init__(self, call_manager):
        self.call_manager = call_manager
    
    def process_multiple_calls(self, calls_list):
        """Procesar múltiples llamadas en paralelo"""
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.call_manager.log_emergency_call, lat, lon, etype, prio)
                for lat, lon, etype, prio in calls_list
            ]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error("Error en llamada paralela: %s", str(e))
        
        logger.info(f"Procesadas {len(results)} llamadas en paralelo")
        return results


class HorizonArchitecture:
    def __init__(self, trainer, call_manager):
        self.trainer = trainer
        self.call_manager = call_manager
        self.horizon_1 = self.Horizon1(trainer, call_manager)
        self.horizon_2 = self.Horizon2(trainer, call_manager)
        self.horizon_3 = self.Horizon3(trainer, call_manager)
    
    class Horizon1:
        """Operacional: Respuesta en tiempo real a llamadas"""
        def __init__(self, trainer, call_manager):
            self.call_manager = call_manager
        
        def handle_call(self, lat, lon, emergency_type="General"):
            return self.call_manager.log_emergency_call(lat, lon, emergency_type)
    
    class Horizon2:
        """Analítico: Monitoreo, métricas, alertas"""
        def __init__(self, trainer, call_manager):
            self.trainer = trainer
            self.call_manager = call_manager
        
        def generate_alerts(self):
            zones = self.trainer.create_geographic_zones(self.trainer.kmeans_model.labels_)
            zones = self.trainer.calculate_social_impact(zones)
            zones = self.trainer.calculate_prevention_index(zones)
            
            alerts = []
            for zone_id, zone in zones.items():
                if zone.get('risk_level') == "Alto":
                    alerts.append({
                        "zone": zone_id,
                        "message": f"Zona {zone_id} con alto riesgo. Accesibilidad: {zone['social_metrics']['accessibility_index']:.1f}%",
                        "action": "Asignar más recursos"
                    })
            
            return alerts
    
    class Horizon3:
        """Estratégico: Planificación, políticas públicas, expansión"""
        def __init__(self, trainer, call_manager):
            self.trainer = trainer
        
        def recommend_new_facilities(self):
            """Recomendar ubicaciones óptimas para nuevos centros"""
            # Basado en zonas con bajo índice de prevención
            zones = self.trainer.create_geographic_zones(self.trainer.kmeans_model.labels_)
            zones = self.trainer.calculate_prevention_index(zones)
            
            low_prevention_zones = [
                (zid, z) for zid, z in zones.items() 
                if z.get('prevention_index', 0) < 50
            ]
            
            recommendations = []
            for zone_id, zone in low_prevention_zones:
                center_lat = zone['center_lat']
                center_lon = zone['center_lon']
                recommendations.append({
                    "zone": zone_id,
                    "recommended_location": {"lat": center_lat, "lon": center_lon},
                    "reason": f"Bajo índice de prevención: {zone['prevention_index']:.1f}",
                    "priority": "Alta"
                })
            
            return recommendations


class ScenarioSimulator:
    def __init__(self, horizon_architecture):
        self.horizon_architecture = horizon_architecture
    
    def simulate_gender_violence_scenario(self):
        """Simular emergencia de violencia de género"""
        logger.info("🚀 ESCENARIO: Violencia de Género en Zona Urbana")
        
        # Llamada de emergencia
        call = self.horizon_architecture.horizon_1.handle_call(
            lat=24.0, lon=-104.5, emergency_type="Violencia de Género"
        )
        
        # Alerta analítica
        alerts = self.horizon_architecture.horizon_2.generate_alerts()
        logger.info(" Alertas generadas: %d", len(alerts))
        
        # Recomendación estratégica
        recs = self.horizon_architecture.horizon_3.recommend_new_facilities()
        logger.info(" Recomendaciones estratégicas: %d", len(recs))
        
        return {
            "scenario": "Gender Violence",
            "call": call,
            "alerts": alerts,
            "recommendations": recs
        }

    def simulate_mass_accident_scenario(self):
        """Simular accidente masivo en carretera"""
        logger.info("🚗 ESCENARIO: Accidente Masivo en Carretera")
        
        # Simular 5 llamadas simultáneas
        calls = [
            (24.1, -104.6, "Accidente Vehicular", 2),
            (24.11, -104.59, "Herido Grave", 3),
            (24.09, -104.61, "Atropello", 2),
            (24.1, -104.6, "Incendio Vehículo", 2),
            (24.095, -104.605, "Pánico Colectivo", 1)
        ]
        
        parallel_agent = ParallelAgent(self.horizon_architecture.call_manager)
        results = parallel_agent.process_multiple_calls(calls)
        
        logger.info("✅ %d llamadas procesadas en paralelo", len(results))
        
        return {
            "scenario": "Mass Accident",
            "calls_processed": len(results),
            "results": results
        }


# ========== FLASK API ==========

app = Flask(__name__)

# Global instances
trainer = None
call_manager = None
horizon = None
simulator = None

@app.before_first_request
def initialize_system():
    global trainer, call_manager, horizon, simulator
    
    logger.info("Inicializando sistema AuraGeoGuard...")
    trainer = GeoGuardTrainer(CONFIG)
    zones, summary = trainer.train()
    
    call_manager = CallMetadataManager(trainer)
    horizon = HorizonArchitecture(trainer, call_manager)
    simulator = ScenarioSimulator(horizon)
    
    logger.info("Sistema inicializado correctamente.")

@app.route('/api/call', methods=['POST'])
def emergency_call():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')
    etype = data.get('type', 'General')
    priority = data.get('priority', 1)
    
    if lat is None or lon is None:
        return jsonify({"error": "Latitud y longitud requeridas"}), 400
    
    call = call_manager.log_emergency_call(lat, lon, etype, priority)
    return jsonify(call)

@app.route('/api/call/women', methods=['POST'])
def women_emergency_call():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')
    priority = data.get('priority', 1)
    
    if lat is None or lon is None:
        return jsonify({"error": "Latitud y longitud requeridas"}), 400
    
    call = call_manager.log_women_emergency_call(lat, lon, priority)
    return jsonify(call)

@app.route('/api/scenario/gender-violence', methods=['GET'])
def gender_violence_scenario():
    result = simulator.simulate_gender_violence_scenario()
    return jsonify(result)

@app.route('/api/scenario/mass-accident', methods=['GET'])
def mass_accident_scenario():
    result = simulator.simulate_mass_accident_scenario()
    return jsonify(result)

@app.route('/api/summary', methods=['GET'])
def project_summary():
    zones = trainer.create_geographic_zones(trainer.kmeans_model.labels_)
    zones = trainer.calculate_social_impact(zones)
    zones = trainer.calculate_prevention_index(zones)
    summary = trainer.generate_project_summary(zones)
    return jsonify(summary)

@app.route('/api/zones', methods=['GET'])
def get_zones():
    zones = trainer.create_geographic_zones(trainer.kmeans_model.labels_)
    zones = trainer.calculate_social_impact(zones)
    zones = trainer.calculate_prevention_index(zones)
    return jsonify(zones)

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    alerts = horizon.horizon_2.generate_alerts()
    return jsonify(alerts)

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    recs = horizon.horizon_3.recommend_new_facilities()
    return jsonify(recs)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "project": "AuraGeoGuard",
        "version": "2.0.0",
        "region": "Durango, México",
        "facilities": len(trainer.facilities_data) if trainer else 0,
        "clusters": CONFIG['n_clusters'],
        "last_trained": trainer.metrics.get('timestamp', 'N/A') if trainer else 'Not trained'
    })


def main():
    """Main execution pipeline"""
    try:
        # Entrenar el sistema
        trainer = GeoGuardTrainer(CONFIG)
        zones, summary = trainer.train()
        
        # Iniciar API
        logger.info(" Iniciando API Flask en http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        logger.error("Training failed: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()