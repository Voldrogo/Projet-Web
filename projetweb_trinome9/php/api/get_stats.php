<?php
// Renvoie 4 statistiques sur les stations d'un departement donne
require_once __DIR__ . "/../../config/db.php";
header("Content-Type: application/json");

// On recupere le code du departement demande + vérif pas d'érreur 
$dep = $_GET["dep"] ?? "";
if ($dep === "") {
    http_response_code(400);
    echo json_encode(["erreur" => "Parametre dep manquant"]);
    exit;
}

// Stat 1 : nombre de stations
#préparation de la requète
$nbStations = $pdo->prepare("SELECT COUNT(*) FROM station WHERE code_departement = ?");
#exécusion de la requete
$nbStations->execute([$dep]);
#passe la requete en une valeur numérique
$nbStations = (int) $nbStations->fetchColumn();




// Stat 2 : nombre de points de charge
#préparation de la requète
$nbPdc = $pdo->prepare("SELECT COUNT(*) FROM point_de_charge p
                        JOIN station s ON p.id_station = s.id_station
                        WHERE s.code_departement = ?");
#exécusion de la requete
$nbPdc->execute([$dep]);
#passe la requete en une valeur numérique 
$nbPdc = (int) $nbPdc->fetchColumn();




// Stat 3 : puissance nominale moyenne des points de charge
#préparation de la requète
$puissance = $pdo->prepare("SELECT ROUND(AVG(p.puissance_nominal), 1) FROM point_de_charge p
                            JOIN station s ON p.id_station = s.id_station
                            WHERE s.code_departement = ?");
#exécusion de la requete
$puissance->execute([$dep]);
#passe la requete en une valeur numérique
$puissanceMoyenne = (float) $puissance->fetchColumn();





// Stat 4 : repartition des stations par type d'implantation
#préparation de la requète
$implantation = $pdo->prepare("SELECT implantation_station, COUNT(*) AS nb
                               FROM station WHERE code_departement = ?
                               GROUP BY implantation_station");
#exécusion de la requete
$implantation->execute([$dep]);
#passe la requete en une valeur numérique
$repartition = $implantation->fetchAll(PDO::FETCH_KEY_PAIR);


#renvoie les 4 statistiques sous forme de json
echo json_encode([
    "nb_stations" => $nbStations,
    "nb_points_de_charge" => $nbPdc,
    "puissance_moyenne" => $puissanceMoyenne,
    "repartition_implantation" => $repartition

]);
?>
