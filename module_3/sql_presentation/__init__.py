from flask import Flask
import psycopg2
import json

# Module imports
from sql_presentation import pages
from load_data import create_connection

def get_db_connection(db_config_path:str) -> psycopg2.extensions.connection:
    with open(db_config_path, 'r', encoding='utf-8') as file:
            db_config = json.load(file)

    # Create a connection to the PostgreSQL database
    conn = create_connection(
        db_name=db_config["db_name"],
        db_user=db_config["db_user"],
        db_password=db_config["db_password"],
        db_host=db_config["db_host"],
        db_port=db_config["db_port"]
    )
    
    return conn

def create_app():
    """Create and configure the Flask application."""
    
    # Create Flask app and register blueprints
    app = Flask(__name__)
    app.register_blueprint(pages.bp)
    
    return app