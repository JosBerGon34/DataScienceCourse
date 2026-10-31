---
layout: default
---

# 🟢 < Module  3.2 > Modern Web Scraping for Data Science

## 🎯 Context & Objectives
In modern Data Science, structured data is not always neatly packaged in CSVs or SQL databases. Often, valuable macroeconomic or sociological indicators must be harvested directly from live web pages or dynamic REST APIs.

In this exercise, you will build an ethical, robust web scraping pipeline using `BeautifulSoup` and `requests`, adhering to `robots.txt` guidelines and implementing rate limiting and error handling.

---

## 📑 Exercise Instructions

### 1. Architectural & Syntactic Specification
When extracting data from HTML trees, target specific DOM elements using CSS selectors:
* Use `requests.get(url, headers=headers)` with custom User-Agent strings to mimic legitimate browser requests.
* Parse the raw text content via `BeautifulSoup(html_content, 'html.parser')`.
* Implement polite scraping practices (e.g., `time.sleep(sec)`) to prevent server overloading.

---

## 2. Practical Task

1. **Target Identification**: Select a public target page containing tabular statistical data or indicators.
2. **Scraper Implementation**: Write a Python script or notebook that:
   * Sends an HTTP GET request with robust error handling (`try-except`, checking status codes `200`, `403`, `404`).
   * Extracts target table rows and columns using BeautifulSoup selectors.
   * Cleans and structures the extracted text into a pandas DataFrame.
3. **Persistence**: Export the scraped dataset cleanly to `data/processed/scraped_data.csv`.

---

## 🌐 Official References & Documentation
* **Requests Library**: [Requests: HTTP for Humans™](https://requests.readthedocs.io/)
* **Beautiful Soup Documentation**: [Beautiful Soup 4 Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---
> 💻 **Your Challenge:** Build and execute your web scraper locally, ensure polite rate limiting, and save your processed dataset before moving on to Module 3.3! 🚀📊