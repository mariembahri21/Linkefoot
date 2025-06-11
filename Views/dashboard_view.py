import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

# ---- Load Your Dataset ----
@st.cache_data
def load_player_data():
    # Replace this with your real dataset path or method
    df = pd.read_csv("")
    return df

def show_radar_chart(player_stats, metrics):
    fig = go.Figure()

    for player in player_stats['player_name'].unique():
        values = player_stats[player_stats['player_name'] == player][metrics].values.flatten().tolist()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics,
            fill='toself',
            name=player
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
 

def display():
    st.title("⚽ Top Player Explorer")

    df = load_player_data()

    # ---- Filters ----
    leagues = df['league'].dropna().unique()
    positions = df['position'].dropna().unique()
    age_groups = ['< 21', '21-25', '26-30', '> 30']

    col1, col2, col3 = st.columns(3)
    selected_league = col1.selectbox("Select League", sorted(leagues))
    selected_position = col2.selectbox("Select Position", sorted(positions))
    selected_age = col3.selectbox("Select Age Group", age_groups)

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
    metrics = ['goals', 'assists', 'rating', 'market_value']
    display_df = df_filtered[['player_name', 'team', 'position', 'age'] + metrics].sort_values(by='rating', ascending=False).reset_index(drop=True)

    st.subheader("📊 Top Players Table")
    gb = GridOptionsBuilder.from_dataframe(display_df)
    gb.configure_pagination()
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_options = gb.build()

    grid_response = AgGrid(display_df, gridOptions=grid_options, update_mode=GridUpdateMode.SELECTION_CHANGED)
    selected = grid_response["selected_rows"]

    # ---- Radar Chart ----
    if selected:
        st.subheader("📈 Radar Comparison")
        selected_df = pd.DataFrame(selected)
        show_radar_chart(selected_df, metrics)
