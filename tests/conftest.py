import pytest
from dotenv import load_dotenv, dotenv_values
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor


@pytest.fixture(autouse=True)  # (scope="session")
def init():
    existing_db_url = os.getenv('DATABASE_URL')
    if not existing_db_url or (
            existing_db_url == dotenv_values(".env")['DATABASE_URL']):
        load_dotenv("tests/.env", override=True)


@pytest.fixture()
def get_test_db():
    DATABASE_URL = os.getenv('DATABASE_URL')
    connection = psycopg2.connect(DATABASE_URL)

    with open("database.sql", "r") as file:
        db_creation_commands = file.read()

    with connection as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("DROP SCHEMA public CASCADE;")
            conn.commit()
            curs.execute(db_creation_commands)

    return connection
