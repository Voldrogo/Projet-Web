<?php
// Renvoie toutes les stations avec leurs coordonnees (pour la carte)
require_once __DIR__ . "/../../config/db.php";
header("Content-Type: application/json");

#requète sql 
$sql = "SELECT id_station, nom_station, adresse_station, implantation_station,
               consolidated_commune, nbre_pdc, longitude, latitude
        FROM station
        WHERE longitude IS NOT NULL AND latitude IS NOT NULL
        ORDER BY id_station";

#exécute la requete et recupère tout sous forme de tableau
$stations = $pdo->query($sql)->fetchAll(PDO::FETCH_ASSOC);
#transforme le tableau en json
echo json_encode($stations);
?>
