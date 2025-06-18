import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import json
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# Load data and models
def load_data_and_models():
    df = pd.read_csv(os.path.join("data", "clustered_players.csv"))
    scaler = joblib.load(os.path.join("models", "scaler.pkl"))
    pca = joblib.load(os.path.join("models", "pca.pkl"))
    hdbscan_model = joblib.load(os.path.join("models", "hdbscan_model.pkl"))
    
    with open(os.path.join("models", "features_used.json")) as f:
        features = json.load(f)

    return df, scaler, pca, hdbscan_model, features

# Find similar players using cosine similarity
def find_similar_players(df, scaler, player_name, features, top_n=5):
    X_scaled = scaler.transform(df[features])
    idx = df[df['name'] == player_name].index[0]
    player_vector = X_scaled[idx].reshape(1, -1)
    similarities = cosine_similarity(player_vector, X_scaled).flatten()
    similar_indices = np.argsort(similarities)[::-1][1:top_n+1]
    return df.loc[similar_indices, ['name', 'team', 'league', 'cluster']], similarities[similar_indices]

# Radar chart between two players
def radar_plot(df, scaler, player1_name, player2_name, features):
    X_scaled = scaler.transform(df[features])
    idx1 = df[df['name'] == player1_name].index[0]
    idx2 = df[df['name'] == player2_name].index[0]

    stats1 = X_scaled[idx1]
    stats2 = X_scaled[idx2]

    labels = features
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    stats1 = np.concatenate((stats1, [stats1[0]]))
    stats2 = np.concatenate((stats2, [stats2[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, stats1, label=player1_name)
    ax.plot(angles, stats2, label=player2_name)
    ax.fill(angles, stats1, alpha=0.25)
    ax.fill(angles, stats2, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.legend()
    return fig

# Main display function for Streamlit
def display():
    st.title("🔍 Analyse de Similarité des Joueurs")

    df, scaler, pca, hdbscan_model, features = load_data_and_models()

    player_names = df['name'].unique()
    selected_player = st.selectbox("Choisissez un joueur", sorted(player_names))

    if selected_player:
        top_n = st.slider("Nombre de joueurs similaires à afficher", 1, 10, 5)
        similar_df, scores = find_similar_players(df, scaler, selected_player, features, top_n=top_n)

        st.write("### Joueurs les plus similaires")
        st.dataframe(similar_df)

        player_to_compare = st.selectbox("Comparer avec :", sorted(player_names))
        st.pyplot(radar_plot(df, scaler, selected_player, player_to_compare, features))
