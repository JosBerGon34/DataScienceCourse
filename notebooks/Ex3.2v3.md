```python
from pathlib import Path
import os
import pandas as pd
import random
#PATHING SCRIPT FOR EVERY EXCERSISE - PROJECT - WORKSPACE
# 1.Literal definition of route pathings(Every user of remote repository must config this pathing in order to find the local repository of his computer)
# My case:
ROOT = Path("/home/josu/Documentos/DataScienceCourse")

# We verify the existence before continue
if not ROOT.exists():
    raise FileNotFoundError(f"❌ The route {ROOT} doesn't exist. Check it.")

# 2. Fix the workspace
os.chdir(ROOT)
print(f"✅ Worskspace enabled!: {os.getcwd()}")

# 3. Define relative pathings to work properly
DATA_TABLES = ROOT / "data" / "raw" / "Tables"

# Let's verify our table folder:
if not DATA_TABLES.exists():
    # If it fails, monitorize the issue: 
    data_dir = ROOT / "data"
    if data_dir.exists():
        print(f"⚠️ the folder 'data' exists but it doesn't have any 'Tables'. 'data' content: {os.listdir(data_dir)}")
    else:
        print(f"⚠️ The folder 'data' doesn't exist on ROOT workspace: {os.listdir(ROOT)}")
    raise FileNotFoundError(f"❌ The tables route {DATA_TABLES} is missing.")

print(f"📂 Tables route detected: {DATA_TABLES}")

```

    ✅ Worskspace enabled!: /home/josu/Documentos/DataScienceCourse
    📂 Tables route detected: /home/josu/Documentos/DataScienceCourse/data/raw/Tables



```python
# ==========================================================
# KNOWLEDGE SCRAPER
# ----------------------------------------------------------
# BLOCK 1 - HTML DOWNLOADER
#
# Purpose:
#     Download the fully rendered HTML source of a webpage.
#
# Responsibilities:
#     - Launch Chromium
#     - Load the webpage
#     - Return HTML
#
# It DOES NOT:
#     - Parse HTML
#     - Search tables
#     - Search lists
#     - Build DataFrames
#
'''
URL
 │
 ▼
download_html()
 │
 ▼
HTML
 │
 ▼
BeautifulSoup
 │
 ▼
Dispatcher
 │
 ├──────────────┐
 ▼              ▼
TABLE      HIERARCHY(Enumerated text list from a Semantic Root)
 │              │
 ▼              ▼
DataFrame   DataFrame
'''
# Input
# -----
# url : str
#     Webpage URL.
#
# Output
# ------
# html : str
#     Complete rendered HTML source.
# ==========================================================

from playwright.async_api import async_playwright


async def download_html(
    url: str,
    executable_path: str = "/usr/bin/chromium",
    headless: bool = True,
    wait_until: str = "domcontentloaded"
) -> str:

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

    return html
```


```python
# ==========================================================
# KNOWLEDGE SCRAPER
# ----------------------------------------------------------
# BLOCK 2 - SCRAPER DISPATCHER
#
# Purpose:
#     Control the complete scraping workflow.
#
# Responsibilities:
#     - Download HTML
#     - Create BeautifulSoup object
#     - Select the appropriate extractor
#     - Return a DataFrame
#
'''
URL
 │
 ▼
download_html()
 │
 ▼
HTML
 │
 ▼
BeautifulSoup
 │
 ▼
Dispatcher
 │
 ├──────────────┐
 ▼              ▼
TABLE      HIERARCHY
 │              │
 ▼              ▼
DataFrame   DataFrame
'''
# Input
# -----
# source : dict
#
# Output
# ------
# pandas.DataFrame
# ==========================================================

from bs4 import BeautifulSoup
import gc


async def scrape_source(source):

    # ---------------------------------------------
    # Download webpage
    # ---------------------------------------------

    html = await download_html(source["url"])

    # ---------------------------------------------
    # Build BeautifulSoup once
    # ---------------------------------------------

    soup = BeautifulSoup(html, "lxml")

    # ---------------------------------------------
    # Dispatcher
    # ---------------------------------------------

    source_type = source["type"].lower()

    if source_type == "table":

        df = extract_table_from_soup(
            soup=soup,
            expected_columns=source["columns"]
        )

    elif source_type == "hierarchy":

        df = extract_hierarchy_from_soup(
            soup=soup,
            root=source["root"]
        )

    else:

        raise ValueError(
            f"Unknown source type: {source_type}"
        )

    # ---------------------------------------------
    # Memory cleanup
    # ---------------------------------------------

    del html
    del soup

    gc.collect()

    return df
```


```python
# ==========================================================
# KNOWLEDGE SCRAPER
# ----------------------------------------------------------
# BLOCK 3 - TABLE EXTRACTOR
#
# Purpose:
#     Extract HTML tables whose headers contain the expected
#     column names.
#
'''
download_html()

↓

html

↓

BeautifulSoup()

↓

extract_table_from_soup()

↓

DataFrame
'''
# Responsibilities:
#     - Search tables
#     - Match headers
#     - Convert HTML table to DataFrame
#     - Keep only requested columns
#
# Input
# -----
# soup : BeautifulSoup
#
# expected_columns : list[str]
#
# Output
# ------
# pandas.DataFrame
# ==========================================================

from io import StringIO
import pandas as pd


def extract_table_from_soup(
    soup,
    expected_columns
):

    # ---------------------------------------------
    # Find every HTML table
    # ---------------------------------------------

    tables = soup.find_all("table")

    # ---------------------------------------------
    # Search matching table
    # ---------------------------------------------

    for table in tables:

        # Read table with pandas
        try:

            df = pd.read_html(
                StringIO(str(table))
            )[0]

        except Exception:
            continue

        # -----------------------------------------
        # Normalize column names
        # -----------------------------------------

        normalized_columns = []

        for col in df.columns:

            col = str(col)

            # Remove line breaks
            col = col.replace("\n", " ")

            # Collapse multiple spaces
            col = " ".join(col.split())

            normalized_columns.append(col)

        df.columns = normalized_columns

        # -----------------------------------------
        # Partial header matching
        # -----------------------------------------

        selected_columns = {}

        for expected in expected_columns:

            for real in df.columns:

                if expected.lower() in real.lower():

                    selected_columns[expected] = real
                    break

        # -----------------------------------------
        # Validate table
        # -----------------------------------------

        if len(selected_columns) == len(expected_columns):

            df = df[
                list(selected_columns.values())
            ]

            df.columns = expected_columns

            return df

    # ---------------------------------------------
    # No matching table
    # ---------------------------------------------

    raise ValueError(
        "No table matching the expected columns was found."
    )
```


```python
# ==========================================================
# KNOWLEDGE SCRAPER
# ----------------------------------------------------------
# BLOCK 4 - HIERARCHY EXTRACTOR
#
# Purpose:
#     Extract hierarchical HTML structures and convert them
#     into a relational DataFrame.
#
# Responsibilities:
#     - Locate hierarchy root
#     - Detect categories
#     - Extract list items
#     - Build DataFrame
#
'''
download_html()

↓

BeautifulSoup()

↓

Dispatcher

↓

TABLE

↓

extract_table_from_soup()

↓

DataFrame

--------------------

HIERARCHY

↓

extract_hierarchy_from_soup()

↓

DataFrame
'''
# Input
# -----
# soup : BeautifulSoup
#
# root : str
#
# Output
# ------
# pandas.DataFrame
# ==========================================================

import pandas as pd


def extract_hierarchy_from_soup(
    soup,
    root
):

    # ---------------------------------------------
    # Locate hierarchy root
    # ---------------------------------------------

    root_heading = None

    for heading in soup.find_all(["h2", "h3"]):

        title = heading.get_text(" ", strip=True)

        if root.lower() in title.lower():

            root_heading = heading
            break

    if root_heading is None:

        raise ValueError(
            f'Hierarchy root "{root}" not found.'
        )

    # ---------------------------------------------
    # Walk through hierarchy
    # ---------------------------------------------

    records = []

    current_section = root

    current_category = None

    node = root_heading.find_next()

    while node:

        # Stop when next H2 starts
        if node.name == "h2" and node != root_heading:

            break

        # -----------------------------------------
        # New category
        # -----------------------------------------

        if node.name == "h3":

            current_category = node.get_text(
                " ",
                strip=True
            )

        # -----------------------------------------
        # Bullet list
        # -----------------------------------------

        elif node.name == "ul" and current_category:

            for li in node.find_all(
                "li",
                recursive=False
            ):

                text = li.get_text(
                    " ",
                    strip=True
                )

                records.append({

                    "Section": current_section,

                    "Category": current_category,

                    "Item": text,

                    "Description": ""

                })

        node = node.find_next()

    # ---------------------------------------------
    # Convert to DataFrame
    # ---------------------------------------------

    df = pd.DataFrame(records)

    return df
```


```python
# ==========================================================
# KNOWLEDGE SCRAPER
# ----------------------------------------------------------
# BLOCK 5 - SOURCES CONFIGURATION
#
# Purpose:
#     Define every scraping task.
#
# Supported types:
#     - table
#     - hierarchy
# ==========================================================

SOURCES = [

    # ------------------------------------------------------
    # ISO Country Codes
    # ------------------------------------------------------
    {
        "name": "CountryCodes",

        "type": "table",

        "url": "https://es.wikipedia.org/wiki/ISO_3166-1_alfa-2",

        "columns": [

            "Código",
            "Nombre del país",
            "Año",
            "ccTLD",
            "ISO 3166-2",
            "Notas"

        ]
    },

    # ------------------------------------------------------
    # Official Languages
    # ------------------------------------------------------
    {
        "name": "OfficialLanguages",

        "type": "table",

        "url": "https://en.wikipedia.org/wiki/List_of_official_languages_by_country_and_territory",

        "columns": [

            "Country/Region",
            "Official language(s)",
            "National language(s)",
            "Regional language(s)",
            "Minority language(s)",
            "Widely spoken"

        ]
    },

    # ------------------------------------------------------
    # European Regions
    # ------------------------------------------------------
    {
        "name": "EuropeRegions",

        "type": "hierarchy",

        "url": "https://en.wikipedia.org/wiki/Regions_of_Europe",

        "root": "Geographical"

    }


]
```


```python
# ==========================================================
# KNOWLEDGE SCRAPER
# ----------------------------------------------------------
# BLOCK 6 - MAIN PIPELINE
#
# Purpose:
#     Execute every source sequentially.
# ==========================================================

datasets = {}

for source in SOURCES:

    print("=" * 60)
    print(f"Processing: {source['name']}")
    print("=" * 60)

    try:

        df = await scrape_source(source)

        datasets[source["name"]] = df

        print(f"Rows: {len(df)}")
        print(df.head())

    except Exception as e:

        print(f"ERROR -> {e}")

print("\nPipeline completed.")
```

    ============================================================
    Processing: CountryCodes
    ============================================================
    Rows: 249
      Código               Nombre del país   Año ccTLD     ISO 3166-2  \
    0     AD                       Andorra  1974   .ad  ISO 3166-2:AD   
    1     AE  Emiratos Árabes Unidos (los)  1974   .ae  ISO 3166-2:AE   
    2     AF                    Afganistán  1974   .af  ISO 3166-2:AF   
    3     AG             Antigua y Barbuda  1974   .ag  ISO 3166-2:AG   
    4     AI                       Anguila  1985   .ai  ISO 3166-2:AI   
    
                                                   Notas  
    0                                                NaN  
    1                                                NaN  
    2                                                NaN  
    3                                                NaN  
    4  AI antes representaba al Territorio Francés de...  
    ============================================================
    Processing: OfficialLanguages
    ============================================================
    Rows: 208
             Country/Region   Official language(s)   National language(s)  \
    0           Abkhazia[a]         Abkhaz Russian                 Abkhaz   
    1  Afghanistan[1][2][3]  Persian (Dari) Pashto  Persian (Dari) Pashto   
    2            Albania[4]               Albanian                    NaN   
    3            Algeria[5]          Arabic Berber          Arabic Berber   
    4               Andorra             Catalan[6]                    NaN   
    
                                    Regional language(s)  \
    0                                                NaN   
    1  Uzbek[b] Turkmen[b] Pashayi[b] Nuristani[b] Ba...   
    2                                                NaN   
    3                                                NaN   
    4                                                NaN   
    
             Minority language(s)   Widely spoken  
    0                    Georgian             NaN  
    1                         NaN  Persian (Dari)  
    2  Greek Macedonian Aromanian         Italian  
    3                         NaN          French  
    4   Spanish French Portuguese             NaN  
    ============================================================
    Processing: mwAeQ
    ============================================================
    ERROR -> Hierarchy root "Peninsulas" not found.
    ============================================================
    Processing: mwAjU
    ============================================================
    ERROR -> Hierarchy root "Regional" not found.
    
    Pipeline completed.



```python
datasets.keys()
```




    dict_keys(['CountryCodes', 'OfficialLanguages'])




```python
datasets["CountryCodes"].info()
```

    <class 'pandas.DataFrame'>
    RangeIndex: 249 entries, 0 to 248
    Data columns (total 6 columns):
     #   Column           Non-Null Count  Dtype
    ---  ------           --------------  -----
     0   Código           248 non-null    str  
     1   Nombre del país  249 non-null    str  
     2   Año              249 non-null    int64
     3   ccTLD            247 non-null    str  
     4   ISO 3166-2       249 non-null    str  
     5   Notas            82 non-null     str  
    dtypes: int64(1), str(5)
    memory usage: 11.8 KB

