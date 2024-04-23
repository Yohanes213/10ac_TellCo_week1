# database_operations.py
import json
import logging
from src.database_connection import connect_to_database, execute_sql_query

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

file_handler = logging.FileHandler('database_operations.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def perform_database_operations(config_file_path, database_name, sql_query):
    """
    Perform database operations such as loading configuration, connecting to the database,
    executing an SQL query, and storing the results in a DataFrame.

    Parameters:
        config_file_path (str): Path to the JSON configuration file.
        database_name (str): Name of the database.
        sql_query (str): SQL query to execute.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the results of the SQL query.
    """
    try:
        # Load database configuration from JSON file
        with open(config_file_path) as f:
            config = json.load(f)

        # Extract database configuration values
        db_config = config.get('database', {})

        # Define connection parameters
        connection_params = {
            "host": db_config.get('host'),
            "user": db_config.get('user'),
            "password": db_config.get('password'),
            "port": db_config.get('port'),
            "database": database_name
        }

        # Connect to the database
        engine = connect_to_database(connection_params)
        logger.info("Connected to the database.")

        # Execute the SQL query and store the results in a DataFrame
        df = execute_sql_query(engine, sql_query)
        logger.info("Executed SQL query successfully.")

        return df
    except Exception as e:
        logger.exception("An error occurred while performing database operations: %s", e)
        return None
