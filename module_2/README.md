# Name: Jon Robert N. Boland (jboland7)

# Module Info: Module 2 - GradCafe Survey Data Scraper

This module provides tools for scraping, cleaning, and saving graduate admissions survey data from TheGradCafe.com. It is designed to respect the site's robots.txt rules and to output structured, cleaned data for further analysis.

## Project Structure

```
module_2/
├── clean.py                # Cleans and standardizes scraped data
├── scraper.py              # Scrapes data from TheGradCafe.com
├── applicant_data.json     # Pull from running clean.py
```

## Features

- **Respects robots.txt:** Before crawling, the scraper checks robots.txt to ensure all paths are allowed for the user agent.
- **Automated scraping:** Collects survey data from TheGradCafe.com, handling multi-page navigation.
- **Data cleaning:** Standardizes program names, degrees, dates, and test scores for analysis.
- **JSON output:** Saves both raw and cleaned data as JSON files

## Installation

1. **Clone the repository:**
   ```powershell
   git clone git@github.com:rob-boland/jhu_software_concepts.git
   cd <repository directory>
   ```

2. **(Recommended) Create and activate a virtual environment:**
   ```powershell
   python -m venv env
   # On Windows:
   .\env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r ../module_2/requirements.txt
   ```

## Usage

### Cleaning Data

Edit clean.py with necessary parameters (url, number of pages to be scraped, etc.) and then run it to scrape and clean your data.

```powershell
python clean.py
```

This will process the raw data and save the cleaned results to `applicant_data.json`.

## Customization

- Adjust scraping parameters (number of results, pages, etc.) in the `scrape_data` and `clean_data` function calls.
- Extend the cleaning logic in `clean.py` to handle additional fields or custom formats.

## Notes

- The scraper will not crawl if any of the specified paths are disallowed by robots.txt.