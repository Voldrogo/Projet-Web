"""
Version batch de predict_cluster.py : predit le cluster de plusieurs points en un seul appel.
Lit une liste [[lat,lon], ...] en JSON sur l'entree standard,
renvoie la liste des clusters en JSON sur la sortie standard.
"""
import sys
import json
import os
import joblib

BASE = os.path.dirname(__file__)

# On charge le modele une seule fois (pas a chaque point)
scaler = joblib.load(os.path.join(BASE, "scaler_clustering.pkl"))
model = joblib.load(os.path.join(BASE, "model_clustering.pkl"))

points = json.load(sys.stdin)
X = scaler.transform(points)
clusters = model.predict(X).tolist()

print(json.dumps([int(c) for c in clusters]))
