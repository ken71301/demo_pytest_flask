import pytest
import os
from factory import create_app
from flask import Flask, _request_ctx_stack, _app_ctx_stack, g, request
from flask.signals import got_request_exception
from datetime import datetime

"""
g與application context的壽命週期是同等的，即在同一request內會有效
舊寫法pytest在call client時為直接 return 故app context與g都不會存活到client.post的一行之後
要讓client.post完之後還能讓整個function留在app context內

請參照以下文件
https://flask.palletsprojects.com/en/2.1.x/appcontext/
https://flask.palletsprojects.com/en/2.1.x/reqcontext/
"""


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture()
def client(app):
    yield app


@pytest.fixture()
def global_param(app):
    # set g here
    pass
