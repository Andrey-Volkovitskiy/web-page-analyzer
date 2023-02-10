from page_analyzer import model
import psycopg2
from psycopg2.extras import NamedTupleCursor
import validators
from datetime import datetime, timezone
from urllib.parse import urlparse, urlunparse


def add(name):
    '''Adds new website to the database

    Agruments:
        name - URL received from a user

    Returns:
        id - website id assigned by the database
        (or raise exception if something went wrong)
    '''

    if len(name) == 0:
        raise model.IncorrectUrlName("URL обязателен")

    elif len(name) > 255:
        raise model.IncorrectUrlName("URL превышает 255 символов")

    is_valid_url = validators.url(name, public=True)
    url_parts = urlparse(name)
    normalized_name = urlunparse((
                        url_parts.scheme,
                        url_parts.netloc,
                        '', '', '', ''))
    if not is_valid_url or normalized_name == '':
        raise model.IncorrectUrlName("Некорректный URL")

    connection = model.db.connect()

    created_at = datetime.now(timezone.utc)
    with connection as conn:
        try:
            with conn.cursor() as curs:
                curs.execute(
                    """INSERT INTO urls (name, created_at)
                       VALUES (%s, %s)
                       RETURNING id""",
                    (normalized_name, created_at)
                )
                id = curs.fetchone()[0]

        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            with conn.cursor() as curs:
                curs.execute(
                    """SELECT (id) FROM urls
                       WHERE name = %s""",
                    (normalized_name, )
                )
                id = curs.fetchone()[0]
            raise model.UrlAlreadyExists("Страница уже существует", id)

    return id


def get_list(per_page=-1, page=1):
    '''Returns the list of websites from database (implements pagination)

    Agruments:
        per_rage - number of websites per page
            (default=-1, which means get all websites without pagination)
        page - the number of requested page (default=1)

    Returns:
        list of named tuples describung websites
    '''
    connection = model.db.connect()
    with connection as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            limit = None if per_page == -1 else per_page
            offset = 0 if per_page < 1 else per_page * (page - 1)

            curs.execute(
                """SELECT * FROM urls
                 ORDER BY created_at DESC
                 LIMIT %s OFFSET %s""",
                (limit, offset)
            )
            list_of_urls = curs.fetchall()

    return list_of_urls


def get_list_with_latest_check(per_page=-1, page=1):
    '''Returns the list of websites with last check results for each

    Agruments:
        per_rage - number of websites per page
            (default=-1, which means get all websites without pagination)
        page - the number of requested page (default=1)

    Returns:
        list of named tuples describung websites
    '''
    connection = model.db.connect()
    with connection as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            limit = None if per_page == -1 else per_page
            offset = 0 if per_page < 1 else per_page * (page - 1)

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
                   LIMIT %s OFFSET %s""",
                (limit, offset)
            )
            list_of_urls = curs.fetchall()

    conn.close()
    return list_of_urls


def find(id):
    '''Returns information about certain website from database

    Agruments:
        id - website id from database

    Returns:
        named tuple describung the website
    '''
    connection = model.db.connect()
    with connection as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                "SELECT * FROM urls WHERE id=%s", (id, )
            )
            the_url = curs.fetchone()
    conn.close()

    return the_url