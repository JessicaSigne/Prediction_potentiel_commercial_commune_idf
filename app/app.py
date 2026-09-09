import gradio as gr
import joblib
import numpy as np
import pandas as pd
import spaces


# ============================================================
# CHARGEMENT DU PIPELINE
# ============================================================

package = joblib.load("pipeline_retail_gb.joblib")

modele = package["model"]
imputer = package["imputer"]
features_retenues = package["features_retenues"]

df_communes = pd.read_excel(
    "table_features_modele.xlsx"
)


# ============================================================
# LISTE DES COMMUNES
# ============================================================

communes = sorted(
    df_communes["nom_commune"]
    .dropna()
    .unique()
    .tolist()
)


# ============================================================
# FONCTION D'ANALYSE
# ============================================================

@spaces.GPU
def analyser_commune(nom_commune):

    # --------------------------------------------------------
    # Vérification de la sélection
    # --------------------------------------------------------

    if not nom_commune:
        return (
            "Veuillez sélectionner une commune.",
            None,
            None,
            None,
            None,
            None
        )

    # --------------------------------------------------------
    # Recherche de la commune
    # --------------------------------------------------------

    ligne = df_communes[
        df_communes["nom_commune"] == nom_commune
    ]

    if ligne.empty:
        return (
            "Commune introuvable.",
            None,
            None,
            None,
            None,
            None
        )

    ligne = ligne.iloc[0]

    # --------------------------------------------------------
    # Valeurs réelles
    # --------------------------------------------------------

    population = int(
        ligne["population_municipale_2023"]
    )

    reel = int(
        ligne["restauration_rapide_2025"]
    )

    # --------------------------------------------------------
    # Préparation des variables pour le modèle
    # --------------------------------------------------------

    cols_imputer = list(
        imputer.feature_names_in_
    )

    X_commune = (
        ligne[cols_imputer]
        .to_frame()
        .T
        .astype(float)
    )

    # --------------------------------------------------------
    # Imputation
    # --------------------------------------------------------

    X_imp = pd.DataFrame(
        imputer.transform(X_commune),
        columns=cols_imputer
    )

    # --------------------------------------------------------
    # Sélection des variables retenues
    # --------------------------------------------------------

    X_commune_imp = X_imp[
        features_retenues
    ]

    # --------------------------------------------------------
    # Prédiction
    # --------------------------------------------------------

    prediction = float(
        modele.predict(X_commune_imp)[0]
    )

    # Une prédiction négative n'a pas de sens
    prediction = max(
        0,
        prediction
    )

    # --------------------------------------------------------
    # Calcul de l'écart
    # --------------------------------------------------------

    ecart = prediction - reel

    if reel > 0:
        ecart_pct = (
            ecart / reel
        ) * 100
    else:
        ecart_pct = None

    # ========================================================
    # CLASSIFICATION
    # ========================================================

    # --------------------------------------------------------
    # CAS 1 : aucune offre réelle
    # --------------------------------------------------------

    if reel == 0:

        if prediction >= 1:

            indice = "🟢 Sous-équipé"
            signal = "Signal de potentiel commercial"

            affichage_ecart = (
                f"{prediction:.1f} établissement(s) attendu(s)"
            )

            interpretation = (
                "Aucun établissement de restauration rapide "
                "n'est actuellement recensé dans la commune, "
                "mais le modèle estime un niveau d'offre "
                "supérieur ou égal à 1 établissement."
            )

        else:

            indice = "🔵 Équilibré"
            signal = "Situation équilibrée"

            affichage_ecart = (
                "Aucun établissement attendu"
            )

            interpretation = (
                "Aucun établissement de restauration rapide "
                "n'est actuellement recensé et le modèle "
                "n'estime pas de niveau d'offre supérieur à zéro."
            )

    # --------------------------------------------------------
    # CAS 2 : sous-équipement relatif
    # --------------------------------------------------------

    elif ecart_pct > 20 and ecart >= 1:

        indice = "🟢 Sous-équipé"
        signal = "Signal de potentiel commercial"

        affichage_ecart = (
            f"{ecart_pct:+.1f} %"
        )

        interpretation = (
            f"Le modèle estime un niveau d'offre de "
            f"{prediction:.1f} établissement(s), contre "
            f"{reel} actuellement observés."
        )

    # --------------------------------------------------------
    # CAS 3 : sur-équipement / saturation
    # --------------------------------------------------------

    elif ecart_pct < -20 and abs(ecart) >= 1:

        indice = "🟠 Saturé"
        signal = "Zone de vigilance"

        affichage_ecart = (
            f"{ecart_pct:+.1f} %"
        )

        interpretation = (
            f"L'offre observée ({reel} établissement(s)) "
            f"est supérieure au niveau attendu par le modèle "
            f"({prediction:.1f})."
        )

    # --------------------------------------------------------
    # CAS 4 : équilibre
    # --------------------------------------------------------

    else:

        indice = "🔵 Équilibré"
        signal = "Situation équilibrée"

        affichage_ecart = (
            f"{ecart_pct:+.1f} %"
        )

        interpretation = (
            f"L'offre observée ({reel} établissement(s)) "
            f"est proche du niveau attendu par le modèle "
            f"({prediction:.1f})."
        )

    # ========================================================
    # TEXTE DE RÉSULTAT
    # ========================================================

    if ecart_pct is not None:

        ecart_texte = (
            f"**Écart relatif : {ecart_pct:+.1f} %**"
        )

    else:

        ecart_texte = (
            f"**Niveau attendu : "
            f"{prediction:.1f} établissement(s)**"
        )

    resultat = f"""
# {nom_commune}

### {indice}

**{signal}**

{interpretation}

{ecart_texte}

---

### Lecture

Le modèle estime le niveau d'offre attendu au regard des
caractéristiques territoriales, démographiques, économiques,
résidentielles et commerciales de la commune.

Cet indicateur constitue un **signal d'aide à la décision**.
Il ne constitue pas une mesure directe de la demande,
de la rentabilité ou de la saturation réelle du marché.
"""

    # ========================================================
    # VALEURS AFFICHÉES
    # ========================================================

    population_affichage = (
        f"{population:,}".replace(",", " ")
    )

    reel_affichage = str(
        reel
    )

    prediction_affichage = (
        f"{prediction:.1f}"
    )

    return (
        resultat,
        population_affichage,
        reel_affichage,
        prediction_affichage,
        affichage_ecart,
        indice
    )


# ============================================================
# INTERFACE GRADIO
# ============================================================

with gr.Blocks(
    title="Retail 2.0 - Intelligence Territoriale"
) as demo:

    gr.Markdown(
        """
# 🍔 Retail 2.0 - Intelligence Territoriale

## Simulateur d'analyse territoriale - Restauration rapide

Cet outil d'aide à la décision estime le **niveau d'offre
attendu en établissements de restauration rapide** pour les
communes d'Île-de-France.

Le modèle **Gradient Boosting** exploite des caractéristiques
territoriales, démographiques, économiques, résidentielles
et commerciales.

La comparaison entre le niveau attendu et l'offre réellement
observée permet d'identifier les communes présentant un
**signal de sous-équipement, d'équilibre ou de sur-équipement**.
"""
    )

    # ========================================================
    # SÉLECTION DE LA COMMUNE
    # ========================================================

    commune = gr.Dropdown(
        choices=communes,
        label="🔎 Rechercher ou sélectionner une commune",
        info="Tapez le nom d'une commune d'Île-de-France",
        interactive=True,
        allow_custom_value=False
    )

    # ========================================================
    # BOUTON
    # ========================================================

    bouton = gr.Button(
        "🔎 Analyser la commune",
        variant="primary"
    )

    # ========================================================
    # RÉSULTAT PRINCIPAL
    # ========================================================

    resultat = gr.Markdown()

    # ========================================================
    # INDICATEURS
    # ========================================================

    with gr.Row():

        population = gr.Textbox(
            label="Population municipale 2023",
            interactive=False
        )

        reel = gr.Textbox(
            label="Offre réelle 2025",
            interactive=False
        )

        prediction = gr.Textbox(
            label="Niveau attendu",
            interactive=False
        )

        ecart = gr.Textbox(
            label="Écart relatif",
            interactive=False
        )

        indice = gr.Textbox(
            label="Diagnostic",
            interactive=False
        )

    # ========================================================
    # ACTION DU BOUTON
    # ========================================================

    bouton.click(
        fn=analyser_commune,
        inputs=commune,
        outputs=[
            resultat,
            population,
            reel,
            prediction,
            ecart,
            indice
        ]
    )

    # ========================================================
    # INFORMATIONS MÉTHODOLOGIQUES
    # ========================================================

    gr.Markdown(
        """
---

### Méthodologie

**Modèle :** GradientBoostingRegressor

**Cible :** nombre d'établissements de restauration rapide
en 2025.

**Variables :** caractéristiques territoriales,
démographiques, économiques, résidentielles et commerciales.

**Indicateur :** comparaison entre le niveau d'offre observé
et le niveau d'offre attendu par le modèle.

**Seuil de diagnostic :**

- Écart relatif supérieur à **+20 %** → Sous-équipé
- Écart relatif inférieur à **-20 %** → Saturé
- Entre les deux → Équilibré

Lorsque la commune ne possède aucun établissement recensé,
l'écart relatif n'est pas calculé. Le niveau attendu est alors
utilisé pour identifier un éventuel signal de potentiel.

---

*L'indicateur constitue un signal d'aide à la décision et ne
remplace pas une étude de marché locale.*
"""
    )


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860
    )