<?php
//Ajoute un nouveau point de charge dans la base (CIR)
require_once __DIR__ . "/../../config/db.php";
header("Content-Type: application/json");

//On recupere les donnees (en JSON)
$data = json_decode(file_get_contents("php://input"), true);

//Verif des champs obligatoires
if (empty($data["id_station"]) || !isset($data["puissance_nominal"])) {
    http_response_code(400);
    echo json_encode(["erreur" => "id_station et puissance_nominal sont obligatoires"]);
    exit;
}

//requete sql ajout de la ligne 
$sql = "INSERT INTO point_de_charge
        (id_pdc_itinerance, puissance_nominal, prise_type_ef, prise_type_2,
         prise_type_combo_ccs, prise_type_chademo, gratuit, paiement_acte,
         paiement_cb, date_mise_en_service, id_station)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)";

$req = $pdo->prepare($sql);
//exécution dans les bons champs
$req->execute([
    $data["id_pdc_itinerance"] ?? "",
    $data["puissance_nominal"],
    $data["prise_type_ef"] ?? 0,
    $data["prise_type_2"] ?? 0,
    $data["prise_type_combo_ccs"] ?? 0,
    $data["prise_type_chademo"] ?? 0,
    $data["gratuit"] ?? 0,
    $data["paiement_acte"] ?? 0,
    $data["paiement_cb"] ?? 0,
    $data["date_mise_en_service"] ?? "",
    $data["id_station"]
]);

echo json_encode(["succes" => true, "id_pdc" => (int) $pdo->lastInsertId()]);
?>
