from page_analyzer import model
from psycopg2.extras import NamedTupleCursor
from datetime import datetime, timezone


def add(url_id):
    '''Checks a website and adds the results to the database

    Agruments:
        url_id - id of the website to checkl

    Returns:
        id - check id assigned by the database
        (or raise exception if something went wrong)
    '''
    if url_id is None:
        raise model.UrlIdIsNone("url_id не может иметь значение 'None'")

    url = model.urls.find(url_id)

    if url is None:
        raise model.UrlIdNotFound(f"url_id '{url_id}' отсутсвует в базе даных")

    check_result = model.analyzer.check(url.name)

    with model.db.connect() as conn:
        with conn.cursor() as curs:
            curs.execute(
                """INSERT INTO checks
                   (url_id, status_code, h1, title, description, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (url_id,
                 check_result['status_code'],
                 check_result['h1'],
                 check_result['title'],
                 check_result['description'],
                 datetime.now(timezone.utc))
            )
            id = curs.fetchone()[0]

    return id


def get_list(url_id):
    '''Returns a list of checks for a certain url (implements pagination)

    Agruments:
        url_id - id of the website of interest

    Returns:
        list of named tuples describung checks
    '''
    with model.db.connect() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                """SELECT * FROM checks
                   WHERE url_id=%s
                   ORDER BY created_at DESC""",
                (url_id, )
            )
            list_of_checks = curs.fetchall()

    return list_of_checks


def find_latest(url_id):
    '''Returns information about last check of certain url

    Agruments:
        url_id - id of the website of interest

    Returns:
        named tuple describung the check results
    '''
    with model.db.connect() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                """SELECT * FROM checks
                   WHERE url_id=%s
                   ORDER BY created_at DESC
                   LIMIT 1""",
                (url_id, )
            )
            the_check = curs.fetchone()

    return the_check
