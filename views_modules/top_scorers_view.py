import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_player_data

def top_scorers_view():
    st.subheader("🎯 Top 5 Buteurs")

    df = load_player_data()

    # Sélection filtres
    col1, col2, col3 = st.columns(3)
    leagues = sorted(df['league'].dropna().unique())
    positions = sorted(df['position'].dropna().unique())
    age_groups = ['< 21', '21-25', '26-30', '> 30']

    selected_league = col1.selectbox("Ligue", leagues, key="top_scorers_league")
    selected_position = col2.selectbox("Poste", positions, key="top_scorers_position")
    selected_age = col3.selectbox("Tranche d’âge", age_groups, key="top_scorers_age")

    # Filtrage
    df_filtered = df[df['league'] == selected_league]
    df_filtered = df_filtered[df_filtered['position'] == selected_position]

    if selected_age == '< 21':
        df_filtered = df_filtered[df_filtered['age'] < 21]
    elif selected_age == '21-25':
        df_filtered = df_filtered[(df_filtered['age'] >= 21) & (df_filtered['age'] <= 25)]
    elif selected_age == '26-30':
        df_filtered = df_filtered[(df_filtered['age'] > 25) & (df_filtered['age'] <= 30)]
    else:
        df_filtered = df_filtered[df_filtered['age'] > 30]

    # Trier par buts
    top_df = df_filtered.sort_values(by='p_goals', ascending=False).head(5)

    if top_df.empty:
        st.warning("Aucun joueur trouvé avec les filtres sélectionnés.")
        return

    fig = px.bar(
        top_df,
        x="name",
        y="p_goals",
        text="p_goals",
        color="overall_rating",
        color_continuous_scale="Turbo",
        title="🎯 Top 5 Buteurs (filtrés)",
        labels={"p_goals": "Buts", "name": "Joueur"}
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Voir les détails"):
        st.dataframe(top_df[['name', 'team', 'position', 'age', 'p_goals', 'assists', 'overall_rating']])

    st.markdown("---")
    st.subheader("🏅 Top 10 Buteurs (toutes ligues confondues)")

    df_top10 = df[df['p_goals'] > 0][['name', 'league', 'p_goals']].sort_values(by='p_goals', ascending=False).head(10)

    fig2 = px.bar(
        df_top10,
        x='name',
        y='p_goals',
        color='league',
        text='p_goals',
        title="Top 10 buteurs (global)",
        labels={'p_goals': 'Buts', 'name': 'Joueur'}
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(xaxis_tickangle=-30)

    st.plotly_chart(fig2, use_container_width=True)

