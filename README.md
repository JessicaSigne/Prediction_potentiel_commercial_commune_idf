# BLOC 5 : Projet Machine Learning - Plateforme prédictive d'aide à l'implantation Retail en Île-de-France

## Présentation du projet

Ce projet constitue le volet **Machine Learning** de la plateforme d'aide à l'implantation Retail en Île-de-France développée dans le cadre du titre **Ingénieur en Science des Données – spécialisation Data et IA**.

Après la collecte, la transformation et la valorisation des données territoriales réalisées dans les blocs précédents, l'objectif de ce bloc est de développer un **modèle prédictif capable d'estimer la dynamique commerciale future des communes franciliennes**.

Le projet vise ainsi à passer d'une analyse descriptive des territoires à une approche **prédictive et décisionnelle**, permettant d'identifier les communes présentant le meilleur potentiel pour l'implantation d'un nouveau commerce de prêt-à-porter.

La démarche repose sur :

* l'exploitation des données historiques des communes ;
* la création de variables explicatives territoriales ;
* la construction d'une variable cible liée à la dynamique commerciale ;
* l'analyse statistique des variables ;
* le traitement des valeurs manquantes et des valeurs atypiques ;
* l'entraînement et l'optimisation d'un modèle de Machine Learning ;
* l'évaluation des performances du modèle ;
* l'estimation de la dynamique commerciale future ;
* la construction d'un score d'opportunité ;
* le classement des communes ;
* la mise à disposition des résultats dans une application interactive ;
* le suivi des performances du modèle dans le temps ;
* la mise en place d'un cycle de réentraînement.

---

# Problématique

L'analyse descriptive permet d'identifier les caractéristiques actuelles d'une commune, mais elle ne permet pas nécessairement d'anticiper son évolution commerciale.

Une commune peut par exemple présenter :

* une population importante ;
* un niveau de vie élevé ;
* une forte concentration d'emplois ;
* une bonne accessibilité ;
* mais également une concurrence commerciale déjà importante.

À l'inverse, certaines communes peuvent présenter une évolution démographique et économique favorable tout en étant relativement peu équipées en commerces.

L'enjeu est donc d'identifier les territoires présentant un **potentiel commercial futur**, et non uniquement ceux qui sont actuellement les plus attractifs.

La problématique retenue est ainsi :

> **Comment exploiter les caractéristiques démographiques, économiques, sociales, territoriales et commerciales historiques afin de prédire la dynamique commerciale future des communes et d'identifier les territoires présentant le meilleur potentiel d'implantation ?**

---

# Objectifs

Le projet a pour objectifs de :

* construire une base de données communale exploitable pour le Machine Learning ;
* exploiter les données historiques disponibles ;
* identifier les variables explicatives pertinentes de la dynamique commerciale ;
* construire une variable cible permettant de mesurer l'évolution commerciale ;
* analyser les relations entre les variables explicatives et la cible ;
* traiter les valeurs manquantes ;
* identifier et traiter les valeurs atypiques ;
* entraîner plusieurs modèles de régression ;
* sélectionner et optimiser le modèle le plus performant ;
* prédire la dynamique commerciale future ;
* construire un indicateur de potentiel commercial ;
* classer les communes selon leur potentiel ;
* mettre les résultats à disposition via une application interactive ;
* suivre les performances du modèle après son déploiement ;
* prévoir un mécanisme de réentraînement lorsque de nouvelles données deviennent disponibles.

---

# Architecture du projet

L'ensemble du projet repose sur une chaîne de traitement allant des données territoriales historiques jusqu'à la recommandation des communes.

```text
Données territoriales historiques
              │
              ▼
     Préparation des données
              │
              ▼
    Analyse exploratoire / EDA
              │
              ▼
   Création des variables explicatives
              │
              ▼
      Création de la variable cible
              │
              ▼
      Analyse statistique
              │
              ▼
  Traitement des valeurs manquantes
              │
              ▼
      Traitement des outliers
              │
              ▼
    Séparation Train / Test
              │
              ▼
       Entraînement modèle
              │
              ▼
    Optimisation des hyperparamètres
              │
              ▼
       Validation du modèle
              │
              ▼
     Prédiction dynamique A+1
              │
              ▼
      Score d'opportunité
              │
              ▼
   Classement des communes
              │
              ▼
      Application Streamlit
              │
              ▼
       Monitoring modèle
              │
              ▼
       Nouvelles données ?
          ↙          ↘
        NON          OUI
         │            │
        STOP     Réentraînement
```

---

# Données utilisées

Les données utilisées proviennent principalement de données territoriales publiques, notamment issues de l'INSEE et des données précédemment consolidées dans PostgreSQL/PostGIS.

L'unité d'analyse retenue est la **commune francilienne**, identifiée par son **code INSEE**.

Les données historiques disponibles couvrent notamment plusieurs millésimes tels que :

* 2017 ;
* 2023 ;
* 2024 ;
* 2025.

Une attention particulière a été portée à la disponibilité temporelle des variables afin d'éviter d'utiliser des informations ne correspondant pas à l'année de référence.

Les données sont organisées autour de plusieurs domaines :

* démographie ;
* population ;
* logements ;
* revenus ;
* emploi ;
* établissements ;
* commerces ;
* équipements ;
* mobilité ;
* caractéristiques territoriales.

---

# Préparation des données

Avant l'entraînement des modèles, plusieurs étapes de préparation ont été réalisées.

## Harmonisation temporelle

Les données provenant de différentes sources ne sont pas nécessairement disponibles pour les mêmes années.

Une étape de contrôle permet donc d'associer chaque valeur à son année réelle de référence.

Les variables temporelles ont été contrôlées afin d'éviter :

* les associations incorrectes entre une valeur et une année ;
* les doublons temporels ;
* l'utilisation d'une donnée provenant d'une année différente de celle attendue.

---

## Identification des valeurs manquantes

Une analyse de la complétude des données a été réalisée avant toute imputation.

Les variables ont été étudiées afin de distinguer :

* les valeurs réellement nulles ;
* les valeurs manquantes pouvant être remplacées ;
* les variables présentant trop peu d'informations ;
* les variables pour lesquelles une imputation aurait introduit un biais.

L'imputation n'est donc pas appliquée automatiquement à toutes les variables.

---

## Traitement des valeurs atypiques

Certaines variables territoriales présentent des distributions fortement asymétriques, notamment en raison de la présence de communes très particulières comme Paris.

Les distributions ont été étudiées graphiquement afin d'identifier les observations atypiques.

Le traitement des outliers est réalisé en tenant compte de la nature de la variable et de la réalité territoriale.

L'objectif n'est pas de supprimer automatiquement les valeurs extrêmes, mais de distinguer :

* les véritables erreurs ou anomalies ;
* les valeurs extrêmes mais cohérentes avec la réalité ;
* les communes présentant naturellement des caractéristiques très différentes du reste du territoire.

---

# Création de la variable cible

Le modèle principal repose sur une approche de **régression de la dynamique commerciale**.

L'objectif est de prédire l'évolution future du nombre de commerces à partir des caractéristiques historiques d'une commune.

La variable cible représente donc la **dynamique commerciale future**, calculée à partir de l'évolution du nombre de commerces entre différentes périodes.

Cette approche permet de ne pas simplement prédire le niveau commercial d'une commune, mais de mesurer sa capacité à évoluer dans le temps.

```text
Historique commercial
        +
Données territoriales
        │
        ▼
Dynamique commerciale future
        │
        ▼
Variable cible
```

L'utilisation de données historiques permet ainsi au modèle d'apprendre les caractéristiques associées aux communes dont l'activité commerciale évolue favorablement.

---

# Variables explicatives

Les variables explicatives regroupent plusieurs dimensions territoriales.

## Démographie

* population totale ;
* évolution de la population ;
* répartition par tranche d'âge ;
* structure démographique ;
* indicateurs d'évolution démographique.

## Activité économique

* nombre d'établissements ;
* nombre d'entreprises ;
* emplois ;
* emplois pour 1 000 habitants ;
* évolution de l'activité économique.

## Commerce

* nombre de commerces ;
* densité commerciale ;
* commerces pour 1 000 habitants ;
* évolution du nombre de commerces ;
* diversité commerciale ;
* indicateurs de concurrence.

## Pouvoir d'achat

* niveau de vie médian ;
* taux de pauvreté ;
* rapport interdécile D9/D1 ;
* indice de Gini.

## Logement

* nombre de logements ;
* évolution du parc de logements ;
* structure des logements ;
* logements selon leur taille.

## Équipements et accessibilité

* équipements de santé ;
* équipements sportifs ;
* infrastructures de transport ;
* services et équipements disponibles dans la commune.

---

# Analyse exploratoire

Une analyse exploratoire approfondie a été réalisée avant la phase de modélisation.

Elle comprend notamment :

* analyse des distributions ;
* analyse des valeurs manquantes ;
* analyse des valeurs atypiques ;
* statistiques descriptives ;
* analyse des corrélations ;
* visualisation des relations entre variables ;
* analyse de la distribution de la variable cible.

Cette étape permet de mieux comprendre la structure des données et d'identifier les variables susceptibles d'être pertinentes pour la prédiction.

---

# Analyse statistique

Plusieurs méthodes statistiques ont été utilisées afin d'évaluer les relations entre les variables.

## Corrélations de Spearman

La corrélation de Spearman a été utilisée pour mesurer les relations monotones entre les variables explicatives et la variable cible.

Cette méthode est particulièrement adaptée aux données territoriales pouvant présenter :

* des distributions non normales ;
* des relations non linéaires ;
* des valeurs extrêmes.

Une matrice de corrélation a été produite afin d'identifier les variables présentant les associations les plus importantes.

---

## Tests statistiques

Des tests statistiques ont également été utilisés afin de compléter l'analyse exploratoire.

Les analyses comprennent notamment :

* tests de corrélation de Spearman ;
* tests de significativité ;
* analyse des p-values ;
* F-test de régression.

Ces analyses permettent de distinguer les relations observées dans l'échantillon des relations statistiquement significatives.

---

# Sélection des variables

L'analyse des variables a permis d'identifier :

* les variables fortement corrélées entre elles ;
* les variables présentant une relation avec la cible ;
* les variables peu informatives ;
* les variables susceptibles d'introduire de la redondance.

Une analyse de l'importance des variables a également été réalisée après entraînement du modèle.

L'objectif est de conserver un ensemble de variables suffisamment informatif tout en limitant :

* la redondance ;
* le bruit ;
* la complexité inutile du modèle.

---

# Modélisation

Le problème est traité comme un problème de **régression supervisée**.

Le principe général est :

```text
Variables territoriales historiques
                │
                ▼
       Modèle de régression
                │
                ▼
Dynamique commerciale prédite
                │
                ▼
      Potentiel commercial
```

Plusieurs approches de Machine Learning peuvent être comparées afin de sélectionner le modèle offrant le meilleur compromis entre :

* performance ;
* robustesse ;
* capacité de généralisation ;
* interprétabilité ;
* complexité.

Le modèle principal retenu repose sur un **Gradient Boosting Regressor**, particulièrement adapté à la modélisation de relations non linéaires entre les caractéristiques territoriales et la dynamique commerciale.

---

# Gradient Boosting

Le Gradient Boosting est une méthode d'ensemble reposant sur la construction successive de modèles faibles, généralement des arbres de décision.

Chaque nouvel arbre cherche à corriger les erreurs réalisées par les modèles précédents.

Dans le cadre du projet, cette méthode permet notamment de prendre en compte :

* les relations non linéaires ;
* les interactions entre variables ;
* les différences importantes entre communes ;
* la complexité des facteurs influençant la dynamique commerciale.

---

# Séparation des données

Les données sont séparées en plusieurs ensembles afin d'évaluer correctement la capacité de généralisation du modèle.

```text
Dataset
   │
   ├── Données d'entraînement
   │
   └── Données de test
```

Les étapes de préparation nécessaires sont réalisées de manière à éviter toute fuite d'information entre les données d'entraînement et les données de test.

Le modèle est ensuite entraîné uniquement sur les données d'entraînement avant d'être évalué sur des données non utilisées lors de l'apprentissage.

---

# Optimisation du modèle

Les hyperparamètres du modèle sont optimisés afin d'améliorer ses performances.

Cette étape permet notamment de rechercher les paramètres permettant d'obtenir un modèle suffisamment performant tout en limitant le surapprentissage.

Les performances sont comparées sur les données d'entraînement et de test afin de vérifier la capacité de généralisation du modèle.

---

# Évaluation du modèle

Le modèle est évalué à l'aide de métriques adaptées à un problème de régression.

Les métriques étudiées comprennent notamment :

* **R²** ;
* **MAE – Mean Absolute Error** ;
* **MSE – Mean Squared Error** ;
* **RMSE – Root Mean Squared Error**.

L'analyse des performances ne repose pas uniquement sur une métrique unique.

Une attention particulière est portée à l'écart entre les performances d'entraînement et celles obtenues sur les données de test afin d'identifier un éventuel surapprentissage.

---

# Prédiction de la dynamique commerciale

Une fois le modèle validé, celui-ci est utilisé pour estimer la dynamique commerciale future des communes.

Le principe est :

```text
Données historiques d'une commune
              │
              ▼
        Modèle ML
              │
              ▼
Dynamique commerciale estimée
              │
              ▼
     Potentiel commercial
```

Cette prédiction constitue la première étape de la construction du système de recommandation territoriale.

---

# Score d'opportunité commerciale

La prédiction de la dynamique commerciale est ensuite transformée en un **score d'opportunité** permettant de faciliter l'interprétation des résultats.

L'objectif est de ne pas uniquement fournir une prédiction numérique, mais de transformer celle-ci en information exploitable par un décideur.

Le score permet notamment de :

* comparer les communes ;
* identifier les territoires présentant un potentiel élevé ;
* prioriser les zones à analyser ;
* faciliter la prise de décision.

---

# Analyse du niveau d'équipement commercial

Le potentiel commercial ne dépend pas uniquement de la croissance prédite.

Une commune présentant une croissance commerciale importante peut également être déjà fortement équipée.

Le projet intègre donc une comparaison entre :

* le niveau commercial observé ;
* le niveau commercial attendu compte tenu des caractéristiques du territoire.

Cette approche permet d'identifier les communes présentant un **déséquilibre entre leur potentiel territorial et leur niveau d'équipement commercial**.

Les communes peuvent ainsi être catégorisées selon leur situation :

```text
Potentiel commercial élevé
          +
Sous-équipement commercial
          │
          ▼
    OPPORTUNITÉ ÉLEVÉE
```

À l'inverse :

```text
Potentiel commercial faible
          +
Forte présence commerciale
          │
          ▼
       SATURATION
```

L'écart est exprimé sous forme relative afin d'éviter une règle fixe applicable de manière identique à toutes les communes.

---

# Classement des communes

Les communes sont classées en fonction de leur potentiel commercial.

Le processus permet d'obtenir :

* une estimation de la dynamique commerciale ;
* un score d'opportunité ;
* un niveau d'équipement ;
* une catégorie territoriale ;
* un classement des communes prioritaires.

L'objectif final est de fournir une aide à la décision permettant d'identifier les territoires présentant le meilleur compromis entre :

* attractivité territoriale ;
* dynamique commerciale ;
* pouvoir d'achat ;
* population ;
* activité économique ;
* concurrence ;
* niveau d'équipement commercial.

---

# Application interactive

Les résultats du modèle sont mis à disposition via une interface interactive.

Deux environnements de restitution ont été envisagés/développés :

* une application **Streamlit** ;
* une application déployée sur **Hugging Face Spaces**.

L'application permet notamment de consulter les informations relatives aux communes et d'explorer leur potentiel commercial.

Les utilisateurs peuvent visualiser :

* les indicateurs territoriaux ;
* les prédictions du modèle ;
* le potentiel commercial ;
* le niveau d'équipement ;
* la classification de la commune ;
* les informations permettant de comparer plusieurs territoires.

---

# Monitoring du modèle

Une étape de monitoring a été mise en place afin de suivre les performances du modèle après son entraînement.

Les métriques obtenues lors des différents entraînements sont conservées afin de pouvoir comparer les performances au cours du temps.

Le monitoring permet notamment de suivre :

* les performances du modèle ;
* les erreurs de prédiction ;
* l'évolution des métriques ;
* les performances par période ;
* les écarts entre les valeurs prédites et observées.

Les résultats sont organisés par période afin de permettre un suivi longitudinal du modèle.

---

# Cycle de réentraînement

Le modèle est conçu selon une logique de Machine Learning évolutive.

Lorsque de nouvelles données deviennent disponibles, un nouveau cycle peut être déclenché.

```text
Nouvelles données
       ↓
Construction du nouveau cycle
       ↓
Réentraînement
       ↓
Validation
       ↓
Comparaison des performances
       ↓
Déploiement
       ↓
Prédictions A+1
       ↓
Fichier de monitoring
       ↓
Évaluation du modèle
       ↓
Nouvelles données ?
    ↙          ↘
  NON          OUI
   ↓            ↓
 STOP      Réentraînement
```

Cette architecture permet d'éviter qu'un modèle soit utilisé indéfiniment sans être réévalué.

Les performances du nouveau modèle peuvent être comparées à celles du modèle précédent avant sa mise en production.

---

# Monitoring des prédictions

En plus du suivi des métriques du modèle, les prédictions sont comparées aux valeurs réellement observées lorsque celles-ci deviennent disponibles.

Cela permet de calculer les écarts entre :

```text
Valeur observée
       -
Valeur prédite
       =
Erreur de prédiction
```

Le suivi de ces erreurs permet d'identifier une éventuelle dégradation des performances du modèle au fil du temps.

Cette démarche contribue à la mise en place d'un processus de **Machine Learning industrialisé et maintenable**.

---

# Technologies utilisées

| Domaine                  | Technologies               |
| ------------------------ | -------------------------- |
| Langage                  | Python                     |
| Manipulation des données | Pandas                     |
| Calcul scientifique      | NumPy                      |
| Machine Learning         | Scikit-learn               |
| Modèle principal         | Gradient Boosting          |
| Analyse statistique      | SciPy                      |
| Visualisation            | Matplotlib                 |
| Base de données          | PostgreSQL / PostGIS       |
| Accès aux données        | SQLAlchemy                 |
| Application              | Streamlit                  |
| Déploiement              | Hugging Face Spaces        |
| Versionning              | Git / GitHub               |
| Environnement            | Jupyter Notebook / VS Code |

---

# Organisation du projet

```text
bloc5/
│
├── notebooks/
│   └── analyse_modelisation.ipynb
│
├── app/
│   └── streamlit_app.py
│
├── model/
│   └── modèle entraîné
│
├── monitoring/
│   └── métriques et résultats de suivi
│
├── data/
│   └── données préparées
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

---

# Workflow Machine Learning

Le workflow complet du projet peut être résumé ainsi :

```text
1. Collecte des données
        ↓
2. Consolidation des données territoriales
        ↓
3. Analyse de la qualité des données
        ↓
4. Traitement des valeurs manquantes
        ↓
5. Traitement des valeurs atypiques
        ↓
6. Création des variables explicatives
        ↓
7. Création de la cible
        ↓
8. Analyse statistique
        ↓
9. Séparation Train / Test
        ↓
10. Entraînement des modèles
        ↓
11. Optimisation
        ↓
12. Évaluation
        ↓
13. Sélection du modèle
        ↓
14. Prédiction A+1
        ↓
15. Score d'opportunité
        ↓
16. Classement des communes
        ↓
17. Restitution dans l'application
        ↓
18. Monitoring
        ↓
19. Réentraînement lorsque nécessaire
```

---

# Résultats obtenus

Le projet permet de passer d'une approche descriptive des territoires à une approche prédictive.

Les principaux résultats sont :

* construction d'une base de données communale exploitable par des modèles de Machine Learning ;
* création d'une variable cible représentant la dynamique commerciale ;
* identification des variables explicatives pertinentes ;
* analyse statistique des relations entre les variables ;
* développement d'un modèle de régression ;
* optimisation du modèle de Gradient Boosting ;
* prédiction de la dynamique commerciale future ;
* création d'un score d'opportunité ;
* classification des communes selon leur niveau de potentiel ;
* identification des territoires potentiellement sous-équipés ;
* identification des territoires potentiellement saturés ;
* mise à disposition des résultats via une application interactive ;
* mise en place d'un système de monitoring ;
* définition d'un cycle de réentraînement.

---

# Valeur métier

Le modèle développé permet d'apporter une réponse plus opérationnelle à la problématique d'implantation commerciale.

Plutôt que de sélectionner une commune uniquement selon son nombre actuel d'habitants ou son niveau de vie, l'approche combine plusieurs dimensions du territoire afin d'estimer son évolution commerciale.

Le système permet ainsi de répondre à plusieurs questions :

* Quelles communes présentent une dynamique commerciale favorable ?
* Quelles communes semblent sous-équipées par rapport à leur potentiel ?
* Quels territoires présentent un risque de saturation ?
* Quelles communes doivent être étudiées prioritairement pour une nouvelle implantation ?
* Comment l'attractivité commerciale d'un territoire peut-elle évoluer dans le temps ?

---

# Limites

Le modèle reste dépendant de la qualité et de la disponibilité des données historiques.

Certaines communes présentent des données incomplètes ou disponibles uniquement pour certains millésimes.

Par ailleurs, la dynamique commerciale peut être influencée par des facteurs difficiles à mesurer dans les données disponibles, tels que :

* les projets immobiliers futurs ;
* les changements d'infrastructures ;
* l'arrivée ou le départ d'enseignes ;
* les évolutions réglementaires ;
* les comportements de consommation ;
* les événements économiques locaux.

Les résultats doivent donc être considérés comme un **outil d'aide à la décision** et non comme une décision automatique d'implantation.

---

# Perspectives

Plusieurs évolutions peuvent être envisagées :

* intégrer davantage de données temporelles ;
* enrichir les données de mobilité ;
* intégrer les données de fréquentation ;
* améliorer la mesure de la concurrence ;
* intégrer davantage d'informations sur les enseignes ;
* tester d'autres modèles de Machine Learning ;
* comparer plusieurs stratégies de scoring ;
* améliorer l'explicabilité des prédictions ;
* mettre en place des alertes automatiques sur la dégradation des performances ;
* automatiser complètement le cycle de réentraînement ;
* intégrer le modèle dans une architecture MLOps complète ;
* développer une API permettant d'interroger les prédictions ;
* améliorer la visualisation cartographique des opportunités.

---

# Chaîne globale de la plateforme

Les différents blocs du projet s'intègrent dans une architecture globale :

```text
                 SOURCES DE DONNÉES
                        │
                        ▼
              ┌───────────────────┐
              │      BLOC 1       │
              │   Data Engineering│
              └─────────┬─────────┘
                        │
                        ▼
              PostgreSQL / PostGIS
                        │
                        ▼
              ┌───────────────────┐
              │      BLOC 2       │
              │    Data Analyst   │
              └─────────┬─────────┘
                        │
                        ▼
             Indicateurs territoriaux
                        │
                        ▼
              ┌───────────────────┐
              │      BLOC 5       │
              │   Machine Learning│
              └─────────┬─────────┘
                        │
                        ▼
             Prédiction commerciale
                        │
                        ▼
              Score d'opportunité
                        │
                        ▼
              Classement communes
                        │
                        ▼
              Streamlit / Hugging Face
                        │
                        ▼
                 Aide à la décision
```

---

# Installation

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement virtuel sous Windows :

```bash
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Lancer l'application Streamlit :

```bash
streamlit run app/streamlit_app.py
```

---

# Auteur

**Jessica SIGNE**

Projet réalisé dans le cadre du **Bloc 5 du titre RNCP : Ingénieur en Science des Données – spécialisation Data et IA**

**Année universitaire : 2025–2026**
