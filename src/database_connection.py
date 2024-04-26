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

def read_table_to_database(engine, sql_query):
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


def write_dataframe_to_database_table(df, engine, table_name):
    """
    Writes a pandas DataFrame to a database table.

    This function efficiently stores the data in the DataFrame to a specified table within the database
    managed by the provided engine.

    Parameters:
        df (pandas.DataFrame): The pandas DataFrame containing the data to be written.
        engine (sqlalchemy.engine.Engine): A SQLAlchemy engine object representing the connection to the database.
        table_name (str): The name of the table in the database where the data will be stored.

    Returns:
        None
    """

    try:
        df.to_sql(table_name, engine, index=False, if_exists='replace')
        logger.info("Data from DataFrame successfully written to table: %s", table_name)
    except Exception as e:
        logger.exception("Failed to write DataFrame to table: %s", e)

    

