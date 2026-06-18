-- Structure de la base IRVE (Trinome 9)
-- Cree la base et les 5 tables.

CREATE DATABASE IF NOT EXISTS rdaoud28 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE rdaoud28;


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `departement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departement` (
  `code_departement` varchar(4) NOT NULL,
  `nom_departement` varchar(32) NOT NULL,
  PRIMARY KEY (`code_departement`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `amenageur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `amenageur` (
  `id_amenageur` int(11) NOT NULL AUTO_INCREMENT,
  `nom_amenageur` varchar(256) NOT NULL,
  `siren_amenageur` varchar(16) NOT NULL,
  `contact_amenageur` varchar(16) NOT NULL,
  PRIMARY KEY (`id_amenageur`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `operateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operateur` (
  `id_operateur` int(11) NOT NULL AUTO_INCREMENT,
  `nom_operateur` varchar(256) NOT NULL,
  `contact_operateur` varchar(256) NOT NULL,
  `telephone_operateur` varchar(32) NOT NULL,
  `nom_enseigne` varchar(256) NOT NULL,
  PRIMARY KEY (`id_operateur`)
) ENGINE=InnoDB AUTO_INCREMENT=506 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `station` (
  `id_station` int(11) NOT NULL AUTO_INCREMENT,
  `id_station_itinerance` varchar(64) NOT NULL,
  `nom_station` varchar(128) NOT NULL,
  `implantation_station` varchar(64) NOT NULL,
  `adresse_station` varchar(256) NOT NULL,
  `code_insee_commune` varchar(8) NOT NULL,
  `consolidated_commune` varchar(126) NOT NULL,
  `consolidated_code_postal` varchar(8) NOT NULL,
  `longitude` decimal(10,6) DEFAULT NULL,
  `latitude` decimal(10,6) DEFAULT NULL,
  `nbre_pdc` int(11) NOT NULL,
  `horaires` varchar(128) NOT NULL,
  `condition_acces` varchar(64) NOT NULL,
  `accessibilite_pmr` varchar(128) NOT NULL,
  `date_maj` date NOT NULL,
  `id_amenageur` int(11) NOT NULL,
  `id_operateur` int(11) NOT NULL,
  `code_departement` varchar(4) NOT NULL,
  PRIMARY KEY (`id_station`),
  KEY `station_id_amenageur_FK` (`id_amenageur`),
  KEY `station_id_operateur_FK` (`id_operateur`),
  KEY `station_code_departement_FK` (`code_departement`),
  CONSTRAINT `station_code_departement_FK` FOREIGN KEY (`code_departement`) REFERENCES `departement` (`code_departement`),
  CONSTRAINT `station_id_amenageur_FK` FOREIGN KEY (`id_amenageur`) REFERENCES `amenageur` (`id_amenageur`),
  CONSTRAINT `station_id_operateur_FK` FOREIGN KEY (`id_operateur`) REFERENCES `operateur` (`id_operateur`)
) ENGINE=InnoDB AUTO_INCREMENT=3496 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `point_de_charge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `point_de_charge` (
  `id_pdc` int(11) NOT NULL AUTO_INCREMENT,
  `id_pdc_itinerance` varchar(64) NOT NULL,
  `puissance_nominal` decimal(10,2) NOT NULL,
  `prise_type_ef` tinyint(1) NOT NULL,
  `prise_type_2` tinyint(1) NOT NULL,
  `prise_type_combo_ccs` tinyint(1) NOT NULL,
  `prise_type_chademo` tinyint(1) NOT NULL,
  `gratuit` tinyint(1) NOT NULL,
  `paiement_acte` tinyint(1) NOT NULL,
  `paiement_cb` tinyint(1) NOT NULL,
  `date_mise_en_service` varchar(64) NOT NULL,
  `predicted_puissance` decimal(10,2) DEFAULT NULL,
  `cluster` int(11) DEFAULT NULL,
  `predicted_implantation` varchar(64) DEFAULT NULL,
  `id_station` int(11) NOT NULL,
  PRIMARY KEY (`id_pdc`),
  KEY `point_de_charge_id_station_FK` (`id_station`),
  CONSTRAINT `point_de_charge_id_station_FK` FOREIGN KEY (`id_station`) REFERENCES `station` (`id_station`)
) ENGINE=InnoDB AUTO_INCREMENT=10002 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

