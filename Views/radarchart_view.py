import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 📥 Load the player data
@st.cache_data
def load_players_data():
    file_path = os.path.join("data/cleaned/sofifa/sofifa_players_cleaned.xlsx")
    return pd.read_excel(file_path)

# 📊 Radar chart comparison function
def radar_chart_comparison(df):
    st.header("📊 Player Radar Comparison")

    # Player selection
    player_names = df['name'].unique()
    player1 = st.selectbox("Choose Player 1", player_names)
    player2 = st.selectbox("Choose Player 2", player_names, index=1)

    # Radar attributes (customize as needed)
    radar_features = [
        'overall_rating', 'potential', 'acceleration', 'sprint_speed',
        'agility', 'reactions', 'ball_control', 'stamina',
        'short_passing', 'finishing'
    ]
    st.markdown("Choose stats to compare:")
    selected_features = st.multiselect("Attributes", radar_features, default=radar_features)

    # Get stats
    p1_data = df[df['name'] == player1][selected_features].mean()
    p2_data = df[df['name'] == player2][selected_features].mean()

    categories = selected_features + [selected_features[0]]  # close the radar circle

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=list(p1_data) + [p1_data[0]],
        theta=categories,
        fill='toself',
        name=player1
    ))

    fig.add_trace(go.Scatterpolar(
        r=list(p2_data) + [p2_data[0]],
        theta=categories,
        fill='toself',
        name=player2
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

# 🚀 Main display function for Streamlit routing
def display():
    df = load_players_data()
    radar_chart_comparison(df)
