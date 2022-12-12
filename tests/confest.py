import pytest
import os

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

    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.config.from_object('config.config_module.ProductionConfig')
    else:
        app.config.from_object('config.config_module.DevelopmentConfig')
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture()
def client(app):
    yield app


@pytest.fixture()
def modify_g(app):
    # set g here
    g.test_user_01 = 'ayumisfan@gmail.com'
    g.test_user_02 = 'jordenchang02@gmail.com'
    g.test_motor_plate = 'DEV-613'
    g.test_motor_number = 'RF3AE0300KT006137'
    query = DataStoreConn().client().query(kind='User')
    query.add_filter("email", '=', g.test_user_01)
    g.user_entity = list(query.fetch())[0]


@pytest.fixture()
def mocked_login_required(mocker):
    """
    token驗證部分的mock，每個有登入需求的測試都應該要接
    """
    mock_blocklist = mocker.patch.object(auth, 'BlockListDAO')
    mock_blocklist.get_by_token.return_value = False

    mock_cipher = mocker.patch.object(auth, 'cipher')
    mock_cipher.decrypt.return_value = 'test'

    mock_jwt = mocker.patch.object(auth, 'jwt')
    mock_jwt.decode.return_value = {'sub': g.user_entity.key.id}
    mock_jwt.DecodeError = jwt.exceptions.DecodeError
    mock_jwt.ExpiredSignatureError = jwt.exceptions.ExpiredSignatureError