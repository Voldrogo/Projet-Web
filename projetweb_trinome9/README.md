# Application Web IRVE — Trinôme 9

Application web d'étude des données de la base nationale des Infrastructures de Recharge
pour Véhicules Électriques (IRVE). Projet Big Data / IA / Web — FISE3 2026.

---

## 1. Prérequis

| Logiciel | Rôle |
|----------|------|
| **PHP 7.4+** | serveur back-end |
| **MySQL / MariaDB** | base de données |
| **Python 3.8+** | scripts d'import et d'IA |

Bibliothèques Python nécessaires :

```bash
pip install pandas pymysql joblib scikit-learn
```

---

## 2. Installation de la base de données

### 2.1 Créer la base et les tables

Dans un terminal MySQL, ou via l'onglet **Importer** de phpMyAdmin, exécuter le script
de structure :

```bash
mysql -u root -p < sql/schema.sql
```

Cela crée la base et les 5 tables :
`departement`, `amenageur`, `operateur`, `station`, `point_de_charge`.


### 2.2 Remplir la base

Import SQL direct (si le serveur MySQL n'est pas accessible en local)**

Importer le fichier de données pré-généré via phpMyAdmin
(base sélectionnée → onglet **Importer** → fichier `sql/data.sql.gz` → **Exécuter**).

---

## 3. Configuration de la connexion

Modifier le fichier `config/db.php` avec les identifiants de votre base :

```php
$host = "127.0.0.1";   // adresse du serveur MySQL
$port = "3306";        // port MySQL
$dbname = "rdaoud28";  // nom de la base
$user = "root";        // utilisateur
$password = "";        // mot de passe
```

---

## 4. Configuration des scripts Python (prédictions IA)

Les fonctionnalités de prédiction appellent les scripts Python depuis PHP. Le chemin de
l'exécutable Python est défini dans les fichiers PHP concernés
(`php/api/predict_clusters.php`, etc.). Adapter si besoin :

```php
$python = "/opt/anaconda3/bin/python3";   // chemin de python3 sur la machine
```
---

## 5. Lancement de l'application

### En local (serveur PHP intégré)

```bash
# Depuis la racine du projet
php -S localhost:8000
```

Puis ouvrir dans le navigateur : **http://localhost:8000**

### Sur le serveur web

Déposer le dossier du projet dans le répertoire web du serveur et accéder à l'URL
correspondante (ex. `https://projets.isen-ouest.info/<dossier>/`).

---

## 6. Structure du projet

```
projetweb_trinome9/
├── index.html              Page d'accueil
├── config/
│   └── db.php              Connexion à la base (PDO)
├── php/api/               Interfaces client-serveur (endpoints)
│   ├── get_points_de_charge.php
│   ├── get_stations.php
│   ├── get_departements.php
│   ├── get_stats.php
│   ├── predict_clusters.php
│   ├── add_pdc.php
│   └── delete_pdc.php
├── pages/                Pages internes (visualisation, statistiques, clusters)
├── assets/
│   ├── css/style.css     Style commun (en-tête / pied de page)
│   ├── js/               Scripts front (un par page)
│   └── img/              Images
├── python/               Script d'import + scripts d'IA + modèles .pkl
├── sql/                  schema.sql (structure) + data.sql (données)
└── docs/                 Maquette, charte, MCD, interfaces, rapport
```

