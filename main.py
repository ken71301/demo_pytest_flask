from factory import create_app

# 用flask的factory method跟blueprint建endpoint
app = create_app()


if __name__ == '__main__':

    app.run('0.0.0.0', port=5000)
