import psycopg2
import os


def init():
    '''Establishes a database connection

    Returns:
        connection - session instanse
        error - error text message
    '''
    connection, error = None, None
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(DATABASE_URL)
    except Exception as e:
        error = (f"Can't establish connection to database. "
                 f"Exception '{e}' type: {type(e)}")

    return (connection, error)
