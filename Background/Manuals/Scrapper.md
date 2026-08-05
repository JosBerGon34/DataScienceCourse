# ==========================================================
# UNIVERSAL HTML TABLE SCRAPER
# ----------------------------------------------------------
# Purpose:
#     Download a rendered webpage and extract a table
#     identified by its column headers.
#
# Workflow:
#     URL
#        ↓
#     Playwright
#        ↓
#     HTML
#        ↓
#     BeautifulSoup
#        ↓
#     Find matching table
#        ↓
#     pandas.DataFrame
#
# Returns:
#     pandas.DataFrame
# ==========================================================

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd


async def scrape_table(
    url: str,
    expected_columns: list[str],
    headless: bool = True,
    executable_path: str = "/usr/bin/chromium",
    wait_until: str = "domcontentloaded"
) -> pd.DataFrame:
    """
    Download a webpage and extract a table using its header names.

    Parameters
    ----------
    url : str
        Target webpage URL.

    expected_columns : list[str]
        Column names used to identify the correct table.

    headless : bool
        Launch Chromium without GUI.

    executable_path : str
        Local Chromium executable.

    wait_until : str
        Page loading strategy.
        Options:
            "load"
            "domcontentloaded"
            "networkidle"

    Returns
    -------
    pandas.DataFrame
        Extracted table.
    """

    # ------------------------------------------
    # Download rendered HTML
    # ------------------------------------------

    pw = await async_playwright().start()

    browser = await pw.chromium.launch(
        executable_path=executable_path,
        headless=headless
    )

    page = await browser.new_page()

    await page.goto(
        url,
        wait_until=wait_until
    )

    html = await page.content()

    await browser.close()
    await pw.stop()

    # ------------------------------------------
    # Search every HTML table
    # ------------------------------------------

    soup = BeautifulSoup(html, "lxml")

    tables = soup.find_all("table")

    # ------------------------------------------
    # Find matching table
    # ------------------------------------------

    for table in tables:

        header = table.find("tr")

        if header is None:
            continue

        cells = header.find_all(["th", "td"])

        columns = [
            cell.get_text(strip=True)
            for cell in cells
        ]

        if all(col in columns for col in expected_columns):

            df = pd.read_html(
                StringIO(str(table))
            )[0]

            return df

    raise ValueError(
        "No table matching the expected columns was found."
    )

    
# ==========================================================
# Block 2 - User Configuration
# SCRAPER CONFIGURATION
# ==========================================================

URL = "https://es.wikipedia.org/wiki/ISO_3166-1_alfa-2"

EXPECTED_COLUMNS = [

    "Código",
    "Nombre del país",
    "Año",
    "ccTLD",
    "ISO 3166-2",
    "Notas"

]

OUTPUT_FILE = DATA_TABLES / "CountryNames.csv"

# ==========================================================
# Block 3 - Execute Scraper
# RUN SCRAPER
# ==========================================================

df = await scrape_table(
    url=URL,
    expected_columns=EXPECTED_COLUMNS
)

display(df.head())

print(f"\nRows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ==========================================================
# Block 4 - Save CSV
# SAVE DATAFRAME
# ==========================================================

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print(f"CSV successfully saved:\n{OUTPUT_FILE}")



