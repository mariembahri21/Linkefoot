import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load XGBoost model and features
xgb_model = joblib.load("models/xgb_market_value_model.pkl")
market_features = joblib.load("models/xgb_market_features.pkl")

def xgb_market_value_section():
    st.subheader("💰 Prédiction de la Valeur Marché (XGBoost)")

    with st.form("xgb_market_form"):
        st.markdown("""
        <div style='background-color:#262730;padding:1.5em;border-radius:12px;color:white;'>
        <b>Entrez les attributs du joueur :</b>
        """, unsafe_allow_html=True)

        # Split features into two columns
        col1, col2 = st.columns(2)
        input_data = {}

        for i, feature in enumerate(market_features):
            label = feature.replace('_', ' ').capitalize()
            default_val = 1.0 if "body_type" in feature or "peak" in feature or "young" in feature or "veteran" in feature else 0.0

            if i % 2 == 0:
                with col1:
                    input_data[feature] = st.number_input(label, value=default_val, key=f"xgb_{feature}")
            else:
                with col2:
                    input_data[feature] = st.number_input(label, value=default_val, key=f"xgb_{feature}")

        st.markdown("</div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("💸 Prédire Valeur Marché")

        if submitted:
            X_input = pd.DataFrame([input_data])
            log_prediction = xgb_model.predict(X_input)[0]
            predicted_value = max(np.expm1(log_prediction), 0)
            st.success(f"💰 Valeur Marché estimée : €{predicted_value:.2f}M")


# THIS FUNCTION IS CALLED BY THE MAIN APP
def display():
    st.title("📊 Prédiction de la Valeur Marché (XGBoost)")
    xgb_market_value_section()
