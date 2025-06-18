# views_modules/top_clubs_by_league.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_player_data

def top_clubs_by_league_view():
    st.subheader("🏆 Top Clubs par Ligue")

    df = load_player_data()

    if 'league' not in df.columns or 'team' not in df.columns or 'points' not in df.columns:
        st.error("Le dataset ne contient pas toutes les colonnes nécessaires.")
        return

    leagues = sorted(df['league'].dropna().unique())
    selected_league = st.selectbox("🌍 Sélectionner une ligue", leagues, key="league_topclubs")

    metric = st.radio("📊 Critère de classement", ['points', 'goals_for'], horizontal=True, key="metric_topclubs")

    df_league = df[df['league'] == selected_league]

    df_agg = df_league.groupby('team')[[metric]].max().reset_index()

    top_teams = df_agg.sort_values(by=metric, ascending=False).head(10)

    fig = px.bar(
        top_teams,
        x='team',
        y=metric,
        text=metric,
        color=metric,
        color_continuous_scale='Viridis',
        title=f"🔝 Top 10 clubs – {metric.replace('_', ' ').capitalize()} ({selected_league})"
    )
    fig.update_layout(xaxis_title="Équipe", yaxis_title=metric.capitalize())
    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Voir les données"):
        st.dataframe(top_teams.reset_index(drop=True))
