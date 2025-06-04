import streamlit as st
import pandas as pd
import os

def load_players_data():
    file_path = os.path.join("data\cleaned\sofascore\players.xlsx")
    return pd.read_excel(file_path)

def display_player_card(player):
    st.markdown(
        f"""
        <div style='background-color:#1e1e1e;padding:1em;margin:1em 0;border-radius:12px;box-shadow: 0 4px 12px rgba(0,0,0,0.4);color:white;'>
            <div style='display: flex; gap: 1em; align-items: center;'>
                <img src="{player['Picture']}" style='width:90px;height:90px;border-radius:12px;object-fit: cover; border: 2px solid #555;' />
                <div>
                    <h3 style='margin: 0;'>{player['Name']}</h3>
                    <p style='margin: 0.25em 0;'>🏷️ League: {player['League']}</p>
                    <p style='margin: 0.25em 0;'>🏟️ Team: {player['Team']}</p>
                    <p style='margin: 0.25em 0;'>⚽ Goals: {player['Goals']}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def display():
    st.title("👟 Top European Players")

    df = load_players_data()

    page_size = 10
    if "players_page" not in st.session_state:
        st.session_state.players_page = 1

    total_pages = (len(df) - 1) // page_size + 1
    start = (st.session_state.players_page - 1) * page_size
    end = start + page_size
    current_df = df.iloc[start:end]

    for _, player in current_df.iterrows():
        display_player_card(player)

    # Pagination controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.players_page > 1:
            if st.button("⬅️ Previous"):
                st.session_state.players_page -= 1
                st.experimental_user()
    with col3:
        if st.session_state.players_page < total_pages:
            if st.button("Next ➡️"):
                st.session_state.players_page += 1
                st.experimental_user()
