import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def scrape_fbref_tables(url, table_id, output_filename):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)  
        soup = BeautifulSoup(driver.page_source, "html.parser")
    finally:
        driver.quit()


    table = soup.find("table", id=table_id)
    if table is None:
        print(f"❌ Tableau avec l'ID '{table_id}' non trouvé.")
        return

    df = pd.read_html(str(table))[0]


    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]


    df.to_excel(output_filename, index=False)
    print(f"✅ Fichier Excel créé : {output_filename}")
    print(df.head())