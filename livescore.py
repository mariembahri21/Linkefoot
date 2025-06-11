from playwright.sync_api import sync_playwright
from datetime import date

def get_matches_from_browser(target_date=None):
    if not target_date:
        target_date = date.today().isoformat()

    url = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{target_date}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # mettre headless=True si tu veux cacher la fenêtre
        context = browser.new_context()
        page = context.new_page()

        # Charge une page pour initier la session
        page.goto("https://www.sofascore.com/football/livescore")
        page.wait_for_timeout(5000)

        # Utiliser fetch depuis le navigateur lui-même (contourne les protections)
        response = page.evaluate(f"""
            async () => {{
                const res = await fetch("{url}");
                return await res.json();
            }}
        """)

        browser.close()

        # Analyse des données
        if "events" in response:
            for match in response["events"]:
                home = match["homeTeam"]["name"]
                away = match["awayTeam"]["name"]
                score = f"{match['homeScore']['current']} - {match['awayScore']['current']}" if match.get("homeScore") else "–"
                status = match["status"]["description"]
                tournament = match["tournament"]["name"]
                print(f"[{tournament}] {home} {score} {away} ({status})")
        else:
            print("Aucune donnée reçue.")
            print(response)

if __name__ == "__main__":
    get_matches_from_browser("2025-06-08")  # Change avec la date souhaitée
