"""
This module provides various functions to query and analyze data from a PostgreSQL database.

Functions:
- count_semester_entries: Counts the number of entries for a specific semester.
- compute_percentage_of_distinct_entries: Computes the percentage of distinct
entries for a given column.
- compute_average_of_column: Computes the average value of a column.
- compute_conditional_average_of_column: Computes the average value of a
column based on a condition.
- compute_accpetance_percentages: Computes the percentage of acceptances.
- create_semester_view: Creates a view for entries of a specific semester.
- compute_fuzzy_average_of_column: Computes the average value of a column
based on a fuzzy condition.
- count_university_program: Counts the number of entries for a specific university and program.

Usage:
Run this module as a script to perform various database queries and computations.
"""

import json
import psycopg2
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

    query = sql.SQL("""SELECT COUNT(*) FROM {table} WHERE term = %s;""").format(
        table=sql.Identifier("applicants")
    )
    cursor.execute(query, (semester,))
    count = cursor.fetchone()[0]

    cursor.close()

    return count

def compute_percentage_of_distinct_entries(conn: psycopg2.extensions.connection,
                                           column: str, table:str="applicants") -> float:
    """Compute the percentage of distinct entries for a given column.
    
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        column (str): The column to compute the percentage of distinct entries for.
        
    Returns:
        percentage: The percentage of each distinct entry in the specified column.
    """

    cursor = conn.cursor()

    # Sanitized query for distinct entries of specified column
    query = sql.SQL("SELECT DISTINCT({field}) FROM {table};").format(
        field=sql.Identifier(column),
        table=sql.Identifier(table)
    )
    cursor.execute(query)
    result = cursor.fetchall()
    distinct_entries = [x[0] for x in result] if result else None

    # Total number of records in table
    query = sql.SQL("SELECT COUNT({field}) FROM {table};").format(
        field=sql.Identifier(column),
        table=sql.Identifier(table)
    )
    cursor.execute(query)
    total_records = cursor.fetchone()[0]

    # Count occurrences of each distinct entry
    distinct_dict = {}
    for entry in distinct_entries:
        query = sql.SQL("SELECT COUNT(*) FROM {table} WHERE {field} = %s;").format(
            field=sql.Identifier(column),
            table=sql.Identifier(table)
        )
        cursor.execute(query, (entry,))
        count = cursor.fetchone()[0]
        distinct_dict[entry] = count

    cursor.close()

    # Handle None values and computer percentages
    distinct_dict[None] = total_records - sum(distinct_dict.values())
    percentage_dict = {k: round((v / total_records) * 100, 2) for k, v in distinct_dict.items()}

    return percentage_dict

def compute_average_of_column(conn: psycopg2.extensions.connection, column:str,
                              table:str='applicants', rounding:int=2) -> float:
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
        query = sql.SQL("SELECT AVG({field}) FROM {table};").format(
            field=sql.Identifier(column),
            table=sql.Identifier(table)
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

    return round(avg, rounding)

def compute_conditional_average_of_column(conn: psycopg2.extensions.connection, column:str,
                                          where_col:str, where_condition:str,
                                          table:str='applicants') -> float:
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
        query = sql.SQL(
            "SELECT AVG({field}) FROM {table} WHERE {conditional_column} = %s;"
        ).format(
            field=sql.Identifier(column),
            table=sql.Identifier(table),
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

    return round(avg, 2)

def compute_accpetance_percentages(conn: psycopg2.extensions.connection,
                                   table:str='applicants') -> float:
    """Compute percentage of accpetances.
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        
    Returns:
        count: The count of entries for the specified semester.
    """

    cursor = conn.cursor()

    # Count total applicants
    count_query = sql.SQL("SELECT COUNT(*) FROM {table}").format(
            table=sql.Identifier(table),
        )
    cursor.execute(count_query)
    count = cursor.fetchone()[0]

    # Count accepted applicnats
    accpeted_query = sql.SQL("SELECT COUNT(*) FROM {table} WHERE status LIKE %s").format(
            table=sql.Identifier(table),
        )
    cursor.execute(accpeted_query, ("Accepted%",))
    accepted_count = cursor.fetchone()[0]

    cursor.close()

    return round((accepted_count / count) * 100, 2)

def create_semester_view(conn: psycopg2.extensions.connection, semester: str,
                         replace:bool=False) -> str:
    """Create a view for all entries of a specific semester. The name will be formatted the
    same as the semester, in lower snake case replacing all whitespace with underscores.
    
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
    except (psycopg2.errors.DuplicateTable, psycopg2.errors.InsufficientPrivilege) as e:
        conn.rollback()
        cursor.close()
        print("View already exists and 'replace' not specified or ",
              f"insufficient privileges to replace view:\n\n{e}")

    return view_name

def compute_fuzzy_average_of_column(conn: psycopg2.extensions.connection, column:str,
                                    where_col:str, where_condition:str,
                                    table:str='applicants') -> float:
    """Compute the average (mean) of a column given a 'WHERE LIKE' condition.
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
        query = sql.SQL(
            "SELECT AVG({field}) FROM {table} WHERE {conditional_column} LIKE %s;"
        ).format(
            field=sql.Identifier(column),
            table=sql.Identifier(table),
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

    return round(avg, 2)

def count_university_program(conn: psycopg2.extensions.connection, university:str,
                             program:str, table:str="applicants"):
    """Count the number of entries that applied to a given university/program.
    Do not need to include % in the strings.
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        university (str): Name of university to be searched for
        program (str): Name of degree program to be searched for
        
    Returns:
        average: The average (mean) of entries for the specified column.
    """

    cursor = conn.cursor()

    university_fuzzy = f"%{university}%"
    program_fuzzy = f"%{program}%"

    # Sanitized query to select count of entries from a given program
    try:
        query = sql.SQL(
            "SELECT COUNT(*) FROM {table} WHERE {field} LIKE %s AND program LIKE %s;"
        ).format(
            table=sql.Identifier(table),
            field=sql.Identifier("program")
        )
        cursor.execute(query, (university_fuzzy, program_fuzzy))
        avg = cursor.fetchall()[0][0]
        cursor.close()

    # Handle errors if trying to average a text-based column
    except psycopg2.errors.UndefinedFunction as e:
        conn.rollback()
        cursor.close()
        print(f"Unable to compute average for text based column:\n\n{e}")
        return None

    return avg

if __name__ == "__main__":

    # Load applicant data and database configuration from JSON files
    APPLICANT_DATA_PATH = r"module_2\applicant_data.json"
    DB_CONFIG_PATH = r"module_3\data\db_config.json"
    with open(APPLICANT_DATA_PATH, 'r', encoding='utf-8') as file:
        applicant_data = json.load(file)
    with open(DB_CONFIG_PATH, 'r', encoding='utf-8') as file:
        db_config = json.load(file)

    # Create a connection to the PostgreSQL database
    connection = create_connection(
        db_name=db_config["db_name"],
        db_user=db_config["db_user"],
        db_password=db_config["db_password"],
        db_host=db_config["db_host"],
        db_port=db_config["db_port"]
    )
    TABLE_NAME = 'applicants'
    FALL_2024_VIEW = create_semester_view(connection, "Fall 2024", replace=False)

    n_fall_2024 = count_semester_entries(connection, "Fall 2024")
    international_percentages = compute_percentage_of_distinct_entries(
        connection, "us_or_international")['International']
    gpa_avg = compute_average_of_column(connection, "gpa")
    gre_avg = compute_average_of_column(connection, "gre")
    gre_v_avg = compute_average_of_column(connection, "gre_v")
    gre_aw_avg = compute_average_of_column(connection, "gre_aw")
    us_fall_2024_gpa = compute_conditional_average_of_column(connection, "gpa",
                                                             "us_or_international",
                                                             "American", table=FALL_2024_VIEW)
    fall_24_accepted = compute_accpetance_percentages(connection, table=FALL_2024_VIEW)
    fall_24_avg__accepted_gpa = compute_fuzzy_average_of_column(connection, "gpa", "status",
                                                                "Accepted%",
                                                                table=FALL_2024_VIEW)
    jhu_cs_count = count_university_program(connection, "Johns Hopkins", "Computer Science")

    print(f"""1. Applicant count:   {n_fall_2024}
2. International percentage:   {international_percentages}%
3. Average GPA:   {gpa_avg}, Average GRE:{gre_avg},
Average GRE V: {gre_v_avg}, Average GRE AW: {gre_aw_avg}
4. Average US Fall 2024 GPA:   {us_fall_2024_gpa}
5. Percentage of Fall 2024 Acceptances:   {fall_24_accepted}%
6. Average GPA of Fall 2024 Acceptances:   {fall_24_avg__accepted_gpa}
7. Entries for JHU Computer Science Applicants:   {jhu_cs_count}
""")

    connection.close()
