import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_player_data

def age_performance_view():
    st.subheader("📈 Évolution de la performance selon l'âge")

    df = load_player_data()

    leagues = df['league'].dropna().unique()
    selected_league = st.selectbox("🌍 Sélectionner une ligue", ["Toutes"] + sorted(leagues.tolist()))

    positions = df['position'].dropna().unique()
    selected_position = st.selectbox("🎯 Sélectionner un poste", ["Tous"] + sorted(positions.tolist()))

    df_filtered = df.copy()

    if selected_league != "Toutes":
        df_filtered = df_filtered[df_filtered['league'] == selected_league]

    if selected_position != "Tous":
        df_filtered = df_filtered[df_filtered['position'] == selected_position]

    required_cols = {'age', 'overall_rating', 'p_goals', 'assists'}
    if not required_cols.issubset(df_filtered.columns):
        st.error(f"Colonnes manquantes dans le dataset : {required_cols - set(df_filtered.columns)}")
        return

    df_age = df_filtered.groupby('age')[['overall_rating', 'p_goals', 'assists']].mean().reset_index()

    # --- Graphe 1 : Overall Rating ---
    st.markdown("#### 🔵 Moyenne du Rating par âge")
    fig1 = px.line(
        df_age,
        x='age',
        y='overall_rating',
        markers=True,
        labels={'overall_rating': "Note moyenne", 'age': "Âge"},
        title="Évolution du rating moyen par âge"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- Graphe 2 : Goals & Assists ---
    st.markdown("#### ⚽ Moyenne des Buts et Passes par âge")
    fig2 = px.line(
        df_age,
        x='age',
        y=['p_goals', 'assists'],
        markers=True,
        labels={'value': "Valeur moyenne", 'variable': "Indicateur", 'age': "Âge"},
        title="Évolution des stats offensives par âge"
    )
    fig2.update_layout(legend_title="Statistique")
    st.plotly_chart(fig2, use_container_width=True)
