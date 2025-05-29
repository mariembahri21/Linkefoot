import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def scrape_sofifa():
    data = []
    headers = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://sofifa.com/leagues", wait_until="domcontentloaded")

        await page.wait_for_selector("table")

        # Get headers
        header_row = await page.query_selector("table > thead > tr")
        header_cells = await header_row.query_selector_all("th")
        for cell in header_cells:
            text = await cell.inner_text()
            headers.append(text.strip())
        headers.append("Picture URL")

        # Pagination loop
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


        await browser.close()

    df = pd.DataFrame(data)

    df.to_excel("sofifa_leagues.xlsx", index=False)
    print("✅ Scraping complete. .")
    return df


if __name__ == "__main__":
    df_result = asyncio.run(scrape_sofifa())
    print(df_result.head())
