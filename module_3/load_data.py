import json
import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name:str, db_user:str, db_password:str, db_host:str="localhost", db_port:int=5432) -> psycopg2.extensions.connection:
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

def insert_applicant_record(conn:psycopg2.extensions.connection, applicant_data:dict, applicant_i:int) -> None:
    """Insert a new applicant record into the database.
    
    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        applicant_data (dict): Dictionary containing applicant data.
        applicant_i (int): Index of the applicant in the data list. Used as primary key.
    """
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO applicants (p_id, program, comments, date_added, url, status, term, us_or_international, gpa, gre, gre_v, gre_aw, degree)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    try:
        cursor.execute(insert_query, (
            applicant_i,
            applicant_data['program_name'],
            applicant_data['comments'],
            applicant_data['date_of_information_added'],
            applicant_data['url_link'],
            " on ".join(applicant_data['applicant_status']),  # Concatenate status with decision date
            applicant_data['program_start_semester'],
            applicant_data['nationality'],
            applicant_data['gpa'],
            applicant_data['gre_score'],
            applicant_data['gre_v_score'],
            applicant_data['gre_aw_score'],
            applicant_data['program_level']
        ))
        conn.commit()
    except Exception as e:
        print(f"Error inserting record: {e} on applicant number {applicant_i}")
        conn.rollback()
    finally:
        cursor.close()


if __name__ == "__main__":
    applicant_data_path = r"module_2\applicant_data.json"
    with open(applicant_data_path, 'r', encoding='utf-8') as file:
        applicant_data = json.load(file)
    # Create a connection to the PostgreSQL database
    conn = create_connection(
        db_name="grad_cafe",
        db_user="rob",
        db_password="C6pk88A#T5pt8nc$",
        db_host="localhost",
        db_port=5432
    )

    for applicant_i, applicant in enumerate(applicant_data):
        # Insert each applicant record into the database
        print(f"Inserting applicant {applicant_i} of {len(applicant_data)}")
        insert_applicant_record(conn, applicant, applicant_i)

    conn.close()