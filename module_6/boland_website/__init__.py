from flask import Flask

# Module imports
from boland_website import pages

def create_app():
    """Create and configure the Flask application."""
    
    # Create Flask app and register blueprints
    app = Flask(__name__)
    app.register_blueprint(pages.bp)
    
    return app