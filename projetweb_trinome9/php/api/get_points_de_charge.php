<?php
// Renvoie tous les points de charge avec le nom de leur station (pour le tableau)
require_once __DIR__ . "/../../config/db.php";
header("Content-Type: application/json");

$sql = "SELECT p.id_pdc, p.id_pdc_itinerance, p.puissance_nominal,
               p.prise_type_2, p.prise_type_combo_ccs, p.gratuit, p.paiement_cb,
               s.nom_station
        FROM point_de_charge p
        JOIN station s ON p.id_station = s.id_station
        ORDER BY p.id_pdc";


#exécute la requete et recupère tout sous forme de tableau
$points = $pdo->query($sql)->fetchAll(PDO::FETCH_ASSOC);
#transforme le tableau en json
echo json_encode($points);
?>
