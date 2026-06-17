<?php
// Test : vérifie la connexion et liste les tables de la base
require_once __DIR__ . "/../config/db.php";
header("Content-Type: application/json");

$tables = $pdo->query("SHOW TABLES")->fetchAll(PDO::FETCH_COLUMN);
echo json_encode([
    "connexion" => "OK",
    "base" => "irve_web",
    "tables" => $tables
], JSON_PRETTY_PRINT);
?>
