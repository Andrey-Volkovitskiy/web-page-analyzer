from flask import (Flask,
                   render_template,
                   make_response)
from dotenv import load_dotenv
import os
import json


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)


@app.get('/')
def index():
    resp = render_template('index.html')
    response = make_response(resp)
    encoded_list = json.dumps([])
    response.set_cookie('users', encoded_list)
    return response
