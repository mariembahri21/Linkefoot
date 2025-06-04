import streamlit as st
import pandas as pd
import os

def load_big5_data():
    file_path = os.path.join("data/cleaned/sofascore/Big5.xlsx")
    return pd.read_excel(file_path)

def display_big5_card(league):
    st.markdown(
        f"""
        <div style='background-color:#1e1e1e;padding:1em;margin:1em 0;border-radius:10px;color:white;'>
            <div style='display: flex; gap: 1em; align-items: center;'>
                <img src="{league['Picture']}" style='width:80px;height:80px;border-radius: 50%; object-fit: cover;' />
                <div>
                    <h3 style='margin: 0;'>{league['League']}</h3>
                    <p style='margin: 0;'>🌍 Country: {league['Country']}<br>
                    🏅 Rank: {league['Rank']}</p>
                    <p style='margin-top: 0.5em;'>{league['Description']}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def display():
    st.title("🏆 Les 5 Grandes Ligues Européennes")

    df = load_big5_data().sort_values("Rank")  # Ensure sorted by rank


    page_size = 5  # Only 5 items max anyway
    if "big5_page" not in st.session_state:
        st.session_state.big5_page = 1

    total_pages = (len(df) - 1) // page_size + 1
    start = (st.session_state.big5_page - 1) * page_size
    end = start + page_size
    current_df = df.iloc[start:end]

    for _, league in current_df.iterrows():
        display_big5_card(league)


