import pytest
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor


@pytest.fixture()
def get_test_db():
    if os.getenv('PROJECT_ENV') not in (
            "GitHub_Workflow_Tests", "Poduction"):
        load_dotenv("tests/.env", override=True)

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
