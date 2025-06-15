"""
This module defines the `pages` blueprint for a Flask application.

It includes routes and functions for rendering pages and querying data from a PostgreSQL database.

Functions:
- get_db_connection: Establishes a connection to the PostgreSQL database using
configuration from a JSON file.
- home: Defines the route for the home page, queries the database, and renders the home
page template with query results.

Usage:
Register the `pages` blueprint with a Flask application to enable the defined routes.
"""

# SQL, config, flask imports
import json
import psycopg2
from flask import Blueprint, render_template

# Intra-package imports
from load_data import create_connection
import query_data

bp = Blueprint("pages", __name__)

def get_db_connection() -> psycopg2.extensions.connection:
    """
    Establishes a connection to the PostgreSQL database using configuration from a JSON file.

    The function reads database connection parameters from a JSON file and uses the
    `create_connection` function to create and return a connection object.

    Returns:
        psycopg2.extensions.connection: A connection object to the PostgreSQL database.
    """
    with open(r"D:\GitHub\JHU 25-01\jhu_software_concepts\module_3\data\db_config.json", 'r',
              encoding='utf-8') as file:
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
    """
    Renders the home page of the web application.

    This function queries the PostgreSQL database for relevant data and passes the results
    as context to the home page template for rendering.

    Returns:
        str: The rendered HTML content for the home page.
    """
    # Empty dictionary to store query responses
    query_responses = {}

    conn = get_db_connection()
    # Build view for semester-specific queries
    fall_2024_view = query_data.create_semester_view(conn, "Fall 2024", replace=False)

    # Query database to pull reponses into Flask
    query_responses["Fall 2024 Applicants:"] = query_data.count_semester_entries(conn, "Fall 2024")
    query_responses["Percentage of International Applicants"] =\
        query_data.compute_percentage_of_distinct_entries(
             conn, "us_or_international")['International']
    query_responses["Average GPA"] = query_data.compute_average_of_column(conn, "gpa")
    query_responses["Average GRE"] = query_data.compute_average_of_column(conn, "gre")
    query_responses["Average GRE V"] = query_data.compute_average_of_column(conn, "gre_v")
    query_responses["Average GRE AW"] = query_data.compute_average_of_column(conn, "gre_aw")
    query_responses["Average GPA of US applicants for Fall 2024"] =\
        query_data.compute_conditional_average_of_column(conn, "gpa", "us_or_international",
                                                         "American", table=fall_2024_view)
    query_responses["Percentage of Fall 2024 applicants accepted"] =\
        query_data.compute_accpetance_percentages(conn, table=fall_2024_view)
    query_responses["Average GPA of accepted Fall 2024 applicants"] =\
        query_data.compute_fuzzy_average_of_column(conn, "gpa", "status", "Accepted%",
                                                   table=fall_2024_view)
    query_responses["Number of applicants to JHU Computer Science programs"] =\
        query_data.count_university_program(conn, "Johns Hopkins", "Computer Science")

    conn.close()

    return render_template("pages/home.html", responses=query_responses)
