import streamlit as st
import pandas as pd
import os

def load_players_data():
    file_path = os.path.join("data/cleaned/sofascore/players.xlsx")
    return pd.read_excel(file_path)

def player_profile_view(player_name):
    st.title("Profil du Joueur")
    df = load_players_data()
    player = df[df['Name'] == player_name].iloc[0]

    st.markdown(
        f"""
        <div style='display: flex; align-items: center; gap: 2em;'>
            <img src="{player['Photo']}" width="150" style="border-radius: 10px;" />
            <div>
                <h2 style="color:#00b4d8;">{player['Name']}</h2>
                <p>Club : <strong>{player['Team']}</strong></p>
                <p>Position : <strong>{player['Position']}</strong></p>
                <p>Note globale : ⭐ {player['Overall_rating']}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Statistiques")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Buts", player.get('Goals', 'N/A'))
        st.metric("Passes", player.get('Assists', 'N/A'))
    with col2:
        st.metric("Matchs", player.get('Matches', 'N/A'))
        st.metric("Minutes jouées", player.get('Minutes', 'N/A'))

    st.markdown("<br><a href='main.py?page=Players' style='color:white;'>← Retour à la liste</a>", unsafe_allow_html=True)
