import pandas as pd
from scraper.Fbref.players_teams import scrape_fbref_tables
from scraper.whoscored.players import scrape_ligue1_players, scrape_whoscored_player_stats
from scraper.whoscored.teams import  scrape_best_and_worst_teams_performance,scrape_best_and_worst_form, scrape_teams_statistics

def run():
    #scrape_ligue1_players()
    #scrape_best_and_worst_teams_performance()
    #scrape_best_and_worst_form()
    #scrape_teams_statistics()
    #asyncio.run(scrape_whoscored_player_stats())
    scrape_fbref_tables(
        url="https://fbref.com/en/comps/Big5/misc/squads/Big-5-European-Leagues-Stats",
        table_id="stats_teams_misc_for",
        output_filename="Squad_Miscellaneous_Stats.xlsx")
    


if __name__ == "__main__":
    run()



# Set up logging
"""
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scraping.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    
    logging.info("Starting Football Performance Analysis scraping...")

    try:
        scrape_players()
        logging.info("Finished scraping Whoscored players.")
    except Exception as e:
        logging.error("Error during scrape_players: %s", str(e))

    try:
        scrape_teams()
        logging.info("Finished scraping Whoscored teams.")
    except Exception as e:
        logging.error("Error during scrape_teams: %s", str(e))

    # Optional: call other sources
    try:
        players_teams.scrape_fbref_players_teams()
        logging.info("Finished scraping Fbref players/teams.")
    except Exception as e:
        logging.error("Error during Fbref scrape: %s", str(e))

    logging.info("All scraping tasks completed.")
"""



