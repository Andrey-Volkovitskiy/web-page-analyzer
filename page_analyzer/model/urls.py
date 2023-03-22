from page_analyzer import exceptions
from page_analyzer import model
from page_analyzer.language import txt
from psycopg2.extras import NamedTupleCursor
from datetime import datetime


def add(url_name):
    '''Adds new website to the database

    Agruments:
        name - URL received from a user

    Returns:
        id - website id assigned by the database
        (or raise exception if something went wrong)
    '''
    created_at = datetime.utcnow()
    with model.db.connect() as conn:
        with conn.cursor() as curs:
            curs.execute(
                    """SELECT (id) FROM urls
                       WHERE name = %s""",
                    (url_name, )
                )
            existing_id = curs.fetchone()

        if existing_id:
            raise exceptions.UrlAlreadyExists(
                txt.MESSAGES['PAGE_EXISTS'],
                existing_id[0])

        with conn.cursor() as curs:
            curs.execute(
                """INSERT INTO urls (name, created_at)
                    VALUES (%s, %s)
                    RETURNING id""",
                (url_name, created_at)
            )
            id = curs.fetchone()[0]
    return id


def get_list_with_latest_check():
    '''Returns the list of websites with last check result for each.

    Returns:
        list of named tuples describung websites
    '''
    with model.db.connect() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                """SELECT DISTINCT ON (urls.id)
                          urls.id AS url_id,
                          name,
                          urls.created_at AS url_created_at,
                          checks.id AS check_id,
                          status_code,
                          h1,
                          title,
                          description,
                          checks.created_at AS check_created_at
                   FROM urls
                   LEFT JOIN checks ON urls.id = checks.url_id
                   ORDER BY urls.id, check_created_at DESC
            """)
            return curs.fetchall()


def find(id):
    '''Returns information about certain website from database

    Agruments:
        id - website id from database

    Returns:
        named tuple describung the website
    '''
    with model.db.connect() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                "SELECT * FROM urls WHERE id=%s", (id, )
            )
            the_url = curs.fetchone()

    return the_url
