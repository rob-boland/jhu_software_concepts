"""
This script serves as the entry point for running the Flask application.

It imports the `app` module from `sql_presentation`, creates the Flask application instance,
and starts the server on localhost at port 5000 with debugging enabled.

Usage:
Run this script to start the web application.
"""

from sql_presentation import app

if __name__ == "__main__":
    # Create Flask app, run with localhost:5000 address.
    app = app.create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
