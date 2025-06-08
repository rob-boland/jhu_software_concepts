from flask import Blueprint, render_template

import psycopg2
import json

from load_data import create_connection
import query_data

bp = Blueprint("pages", __name__)

def get_db_connection() -> psycopg2.extensions.connection:
    with open(r"D:\GitHub\JHU 25-01\jhu_software_concepts\module_3\data\db_config.json", 'r', encoding='utf-8') as file:
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

# Define routes for each page
@bp.route("/")
def home():

    conn = get_db_connection()

    test = query_data.count_semester_entries(conn, "Fall 2024")
    print(test)

    return render_template("pages/home.html")