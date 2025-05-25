# Boland Website Flask Application

This is a Flask web application written by Jon Robert N. Boland. The app is organized as a Python package and can be run by installing requirements.txt and running python run.py.

## Project Structure

Module_1/
│   run.py
│   requirements.txt
│
├───boland_website/
│   │   __init__.py
│   │   pages.py
│   │
│   ├───static/
│   │   └───images/
│   │   styles.css
│   └───templates/
│       │   base.html
│       │   _navigation.html
│       └───pages/
│           home.html
│           contact.html
|           projects.html

## Installation

1. **Clone the repository:**
   $ cd <repository-folder>
   $ git clone git@github.com:rob-boland/jhu_software_concepts.git

2. **(Recommended) Create and activate a virtual environment:**
   $ cd <repository-folder>
   $ python -m venv env
   # On Windows:
        .\env\Scripts\activate
   # On macOS/Linux:
        source env/bin/activate

3. **Install dependencies:**
   $ pip install -r requirements.txt


## Running the Application

This application is designed to be run simply with the run.py file:

$ python run.py

The app will start in debug mode and be accessible at [http://localhost:5000].

## Project Organization

- `run.py`: Entry point for running the app directly.
- `boland_website/`: Main package containing the Flask app factory and blueprints.
- `static/`: Static files (CSS, images, etc.).
- `templates/`: Jinja2 templates for HTML pages.
- `requirements.txt`: Python dependencies.

## Customization

- Add new pages by creating new view functions and templates in the `boland_website` package.
- Update navigation in `_navigation.html`.
- Add static assets (images, CSS) to the `static/` directory.