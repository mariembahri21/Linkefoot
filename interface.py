import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Football Dashboard", layout="wide")

def convert_currency(val):
    if isinstance(val, str):
        val = val.replace("€", "").replace(",", "").strip()
        if val.endswith("M"):
            return float(val[:-1]) * 1_000_000
        elif val.endswith("K"):
            return float(val[:-1]) * 1_000
        else:
            try:
                return float(val)
            except:
                return 0.0
    return val

# 📦 Chargement des données
@st.cache_data
def load_data():
    return pd.read_excel("data/cleaned/sofifa/sofifa_players_clnd.xlsx")

df = load_data()

# 🔧 Prétraitement
df["Overall rating"] = pd.to_numeric(df["Overall rating"], errors="coerce")
df["Potential"] = pd.to_numeric(df["Potential"], errors="coerce")
df["Value"] = df["Value"].apply(convert_currency)
df["Wage"] = df["Wage"].apply(convert_currency)


# 📷 Fonction pour vérifier les images
def check_image_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except:
        return False

def show_player_image(url, width=100):
    default_image = "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"
    if check_image_url(url):
        st.image(url, width=width)
    else:
        st.image(default_image, width=width)

# 🎯 Sidebar - Filtres
st.sidebar.title("🎯 Filtres")
search = st.sidebar.text_input("🔍 Rechercher un joueur")
teams = st.sidebar.multiselect("Équipe", df["Team"].unique(), default=df["Team"].unique())
positions = st.sidebar.multiselect("Poste", df["Positions"].unique(), default=df["Positions"].unique())
min_rating = st.sidebar.slider("Note minimale", 0, 100, 0)

# 🔍 Filtrage des données
df_filtered = df[
    df["Name"].str.lower().str.contains(search.lower()) &
    df["Team"].isin(teams) &
    df["Positions"].isin(positions) &
    (df["Overall rating"] >= min_rating)
]

# 🔺 Pagination
players_per_page = 10
if "page" not in st.session_state:
    st.session_state.page = 1

total_pages = max(1, (len(df_filtered) - 1) // players_per_page + 1)
start = (st.session_state.page - 1) * players_per_page
end = start + players_per_page
current_players = df_filtered.iloc[start:end]

# 🏆 Titre
st.title("⚽ Football Player Explorer")

# 👤 Affichage des joueurs
for _, player in current_players.iterrows():
    with st.container():
        cols = st.columns([1, 3])
        with cols[0]:
            show_player_image(player["Picture URL"], width=100)
        with cols[1]:
            st.markdown(f"### {player['Name']} ({player['Age']} ans)")
            st.markdown(f"**Poste :** {player['Positions']} &nbsp;&nbsp; | &nbsp;&nbsp; **Équipe :** {player['Team']}")
            st.markdown(f"**Note :** {player['Overall rating']} &nbsp;&nbsp; | &nbsp;&nbsp; **Potentiel :** {player['Potential']}")
            st.markdown(f"**Contrat :** {player['Contract Dates']}")
            st.markdown(f"**Valeur :** {player['Value']} &nbsp;&nbsp; | &nbsp;&nbsp; **Salaire :** {player['Wage']}")

            with st.expander("📊 Voir les statistiques clés"):
                st.write(f"- 🧠 Réactions : {player['Reactions']}")
                st.write(f"- 🎯 Passes courtes : {player['Short passing']}")
                st.write(f"- 🏃‍♂️ Vitesse : {player['Sprint speed']}")
                st.write(f"- 🔥 Puissance tir : {player['Shot power']}")
                st.write(f"- 💪 Force : {player['Strength']}")
                st.write(f"- 🧠 Mentalité : {player['Aggression']} / {player['Total mentality']}")

# ⏭️ Pagination stylisée
pagination_css = """
<style>
.pagination-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 2rem;
    padding: 1rem;
    background-color: #1e1e1e;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
}
.pagination-button {
    background-color: #333;
    color: white;
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
}
.pagination-button:hover {
    background-color: #555;
}
.pagination-text {
    color: white;
    font-size: 1rem;
}
</style>
"""

st.markdown(pagination_css, unsafe_allow_html=True)

col_space_left, col_main, col_space_right = st.columns([1, 8, 1])
with col_main:
    st.markdown('<div class="pagination-container">', unsafe_allow_html=True)

    col_prev, col_txt, col_next = st.columns([2, 2, 2])
    with col_prev:
        if st.button("⬅️ Précédent", key="prev", help="Page précédente"):
            if st.session_state.page > 1:
                st.session_state.page -= 1

    with col_txt:
        st.markdown(f'<p class="pagination-text">Page {st.session_state.page} sur {total_pages}</p>', unsafe_allow_html=True)

    with col_next:
        if st.button("Suivant ➡️", key="next", help="Page suivante"):
            if st.session_state.page < total_pages:
                st.session_state.page += 1

    st.markdown('</div>', unsafe_allow_html=True)
