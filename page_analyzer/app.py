from flask import (Flask,
                   request,
                   url_for,
                   flash,
                   redirect,
                   render_template,
                   get_flashed_messages)
from dotenv import load_dotenv
import os
from page_analyzer import urls, checks


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.get('/')
def get_new(messages=[], old_url=''):
    return render_template(
        'index.html',
        messages=messages,
        old_url=old_url
    )


@app.post('/')
def post_new():
    url = request.form['url']

    id, error = urls.add(url)
    if error:
        return get_new(
            messages=[('error', error)],
            old_url=url
        )

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=id))


@app.get('/urls')
def show_urls():
    url_list = urls.get_list_with_latest_check()
    url_list.sort(reverse=True, key=lambda x: x.url_created_at)

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'show_urls.html',
        messages=messages,
        url_list=url_list
    )


@app.get('/urls/<int:id>')
def show_url(id):
    url = urls.find(id)
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
    _, error = checks.add(url_id=url_id)

    if error:
        flash(error, 'error')
    else:
        flash("Страница успешно проверена", "success")

    return redirect(url_for('show_url', id=url_id))


def code_404():
    return render_template('404.html'), 404
