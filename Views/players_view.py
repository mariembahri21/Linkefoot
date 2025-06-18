import streamlit as st
import pandas as pd
import os

def load_players_data():
    file_path = os.path.join("data/cleaned/sofifa/sofifa_players.xlsx")
    return pd.read_excel(file_path)

def display_player_card(player):
    with st.container():
        st.markdown(
            f"""
            <div style='background-color:#1e1e1e;padding:1em;border-radius:10px;color:white;text-align:center;'>
                <img src="{player['picture']}" width="100" style="border-radius: 10px;" />
                <h4>{player['name']}</h4>
                <p>{player['team']}<br>{player['positions']} | {player['age']} ans</p>
                <p>⭐ {player['overall_rating']}</p>
            </div>
            """, unsafe_allow_html=True
        )

        with st.expander("Voir plus"):
            st.markdown(f"""
            **Taille**: {player.get('height', 'N/A')} cm  
            **Poids**: {player.get('weight', 'N/A')} kg  
            **Pied préféré**: {player.get('foot', 'N/A')}  
            **Potentiel**: {player.get('potential', 'N/A')}  
            **Valeur marchande**: {player.get('market_value_m', 'N/A')} M€  
            **Salaire**: {player.get('wage_k', 'N/A')} K€  
            **Positionnement**: {player.get('best_position', 'N/A')}  
            **Body type**: {player.get('body_type', 'N/A')}  
            **Vitesse**: {player.get('sprint_speed', 'N/A')}
            """)

def display():
    st.title("📋 Liste des Joueurs")

    df = load_players_data()

    # --- Search bar and dropdown ---
    st.subheader("🔎 Rechercher un joueur")
    search = st.text_input("Tapez un nom de joueur")
    player_names = df["name"].dropna().unique()
    selected_from_list = st.selectbox("Ou sélectionnez depuis la liste :", [""] + sorted(player_names))

    if search:
        df = df[df["name"].str.contains(search, case=False, na=False)]
    elif selected_from_list:
        df = df[df["name"] == selected_from_list]

    # --- Pagination setup ---
    page_size = 9
    if "player_page" not in st.session_state:
        st.session_state.player_page = 1

    total_pages = (len(df) - 1) // page_size + 1
    start = (st.session_state.player_page - 1) * page_size
    end = start + page_size
    current_df = df.iloc[start:end]

    # --- Display player cards in rows of 3 ---
    for i in range(0, len(current_df), 3):
        row = current_df.iloc[i:i + 3]
        cols = st.columns(3)
        for idx, player in enumerate(row.iterrows()):
            with cols[idx]:
                display_player_card(player[1])

    # --- Pagination controls ---
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.player_page > 1:
            if st.button("⬅️ Page précédente"):
                st.session_state.player_page -= 1
    with col3:
        if st.session_state.player_page < total_pages:
            if st.button("➡️ Page suivante"):
                st.session_state.player_page += 1
