# ppg_prediction_view.py

import streamlit as st
import pandas as pd
import joblib
import os

# Load model, scaler, and expected feature columns
model_path = os.path.join("models", "ppg_lasso_model.pkl")
scaler_path = os.path.join("models", "ppg_scaler.pkl")
features_path = os.path.join("models", "ppg_feature_columns.pkl")

lasso_model = joblib.load(model_path)
ppg_scaler = joblib.load(scaler_path)
feature_cols = joblib.load(features_path)

def display():
    st.subheader("📊 Prédiction des Points Par Match (PPG)")

    with st.form("ppg_form"):
        st.markdown("""<div style='background-color:#1e1e1e;padding:1em;border-radius:12px;color:white;'>
        <b>Entrez les statistiques de l’équipe :</b>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            wins = st.number_input("Matchs Gagnés", 0, 38, 15)
            draws = st.number_input("Matchs Nuls", 0, 38, 10)
            losts = st.number_input("Matchs Perdus", 0, 38, 10)
            goals_for = st.number_input("Buts Marqués", 0, 100, 50)
            goals_against = st.number_input("Buts Concédés", 0, 100, 30)
            titles_won = st.number_input("Titres Gagnés", 0, 10, 1)
            players = st.number_input("Nombre de Joueurs", 11, 40, 25)

        with col2:
            overall = st.number_input("Note Globale", 50, 100, 75)
            attack = st.number_input("Note Attaque", 50, 100, 75)
            midfield = st.number_input("Note Milieu", 50, 100, 75)
            defence = st.number_input("Note Défense", 50, 100, 75)
            club_worth = st.number_input("Valeur Club (Millions €)", 1, 10000, 500)
            domestic_prestige = st.number_input("Prestige National (0-10)", 0, 10, 5)
            international_prestige = st.number_input("Prestige International (0-10)", 0, 10, 5)
            starting_xi_average_age = st.number_input("Âge Moyen XI Titulaire", 16.0, 40.0, 26.5)

        submitted = st.form_submit_button("Prédire le PPG")

        if submitted:
            # Build input dictionary to match feature columns
            form_values = {
                'wins': wins,
                'draws': draws,
                'losts': losts,
                'goals_for': goals_for,
                'goals_against': goals_against,
                'overall': overall,
                'attack': attack,
                'midfield': midfield,
                'defence': defence,
                'club_worth_million_euro': club_worth,
                'domestic_prestige': domestic_prestige,
                'international_prestige': international_prestige,
                'titles_won': titles_won,
                'players': players,
                'starting_xi_average_age': starting_xi_average_age
            }

            # Ensure order matches training
            input_data = pd.DataFrame([[form_values[col] for col in feature_cols]], columns=feature_cols)

            # Scale and predict
            input_scaled = ppg_scaler.transform(input_data)
            predicted_ppg = lasso_model.predict(input_scaled)[0]

            st.success(f"📈 Points par Match Prédits : **{predicted_ppg:.2f}**")
