import pandas as pd
import streamlit as st

@st.cache_data
def load_player_data():
    df = pd.read_excel("merged_players.xlsx")
    return df
