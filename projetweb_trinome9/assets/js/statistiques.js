const API = "../php/api/";

// Remplit le menu deroulant avec les departements
function chargerDepartements() {
  //requete fetch qui retourne les departement 
  fetch(API + "get_departements.php")
    //convertie la réponse en json 
    .then(reponse => reponse.json())
    //traitement des données ( définission nom + option )
    .then(departements => {
      const select = document.querySelector("#select-dep");
      //parcours la liste de departement 
      departements.forEach(d => {
        const option = document.createElement("option");
        option.value = d.code_departement;
        option.textContent = d.nom_departement;
        select.appendChild(option);
      });
    });
}

//Recupere et affiche les statistiques du departement choisi
function chargerStats(dep) {
  //requete fetch qui retourne les departement 
  fetch(API + "get_stats.php?dep=" + dep)
    .then(reponse => reponse.json())
    .then(stats => {
      //affichage des différentes statistiques dans le html
      document.querySelector("#zone-stats").style.display = "block";
      document.querySelector("#stat-stations").textContent = stats.nb_stations;
      document.querySelector("#stat-pdc").textContent = stats.nb_points_de_charge;
      document.querySelector("#stat-puissance").textContent = stats.puissance_moyenne;
      //génère le graphique camembert
      afficherGraphique(stats.repartition_implantation);
    });
}

// Affiche la repartition par implantation en camembert (Plotly) ( fait avec l'ia )
function afficherGraphique(repartition) {
  const labels = Object.keys(repartition);
  const valeurs = Object.values(repartition);

  Plotly.newPlot("graphique-implantation", [{
    labels: labels,
    values: valeurs,
    type: "pie"
  }], {
    title: "Répartition des stations par type d'implantation"
  });
}

// Rechargement quand changement de departement 
document.querySelector("#select-dep").addEventListener("change", e => {
  if (e.target.value) chargerStats(e.target.value);
});

chargerDepartements();
