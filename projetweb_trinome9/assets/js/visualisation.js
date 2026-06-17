const API = "../php/api/";



// Remplit le tableau des points de charge
function chargerTableau() {
  //envoie requète fetch qui renvoie les points de charge puis convertie en js
  fetch(API + "get_points_de_charge.php")
    .then(reponse => reponse.json())
    //traite les donnée ( remplissage du tableau)
    .then(points => {
      const corps = document.querySelector("#tableau-pdc tbody");
      points.forEach(p => {
        const ligne = document.createElement("tr");
        ligne.innerHTML = `
          <td>${p.id_pdc}</td>
          <td>${p.nom_station}</td>
          <td>${p.puissance_nominal}</td>
          <td>${p.prise_type_2 == 1 ? "Oui" : "Non"}</td>
          <td>${p.prise_type_combo_ccs == 1 ? "Oui" : "Non"}</td>
          <td>${p.gratuit == 1 ? "Oui" : "Non"}</td>
          <td>${p.paiement_cb == 1 ? "Oui" : "Non"}</td>`;
        corps.appendChild(ligne);
      });
    });
}


// Affiche les stations sur la carte Leaflet
function chargerCarte() {
  //création de la carte Leaflet
  const carte = L.map("carte").setView([46.6, 2.5], 6);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap"
  }).addTo(carte);

  //récupère les points de charge 
  fetch(API + "get_stations.php")
    .then(reponse => reponse.json())
    .then(stations => {
      stations.forEach(s => {
        const popup = `<b>${s.nom_station}</b><br>
          ${s.adresse_station}<br>
          Implantation : ${s.implantation_station}<br>
          Nombre de bornes : ${s.nbre_pdc}`;
          //créer un marqueur pour chaque station et l'ajoute à la carte avec un popup
        L.marker([s.latitude, s.longitude]).addTo(carte).bindPopup(popup);
      });
    });
}

chargerTableau();
chargerCarte();
