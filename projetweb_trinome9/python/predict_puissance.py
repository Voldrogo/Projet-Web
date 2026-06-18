"""
Script CLI – Besoin Client 4 : classification de la vitesse de recharge
Usage :
  python predict_puissance.py --implantation "Voirie" --nbre_pdc 2 --lat 48.85 --lon 2.35

Sortie : Lente | Normale | Rapide | Ultra-rapide

Arguments obligatoires :
  --implantation  Type d'implantation (ex: "Voirie", "Parking public",
                  "Parking privé à usage public", "Station dédiée à la recharge rapide")
  --nbre_pdc      Nombre de points de charge (ex: 2)
  --lat           Latitude  (ex: 48.8566)
  --lon           Longitude (ex: 2.3522)

Arguments optionnels (défaut = 0) :
  --prise_ef      1 si prise type EF (domestique), sinon 0
  --prise_2       1 si prise type 2, sinon 0
  --prise_ccs     1 si prise combo CCS (recharge rapide), sinon 0
  --prise_chademo 1 si prise CHAdeMO (recharge rapide), sinon 0
  --prise_autre   1 si autre prise, sinon 0
  --paiement_acte 1 si paiement à l'acte, sinon 0
  --paiement_cb   1 si paiement CB, sinon 0
  --acces_reserve 1 si accès réservé, 0 si accès libre

Exemples :
  python predict_puissance.py --implantation "Voirie" --nbre_pdc 2 --lat 48.85 --lon 2.35 --prise_2 1
  -> Catégorie prédite : Normale

  python predict_puissance.py --implantation "Station dédiée à la recharge rapide" --nbre_pdc 4 --lat 47.0 --lon 2.0 --prise_ccs 1 --prise_chademo 1
  -> Catégorie prédite : Ultra-rapide
"""
import argparse
import numpy as np
import joblib
import os

BASE = os.path.dirname(os.path.abspath(__file__))


def predict_vitesse(features: list) -> str:
    model     = joblib.load(os.path.join(BASE, 'model_classification_bc4.pkl'))
    le_vitesse = joblib.load(os.path.join(BASE, 'label_encoder_vitesse.pkl'))
    X = np.array([features])
    pred = model.predict(X)
    return le_vitesse.inverse_transform(pred)[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prédit la catégorie de vitesse de recharge d'une borne IRVE."
    )
    parser.add_argument('--implantation',   type=str,   required=True)
    parser.add_argument('--nbre_pdc',       type=int,   required=True)
    parser.add_argument('--lat',            type=float, required=True)
    parser.add_argument('--lon',            type=float, required=True)
    parser.add_argument('--prise_ef',       type=int,   default=0)
    parser.add_argument('--prise_2',        type=int,   default=1)
    parser.add_argument('--prise_ccs',      type=int,   default=0)
    parser.add_argument('--prise_chademo',  type=int,   default=0)
    parser.add_argument('--prise_autre',    type=int,   default=0)
    parser.add_argument('--paiement_acte',  type=int,   default=1)
    parser.add_argument('--paiement_cb',    type=int,   default=1)
    parser.add_argument('--acces_reserve',  type=int,   default=0)
    args = parser.parse_args()

    le_implant = joblib.load(os.path.join(BASE, 'label_encoder_implant.pkl'))
    try:
        implantation_enc = int(le_implant.transform([args.implantation])[0])
    except ValueError:
        print(f"Valeur inconnue pour --implantation : '{args.implantation}'")
        print(f"Valeurs acceptées : {list(le_implant.classes_)}")
        exit(1)

    features = [
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
        args.acces_reserve,
        implantation_enc,
    ]

    resultat = predict_vitesse(features)
    print(f"Catégorie prédite : {resultat}")
