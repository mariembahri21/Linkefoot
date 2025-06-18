import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_player_data

def heatmap_view():
    st.subheader("🔥 Heatmap Interactive – Clubs d’un Championnat")

    df = load_player_data()

    # Filtres
    leagues = sorted(df['league'].dropna().unique())
    selected_league = st.selectbox("🌍 Sélectionner une ligue", leagues)

    df_league = df[df['league'] == selected_league]

    if df_league.empty:
        st.warning("Aucun club disponible pour cette ligue.")
        return

    # Agréger par club
    df_clubs = df_league.groupby('team').agg({
        'goals_for': 'max',
        'goals_against': 'max',
        'points': 'max',
        'wins': 'max',
        'draws': 'max',
        'loses': 'max',
        'difference': 'max'
    }).reset_index()

    df_melt = df_clubs.melt(id_vars='team', var_name='Statistique', value_name='Valeur')

    fig = px.imshow(
        df_melt.pivot(index='team', columns='Statistique', values='Valeur'),
        color_continuous_scale='YlGnBu',
        aspect='auto',
        labels=dict(x="Statistique", y="Équipe", color="Valeur"),
        title=f"🔍 Statistiques comparatives des clubs – {selected_league}"
    )

    st.plotly_chart(fig, use_container_width=True)
