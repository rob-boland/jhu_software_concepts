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

## Approach

### scraper.py Functions

- **_get_robots_txt(url, paths):**
  - Fetches and parses the site's robots.txt file using  robotparser.
  - Checks if the specified paths are allowed for the user agent before scraping begins.
  - Returns a dictionary mapping each path to a boolean indicating permission.

- **_parse_column_titles(soup):**
  - Extracts column titles from the survey table's header (`<thead>`).
  - Cleans and standardizes the column names for downstream use.

- **_parse_rows(soup):**
  - Iterates through the table body (`<tbody>`) to extract all survey result rows.
  - Handles multi-row entries, combining related data into a single list per result.
  - Strips whitespace and collects links where appropriate.

- **scrape_data(agent, url, paths, min_results, max_pages_to_crawl, starting_page):**
  - Manages all elements of the scraping process.
  - Checks robots.txt permissions, then iteratively fetches and parses survey pages using urllib3.
  - Collects all results and column titles, returning them for further processing.

### clean.py Functions and Variables

- **_categories:**
  - Standardized category names for dict and JSON outputs.

- **_separate_program_name_from_level(program_name_and_level):**
  - Splits a combined program name and degree string into separate fields using regex or newline.

- **_clean_secondary_rows(row_data):**
  - Extracts and standardizes GRE, GPA, and comments from secondary rows of survey data.
  - Uses regex to parse scores and rejects missing or malformed data.

- **_convert_date_to_iso(date_str):**
  - Converts date strings to ISO format (YYYY-MM-DD) and extracts the year.
  - Handles parsing errors by returning the original string and the current year.

- **_clean_applicant_status(full_status_str, year):**
  - Standardizes the applicant status (e.g., Accepted, Rejected) and extracts the decision date.
  - Uses regex to find and format the date.

- **save_data(data, filename):**
  - Saves cleaned data to a JSON file with pretty formatting.

- **load_data(filename):**
  - Loads data from a JSON file for further analysis or processing.

- **clean_data(agent, url, paths, min_results, max_pages_to_crawl, starting_page):**
  - Main cleaning pipeline: calls `scrape_data`, then processes and standardizes each result.
  - Builds a dictionary for each row with consistent keys and cleaned values.

## Known Bugs and Limitations

- **Fragile HTML Parsing:** The scraper relies on the current HTML structure of TheGradCafe survey pages. If the website changes its table or row structure, the scraper may fail or return incorrect data.
- **Regex Assumptions:** The regex used for extracting degrees, GRE, and GPA scores assumes specific formats. Unusual or unexpected formats may not be parsed correctly.
- **Date Parsing Errors:** If the date format on the site changes, `_convert_date_to_iso` may fail and default to the current year, potentially introducing inaccuracies.