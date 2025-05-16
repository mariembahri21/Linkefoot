from playwright.sync_api import sync_playwright, TimeoutError
import pandas as pd



def scrape_best_and_worst_form():
    best_rows, worst_rows = [], []
    columns = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto("https://www.whoscored.com/statistics/teams", wait_until="domcontentloaded", timeout=60000)
        except TimeoutError:
            print("[Erreur] Timeout lors du chargement de la page.")
            browser.close()
            return None, None

      
        try:
            page.click("text=AGREE", timeout=3000)
        except:
            pass

        def scrape_form_table():
            rows_data = []
            nonlocal columns
            try:
                page.wait_for_selector("#forms-grid thead tr th", timeout=10000)
                headers = page.query_selector_all("#forms-grid thead tr th")
                columns = [header.inner_text().strip() for header in headers]
            except Exception as e:
                print(f"[Erreur] Lecture des en-têtes : {e}")
                return rows_data

            try:
                page.wait_for_selector("ul.statistics-pages.forms", timeout=10000)
                pagination_buttons = page.query_selector_all('ul.statistics-pages.forms li')
                total_pages = len(pagination_buttons)
            except:
                total_pages = 1

            for page_num in range(1, total_pages + 1):
                page.wait_for_timeout(1500)
                try:
                    rows = page.query_selector_all("#forms-grid tbody tr")
                    for row in rows:
                        cells = row.query_selector_all("td")
                        row_data = []

                        for i, cell in enumerate(cells):
                            if i == len(cells) - 1:
                                links = cell.query_selector_all("a")
                                form = ''.join([link.inner_text().strip().lower() for link in links])
                                row_data.append(form)
                            else:
                                row_data.append(cell.inner_text().strip())
                        if row_data:
                            rows_data.append(row_data)
                except Exception as e:
                    print(f"[Erreur] Scraping à la page {page_num} : {e}")

                if page_num < total_pages:
                    try:
                        page.click(f'ul.statistics-pages.forms li[data-value="{page_num + 1}"]')
                        page.wait_for_timeout(1500)
                    except Exception as e:
                        print(f"[Avertissement] Impossible de changer de page : {e}")
                        break

            return rows_data

     
        print("[Info] Scraping 'Best Form'...")
        best_rows = scrape_form_table()

   
        try:
            print("[Info] Passage à l'onglet 'Worst Form'...")
            page.click("#forms-tab > li:nth-child(2) > a") 
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"[Erreur] Impossible de cliquer sur l'onglet Worst : {e}")
            browser.close()
            return pd.DataFrame(best_rows, columns=columns), None

      
        print("[Info] Scraping 'Worst Form'...")
        worst_rows = scrape_form_table()

        browser.close()

    df_best_form = pd.DataFrame(best_rows, columns=columns)
    df_worst_form = pd.DataFrame(worst_rows, columns=columns)


    output_file = "team_forms.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_best_form.to_excel(writer, sheet_name='Best Form', index=False)
        df_worst_form.to_excel(writer, sheet_name='Worst Form', index=False)

    print(f"[Succès] Données enregistrées dans '{output_file}'")
    return df_best_form, df_worst_form




def scrape_best_and_worst_teams_performance():
    best_rows, worst_rows = [], []
    columns = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto("https://www.whoscored.com/statistics/teams", wait_until="domcontentloaded", timeout=60000)
        except TimeoutError:
            print("[Erreur] Timeout lors du chargement de la page.")
            browser.close()
            return None, None

        try:
            page.click("text=AGREE", timeout=3000)
        except:
            pass  
        def scrape_table():
            rows_data = []
            try:
                headers = page.query_selector_all("#performances-grid thead tr th")
                nonlocal columns
                columns = [header.inner_text().strip() for header in headers]
            except Exception as e:
                print(f"[Erreur] Impossible de lire les en-têtes : {e}")
                return rows_data

            try:
                page.wait_for_selector("#performances > ul", timeout=10000)
                pagination_buttons = page.query_selector_all('#performances > ul li')
                total_pages = len(pagination_buttons)
            except:
                total_pages = 1

            for page_num in range(1, total_pages + 1):
                page.wait_for_timeout(1500)
                try:
                    rows = page.query_selector_all("#performances-grid > tbody > tr")
                    for row in rows:
                        cells = row.query_selector_all("td")
                        row_data = [cell.inner_text().strip() for cell in cells]
                        if row_data:
                            rows_data.append(row_data)
                except Exception as e:
                    print(f"[Erreur] à la page {page_num} : {e}")

                if page_num < total_pages:
                    try:
                        page.click(f'#performances > ul [data-value="{page_num + 1}"]')
                        page.wait_for_timeout(1500)
                    except:
                        break
            return rows_data

   
        print("[Info] Scraping du tableau 'Best' en cours...")
        best_rows = scrape_table()


        try:
            print("[Info] Passage à l'onglet 'Worst'...")
            page.click("#performances-type > li:nth-child(2) > a")  
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"[Erreur] Impossible de cliquer sur 'Worst' : {e}")
            browser.close()
            return pd.DataFrame(best_rows, columns=columns), None

        print("[Info] Scraping du tableau 'Worst' en cours...")
        worst_rows = scrape_table()

        browser.close()

    df_best_form = pd.DataFrame(best_rows, columns=columns)
    df_worst_form = pd.DataFrame(worst_rows, columns=columns)

 
    output_file = "teams_pefrormnace.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_best_form.to_excel(writer, sheet_name='Best Performance', index=False)
        df_worst_form.to_excel(writer, sheet_name='Worst Performance', index=False)

    print(f"[Succès] Données enregistrées dans '{output_file}'")
    return df_best_form, df_worst_form



def scrape_teams_statistics():
    all_rows = []
    columns = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.whoscored.com/statistics", wait_until="domcontentloaded", timeout=60000)

      
        try:
            page.click("text=AGREE")
        except:
            pass
        page.wait_for_timeout(6000)
        try:
            button=page.query_selector("body > div.webpush-swal2-container.webpush-swal2-center.webpush-swal2-fade.webpush-swal2-shown > div > div.webpush-swal2-header > button")
            button.click()
        except:
            pass

 
        page.wait_for_selector("#top-team-stats-summary")

   
        headers = page.query_selector_all("#top-team-stats-summary-grid > thead > tr")
        columns = [header.inner_text().strip() for header in headers[0].query_selector_all("th")]

        while True:
            page.wait_for_timeout(2000)
            rows = page.query_selector_all("#top-team-stats-summary-content > tr")
            for row in rows:
                player_data = [cell.inner_text().strip() for cell in row.query_selector_all("td")]
                all_rows.append(player_data)

            next_button = page.query_selector("#next")
            if next_button and "disabled" not in next_button.get_attribute("class"):
                next_button.click()
            else:
                break

        browser.close()
    df= pd.DataFrame(all_rows, columns=columns)
    output_file = "teams_stats.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    print(f"[Succès] Données enregistrées dans '{output_file}'")
    return df
    
    



