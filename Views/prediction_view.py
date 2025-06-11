import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load models and scalers
goal_model = joblib.load("models/goal_model.pkl")
goal_scaler = joblib.load("models/goal_scaler.pkl")

market_model = load_model("models/market_value_model.h5")
market_scaler = joblib.load("models/market_value_scaler.pkl")


def goal_prediction_section():
    st.subheader("🎯 Prédiction des Buts")

    with st.form("goal_form"):
        st.markdown("""
        <div style='background-color:#262730;padding:1.5em;border-radius:12px;color:white;'>
        <b>Remplissez les stats du joueur :</b>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Âge", 16, 40, 25)
            overall_rating = st.number_input("Note Globale", 40, 100, 70)
            p_matches_played = st.number_input("Matchs Joués", 0, 60, 30)
            assists = st.number_input("Passes Décisives", 0, 30, 5)
            expected_goals = st.number_input("Buts Attendus (xG)", 0.0, 40.0, 5.0)
            dribbles = st.number_input("Dribbles Réussis", 0, 150, 30)

        with col2:
            tackles = st.number_input("Tacles", 0, 150, 20)
            pass_acc = st.number_input("Précision Passes (%)", 0, 100, 75)
            goals_per_90 = st.number_input("Buts / 90 min", 0.0, 2.0, 0.5)
            assists_per_90 = st.number_input("Assists / 90 min", 0.0, 2.0, 0.3)
            xg_per_90 = st.number_input("xG / 90 min", 0.0, 2.0, 0.4)
            minutes_played = st.number_input("Minutes Jouées", 0, 6000, 2500)

        st.markdown("</div>", unsafe_allow_html=True)
        submitted_goals = st.form_submit_button("🔮 Prédire les Buts")

        if submitted_goals:
            goal_input = np.array([[age, overall_rating, p_matches_played, assists,
                                    expected_goals, dribbles, tackles, pass_acc,
                                    goals_per_90, assists_per_90, xg_per_90, minutes_played]])
            goal_input_scaled = goal_scaler.transform(goal_input)
            goal_pred = goal_model.predict(goal_input_scaled)[0]
            st.success(f"⚽ Buts Prévus : {goal_pred:.2f} buts")



# THIS FUNCTION IS CALLED BY THE MAIN APP
def display():
    st.title("📊 Outil de Prédiction des Statistiques Joueurs")
    goal_prediction_section()

