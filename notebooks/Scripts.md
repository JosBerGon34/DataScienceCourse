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
            "Located in the south of Europe...",
            "Comprising the central portion...",
            # ... tantas como necesites o dejes vacío para usar el parser automático
        ]
    }
]


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





# Ejemplo dentro de tu bucle de procesamiento de sources:
for source in SOURCES:
    if source["type"] == "hierarchy":
        html = fetch_page_html(source["url"])
        soup = BeautifulSoup(html, "html.parser")
        
        # Extraemos pasándole la lista manual si está configurada en el source
        manual_desc = source.get("manual_descriptions", None)
        dfRegions = extract_hierarchy_from_soup(soup, root=source["root"], manual_descriptions=manual_desc)