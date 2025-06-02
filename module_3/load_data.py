import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
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

conn = create_connection(
    db_name="grad_cafe",
    db_user="rob",
    db_password="C6pk88A#T5pt8nc$",
    db_host="localhost",
    db_port=5432
)

def close_connection(connection):
    """Close the database connection.
    
    Args:
        connection: A psycopg2 connection object.
    """
    if connection:
        connection.close()
        print("Database connection closed.")
    else:
        print("No connection to close.")
close_connection(conn)