# perform_database_operations.py
import json
import logging
from src.database_connection import connect_to_database, write_dataframe_to_database_table,read_table_to_database

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

file_handler = logging.FileHandler('database_operations.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def perform_database_operations(config_file_path, database_name, sql_query, data_to_write=None, table_name=None):
    """
    Perform database operations such as loading configuration, connecting to the database,
    executing an SQL query (optional), writing data to a table (optional), and storing query results (if applicable) in a DataFrame.

    Parameters:
        config_file_path (str): Path to the JSON configuration file.
        database_name (str): Name of the database.
        sql_query (str): SQL query to execute (can be None if only writing data).
        data_to_write (pd.DataFrame, optional): The pandas DataFrame containing data to write to a table. Defaults to None.
        table_name (str): The name of the table (can be None if only reading).

    Returns:
        pd.DataFrame (optional): A pandas DataFrame containing the results of the SQL query,
                                  or None if only writing data.
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

        # Execute the SQL query and store the results in a DataFrame (if provided)
        df = None
        if sql_query:
            df = read_table_to_database(engine, sql_query) 
            logger.info("Executed SQL query successfully.")

        # Write data to a table (if provided)
        if data_to_write is not None:
            write_dataframe_to_database_table(data_to_write, engine, table_name)
            logger.info("Data written to table: %s", table_name)

        return df
    except Exception as e:
        logger.exception("An error occurred while performing database operations: %s", e)
        return None