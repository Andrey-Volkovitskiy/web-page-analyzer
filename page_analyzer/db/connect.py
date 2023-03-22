import psycopg2
import os
from page_analyzer import exceptions
from page_analyzer.language import txt


def connect_to_db():
    '''Establishes a database connection

    Returns:
        connection - session instanse
        (or raise exception if something went wrong)
    '''
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(DATABASE_URL)

    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as e:
        raise exceptions.DbConnecionError(
            f"{txt.MESSAGES['CANT_CONNECT_TO_DB']} "
            f"Exception '{e}'")

    return connection
