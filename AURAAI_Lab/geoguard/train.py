"""
AuraGeoGuard - Geographic POI Clustering & Routing
Advanced training pipeline for emergency facility location and routing
using K-Means clustering and nearest neighbor search for Durango, Mexico.

Author: AuraAI_Lab
Version: 1.0.0
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
        
        # Save
        self.save_artifacts(clusters, zones)
        
        logger.info("=" * 80)
        logger.info("TRAINING COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)


def main():
    """Main execution pipeline"""
    try:
        trainer = GeoGuardTrainer(CONFIG)
        trainer.train()
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error("Training failed: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
