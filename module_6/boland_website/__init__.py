"""
__init__.py

This module initializes the Flask application package for the SQL Data Presentation Web App.
It defines the application factory function `create_app`, which configures and returns a Flask app
instance. This allows for flexible configuration and testing of the web application.

Functions:
    create_app(): Application factory that sets up and returns the Flask app.
"""

from flask import Flask

# Module imports
from boland_website import pages

def create_app():
    """Create and configure the Flask application."""

    # Create Flask app and register blueprints
    app = Flask(__name__, static_folder="static")
    app.register_blueprint(pages.bp)

    return app
