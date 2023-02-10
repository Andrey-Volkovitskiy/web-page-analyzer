from flask import (Flask,
                   request,
                   url_for,
                   flash,
                   redirect,
                   render_template,
                   get_flashed_messages)
from dotenv import load_dotenv
import os
from page_analyzer.model import urls, checks
from page_analyzer import model


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.get('/')
def get_new(messages=[], old_url=''):  # TODO удалить messages и old_url
    messages = messages or get_flashed_messages(with_categories=True)

    return render_template(
        'index.html',
        messages=messages,
        old_url=old_url
    )


@app.post('/')
def post_new():
    url = request.form['url']

    try:
        id = urls.add(url)

    except model.DbConnecionError as e:
        flash(e.args[0], 'error')
        return code_500()

    except model.IncorrectUrlName as e:
        flash(e.args[0], "error")
        return get_new(old_url=url)

    except model.UrlAlreadyExists as e:
        flash(e.args[0], "error")
        id = e.args[1]

    return redirect(url_for('show_url', id=id))


@app.get('/urls')
def show_urls():
    try:
        url_list = urls.get_list_with_latest_check()
        url_list.sort(reverse=True, key=lambda x: x.url_created_at)
    except model.DbConnecionError as e:
        flash(e.args[0], 'error')
        return code_500()

    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show_urls.html',
        messages=messages,
        url_list=url_list
    )


@app.get('/urls/<int:id>')
def show_url(id):
    try:
        url = urls.find(id)
    except model.DbConnecionError as e:
        flash(e.args[0], 'error')
        return code_500()

    if not url:
        return code_404()

    list_of_checks = checks.get_list(id)

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'show_url.html',
        messages=messages,
        url=url,
        checks=list_of_checks
    )


@app.post('/urls/<int:url_id>/checks')
def check(url_id):
    try:
        checks.add(url_id=url_id)
        flash("Страница успешно проверена", "success")

    except model.DbConnecionError as e:
        flash(e.args[0], 'error')
        return code_500()

    except (model.DbConsistanceError, model.UrlCheckError) as e:
        flash(e.args[0], "error")

    return redirect(url_for('show_url', id=url_id))


def code_404():
    return render_template('404.html'), 404


def code_500():
    messages = get_flashed_messages(with_categories=True)
    return render_template('500.html', messages=messages), 500
