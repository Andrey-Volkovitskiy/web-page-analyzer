from page_analyzer import model
from page_analyzer.language import txt
import psycopg2
from psycopg2.extras import NamedTupleCursor
import validators
from datetime import datetime
from urllib.parse import urlparse, urlunparse


def normalize(name):
    '''Checks if URL name is valid. If valid returns a normalized name.

    Arguments:
        name - URL name

    Returns:
        normalized URL name
        (or raise an excetpion if the name isn't valid)
    '''
    if len(name) == 0:
        raise model.IncorrectUrlName(txt.MESSAGES['URL_CANT_BE_EMPTY'])

    elif len(name) > 255:
        raise model.IncorrectUrlName(txt.MESSAGES['URL_TOO_LONG'])

    url_parts = urlparse(name, scheme='http')
    normalized_name = urlunparse((
        url_parts.scheme,
        url_parts.netloc or url_parts.path,
        '', '', '', ''))

    is_valid_url = validators.url(normalized_name, public=True)
    if not is_valid_url or normalized_name == '':
        raise model.IncorrectUrlName(txt.MESSAGES['INCORRECT_URL'])

    return normalized_name


def add(name):
    '''Adds new website to the database

    Agruments:
        name - URL received from a user

    Returns:
        id - website id assigned by the database
        (or raise exception if something went wrong)
    '''
    normalized_name = normalize(name)

    created_at = datetime.utcnow()
    with model.db.connect() as conn:
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
            raise model.UrlAlreadyExists(txt.MESSAGES['PAGE_EXISTS'], id)

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
