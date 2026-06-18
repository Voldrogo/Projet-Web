<?php
// Renvoie la liste des departements qui ont au moins une station (pour le menu deroulant)
require_once __DIR__ . "/../../config/db.php";
header("Content-Type: application/json");

#requète sql 
$sql = "SELECT DISTINCT d.code_departement, d.nom_departement
        FROM departement d
        JOIN station s ON s.code_departement = d.code_departement
        ORDER BY d.nom_departement";

#exécute la requete et recupère tout sous forme de tableau
$departements = $pdo->query($sql)->fetchAll(PDO::FETCH_ASSOC);
#transforme le tableau en json
echo json_encode($departements);
?>
