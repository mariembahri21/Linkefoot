import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def scrape_sofifa():
    data = []
    headers = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://sofifa.com/players?col=tt&sort=desc&showCol%5B%5D=pi&showCol%5B%5D=ae&showCol%5B%5D=hi&showCol%5B%5D=wi&showCol%5B%5D=pf&showCol%5B%5D=oa&showCol%5B%5D=pt&showCol%5B%5D=bo&showCol%5B%5D=bp&showCol%5B%5D=jt&showCol%5B%5D=vl&showCol%5B%5D=wg&showCol%5B%5D=ta&showCol%5B%5D=cr&showCol%5B%5D=fi&showCol%5B%5D=he&showCol%5B%5D=sh&showCol%5B%5D=ts&showCol%5B%5D=tt&showCol%5B%5D=dr&showCol%5B%5D=cu&showCol%5B%5D=fr&showCol%5B%5D=lo&showCol%5B%5D=bl&showCol%5B%5D=to&showCol%5B%5D=ac&showCol%5B%5D=sp&showCol%5B%5D=ag&showCol%5B%5D=re&showCol%5B%5D=ba&showCol%5B%5D=tp&showCol%5B%5D=so&showCol%5B%5D=ju&showCol%5B%5D=st&showCol%5B%5D=sr&showCol%5B%5D=ln&showCol%5B%5D=ar&showCol%5B%5D=pe&showCol%5B%5D=te&showCol%5B%5D=td&showCol%5B%5D=ma&showCol%5B%5D=sa&showCol%5B%5D=sl&showCol%5B%5D=tg&showCol%5B%5D=bs&showCol%5B%5D=wk&showCol%5B%5D=sk&showCol%5B%5D=ir&showCol%5B%5D=bt", wait_until="domcontentloaded")

        await page.wait_for_selector("table")

        # Get headers
        header_row = await page.query_selector("table > thead > tr")
        header_cells = await header_row.query_selector_all("th")
        for cell in header_cells:
            text = await cell.inner_text()
            headers.append(text.strip())
        headers.append("Picture URL")

        # Pagination loop
        while True:
            await page.wait_for_selector("table")
            rows = await page.query_selector_all("table > tbody > tr")

            for row in rows:
                try:
                    cols = await row.query_selector_all("td")
                    row_data = {}
                    for i in range(min(len(headers) - 1, len(cols))):
                        value = await cols[i].inner_text()
                        row_data[headers[i]] = value.strip()

                    # Get image URL
                    img = await row.query_selector("td.a1 img")
                    image_url = await img.get_attribute("data-src") if img else None
                    row_data["Picture URL"] = image_url

                    data.append(row_data)
                except Exception as e:
                    print(f"Error scraping row: {e}")

            # Go to next page
            try:
                next_button = page.locator("text=Next ")
                if await next_button.is_visible():
                    await next_button.click()
                    await page.wait_for_timeout(1500)
                else:
                    break
            except Exception as e:
                print(f"No more pages or error: {e}")
                break

        await browser.close()

    df = pd.DataFrame(data)
    
    # ✅ Save to Parquet
    df.to_excel("sofifa_players.xslx", index=False)
    print("✅ Scraping complete")
    return df

# Example usage
if __name__ == "__main__":
    df_result = asyncio.run(scrape_sofifa())
    print(df_result.head())
