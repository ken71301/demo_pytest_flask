import requests
import pytest
from requests import get
from flask import g
import crawler


@pytest.mark.crawler
def test_mock_patch(mocker, client, global_param):
    """
    mocker.patch
    simple test 01
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'name': 'me'}

    mock_get = mocker.patch('requests.get')
    mock_get.return_value = mock_response

    response = client.get("/connect")

    assert response.status_code == 200
    assert response.json['name'] == 'me'


@pytest.mark.crawler
def test_mock_patch_is_global(mocker, client, global_param):
    """
    mocker.patch
    simple test 02
    """
    # here is ok
    test = requests.get("https://www.google.com.tw/")
    print(test)

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'name': 'me'}

    mock_get = mocker.patch('requests.get')
    mock_get.return_value = mock_response

    # here we got something...
    # patch is global,
    test = requests.get("https://www.google.com.tw/")
    print(test)

    # you can dodge it, but ugly
    # mock an object is global replace, bypass it by import other object,
    # but its very ugly, we recommend use patch.object
    test = get("https://www.google.com.tw/")
    print(test)

    response = client.get("/connect")

    assert response.json['name'] == 'me'


@pytest.mark.crawler
def test_mock_patch_object(mocker, client, global_param):
    """
    mocker.patch.object
    simple test
    """

    # here is ok
    test = requests.get("https://www.google.com.tw/")
    print(test)

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'name': 'me'}

    # patch.object replace a object (object-level)
    # in crawler.py, we do:
    # import requests, so
    mock_requests = mocker.patch.object(crawler, 'requests')
    mock_requests.get.return_value = mock_response

    # and ot os ok
    test = requests.get("https://www.google.com.tw/")
    print(test)

    response = client.get("/connect")

    assert response.json['name'] == 'me'
