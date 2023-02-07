import requests


def check(url_name):
    '''Checks a url for status code, h1, title and etc.

    Agruments:
        url_name - url of the website of interest

    Returns:
        result - dict with status code, h1, title, description
            recieved from the website
        error message - if somethig went wrong
    '''
    result = {}
    error = None

    try:
        r = requests.get(url_name)
        result['status_code'] = r.status_code
        result['h1'] = None
        result['title'] = None
        result['description'] = None
    except requests.exceptions.RequestException:
        error = "Произошла ошибка при проверке"

    return (result, error)
