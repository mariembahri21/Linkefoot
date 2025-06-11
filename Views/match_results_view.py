import streamlit as st
import pandas as pd
from datetime import datetime
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from streamlit_autorefresh import st_autorefresh

# --- Fonction pour récupérer les matchs ---
def get_matches_by_date(selected_date):
    url = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{selected_date}"

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = uc.Chrome(options=options)
        driver.get(url)
        json_data = driver.find_element(By.TAG_NAME, "pre").text
        driver.quit()
        data = json.loads(json_data)
    except Exception as e:
        st.error(f"Erreur lors de la récupération : {e}")
        return []

    if "events" not in data:
        return []

    matches = []
    for event in data["events"]:
        try:
            matches.append({
                "country": event["tournament"]["category"]["name"],
                "competition": event["tournament"]["name"],
                "home": event["homeTeam"]["name"],
                "away": event["awayTeam"]["name"],
                "score": f"{event['homeScore']['current']} - {event['awayScore']['current']}" if event.get("homeScore") else "–",
                "status": event["status"]["description"].lower()
            })
        except:
            continue

    return matches

# --- Affichage Streamlit ---
def display():
    st.title("📅 Résultats des matchs par jour")

    # Rafraîchissement automatique toutes les 30 minutes
    st_autorefresh(interval=1800000, limit=None, key="match_autorefresh")

    # Date par défaut = aujourd’hui
    today = datetime.today().date()
    min_date = datetime(2025, 5, 15).date()

    # Sélection de la date
    st.subheader("📌 Filtres")
    selected_date = st.date_input("Sélectionnez une date :", today, min_value=min_date, max_value=today)

    # Récupération des matchs
    with st.spinner(f"Chargement des matchs pour {selected_date}..."):
        matches = get_matches_by_date(selected_date.isoformat())

    if not matches:
        st.info("Aucun match trouvé pour cette date.")
        return

    df = pd.DataFrame(matches)

    # Affichage des filtres dans la page (pas dans la sidebar)
    all_statuses = df["status"].dropna().unique().tolist()
    selected_status = st.multiselect(
        "Filtrer par statut de match (optionnel) :", options=all_statuses
    )

    # Filtrage si l'utilisateur a sélectionné quelque chose
    if selected_status:
        df = df[df["status"].isin(selected_status)]

    if df.empty:
        st.warning("Aucun match ne correspond aux critères sélectionnés.")
        return

    # Groupement par pays et compétition
    grouped = df.groupby(["country", "competition"])

    for (country, competition), group in grouped:
        st.markdown(f"### 🌍 {country} – *{competition}*")
        for _, row in group.iterrows():
            st.markdown(
                f"<div style='padding:5px;border-bottom:1px solid #444;'>"
                f"<b>{row['home']}</b> {row['score']} <b>{row['away']}</b> "
                f"<span style='float:right; color:gray;'>({row['status'].capitalize()})</span>"
                f"</div>", unsafe_allow_html=True
            )

