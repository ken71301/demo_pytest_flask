import requests
from flask import Blueprint, request, render_template, g, Response
import jwt


app = Blueprint('crawler', __name__)


@app.route('/mock_test', methods=['GET'])
def connect_mock():
    # try to connect to a website
    response = requests.get(f'https://example.com/users/me')

    print(type(response))
    print(response.json())

    return response.json()


@app.route('/side_effect_test', methods=['GET'])
def connect_side_effect():
    # try to connect to a website
    response_name = requests.get(f'https://example.com/users/me')
    name = response_name.json()

    response_gender = requests.get(f'https://example.com/users/me/gender')
    gender = response_gender.json()

    name.update(gender)
    return name

