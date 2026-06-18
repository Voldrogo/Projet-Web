"""
Script CLI – Besoin Client 2 : prédiction du cluster géographique
Usage : python predict_cluster.py --lat 48.8566 --lon 2.3522
"""
import argparse
import numpy as np
import joblib
import os

BASE = os.path.dirname(__file__)


def predict_cluster(lat: float, lon: float) -> int:
    scaler = joblib.load(os.path.join(BASE, 'scaler_clustering.pkl'))
    model  = joblib.load(os.path.join(BASE, 'model_clustering.pkl'))
    X = scaler.transform([[lat, lon]])
    return int(model.predict(X)[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prédit le cluster géographique d\'une borne IRVE.')
    parser.add_argument('--lat', type=float, required=True, help='Latitude de la borne')
    parser.add_argument('--lon', type=float, required=True, help='Longitude de la borne')
    args = parser.parse_args()

    cluster = predict_cluster(args.lat, args.lon)
    print(f'Cluster associé : {cluster}')
