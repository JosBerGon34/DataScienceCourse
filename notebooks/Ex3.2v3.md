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
# BLOCK 2 - SCRAPER DISPATCHER (UPDATED SIGNATURE)
#
# Purpose:
#     Control the complete scraping workflow, supporting 
#     optional manual description injections for hierarchies.
# ==========================================================

from bs4 import BeautifulSoup
import gc


async def scrape_source(source, manual_descriptions=None):

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

        # Fallback to function argument or fallback to source dictionary key
        manual_desc = manual_descriptions or source.get("manual_descriptions", None)

        df = extract_hierarchy_from_soup(
            soup=soup,
            root=source["root"],
            manual_descriptions=manual_desc
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
# BLOCK 4 - HYBRID HIERARCHY EXTRACTOR (MANUAL & AUTO)
# ==========================================================

import re
import pandas as pd


def extract_hierarchy_from_soup(
    soup,
    root,
    manual_descriptions=None
):
    """
    Extracts hierarchical lists with fallback support for manual description injection 
    ordered by appearance.
    """

    # ---------------------------------------------
    # 1. Locate the hierarchy root heading
    # ---------------------------------------------
    root_heading = None

    for heading in soup.find_all(["h2", "h3", "h4", "h5", "h6"]):
        title = heading.get_text(" ", strip=True)
        if root.lower() in title.lower():
            root_heading = heading
            break

    if root_heading is None:
        raise ValueError(f'Hierarchy root "{root}" not found.')

    root_section = root_heading.find_parent("section")
    if not root_section:
        root_section = root_heading.parent

    # ---------------------------------------------
    # 2. Walk through hierarchy and map descriptions
    # ---------------------------------------------
    records = []
    current_section = root
    current_category = None

    search_scope = root_section if root_section else root_heading
    nodes = search_scope.find_all(["h3", "h4", "h5", "ul", "ol"])

    # Global counter to track sequential appearance for manual injection
    global_item_index = 0

    for node in nodes:
        text_val = node.get_text(" ", strip=True)

        if node.name in ["h3", "h4", "h5"]:
            if root.lower() not in text_val.lower():
                current_category = text_val

        elif node.name in ["ul", "ol"] and current_category:
            list_items = node.find_all("li", recursive=False)

            for li in list_items:
                full_text = li.get_text(" ", strip=True)
                
                # Extract item title via bold tags first
                bold_tag = li.find(["b", "strong"])
                if bold_tag:
                    item_title = bold_tag.get_text(" ", strip=True)
                    bold_tag.decompose()
                    auto_description = li.get_text(" ", strip=True).lstrip("—-: ").strip()
                else:
                    parts = re.split(r'[:—–-]', full_text, maxsplit=1)
                    if len(parts) > 1:
                        item_title = parts[0].strip()
                        auto_description = parts[1].strip()
                    else:
                        item_title = full_text
                        auto_description = ""

                # Hybrid logic: If manual descriptions are provided and within bounds, use them!
                if manual_descriptions and global_item_index < len(manual_descriptions):
                    description = manual_descriptions[global_item_index]
                else:
                    description = auto_description

                records.append({
                    "Section": current_section,
                    "Category": current_category,
                    "Item": item_title,
                    "Description": description
                })

                global_item_index += 1

    # ---------------------------------------------
    # 3. Convert to DataFrame and Validate
    # ---------------------------------------------
    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError(f"No hierarchical items parsed under root '{root}'.")

    return df
```


```python
# ==========================================================
# KNOWLEDGE SCRAPER
# ----------------------------------------------------------
# BLOCK 5 - SOURCES CONFIGURATION (WITH HYBRID FALLBACK)
# ==========================================================

SOURCES = [
    {
        "name": "CountryCodes",
        "type": "table",
        "url": "https://es.wikipedia.org/wiki/ISO_3166-1_alfa-2",
        "columns": ["Código", "Nombre del país", "Año", "ccTLD", "ISO 3166-2", "Notas"]
    },
    {
        "name": "OfficialLanguages",
        "type": "table",
        "url": "https://en.wikipedia.org/wiki/List_of_official_languages_by_country_and_territory",
        "columns": ["Country/Region", "Official language(s)", "National language(s)", "Regional language(s)", "Minority language(s)", "Widely spoken"]
    },
    {
        "name": "EuropeRegions",
        "type": "hierarchy",
        "url": "https://en.wikipedia.org/wiki/Regions_of_Europe",
        "root": "Geographical",
        
        # Opcional: Lista manual de descripciones en orden exacto de aparición por si el HTML se bugea
        
            "manual_descriptions": [
            "Located in the south of Europe, the Apennine Peninsula contains the states of Italy, San Marino, and Vatican City",
            "The Balkan Peninsula is located in Southeastern Europe and the following countries and territories occupy land on the peninsula either exclusively or partially: Albania, Bosnia and Herzegovina, Bulgaria, Croatia (approximately the southern half), Greece, Kosovo, Montenegro, North Macedonia, Romania (the Dobrudja region), Serbia, Slovenia (the coastal section), and Turkey (East Thrace)",
            "Located in the north of Europe, including Finland, Norway, Sweden, and part of Russia",
            "Located in Southwestern Europe, this peninsula contains Andorra, Gibraltar, Portugal, Spain, and a small part of France",
            "Jutland of Denmark (main part of the country excluding its islands) and the Schleswig-Holstein region of Germany",
            "Located in the north of Europe, including Norway, Sweden, and part of Finland",
            "United Kingdom, Ireland, Iceland, Belgium, the Netherlands, Portugal, Spain, France, western Scandinavia and Germany.",
            "States that occupy the Alps: Austria, Switzerland, Liechtenstein, Slovenia, Germany, France, and Italy",
            "In its broadest sense, encompasses Albania, Bosnia and Hercegovina, Bulgaria, Croatia, Greece, Hungary, Kosovo, Moldova, Montenegro, North Macedonia, Romania, Serbia, Slovenia and European Turkey",
            "The term Baltic states emerged after World War I referring to the new sovereign states that emerged on the east coast of the Baltic Sea: Finland, Estonia, Latvia, and Lithuania. Since World War II, the term has been used for just Estonia, Latvia, and Lithuania.[7]",
            "Guernsey, The Isle of Man, the Republic of Ireland, Jersey and the United Kingdom",
            "Czech Republic, Hungary, Poland, Romania, Serbia, Slovakia, and Ukraine",
            "Armenia, Azerbaijan, Georgia, and Russia; also the disputed territories of Abkhazia, and South Ossetia",
            "Guernsey and Jersey",
            "Belgium, Luxembourg, the Netherlands, parts of France, and parts of Germany. Benelux: Belgium, the Netherlands, and Luxembourg",
            "Sweden, Norway, Finland, Denmark, Greenland, and Iceland. Scandinavia: Sweden, Norway, Denmark, Fennoscandia: Finland, Sweden, Norway and Karelia; a geological region defined by the Fennoscandian",
            "States that lie along the River Danube: Austria, Bulgaria, Croatia, Germany, Hungary, Moldova, Romania, Serbia, Slovakia, and Ukraine",
            "Slovenia, Croatia, Bosnia and Herzegovina, Montenegro, Albania, Serbia, Kosovo and Italy occupy a small portion of the Dinaric Alps.[citation needed]",
            "Chain of Islands in the North Atlantic: Azores, Canary Islands, Madeira; also including Cape Verde, an independent African nation",
            "Mediterranean nations are European countries on the Mediterranean Basin: Portugal, Spain, France, Monaco, Italy, Slovenia, San Marino, Croatia, Bosnia and Herzegovina, Montenegro, Albania, Greece, Turkey, Cyprus, Malta, and the British territory of Gibraltar. Adriatic region: Italy, Slovenia, Croatia, Bosnia and Herzegovina, Montenegro, Albania",
            "The Black Sea nations (although some sections lie within Asia) are: Abkhazia (de facto state), Bulgaria, Georgia, Romania, Russia, Turkey, and Ukraine",
            "The world's largest lake which forms a section of the Asian-European border has five countries occupying its shore. Iran and Turkmenistan lie entirely within Asia while the following countries are transcontinental and have sovereignty over the Caspian Sea's European sector: Azerbaijan, Kazakhstan, and Russia",
            "Blue Banana: describing the concentration of the wealth/economic productivity of Europe in a banana-shaped band running from north west England, London, through Benelux, eastern France, western Germany to northern Italy."
            # ... tantas como necesites o dejes vacío para usar el parser automático
        ]
    }
]
```


```python
# ==========================================================
# KNOWLEDGE SCRAPER
# ----------------------------------------------------------
# BLOCK 6 - MAIN PIPELINE (HYBRID RESILIENT EXECUTION)
#
# Purpose:
#     Execute every source sequentially, passing optional 
#     manual descriptions or parameters to handle complex 
#     hierarchical structures and tables robustly.
# ==========================================================

datasets = {}

for source in SOURCES:

    print("=" * 60)
    print(f"Processing: {source['name']}")
    print("=" * 60)

    try:
        # Check if the source defines a hierarchy type with manual fallback descriptions
        if source.get("type") == "hierarchy":
            # Pass manual descriptions if configured in the source dictionary
            manual_desc = source.get("manual_descriptions", None)
            
            # Execute scraping task with hybrid parameters
            df = await scrape_source(source, manual_descriptions=manual_desc)
        else:
            # Standard execution for tables or other types
            df = await scrape_source(source)

        # Store resulting DataFrame in the datasets dictionary
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
    Processing: EuropeRegions
    ============================================================
    Rows: 28
            Section    Category                                    Item  \
    0  Geographical  Peninsulas  Apennine Peninsula (Italian Peninsula)   
    1  Geographical  Peninsulas                        Balkan Peninsula   
    2  Geographical  Peninsulas                 Fennoscandian Peninsula   
    3  Geographical  Peninsulas                       Iberian Peninsula   
    4  Geographical  Peninsulas                       Jutland Peninsula   
    
                                             Description  
    0  Located in the south of Europe, the Apennine P...  
    1  The Balkan Peninsula is located in Southeaster...  
    2  Located in the north of Europe, including Finl...  
    3  Located in Southwestern Europe, this peninsula...  
    4  Jutland of Denmark (main part of the country e...  
    
    Pipeline completed.



```python
datasets['EuropeRegions'].head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Section</th>
      <th>Category</th>
      <th>Item</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Apennine Peninsula (Italian Peninsula)</td>
      <td>Located in the south of Europe, the Apennine P...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Balkan Peninsula</td>
      <td>The Balkan Peninsula is located in Southeaster...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Fennoscandian Peninsula</td>
      <td>Located in the north of Europe, including Finl...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Iberian Peninsula</td>
      <td>Located in Southwestern Europe, this peninsula...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Jutland Peninsula</td>
      <td>Jutland of Denmark (main part of the country e...</td>
    </tr>
  </tbody>
</table>
</div>




```python
datasets['CountryCodes'].to_csv(DATA_TABLES / "EUcodecountries.csv", index=False, encoding="utf-8")
datasets['OfficialLanguages'].to_csv(DATA_TABLES / "EUlanguages.csv", index=False, encoding="utf-8")
datasets['EuropeRegions'].to_csv(DATA_TABLES / "EURegions.csv", index=False, encoding="utf-8")

```


```python
dfregions = pd.DataFrame(datasets['EuropeRegions'])
```


```python
dfregions.head(27)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Section</th>
      <th>Category</th>
      <th>Item</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Apennine Peninsula (Italian Peninsula)</td>
      <td>Located in the south of Europe, the Apennine P...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Balkan Peninsula</td>
      <td>The Balkan Peninsula is located in Southeaster...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Fennoscandian Peninsula</td>
      <td>Located in the north of Europe, including Finl...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Iberian Peninsula</td>
      <td>Located in Southwestern Europe, this peninsula...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Jutland Peninsula</td>
      <td>Jutland of Denmark (main part of the country e...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Scandinavian Peninsula</td>
      <td>Located in the north of Europe, including Norw...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Atlantic Europe</td>
      <td>United Kingdom, Ireland, Iceland, Belgium, the...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Alpine countries</td>
      <td>States that occupy the Alps: Austria, Switzerl...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>United Kingdom , Ireland , Iceland , Belgium ,...</td>
      <td>In its broadest sense, encompasses Albania, Bo...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Balkans region</td>
      <td>The term Baltic states emerged after World War...</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Baltic Rim region</td>
      <td>Guernsey, The Isle of Man, the Republic of Ire...</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Baltic states</td>
      <td>Czech Republic, Hungary, Poland, Romania, Serb...</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>British Isles</td>
      <td>Armenia, Azerbaijan, Georgia, and Russia; also...</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Carpathian states</td>
      <td>Guernsey and Jersey</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Caucasus</td>
      <td>Belgium, Luxembourg, the Netherlands, parts of...</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Channel Islands</td>
      <td>Sweden, Norway, Finland, Denmark, Greenland, a...</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Low Countries</td>
      <td>States that lie along the River Danube: Austri...</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Benelux</td>
      <td>Slovenia, Croatia, Bosnia and Herzegovina, Mon...</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Nordic countries</td>
      <td>Chain of Islands in the North Atlantic: Azores...</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Scandinavia</td>
      <td>Mediterranean nations are European countries o...</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Fennoscandia</td>
      <td>The Black Sea nations (although some sections ...</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Danubian countries</td>
      <td>The world's largest lake which forms a section...</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Dinaric Alps</td>
      <td>Blue Banana: describing the concentration of t...</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Macaronesia</td>
      <td></td>
    </tr>
    <tr>
      <th>24</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Mediterranean countries</td>
      <td></td>
    </tr>
    <tr>
      <th>25</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Adriatic region</td>
      <td>Italy , Slovenia , Croatia , Bosnia and Herzeg...</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Black Sea region</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>


