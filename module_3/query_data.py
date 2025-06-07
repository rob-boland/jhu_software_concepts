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

    cursor.close()

    # Handle None values and computer percentages
    distinct_dict[None] = total_records - sum(distinct_dict.values())
    percentage_dict = {k: round((v / total_records) * 100, 2) for k, v in distinct_dict.items()}

    return percentage_dict

def compute_average_of_column(conn: psycopg2.extensions.connection, column:str) -> float:
    """Compute the average (mean) of a column.
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        column (str): The column to average entries for, e.g., 'gpa'.
        
    Returns:
        average: The average (mean) of entries for the specified column.
    """

    cursor = conn.cursor()

    # Sanitized query for average of specified column
    try:
        query = sql.SQL("SELECT AVG({field}) FROM applicants;").format(
            field=sql.Identifier(column)
        )
        cursor.execute(query)
        avg = cursor.fetchall()[0][0]
        cursor.close()

    # Handle errors if trying to average a text-based column
    except psycopg2.errors.UndefinedFunction as e:
        conn.rollback()
        cursor.close()
        print(f"Unable to compute average for text based column:\n\n{e}")
        return None

    return avg

def compute_conditional_average_of_column(conn: psycopg2.extensions.connection, column:str, where_col:str, where_condition:str) -> float:
    """Compute the average (mean) of a column given a 'WHERE' condition.
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        column (str): The column to average entries for, e.g., 'gpa'.
        where_col (str): The column of the 'WHERE' condition
        where_condition (str): The condition 'WHERE {col} = {condition}'
        
    Returns:
        average: The average (mean) of entries for the specified column.
    """

    cursor = conn.cursor()

    # Sanitized query for average of specified column
    try:
        query = sql.SQL("SELECT AVG({field}) FROM applicants WHERE {conditional_column} = %s;").format(
            field=sql.Identifier(column),
            conditional_column=sql.Identifier(where_col),
        )
        cursor.execute(query, (where_condition,))
        avg = cursor.fetchall()[0][0]
        cursor.close()

    # Handle errors if trying to average a text-based column
    except psycopg2.errors.UndefinedFunction as e:
        conn.rollback()
        cursor.close()
        print(f"Unable to compute average for text based column:\n\n{e}")
        return None

    return avg

def compute_accpetance_percentages(conn: psycopg2.extensions.connection, semester: str) -> int:
    """Compute percentage of accpetances for a specific semester in the database.
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        semester (str): The semester to count entries for, e.g., 'Fall 2024'.
        
    Returns:
        count: The count of entries for the specified semester.
    """

    cursor = conn.cursor()

    # Count total applicants
    count_query = """SELECT COUNT(*) FROM applicants WHERE term = %s;"""
    cursor.execute(count_query, (semester,))
    count = cursor.fetchone()[0]

    # Count accepted applicnats
    accpeted_query = """SELECT COUNT(*) FROM applicants WHERE term = %s AND status LIKE %s;"""
    cursor.execute(accpeted_query, (semester, "Accepted%"))
    accepted_count = cursor.fetchone()[0]

    cursor.close()

    return round((accepted_count / count) * 100, 2)

def create_semester_view(conn: psycopg2.extensions.connection, semester: str, replace:bool=False) -> str:
    """Create a view for all entries of a specific semester. The name will be formatted the same as the
    semester, in lower snake case replacing all whitespace with underscores.
    
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        semester (str): The semester to create the view for.
        replace (bool): If true, this query will replace the view of the same name.
        
    Returns:
        view_str: The name of the view.
    """
    view_name = semester.replace(" ", "_").lower()
    cursor = conn.cursor()

    # Build query and execute
    query_beginning = f"CREATE{' OR REPLACE' if replace else ''}"
    query = sql.SQL(query_beginning + """ VIEW {field} AS
                    SELECT * FROM applicants WHERE term = %s;""").format(
        field=sql.Identifier(view_name),
    )
    try:
        cursor.execute(query, (semester,))
        conn.commit()
        cursor.close()
    except psycopg2.errors.DuplicateTable or psycopg2.errors.InsufficientPrivilege as e:
        conn.rollback()
        cursor.close()
        print(f"View already exists and 'replace not specified or insufficient privileges to replace view:\n\n{e}")
    
    return view_name

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
    table = 'applicants'
    fall_2024_view = create_semester_view(conn, "Fall 2024", replace=False)
    

    n_fall_2024 = count_semester_entries(conn, "Fall 2024")
    international_percentages = compute_percentage_of_distinct_entries(
        conn, "us_or_international")['International']
    gpa_avg = compute_average_of_column(conn, "gpa")
    us_gpa = compute_conditional_average_of_column(conn, "gpa", "us_or_international", "American")
    fall_24_accepted = compute_accpetance_percentages(conn, "Fall 2024")


    

    conn.close()