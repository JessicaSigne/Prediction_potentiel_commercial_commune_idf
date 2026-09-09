from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(
    title="API Restauration Rapide Île-de-France",
    version="1.0.0"
)

# ============================================================
# Chargement des artefacts
# ============================================================

package = joblib.load("pipeline_retail_gb.joblib")

modele = package["model"]
imputer = package["imputer"]
features_retenues = package["features_retenues"]

df_communes = pd.read_excel("table_features_modele.xlsx")


# ============================================================
# Endpoint de prédiction
# ============================================================

@app.post("/predict")
def predict_commune(nom_commune: str):

    ligne = df_communes[
        df_communes["nom_commune"] == nom_commune
    ]

    if ligne.empty:
        return {
            "error": "Commune introuvable"
        }

    # Variables attendues par l'imputer
    cols_imputer = list(
        imputer.feature_names_in_
    )

    # Préparation de la commune
    X_commune = (
        ligne.iloc[0][cols_imputer]
        .to_frame()
        .T
        .astype(float)
    )

    # Imputation
    X_imp = pd.DataFrame(
        imputer.transform(X_commune),
        columns=cols_imputer
    )

    # Sélection des variables du modèle
    X_imp = X_imp[features_retenues]

    # Prédiction
    pred_reel = float(
        modele.predict(X_imp)[0]
    )

    # Une prédiction négative n'a pas de sens
    pred_reel = max(0, pred_reel)

    return {
        "commune": nom_commune,
        "population": int(
            ligne.iloc[0]["population_municipale_2023"]
        ),
        "restaurants_predits": round(
            pred_reel,
            1
        )
    }

# Lancement : uvicorn api_retail:app --reload