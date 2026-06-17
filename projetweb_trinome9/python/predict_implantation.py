"""
Script CLI – Besoin Client 3 : prédiction du type d'implantation
Usage :
  python predict_implantation.py --puissance_nominale 22.0 --nbre_pdc 4 --lat 48.85 --lon 2.35

Arguments obligatoires :
  --puissance_nominale  Puissance en kW (ex: 7.4, 22.0, 50.0, 150.0)
  --nbre_pdc            Nombre de points de charge (ex: 2)
  --lat                 Latitude  (ex: 48.8566)
  --lon                 Longitude (ex: 2.3522)

Arguments optionnels (défaut = 0/False) :
  --prise_ef            1 si prise type EF, sinon 0
  --prise_2             1 si prise type 2, sinon 0
  --prise_ccs           1 si prise combo CCS, sinon 0
  --prise_chademo       1 si prise CHAdeMO, sinon 0
  --prise_autre         1 si autre prise, sinon 0
  --paiement_acte       1 si paiement à l'acte, sinon 0
  --paiement_cb         1 si paiement CB, sinon 0
  --acces_reserve       1 si accès réservé, 0 si accès libre
"""
import argparse
import numpy as np
import joblib
import os

BASE = os.path.dirname(os.path.abspath(__file__))


def predict_implantation(features: list) -> str:
    model   = joblib.load(os.path.join(BASE, 'model_classification.pkl'))
    encoder = joblib.load(os.path.join(BASE, 'label_encoder_classif.pkl'))
    X = np.array([features])
    pred = model.predict(X)
    return encoder.inverse_transform(pred)[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prédit le type d'implantation d'une borne IRVE.")
    parser.add_argument('--puissance_nominale', type=float, required=True)
    parser.add_argument('--nbre_pdc',           type=int,   required=True)
    parser.add_argument('--lat',                type=float, required=True)
    parser.add_argument('--lon',                type=float, required=True)
    parser.add_argument('--prise_ef',           type=int,   default=0)
    parser.add_argument('--prise_2',            type=int,   default=1)
    parser.add_argument('--prise_ccs',          type=int,   default=0)
    parser.add_argument('--prise_chademo',      type=int,   default=0)
    parser.add_argument('--prise_autre',        type=int,   default=0)
    parser.add_argument('--paiement_acte',      type=int,   default=1)
    parser.add_argument('--paiement_cb',        type=int,   default=1)
    parser.add_argument('--acces_reserve',      type=int,   default=0)
    args = parser.parse_args()

    features = [
        args.puissance_nominale,
        args.nbre_pdc,
        args.lat,
        args.lon,
        args.prise_ef,
        args.prise_2,
        args.prise_ccs,
        args.prise_chademo,
        args.prise_autre,
        args.paiement_acte,
        args.paiement_cb,
        args.acces_reserve
    ]

    resultat = predict_implantation(features)
    print(f"Type d'implantation prédit : {resultat}")
