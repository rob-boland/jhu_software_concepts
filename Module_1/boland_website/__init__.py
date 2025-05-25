from flask import Flask

# Module imports
from boland_website import pages

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(pages.bp)
    
    return app