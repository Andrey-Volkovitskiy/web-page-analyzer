from flask import (Flask,
                   request,
                   url_for,
                   flash,
                   redirect,
                   render_template,
                   get_flashed_messages)
from dotenv import load_dotenv
import os
from functools import wraps
from page_analyzer import model


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


def checking_db_connection(function):
    '''Decorates the routing function to check that connection
            to the database was successfully established.

    Returns:
        If connection to the database cannot be established,
            returns the code 500 and the page with corresponding message
    '''
    @wraps(function)
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)

        except model.DbConnecionError as e:
            flash(e.args[0], 'error')
            return code_500()

    return inner


def get_status_code(messages):
    '''Returns the status code depends on messages.

    Agruments:
        messages - flash messages

    Returns:
        http status code
    '''
    if "error" not in [category for category, _ in messages]:
        return 200
    else:
        return 422


@app.get('/')
def get_new():
    '''Routing to display the add website form.'''

    messages = get_flashed_messages(with_categories=True)
    try:
        old_url = request.form['url']
    except KeyError:
        old_url = ''

    return render_template(
        'index.html',
        messages=messages,
        old_url=old_url
    ), get_status_code(messages)


@app.post('/urls')
@checking_db_connection
def post_new():
    '''Routing to add new website in database.'''

    url = request.form['url']

    try:
        id = model.urls.add(url)
        flash("Страница успешно добавлена", "success")

    except model.IncorrectUrlName as e:
        flash(e.args[0], "error")
        return get_new()

    except model.UrlAlreadyExists as e:
        flash(e.args[0], "error")
        id = e.args[1]

    return redirect(url_for('show_url', id=id))


@app.get('/urls')
@checking_db_connection
def show_urls():
    '''Routing to display a list of all websites.'''

    url_list = model.urls.get_list_with_latest_check()
    url_list.sort(reverse=True, key=lambda x: x.url_created_at)

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'show_urls.html',
        messages=messages,
        url_list=url_list
    ), get_status_code(messages)


@app.get('/urls/<int:id>')
@checking_db_connection
def show_url(id):
    '''Routing to display information about a specific website.'''
    url = model.urls.find(id)

    if not url:
        return code_404()

    list_of_checks = model.checks.get_list(id)

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'show_url.html',
        messages=messages,
        url=url,
        checks=list_of_checks
    ), get_status_code(messages)


@app.post('/urls/<int:url_id>/checks')
@checking_db_connection
def check(url_id):
    '''Routing to check a website for SEO.'''
    try:
        model.checks.add(url_id=url_id)
        flash("Страница успешно проверена", "success")

    except (model.DbConsistanceError, model.UrlCheckError) as e:
        flash(e.args[0], "error")

    return redirect(url_for('show_url', id=url_id))


def code_404():
    '''Routing for Page Not Found.'''
    return render_template('404.html'), 404


def code_500():
    '''Routing for Internal Server Error.'''
    messages = get_flashed_messages(with_categories=True)
    return render_template('500.html', messages=messages), 500
