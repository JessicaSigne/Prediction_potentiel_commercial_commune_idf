from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.providers.smtp.operators.smtp import EmailOperator

from sqlalchemy import create_engine, text


# ============================================================
# 1. PARAMÈTRES GÉNÉRAUX
# ============================================================

EMAIL_DESTINATAIRE = "jessica.signe@ynov.com"

DOSSIER_DONNEES = "/opt/airflow/donnees"

FICHIER_MONITORING = (
    f"{DOSSIER_DONNEES}/monitoring_modele.xlsx"
)


# ============================================================
# 2. VÉRIFICATION D'UNE NOUVELLE ANNÉE
# ============================================================

def verifier_nouvelle_annee():

    engine = create_engine(
        "postgresql+psycopg2://DB_USER:DB_PASSWORD@HOST:5432/DATABASE"
    )

    tables_fin = [
        "fin_caracteristiques_logement",
        "fin_emploi_forme_juridique",
        "fin_infrastructures_de_proximite",
        "fin_mobilite_domicile_travail",
        "fin_population_emploi",
        "fin_pouvoir_achat_population",
        "fin_recensement_population",
        "fin_reference_population"
    ]

    # --------------------------------------------------------
    # Année dynamique
    # --------------------------------------------------------

    annee_actuelle = datetime.now().year
    annee_reference = annee_actuelle - 1

    annees_trouvees = []

    # --------------------------------------------------------
    # Recherche de la dernière année disponible
    # dans chaque table fin_
    # --------------------------------------------------------

    with engine.connect() as conn:

        for table in tables_fin:

            query = text(f"""
                SELECT MAX(annee_recensement)
                FROM {table}
                WHERE annee_recensement IS NOT NULL
            """)

            resultat = conn.execute(query).scalar()

            if resultat is not None:

                derniere_annee_table = int(resultat)

                annees_trouvees.append(
                    derniere_annee_table
                )

                print(
                    f"{table} → "
                    f"dernière année disponible : "
                    f"{derniere_annee_table}"
                )

            else:

                print(
                    f"{table} → "
                    "aucune année disponible"
                )

    # --------------------------------------------------------
    # Aucune donnée trouvée
    # --------------------------------------------------------

    if not annees_trouvees:

        print(
            "❌ Aucune année de recensement "
            "n'a été trouvée dans les tables fin_."
        )

        return False

    # --------------------------------------------------------
    # On récupère la dernière année disponible
    # parmi toutes les tables
    # --------------------------------------------------------

    derniere_annee = max(annees_trouvees)

    print("\n==============================================")
    print("VÉRIFICATION DU NOUVEAU MILLÉSIME")
    print("==============================================")

    print(
        f"Année actuelle     : {annee_actuelle}"
    )

    print(
        f"Année de référence : {annee_reference}"
    )

    print(
        f"Dernière année disponible : "
        f"{derniere_annee}"
    )

    # --------------------------------------------------------
    # Une nouvelle année est disponible
    # --------------------------------------------------------

    if derniere_annee > annee_reference:

        print(
            f"\n✅ Nouvelle année détectée : "
            f"{derniere_annee}"
        )

        print(
            "La suite du pipeline va être exécutée."
        )

        return True

    # --------------------------------------------------------
    # Aucune nouvelle année
    # --------------------------------------------------------

    print(
        "\n⏹️ Aucune nouvelle année disponible."
    )

    print(
        "La modélisation et les tâches suivantes "
        "seront ignorées."
    )

    return False


# ============================================================
# 3. CONFIGURATION PAR DÉFAUT
# ============================================================

default_args = {

    "owner": "Jessica_IA_m2",

    "depends_on_past": False,

    "start_date": datetime(2026, 1, 1),

    "email": [
        EMAIL_DESTINATAIRE
    ],

    "email_on_failure": True,

    "email_on_retry": False,

    "retries": 1,

    "retry_delay": timedelta(minutes=5),
}


# ============================================================
# 4. DÉFINITION DU DAG
# ============================================================

with DAG(

    dag_id="pipeline_retail_intelligence_idf",

    default_args=default_args,

    description=(
        "Pipeline ETL, modélisation prédictive et "
        "monitoring du scoring Retail en Île-de-France"
    ),

    # Exécution mensuelle
    schedule="@monthly",

    catchup=False,

    max_active_runs=1,

    tags=[
        "retail",
        "idf",
        "etl",
        "machine-learning",
        "monitoring"
    ],

) as dag:


    # ========================================================
    # TÂCHE A — EXTRACTION DES DONNÉES
    # ========================================================

    task_collecte = BashOperator(

        task_id="extraction_donnees",

        bash_command=(

            "jupyter nbconvert "
            "--to notebook "
            "--execute "

            f"{DOSSIER_DONNEES}/collecte_donnees.ipynb "

            "--output "

            f"{DOSSIER_DONNEES}/"
            "collecte_donnees_execute.ipynb"
        ),
    )


    # ========================================================
    # TÂCHE B — STOCKAGE DES DONNÉES BRUTES
    # ========================================================

    task_stockage = BashOperator(

        task_id="stockage_donnees_brutes",

        bash_command=(

            "jupyter nbconvert "
            "--to notebook "
            "--execute "

            f"{DOSSIER_DONNEES}/"
            "stockage_intermediaire_donnees.ipynb "

            "--output "

            f"{DOSSIER_DONNEES}/"
            "stockage_intermediaire_execute.ipynb"
        ),
    )


    # ========================================================
    # TÂCHE C — TRANSFORMATION ET STOCKAGE FINAL
    # ========================================================

    task_transformation = BashOperator(

        task_id=(
            "transformation_et_stockage_"
            "donnees_finales"
        ),

        bash_command=(

            "jupyter nbconvert "
            "--to notebook "
            "--execute "

            f"{DOSSIER_DONNEES}/"
            "transformation_stockage_final.ipynb "

            "--output "

            f"{DOSSIER_DONNEES}/"
            "transformation_stockage_final_execute.ipynb"
        ),
    )


    # ========================================================
    # TÂCHE D — VÉRIFICATION D'UNE NOUVELLE ANNÉE
    # ========================================================

    verification_nouvelle_annee = ShortCircuitOperator(

        task_id="verification_nouvelle_annee",

        python_callable=verifier_nouvelle_annee,
    )


    # ========================================================
    # TÂCHE E — CRÉATION DE LA TABLE DE MODÉLISATION
    # ========================================================

    task_table_modelisation = BashOperator(

        task_id="creation_table_modelisation",

        bash_command=(

            "jupyter nbconvert "
            "--to notebook "
            "--execute "

            f"{DOSSIER_DONNEES}/"
            "creation_table_modelisation.ipynb "

            "--output "

            f"{DOSSIER_DONNEES}/"
            "creation_table_modelisation_execute.ipynb"
        ),
    )


    # ========================================================
    # TÂCHE F — MODÉLISATION PRÉDICTIVE
    # ========================================================

    task_modelisation = BashOperator(

        task_id="modelisation_predictive",

        bash_command=(

            "jupyter nbconvert "
            "--to notebook "
            "--execute "

            f"{DOSSIER_DONNEES}/"
            "modelisation_predictive.ipynb "

            "--output "

            f"{DOSSIER_DONNEES}/"
            "modelisation_predictive_execute.ipynb"
        ),
    )


    # ========================================================
    # TÂCHE G — ENVOI DU RAPPORT DE MONITORING
    # ========================================================

    task_envoi_rapport = EmailOperator(

        task_id="envoi_rapport_monitoring",

        to=EMAIL_DESTINATAIRE,

        subject=(
            "Monitoring modèle Retail IDF "
            "— rapport automatique"
        ),

        html_content="""

        <h3>
            Rapport de monitoring du modèle Retail IDF
        </h3>

        <p>
            Bonjour,
        </p>

        <p>
            Le pipeline Retail Intelligence
            Île-de-France s'est exécuté avec succès.
        </p>

        <p>
            Vous trouverez en pièce jointe le rapport
            Excel contenant les performances du modèle
            et les informations de monitoring.
        </p>

        <p>
            Le rapport présente notamment les métriques
            <b>R²</b>, <b>RMSE</b>, <b>MAE</b>,
            ainsi que le nombre d'observations
            par période.
        </p>

        <br>

        <p>
            <i>
                Message automatique généré par Airflow.
            </i>
        </p>

        """,

        files=[
            FICHIER_MONITORING
        ],
    )


    # ========================================================
    # TÂCHE H — NETTOYAGE DES FICHIERS TEMPORAIRES
    # ========================================================

    task_nettoyage = BashOperator(

        task_id="nettoyage_fichiers_temporaires",

        bash_command=(

            f"rm -f "
            f"{DOSSIER_DONNEES}/*.csv "
            f"{DOSSIER_DONNEES}/*.pkl "
            f"{DOSSIER_DONNEES}/*.json "
            f"{DOSSIER_DONNEES}/*_execute.ipynb"
        ),
    )


    # ========================================================
    # 5. ENCHAÎNEMENT DES TÂCHES
    # ========================================================

    (

        task_collecte

        >> task_stockage

        >> task_transformation

        >> verification_nouvelle_annee

        >> task_table_modelisation

        >> task_modelisation

        >> task_envoi_rapport

        >> task_nettoyage

    )

# docker exec airflow_container airflow dags trigger pipeline_retail_intelligence_idf puis http://localhost:8080