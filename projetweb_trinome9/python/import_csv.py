"""
Importe une partie des donnees du CSV IRVE dans la base MySQL irve_web.
Les amenageurs, operateurs et departements sont dedupliques ;
chaque station n'est inseree qu'une fois, chaque ligne du CSV devient un point de charge.
"""

import pandas as pd
import pymysql

# --- Configuration ---
CSV = "/Users/voldrogo/Desktop/projetia_trinome9/Besoin_Client_2/export_IA.csv"
LIMIT_ROWS = 10000   # nombre de lignes importees ("quelques donnees"), mettre None pour tout

DB = dict(host="127.0.0.1", user="root", password="", database="rdaoud28", charset="utf8mb4")

# Noms des departements (pour le menu deroulant des statistiques)
DEPARTEMENTS = {
    "01":"Ain","02":"Aisne","03":"Allier","04":"Alpes-de-Haute-Provence","05":"Hautes-Alpes",
    "06":"Alpes-Maritimes","07":"Ardeche","08":"Ardennes","09":"Ariege","10":"Aube","11":"Aude",
    "12":"Aveyron","13":"Bouches-du-Rhone","14":"Calvados","15":"Cantal","16":"Charente",
    "17":"Charente-Maritime","18":"Cher","19":"Correze","21":"Cote-d'Or","22":"Cotes-d'Armor",
    "23":"Creuse","24":"Dordogne","25":"Doubs","26":"Drome","27":"Eure","28":"Eure-et-Loir",
    "29":"Finistere","2A":"Corse-du-Sud","2B":"Haute-Corse","30":"Gard","31":"Haute-Garonne",
    "32":"Gers","33":"Gironde","34":"Herault","35":"Ille-et-Vilaine","36":"Indre",
    "37":"Indre-et-Loire","38":"Isere","39":"Jura","40":"Landes","41":"Loir-et-Cher","42":"Loire",
    "43":"Haute-Loire","44":"Loire-Atlantique","45":"Loiret","46":"Lot","47":"Lot-et-Garonne",
    "48":"Lozere","49":"Maine-et-Loire","50":"Manche","51":"Marne","52":"Haute-Marne","53":"Mayenne",
    "54":"Meurthe-et-Moselle","55":"Meuse","56":"Morbihan","57":"Moselle","58":"Nievre","59":"Nord",
    "60":"Oise","61":"Orne","62":"Pas-de-Calais","63":"Puy-de-Dome","64":"Pyrenees-Atlantiques",
    "65":"Hautes-Pyrenees","66":"Pyrenees-Orientales","67":"Bas-Rhin","68":"Haut-Rhin","69":"Rhone",
    "70":"Haute-Saone","71":"Saone-et-Loire","72":"Sarthe","73":"Savoie","74":"Haute-Savoie",
    "75":"Paris","76":"Seine-Maritime","77":"Seine-et-Marne","78":"Yvelines","79":"Deux-Sevres",
    "80":"Somme","81":"Tarn","82":"Tarn-et-Garonne","83":"Var","84":"Vaucluse","85":"Vendee",
    "86":"Vienne","87":"Haute-Vienne","88":"Vosges","89":"Yonne","90":"Territoire de Belfort",
    "91":"Essonne","92":"Hauts-de-Seine","93":"Seine-Saint-Denis","94":"Val-de-Marne",
    "95":"Val-d'Oise","971":"Guadeloupe","972":"Martinique","973":"Guyane","974":"La Reunion",
    "976":"Mayotte",
}


def bool01(v):
    return 1 if str(v).strip().lower() == "true" else 0

def txt(v, maxlen):
    if pd.isna(v):
        return ""
    return str(v)[:maxlen]

def num(v, default=0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default

def code_dep(insee):
    """Deduit le code departement depuis le code INSEE de la commune."""
    s = str(insee).strip()
    if s.startswith("97"):
        return s[:3]
    return s[:2]


df = pd.read_csv(CSV, low_memory=False)
if LIMIT_ROWS:
    df = df.head(LIMIT_ROWS)

conn = pymysql.connect(**DB)
cur = conn.cursor()

# On vide les tables avant import (re-execution propre)
cur.execute("SET FOREIGN_KEY_CHECKS=0")
for t in ["point_de_charge", "station", "amenageur", "operateur", "departement"]:
    cur.execute(f"TRUNCATE TABLE {t}")
cur.execute("SET FOREIGN_KEY_CHECKS=1")

amenageurs, operateurs, departements, stations = {}, {}, {}, {}

for _, r in df.iterrows():
    # --- departement ---
    code = code_dep(r["code_insee_commune"])
    if code and code not in departements:
        nom = DEPARTEMENTS.get(code, code)
        cur.execute("INSERT INTO departement VALUES (%s,%s)", (code, nom))
        departements[code] = True

    # --- amenageur (dedup sur nom + siren) ---
    cle_a = (txt(r["nom_amenageur"], 256), txt(r["siren_amenageur"], 16))
    if cle_a not in amenageurs:
        cur.execute(
            "INSERT INTO amenageur (nom_amenageur,siren_amenageur,contact_amenageur) VALUES (%s,%s,%s)",
            (cle_a[0], cle_a[1], txt(r["contact_amenageur"], 16)))
        amenageurs[cle_a] = cur.lastrowid

    # --- operateur (dedup sur nom + enseigne) ---
    cle_o = (txt(r["nom_operateur"], 256), txt(r["nom_enseigne"], 256))
    if cle_o not in operateurs:
        cur.execute(
            "INSERT INTO operateur (nom_operateur,contact_operateur,telephone_operateur,nom_enseigne) VALUES (%s,%s,%s,%s)",
            (cle_o[0], txt(r["contact_operateur"], 256), txt(r["telephone_operateur"], 32), cle_o[1]))
        operateurs[cle_o] = cur.lastrowid

    # --- station (dedup sur id_station_itinerance) ---
    sid = txt(r["id_station_itinerance"], 64)
    if sid and sid not in stations:
        cur.execute(
            """INSERT INTO station
            (id_station_itinerance,nom_station,implantation_station,adresse_station,
             code_insee_commune,consolidated_commune,consolidated_code_postal,longitude,latitude,
             nbre_pdc,horaires,condition_acces,accessibilite_pmr,date_maj,
             id_amenageur,id_operateur,code_departement)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (sid, txt(r["nom_station"], 128), txt(r["implantation_station"], 64),
             txt(r["adresse_station"], 256), txt(r["code_insee_commune"], 8),
             txt(r["consolidated_commune"], 126), txt(r["consolidated_code_postal"], 8),
             num(r["consolidated_longitude"]), num(r["consolidated_latitude"]),
             int(num(r["nbre_pdc"], 1)), txt(r["horaires"], 128), txt(r["condition_acces"], 64),
             txt(r["accessibilite_pmr"], 128), str(r["date_maj"])[:10] if not pd.isna(r["date_maj"]) else "2000-01-01",
             amenageurs[cle_a], operateurs[cle_o], code))
        stations[sid] = cur.lastrowid

    # --- point de charge (une ligne CSV = un PDC) ---
    if sid in stations:
        cur.execute(
            """INSERT INTO point_de_charge
            (id_pdc_itinerance,puissance_nominal,prise_type_ef,prise_type_2,prise_type_combo_ccs,
             prise_type_chademo,gratuit,paiement_acte,paiement_cb,date_mise_en_service,id_station)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (txt(r["id_pdc_itinerance"], 64), num(r["puissance_nominale"]),
             bool01(r["prise_type_ef"]), bool01(r["prise_type_2"]), bool01(r["prise_type_combo_ccs"]),
             bool01(r["prise_type_chademo"]), bool01(r["gratuit"]), bool01(r["paiement_acte"]),
             bool01(r["paiement_cb"]), txt(r["date_mise_en_service"], 64), stations[sid]))

conn.commit()

# --- Bilan ---
for t in ["departement", "amenageur", "operateur", "station", "point_de_charge"]:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    print(f"{t:18} : {cur.fetchone()[0]} lignes")

cur.close()
conn.close()
print("Import termine.")
