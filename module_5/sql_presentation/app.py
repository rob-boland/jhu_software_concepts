"""
This module defines the Flask application factory function `create_app`.

It imports and registers the `pages` blueprint from the `sql_presentation` package.

Functions:
- create_app: Creates and configures the Flask application instance.

Usage:
Use this module to initialize and configure the Flask application.
"""
from flask import Flask

# Module imports
from sql_presentation import pages


def create_app():
    """Create and configure the Flask application."""

    # Create Flask app and register blueprints
    app = Flask(__name__)
    app.register_blueprint(pages.bp)

    return app
