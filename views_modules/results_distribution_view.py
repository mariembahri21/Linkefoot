import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_player_data

def results_distribution_view():
    st.subheader("📊 Répartition des Résultats (Win / Draw / Lose)")

    df = load_player_data()

    # Choix du mode
    mode = st.radio("Afficher les résultats par :", ["Ligue", "Équipe"])

    if mode == "Ligue":
        leagues = sorted(df['league'].dropna().unique())
        selected_league = st.selectbox("Choisir une ligue", leagues)
        df_filtered = df[df['league'] == selected_league]

        agg_results = df_filtered.groupby('league')[['wins', 'draws', 'loses']].sum().reset_index()
        row = agg_results.iloc[0]
        data = pd.DataFrame({
            "Résultat": ['Victoires', 'Nuls', 'Défaites'],
            "Nombre": [row['wins'], row['draws'], row['loses']]
        })

    else:
        teams = sorted(df['team'].dropna().unique())
        selected_team = st.selectbox("Choisir une équipe", teams)
        df_filtered = df[df['team'] == selected_team]

        if df_filtered.empty:
            st.warning("Aucune donnée disponible pour cette équipe.")
            return

        # On suppose que les colonnes sont les mêmes pour tous les joueurs d'une équipe
        row = df_filtered.iloc[0]
        data = pd.DataFrame({
            "Résultat": ['Victoires', 'Nuls', 'Défaites'],
            "Nombre": [row['wins'], row['draws'], row['loses']]
        })

    # Affichage Pie Chart
    fig = px.pie(
        data,
        names="Résultat",
        values="Nombre",
        hole=0.4,
        color="Résultat",
        title=f"Répartition des résultats - {selected_league if mode == 'Ligue' else selected_team}",
        color_discrete_map={
            'Victoires': '#00b894',
            'Nuls': '#fdcb6e',
            'Défaites': '#d63031'
        }
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
