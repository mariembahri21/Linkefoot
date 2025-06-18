import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_player_data

def team_rankings_view():
    st.subheader("🏆 Classement des équipes – Victoires & Défaites")

    df = load_player_data()

    # S'assurer que les colonnes nécessaires existent
    required_cols = ['team', 'league', 'wins', 'loses']
    if not all(col in df.columns for col in required_cols):
        st.error("Les colonnes nécessaires ne sont pas présentes dans le dataset.")
        return

    # Regrouper par équipe (certains datasets ont les lignes par joueur)
    agg_df = df.groupby(['team', 'league'], as_index=False).agg({
        'wins': 'max',
        'loses': 'max'
    })

    # Top 10 victoires
    top_wins = agg_df.sort_values(by='wins', ascending=False).head(10)

    # Top 10 défaites
    top_loses = agg_df.sort_values(by='loses', ascending=False).head(10)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Top 10 Équipes avec le plus de **Victoires**")
        fig1 = px.bar(
            top_wins,
            x='team',
            y='wins',
            color='league',
            text='wins',
            title="Top Victoires",
            labels={'wins': 'Victoires', 'team': 'Équipe'}
        )
        fig1.update_traces(textposition="outside")
        fig1.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### ❌ Top 10 Équipes avec le plus de **Défaites**")
        fig2 = px.bar(
            top_loses,
            x='team',
            y='loses',
            color='league',
            text='loses',
            title="Top Défaites",
            labels={'loses': 'Défaites', 'team': 'Équipe'}
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig2, use_container_width=True)
