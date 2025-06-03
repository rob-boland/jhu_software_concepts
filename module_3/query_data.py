import json
import psycopg2
from psycopg2 import OperationalError
from psycopg2 import sql

from load_data import create_connection

def count_semester_entries(conn: psycopg2.extensions.connection, semester: str) -> int:
    """Count the number of entries for a specific semester in the database.
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        semester (str): The semester to count entries for, e.g., 'Fall 2024'.
        
    Returns:
        count: The count of entries for the specified semester.
    """

    cursor = conn.cursor()

    query = """SELECT COUNT(*) FROM applicants WHERE term = %s;"""
    cursor.execute(query, (semester,))
    count = cursor.fetchone()[0]

    cursor.close()

    return count

def compute_percentage_of_distinct_entries(conn: psycopg2.extensions.connection, column: str) -> float:
    """Compute the percentage of distinct entries for a given column.
    
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        column (str): The column to compute the percentage of distinct entries for.
        
    Returns:
        percentage: The percentage of each distinct entry in the specified column.
    """
    
    cursor = conn.cursor()

    # Sanitized query for distinct entries of specified column
    query = sql.SQL("SELECT DISTINCT({field}) FROM applicants;").format(
        field=sql.Identifier(column)
    )
    cursor.execute(query)
    result = cursor.fetchall()
    distinct_entries = [x[0] for x in result] if result else None

    # Total number of records in table
    query = sql.SQL("SELECT COUNT({field}) FROM applicants;").format(
        field=sql.Identifier(column)
    )
    cursor.execute(query)
    total_records = cursor.fetchone()[0]

    # Count occurrences of each distinct entry
    distinct_dict = dict()
    for entry in distinct_entries:
        query = sql.SQL("SELECT COUNT(*) FROM applicants WHERE {field} = %s;").format(
            field=sql.Identifier(column)
        )
        cursor.execute(query, (entry,))
        count = cursor.fetchone()[0]
        distinct_dict[entry] = count
    
    # Handle None values and computer percentages
    distinct_dict[None] = total_records - sum(distinct_dict.values())
    percentage_dict = {k: (v / total_records) * 100 for k, v in distinct_dict.items()}

    return percentage_dict

if __name__ == "__main__":

    # Load applicant data and database configuration from JSON files
    applicant_data_path = r"module_2\applicant_data.json"
    db_config_path = r"module_3\data\db_config.json"
    with open(applicant_data_path, 'r', encoding='utf-8') as file:
        applicant_data = json.load(file)
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

    n_fall_2024 = count_semester_entries(conn, "Fall 2024")
    percentages = compute_percentage_of_distinct_entries(conn, "us_or_international")
    

    conn.close()