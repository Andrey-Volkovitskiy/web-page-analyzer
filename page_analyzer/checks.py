from page_analyzer import db, urls
from psycopg2.extras import NamedTupleCursor
from datetime import datetime, timezone


def add(url_id, status_code=None, h1=None, title=None, description=None):
    '''Adds results of a website check to the database

    Agruments:
        url_id - id of the website to check
        status_code - http response code
        h1, title, description - the tags expracted from site hlml

    Returns:
        id - check id assigned by the database
        error message - if somethig went wrong
    '''
    id, error = None, None

    if url_id is None:
        error = "url_id can't be 'None'"
        return (id, error)

    connection, connect_error = db.connect()
    if connect_error:
        return (id, connect_error)

    if urls.find(url_id) is None:
        error = "url_id not found in database"
        return (id, error)

    created_at = datetime.now(timezone.utc)
    with connection as conn:
        with conn.cursor() as curs:
            curs.execute(
                """INSERT INTO checks
                   (url_id, status_code, h1, title, description, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (url_id, status_code, h1, title, description, created_at)
            )
            id = curs.fetchone()[0]

    conn.close()
    return (id, error)


def get_list(url_id, per_page=-1, page=1):
    '''Returns a list of checks for a certain url (implements pagination)

    Agruments:
        url_id - id of the website of interest
        per_rage - number of websites per page
            (default=-1, which means get all websites without pagination)
        page - the number of requested page (default=1)

    Returns:
        list of named tuples describung websites
    '''
    connection, _ = db.connect()
    with connection as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            limit = None if per_page == -1 else per_page
            offset = 0 if per_page < 1 else per_page * (page - 1)

            curs.execute(
                """SELECT * FROM checks
                   WHERE url_id=%s
                   ORDER BY created_at DESC
                   LIMIT %s OFFSET %s""",
                (url_id, limit, offset)
            )
            list_of_checks = curs.fetchall()

    conn.close()
    return list_of_checks


def find_latest(url_id):
    '''Returns information about last check of certain url

    Agruments:
        id - id of the website of interest

    Returns:
        named tuple describung the check results
    '''
    connection, _ = db.init()
    with connection as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                """SELECT * FROM checks
                   WHERE url_id=%s
                   ORDER BY created_at DESC
                   LIMIT 1""",
                (url_id, )
            )
            the_check = curs.fetchone()

    conn.close()
    return the_check
