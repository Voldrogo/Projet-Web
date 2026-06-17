<?php
// Connexion à la base de données MySQL via PDO
$host = "127.0.0.1";
$port = "3306";
$dbname = "irve_web";
$user = "root";
$password = "";

try {
    $pdo = new PDO(
        "mysql:host=$host;port=$port;dbname=$dbname;charset=utf8mb4",
        $user,
        $password,
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(["erreur" => "Connexion BDD impossible : " . $e->getMessage()]);
    exit;
}
?>
