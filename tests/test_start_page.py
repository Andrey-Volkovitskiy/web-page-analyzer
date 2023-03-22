import pytest
from page_analyzer.app import app
from psycopg2.extras import NamedTupleCursor
from datetime import datetime
from flask import url_for


with app.test_request_context():
    GET_PAGE = url_for('get_new')
    POST_PAGE = url_for('post_new')
    SHOW_PAGE = url_for('show_url', id=1)


def test_basic_content():
    client = app.test_client()
    response = client.get(GET_PAGE)
    assert "Бесплатно проверяйте сайты на SEO пригодность" in response.text
    assert "Проверить" in response.text


def test_add_new_correct_url(get_test_db):
    URL = "http://www.mytest-12.com"
    pre_test_time = datetime.utcnow()

    client = app.test_client()
    response = client.post(POST_PAGE, data={'url': URL}, follow_redirects=True)

    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == SHOW_PAGE
    assert "Страница успешно добавлена" in response.text
    assert URL in response.text

    with get_test_db as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls")
            db_records = curs.fetchall()
    assert len(db_records) == 1
    assert db_records[0].id == 1
    assert db_records[0].name == URL
    assert db_records[0].created_at >= pre_test_time


def test_add_old_correct_url(get_test_db):
    URL = "http://www.mytest-13.com"

    pre_1st_time = datetime.utcnow()
    client = app.test_client()
    response = client.post(POST_PAGE, data={'url': URL}, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == SHOW_PAGE
    assert "Страница успешно добавлена" in response.text

    pre_2nd_time = datetime.utcnow()
    response = client.post(POST_PAGE, data={'url': URL}, follow_redirects=True)

    assert response.status_code == 422
    assert len(response.history) == 1
    assert response.request.path == SHOW_PAGE
    assert "Страница уже существует" in response.text
    assert URL in response.text

    with get_test_db as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls")
            db_records = curs.fetchall()
    assert len(db_records) == 1
    assert db_records[0].id == 1
    assert db_records[0].name == URL
    assert pre_1st_time <= db_records[0].created_at <= pre_2nd_time


@pytest.mark.parametrize("URL, error_message", [
    ("mytest-@13caiuh", "Некорректный URL"),
    ("", "URL обязателен"),
    (f"https://www.google.com/search?q={str(10**255)}",
        "URL превышает 255 символов"), ])
def test_add_incorrect_url(get_test_db, URL, error_message):
    client = app.test_client()
    response = client.post(POST_PAGE, data={'url': URL}, follow_redirects=True)

    assert response.status_code == 422
    assert response.request.path == GET_PAGE
    assert error_message in response.text
    assert URL in response.text

    with get_test_db as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls")
            db_records = curs.fetchall()
    assert len(db_records) == 0
