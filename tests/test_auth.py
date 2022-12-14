from flask import g


def test_index(client, global_param):
    # 測試call index頁面的flow
    # 測試頁面是否輸出與內容是否符合預期
    # 預期回復status code 200
    response = client.get("/")

    assert response.status_code == 200
    assert b"Server is alive." in response.data


def test_login_page(client, global_param):
    # 測試get登入頁面功能是否正常
    # 預期回復status code 200

    response = client.get("/login")

    assert response.status_code == 200


def test_login(client, global_param):
    # 測試post登入功能
    # 於測試中可驗證g，可以看到測試中給的g變數
    # 預期回復status code 200
    payload = {"username": 'admin',
               "password": 'password'}

    # use data to deal with formdata
    response = client.post("/login", data=payload)

    assert response.status_code == 200
    assert "登入成功" in response.text
    assert g.current_user == 'admin'
    assert g.user_pwd == 'test'


def test_login2(client_return):
    # 測試若return test client，於call api結束後測試不會停留在flask的life cycle內，故測試看不懂g
    payload = {"username": 'admin',
               "password": 'password'}

    # use data to deal with formdata
    response = client_return.post("/login", data=payload)

    assert response.status_code == 200
    assert "登入成功" in response.text
    assert g.current_user == 'admin'


def test_login3(client_yield):
    # 測試yield test client的狀況下，於call api結束後仍停留在flask life cycle內，故測試看得懂g
    payload = {"username": 'admin',
               "password": 'password'}

    # use data to deal with formdata
    response = client_yield.post("/login", data=payload)

    assert response.status_code == 200
    assert "登入成功" in response.text
    assert g.current_user == 'admin'

