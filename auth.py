from flask import Blueprint, request, render_template, g

app = Blueprint('auth', __name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 簡單的登入實作，get時給登入頁的html，post時驗證輸入的帳號密碼

    if request.method == 'POST':
        # 取得使用者輸入的帳號和密碼
        username = request.form['username']
        password = request.form['password']

        # 檢查帳號和密碼是否正確
        if check_credentials(username, password):
            g.current_user = 'admin'
            return "登入成功"
        else:
            return "登入失敗"
    else:
        # 顯示登入表單
        return render_template('login.html')


@app.route('/')
def index():
    return 'Server is alive.'


# 檢查帳號和密碼的函數
def check_credentials(username, password):
    # 返回帳號和密碼是否正確
    return username == "admin" and password == "password"

