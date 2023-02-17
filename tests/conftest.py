import pytest
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor


@pytest.fixture()
def get_test_db():
    with open("database.sql", "r") as file:
        db_creation_commands = file.read()

    if not os.getenv('TEST_DATABASE_URL'):
        load_dotenv("tests/.env", override=True)
    TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')
    connection = psycopg2.connect(TEST_DATABASE_URL)

    with connection as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("DROP SCHEMA public CASCADE;")
            conn.commit()
            curs.execute(db_creation_commands)

    return connection
