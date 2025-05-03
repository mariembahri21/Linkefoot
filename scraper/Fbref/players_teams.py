import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def scrape_fbref_tables(url, table_id, output_filename):
    # Configurer le navigateur (Chrome headless)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        # Aller sur la page
        driver.get(url)
        time.sleep(5)  # Tu peux remplacer par WebDriverWait pour plus de robustesse

        # Récupérer le HTML
        soup = BeautifulSoup(driver.page_source, "html.parser")
    finally:
        driver.quit()

    # Extraire le tableau
    table = soup.find("table", id=table_id)
    if table is None:
        print(f"❌ Tableau avec l'ID '{table_id}' non trouvé.")
        return

    df = pd.read_html(str(table))[0]

    # Aplatir les colonnes si MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]

    # Exporter
    df.to_excel(output_filename, index=False)
    print(f"✅ Fichier Excel créé : {output_filename}")
    print(df.head())