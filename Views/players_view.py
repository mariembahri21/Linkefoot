# players_view.py

import streamlit as st
import pandas as pd
import os

def load_players_data():
    file_path = os.path.join("data/cleaned/sofifa/sofifa_players_clnd.xlsx")
    return pd.read_excel(file_path)

def display_player_card(player):
    player_name = player['Name']
    st.markdown(
        f"""
        <div style='background-color:#1e1e1e;padding:1em;margin:0.5em 0;border-radius:10px;color:white;'>
            <img src="{player['Picture_URL']}" width="100" style="border-radius: 10px;" />
            <h4>{player_name}</h4> Age: {player['Age']} ans<br>
            Club: {player['Team']}<br>
            Position: {player['Positions']}<br>
            Goals: {player['Goals']}<br>
            Assists: {player['Assists']}<br>
            Age: {player['Age']} ans<br>
            Rating: ⭐ {player['Overall_rating']}<br>
            <a href="?page=player_profile&name={player_name}" style="color:#00b4d8;">Voir le profil →</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display():  # <-- Ceci doit exister exactement avec ce nom
    st.title("Liste des Joueurs")

    df = load_players_data()

    search = st.text_input("🔎 Rechercher un joueur")
    if search:
        df = df[df["Name"].str.contains(search, case=False, na=False)]

    page_size = 10
    if "player_page" not in st.session_state:
        st.session_state.player_page = 1

    total_pages = (len(df) - 1) // page_size + 1
    start = (st.session_state.player_page - 1) * page_size
    end = start + page_size
    current_df = df.iloc[start:end]

    for _, player in current_df.iterrows():
        display_player_card(player)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.player_page > 1:
            if st.button("⬅️ Page précédente"):
                st.session_state.player_page -= 1
    with col3:
        if st.session_state.player_page < total_pages:
            if st.button("➡️ Page suivante"):
                st.session_state.player_page += 1
