# database_connection.py
import pandas as pd
import logging
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

file_handler = logging.FileHandler('database_connection.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def connect_to_database(connection_params):
    """
    Connect to the PostgreSQL database.

    Parameters:
        connection_params (dict): Dictionary containing connection parameters.

    Returns:
        sqlalchemy.engine.Engine: SQLAlchemy engine object representing the database connection.
    """
    try:
        connection_string = f"postgresql+psycopg2://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['database']}"
        engine = create_engine(connection_string)
        logger.info("Database connection established successfully")
        return engine
    except Exception as e:
        logger.exception("Failed to connect to the database: %s", e)

def execute_sql_query(engine, sql_query):
    """
    Execute a SQL query on the provided database engine.

    Parameters:
        engine (sqlalchemy.engine.Engine): SQLAlchemy engine object representing the database connection.
        sql_query (str): SQL query to execute.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the results of the SQL query.
    """
    try:
        df = pd.read_sql(sql_query, con=engine)
        logger.info("SQL query executed successfully: %s", sql_query)
        return df
    except Exception as e:
        logger.exception("Failed to execute SQL query: %s", e)
