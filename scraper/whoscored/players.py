from playwright.sync_api import sync_playwright
import pandas as pd
from playwright.async_api import async_playwright

def scrape_ligue1_players():
    all_rows = []
    columns = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.whoscored.com/statistics", wait_until="domcontentloaded", timeout=60000)

        # Accepter les cookies
        try:
            page.click("text=AGREE")
        except:
            pass

        # Navigation vers les joueurs
        page.wait_for_selector("#statistics-table-summary")

        # Récupération des en-têtes
        headers = page.query_selector_all("#player-table-statistics-head > tr")
        columns = [header.inner_text().strip() for header in headers[0].query_selector_all("th")]

        while True:
            page.wait_for_timeout(2000)
            rows = page.query_selector_all("#player-table-statistics-body > tr")
            for row in rows:
                player_data = [cell.inner_text().strip() for cell in row.query_selector_all("td")]
                all_rows.append(player_data)

            next_button = page.query_selector("#next")
            if next_button and "disabled" not in next_button.get_attribute("class"):
                next_button.click()
            else:
                break

        browser.close()



async def scrape_whoscored_player_stats():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.whoscored.com/statistics", wait_until="domcontentloaded", timeout=60000)

        # Accepter les cookies si le bouton existe
        try:
            await page.click("text=AGREE", timeout=5000)
        except:
            pass

        await page.click('#top-player-stats-options > li:nth-child(1) > a', timeout=60000)
        await page.wait_for_selector('#top-player-stats', timeout=10000)
        await page.click('#apps > dd:nth-child(2) > a', timeout=60000)

        await page.wait_for_selector("#player-table-statistics-head > tr", timeout=10000)
        header_row = await page.query_selector("#player-table-statistics-head > tr")
        columns = [await (await th.get_property("innerText")).json_value() for th in await header_row.query_selector_all("th")]

        all_data = []
        page_num = 1

        while True:
            print(f"📄 Scraping page {page_num}...")

            await page.wait_for_selector("#player-table-statistics-body > tr", timeout=10000)
            rows = await page.query_selector_all("#player-table-statistics-body > tr")

            for row in rows:
                cells = await row.query_selector_all("td")
                row_data = [await (await cell.get_property("innerText")).json_value() for cell in cells]
                if row_data:
                    all_data.append(row_data)

            try:
                # Utiliser le bon bouton "Next" par son conteneur unique
                next_locator = page.locator("#statistics-paging-summary #next")

                if await next_locator.count() == 0:
                    print("❌ Bouton 'Next' introuvable.")
                    break

                class_attr = await next_locator.get_attribute("class")
                if class_attr and "disabled" in class_attr:
                    print("✅ Dernière page atteinte.")
                    break
                    
                await page.wait_for_selector("#statistics-table-summary-loading", state="hidden", timeout=10000)

                # Scroll dans le champ de vision
                try:
                    await next_locator.scroll_into_view_if_needed()
                except:
                    pass

                try:
                    await next_locator.click()
                except Exception as click_error:
                    print("⚠️ Obstacle détecté lors du clic, tentative de suppression...")

                    # Supprimer des overlays pub s'ils bloquent
                    try:
                        ad_overlay = page.locator("#sn_gg_ad_wrapper, .popup-close, .overlay, .loading-spinner-container-shade")
                        if await ad_overlay.is_visible():
                            await ad_overlay.evaluate("el => el.remove()")
                            print("🧹 Élément bloquant supprimé")
                    except:
                        pass

                    # Réessayer le clic
                    await next_locator.click()

                await page.wait_for_timeout(2000)
                page_num += 1

            except Exception as e:
                print(f"❌ Erreur navigation : {e}")
                break

        await browser.close()

        # ✅ Création du DataFrame
        df = pd.DataFrame(all_data, columns=columns)
        print(f"✅ {len(df)} lignes collectées")

        # ✅ Sauvegarde Excel
        excel_file = "player_statistics.xlsx"
        df.to_excel(excel_file, index=False, engine="openpyxl")
        print(f"📁 Données sauvegardées dans '{excel_file}'")
    



