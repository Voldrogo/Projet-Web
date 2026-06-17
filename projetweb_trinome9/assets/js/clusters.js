const API = "../php/api/";

// Couleurs utilisees pour distinguer les clusters
const COULEURS = ["red", "blue", "green", "orange", "purple", "darkred",
                  "cadetblue", "darkgreen", "darkblue", "black"];

// Lance la prediction puis affiche les points colores par cluster sur la carte
function chargerClusters() {
  //chargement carte Leaflet
  const carte = L.map("carte").setView([46.6, 2.5], 6);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap"
  }).addTo(carte);

  //requete fetch qui retourne les points de charge avec leur cluster
  fetch(API + "predict_clusters.php")
    .then(reponse => reponse.json())
    .then(points => {
      document.querySelector("#message").textContent =
        points.length + " points de charge répartis par cluster :";
      points.forEach(p => {
        const couleur = COULEURS[p.cluster % COULEURS.length];
        const popup = `<b>Point de charge n°${p.id_pdc}</b><br>
          Station : ${p.nom_station}<br>
          Puissance : ${p.puissance_nominal} kW<br>
          Cluster : ${p.cluster}`;
        L.circleMarker([p.latitude, p.longitude], {
          radius: 6,
          color: couleur,
          fillColor: couleur,
          fillOpacity: 0.8
        }).addTo(carte).bindPopup(popup);
      });
    });
}

chargerClusters();
