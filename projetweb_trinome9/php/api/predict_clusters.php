<?php
// Predit le cluster de chaque point de charge via le script Python, met a jour la base
// et renvoie les points avec leurs coordonnees et leur cluster (pour la carte coloree).
require_once __DIR__ . "/../../config/db.php";
header("Content-Type: application/json");

$python = "/opt/anaconda3/bin/python3";
$script = __DIR__ . "/../../python/predict_cluster_batch.py";

// On recupere les points de charge avec les coordonnees et infos de leur station
$sql = "SELECT p.id_pdc, p.puissance_nominal, s.nom_station, s.latitude, s.longitude
        FROM point_de_charge p
        JOIN station s ON p.id_station = s.id_station
        WHERE s.latitude IS NOT NULL AND s.longitude IS NOT NULL";
$points = $pdo->query($sql)->fetchAll(PDO::FETCH_ASSOC);

// On prepare la liste [[lat,lon], ...] envoyee au script Python
$coords = array_map(fn($p) => [(float)$p["latitude"], (float)$p["longitude"]], $points);

// Appel du script Python : on lui envoie les coordonnees sur stdin, on lit les clusters sur stdout
$descripteurs = [0 => ["pipe", "r"], 1 => ["pipe", "w"], 2 => ["pipe", "w"]];
$process = proc_open("$python $script", $descripteurs, $tuyaux);
fwrite($tuyaux[0], json_encode($coords));
fclose($tuyaux[0]);
$sortie = stream_get_contents($tuyaux[1]);
fclose($tuyaux[1]);
proc_close($process);

$clusters = json_decode($sortie, true);
if ($clusters === null) {
    http_response_code(500);
    echo json_encode(["erreur" => "Echec du script Python"]);
    exit;
}

// Mise a jour de la base et construction de la reponse
$maj = $pdo->prepare("UPDATE point_de_charge SET cluster = ? WHERE id_pdc = ?");
$resultat = [];
foreach ($points as $i => $p) {
    $maj->execute([$clusters[$i], $p["id_pdc"]]);
    $resultat[] = [
        "id_pdc" => (int)$p["id_pdc"],
        "nom_station" => $p["nom_station"],
        "puissance_nominal" => $p["puissance_nominal"],
        "latitude" => (float)$p["latitude"],
        "longitude" => (float)$p["longitude"],
        "cluster" => $clusters[$i]
    ];
}

echo json_encode($resultat);
?>
