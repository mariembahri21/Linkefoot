import streamlit as st
import pandas as pd
import os

def load_teams_data():
    file_path = os.path.join("data/cleaned/sofifa/sofifa_teams_clnd.xlsx")
    return pd.read_excel(file_path)

def display_team_card(team):
    st.markdown(
        f"""
        <div style='background-color:#1e1e1e;padding:1em;margin:1em 0;border-radius:10px;color:white;'>
        <div style='display: flex; gap: 1em; align-items: center;
                    background-color: #1e1e1e; padding: 1em; margin: 1em 0;
                    border-radius: 12px; color: white;'>
            <img src="{team['Picture_URL']}" style='width:80px;height:80px;border-radius: 50%; object-fit: cover;' />
            <div>
            <strong>{team['Team']}</strong><br>
            League: {team['League']}<br>
            Titles won: 🏆 {team['Titles_won']}
        </div>
        """,
        unsafe_allow_html=True,
    )

def display():
    st.title("Liste des Équipes")

    df = load_teams_data()

    search = st.text_input("🔎 Rechercher une équipe")
    if search:
        df = df[df["Team"].str.contains(search, case=False, na=False)]

    page_size = 10
    if "team_page" not in st.session_state:
        st.session_state.team_page = 1

    total_pages = (len(df) - 1) // page_size + 1
    start = (st.session_state.team_page - 1) * page_size
    end = start + page_size
    current_df = df.iloc[start:end]

    for _, team in current_df.iterrows():
        display_team_card(team)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.team_page > 1:
            if st.button("⬅️ Page précédente"):
                st.session_state.team_page -= 1
    with col3:
        if st.session_state.team_page < total_pages:
            if st.button("➡️ Page suivante"):
                st.session_state.team_page += 1
