
## 1. Introduction to APIs & Data Extraction

An **API** (Application Programming Interface) is a structured interface that allows two software systems to communicate over the web. In modern data workflows, REST (Representational State Transfer) APIs serve as the standard mechanism for fetching live data, interacting with remote databases, and integrating external microservices.

### Key Protocols & Data Formats

* **HTTP/HTTPS Protocols**:
  * `GET`: Retrieves data from a server without modifying state.
  * `POST`: Sends new data payload to a server.
  * `PUT` / `PATCH`: Updates existing resources on the server.
  * `DELETE`: Removes a resource from the server.

* **Data Exchange Formats**:
  * **JSON** (*JavaScript Object Notation*): The standard lightweight format for web APIs. Highly native to Python (`dict`/`list`).
  * **XML** (*Extensible Markup Language*): Verbose, tree-structured format. Common in legacy systems and official statistical portals (e.g., World Bank default). Requires parsing via `xml.etree.ElementTree` or `BeautifulSoup`.
  * **Plain Text / Markdown / CSV**: Direct raw file responses often used for quick ingestion or LLM context streaming.

---

## 2. Role in Data Science & AI Agent Workflows

### Data Science & Analytics
* **Panel Data Construction**: Automated gathering of longitudinal macro-economic indicators (e.g., Eurostat, World Bank) and social survey microdata.
* **Pipeline Automation**: ETL/ELT pipelines fetch remote dynamic endpoints instead of static manual file downloads.
* **Feature Engineering**: Real-time enrichment of local datasets with third-party geospatial, financial, or demographic attributes.

### AI Agents & Function Calling
* **Tool Augmentation**: AI agents execute programmatic API calls to ground output in deterministic real-time data.
* **ReAct Loops**: Agent reasoning steps invoke Python scripts using `requests` to fetch dynamic web contexts, parse JSON/XML responses, and feed the truncated payload back into the context window.
* **Structured State**: Agents interact with REST endpoints using strict JSON schemas to trigger external workflows or update database states.

---

## 3. Structural Design of a Production-Ready Script

To ensure stability against network timeouts, throttling, rate limits (HTTP 429), and gateway errors (HTTP 502/504), an extraction script must implement the following architectural patterns:

1. **Persistent Connections (`requests.Session`)**: Reuses underlying TCP sockets to reduce latency and handshake overhead.
2. **Custom HTTP Headers**: Emulates standard browser requests (`User-Agent`) and explicitly sets accepted content types.
3. **Throttling (`time.sleep`)**: Introduces rate-limiting delays between iterations to avoid IP bans or rate limits.
4. **Resilience & Retries**: Implements exponential backoff or retry logic for intermittent network drops.
5. **Decoupled Local Storage**: Saves raw file payloads directly to disk prior to memory parsing.

---

## 4. Production Script Architecture (Python Example)

The following production template downloads data safely, handles exceptions gracefully, and builds a clean `pandas` Panel DataFrame.

```python
import os
import time
import requests
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET

# ---------------------------------------------------------
# 1. PARAMETERIZATION & CONFIGURATION
# ---------------------------------------------------------
COUNTRIES = ['AT', 'BE', 'DE', 'EE', 'ES', 'FI', 'FR', 'GB', 'HU', 'IE', 'NL', 'NO', 'PL', 'PT', 'SE']
YEARS = [2004, 2014, 2024]
RAW_DATA_DIR = "data/raw_xml"

INDICATORS = {
    'NY.GDP.PCAP.CD': 'gdpcapita',
    'SL.UEM.TOTL.ZS': 'unemployment',
    'FP.CPI.TOTL.ZG': 'inflation',
    'SP.POP.TOTL': 'population',
    'SI.POV.GINI': 'gini'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': 'application/xml,application/json',
    'Connection': 'close'
}

# Ensure destination directory exists
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# ---------------------------------------------------------
# 2. EXTRACTION PHASE (Network I/O with Throttling)
# ---------------------------------------------------------
def download_api_payloads(countries, indicators, delay=2.0, max_retries=3):
    """
    Downloads XML payloads from World Bank API with session handling,
    exponential retries, and explicit disk saving.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    
    total_calls = len(countries) * len(indicators)
    counter = 0

    print("=== PHASE 1: STARTING DOWNLOAD LOOP ===")
    
    for country in countries:
        for code, var_name in indicators.items():
            counter += 1
            file_path = os.path.join(RAW_DATA_DIR, f"{country}_{var_name}.xml")
            
            # Idempotent execution: Skip existing files
            if os.path.exists(file_path):
                print(f"[{counter}/{total_calls}] Exists locally: {country}_{var_name}.xml")
                continue

            url = f"[https://api.worldbank.org/v2/country/](https://api.worldbank.org/v2/country/){country}/indicator/{code}?date=2004:2024&per_page=1000"
            
            for attempt in range(1, max_retries + 1):
                try:
                    response = session.get(url, timeout=15)
                    
                    if response.status_code == 200:
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                            f.flush()
                        print(f"[{counter}/{total_calls}] Downloaded: {country}_{var_name}.xml")
                        break
                    else:
                        print(f"[{counter}/{total_calls}] HTTP {response.status_code} for {country}-{var_name}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"Attempt {attempt} failed for {country}-{var_name}: {e}")
                    if attempt < max_retries:
                        time.sleep(delay * attempt)  # Exponential backoff
                    else:
                        print(f"Failed to fetch {country}-{var_name} after {max_retries} attempts.")

            # Throttling delay between API calls
            time.sleep(delay)

# ---------------------------------------------------------
# 3. PARSING PHASE (Offline Processing)
# ---------------------------------------------------------
def parse_local_xml_files(countries, indicators, target_years):
    """
    Parses locally saved XML files into a structured list of dictionaries.
    """
    parsed_records = []

    print("\n=== PHASE 2: PARSING LOCALPAYLOADS ===")
    
    for country in countries:
        for code, var_name in indicators.items():
            file_path = os.path.join(RAW_DATA_DIR, f"{country}_{var_name}.xml")
            
            if not os.path.exists(file_path):
                continue
                
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                
                # Iterate over data nodes ignoring XML namespace prefix
                for elem in root.iter():
                    if elem.tag.endswith('data'):
                        date_val = None
                        num_val = None
                        
                        for child in elem:
                            if child.tag.endswith('date'):
                                date_val = child.text
                            elif child.tag.endswith('value'):
                                num_val = child.text
                        
                        if date_val and num_val is not None and num_val.strip() != "":
                            year = int(date_val)
                            if year in target_years:
                                parsed_records.append({
                                    'geo': country,
                                    'year': year,
                                    'variable': var_name,
                                    'value': float(num_val)
                                })
            except Exception as e:
                print(f"Error parsing file {file_path}: {e}")

    return pd.DataFrame(parsed_records)

# ---------------------------------------------------------
# 4. MAIN EXECUTION & DATAFRAME COOKING
# ---------------------------------------------------------
if __name__ == "__main__":
    # Step 1: Download raw data safely
    download_api_payloads(COUNTRIES, INDICATORS, delay=1.5)
    
    # Step 2: Parse downloaded raw files
    df_raw = parse_local_xml_files(COUNTRIES, INDICATORS, YEARS)
    
    # Step 3: Build base panel skeleton (45 rows: 15 countries x 3 years)
    panel_index = pd.MultiIndex.from_product([COUNTRIES, YEARS], names=['geo', 'year'])
    df_panel = pd.DataFrame(index=panel_index).reset_index()
    
    # Step 4: Pivot and update panel in memory
    if not df_raw.empty:
        df_pivoted = df_raw.pivot_table(
            index=['geo', 'year'], 
            columns='variable', 
            values='value'
        ).reset_index()
        
        df_panel = df_panel.set_index(['geo', 'year'])
        df_pivoted = df_pivoted.set_index(['geo', 'year'])
        
        df_panel.update(df_pivoted)
        df_panel = df_panel.reset_index()

    print("\n=== COOKED IN-MEMORY PANEL DATAFRAME ===")
    print(df_panel.head(10))