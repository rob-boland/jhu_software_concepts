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

    query_responses = {}

    conn = get_db_connection()

    # Build view for semester-specific queries
    fall_2024_view = query_data.create_semester_view(conn, "Fall 2024", replace=False)

    # Query database to pull reponses into Flask
    query_responses["n_fall_2024"] = query_data.count_semester_entries(conn, "Fall 2024")
    query_responses["international_percentages"] = query_data.compute_percentage_of_distinct_entries(
        conn, "us_or_international")['International']
    query_responses["gpa_avg"] = query_data.compute_average_of_column(conn, "gpa")
    query_responses["gre_avg"] = query_data.compute_average_of_column(conn, "gre")
    query_responses["gre_v_avg"] = query_data.compute_average_of_column(conn, "gre_v")
    query_responses["gre_aw_avg"] = query_data.compute_average_of_column(conn, "gre_aw")
    query_responses["us_fall_2024_gpa"] = query_data.compute_conditional_average_of_column(conn, "gpa", "us_or_international", "American", table=fall_2024_view)
    query_responses["fall_24_accepted"] = query_data.compute_accpetance_percentages(conn, table=fall_2024_view)
    query_responses["fall_24_avg__accepted_gpa"] = query_data.compute_fuzzy_average_of_column(conn, "gpa", "status", "Accepted%", table=fall_2024_view)
    query_responses["jhu_cs_count"] = query_data.count_university_program(conn, "Johns Hopkins", "Computer Science")

    test = query_data.count_semester_entries(conn, "Fall 2024")
    print(test)

    return render_template("pages/home.html", responses=query_responses)