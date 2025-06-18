import streamlit as st
import numpy as np
import pandas as pd
import joblib
import json
from scipy.special import inv_boxcox

# Load model and config
rf_model = joblib.load("best_randomforest_market_value_model.pkl")
with open("boxcox_lambda.json", "r") as f:
    fitted_lambda = json.load(f)["lambda"]

with open("selected_features.json", "r") as f:
    market_features = json.load(f)

# Default values
default_values = {
    "release_clause_m": 242.9,
    "international_reputation": 94,
    "overall_rating": 91,
    "reactions": 95,
    "potential": 94,
    "composure": 97,
    "vision": 92,
    "wage_k": 565,
    "shortpassing": 88,
    "ballcontrol": 96.00
}

def rf_market_value_section():
    st.subheader("💰 Prédiction de la Valeur Marché des Joueurs")

    with st.form("rf_market_form"):
        st.markdown("""
        <div style='background-color:#262730;padding:1.5em;border-radius:12px;color:white;'>
        <b>Entrez les attributs du joueur :</b>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        input_data = {}

        for i, feature in enumerate(market_features):
            label = feature.replace('_', ' ').capitalize()
            default_val = default_values.get(feature, 0.0)

            if i % 2 == 0:
                with col1:
                    input_data[feature] = st.number_input(label, value=default_val, key=f"rf_{feature}")
            else:
                with col2:
                    input_data[feature] = st.number_input(label, value=default_val, key=f"rf_{feature}")

        st.markdown("</div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("💸 Prédire Valeur Marché")

        if submitted:
            X_input = pd.DataFrame([input_data])
            bc_prediction = rf_model.predict(X_input)[0]
            predicted_value = max(inv_boxcox(bc_prediction, fitted_lambda), 0)
            st.success(f"💰 Valeur Marché estimée : €{predicted_value:.2f}M")

def display():
    st.title("📊 Prédiction de la Valeur Marché")
    rf_market_value_section()
