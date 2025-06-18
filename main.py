import streamlit as st
import time
from Views import (
    players_view, teams_view, leagues_view,
    big5_view,  prediction_view, similar_players_view,
    market_value_view, face_recognition_view, match_results_view
)
from Views.dashboard_view import dashboard_view  # ✅ ajoute cette ligne séparément


# --- Configuration de la page ---
st.set_page_config(page_title="Football Analytics", layout="wide")

# --- STYLING CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1a2e 100%);
        color: white;
    }
    .stButton > button {
        width: 100%;
        margin: 0.2em 0;
        font-weight: 500;
        color: white;
        background-color: #1e1e1e;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #00b4d8;
        transform: scale(1.05);
        color: white;
    }
    div[data-testid="stToolbar"] {
        visibility: hidden;
    }
    .top-nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: #00b4d8;
        padding: 1rem 2rem;
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .top-nav img {
        height: 40px;
        margin-right: 12px;
    }
    .top-nav span {
        font-size: 1.4rem;
        color: white;
        font-weight: bold;
    }
    .main-content {
        padding-top: 4.5rem;
    }
    </style>

    <div class="top-nav">
        <img src="logo.png" />
        <span>⚽ Football Analytics Dashboard</span>
    </div>
    <div class="main-content">
""", unsafe_allow_html=True)

# --- Initialisation page sélectionnée ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- Définition des pages ---
nav_items = {
    "🏠 Home": "Home",
    "👤 Players": "Players",
    "🏟️ Teams": "Teams",
    "🌍 Leagues": "Leagues",
    "🌍 Big 5 leagues": "Big_5_leagues",
    "📊 Dashboards": "Dashboards",
    "🔮 Player Goals Prediction": "Prediction",
    "🔁 Similar Players": "Similar_Players",
    "💰 Market Value Prediction": "Market_Value_Prediction",
    "🧠 Facial Recognition": "Face_Recognition",
    "📅 Match Results": "Match_Results"
}

# --- Sidebar avec boutons classiques ---
st.sidebar.title("📂 Navigation")
for label, key in nav_items.items():
    if st.sidebar.button(label):
        st.session_state.page = key

# --- Page d'accueil ---
if st.session_state.page == "Home":
    st.subheader("🎯 Bienvenue dans votre centre d'analyse footballistique intelligent")
    st.markdown("Naviguez via la barre latérale ou utilisez l'accès rapide ci-dessous.")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("logo.png", width=180)
    with col2:
        st.markdown("""
        <div style="font-size:16px;">
        
        📌 Accédez à des analyses détaillées sur les joueurs, les équipes et les championnats.
        
        
        📊 Visualisez des dashboards dynamiques basés sur les performances réelles.
        
        📅 Suivez les résultats de matchs mis à jour quotidiennement.
        
        🔍 Comparez les joueurs, estimez leur valeur et explorez les prédictions statistiques. 
        
        🧠 Découvrez notre module de reconnaissance faciale des joueurs.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🚀 Accès rapide aux modules clés")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 👤 Joueurs")
        st.markdown("Analyse complète des profils")
        if st.button("Accéder", key="players"): st.session_state.page = "Players"
    with col2:
        st.markdown("#### 📊 Dashboards")
        st.markdown("Vue globale des performances")
        if st.button("Accéder", key="dashboards"): st.session_state.page = "Dashboards"
    with col3:
        st.markdown("#### 📅 Résultats")
        st.markdown("Matchs mis à jour")
        if st.button("Accéder", key="results"): st.session_state.page = "Match_Results"

# --- Routing vers les pages ---
elif st.session_state.page == "Players": players_view.display()
elif st.session_state.page == "Teams": teams_view.display()
elif st.session_state.page == "Leagues": leagues_view.display()
elif st.session_state.page == "Big_5_leagues": big5_view.display()
elif st.session_state.page == "Dashboards": dashboard_view()
elif st.session_state.page == "Prediction": prediction_view.display()
elif st.session_state.page == "Similar_Players": similar_players_view.display()
elif st.session_state.page == "Market_Value_Prediction": market_value_view.display()
elif st.session_state.page == "Face_Recognition": face_recognition_view.display()
elif st.session_state.page == "Match_Results": match_results_view.display()

# --- Footer ---
st.markdown("""
    <hr style="margin-top: 3em;">
    <div style="text-align: center; font-size: 0.9em; color: gray;">
        ⚽ Made by Mariem Bahri — Football Analytics 2024/2025  
        <br>
        <a href='https://github.com/' style='color: #888;' target='_blank'>GitHub</a> | 
        <a href='mailto:example@email.com' style='color: #888;'>Contact</a>
    </div>
    </div> <!-- closes .main-content -->
""", unsafe_allow_html=True)
