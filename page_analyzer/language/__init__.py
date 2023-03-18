import os

if os.getenv('LANGUAGE') == 'en':
    from page_analyzer.language import en as txt  # noqa: F401
else:
    from page_analyzer.language import ru as txt  # noqa: F401
