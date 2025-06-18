#from views_modules.radar_chart_view import show_radar_chart
from views_modules.team_rankings_view import team_rankings_view
from views_modules.results_distribution_view import results_distribution_view
from views_modules.top_clubs_by_league_view import top_clubs_by_league_view

from views_modules.top_10_view import top_teams_stats_view
from views_modules.top_scorers_view import top_scorers_view
from views_modules.off_vs_def_view import off_vs_def_view
from views_modules.team_stats_view import team_stats_view
from views_modules.top_performers_view import top_performers_view
from views_modules.heatmap import heatmap_view
from views_modules.age_performance_view import age_performance_view
import streamlit as st


def dashboard_view():
    st.title("📊 Tableau de Bord – Football Analytics")

    tab1, tab2= st.tabs(["👤 Joueurs", "🏟️ Équipes"])

    with tab1:
        st.subheader("🎯 Top 5 Buteurs par Profil")
        top_scorers_view()
        st.subheader("Performance moyenne selon l’âge")
        age_performance_view()  # 👈 ajout ici
        st.subheader("Analyse Offensif vs Défensif des Joueurs")
        off_vs_def_view()  # 👈 ajout ici
        st.subheader("Top Performers")
        top_performers_view()



    with tab2:
        st.subheader("Répartition des Résultats")
        results_distribution_view()
        st.subheader("🏆 Top Clubs par Ligue")
        top_clubs_by_league_view()
        st.subheader("Statistiques par Club")
        team_stats_view()
        st.subheader("Heatmap des Statistiques Collectives")
        heatmap_view()
        st.markdown("📈 Classements des Victoires/Défaites")
        team_rankings_view()
        st.subheader("🏆 Statistiques Collectives des Équipes")
        top_teams_stats_view()
        





 
