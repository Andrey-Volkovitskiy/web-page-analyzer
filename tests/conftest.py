import pytest
from dotenv import load_dotenv, dotenv_values
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor


@pytest.fixture(autouse=True)  # (scope="session")
def init():
    existing_db_url = os.getenv('DATABASE_URL')
    if not existing_db_url or (
            os.getenv('PROJECT_ENV') == "Dev" and
            existing_db_url == dotenv_values(".env").get('DATABASE_URL')):
        load_dotenv("tests/.env", override=True)
        os.environ['SECRET_KEY'] = "testPass"


@pytest.fixture()
def get_test_db():
    DATABASE_URL = os.getenv('DATABASE_URL')
    connection = psycopg2.connect(DATABASE_URL)

    db_schema_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..', 'database.sql'))
    with open(db_schema_path, "r") as file:
        db_creation_commands = file.read()

    with connection as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("DROP SCHEMA public CASCADE")
            curs.execute("CREATE SCHEMA public")
            conn.commit()
            curs.execute(db_creation_commands)

    return connection
