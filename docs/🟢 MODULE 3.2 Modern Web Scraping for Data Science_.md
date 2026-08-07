### 🎯 Context & Objectives
  
Traditional HTTP clients (like `requests`) often fail on modern web portals due to dynamic JavaScript rendering, client-side hydration, or basic bot detection mechanisms.
  
In this exercise, you will build a modern, robust web scraping pipeline using **Playwright** (Python API) combined with **Parsel** or **pandas** for structural parsing. You will also set up an isolated virtual environment using **`uv`**, perfectly tailored for your CachyOS Linux system.
  
```
uv add playwright parsel pandas
uv run playwright install chromium
```
1. **Execution Context**:
  
    - Ensure your VS Code / VSCodium workspace selects the Python interpreter created within `.venv` by `uv`.
  
  
#### 2. Syntactic / Algorithmic Level (Async Playwright & Dynamic Scraping)
  
In your local script or notebook (`notebooks/03_2_web_scraping.ipynb`), implement the following technical architecture:
  
1. **Headless Browser Initialization**:
  
    - Launch a Playwright Chromium browser instance using the asynchronous API (`async play_wright()`) or synchronous context manager (`sync_api`).
  
    - Configure custom viewport dimensions and a modern User-Agent string within `browser.new_context()`.
  
2. **DOM Navigation & Element Waiting**:
  
    - Navigate to the target web page using `page.goto(url, wait_until="domcontentloaded")`.
  
    - Explicitly wait for the target data table or container element to render using `page.wait_for_selector("table")`.
  
3. **DOM Content Retrieval & Parsing**:
  
    - Extract rendered HTML content using `page.content()`.
  
    - Pass the raw HTML to **Parsel** (`parsel.Selector(text=html)`) or **pandas** (`pd.read_html(html)`) to retrieve tabular records cleanly using CSS or XPath selectors.
  
  
#### 3. Applied Data Science Level (Country Metadata Extraction)
  
Extract demographic/cultural metadata for European countries to enrich our core project pipeline:
  
1. **Target Data Source**:
  
    - Scrape tabular data from an open web source containing European nation details (e.g., Wikipedia/EU portal tables).
  
    - Extract at least 3 structural variables per country:
  
        - Country Name / ISO Code (e.g., `ES`, `DE`, `FR`).
  
        - Primary Official Language or Capital City.
  
        - Geographic / Cultural Region (e.g., Western Europe, Southern Europe, Nordic).
  
2. **Data Cleaning & Export**:
  
    - Strip reference markers (e.g., `[1]`, `[note A]`) using regular expressions (`re.sub(r'<p align="center"><img src="https://latex.codecogs.com/gif.latex?.*?"/></p>  
', '', text)`).
  
    - Align country names or codes to match the standard `geo` / `CNTRY` keys used in Eurostat and ESS microdata.
  
    - Export the cleaned DataFrame to `data/processed/scraped_country_metadata.csv`.
  
  
### 🌐 Official References for Documentation
  
- **Playwright for Python Official Docs**: [Playwright Python API](https://playwright.dev/python/docs/intro )
  
- **Parsel Selector Library**: [Parsel Documentation](https://parsel.readthedocs.io/en/latest/ )
  
- **`uv` Fast Python Package Manager**: [Astral `uv` Documentation](https://www.google.com/search?q=%5Bhttps://docs.astral.sh/uv/%5D/(https://docs.astral.sh/uv// ))
  
  
### 📚 Recommended Manuals & CheatSheets
  
- **Playwright Cheat Sheet**: [ScrapingBee Playwright Python Guide](https://www.google.com/search?q=https://www.scrapingbee.com/blog/playwright-python/ )
  
- **Parsel XPath/CSS Selectors**: [Scrapy & Parsel Selectors Guide](https://docs.scrapy.org/en/latest/topics/selectors.html )
  
  
💻 **Your Challenge**: Set up `uv`, install Playwright browser binaries, run the scraper script in your local environment, and export `scraped_country_metadata.csv`.
  
When you complete it, let me know to proceed to **Exercise 3.3: SQL Database Persistence & Custom CSV Export**.
  