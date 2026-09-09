# BLOC 1 : Projet Data Engineering - Plateforme d'aide à l'implantation Retail en Île-de-France

## Présentation du projet

Ce projet a été réalisé dans le cadre du Bloc de compétences **« Collecter, Transformer et Sécuriser des Données »**.

L'objectif est de concevoir une chaîne de traitement de données entièrement automatisée permettant de collecter, transformer, stocker et sécuriser des données territoriales afin d'aider à l'identification des zones les plus attractives pour l'ouverture d'un commerce de prêt-à-porter en Île-de-France.

L'ensemble du pipeline est orchestré avec **Apache Airflow**, les données sont stockées dans **PostgreSQL/PostGIS**, puis mises à disposition des Data Analysts et Data Scientists.

---

# Problématique

L'ouverture d'un nouveau point de vente représente un investissement important.

Le choix d'un mauvais emplacement peut entraîner :

- une faible fréquentation ;
- une concurrence trop importante ;
- une inadéquation avec la population locale ;
- un chiffre d'affaires insuffisant.

L'objectif de ce projet est donc de répondre à la problématique suivante :

> Comment exploiter des données démographiques, socio-économiques, territoriales et concurrentielles afin d'identifier les zones les plus attractives pour l'implantation d'un nouveau commerce en Île-de-France ?

---

# Objectifs

Le pipeline développé permet de :

- automatiser la collecte de données ;
- centraliser plusieurs sources Open Data ;
- nettoyer et transformer les données ;
- construire une base PostgreSQL cohérente ;
- mettre les données à disposition des équipes Data ;
- garantir la sécurité et l'intégrité des données.

---

# Structure du projet

Le projet est organisé selon une architecture modulaire afin de séparer les différentes étapes du pipeline ETL.

```text
automation/
│
├── dags/
│   ├── dag_retail_idf.py              # Définition du pipeline Airflow
│   └── __pycache__/                   # Fichiers compilés Python (ignorés par Git)
│
├── plugins/                           # Extensions Airflow
│   ├── .gitkeep 
|
├── collecte_donnees.ipynb             # Extraction des données (API, Open Data)
├── stockage_intermediaire_donnees.ipynb   # Nettoyage et stockage des données brutes                                 
├── transformation_stockage_final.ipynb  # Transformation et chargement PostgreSQL
│                                     
├── docker-compose.yaml                # Déploiement des services Docker
├── requirements.txt                   # Dépendances Python
├── README.md                          # Documentation du projet
└── .env                               # Variables d'environnement (non versionné)
```

### Description des principaux composants

| Élément | Description |
|----------|-------------|
| `collecte_donnees.ipynb` | Extraction automatisée des données depuis les API et les sources Open Data. |
| `stockage_intermédiaire_donnees.ipynb` | Nettoyage, validation et stockage des données intermédiaires. |
| `transformation_stockage_final.ipynb` | Transformation des jeux de données et chargement des tables finales dans PostgreSQL. |
| `dag_retail_idf.py` | Orchestration complète du pipeline avec Apache Airflow. |
| `docker-compose.yaml` | Déploiement des conteneurs nécessaires au fonctionnement de la plateforme. |
| `requirements.txt` | Liste des bibliothèques Python nécessaires à l'exécution du projet. |



# Architecture technique

Le projet repose sur une architecture Data Engineering composée des briques suivantes :

- API INSEE (MELoDI)
- Open Data (data.gouv.fr)
- OpenStreetMap
- Scripts Python
- Apache Airflow
- Docker
- PostgreSQL / PostGIS
- Pandas
- SQLAlchemy
- DBeaver

Les traitements sont entièrement automatisés via un DAG Airflow exécuté selon une planification hebdomadaire.

---

# Sources de données

Les données proviennent exclusivement de sources publiques.

| Source | Type | Utilisation |
|--------|------|-------------|
| API INSEE MELoDI | API REST | Population, revenus, logements, équipements, emploi |
| Data.gouv.fr | API / Open Data | Données de mobilité et infrastructures |
| OpenStreetMap | API | Géolocalisation |
| Web Scraping | Python | Données concurrentielles (respect des CGU) |

---

# Jeux de données exploités

Les principaux jeux de données INSEE utilisés sont :

- DS_RP_POPULATION_PRINC
- DS_RP_LOGEMENT_PRINC
- DS_FILOSOFI_CC
- DS_BPE
- DS_FLORES_ECONOMIC_SPHERE
- DS_POPULATIONS_REFERENCE

Chaque jeu de données est transformé afin d'obtenir une structure tabulaire directement exploitable par les équipes Data.

---

# Pipeline ETL

Le pipeline suit une architecture ETL classique.

## Extraction

Les données sont collectées :

- via des API REST ;
- via des requêtes SQL ;
- via des scripts de Web Scraping ;
- via des jeux Open Data.

## Transformation

Les traitements réalisés comprennent notamment :

- nettoyage des données ;
- suppression des doublons ;
- renommage des variables ;
- transformation des codes INSEE en variables métiers ;
- agrégation ;
- pivot des tables ;
- harmonisation des types de données ;
- contrôle qualité.

Toutes les transformations sont réalisées avec **Pandas**.

## Chargement

Les données transformées sont injectées dans PostgreSQL via SQLAlchemy.

Les tables finales sont organisées par domaine métier :

- population ;
- logements ;
- revenus ;
- équipements ;
- emploi ;
- mobilité.

---

# Orchestration

L'ensemble du pipeline est orchestré avec Apache Airflow.

Le DAG réalise automatiquement les étapes suivantes :

1. Extraction des données.
2. Stockage des données brutes.
3. Transformation.
4. Chargement PostgreSQL.
5. Nettoyage des fichiers temporaires.

Chaque tâche est journalisée.

En cas d'échec :

- le DAG est interrompu ;
- les logs sont conservés ;
- une notification est envoyée automatiquement par e-mail.

En cas de succès :

- une notification par mail confirme le bon déroulement du pipeline.

---

# Modèle de données

La base PostgreSQL est organisée selon une approche relationnelle.

Les tables utilisent :

- Primary Keys
- Foreign Keys
- contraintes NOT NULL
- contraintes CHECK
- contraintes UNIQUE

Les variables sont normalisées afin de faciliter les jointures entre les différentes tables.

---

# Politique de sécurité

Une politique de sécurité a été définie afin de garantir :

- la confidentialité ;
- l'intégrité ;
- la disponibilité des données.

Les principales mesures mises en œuvre sont :

- authentification PostgreSQL ;
- séparation des rôles ;
- accès en lecture seule pour les analystes ;
- accès en écriture réservé au Data Engineer ;
- sauvegardes régulières ;
- chiffrement du volume de stockage ;
- Chiffrement des mots de passe dans un fichier .env;
- communication sécurisée via TLS.

Les données exploitées étant issues de l'Open Data, aucune donnée personnelle n'est traitée.

Le projet respecte ainsi les principes du RGPD.

---

# Gestion des rôles

Deux profils PostgreSQL ont été créés.

## Data Engineer

Autorisations :

- CREATE
- INSERT
- UPDATE
- DELETE
- ALTER
- DROP

Responsabilités :

- alimentation de la base ;
- maintenance du pipeline ;
- exécution des traitements ETL.

## Data Analyst / Data Scientist

Autorisations :

- SELECT uniquement sur les tables finales.

Responsabilités :

- analyses exploratoires ;
- visualisation ;
- modélisation.

La séparation des rôles garantit la protection des données contre les modifications accidentelles.

---

# Continuité de service

Afin d'assurer la disponibilité de la plateforme :

- les traitements sont conteneurisés avec Docker ;
- les bases sont sauvegardées régulièrement ;
- les scripts sont versionnés avec Git ;
- le pipeline peut être relancé automatiquement via Airflow.

Cette organisation garantit la reproductibilité complète de l'environnement.

---

# Technologies utilisées

| Domaine | Technologies |
|----------|--------------|
| Langage | Python |
| Base de données | PostgreSQL / PostGIS |
| Orchestration | Apache Airflow |
| Conteneurisation | Docker |
| Analyse | Pandas |
| Requêtes SQL | SQLAlchemy |
| IDE | VS Code |
| Administration BDD | DBeaver |
| Versionning | Git |

---

# Résultats obtenus

Le pipeline permet :

- la collecte automatisée des données ;
- leur transformation en tables métier ;
- leur chargement dans PostgreSQL ;
- leur mise à disposition des équipes Data ;
- une exécution planifiée et supervisée via Airflow.

L'ensemble du processus est reproductible, sécurisé et industrialisable.

---

# Perspectives

Les données produites pourront être utilisées pour :

- construire un score d'attractivité commerciale ;
- développer des modèles de Machine Learning ;
- recommander les meilleures communes d'implantation ;
- alimenter un tableau de bord décisionnel.

---


Projet réalisé dans le cadre du Bloc 1 du titre RNCP : **Ingénieur en Science des Données – spécialisation Data et IA**

Année universitaire : 2025–2026





# BLOC 2 : Projet Data Analyst - Plateforme d'aide à l'implantation Retail en Île-de-France

![Python](https://img.shields.io/badge/Python-3.12-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![PostGIS](https://img.shields.io/badge/PostGIS-Enabled-green)
![Tableau Public](https://img.shields.io/badge/Tableau_Public-Visualization-E97627)
![License](https://img.shields.io/badge/License-MIT-lightgrey)


## Objectif

Ce second bloc du projet prolonge le travail réalisé lors du Bloc 1, consacré à la collecte, au nettoyage et à la structuration des données Open Data.

L'objectif est de transformer les données consolidées en indicateurs d'aide à la décision afin d'identifier les communes franciliennes présentant un potentiel intéressant pour l'implantation d'un nouveau commerce.

Le projet couvre l'ensemble de la chaîne analytique :

- consolidation des données issues de PostgreSQL ;
- calcul d'indicateurs métiers avec Python/Pandas ;
- analyses statistiques ;
- validation d'hypothèses ;
- création d'un tableau de bord interactif sous Tableau Public.

---

## Technologies utilisées

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib
- PostgreSQL
- PostGIS
- SQLAlchemy
- Tableau Public

---

## Architecture du projet

L'ensemble des analyses se trouvent dans le fichier : `analyse_valorisation_donnees.ipynb`



---

## Indicateurs calculés

Les principaux indicateurs produits sont notamment :

### Démographie

- Population totale
- Répartition par tranche d'âge
- Evolution de population

### Activité économique

- Emplois pour 1 000 habitants
- Etablissements pour 1 000 habitants

### Commerce

- Nombre de commerces
- Densité commerciale
- Commerces pour 1 000 habitants
- Diversité commerciale

### Pouvoir d'achat

- Niveau de vie médian
- Taux de pauvreté
- Rapport interdécile D9/D1
- Indice de Gini

### Equipements

- Services de santé
- Infrastructures sportives
- Infrastructures de transport
- Commerces alimentaires

---

## Analyses statistiques

Le projet comporte plusieurs analyses statistiques :

- matrice de corrélation de Spearman ;
- tests de corrélation de Spearman ;
- visualisation des distributions ;
- interprétation des coefficients de corrélation ;
- validation ou rejet des hypothèses de travail.

Les analyses portent notamment sur :

- la relation entre la population et le nombre de commerces ;
- le lien entre le niveau de vie médian et la densité commerciale ;
- l'association entre les infrastructures de transport et les emplois.

---

## Dashboard

Le dashboard a été développé avec Tableau Public.

Il permet de visualiser :

- les principaux KPI ;
- une carte du niveau de vie médian par commune ;
- les communes les plus peuplées ;
- les emplois pour 1 000 habitants ;
- la répartition des commerces par catégorie.

Deux filtres interactifs sont disponibles :

- année de référence ;
- commune.


---

## Installation

Créer un environnement virtuel :

```bash
python -m venv .venv


# Auteur : 
Jessica SIGNE

Lien git : https://github.com/JessicaSigne/data_infrastructure_implantation_retail_idf.git