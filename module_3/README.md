# Name: Jon Robert N. Boland (jboland7)

# Module Info: Module 3 - SQL Data Presentation Web App

This module provides a Flask web application for querying, analyzing, and presenting data from a SQL database. It includes scripts for loading data, running queries, and displaying results interactively.

## Project Structure

```
module_3/
├── load_data.py                # Loads data into the SQL database
├── query_data.py               # Executes SQL queries and returns results
├── run.py                      # Entry point to run the Flask app
├── data/
│   └── db_config.json          # Database configuration
├── sql_presentation/
│   ├── app.py                  # Flask app factory
│   ├── pages.py                # Flask routes and query logic
│   ├── static/
│   │   └── styles.css          # CSS for web app
│   └── templates/
│       └── pages/
│           └── home.html       # Main page template
```

## Features

 - **Database Loading**: Use load_data.py to populate the SQL database from source files.
 - **Flexible Querying**: Use query_data.py to run SQL queries and retrieve results.
 - **Web Presentation**: Flask app displays query results and analytics in styled containers on the home page.
 - **Dynamic Rendering**: All query responses are passed from Flask and rendered as blocks for easy extension and styling.

## Installation

1. **Clone the repository:**
   ```powershell
   git clone git@github.com:rob-boland/jhu_software_concepts.git
   cd <repository directory>/module_3
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
   pip install -r ../module_3/requirements.txt
   ```

## Usage

### Load Data into Database
Edit load_data.py as needed and run
```powershell
python load_data.py
```

### Query Data from Database
Edit query_data.py or use it as a module to run SQL queries
```powershell
python query_data.py
```

### Run the Web Application
Start the Flask app to view and interact with query results in your browser:
```powershell
python run.py
```

Navigate to http://localhost:5000 to view the web interface.

### Customization
 - Add or modify SQL queries in pages.py to change what is displayed on the home page.
 - Update home.html to change the layout or add new data blocks.
 - Style the app by editing static/styles.css.
 - Adjust database configuration in data/db_config.json as needed.

## Notes

- Database configurations are not included in this package. By default, the program looks for a config file at data/db_config.json.
- Many queries depend on building specific views in the database. Ensure you have adequate permissions to adjust the views you need to utilize, or create your own.

## Approach

 - **load_data.py**: Loads data from source files and populates the SQL database using configuration in db_config.json.
 - **query_data.py**: Provides functions to execute SQL queries and return results for use in the web app or for analysis.
 - **sql_presentation/app.py**: Sets up the Flask application and configuration.
 - **sql_presentation/pages.py**: Defines Flask routes and logic for querying the database and passing results to templates. All query responses are passed as a dictionary to the home page and rendered dynamically.
 - **sql_presentation/templates/pages/home.html**: Renders each query response in a styled block using Jinja2 templating. Uses CSS classes for easy customization.

## Known Bugs and Limitations

 - **Database Schema Assumptions**: The code assumes a specific schema and may require updates if the database structure changes.
 - **Error Handling**: Minimal error handling for database connection or query failures.
 - **Static Query Set**: Only queries defined in pages.py are available on the web interface unless extended.
 - **No Authentication**: The web app is open and does not restrict access or editing.