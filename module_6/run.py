"""
run.py

This module serves as the entry point for running the Flask web application.
It creates the Flask app instance using the application factory and starts the development server.

Usage:
    python run.py

The app will be available at http://localhost:5000 by default.
"""

import boland_website

if __name__ == "__main__":
    # Create Flask app, run with localhost:5000 address.
    app = boland_website.create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
