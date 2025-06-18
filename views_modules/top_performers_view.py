# views_modules/top_performers.py
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from views_modules.radar_chart_view import show_radar_chart
from utils.data_loader import load_player_data

def top_performers_view():
    st.subheader("📊 Top Player Explorer")

    df = load_player_data()



    # ---- Filters ----
    leagues = df['league'].dropna().unique()
    positions = df['position'].dropna().unique()
    age_groups = ['< 21', '21-25', '26-30', '> 30']

    col1, col2, col3 = st.columns(3)
    selected_league = col1.selectbox("Ligue", sorted(leagues))
    selected_position = col2.selectbox("Poste", sorted(positions))
    selected_age = col3.selectbox("Tranche d'âge", age_groups)

    # ---- Filter Data ----
    df_filtered = df[df['league'] == selected_league]
    df_filtered = df_filtered[df_filtered['position'] == selected_position]

    if selected_age == '< 21':
        df_filtered = df_filtered[df_filtered['age'] < 21]
    elif selected_age == '21-25':
        df_filtered = df_filtered[(df_filtered['age'] >= 21) & (df_filtered['age'] <= 25)]
    elif selected_age == '26-30':
        df_filtered = df_filtered[(df_filtered['age'] > 25) & (df_filtered['age'] <= 30)]
    else:
        df_filtered = df_filtered[df_filtered['age'] > 30]

    # ---- Show Table with Metrics ----
    metrics = ['p_goals', 'assists', 'overall_rating', 'value_m']
    display_df = df_filtered[['name', 'team', 'position', 'age'] + metrics].sort_values(by='overall_rating', ascending=False).reset_index(drop=True)

    st.subheader("📋 Tableau des Performances")
    gb = GridOptionsBuilder.from_dataframe(display_df)
    gb.configure_pagination()
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_options = gb.build()

    grid_response = AgGrid(display_df, gridOptions=grid_options, update_mode=GridUpdateMode.SELECTION_CHANGED)
    selected = grid_response["selected_rows"]


