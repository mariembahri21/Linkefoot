import streamlit as st
import numpy as np
import pandas as pd
import joblib
import json


# === Chargement du modèle et des features ===
goal_model = joblib.load("models/xgb_goals_model_reduced.pkl")
with open("models/features_goals_reduced.json", "r") as f:
    features = json.load(f)

# === Section principale ===
def goal_prediction_section():
    st.subheader("🎯 Prédiction des Buts")

    with st.form("goal_form"):
        st.markdown("""
        <div style='background-color:#262730;padding:1.5em;border-radius:12px;color:white;'>
        <b>Remplissez les statistiques du joueur :</b>
        """, unsafe_allow_html=True)

        # Création des colonnes pour une disposition élégante
        col1, col2 = st.columns(2)
        input_data = {}

        # Génération dynamique des champs de saisie
        for i, feature in enumerate(features):
            label = feature.replace("_", " ").replace("(", "").replace(")", "").capitalize()
            default = 0.0 if "per_90" in feature or "xg" in feature.lower() else 1.0

            if i % 2 == 0:
                with col1:
                    input_data[feature] = st.number_input(label, value=default, key=feature)
            else:
                with col2:
                    input_data[feature] = st.number_input(label, value=default, key=feature)

        st.markdown("</div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔮 Prédire les Buts")

        # Prédiction à la soumission
        if submitted:
            X_input = pd.DataFrame([input_data])
            predicted_goals = goal_model.predict(X_input)[0]
            st.success(f"⚽ **Buts Prévus : {predicted_goals:.2f} buts**")

# === Exécution principale ===
def display():
    st.title("📊 Outil de Prédiction des Buts Joueurs")
    goal_prediction_section()

if __name__ == "__main__":
    display()
