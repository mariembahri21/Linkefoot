import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_player_data

# Fonction utilitaire pour transformer last_5 en score moyen
def score_last_5(last5: str) -> float:
    score_map = {'w': 3, 'd': 1, 'l': 0}
    results = last5.lower().split("_")
    return round(sum(score_map.get(r, 0) for r in results) / len(results), 2) if results else None

# Fonction pour afficher l'évolution graphique des 5 derniers matchs
def plot_last_5_chart(last5_str, team_name):
    score_map = {'w': 3, 'd': 1, 'l': 0}
    results = last5_str.lower().split("_")
    scores = [score_map.get(r, 0) for r in results]
    matches = [f"Match {i+1}" for i in range(len(scores))]

    df_plot = pd.DataFrame({
        "Match": matches,
        "Score": scores
    })

    fig = px.line(df_plot, x="Match", y="Score", markers=True,
                  title=f"📉 Résultats des 5 derniers matchs – {team_name}",
                  labels={"Score": "Résultat (W=3, D=1, L=0)"})
    st.plotly_chart(fig, use_container_width=True)

def team_stats_view():
    st.subheader("🏟️ Vue Club – Statistiques par Équipe")

    df = load_player_data()

    # --- Filtres ---
    countries = sorted(df['league'].dropna().unique())
    selected_country = st.selectbox("🌍 Sélectionner une ligue/pays", countries)

    df_country = df[df['league'] == selected_country]
    teams = sorted(df_country['team'].dropna().unique())
    selected_team = st.selectbox("🏟️ Sélectionner un club", teams)

    df_team = df_country[df_country['team'] == selected_team]

    if df_team.empty:
        st.warning("Aucune donnée disponible pour cette équipe.")
        return

    # --- KPIs ---
    st.markdown("### 🔢 Statistiques globales du club")

    total_wins = df_team['wins'].max()
    total_draws = df_team['draws'].max()
    total_loses = df_team['loses'].max()
    total_goals_for = df_team['goals_for'].max()
    total_goals_against = df_team['goals_against'].max()
    goal_diff = df_team['difference'].max()
    total_points = df_team['points'].max()

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Victoires", total_wins)
    col2.metric("➖ Nuls", total_draws)
    col3.metric("❌ Défaites", total_loses)

    col4, col5, col6 = st.columns(3)
    col4.metric("⚽ Buts marqués", total_goals_for)
    col5.metric("🛡️ Buts encaissés", total_goals_against)
    col6.metric("📈 Différence de buts", goal_diff)

    st.metric("🏆 Points", total_points)

    # --- Forme récente ---
    if 'last_5' in df_team.columns:
        last5 = df_team['last_5'].dropna().iloc[0]
        st.markdown("### 📉 Derniers résultats du club")
        plot_last_5_chart(last5, selected_team)

        score = score_last_5(last5)
        st.metric("Score moyen (5 derniers matchs)", score)
    else:
        st.info("Aucune donnée de forme disponible.")
