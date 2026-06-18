<?php
//Supprime un point de charge de la base (CIR)
require_once __DIR__ . "/../../config/db.php";
header("Content-Type: application/json");

//On recupere les donnees (en JSON)
$data = json_decode(file_get_contents("php://input"), true);

//Verif du champ obligatoire
if (empty($data["id_pdc"])) {
    http_response_code(400);
    echo json_encode(["erreur" => "id_pdc est obligatoire"]);
    exit;
}

//Suppression du point de charge
$req = $pdo->prepare("DELETE FROM point_de_charge WHERE id_pdc = ?");
$req->execute([$data["id_pdc"]]);

//rowCount pour verifier que la ligne est bien suprimée 
if ($req->rowCount() === 0) {
    http_response_code(404);
    echo json_encode(["erreur" => "Point de charge introuvable"]);
    exit;
}

echo json_encode(["succes" => true]);
?>
