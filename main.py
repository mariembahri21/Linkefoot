import streamlit as st
from Views import (
    players_view, teams_view, leagues_view, dashboard_view,
    big5_view, eu_players_view, prediction_view, similar_players_view,
    market_value_view, radarchart_view, ppg_prediction_view, face_recognition_view, match_results_view
)

# --- Page Config ---
st.set_page_config(page_title="Football Analytics", layout="wide")

# ---------------------- DARK THEME STYLING ----------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    .stButton > button {
        width: 100%;
        margin: 0.2em 0;
        font-weight: 500;
        color: white;
        background-color: #1e1e1e;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background-color: #00b4d8;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- FIXED TOP NAVBAR WITH CENTERED LOGO ----------------------
st.markdown("""
    <style>
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
        <span>Football Analytics Dashboard</span>
    </div>
    <div class="main-content">
""", unsafe_allow_html=True)

# ---------------------- NAVIGATION STATE ----------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------------- SIDEBAR NAVIGATION ----------------------

nav_items = {
    "🏠 Home": "Home",
    "👤 Players": "Players",
    "🏟️ Teams": "Teams",
    "🌍 Leagues": "Leagues",
    "🌍 Big 5 leagues": "Big_5_leagues",
    "⚽ European Players": "European_Players",
    "📊 Dashboards": "Dashboards",
    "🔮 Player Stats Prediction": "Prediction",
    "🔁 Similar Players": "Similar_Players",
    "💰 Market Value Prediction": "Market_Value_Prediction",
    "📊 Player Radar Comparison": "Radar_Comparison",
    "📈 PPG Prediction": "PPG_Prediction",
    "🧠 Facial Recognition": "Face_Recognition",
    "📅 Match Results": "Match_Results" 
}

for label, key in nav_items.items():
    if st.sidebar.button(label):
        st.session_state.page = key

# ---------------------- MAIN PAGE ROUTING ----------------------
if st.session_state.page == "Home":
    st.subheader("Bienvenue dans votre centre d'analyse interactif des données footballistiques !")
    st.markdown("Utilisez la barre latérale pour naviguer entre les sections.")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("logo.png", width=200)
    with col2:
        st.markdown("""
        <div style="font-size:16px;">
        📌 Accédez à des analyses détaillées sur les joueurs, les équipes et les championnats. 
         
        📊 Visualisez des dashboards dynamiques basés sur les performances réelles.  
        
        🔍 Comparez les joueurs, estimez leur valeur et explorez les prédictions statistiques.  
        
        🧠 Découvrez notre module de reconnaissance faciale des joueurs.  
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == "Players":
    players_view.display()
elif st.session_state.page == "Teams":
    teams_view.display()
elif st.session_state.page == "Leagues":
    leagues_view.display()
elif st.session_state.page == "Big_5_leagues":
    big5_view.display()
elif st.session_state.page == "European_Players":
    eu_players_view.display()
elif st.session_state.page == "Dashboards":
    dashboard_view.display()
elif st.session_state.page == "Prediction":
    prediction_view.display()
elif st.session_state.page == "Similar_Players":
    similar_players_view.display()
elif st.session_state.page == "Market_Value_Prediction":
    market_value_view.display()
elif st.session_state.page == "Radar_Comparison":
    radarchart_view.display()
elif st.session_state.page == "PPG_Prediction":
    ppg_prediction_view.display()
elif st.session_state.page == "Face_Recognition":
    face_recognition_view.display()
elif st.session_state.page == "Match_Results":
    match_results_view.display()

# ---------------------- FOOTER ----------------------
st.markdown("""
    <hr style="margin-top: 3em;">
    <div style="text-align: center; font-size: 0.9em; color: gray;">
        ⚽ Made with ❤️ by Mariem Bahri — Football Analytics 2024/2025  
        <br>
        <a href='https://github.com/' style='color: #888;' target='_blank'>GitHub</a> | 
        <a href='mailto:example@email.com' style='color: #888;'>Contact</a>
    </div>
    </div> <!-- closes .main-content -->
""", unsafe_allow_html=True)
