# ⚽ Football Performance Analysis

This project scrapes and analyzes football (soccer) performance data from multiple sources, including **WhoScored** and **Fbref**, to help analyze teams, players, and leagues across the Big 5 European leagues.

---

## 📂 Project Structure


---

## 🚀 How to Run
1. **install the Data**

    The data used for this project can be downloaded [here](https://drive.google.com/drive/folders/1dajtz-wJK6Ipsyo7Vi9GpCWQ3LcyDllZ?usp=drive_link).


2. **Install dependencies**  
   Make sure you're in your virtual environment and run:
    pip install -r requirements.txt

   Run the scraper:
    To scrape data from WhoScored and Fbref:
    python main.py
    Output will be logged to logs/scraping.log.

## 📊 Data Sources

- WhoScored

- Fbref

Data is exported into Excel files (.xlsx) for further analysis.

## 🔧 Features

Modular scraping structure (players & teams per source)

Multi-source integration (WhoScored & Fbref)

Clean Excel exports for easy processing


✅ To-Do

 Clean and preprocess raw data

 Explore and visualize data insights

 Compare player and team performance across leagues

 Build metrics and models for advanced analysis