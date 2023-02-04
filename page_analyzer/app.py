from flask import (Flask,
                   request,
                   url_for,
                   flash,
                   redirect,
                   render_template,
                   get_flashed_messages)
from dotenv import load_dotenv
import os
from . import urls


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


@app.get('/urls/<int:id>')
def show_url(id):
    url = urls.find(id)
    if not url:
        return code_404()

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'show_url.html',
        messages=messages,
        url=url
    )


@app.get('/urls')   # проверить '/urls/
def show_urls():
    url_list = urls.get_list()

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'show_urls.html',
        messages=messages,
        url_list=url_list
    )


def code_404():
    return render_template('404.html'), 404
