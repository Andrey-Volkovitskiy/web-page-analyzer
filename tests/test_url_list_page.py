from page_analyzer.app import app
from datetime import datetime
from flask import url_for
import os
from bs4 import BeautifulSoup
import requests_mock
from tests import conftest


with app.test_request_context():
    CORRECT_URL = "http://www.gmail.com"
    INCORRECT_URL = "http://wrong.com"
    GET_PAGE = url_for('show_urls')
    POST_URL = url_for('post_new')
    POST_CHECK = url_for('check', url_id=1)


def test_basic_content(get_test_db):
    client = app.test_client()
    response = client.get(GET_PAGE)
    assert response.status_code == 200
    assert response.request.path == GET_PAGE
    assert "Сайты" in response.text

    soup = BeautifulSoup(response.data, 'html.parser')
    rows = soup.find_all('tr')
    assert len(rows) == 1


def test_missing_db_connection():
    conftest.missing_db_connection(GET_PAGE)


def test_add_to_list(get_test_db):
    pre_test_time = datetime.utcnow()

    client = app.test_client()
    client.post(POST_URL, data={'url': CORRECT_URL})
    client.post(POST_URL, data={'url': CORRECT_URL})
    client.post(POST_URL, data={'url': INCORRECT_URL})

    fixture_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 'fixtures/gmail.html'))
    with open(fixture_path, 'r') as f:
        HTML = f.read()

    with requests_mock.Mocker() as m:
        m.get(CORRECT_URL, text=HTML)
        m.status_code = 200
        client.post(POST_CHECK)

    response = client.get(GET_PAGE)
    assert response.status_code == 422
    assert response.request.path == GET_PAGE
    assert "Сайты" in response.text
    assert "Страница уже существует" in response.text

    soup = BeautifulSoup(response.data, 'html.parser')
    rows = soup.find_all('tr')
    assert len(rows) == 3

    row0 = rows[0].get_text()
    assert "ID" in row0
    assert "Имя" in row0
    assert "Последняя проверка" in row0
    assert "Код ответа" in row0

    row1 = rows[1].get_text()
    assert INCORRECT_URL in row1
    assert "200" not in row1
    assert pre_test_time.strftime("%Y-%m-%d") not in row1

    row2 = rows[2].get_text()
    assert CORRECT_URL in row2
    assert "200" in row2
    assert pre_test_time.strftime("%Y-%m-%d") in row2
