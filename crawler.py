import requests
from flask import Blueprint, request, render_template, g, Response


app = Blueprint('crawler', __name__)


@app.route('/connect', methods=['GET', 'POST'])
def connect():
    # try to connect to a website
    response = requests.get(f'https://example.com/users/me')

    print(type(response))
    print(response.json())

    return response.json()
