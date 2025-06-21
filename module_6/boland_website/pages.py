"""
pages.py

This module defines the Flask routes and page logic for the SQL Data Presentation Web App.
It handles HTTP requests, executes SQL queries using helper functions, and passes query results
to Jinja2 templates for dynamic rendering in the web interface.

Functions:
    home(): Renders the home page with query results and analytics.
    [Other route functions]: Define additional pages or API endpoints as needed.
"""

from flask import Blueprint, render_template

bp = Blueprint("pages", __name__)

# Define routes for each page
@bp.route("/")
def home():
    """Generate home HTML"""
    return render_template("pages/home.html")

@bp.route("/contact")
def contact():
    """Generate contact HTML"""
    return render_template("pages/contact.html")

@bp.route("/projects")
def projects():
    """Generate projects HTML"""
    return render_template("pages/projects.html")
