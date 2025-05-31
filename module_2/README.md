# GradCafe Survey Data Scraper (Module 2)

This module provides tools for scraping, cleaning, and saving graduate admissions survey data from TheGradCafe.com. It is designed to respect the site's robots.txt rules and to output structured, cleaned data for further analysis.

## Project Structure

```
module_2/
├── clean.py                # Cleans and standardizes scraped data
├── scraper.py              # Scrapes data from TheGradCafe.com
├── data/
│   ├── cleaned_survey_data.json
│   └── survey_data_working.json
```

## Features

- **Respects robots.txt:** Before crawling, the scraper checks robots.txt to ensure all paths are allowed for the user agent.
- **Automated scraping:** Collects survey data from TheGradCafe.com, handling multi-page navigation.
- **Data cleaning:** Standardizes program names, degrees, dates, and test scores for analysis.
- **JSON output:** Saves both raw and cleaned data as JSON files for easy use in data science workflows.

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
   pip install -r ../Module_1/requirements.txt
   ```

## Usage

### Scraping Data

To scrape survey data and save the raw results:

```powershell
python scraper.py
```

This will crawl TheGradCafe survey pages (respecting robots.txt) and save the results to `data/survey_data_working.json`.

### Cleaning Data

To clean and standardize the scraped data:

```powershell
python clean.py
```

This will process the raw data and save the cleaned results to `data/cleaned_survey_data.json`.

## Customization

- Adjust scraping parameters (number of results, pages, etc.) in the `scrape_data` and `clean_data` function calls.
- Extend the cleaning logic in `clean.py` to handle additional fields or custom formats.

## Notes

- The scraper will not crawl any paths disallowed by robots.txt.
- All data is saved in JSON format for easy downstream analysis.

## License

This project is for educational purposes.
