import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_player_data

def off_vs_def_view():
    st.subheader("🎯 Analyse Offensif vs Défensif des Joueurs")

    df = load_player_data()

    # Vérification des colonnes nécessaires
    required_cols = {'position', 'league', 'age', 'p_goals', 'assists', 'interceptions', 'standingtackle', 'overall_rating'}
    if not required_cols.issubset(df.columns):
        st.error(f"Colonnes manquantes dans le dataset : {required_cols - set(df.columns)}")
        return

    # Filtres
    # Filtres avec clés uniques
    col1, col2, col3 = st.columns(3)
    selected_league = col1.selectbox("🌍 Sélectionner une ligue", ["Toutes"] + sorted(df['league'].dropna().unique()), key="league_filter")
    selected_position = col2.selectbox("🎯 Sélectionner un poste", ["Tous"] + sorted(df['position'].dropna().unique()), key="position_filter")
    age_range = col3.slider("📅 Âge", int(df['age'].min()), int(df['age'].max()), (18, 35), key="age_filter")


    # Application des filtres
    df_filtered = df.copy()
    if selected_league != "Toutes":
        df_filtered = df_filtered[df_filtered['league'] == selected_league]
    if selected_position != "Tous":
        df_filtered = df_filtered[df_filtered['position'] == selected_position]
    df_filtered = df_filtered[(df_filtered['age'] >= age_range[0]) & (df_filtered['age'] <= age_range[1])]

    if df_filtered.empty:
        st.warning("Aucun joueur trouvé pour ces critères.")
        return

    # Calcul indicateurs
    df_filtered['offense'] = df_filtered['p_goals'] + df_filtered['assists']
    df_filtered['defense'] = df_filtered['interceptions'] + df_filtered['standingtackle']

    # Graphique scatter
    fig = px.scatter(
        df_filtered,
        x='offense',
        y='defense',
        color='overall_rating',
        hover_data=['name', 'position', 'team', 'age'],
        labels={'offense': "Performance Offensive", 'defense': "Performance Défensive"}
    )
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(coloraxis_colorbar=dict(title="Rating"))

    st.plotly_chart(fig, use_container_width=True)
