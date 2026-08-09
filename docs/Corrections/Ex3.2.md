3. Applied Data Science Level (Country Metadata Extraction)
Extract demographic/cultural metadata for European countries to enrich our core project pipeline:

Target Data Source:

Scrape tabular data from an open web source containing European nation details (e.g., Wikipedia/EU portal tables).

Extract at least 3 structural variables per country:

Country Name / ISO Code (e.g., ES, DE, FR).

Primary Official Language or Capital City.

Geographic / Cultural Region (e.g., Western Europe, Southern Europe, Nordic).

Data Cleaning & Export:

Strip reference markers (e.g., [1], [note A]) using regular expressions (re.sub(r'\[.*?\]', '', text)).

Align country names or codes to match the standard geo / CNTRY keys used in Eurostat and ESS microdata.

Export the cleaned DataFrame to data/processed/scraped_country_metadata.csv.

3.1 Target Data Source:
Extract at least 3 structural variables per country:

Country Name / ISO Code (e.g., ES, DE, FR).

Primary Official Language or Capital City.

Geographic / Cultural Region (e.g., Western Europe, Southern Europe, Nordic).

we will use a pipeline for extract lists and tables from webs using , playwright for download html, beautifulsoup and pandas to search the bodies from html we want to format in dataframes mostly.


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


```python
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
    executable_path= None,
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
#     optional manual description injections for hierarchies,
#     plus optional root_id / category_ids XPath-style anchors.
# ==========================================================



from bs4 import BeautifulSoup
import gc


async def scrape_source(
    source,
    manual_descriptions=None,
    root_id=None,
    category_ids=None
):

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
        root_id_val = root_id or source.get("root_id", None)
        category_ids_val = category_ids or source.get("category_ids", None)

        df = extract_hierarchy_from_soup(
            soup=soup,
            root=source["root"],
            manual_descriptions=manual_desc,
            root_id=root_id_val,
            category_ids=category_ids_val
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
import re
import pandas as pd


HEADING_TAGS = ["h2", "h3", "h4", "h5", "h6"]


def _heading_text_in_node(node):
    """Returns the heading text of a node if it IS a heading, or wraps
    a heading (MediaWiki's <div class="mw-heading..."> wrapper)."""
    if node.name in HEADING_TAGS:
        return node.get_text(" ", strip=True)

    if node.name == "div":
        classes = node.get("class") or []
        if any(c.startswith("mw-heading") for c in classes):
            inner = node.find(HEADING_TAGS)
            if inner:
                return inner.get_text(" ", strip=True)

    return None


def _extract_items_from_ul(ul):
    """Extracts (item_title, inline_description, parent_item) for every
    top-level <li> in `ul`, recursing into nested <ul> sub-items (which
    are tagged with Parent_item, since they typically don't get their
    own paired <dl>)."""
    results = []

    for li in ul.find_all("li", recursive=False):

        nested_uls = li.find_all("ul", recursive=False)

        bold_tag = li.find(["b", "strong"])

        if bold_tag:
            item_title = bold_tag.get_text(" ", strip=True)
            # text of the <li> AFTER removing the bold tag's own text,
            # so we can recover an inline description if present
            # (used mainly for nested sub-items without their own <dl>)
            li_text_after_bold = li.get_text(" ", strip=True)
            if li_text_after_bold.startswith(item_title):
                inline_description = li_text_after_bold[len(item_title):].strip(" :.-")
            else:
                inline_description = ""
        else:
            full_text = li.get_text(" ", strip=True)
            for nested in nested_uls:
                nested_text = nested.get_text(" ", strip=True)
                if nested_text:
                    full_text = full_text.replace(nested_text, "")
            parts = re.split(r"[:—–-]", full_text, maxsplit=1)
            if len(parts) > 1:
                item_title = parts[0].strip()
                inline_description = parts[1].strip()
            else:
                item_title = full_text
                inline_description = ""

        # strip nested-ul text out of the inline description so a child
        # sub-item's text isn't duplicated into the parent's description
        for nested in nested_uls:
            nested_text = nested.get_text(" ", strip=True)
            if nested_text and nested_text in inline_description:
                inline_description = inline_description.replace(nested_text, "").strip()

        results.append((item_title, inline_description, None))

        for nested in nested_uls:
            for (sub_title, sub_desc, _) in _extract_items_from_ul(nested):
                results.append((sub_title, sub_desc, item_title))

    return results


def extract_hierarchy_from_soup(
    soup,
    root,
    manual_descriptions=None,
    root_id=None,
    category_ids=None
):
    """
    Extracts hierarchical lists with fallback support for manual description
    injection ordered by appearance. Same signature/behavior contract as
    before, PLUS two new optional parameters:

        root_id       : str or None
            If given, looks up the root container directly by HTML id
            (soup.find(id=root_id)) instead of searching heading text.

        category_ids  : dict[str, str] or None
            Maps a category label (as it should appear in the "Category"
            column) to the HTML id of its container, e.g.
            {"Peninsulas": "mwAeQ", "Regional": "mwAjU"}. When the walker
            reaches a heading whose text matches one of these labels, it
            jumps directly to that id's element instead of relying on
            the automatic heading-text detection — useful when heading
            text is ambiguous or repeated on the page.
    """

    # ---------------------------------------------
    # 1. Locate the hierarchy root heading (unchanged)
    # ---------------------------------------------
    root_section = None

    if root_id:
        root_section = soup.find(id=root_id)

    if root_section is None:
        root_heading = None

        for heading in soup.find_all(HEADING_TAGS):
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

    # Global counter to track sequential appearance for manual injection
    global_item_index = 0

    def walk(container, current_category):
        nonlocal global_item_index

        # Direct-children traversal only: this is what prevents nested
        # <ul> (sub-groupings) from leaking into the outer loop.
        children = [c for c in container.children if getattr(c, "name", None)]

        i = 0
        while i < len(children):
            node = children[i]

            # -----------------------------------------
            # Nested <section> (MediaWiki wraps every
            # sub-heading's content in its own <section>)
            # -----------------------------------------
            if node.name == "section":
                nested_heading_text = None
                nested_heading = node.find(HEADING_TAGS)
                if nested_heading:
                    nested_heading_text = nested_heading.get_text(" ", strip=True)

                target_category = nested_heading_text if nested_heading_text else current_category

                # If this category has a known id, jump straight to it
                # instead of trusting the nested <section> we happened
                # to land on while walking — more robust when the DOM
                # nesting doesn't match expectations.
                if category_ids and target_category in category_ids:
                    forced = soup.find(id=category_ids[target_category])
                    if forced is not None:
                        node = forced

                walk(node, target_category)

            # -----------------------------------------
            # Heading (bare, or wrapped in div.mw-heading)
            # -----------------------------------------
            else:
                heading_text = _heading_text_in_node(node)

                if heading_text is not None:
                    if root.lower() not in heading_text.lower():
                        current_category = heading_text

                # -----------------------------------------
                # List of items
                # -----------------------------------------
                elif node.name in ("ul", "ol") and current_category:

                    items = _extract_items_from_ul(node)

                    # Look ahead: is the very next sibling a <dl> with
                    # the description(s) for the item(s) just parsed?
                    next_el = children[i + 1] if i + 1 < len(children) else None
                    dd_texts = []
                    consumed_dl = False

                    if next_el is not None and next_el.name == "dl":
                        dd_tags = next_el.find_all("dd", recursive=False)
                        if not dd_tags:
                            dd_tags = next_el.find_all("dd")
                        dd_texts = [dd.get_text(" ", strip=True) for dd in dd_tags]
                        consumed_dl = True

                    dd_cursor = 0

                    for item_title, inline_description, parent_item in items:

                        if manual_descriptions and global_item_index < len(manual_descriptions):
                            description = manual_descriptions[global_item_index]

                        elif parent_item is None and dd_cursor < len(dd_texts):
                            # only top-level items (parent_item is None)
                            # consume the paired <dl>; nested sub-items
                            # fall back to their own inline text
                            description = dd_texts[dd_cursor]
                            dd_cursor += 1

                        else:
                            description = inline_description

                        records.append({
                            "Section": current_section,
                            "Category": current_category,
                            "Item": item_title,
                            "Description": description,
                            "Parent_item": parent_item,
                        })

                        global_item_index += 1

                    if consumed_dl:
                        i += 1  # skip the <dl> we already consumed

            i += 1

    walk(root_section, None)

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

        # NUEVO, opcional — Nodo 0 de tu esquema (id real del <section> o heading)
        "root_id": "mwAeM",

        # NUEVO, opcional — Nodo 1A / 1X: id de cada categoría conocida.
        # Solo hace falta el ID del nodo de categoría, no de cada ítem —
        # el resto de la jerarquía (Nodo 2AY, Nodo 3A) se recorre solo.
        "category_ids": {
            "Peninsulas": "mwAeQ",
            "Regional": "mwAjU",
            "Other groupings": "mwA2o",
        },

        "manual_descriptions": [
            # ... igual que ya lo tenías, se sigue usando como override
            # de máxima prioridad si lo rellenas
        ]
    }
]
```


```python
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
        if source.get("type") == "hierarchy":
            manual_desc = source.get("manual_descriptions", None)

            # NUEVO: se pasan si existen, si no, quedan en None y el
            # comportamiento es idéntico al actual
            root_id = source.get("root_id", None)
            category_ids = source.get("category_ids", None)

            df = await scrape_source(
                source,
                manual_descriptions=manual_desc,
                root_id=root_id,
                category_ids=category_ids,
            )
        else:
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
    Processing: EuropeRegions
    ============================================================
    Rows: 23
            Section    Category                                    Item  \
    0  Geographical  Peninsulas  Apennine Peninsula (Italian Peninsula)   
    1  Geographical  Peninsulas                        Balkan Peninsula   
    2  Geographical  Peninsulas                 Fennoscandian Peninsula   
    3  Geographical  Peninsulas                       Iberian Peninsula   
    4  Geographical  Peninsulas                       Jutland Peninsula   
    
                                             Description Parent_item  
    0  Located in the south of Europe, the Apennine P...         NaN  
    1  The Balkan Peninsula is located in Southeaster...         NaN  
    2  Located in the north of Europe, including Finl...         NaN  
    3  Located in Southwestern Europe, this peninsula...         NaN  
    4  Jutland of Denmark (main part of the country e...         NaN  
    
    Pipeline completed.



```python
pd.DataFrame(datasets['EuropeRegions']).to_csv(DATA_TABLES / "EuRegions.csv")

```


```python
dfEUCodes = pd.DataFrame(datasets['CountryCodes'])
```


```python
dfEUCodes.info()
print(f"\n {dfEUCodes}")
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
    
         Código               Nombre del país   Año ccTLD     ISO 3166-2  \
    0       AD                       Andorra  1974   .ad  ISO 3166-2:AD   
    1       AE  Emiratos Árabes Unidos (los)  1974   .ae  ISO 3166-2:AE   
    2       AF                    Afganistán  1974   .af  ISO 3166-2:AF   
    3       AG             Antigua y Barbuda  1974   .ag  ISO 3166-2:AG   
    4       AI                       Anguila  1985   .ai  ISO 3166-2:AI   
    ..     ...                           ...   ...   ...            ...   
    244     YE                         Yemen  1974   .ye  ISO 3166-2:YE   
    245     YT                       Mayotte  1993   .yt  ISO 3166-2:YT   
    246     ZA                     Sudáfrica  1974   .za  ISO 3166-2:ZA   
    247     ZM                        Zambia  1974   .zm  ISO 3166-2:ZM   
    248     ZW                      Zimbabue  1980   .zw  ISO 3166-2:ZW   
    
                                                     Notas  
    0                                                  NaN  
    1                                                  NaN  
    2                                                  NaN  
    3                                                  NaN  
    4    AI antes representaba al Territorio Francés de...  
    ..                                                 ...  
    244  Anterior nombre ISO del país: Yemen, República...  
    245                                                NaN  
    246  Código obtenido del nombre en neerlandés: Zuid...  
    247                                                NaN  
    248               Antes llamado Rhodesia del Sur (RH).  
    
    [249 rows x 6 columns]



```python
#We only need few of those columms also the index could be our factorized ID for the countries we will use.
from dataclasses import replace


dfEUCodes.drop(columns=['Año', 'ccTLD', 'ISO 3166-2', 'Notas'], inplace=True)   

```


```python
dfLangsCntry = pd.DataFrame(datasets['OfficialLanguages'])
```


```python
# Lets merge the dataframes to unify the languages spoken and ISO 3166-2 country codes, but we will need to
# translate the country column to english in order to use it for group the values.
# Lets use googletranslator from deep_translator library to translate country column from dfEUCodes.
from deep_translator import GoogleTranslator
import pandas as pd

traductor = GoogleTranslator(source='es', target='en')

def traducir_seguro(texto):
    if pd.isna(texto): return texto
    try:
        return traductor.translate(texto)
    except:
        return texto

dfEUCodes['Countries'] = dfEUCodes['Nombre del país'].apply(traducir_seguro)   
```


```python
#Lets filter dfLangsCntry Country/Region columms. Deleting all the indicators of quanity languages spoken.
#So we get the first string before the sign is shown in the index value from that columm.
dfLangsCntry['Countries'] = dfLangsCntry['Country/Region'].str.split('[').str[0]
```


```python
#Now we delete the old columm
dfLangsCntry.drop(columns=['Country/Region'], inplace=True)   
```


```python
#Now we merge both dataframes using dfEuCodes['Countries'] and dfLangsCntry['Countries'] values as a nexus.
dfEu = pd.merge(
    dfEUCodes,
    dfLangsCntry,
    on="Countries",
    how="inner"
)
dfEu.head()
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
      <th>Código</th>
      <th>Nombre del país</th>
      <th>Countries</th>
      <th>Official language(s)</th>
      <th>National language(s)</th>
      <th>Regional language(s)</th>
      <th>Minority language(s)</th>
      <th>Widely spoken</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AD</td>
      <td>Andorra</td>
      <td>Andorra</td>
      <td>Catalan[6]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Spanish French Portuguese</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AE</td>
      <td>Emiratos Árabes Unidos (los)</td>
      <td>United Arab Emirates</td>
      <td>Arabic</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>English</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AF</td>
      <td>Afganistán</td>
      <td>Afghanistan</td>
      <td>Persian (Dari) Pashto</td>
      <td>Persian (Dari) Pashto</td>
      <td>Uzbek[b] Turkmen[b] Pashayi[b] Nuristani[b] Ba...</td>
      <td>NaN</td>
      <td>Persian (Dari)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AG</td>
      <td>Antigua y Barbuda</td>
      <td>Antigua and Barbuda</td>
      <td>(English has de facto status) Spanish</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Antiguan and Barbudan Creole</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AL</td>
      <td>Albania</td>
      <td>Albania</td>
      <td>Albanian</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Greek Macedonian Aromanian</td>
      <td>Italian</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Lets clean the cache
del df, dfEUCodes, dfLangsCntry
gc.collect()
```




    1280




```python
#Lets save this valuable dataframe as 'GlobalCountriesLang.csv'
dfEu.to_csv(DATA_TABLES / "GlobalCountriesLang.csv")
pd.DataFrame(datasets['EuropeRegions']).to_csv(DATA_TABLES / "EuRegions.csv")
```

In this document we achieved to make a logic pipeline for data extraction from websites:
Using Playwright as HTML downloader, Beautiful soup to identify wich htmls blocks we need to parse
then we used pandas as our main translator between html syntax and python equivalence. Asking only for
text headers we can observe in non development html view.
# WE achieved the first part of the exercise, data scrapping and data storagement as CSV.
# The next part of the exercise(Ex3.2part2.ipynb) will be data cleaning and preparation of different data blocks.
