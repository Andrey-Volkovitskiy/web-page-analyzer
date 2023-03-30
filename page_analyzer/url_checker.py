import requests
from page_analyzer.language import txt
from page_analyzer import exceptions
from bs4 import BeautifulSoup


def check(url_name):
    '''Checks the url for status code, h1, title and etc.

    Agruments:
        url_name - url of the website of interest

    Returns:
        result - dict with status code, h1, title,
            description recieved from the website
        (or raise exception if something went wrong)
    '''
    result = {}

    try:
        r = requests.get(url_name)
        result['status_code'] = r.status_code
        if result['status_code'] != 200:
            raise exceptions.UrlCheckError(
                txt.MESSAGES['ERROR_DURING_CHECK'])

        r.encoding = r.apparent_encoding
        response_html = r.text
        soup = BeautifulSoup(response_html, 'html.parser')

        h1_tag = soup.h1
        result['h1'] = h1_tag.get_text() if h1_tag else None

        t_tag = soup.title
        result['title'] = t_tag.get_text() if t_tag else None

        d_tags = soup.find_all(is_description)
        result['description'] = d_tags[0]['content'] if d_tags else None

    except requests.exceptions.RequestException:
        raise exceptions.UrlCheckError(txt.MESSAGES['ERROR_DURING_CHECK'])

    return result


def is_description(tag):
    '''Checks if the tag is <meta name=description content=...

    Agruments:
        tag - html tag to explore

    Returns:
        True / False
    '''

    if tag.name == 'meta':
        return tag.get('name') == 'description' and tag.get('content')
