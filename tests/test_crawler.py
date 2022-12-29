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
    講解mock.patch
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'name': 'me'}

    mock_get = mocker.patch('requests.get')
    mock_get.return_value = mock_response

    response = client.get("/mock_test")

    assert response.status_code == 200
    assert response.json['name'] == 'me'


@pytest.mark.crawler
def test_mock_patch_is_global(mocker, client, global_param):
    """
    mocker.patch
    simple test 02
    講解mock.patch的特性及缺點
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
    # patch is module level
    test = requests.get("https://www.google.com.tw/")
    print(test)

    # patch an object is module level, bypass it by import other object,
    # but its very ugly, we recommend use patch.object if needed
    test = get("https://www.google.com.tw/")
    print(test)

    response = client.get("/mock_test")

    assert response.json['name'] == 'me'


@pytest.mark.crawler
def test_mock_patch_object(mocker, client, global_param):
    """
    mocker.patch.object
    simple test
    講解patch.object與patch的不同
    講解在測試會經過多個檔案時如何讓mock侷限在單一檔案內
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

    response = client.get("/mock_test")

    assert response.json['name'] == 'me'


@pytest.mark.crawler
def test_mock_patch_object_side_effect(mocker, client, global_param):
    """
    預定講解side_effect
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'name': 'me'}

    mock_response_another = mocker.Mock()
    mock_response_another.status_code = 200
    mock_response_another.json.return_value = {'gender': 'male'}

    mock_requests = mocker.patch.object(crawler, 'requests')
    mock_requests.get.side_effect = [mock_response, mock_response_another]

    response = client.get("/side_effect_test")

    assert response.json == {'name': 'me', 'gender': 'male'}

