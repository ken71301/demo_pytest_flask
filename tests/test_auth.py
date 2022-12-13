from flask import g
import pytest
from datetime import datetime


def test_index(client, global_param):

    response = client.get("/")

    assert response.status_code == 200
    assert b"ok" in response.data


def test_login_page(client, global_param):

    response = client.get("/login")

    assert response.status_code == 200


def test_login(client, global_param):

    payload = {"username": 'admin',
               "password": 'password'}

    # use data to deal with formdata
    response = client.post("/login", data=payload)

    assert response.status_code == 200
    assert "登入成功" in response.text

