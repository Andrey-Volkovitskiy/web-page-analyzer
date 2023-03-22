from flask import (Flask,
                   request,
                   session,
                   url_for,
                   flash,
                   redirect,
                   render_template,
                   get_flashed_messages)
from dotenv import load_dotenv
import os
import page_analyzer.db as db
from page_analyzer import url_checker
from page_analyzer import url_validator
from page_analyzer.language import txt
from page_analyzer import exceptions
import secrets


load_dotenv(".env")

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or secrets.token_hex(16)


def get_status_code():
    '''Returns the status code depends on messages.

    Returns:
        http status code
    '''
    messages = get_flashed_messages(with_categories=True)
    if "error" not in [category for category, _ in messages]:
        return 200
    else:
        return 422


@app.get('/')
def get_new():
    '''Routing to display the add website form.'''

    old_url = session.pop('old_url', '')

    return render_template(
        'index.html',
        old_url=old_url,
        txt=txt.TEMPLATES
    ), get_status_code()


@app.post('/urls')
def post_new():
    '''Routing to add new website in database.'''

    url_name = request.form['url']

    try:
        normalized_name = url_validator.normalize(url_name)

    except exceptions.IncorrectUrlName as e:
        flash(e.args[0], "error")
        session['old_url'] = url_name
        return redirect(url_for('get_new'))

    try:
        id = db.urls.add(normalized_name)
        flash(txt.PAGE_ADDED_SUCCESSFULLY, "success")

    except exceptions.UrlAlreadyExists as e:
        message, existing_id = e.args[0], e.args[1]
        flash(message, "error")
        id = existing_id

    return redirect(url_for('show_url', id=id))


@app.get('/urls')
def show_urls():
    '''Routing to display a list of all websites.'''

    url_list = db.urls.get_list_with_latest_check()
    url_list.sort(reverse=True, key=lambda x: x.url_created_at)

    return render_template(
        'show_urls.html',
        url_list=url_list,
        txt=txt.TEMPLATES
    ), get_status_code()


@app.get('/urls/<int:id>')
def show_url(id):
    '''Routing to display information about a specific website.'''
    url = db.urls.find(id)

    if not url:
        return get_404()

    list_of_checks = db.checks.get_list(id)

    return render_template(
        'show_url.html',
        url=url,
        checks=list_of_checks,
        txt=txt.TEMPLATES
    ), get_status_code()


@app.post('/urls/<int:url_id>/checks')
def check(url_id):
    '''Routing to check a website for SEO.'''
    url = db.urls.find(url_id)

    check_result = None
    try:
        check_result = url_checker.check(url.name)
    except exceptions.UrlCheckError as e:
        flash(e.args[0], "error")

    if check_result:
        db.checks.add(url_id, check_result)
        flash(txt.PAGE_CHECKED_SUCCESSFULLY, "success")

    return redirect(url_for('show_url', id=url_id))


@app.errorhandler(exceptions.DbConnecionError)
def handle_DbConnecionError(e):
    flash(e.args[0], 'error')
    return get_500()


def get_404():
    '''Routing for Page Not Found.'''
    return render_template('404.html', txt=txt.TEMPLATES), 404


def get_500():
    '''Routing for Internal Server Error.'''
    return render_template(
        '500.html',
        txt=txt.TEMPLATES
    ), 500
