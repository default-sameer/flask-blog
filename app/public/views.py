from flask import render_template, url_for, current_app
import requests
import json
from app import fa
from app.public import public


@public.route('/')
def index():
    return render_template('public/index.html', title='Home')
