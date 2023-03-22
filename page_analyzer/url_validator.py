import validators
from urllib.parse import urlparse, urlunparse
from page_analyzer.language import txt
from page_analyzer import exceptions


def normalize(name):
    '''Checks if URL name is valid. If valid returns a normalized name.

    Arguments:
        name - URL name

    Returns:
        normalized URL name
        (or raise an excetpion if the name isn't valid)
    '''
    if len(name) == 0:
        raise exceptions.IncorrectUrlName(txt.MESSAGES['URL_CANT_BE_EMPTY'])

    elif len(name) > 255:
        raise exceptions.IncorrectUrlName(txt.MESSAGES['URL_TOO_LONG'])

    url_parts = urlparse(name, scheme='http')
    normalized_name = urlunparse((
        url_parts.scheme,
        url_parts.netloc or url_parts.path,
        '', '', '', ''))

    is_valid_url = validators.url(normalized_name, public=True)
    if not is_valid_url or normalized_name == '':
        raise exceptions.IncorrectUrlName(txt.MESSAGES['INCORRECT_URL'])

    return normalized_name
