import psycopg2
import os
from page_analyzer import model


def connect():
    '''Establishes a database connection

    Returns:
        connection - session instanse
        (or raise exception if something went wrong)
    '''
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(DATABASE_URL)

    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as e:
        raise model.DbConnecionError(
            "Невозможно установить соединение с базой данных. "
            f"Exception '{e}'")

    return connection
