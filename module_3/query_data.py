import json
import psycopg2
from psycopg2 import OperationalError

from load_data import create_connection

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

    conn.close()