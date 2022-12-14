import pytest
import os
from factory import create_app
from flask import Flask, _request_ctx_stack, _app_ctx_stack, g, request
from flask.signals import got_request_exception
from datetime import datetime

"""
g與application context的壽命週期是同等的，即在同一request內會有效
若pytest在call client時為直接return (見app_return)，app context與g都不會存活到client.post的一行之後
要讓client.post完之後還能讓整個function留在app context內，才能測試g


請參照以下文件
https://flask.palletsprojects.com/en/2.1.x/appcontext/
https://flask.palletsprojects.com/en/2.1.x/reqcontext/
"""


@pytest.fixture()
def app():
    app = create_app()
    # flask建議於測試時加入config
    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as test_client:
        # 手動打開 app context，讓整個測試都能用g
        with app.app_context():
            # yield讓測試結束前，測試本身都能停留在request行為內
            yield test_client


@pytest.fixture()
def client(app):
    return app


@pytest.fixture()
def global_param(app):
    # 在手動打開app context的狀況下，整個測試都能被flask g所覆蓋，可以提高測試的便利程度
    g.user_pwd = 'test'


@pytest.fixture()
def app_return():
    # 示範不yield，return test client的flow
    # 只能測試response本身，沒有辦法看到request流程內部的狀況(g, signal之類)
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as test_client:
        return test_client


@pytest.fixture()
def client_return(app_return):
    return app_return


@pytest.fixture()
def app_yield():
    # 示範不打開app context，可以在call client後測試g，但無法事先設定
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as test_client:
        yield test_client


@pytest.fixture()
def client_yield(app_yield):
    return app_yield


@pytest.fixture()
def global_param_no_context(app_yield):
    # 示範於測試中設定g失敗
    g.user_pwd = 'test'

