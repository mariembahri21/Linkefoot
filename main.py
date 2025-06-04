import streamlit as st
from Views import players_view, teams_view, leagues_view, dashboard_view, big5_view, eu_players_view

st.set_page_config(page_title="Football Analytics", layout="wide")

# Session state to control navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar Navigation using buttons
st.sidebar.markdown("## Navigation")
if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"
if st.sidebar.button("👤 Players"):
    st.session_state.page = "Players"
if st.sidebar.button("🏟️ Teams"):
    st.session_state.page = "Teams"
if st.sidebar.button("🌍 Leagues"):
    st.session_state.page = "Leagues"
if st.sidebar.button("🌍 Big 5 leagues"):
    st.session_state.page = "Big_5_leagues"
if st.sidebar.button("⚽ European Players"):
    st.session_state.page = "European_Players"
if st.sidebar.button("📊 Dashboards"):
    st.session_state.page = "Dashboards"

# Display selected page
if st.session_state.page == "Home":
    st.title("Bienvenue sur le Football Analytics Dashboard ⚽")
    st.write("Utilisez la barre latérale pour naviguer entre les sections.")
elif st.session_state.page == "Players":
    players_view.display()
elif st.session_state.page == "Teams":
    teams_view.display()
elif st.session_state.page == "Leagues":
    leagues_view.display()
elif st.session_state.page == "Big_5_leagues":
    big5_view.display()
elif st.session_state.page == "European_Players":
    eu_players_view.display()
elif st.session_state.page == "Dashboards":
    dashboard_view.display()
