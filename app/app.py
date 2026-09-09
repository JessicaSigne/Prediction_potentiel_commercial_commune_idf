import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Retail 2.0 — Intelligence Territoriale Île-de-France",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# IDENTITÉ VISUELLE (Palette bleue, contrastes sidebar corrigés)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

        :root {
            --paper: #EAF0F8;
            --paper-card: #F6F9FD;
            --blue-900: #0B2A52;
            --blue-800: #123A6B;
            --blue-700: #1B4C86;
            --blue-500: #2E68B0;
            --blue-300: #7FA8DA;
            --blue-100: #D3E2F5;
            --line: #C4D6EC;
            --text-secondary: #4A5C78;
            --green: #2E7D46;
            --red: #B3372C;
        }

        html, body, [class*="css"] {
            font-family: 'IBM Plex Sans', sans-serif;
            background-color: var(--paper);
            color: var(--blue-900);
        }

        .main { background-color: var(--paper); padding: 1.5rem 2rem 3rem; }

        /* ── En-tête ────────────────────────────────────────────────────── */
        .app-eyebrow {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.78rem;
            color: var(--blue-500);
            letter-spacing: 0.02em;
            margin-bottom: 0.3rem;
        }
        h1.app-title {
            font-family: 'Fraunces', serif;
            font-weight: 600;
            font-size: 2.4rem;
            color: var(--blue-900);
            margin: 0 0 0.5rem 0;
            line-height: 1.15;
        }
        .app-subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
            max-width: 65ch;
            line-height: 1.5;
            margin-bottom: 1.1rem;
        }
        .app-rule {
            border: none;
            border-top: 1px solid var(--line);
            margin: 0 0 1.8rem 0;
        }

        /* ── Encart focus Restauration Rapide ──────────────────────────── */
        .fast-food-focus {
            background: var(--paper-card);
            border-left: 4px solid var(--blue-500);
            padding: 12px 16px;
            margin-bottom: 1.5rem;
            font-size: 0.95rem;
            color: var(--blue-900);
            border-radius: 0 4px 4px 0;
        }

        /* ── Barre latérale : panneau de commande bleu (Visibilité totale) ── */
        [data-testid="stSidebar"] {
            background-color: var(--blue-900);
            border-right: 1px solid var(--blue-800);
        }
        [data-testid="stSidebar"] > div { padding-top: 1.6rem; }
        .sidebar-label {
            font-family: 'IBM Plex Mono', monospace;
            color: var(--blue-300);
            font-size: 0.78rem;
            letter-spacing: 0.04em;
            font-weight: 600;
            margin: 0 0 0.9rem 0.2rem;
            text-transform: uppercase;
        }
        /* Forçage de l'écriture en blanc pour une lisibilité parfaite */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
            border-left: 3px solid transparent;
            border-radius: 0;
            padding: 8px 12px;
            margin-bottom: 4px;
            transition: border-color 0.15s, background-color 0.15s;
        }
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
            background-color: var(--blue-700);
            border-left-color: var(--blue-300);
        }
        [data-testid="stSidebar"] .stAlert {
            background-color: var(--blue-800) !important;
            border: 1px solid var(--blue-500);
            border-radius: 2px;
            color: #FFFFFF !important;
        }

        /* ── Boutons ───────────────────────────────────────────────────── */
        .stButton>button {
            background-color: var(--blue-700);
            color: #FFFFFF;
            border-radius: 2px;
            font-weight: 500;
            border: 1px solid var(--blue-700);
            padding: 0.5rem 1.3rem;
            transition: background-color 0.15s;
        }
        .stButton>button:hover {
            background-color: var(--blue-900);
            border-color: var(--blue-900);
            color: #FFFFFF;
        }

        /* ── Cartes de mesure ─────────────────────────────────────────── */
        .measure-row { display: flex; gap: 14px; flex-wrap: wrap; margin: 0.4rem 0 1.4rem; }
        .measure-card {
            position: relative;
            background: var(--paper-card);
            border: 1px solid var(--line);
            padding: 16px 18px;
            flex: 1;
            min-width: 170px;
        }
        .measure-card::before, .measure-card::after {
            content: '';
            position: absolute;
            width: 12px;
            height: 12px;
        }
        .measure-card::before {
            top: -1px; left: -1px;
            border-top: 2px solid var(--blue-500);
            border-left: 2px solid var(--blue-500);
        }
        .measure-card::after {
            bottom: -1px; right: -1px;
            border-bottom: 2px solid var(--blue-500);
            border-right: 2px solid var(--blue-500);
        }
        .measure-label {
            font-size: 0.82rem;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }
        .measure-value {
            font-family: 'IBM Plex Mono', monospace;
            font-weight: 600;
            font-size: 1.5rem;
            color: var(--blue-900);
        }
        .measure-delta {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 4px;
        }
        .measure-delta.up { color: var(--green); }
        .measure-delta.down { color: var(--red); }
        .measure-delta.flat { color: var(--text-secondary); }

        /* ── Encarts de lecture ────────────────────────────────────────── */
        .callout {
            border-left: 3px solid var(--blue-500);
            background: var(--paper-card);
            padding: 14px 18px;
            margin: 0.6rem 0 1.4rem;
            line-height: 1.55;
        }
        .callout b { color: var(--blue-900); }
        .callout.opportunity { border-left-color: var(--green); }
        .callout.saturation { border-left-color: var(--red); }
        .callout.balanced { border-left-color: var(--blue-500); }

        /* ── Titres de section ─────────────────────────────────────────── */
        h2, h3 { color: var(--blue-900); font-weight: 600; font-family: 'IBM Plex Sans', sans-serif; }
        .section-note { color: var(--text-secondary); font-size: 0.92rem; margin-bottom: 0.8rem; }

        /* ── Cadre image (module SHAP) ─────────────────────────────────── */
        .figure-frame {
            border: 1px solid var(--line);
            background: var(--paper-card);
            padding: 12px;
        }

        /* ── Pied de page ─────────────────────────────────────────────── */
        .app-footer {
            margin-top: 2.4rem;
            padding-top: 0.9rem;
            border-top: 1px solid var(--line);
            font-size: 0.8rem;
            color: var(--text-secondary);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def measure_card(label, value, delta_text=None, delta_sign="flat"):
    arrow = {"up": "▲", "down": "▼", "flat": "▬"}.get(delta_sign, "")
    delta_html = (
        f'<div class="measure-delta {delta_sign}">{arrow} {delta_text}</div>'
        if delta_text
        else ""
    )
    return (
        f'<div class="measure-card">'
        f'<div class="measure-label">{label}</div>'
        f'<div class="measure-value">{value}</div>'
        f"{delta_html}"
        f"</div>"
    )


# ── En-tête ───────────────────────────────────────────────────────────────
st.markdown('<div class="app-eyebrow">RETAIL 2.0 · RESTAURATION RAPIDE · ÎLE-DE-FRANCE</div>', unsafe_allow_html=True)
st.markdown('<h1 class="app-title">Simulateur prédictif d\'implantation retail</h1>', unsafe_allow_html=True)
st.markdown( 
    '<div class="app-subtitle">Outil d\'aide à la décision stratégique spécialisé dans la '
    "<b>restauration rapide</b>. Il croise les bases INSEE (équipements et niveau de vie) avec un modèle Gradient Boosting pour estimer, commune par commune, le niveau attendu "
    "d'établissements et identifier les communes présentant un signal de potentiel commercial.</div>", 
    unsafe_allow_html=True, 
)

# Sous-titre orienté métier / restauration rapide
st.markdown( 
    '<div class="fast-food-focus"><b>Focus Métier :</b> Analyse du '
    'niveau d\'équipement en restauration rapide et identification des '
    'communes présentant un signal de potentiel commercial.</div>', 
    unsafe_allow_html=True, 
)

st.markdown('<hr class="app-rule">', unsafe_allow_html=True)


@st.cache_resource
def load_app_assets():
  package = joblib.load("pipeline_retail_gb.joblib")
  features_retenues = package["features_retenues"]
  df = pd.read_excel("table_features_modele.xlsx")
  return package, df, features_retenues


package, df_communes, features_retenues = load_app_assets()
modele = package["model"]
imputer = package["imputer"]

# ── Barre latérale ──────────────────────────────────────────────────────
manquantes = [f for f in features_retenues if f not in df_communes.columns]
st.sidebar.markdown('<div class="sidebar-label">ÉTAT DU MODÈLE</div>', unsafe_allow_html=True)
if manquantes:
  st.sidebar.error(f"{len(manquantes)} feature(s) manquante(s) dans le jeu de données.")
else:
  st.sidebar.success("Intégrité validée — modèle opérationnel.")

st.sidebar.markdown('<div class="sidebar-label" style="margin-top:1.4rem;">MODULES</div>', unsafe_allow_html=True)
choix_module = st.sidebar.radio(
    "Sélectionner un module",
    [
        "1. Simulateur par commune",
        "2. Palmarès des opportunités",
        "3. Lecture globale du modèle",
    ],
    label_visibility="collapsed",
)


# ── MODULE 1 ────────────────────────────────────────────────────────────
if choix_module == "1. Simulateur par commune":
  st.subheader("Analyse et prédiction par commune")
  st.markdown(
      '<div class="section-note">Choisissez une commune pour comparer son offre '
      "actuelle en restauration rapide au potentiel estimé par le modèle.</div>",
      unsafe_allow_html=True,
  )

  liste_communes = sorted(df_communes["nom_commune"].dropna().unique())
  commune_selectionnee = st.selectbox(
      "Sélectionner une commune francilienne :", liste_communes
  )

  if st.button("Lancer la simulation"):
    ligne = df_communes[
        df_communes["nom_commune"] == commune_selectionnee
    ].iloc[0]
    population = int(ligne["population_municipale_2023"])
    reel = int(ligne["restauration_rapide_2025"])

    cols_imputer = list(imputer.feature_names_in_)
    X_commune = ligne[cols_imputer].to_frame().T.astype(float)
    X_imp = pd.DataFrame(imputer.transform(X_commune), columns=cols_imputer)
    X_commune_imp = X_imp[features_retenues]
    pred_reel = float(modele.predict(X_commune_imp)[0])
    pred_reel = max(0, pred_reel)
    ecart = pred_reel - reel

    st.markdown("#### Résultats de l'évaluation")

    if ecart > 2:
      indice, delta_sign = "Sous-équipé", "up"
    elif ecart < -2:
      indice, delta_sign = "Supérieur au niveau attendu", "down"
    else:
      indice, delta_sign = "Équilibré", "flat"

    cards = (
        measure_card("Population totale", f"{population:,}".replace(",", " ") + " hab.")
        + measure_card("Offre actuelle", f"{reel}")
        + measure_card("Niveau attendu", f"{pred_reel:.1f}")
        + measure_card("Indice de potentiel", indice, f"{ecart:+.1f}", delta_sign)
    )
    st.markdown(f'<div class="measure-row">{cards}</div>', unsafe_allow_html=True)

    if ecart > 2:
      st.markdown(
          f'<div class="callout opportunity"><b>Signal de potentiel commercial identifié '
          f"pour {commune_selectionnee}.</b><br>Le modèle anticipe un besoin "
          f"supérieur à l'offre en place ({pred_reel:.1f} prédits pour {reel} "
          f"réels).</div>",
          unsafe_allow_html=True,
      )
    elif ecart < -2:
      st.markdown(
        f'<div class="callout saturation"><b>Zone de vigilance pour '
        f"{commune_selectionnee}.</b><br>"
        f"L'offre observée ({reel} établissements) est supérieure au niveau "
        f"attendu selon le modèle ({pred_reel:.1f}), soit un écart de "
        f"{ecart:+.1f} établissements.</div>",
        unsafe_allow_html=True,
      )
    else:
      st.markdown(
        f'<div class="callout balanced"><b>Situation équilibrée pour '
        f"{commune_selectionnee}.</b><br>"
        f"L'offre observée ({reel} établissements) est proche du niveau "
        f"attendu par le modèle ({pred_reel:.1f}).</div>",
          unsafe_allow_html=True,
      )


# ── MODULE 2 ────────────────────────────────────────────────────────────
elif choix_module == "2. Palmarès des opportunités":
  st.subheader("Classement des zones à fort potentiel et de saturation")
  st.markdown(
    '<div class="section-note">Écart entre le niveau attendu par le modèle et '
    "l'offre réelle en restauration rapide, trié dans les deux sens pour "
    "identifier les communes présentant un signal de potentiel ou une offre "
    "supérieure au niveau attendu.</div>",
      unsafe_allow_html=True,
  )

  cols_imputer = list(imputer.feature_names_in_)
  X_all = df_communes[cols_imputer].astype(float)
  X_all_imp = pd.DataFrame(imputer.transform(X_all), columns=cols_imputer)[
      features_retenues
  ]
  preds_reel = modele.predict(X_all_imp)

  df_analyse = df_communes[
      ["nom_commune", "population_municipale_2023", "restauration_rapide_2025"]
  ].copy()
  df_analyse["Restaurants Prédits"] = preds_reel
  df_analyse["Écart Brut"] = preds_reel - df_analyse["restauration_rapide_2025"]
  df_analyse.rename(
      columns={
          "nom_commune": "Commune",
          "population_municipale_2023": "Population",
          "restauration_rapide_2025": "Offre Réelle",
      },
      inplace=True,
  )

  def formater(df_in):
    d = df_in[
        [
            "Commune",
            "Population",
            "Offre Réelle",
            "Restaurants Prédits",
            "Écart Brut",
        ]
    ].copy()
    d["Population"] = d["Population"].apply(
        lambda x: f"{int(x):,}".replace(",", " ")
    )
    d["Restaurants Prédits"] = d["Restaurants Prédits"].round(1)
    d["Écart Brut"] = d["Écart Brut"].round(1)
    return d.reset_index(drop=True)

  tab1, tab2 = st.tabs(
      ["Signal de potentiel (top 10)", "Offre supérieure au niveau attendu (top 10)"]
  )
  with tab1:
    st.markdown(
        '<div class="section-note">Écarts positifs les plus marqués — '
        "communes où l'offre observée est inférieure au niveau attendu par le modèle.</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(
        formater(
            df_analyse.sort_values("Écart Brut", ascending=False).head(10)
        ),
        use_container_width=True,
    )
  with tab2:
    st.markdown(
        '<div class="section-note">Écarts négatifs les plus élevés — '
        "communes où l'offre observée est supérieure au niveau attendu par le modèle.</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(
        formater(
            df_analyse.sort_values("Écart Brut", ascending=True).head(10)
        ),
        use_container_width=True,
    )


# ── MODULE 3 ────────────────────────────────────────────────────────────
elif choix_module == "3. Lecture globale du modèle":

    from pathlib import Path

    st.subheader("Explicabilité globale du modèle")

    st.markdown(
        '<div class="section-note">'
        "Impact marginal de chaque variable explicative sur la prédiction "
        "du nombre d'établissements de restauration rapide (analyse SHAP)."
        "</div>",
        unsafe_allow_html=True,
    )

    BASE_DIR = Path(__file__).resolve().parent
    SHAP_PATH = BASE_DIR / "shap_global.png"

    # st.write("Chemin :", SHAP_PATH)
    # st.write("Existe :", SHAP_PATH.exists())

    if SHAP_PATH.exists():

        st.image(
            str(SHAP_PATH),
            caption="Impact global des variables explicatives sur la prédiction (SHAP)",
        )

    else:

        st.error(
            f"Le fichier shap_global.png est introuvable dans : {BASE_DIR}"
        )

# Lancement : streamlit run app.py