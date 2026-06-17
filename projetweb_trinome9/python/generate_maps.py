"""
Script BC1 – Génération des cartes IRVE
Usage : python generate_maps.py

Génère deux fichiers HTML :
  - carte_implantation.html  : carte interactive par type d'implantation
  - heatmap_densite.html     : heatmap de densité spatiale

Le fichier export_IA.csv doit être dans le même dossier.
"""
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
import os

BASE = os.path.dirname(os.path.abspath(__file__))
CSV  = os.path.join(BASE, 'export_IA.csv')


def load_and_clean():
    df = pd.read_csv(CSV, low_memory=False)
    cols = ['consolidated_latitude', 'consolidated_longitude',
            'implantation_station', 'puissance_nominale']
    df_map = df[cols].dropna()
    df_map = df_map[
        (df_map['consolidated_latitude']  >= 41) & (df_map['consolidated_latitude']  <= 52) &
        (df_map['consolidated_longitude'] >= -6) & (df_map['consolidated_longitude'] <= 10) &
        (df_map['puissance_nominale'] <= 400)
    ]
    return df_map


def generate_implantation_map(df_map):
    COLOR_MAP = {
        'Voirie'                              : 'blue',
        'Parking public'                      : 'green',
        'Parking privé à usage public'        : 'orange',
        'Parking privé réservé à la clientèle': 'red',
        'Station dédiée à la recharge rapide' : 'purple',
    }
    carte = folium.Map(location=[46.8, 2.3], zoom_start=6)
    cluster_layer = MarkerCluster(name='Bornes IRVE').add_to(carte)

    for _, row in df_map.iterrows():
        folium.CircleMarker(
            location=[row['consolidated_latitude'], row['consolidated_longitude']],
            radius=4,
            color=COLOR_MAP.get(row['implantation_station'], 'gray'),
            fill=True, fill_opacity=0.7,
            popup=f"{row['implantation_station']} — {row['puissance_nominale']} kW"
        ).add_to(cluster_layer)

    legend_html = """
    <div style="position:fixed;bottom:30px;left:30px;z-index:9999;background:white;
                padding:10px;border-radius:5px;border:1px solid #ccc;font-size:13px;">
    <b>Type d'implantation</b><br>
    <i style="background:blue;width:12px;height:12px;display:inline-block"></i> Voirie<br>
    <i style="background:green;width:12px;height:12px;display:inline-block"></i> Parking public<br>
    <i style="background:orange;width:12px;height:12px;display:inline-block"></i> Parking privé public<br>
    <i style="background:red;width:12px;height:12px;display:inline-block"></i> Parking réservé clientèle<br>
    <i style="background:purple;width:12px;height:12px;display:inline-block"></i> Station dédiée rapide
    </div>"""
    carte.get_root().html.add_child(folium.Element(legend_html))
    out = os.path.join(BASE, 'carte_implantation.html')
    carte.save(out)
    print(f'Carte sauvegardée : {out}')


def generate_heatmap(df_map):
    heatmap_carte = folium.Map(location=[46.8, 2.3], zoom_start=6)
    heat_data = df_map[['consolidated_latitude', 'consolidated_longitude']].values.tolist()
    HeatMap(heat_data, radius=10, blur=15, max_zoom=1).add_to(heatmap_carte)
    out = os.path.join(BASE, 'heatmap_densite.html')
    heatmap_carte.save(out)
    print(f'Heatmap sauvegardée : {out}')


if __name__ == '__main__':
    print('Chargement des données...')
    df_map = load_and_clean()
    print(f'{len(df_map)} bornes chargées.')
    generate_implantation_map(df_map)
    generate_heatmap(df_map)
    print('Terminé.')
