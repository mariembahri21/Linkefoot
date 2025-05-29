import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def scrape_sofifa():
    data = []
    headers = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://sofifa.com/teams?&showCol%5B%5D=oa&showCol%5B%5D=at&showCol%5B%5D=md&showCol%5B%5D=df&showCol%5B%5D=ps&showCol%5B%5D=sa&showCol%5B%5D=ti&showCol%5B%5D=cw&showCol%5B%5D=ip&showCol%5B%5D=dp&showCol%5B%5D=bs&showCol%5B%5D=bd&showCol%5B%5D=bp&showCol%5B%5D=bps&showCol%5B%5D=cc&showCol%5B%5D=cp&showCol%5B%5D=cs&showCol%5B%5D=cps&showCol%5B%5D=da", wait_until="domcontentloaded")

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

    df.to_excel("sofifa_teams.xlsx", index=False)
    print("✅ Scraping complete. .")
    return df


if __name__ == "__main__":
    df_result = asyncio.run(scrape_sofifa())
    print(df_result.head())
