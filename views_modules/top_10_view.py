import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_player_data

def top_teams_stats_view():
    st.subheader("🏆 Statistiques Collectives des Équipes")

    df = load_player_data()

    if 'team' not in df.columns or 'league' not in df.columns:
        st.error("Colonnes nécessaires manquantes dans le dataset.")
        return

    df_team = df.groupby(['team', 'league']).agg({
        'goals_for': 'max',
        'goals_against': 'max'
    }).reset_index()

    # 🥇 Top 10 équipes offensives
    st.markdown("### ⚽ Top 10 équipes les plus offensives")
    top_attack = df_team.sort_values(by='goals_for', ascending=False).head(10)
    fig_attack = px.bar(
        top_attack, x='team', y='goals_for', color='league',
        title="Buts marqués par club",
        labels={'goals_for': 'Buts marqués', 'team': 'Équipe'}
    )
    st.plotly_chart(fig_attack, use_container_width=True)

    # 🛡️ Top 10 meilleures défenses
    st.markdown("### 🛡️ Top 10 meilleures défenses (moins de buts encaissés)")
    top_defense = df_team.sort_values(by='goals_against').head(10)
    fig_defense = px.bar(
        top_defense, x='team', y='goals_against', color='league',
        title="Buts encaissés par club",
        labels={'goals_against': 'Buts encaissés', 'team': 'Équipe'}
    )
    st.plotly_chart(fig_defense, use_container_width=True)
