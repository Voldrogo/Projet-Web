const API = "../php/api/";

const PAR_PAGE = 50;
let tousLesPoints = [];
let pointsAffiches = [];   // points apres filtrage
let pageActuelle = 1;

// Recupere tous les points de charge puis affiche la 1re page
function chargerTableau() {
  fetch(API + "get_points_de_charge.php")
    .then(reponse => reponse.json())
    .then(points => {
      tousLesPoints = points;
      pointsAffiches = points;
      remplirSuggestions();
      afficherPage(1);
    });
}

// Remplit la liste de suggestions (completion auto) avec les noms de station
function remplirSuggestions() {
  const noms = [...new Set(tousLesPoints.map(p => p.nom_station))];
  const liste = document.querySelector("#liste-stations");
  noms.forEach(nom => {
    const option = document.createElement("option");
    option.value = nom;
    liste.appendChild(option);
  });
}

// Filtre le tableau selon le texte saisi (nom de station)
function filtrer() {
  const texte = document.querySelector("#filtre-station").value.toLowerCase();
  pointsAffiches = tousLesPoints.filter(p => p.nom_station.toLowerCase().includes(texte));
  afficherPage(1);
}

// Affiche les 50 lignes de la page demandee
function afficherPage(numero) {
  pageActuelle = numero;
  const debut = (numero - 1) * PAR_PAGE;
  const corps = document.querySelector("#tableau-pdc tbody");
  corps.innerHTML = "";
  pointsAffiches.slice(debut, debut + PAR_PAGE).forEach(p => {
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

  // Met a jour le compteur et les boutons
  const nbPages = Math.ceil(pointsAffiches.length / PAR_PAGE);
  document.querySelector("#info-page").textContent = `Page ${pageActuelle} / ${nbPages}`;
  document.querySelector("#btn-prec").disabled = (pageActuelle === 1);
  document.querySelector("#btn-suiv").disabled = (pageActuelle === nbPages);
}

// Boutons precedent / suivant
function pagePrecedente() {
  if (pageActuelle > 1) afficherPage(pageActuelle - 1);
}
function pageSuivante() {
  if (pageActuelle < Math.ceil(pointsAffiches.length / PAR_PAGE)) afficherPage(pageActuelle + 1);
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
