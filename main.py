from flask import Flask, request, render_template


def create_app():
    main_app = Flask(__name__)
    return main_app


app = create_app()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 取得使用者輸入的帳號和密碼
        username = request.form['username']
        password = request.form['password']

        # 檢查帳號和密碼是否正確
        if check_credentials(username, password):
            return "登入成功"
        else:
            return "登入失敗"
    else:
        # 顯示登入表單
        return render_template('login.html')


# 檢查帳號和密碼的函數
def check_credentials(username, password):
    # 返回帳號和密碼是否正確
    return username == "admin" and password == "password"


if __name__ == '__main__':

    app.run('0.0.0.0', port=5000)
