import pytest
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from page_analyzer.app import app


@pytest.fixture(autouse=True)  # (scope="session")
def init():
    load_dotenv("tests/.env", override=True)
    app.secret_key = os.getenv('SECRET_KEY')


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


def missing_db_connection(url):
    actual_database_url = os.getenv("DATABASE_URL")
    os.environ["DATABASE_URL"] = "wrong"

    try:
        client = app.test_client()
        response = client.get(url)
    finally:
        os.environ["DATABASE_URL"] = actual_database_url

    assert response.status_code == 500
    assert response.request.path == url
    assert "Невозможно установить соединение с базой данных." in response.text
