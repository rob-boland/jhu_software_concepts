"""
This module provides functionality for loading applicant data from a JSON file and inserting it
into a PostgreSQL database.

Functions:
- create_connection: Establishes a connection to the PostgreSQL database.
- insert_applicant_record: Inserts an applicant record into the database.

Usage:
Run this module as a script to load applicant data from a JSON file and insert it into the
database.
"""

import json
import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name:str, db_user:str, db_password:str, db_host:str="localhost",
                      db_port:int=5432) -> psycopg2.extensions.connection:
    """Create a database connection to the PostgreSQL database specified by the
    connection parameters.
    
    Args:
        db_name (str): Database name.
        db_user (str): Database user.
        db_password (str): Database password.
        db_host (str): Database host.
        db_port (int): Database port.
    
    Returns:
        connection: A psycopg2 connection object or None if the connection fails.
    """
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to the PostgreSQL database established successfully.")
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
    return connection

def insert_applicant_record(connection:psycopg2.extensions.connection, applicant_data_dict:dict,
                            applicant_number:int) -> None:
    """Insert a new applicant record into the database.
    
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        applicant_data (dict): Dictionary containing applicant data.
        applicant_i (int): Index of the applicant in the data list. Used as primary key.
    """

    cursor = connection.cursor()
    insert_query = """
    INSERT INTO applicants (p_id, program, comments, date_added, url, status, term, us_or_international, gpa, gre, gre_v, gre_aw, degree)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    try:
        cursor.execute(insert_query, (
            applicant_number,
            f"{applicant_data_dict['university']} : {applicant_data_dict['program_name']}",
            applicant_data_dict['comments'],
            applicant_data_dict['date_of_information_added'],
            applicant_data_dict['url_link'],
            " on ".join(applicant_data_dict['applicant_status']),  # Concat status w/ decision date
            applicant_data_dict['program_start_semester'],
            applicant_data_dict['nationality'],
            applicant_data_dict['gpa'],
            applicant_data_dict['gre_score'],
            applicant_data_dict['gre_v_score'],
            applicant_data_dict['gre_aw_score'],
            applicant_data_dict['program_level']
        ))
        connection.commit()
    except psycopg2.OperationalError as e:
        print(f"Error inserting record: {e} on applicant number {applicant_number}")
        connection.rollback()
    finally:
        cursor.close()


if __name__ == "__main__":
    APPLICANT_DATA_PATH = r"module_2\applicant_data.json"
    DB_CONFIG_PATH = r"module_3\data\db_config.json"
    with open(APPLICANT_DATA_PATH, 'r', encoding='utf-8') as file:
        applicant_data = json.load(file)
    with open(DB_CONFIG_PATH, 'r', encoding='utf-8') as file:
        db_config = json.load(file)

    # Create a connection to the PostgreSQL database
    conn = create_connection(
        db_name=db_config["db_name"],
        db_user=db_config["db_user"],
        db_password=db_config["db_password"],
        db_host=db_config["db_host"],
        db_port=db_config["db_port"]
    )

    for applicant_i, applicant in enumerate(applicant_data):
        # Insert each applicant record into the database
        print(f"Inserting applicant {applicant_i} of {len(applicant_data)}")
        insert_applicant_record(conn, applicant, applicant_i)

    conn.close()
